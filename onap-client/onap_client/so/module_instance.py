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
from onap_client.exceptions import ServiceInstanceNotFound, VNFInstanceNotFound, ModuleInstanceNotFound
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
    }

    def _create(self, instance_input):
        tenant_id = so.service_instance.get_tenant_id(
            instance_input.get("cloud_region"),
            instance_input.get("cloud_owner"),
            instance_input.get("tenant_name")
        )
        instance_input["tenant_id"] = tenant_id

        service_instance = so.vnf_instance.get_service_instance(
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
        service_model_invariant_id = model_information["model-invariant-uuid"]
        service_model_version_id = model_information["model-uuid"]
        service_model_version = model_information["model-version"]
        service_model_name = model_information["model-name"]

        vnf_instance = so.vnf_instance.get_vnf_instance(
            service_instance, instance_input.get("vnf_instance_name")
        )
        if not vnf_instance:
            raise VNFInstanceNotFound(
                "No vnf instance found for {}".format(
                    instance_input.get("vnf_instance_name")
                )
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
            service_model_name, vnf_model_name
        )

        module_model = so.vnf_instance.get_module_model(
            vnf_model, instance_input.get("heat_template_name")
        )
        model_invariant_id = module_model.get("invariantUUID")
        model_version_id = module_model.get("groupUUID")
        model_customization_id = module_model.get("customizationUUID")
        model_name = module_model.get("groupName")
        model_version = module_model.get("version")

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

        return create_module_instance(instance_input)


def create_module_instance(instance_input):
    oc = Client()

    preload = sdnc.preload.Preload(
        preload_path=instance_input.get("preload_path"),
        vnf_instance_name=instance_input.get("vnf_instance_name"),
        service_instance_name=instance_input.get("service_instance_name"),
        module_instance_name=instance_input.get("module_instance_name"),
        heat_template_name=instance_input.get("heat_template_name"),
        api_type=instance_input.get("api_type")
    )
    preload.create()

    headers = {"X-TransactionId": str(uuid.uuid4())}
    module_instance = oc.so.service_instantiation.create_module_instance(
        **instance_input, **headers
    )

    request_id = module_instance.response_data.get("requestReferences", {}).get(
        "requestId"
    )

    instance_input["request_info"] = so.service_instance.poll_request(request_id)

    return instance_input


@utility
def delete_module_instance(service_instance_name, vnf_instance_name, module_instance_name, api_type="GR_API"):
    """Delete a Module Instance from SO"""
    oc = Client()

    si = so.service_instance.get_service_instance(service_instance_name)
    si_id = si.get("service-instance-id")
    for vnfi in si.get("service-data", {}).get("vnfs", {}).get("vnf", []):
        vnfi_id = vnfi.get("vnf-id")
        if vnfi.get("vnf-data", {}).get("vnf-request-input", {}).get("vnf-name") == vnf_instance_name:
            for modulei in vnfi.get("vnf-data").get("vf-modules", {}).get("vf-module", []):
                if modulei.get("vf-module-data", {}).get("vf-module-request-input", {}).get("vf-module-name") == module_instance_name:
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

    raise ModuleInstanceNotFound("Module Instance was not found: {} {} {}".format(service_instance_name, vnf_instance_name, module_instance_name))
