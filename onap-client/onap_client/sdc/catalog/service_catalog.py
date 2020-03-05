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

from onap_client import sdc
from onap_client import config
from onap_client.sdc.client import SDCClient

PAYLOADS_DIR = config.PAYLOADS_DIR
sdc_properties = sdc.SDC_PROPERTIES
application_id = config.APPLICATION_ID


class ServiceCatalog(SDCClient):
    @property
    def catalog_resources(self):
        return CATALOG_RESOURCES

    @property
    def namespace(self):
        return "service"


CATALOG_RESOURCES = {
    "ADD_CATALOG_SERVICE": {
        "verb": "POST",
        "description": "Creates a Service in the SDC catalog",
        "uri": partial(
            "{endpoint}{service_path}".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_SERVICES_PATH,
        ),
        "payload": "{}/catalog_service.jinja".format(PAYLOADS_DIR),
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
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"catalog_service_id": ("uniqueId",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "ADD_RESOURCE_INSTANCE": {
        "verb": "POST",
        "description": "Attaches a Resource to a Service",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_service_id}/resourceInstance".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_SERVICES_PATH,
        ),
        "uri-parameters": ["catalog_service_id"],
        "payload": "{}/resource_instance.jinja".format(PAYLOADS_DIR),
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
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"catalog_resource_instance_id": ("uniqueId",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "CHECKIN_SERVICE": {
        "verb": "POST",
        "description": "Checks a service into the SDC Catalog",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_service_id}/lifecycleState/checkin".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_SERVICES_PATH,
        ),
        "uri-parameters": ["catalog_service_id"],
        "payload": "{}/user_remarks.jinja".format(PAYLOADS_DIR),
        "payload-parameters": ["user_remarks"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "REQUEST_SERVICE_CERTIFICATION": {
        "verb": "POST",
        "description": "Requests certification of a service into the SDC Catalog",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_service_id}/lifecycleState/certificationRequest".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_SERVICES_PATH,
        ),
        "uri-parameters": ["catalog_service_id"],
        "payload": "{}/user_remarks.jinja".format(PAYLOADS_DIR),
        "payload-parameters": ["user_remarks"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "START_SERVICE_CERTIFICATION": {
        "verb": "POST",
        "description": "Starts certification of a service into the SDC Catalog",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_service_id}/lifecycleState/startCertification".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_SERVICES_PATH,
        ),
        "uri-parameters": ["catalog_service_id"],
        "payload": "{}/user_remarks.jinja".format(PAYLOADS_DIR),
        "payload-parameters": ["user_remarks"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_TESTER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "FINISH_SERVICE_CERTIFICATION": {
        "verb": "POST",
        "description": "Finishes certification of a service from the SDC Catalog",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_service_id}/lifecycleState/certify".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_SERVICES_PATH,
        ),
        "uri-parameters": ["catalog_service_id"],
        "payload": "{}/user_remarks.jinja".format(PAYLOADS_DIR),
        "payload-parameters": ["user_remarks"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_TESTER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"catalog_service_id": ("uniqueId",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "APPROVE_SERVICE_CERTIFICATION": {
        "verb": "POST",
        "description": "Approves a service from the SDC Catalog",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_service_id}/distribution-state/approve".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_SERVICES_PATH,
        ),
        "uri-parameters": ["catalog_service_id"],
        "payload": "{}/user_remarks.jinja".format(PAYLOADS_DIR),
        "payload-parameters": ["user_remarks"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_GOVERNOR_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "DISTRIBUTE_SDC_SERVICE": {
        "verb": "POST",
        "description": "Distributes a service from the SDC Catalog",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_service_id}/distribution/PROD/activate".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_SERVICES_PATH,
        ),
        "uri-parameters": ["catalog_service_id"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_OPS_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "ADD_CATALOG_SERVICE_PROPERTY": {
        "verb": "POST",
        "description": "Add a property value for a VF in a Service",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_service_id}/resourceInstance/{catalog_resource_instance_id}/properties".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "uri-parameters": ["catalog_service_id", "catalog_resource_instance_id"],
        "payload": "{}/catalog_service_property.jinja".format(PAYLOADS_DIR),
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
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "ADD_CATALOG_SERVICE_INPUT": {
        "verb": "POST",
        "description": "Add an input value for a VF in a Service",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_service_id}/resourceInstance/{catalog_resource_instance_id}/inputs".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "uri-parameters": ["catalog_service_id", "catalog_resource_instance_id"],
        "payload": "{}/catalog_service_property.jinja".format(PAYLOADS_DIR),
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
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "GET_SDC_SERVICE": {
        "verb": "GET",
        "description": "Gets a service from the SDC Catalog",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_service_id}".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_SERVICES_PATH,
        ),
        "uri-parameters": ["catalog_service_id"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "GET_SERVICES": {
        "verb": "GET",
        "description": "Get all services in the SDC catalog",
        "uri": partial(
            "{endpoint}{service_path}".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_SCREEN_PATH,
        ),
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"services": ("services",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "GET_SERVICE_DISTRIBUTION": {
        "verb": "GET",
        "description": "Gets the distribution for a service from the SDC Catalog",
        "uri": partial(
            "{endpoint}{service_path}/{distribution_service_id}/distribution".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_SERVICES_PATH,
        ),
        "uri-parameters": ["distribution_service_id"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "GET_SERVICE_DISTRIBUTION_DETAILS": {
        "verb": "GET",
        "description": "Gets the distribution details for a service from the SDC Catalog",
        "uri": partial(
            "{endpoint}{service_path}/distribution/{distribution_id}".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_SERVICES_PATH,
        ),
        "uri-parameters": ["distribution_id"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
}
