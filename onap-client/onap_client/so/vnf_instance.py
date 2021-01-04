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
from onap_client.client.clients import get_client as Client
from onap_client.exceptions import VNFComponentNotFound
from onap_client import sdc
from onap_client import so
from onap_client.util import utility


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

    def _create(self, instance_input):
        tenant_id = so.service_instance.get_tenant_id(
            instance_input.get("cloud_region"),
            instance_input.get("cloud_owner"),
            instance_input.get("tenant_name"),
            oc=self.oc
        )
        instance_input["tenant_id"] = tenant_id

        service_instance = so.service_instance.get_service_instance(
            instance_input.get("service_instance_name"),
            oc=self.oc
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
            service_model_name, instance_input.get("model_name"), oc=self.oc
        )
        if not vnf_component:
            raise VNFComponentNotFound(
                "No component found for {}".format(instance_input.get("model_name"))
            )
        vnf_model_customization_id = vnf_component["customizationUUID"]
        vnf_model_version_id = vnf_component["actualComponentUid"]
        vnf_model_version = vnf_component["componentVersion"]

        vnf_model = self.oc.sdc.vnf.get_catalog_resource(
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

        return create_vnf_instance(instance_input, oc=self.oc)

    def _delete(self, instance_input):
        request = delete_vnf_instance(
            instance_input.get("service_instance_name"),
            instance_input.get("vnf_instance_name"),
            instance_input.get("api_type"),
            oc=self.oc
        )
        request_id = request.get("requestReferences", {}).get(
            "requestId"
        )
        so.service_instance.poll_request(request_id, oc=self.oc)


def get_vnf_model_component(service_model_name, vnf_model_name, oc=None):
    if not oc:
        oc = Client()

    catalog_service_id, catalog_service = sdc.service.get_service_id(service_model_name, oc=oc)

    service_model = oc.sdc.service.get_sdc_service(
        catalog_service_id=catalog_service_id
    ).response_data

    for component in service_model.get("componentInstances", []):
        if component["componentName"] == vnf_model_name:
            return component
    return None


def create_vnf_instance(instance_input, oc=None):
    if not oc:
        oc = Client()

    headers = {"X-TransactionId": str(uuid.uuid4())}
    vnf_instance = oc.so.service_instantiation.create_vnf_instance(
        **instance_input, **headers
    )

    request_id = vnf_instance.response_data.get("requestReferences", {}).get(
        "requestId"
    )

    instance_input["request_info"] = so.service_instance.poll_request(request_id, oc=oc)

    return instance_input


@utility
def delete_vnf_instance(service_instance_name, vnf_instance_name, api_type="GR_API", oc=None):
    """Delete a VNF Instance from SO"""
    if not oc:
        oc = Client()

    si = so.service_instance.get_service_instance(service_instance_name, oc=oc)
    vnfi = so.service_instance.get_vnf_instance(si, vnf_instance_name)

    si_id = si.get("service-instance-id")
    vnfi_id = vnfi.get("vnf-id")
    invariant_id = vnfi.get("vnf-data").get("vnf-information").get("onap-model-information").get("model-invariant-uuid")
    vnf_version = vnfi.get("vnf-data").get("vnf-information").get("onap-model-information").get("model-version")
    tenant_id = vnfi.get("vnf-data").get("vnf-request-input").get("tenant")
    cloud_owner = vnfi.get("vnf-data").get("vnf-request-input").get("cloud-owner")
    cloud_region = vnfi.get("vnf-data").get("vnf-request-input").get("aic-cloud-region")

    return oc.so.service_instantiation.delete_vnf_instance(
        vnf_invariant_id=invariant_id,
        vnf_version=vnf_version,
        vnf_name=vnf_instance_name,
        cloud_region=cloud_region,
        cloud_owner=cloud_owner,
        tenant_id=tenant_id,
        vnf_instance_id=vnfi_id,
        service_instance_id=si_id,
        api_type=api_type,
    ).response_data
