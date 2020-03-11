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

import json
import tempfile

from onap_client.resource import Resource
from onap_client.client.clients import Client as SDNCClient
from onap_client.exceptions import ServiceInstanceNotFound, VNFInstanceNotFound
from onap_client import so
from onap_client.config import LOG as logger

oc = SDNCClient()
sdnc_client = oc.sdnc


class Preload(Resource):
    resource_name = "PRELOAD"
    spec = {
        "api_type": {"type": str, "required": True},
        "preload_path": {"type": str, "required": True},
        "service_instance_name": {"type": str, "required": True},
        "vnf_instance_name": {"type": str, "required": True},
        "module_instance_name": {"type": str, "required": True},
        "heat_template_name": {"type": str, "required": True},
    }

    def __init__(
        self,
        preload_path,
        vnf_instance_name,
        service_instance_name,
        module_instance_name,
        heat_template_name,
        api_type,
    ):
        instance_input = {}

        instance_input["preload_path"] = preload_path
        instance_input["vnf_instance_name"] = vnf_instance_name
        instance_input["service_instance_name"] = service_instance_name
        instance_input["module_instance_name"] = module_instance_name
        instance_input["heat_template_name"] = heat_template_name
        instance_input["api_type"] = api_type

        super().__init__(instance_input)

    def _create(self, instance_input):
        service_instance = so.vnf_instance.get_service_instance(
            instance_input.get("service_instance_name")
        )
        if not service_instance:
            raise ServiceInstanceNotFound(
                "No service instance found for {}".format(
                    instance_input.get("service_instance_name")
                )
            )

        vnf_instance = so.vnf_instance.get_vnf_instance(
            service_instance, instance_input.get("vnf_instance_name")
        )
        if not vnf_instance:
            raise VNFInstanceNotFound(
                "No vnf instance found for {}".format(
                    instance_input.get("vnf_instance_name")
                )
            )

        service_model_information = (
            service_instance.get("service-data")
            .get("service-information")
            .get("onap-model-information")
        )
        service_model_name = service_model_information["model-name"]
        vnf_model_information = (
            vnf_instance.get("vnf-data")
            .get("vnf-information")
            .get("onap-model-information")
        )
        vnf_model_name = vnf_model_information["model-name"]

        vnf_component = so.vnf_instance.get_vnf_model_component(
            service_model_name, vnf_model_name
        )
        module_model = so.vnf_instance.get_module_model(
            vnf_component, instance_input.get("heat_template_name")
        )

        preload_path = update_preload_with_instance(
            instance_input.get("preload_path"),
            instance_input.get("api_type"),
            "{}/{} 0".format(service_model_name, vnf_model_name),
            instance_input.get("vnf_instance_name"),
            instance_input.get("module_instance_name"),
            module_model.get("groupName"),
        )

        logger.info("Created preload {}".format(preload_path))

        create_preload(preload_path, instance_input.get("api_type"))

        return instance_input

    def _post_create(self):
        pass

    def _submit(self):
        pass


def create_preload(preload_path, api_type):
    if api_type == "GR_API":
        sdnc_client.operations.gr_api_preload(preload_path=preload_path)
    elif api_type == "VNF_API":
        sdnc_client.operations.vnf_api_preload(preload_path=preload_path)


def update_preload_with_instance(
    preload_path,
    api_type,
    vnf_type,
    vnf_instance_name,
    module_instance_name,
    module_model_name,
):
    with open(preload_path, "r") as f:
        preload_data = json.loads(f.read())

    if api_type == "GR_API":
        data = {"vnf-name": vnf_instance_name, "vnf-type": vnf_type}
        preload_data["input"]["preload-vf-module-topology-information"][
            "vnf-topology-identifier-structure"
        ] = data
        data = {
            "vf-module-type": module_model_name,
            "vf-module-name": module_instance_name,
        }
        preload_data["input"]["preload-vf-module-topology-information"][
            "vf-module-topology"
        ]["vf-module-topology-identifier"] = data
    elif api_type == "VNF_API":
        data = {
            "vnf-name": module_instance_name,
            "vnf-type": module_model_name,
            "generic-vnf-type": vnf_type,
            "generic-vnf-name": vnf_instance_name,
        }
        preload_data["input"]["vnf-topology-information"][
            "vnf-topology-identifier"
        ] = data

    filename = ""
    with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as f:
        filename = f.name
        json.dump(preload_data, f, indent=4)

    return filename
