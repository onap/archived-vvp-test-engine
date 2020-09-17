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

from onap_client.sdc.client import SDCClient


class ServiceCatalog(SDCClient):
    @property
    def namespace(self):
        return "service"

    @property
    def catalog_resources(self):
        return {
            "ADD_CATALOG_SERVICE": {
                "verb": "POST",
                "description": "Creates a Service in the SDC catalog",
                "uri": partial(
                    "{endpoint}{service_path}".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "payload": "{}/catalog_service.jinja".format(self.config.payload_directory),
                "payload-parameters": [
                    "service_name",
                    "instantiation_type",
                    "contact_id",
                    "category_name",
                    "category_id",
                    "category_name_lower",
                    "category_name_icon",
                    "tag",
                    "project_code",
                    "environment_context",
                    "ecomp_generated_naming",
                    "description",
                    "service_type",
                    "service_role",
                    "naming_policy",
                ],
                "success_code": 201,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "return_data": {"catalog_service_id": ("uniqueId",)},
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "CHECKOUT_CATALOG_SERVICE": {
                "verb": "POST",
                "description": "Creates a new version of a Service in the SDC catalog",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}/lifecycleState/CHECKOUT".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "uri-parameters": ["catalog_service_id"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "return_data": {"catalog_service_id": ("uniqueId",)},
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "ADD_RESOURCE_INSTANCE": {
                "verb": "POST",
                "description": "Attaches a Resource to a Service",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}/resourceInstance".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "uri-parameters": ["catalog_service_id"],
                "payload": "{}/resource_instance.jinja".format(self.config.payload_directory),
                "payload-parameters": [
                    "milli_timestamp",
                    "catalog_resource_id",
                    "catalog_resource_name",
                    "originType",
                    "posX",
                    "posY",
                ],
                "success_code": 201,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "return_data": {"catalog_resource_instance_id": ("uniqueId",)},
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "DELETE_RESOURCE_FROM_SERVICE": {
                "verb": "DELETE",
                "description": "Deletes a resource from a service.",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}/resourceInstance/{resource_instance_id}".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "uri-parameters": ["catalog_service_id", "resource_instance_id"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "UPDATE_RESOURCE_VERSION": {
                "verb": "POST",
                "description": "Updates a component version in a service",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}/resourceInstance/{component_name}/changeVersion".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "uri-parameters": ["catalog_service_id", "component_name"],
                "payload": "{}/update_resource_instance.jinja".format(self.config.payload_directory),
                "payload-parameters": [
                    "component_id",
                ],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "CHECKIN_SERVICE": {
                "verb": "POST",
                "description": "Checks a service into the SDC Catalog",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}/lifecycleState/checkin".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "uri-parameters": ["catalog_service_id"],
                "payload": "{}/user_remarks.jinja".format(self.config.payload_directory),
                "payload-parameters": ["user_remarks"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "REQUEST_SERVICE_CERTIFICATION": {
                "verb": "POST",
                "description": "Requests certification of a service into the SDC Catalog",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}/lifecycleState/certificationRequest".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "uri-parameters": ["catalog_service_id"],
                "payload": "{}/user_remarks.jinja".format(self.config.payload_directory),
                "payload-parameters": ["user_remarks"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "START_SERVICE_CERTIFICATION": {
                "verb": "POST",
                "description": "Starts certification of a service into the SDC Catalog",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}/lifecycleState/startCertification".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "uri-parameters": ["catalog_service_id"],
                "payload": "{}/user_remarks.jinja".format(self.config.payload_directory),
                "payload-parameters": ["user_remarks"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_tester_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "FINISH_SERVICE_CERTIFICATION": {
                "verb": "POST",
                "description": "Finishes certification of a service from the SDC Catalog",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}/lifecycleState/certify".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "uri-parameters": ["catalog_service_id"],
                "payload": "{}/user_remarks.jinja".format(self.config.payload_directory),
                "payload-parameters": ["user_remarks"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_tester_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "return_data": {"catalog_service_id": ("uniqueId",)},
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "APPROVE_SERVICE_CERTIFICATION": {
                "verb": "POST",
                "description": "Approves a service from the SDC Catalog",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}/distribution-state/approve".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "uri-parameters": ["catalog_service_id"],
                "payload": "{}/user_remarks.jinja".format(self.config.payload_directory),
                "payload-parameters": ["user_remarks"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_governor_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "DISTRIBUTE_SDC_SERVICE": {
                "verb": "POST",
                "description": "Distributes a service from the SDC Catalog",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}/distribution/PROD/activate".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "uri-parameters": ["catalog_service_id"],
                "success_code": 200,
                "header-parameters": ["X-TransactionId"],
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_ops_user_id,
                    # "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "ADD_CATALOG_SERVICE_PROPERTY": {
                "verb": "POST",
                "description": "Add a property value for a VF in a Service",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}/resourceInstance/{catalog_resource_instance_id}/properties".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_RESOURCES_PATH,
                ),
                "uri-parameters": ["catalog_service_id", "catalog_resource_instance_id"],
                "payload": "{}/catalog_service_property.jinja".format(self.config.payload_directory),
                "payload-parameters": [
                    "unique_id",
                    "parent_unique_id",
                    "owner_id",
                    "input_name",
                    "input_value",
                    "schema_type",
                    "property_type",
                ],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "ADD_CATALOG_SERVICE_INPUT": {
                "verb": "POST",
                "description": "Add an input value for a VF in a Service",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}/resourceInstance/{catalog_resource_instance_id}/inputs".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_RESOURCES_PATH,
                ),
                "uri-parameters": ["catalog_service_id", "catalog_resource_instance_id"],
                "payload": "{}/catalog_service_property.jinja".format(self.config.payload_directory),
                "payload-parameters": [
                    "unique_id",
                    "parent_unique_id",
                    "owner_id",
                    "input_name",
                    "input_value",
                ],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "UPDATE_MODULE_DEPLOYMENT_PROPERTIES": {
                "verb": "POST",
                "description": "Updates the deployment properties for a module.",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}/resourceInstance/{catalog_resource_instance_id}/artifacts/{module_id}".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_RESOURCES_PATH,
                ),
                "uri-parameters": ["catalog_service_id", "catalog_resource_instance_id", "module_id"],
                "payload": "{}/generic_payload.jinja".format(self.config.payload_directory),
                "payload-parameters": [
                    "payload_data",
                ],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "GET_SDC_SERVICE": {
                "verb": "GET",
                "description": "Gets a service from the SDC Catalog",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "uri-parameters": ["catalog_service_id"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "GET_SERVICES": {
                "verb": "GET",
                "description": "Get all services in the SDC catalog",
                "uri": partial(
                    "{endpoint}{service_path}".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_SCREEN_PATH,
                ),
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "return_data": {"services": ("services",)},
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "GET_SERVICE_DISTRIBUTION": {
                "verb": "GET",
                "description": "Gets the distribution for a service from the SDC Catalog",
                "uri": partial(
                    "{endpoint}{service_path}/{distribution_service_id}/distribution".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "uri-parameters": ["distribution_service_id"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "GET_SERVICE_DISTRIBUTION_DETAILS": {
                "verb": "GET",
                "description": "Gets the distribution details for a service from the SDC Catalog",
                "uri": partial(
                    "{endpoint}{service_path}/distribution/{distribution_id}".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "uri-parameters": ["distribution_id"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
            "GET_SDC_CSAR": {
                "verb": "GET",
                "description": "Returns the CSAR for a service.",
                "uri": partial(
                    "{endpoint}{service_path}/{catalog_service_id}/artifacts/{csar_artifact_id}".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_CATALOG_SERVICES_PATH,
                ),
                "uri-parameters": ["catalog_service_id", "csar_artifact_id"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (
                    self.global_sdc_username,
                    self.global_sdc_password,
                ),
            },
        }
