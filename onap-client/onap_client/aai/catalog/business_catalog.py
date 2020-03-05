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

from onap_client import aai
from onap_client import config
from onap_client.aai.client import AAIClient

PAYLOADS_DIR = config.PAYLOADS_DIR
aai_properties = aai.AAI_PROPERTIES
application_id = config.APPLICATION_ID


class BusinessClient(AAIClient):
    @property
    def catalog_resources(self):
        return CATALOG_RESOURCES

    @property
    def namespace(self):
        return "business"


CATALOG_RESOURCES = {
    "GET_OWNING_ENTITY": {
        "verb": "GET",
        "description": "Queries AAI for an owning entity",
        "uri": partial(
            "{endpoint}{service_path}/owning-entities?owning-entity-name={name}".format,
            endpoint=aai_properties.AAI_BE_ENDPOINT,
            service_path=aai_properties.AAI_BUSINESS_PATH,
        ),
        "uri-parameters": ["name"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (aai_properties.AAI_USERNAME, aai_properties.AAI_PASSWORD,),
    },
    "GET_OWNING_ENTITIES": {
        "verb": "GET",
        "description": "Queries AAI for all owning entities",
        "uri": partial(
            "{endpoint}{service_path}/owning-entities".format,
            endpoint=aai_properties.AAI_BE_ENDPOINT,
            service_path=aai_properties.AAI_BUSINESS_PATH,
        ),
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (aai_properties.AAI_USERNAME, aai_properties.AAI_PASSWORD,),
    },
    "GET_CUSTOMER": {
        "verb": "GET",
        "description": "Queries AAI for a customer",
        "uri": partial(
            "{endpoint}{service_path}/customers?global-customer-id={name}".format,
            endpoint=aai_properties.AAI_BE_ENDPOINT,
            service_path=aai_properties.AAI_BUSINESS_PATH,
        ),
        "uri-parameters": ["name"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (aai_properties.AAI_USERNAME, aai_properties.AAI_PASSWORD,),
    },
    "GET_CUSTOMERS": {
        "verb": "GET",
        "description": "Queries AAI for all customers",
        "uri": partial(
            "{endpoint}{service_path}/customers".format,
            endpoint=aai_properties.AAI_BE_ENDPOINT,
            service_path=aai_properties.AAI_BUSINESS_PATH,
        ),
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (aai_properties.AAI_USERNAME, aai_properties.AAI_PASSWORD,),
    },
    "GET_PLATFORM": {
        "verb": "GET",
        "description": "Queries AAI for a platform",
        "uri": partial(
            "{endpoint}{service_path}/platforms?platform-name={name}".format,
            endpoint=aai_properties.AAI_BE_ENDPOINT,
            service_path=aai_properties.AAI_BUSINESS_PATH,
        ),
        "uri-parameters": ["name"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (aai_properties.AAI_USERNAME, aai_properties.AAI_PASSWORD,),
    },
    "GET_PLATFORMS": {
        "verb": "GET",
        "description": "Queries AAI for all platforms",
        "uri": partial(
            "{endpoint}{service_path}/platforms".format,
            endpoint=aai_properties.AAI_BE_ENDPOINT,
            service_path=aai_properties.AAI_BUSINESS_PATH,
        ),
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (aai_properties.AAI_USERNAME, aai_properties.AAI_PASSWORD,),
    },
    "GET_PROJECT": {
        "verb": "GET",
        "description": "Queries AAI for a project",
        "uri": partial(
            "{endpoint}{service_path}/projects/project/{name}".format,
            endpoint=aai_properties.AAI_BE_ENDPOINT,
            service_path=aai_properties.AAI_BUSINESS_PATH,
        ),
        "uri-parameters": ["name"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (aai_properties.AAI_USERNAME, aai_properties.AAI_PASSWORD,),
    },
    "GET_PROJECTS": {
        "verb": "GET",
        "description": "Queries AAI for all projects",
        "uri": partial(
            "{endpoint}{service_path}/projects".format,
            endpoint=aai_properties.AAI_BE_ENDPOINT,
            service_path=aai_properties.AAI_BUSINESS_PATH,
        ),
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (aai_properties.AAI_USERNAME, aai_properties.AAI_PASSWORD,),
    },
    "GET_LINES_OF_BUSINESS": {
        "verb": "GET",
        "description": "Queries AAI for all lobs",
        "uri": partial(
            "{endpoint}{service_path}/lines-of-business".format,
            endpoint=aai_properties.AAI_BE_ENDPOINT,
            service_path=aai_properties.AAI_BUSINESS_PATH,
        ),
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (aai_properties.AAI_USERNAME, aai_properties.AAI_PASSWORD,),
    },
    "CREATE_CUSTOMER": {
        "verb": "PUT",
        "description": "Creates a customer in AAI",
        "uri": partial(
            "{endpoint}{service_path}/customers/customer/{customer_name}".format,
            endpoint=aai_properties.AAI_BE_ENDPOINT,
            service_path=aai_properties.AAI_BUSINESS_PATH,
        ),
        "uri-parameters": ["customer_name"],
        "payload-parameters": ["customer_name", "subscriber_name"],
        "payload": "{}/aai_create_customer.jinja".format(PAYLOADS_DIR),
        "success_code": 201,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (aai_properties.AAI_USERNAME, aai_properties.AAI_PASSWORD,),
    },
    "GET_CUSTOMER_SUBSCRIPTIONS": {
        "verb": "GET",
        "description": "Queries AAI the subscriptions for a customer",
        "uri": partial(
            "{endpoint}{service_path}/customers/customer/{customer_name}/service-subscriptions".format,
            endpoint=aai_properties.AAI_BE_ENDPOINT,
            service_path=aai_properties.AAI_BUSINESS_PATH,
        ),
        "uri-parameters": ["customer_name"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (aai_properties.AAI_USERNAME, aai_properties.AAI_PASSWORD,),
    },
    "GET_SERVICE_INSTANCES": {
        "verb": "GET",
        "description": "Queries AAI the service instances for a customer subscription",
        "uri": partial(
            "{endpoint}{service_path}/customers/customer/{customer_name}/service-subscriptions/service-subscription/{subscription_name}/service-instances".format,
            endpoint=aai_properties.AAI_BE_ENDPOINT,
            service_path=aai_properties.AAI_BUSINESS_PATH,
        ),
        "uri-parameters": ["customer_name", "subscription_name"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (aai_properties.AAI_USERNAME, aai_properties.AAI_PASSWORD,),
    },
}
