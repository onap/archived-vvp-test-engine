# -*- coding: utf8 -*-
# ============LICENSE_START=======================================================
# org.onap.vvp/validation-scripts
# ===================================================================
# Copyright © 2020 AT&T Intellectual Property. All rights reserved.
# ===================================================================
#
# Unless otherwise specified, all software contained herein is licensed
# under the Apache License, Version 2.0 (the "License");
# you may not use this software except in compliance with the License.
# You may obtain a copy of the License at
#
#             http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#
# Unless otherwise specified, all documentation contained herein is licensed
# under the Creative Commons License, Attribution 4.0 Intl. (the "License");
# you may not use this documentation except in compliance with the License.
# You may obtain a copy of the License at
#
#             https://creativecommons.org/licenses/by/4.0/
#
# Unless required by applicable law or agreed to in writing, documentation
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ============LICENSE_END============================================

import uuid

from onap_client.lib import generate_dummy_string
from onap_client.resource import Resource
from onap_client.client.clients import Client as SOClient
from onap_client.exceptions import (
    ServiceInstanceNotFound,
    VNFComponentNotFound,
    ModuleModelNameNotFound,
    NoArtifactFoundInModel,
)
from onap_client import sdc
from onap_client import so


oc = SOClient()
so_client = oc.so
sdc_client = oc.sdc
sdnc_client = oc.sdnc


class VNFInstance(Resource):
    resource_name = "VNF_INSTANCE"
    spec = {
        "vnf_instance_name": {
            "type": str,
            "required": False,
            "default": generate_dummy_string("VNF_"),
        },
        "service_instance_name": {"type": str, "required": True},
        "requestor_id": {"type": str, "required": False, "default": "cs0008"},
        "model_name": {"type": str, "required": True},
        "tenant_name": {"type": str, "required": True},
        "cloud_owner": {"type": str, "required": True},
        "cloud_region": {"type": str, "required": True},
        "api_type": {"type": str, "required": False, "default": "GR_API"},
        "platform": {"type": str, "required": True},
        "line_of_business": {"type": str, "required": True},
    }

    def __init__(
        self,
        vnf_instance_name,
        service_instance_name,
        requestor_id,
        model_name,
        tenant_name,
        cloud_owner,
        cloud_region,
        api_type,
        platform,
        line_of_business,
    ):
        instance_input = {}

        tenant_id = so.service_instance.get_tenant_id(cloud_region, cloud_owner, tenant_name)

        instance_input["vnf_instance_name"] = vnf_instance_name
        instance_input["service_instance_name"] = service_instance_name
        instance_input["requestor_id"] = requestor_id
        instance_input["model_name"] = model_name
        instance_input["tenant_id"] = tenant_id
        instance_input["cloud_owner"] = cloud_owner
        instance_input["cloud_region"] = cloud_region
        instance_input["api_type"] = api_type
        instance_input["platform"] = platform
        instance_input["line_of_business"] = line_of_business

        super().__init__(instance_input)

    def _create(self, instance_input):
        service_instance = get_service_instance(
            instance_input.get("service_instance_name")
        )
        if not service_instance:
            raise ServiceInstanceNotFound(
                "No service instance found for {}".format(
                    instance_input.get("service_instance_name")
                )
            )
        service_instance_id = service_instance.get("service-instance-id")
        model_information = (
            service_instance.get("service-data")
            .get("service-information")
            .get("onap-model-information")
        )
        service_invariant_id = model_information["model-invariant-uuid"]
        service_model_id = model_information["model-uuid"]
        service_model_version = model_information["model-version"]
        service_model_name = model_information["model-name"]

        vnf_component = get_vnf_model_component(
            service_model_name, instance_input.get("model_name")
        )
        if not vnf_component:
            raise VNFComponentNotFound(
                "No component found for {}".format(instance_input.get("model_name"))
            )
        vnf_model_customization_id = vnf_component["customizationUUID"]
        vnf_model_version_id = vnf_component["actualComponentUid"]
        vnf_model_version = vnf_component["componentVersion"]

        vnf_model = sdc_client.vnf.get_catalog_resource(
            catalog_resource_id=vnf_model_version_id,
        ).response_data
        vnf_model_invariant_id = vnf_model["invariantUUID"]

        instance_input["model_invariant_id"] = vnf_model_invariant_id
        instance_input["model_version_id"] = vnf_model_version_id
        instance_input["model_customization_id"] = vnf_model_customization_id
        instance_input["model_version"] = vnf_model_version
        instance_input["service_model_name"] = service_model_name
        instance_input["service_model_invariant_id"] = service_invariant_id
        instance_input["service_model_version"] = service_model_version
        instance_input["service_model_version_id"] = service_model_id
        instance_input["service_instance_id"] = service_instance_id

        return create_vnf_instance(instance_input)

    def _post_create(self):
        pass

    def _submit(self):
        pass


def get_vnf_model_component(service_model_name, vnf_model_name):
    service_model = sdc_client.service.get_sdc_service(
        catalog_service_id=sdc.service.get_service_id(service_model_name)
    ).response_data

    for component in service_model.get("componentInstances", []):
        if component["componentName"] == vnf_model_name:
            return component
    return None


def get_service_instance(service_instance_name):
    service_instances = sdnc_client.config.get_service_instances().response_data
    for si in service_instances.get("services", {}).get("service", []):
        si_name = (
            si.get("service-data", {})
            .get("service-request-input", {})
            .get("service-instance-name")
        )
        if si_name == service_instance_name:
            return si
    return None


def get_module_model(vnf_model, heat_template_name):
    artifact_uuid = None
    deployment_artifacts = vnf_model.get("deploymentArtifacts", {})
    for artifact_name, artifact_data in deployment_artifacts.items():
        if artifact_data.get("artifactName") == heat_template_name:
            artifact_uuid = artifact_data.get("artifactUUID")

    if not artifact_uuid:
        raise NoArtifactFoundInModel(
            "Heat Template {} was not found in service model".format(heat_template_name)
        )

    group_instances = vnf_model.get("groupInstances", [])
    for instance in group_instances:
        if artifact_uuid in instance.get("artifactsUuid", []):
            # return instance.get("groupName")
            return instance

    raise ModuleModelNameNotFound(
        "Module Model Name for {} was not found in service model".format(
            heat_template_name
        )
    )


def get_vnf_instance(service_instance, vnf_instance_name):
    for vnf_instance in (
        service_instance.get("service-data", {}).get("vnfs", {}).get("vnf", [])
    ):
        vi_name = (
            vnf_instance.get("vnf-data", {}).get("vnf-information", {}).get("vnf-name")
        )
        if vi_name == vnf_instance_name:
            return vnf_instance
    return None


def create_vnf_instance(instance_input):
    headers = {"X-TransactionId": str(uuid.uuid4())}
    vnf_instance = so_client.service_instantiation.create_vnf_instance(
        **instance_input, **headers
    )

    request_id = vnf_instance.response_data.get("requestReferences", {}).get(
        "requestId"
    )

    instance_input["request_info"] = so.service_instance.poll_request(request_id)

    return instance_input
