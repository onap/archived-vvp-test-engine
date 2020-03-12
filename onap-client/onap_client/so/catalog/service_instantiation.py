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
from functools import partial

from onap_client import so
from onap_client import config
from onap_client.so.client import SOClient

PAYLOADS_DIR = config.PAYLOADS_DIR
so_properties = so.SO_PROPERTIES
application_id = config.APPLICATION_ID


class ServiceInstantiationClient(SOClient):
    @property
    def catalog_resources(self):
        return CATALOG_RESOURCES

    @property
    def namespace(self):
        return "service_instantiation"


CATALOG_RESOURCES = {
    "CREATE_SERVICE_INSTANCE": {
        "verb": "POST",
        "description": "Creates a Service Instance from the service catalog",
        "uri": partial(
            "{endpoint}{service_path}".format,
            endpoint=so_properties.SO_ENDPOINT,
            service_path=so_properties.SO_SERVICE_INSTANCE_PATH,
        ),
        "payload": "{}/so_service_instance.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "service_instance_name",
            "requestor_id",
            "model_invariant_id",
            "model_version_id",
            "model_name",
            "model_version",
            "tenant_id",
            "cloud_owner",
            "cloud_region",
            "api_type",
            "service_type",
            "customer_id",
            "project_name",
            "owning_entity_id",
        ],
        "header-parameters": ["X-TransactionId"],
        "success_code": 202,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            # "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (so_properties.SO_USERNAME, so_properties.SO_PASSWORD),
    },
    "DELETE_SERVICE_INSTANCE": {
        "verb": "DELETE",
        "description": "Deletes a VNF Instance.",
        "uri": partial(
            "{endpoint}{service_path}/{service_instance_id}".format,
            endpoint=so_properties.SO_ENDPOINT,
            service_path=so_properties.SO_SERVICE_INSTANCE_PATH,
        ),
        "uri-parameters": ["service_instance_id"],
        "payload": "{}/so_delete_service.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "service_invariant_id",
            "service_name",
            "service_version",
            "api_type",
        ],
        "header-parameters": ["X-TransactionId"],
        "success_code": 202,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            # "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (so_properties.SO_USERNAME, so_properties.SO_PASSWORD),
    },
    "CREATE_VNF_INSTANCE": {
        "verb": "POST",
        "description": "Creates a VNF Instance.",
        "uri": partial(
            "{endpoint}{service_path}/{service_instance_id}/vnfs".format,
            endpoint=so_properties.SO_ENDPOINT,
            service_path=so_properties.SO_SERVICE_INSTANCE_PATH,
        ),
        "uri-parameters": ["service_instance_id"],
        "payload": "{}/so_vnf_instance.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "vnf_instance_name",
            "requestor_id",
            "model_invariant_id",
            "model_version_id",
            "model_name",
            "model_version",
            "model_customization_id",
            "tenant_id",
            "cloud_owner",
            "cloud_region",
            "api_type",
            "platform",
            "line_of_business",
            "service_model_name",
            "service_model_invariant_id",
            "service_model_version",
            "service_model_version_id",
            "service_instance_id",
        ],
        "header-parameters": ["X-TransactionId"],
        "success_code": 202,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            # "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (so_properties.SO_USERNAME, so_properties.SO_PASSWORD),
    },
    "DELETE_VNF_INSTANCE": {
        "verb": "DELETE",
        "description": "Deletes a VNF Instance.",
        "uri": partial(
            "{endpoint}{service_path}/{service_instance_id}/vnfs/{vnf_instance_id}".format,
            endpoint=so_properties.SO_ENDPOINT,
            service_path=so_properties.SO_SERVICE_INSTANCE_PATH,
        ),
        "uri-parameters": ["service_instance_id", "vnf_instance_id"],
        "payload": "{}/so_delete_vnf.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "vnf_invariant_id",
            "vnf_name",
            "vnf_version",
            "cloud_region",
            "cloud_owner",
            "tenant_id",
            "api_type",
        ],
        "header-parameters": ["X-TransactionId"],
        "success_code": 202,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            # "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (so_properties.SO_USERNAME, so_properties.SO_PASSWORD),
    },
    "CREATE_MODULE_INSTANCE": {
        "verb": "POST",
        "description": "Creates a VNF Module Instance.",
        "uri": partial(
            "{endpoint}{service_path}/{service_instance_id}/vnfs/{vnf_instance_id}/vfModules".format,
            endpoint=so_properties.SO_ENDPOINT,
            service_path=so_properties.SO_SERVICE_INSTANCE_PATH,
        ),
        "uri-parameters": ["service_instance_id", "vnf_instance_id"],
        "payload": "{}/so_create_module.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "module_instance_name",
            "model_invariant_id",
            "model_version_id",
            "model_name",
            "model_version",
            "model_customization_id",
            "model_name",
            "api_type",
            "tenant_id",
            "cloud_owner",
            "cloud_region",
            "service_instance_id",
            "service_model_name",
            "service_model_invariant_id",
            "service_model_version",
            "service_model_version_id",
            "vnf_instance_id",
            "vnf_model_name",
            "vnf_model_invariant_id",
            "vnf_model_version",
            "vnf_model_version_id",
            "vnf_model_customization_id",
        ],
        "header-parameters": ["X-TransactionId"],
        "success_code": 202,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            # "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (so_properties.SO_USERNAME, so_properties.SO_PASSWORD),
    },
    "DELETE_MODULE_INSTANCE": {
        "verb": "DELETE",
        "description": "Deletes a VNF Module Instance.",
        "uri": partial(
            "{endpoint}{service_path}/{service_instance_id}/vnfs/{vnf_instance_id}/vfModules/{vf_module_id}".format,
            endpoint=so_properties.SO_ENDPOINT,
            service_path=so_properties.SO_SERVICE_INSTANCE_PATH,
        ),
        "uri-parameters": ["service_instance_id", "vnf_instance_id", "vf_module_id"],
        "payload": "{}/so_delete_module.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "module_invariant_id",
            "module_name",
            "module_version",
            "cloud_region",
            "cloud_owner",
            "tenant_id",
            "api_type",
        ],
        "header-parameters": ["X-TransactionId"],
        "success_code": 202,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            # "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (so_properties.SO_USERNAME, so_properties.SO_PASSWORD),
    },
    "GET_REQUEST_STATUS": {
        "verb": "GET",
        "description": "Queries the status for a given request ID",
        "uri": partial(
            "{endpoint}{service_path}/{request_id}".format,
            endpoint=so_properties.SO_ENDPOINT,
            service_path=so_properties.SO_ORCHESTRATION_PATH,
        ),
        "uri-parameters": ["request_id"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (so_properties.SO_USERNAME, so_properties.SO_PASSWORD),
    },
    "GET_SERVICE_MODEL": {
        "verb": "GET",
        "description": "Searches the SO catalog for a service model",
        "uri": partial(
            "{endpoint}/service/search/findOneByModelName?modelName={model_name}".format,
            endpoint=so_properties.SO_ENDPOINT,
        ),
        "uri-parameters": ["model_name"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (so_properties.SO_USERNAME, so_properties.SO_PASSWORD),
    },
    "GET_SERVICE_MODEL_DETAILS": {
        "verb": "GET",
        "description": "Searches the SO catalog for a service model",
        "uri": partial(
            "{endpoint}/service/search/findOneByModelName?modelName={model_name}".format,
            endpoint=so_properties.SO_ENDPOINT,
        ),
        "uri-parameters": ["model_name"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (so_properties.SO_USERNAME, so_properties.SO_PASSWORD),
    },
}
