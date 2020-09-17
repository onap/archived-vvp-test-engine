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
from onap_client.resource import Resource
from onap_client.client.clients import get_client as Client
from onap_client.exceptions import (
    ModuleModelNameNotFound,
    NoArtifactFoundInModel,
)
from onap_client import so
from onap_client import sdnc
from onap_client.util import utility


class ModuleInstance(Resource):
    resource_name = "MODULE_INSTANCE"
    spec = {
        "module_instance_name": {"type": str, "required": True},
        "vnf_instance_name": {"type": str, "required": True},
        "service_instance_name": {"type": str, "required": True},
        "requestor_id": {"type": str, "required": False, "default": "cs0008"},
        "heat_template_name": {"type": str, "required": True},
        "preload_path": {"type": str, "required": True},
        "tenant_name": {"type": str, "required": True},
        "cloud_owner": {"type": str, "required": True},
        "cloud_region": {"type": str, "required": True},
        "api_type": {"type": str, "required": False, "default": "GR_API"},
        "volume_group_name": {"type": str, "required": False},
    }

    def _create(self, instance_input):
        tenant_id = so.service_instance.get_tenant_id(
            instance_input.get("cloud_region"),
            instance_input.get("cloud_owner"),
            instance_input.get("tenant_name"),
            oc=self.oc
        )
        instance_input["tenant_id"] = tenant_id

        service_instance = so.service_instance.get_service_instance(
            instance_input.get("service_instance_name"), oc=self.oc
        )
        service_instance_id = service_instance.get("service-instance-id")
        model_information = (
            service_instance.get("service-data")
            .get("service-information")
            .get("onap-model-information")
        )
        service_model_invariant_id = model_information["model-invariant-uuid"]
        service_model_version_id = model_information["model-uuid"]
        service_model_version = model_information["model-version"]
        service_model_name = model_information["model-name"]

        vnf_instance = so.service_instance.get_vnf_instance(
            service_instance, instance_input.get("vnf_instance_name")
        )

        vnf_model_information = vnf_instance.get("vnf-data").get("vnf-information")
        vnf_instance_id = vnf_model_information.get("vnf-id")
        vnf_model_name = vnf_model_information.get("onap-model-information").get(
            "model-name"
        )
        vnf_model_invariant_id = vnf_model_information.get(
            "onap-model-information"
        ).get("model-invariant-uuid")
        vnf_model_version_id = vnf_model_information.get("onap-model-information").get(
            "model-uuid"
        )
        vnf_model_customization_id = vnf_model_information.get(
            "onap-model-information"
        ).get("model-customization-uuid")
        vnf_model_version = vnf_model_information.get("onap-model-information").get(
            "model-version"
        )

        vnf_model = so.vnf_instance.get_vnf_model_component(
            service_model_name, vnf_model_name, oc=self.oc
        )

        module_model = get_module_model(
            vnf_model, instance_input.get("heat_template_name")
        )
        model_invariant_id = module_model.get("invariantUUID")
        model_version_id = module_model.get("groupUUID")
        model_customization_id = module_model.get("customizationUUID")
        model_name = module_model.get("groupName")
        model_version = module_model.get("version")

        volume_group = module_uses_volume_group(module_model) and instance_input.get("volume_group_name")

        instance_input["model_invariant_id"] = model_invariant_id
        instance_input["model_version_id"] = model_version_id
        instance_input["model_name"] = model_name
        instance_input["model_version"] = model_version
        instance_input["model_customization_id"] = model_customization_id
        instance_input["service_instance_id"] = service_instance_id
        instance_input["service_model_name"] = service_model_name
        instance_input["service_model_invariant_id"] = service_model_invariant_id
        instance_input["service_model_version"] = service_model_version
        instance_input["service_model_version_id"] = service_model_version_id
        instance_input["vnf_instance_id"] = vnf_instance_id
        instance_input["vnf_model_name"] = vnf_model_name
        instance_input["vnf_model_invariant_id"] = vnf_model_invariant_id
        instance_input["vnf_model_version_id"] = vnf_model_version_id
        instance_input["vnf_model_version"] = vnf_model_version
        instance_input["vnf_model_customization_id"] = vnf_model_customization_id

        return create_module_instance(instance_input, volume_group=volume_group, oc=self.oc)

    def _delete(self, instance_input):
        if instance_input.get("volume_group_name"):
            request = delete_volume_module_instance(
                instance_input.get("service_instance_name"),
                instance_input.get("vnf_instance_name"),
                instance_input.get("volume_group_name"),
                instance_input.get("api_type"),
                oc=self.oc,
            )
            request_id = request.get("requestReferences", {}).get(
                "requestId"
            )
            so.service_instance.poll_request(request_id, oc=self.oc)

        request = delete_module_instance(
            instance_input.get("service_instance_name"),
            instance_input.get("vnf_instance_name"),
            instance_input.get("module_instance_name"),
            instance_input.get("api_type"),
            oc=self.oc,
        )
        request_id = request.get("requestReferences", {}).get(
            "requestId"
        )
        so.service_instance.poll_request(request_id, oc=self.oc)


def create_module_instance(instance_input, volume_group=False, oc=None):
    if not oc:
        oc = Client()

    preload = sdnc.preload.Preload(
        preload_path=instance_input.get("preload_path"),
        vnf_instance_name=instance_input.get("vnf_instance_name"),
        service_instance_name=instance_input.get("service_instance_name"),
        module_instance_name=instance_input.get("module_instance_name"),
        heat_template_name=instance_input.get("heat_template_name"),
        api_type=instance_input.get("api_type"),
        oc=oc
    )
    preload.create()

    headers = {"X-TransactionId": str(uuid.uuid4())}

    if volume_group:
        volume_instance = oc.so.service_instantiation.create_volume_module_instance(
            volume_module_instance_name=instance_input.get("volume_group_name"),
            **instance_input,
            **headers
        )
        request_id = volume_instance.response_data.get("requestReferences", {}).get(
            "requestId"
        )
        so.service_instance.poll_request(request_id, oc=oc)

    module_instance = oc.so.service_instantiation.create_module_instance(
        **instance_input, **headers
    )

    request_id = module_instance.response_data.get("requestReferences", {}).get(
        "requestId"
    )

    instance_input["request_info"] = so.service_instance.poll_request(request_id, oc=oc)

    return instance_input


@utility
def delete_module_instance(service_instance_name, vnf_instance_name, module_instance_name, api_type="GR_API", oc=None):
    """Delete a Module Instance from SO"""
    if not oc:
        oc = Client()

    si = so.service_instance.get_service_instance(service_instance_name, oc=oc)
    vnfi = so.service_instance.get_vnf_instance(si, vnf_instance_name)
    modulei = so.service_instance.get_module_instance(vnfi, module_instance_name)

    si_id = si.get("service-instance-id")
    vnfi_id = vnfi.get("vnf-id")
    module_id = modulei.get("vf-module-id")
    module_invariant_id = modulei.get("vf-module-data").get("vf-module-topology").get("onap-model-information").get("model-invariant-uuid")
    module_version = modulei.get("vf-module-data").get("vf-module-topology").get("onap-model-information").get("model-version")
    module_name = modulei.get("vf-module-data").get("vf-module-topology").get("onap-model-information").get("model-name")
    tenant_id = modulei.get("vf-module-data").get("vf-module-request-input").get("tenant")
    cloud_owner = modulei.get("vf-module-data").get("vf-module-request-input").get("cloud-owner")
    cloud_region = modulei.get("vf-module-data").get("vf-module-request-input").get("aic-cloud-region")

    return oc.so.service_instantiation.delete_module_instance(
        module_invariant_id=module_invariant_id,
        module_name=module_name,
        module_version=module_version,
        cloud_region=cloud_region,
        cloud_owner=cloud_owner,
        tenant_id=tenant_id,
        vnf_instance_id=vnfi_id,
        service_instance_id=si_id,
        vf_module_id=module_id,
        api_type=api_type
    ).response_data


@utility
def delete_volume_module_instance(service_instance_name, vnf_instance_name, volume_module_name, api_type="GR_API", oc=None):
    """Delete a Module Instance from SO"""
    if not oc:
        oc = Client()

    si = so.service_instance.get_service_instance(service_instance_name, oc=oc)
    vnfi = so.service_instance.get_vnf_instance(si, vnf_instance_name)

    vnf_model_information = vnfi.get("vnf-data").get("vnf-information")
    service_model_information = (
        si.get("service-data")
        .get("service-information")
        .get("onap-model-information")
    )
    service_model_name = service_model_information["model-name"]
    vnf_model_name = vnf_model_information.get("onap-model-information").get(
        "model-name"
    )

    si_id = si.get("service-instance-id")
    vnfi_id = vnfi.get("vnf-id")

    tenant_id = vnfi.get("vnf-data").get("vnf-request-input").get("tenant")
    cloud_owner = vnfi.get("vnf-data").get("vnf-request-input").get("cloud-owner")
    cloud_region = vnfi.get("vnf-data").get("vnf-request-input").get("aic-cloud-region")

    volume_group_instance = get_volume_group_instance(volume_module_name, cloud_owner, cloud_region, oc=oc)
    volume_customization_id = volume_group_instance.get("model-customization-id")
    vnf_component = so.vnf_instance.get_vnf_model_component(
        service_model_name, vnf_model_name, oc=oc
    )
    volume_group_component = get_volume_group_from_vnf_model(vnf_component, volume_customization_id)

    return oc.so.service_instantiation.delete_volume_module_instance(
        volume_module_id=volume_group_instance.get("volume-group-id"),
        module_invariant_id=volume_group_component.get("invariantUUID"),
        module_name=volume_group_component.get("groupName"),
        module_version=volume_group_component.get("version"),
        cloud_region=cloud_region,
        cloud_owner=cloud_owner,
        tenant_id=tenant_id,
        vnf_instance_id=vnfi_id,
        service_instance_id=si_id,
        api_type=api_type
    ).response_data


def module_uses_volume_group(module_model):
    for prop in module_model.get("properties"):
        if prop.get("name", "") == "volume_group" and prop.get("value") == "true":
            return True
    return False


def get_volume_group_instance(volume_group_name, cloud_owner, cloud_region, oc=None):
    if not oc:
        oc = Client()

    volume_group_list = oc.aai.cloud_infrastructure.get_volume_groups(
        cloud_owner=cloud_owner,
        cloud_region=cloud_region
    ).response_data

    for volume_group in volume_group_list.get("volume-group", []):
        if volume_group.get("volume-group-name") == volume_group_name:
            return volume_group

    return {}


def get_volume_group_from_vnf_model(vnf_component, volume_group_customization_id):
    for group_instance in vnf_component.get("groupInstances", []):
        if group_instance.get("customizationUUID") == volume_group_customization_id:
            return group_instance
    return {}


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
