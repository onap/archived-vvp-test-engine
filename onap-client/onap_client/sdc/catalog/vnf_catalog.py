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


class VNFCatalog(SDCClient):
    @property
    def catalog_resources(self):
        return CATALOG_RESOURCES

    @property
    def namespace(self):
        return "vnf"


CATALOG_RESOURCES = {
    "ADD_CATALOG_RESOURCE": {
        "verb": "POST",
        "description": "Adds a VNF to the SDC catalog",
        "uri": partial(
            "{endpoint}{service_path}".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "payload": "{}/catalog_resource.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "software_product_id",
            "vnf_name",
            "vendor_name",
            "resource_type",
            "categories",
            "contact_id",
        ],
        "success_code": 201,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"catalog_resource_id": ("uniqueId",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "CERTIFY_CATALOG_RESOURCE": {
        "verb": "POST",
        "description": "Certifies a VNF in the SDC catalog",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}/lifecycleState/certify".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "uri-parameters": ["catalog_resource_id"],
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
        "return_data": {"catalog_resource_id": ("uniqueId",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "ADD_CATALOG_RESOURCE_INPUT": {
        "verb": "POST",
        "description": "Adds an input value for a VNF",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}/update/inputs".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "payload": "{}/catalog_vnf_input.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "input_default_value",
            "input_name",
            "input_parent_unique_id",
            "input_unique_id",
            "input_owner_id",
        ],
        "uri-parameters": ["catalog_resource_id"],
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
    "UPDATE_CATALOG_RESOURCE": {
        "verb": "PUT",
        "description": "Creates a new version of a VF resource",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "uri-parameters": ["catalog_resource_id"],
        "success_code": 200,
        "payload": "{}/generic_payload.jinja".format(PAYLOADS_DIR),
        "payload-parameters": ["payload_data"],
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
    "CHECKOUT_CATALOG_RESOURCE": {
        "verb": "POST",
        "description": "Checks out a VF from the catalog",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}/lifecycleState/CHECKOUT".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "uri-parameters": ["catalog_resource_id"],
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
    "ADD_CATALOG_RESOURCE_PROPERTY": {
        "verb": "POST",
        "description": "Adds an property value for a VNF",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}/resourceInstance/{catalog_resource_instance_id}/inputs".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "payload": "{}/catalog_vnf_property.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "unique_id",
            "parent_unique_id",
            "owner_id",
            "property_name",
            "property_default_value",
            "schema_type",
            "property_type",
        ],
        "uri-parameters": ["catalog_resource_id", "catalog_resource_instance_id"],
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
    "ADD_CATALOG_RESOURCE_PROPERTY_NON_VF": {
        "verb": "POST",
        "description": "Adds an property value for a VNF",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}/resourceInstance/{catalog_resource_instance_id}/properties".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "payload": "{}/catalog_vnf_property.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "unique_id",
            "parent_unique_id",
            "owner_id",
            "property_name",
            "property_default_value",
            "schema_type",
            "property_type",
        ],
        "uri-parameters": ["catalog_resource_id", "catalog_resource_instance_id"],
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
    "ADD_CATALOG_RESOURCE_POLICY": {
        "verb": "POST",
        "description": "Adds an policy resource to a VNF",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}/policies/{catalog_policy_name}".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "uri-parameters": ["catalog_resource_id", "catalog_policy_name"],
        "success_code": 201,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"catalog_resource_id": ("uniqueId",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "ADD_CATALOG_POLICY_PROPERTY": {
        "verb": "PUT",
        "description": "Adds a property to a policy for a VNF",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}/policies/{catalog_policy_id}/properties".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "uri-parameters": ["catalog_resource_id", "catalog_policy_id"],
        "payload": "{}/catalog_vnf_policy_property.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "unique_id",
            "property_name",
            "property_default_value",
            "description",
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
    "ADD_CATALOG_RESOURCE_GROUP": {
        "verb": "POST",
        "description": "Adds an group resource to a VNF",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}/groups/{catalog_group_name}".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "uri-parameters": ["catalog_resource_id", "catalog_group_name"],
        "success_code": 201,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"catalog_resource_id": ("uniqueId",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "ADD_CATALOG_GROUP_PROPERTY": {
        "verb": "PUT",
        "description": "Adds a property to a group for a VNF",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}/groups/{catalog_group_id}/properties".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "uri-parameters": ["catalog_resource_id", "catalog_group_id"],
        "payload": "{}/catalog_vnf_group_property.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "unique_id",
            "property_name",
            "property_default_value",
            "description",
            "property_type",
            "owner_id",
            "parent_unique_id",
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
    "ADD_GROUP_TO_INSTANCE": {
        "verb": "POST",
        "description": "Associate a group with a Catalog Instance",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}/groups/{catalog_group_id}/members".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "payload": "{}/catalog_vnf_group.jinja".format(PAYLOADS_DIR),
        "payload-parameters": ["instance_id"],
        "uri-parameters": ["catalog_resource_id", "catalog_group_id"],
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
    "ADD_POLICY_TO_INSTANCE": {
        "verb": "POST",
        "description": "Associate a policy with a Catalog Instance",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}/policies/{catalog_policy_id}/targets".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "payload": "{}/catalog_vnf_policy.jinja".format(PAYLOADS_DIR),
        "payload-parameters": ["instance_ids"],
        "uri-parameters": ["catalog_resource_id", "catalog_policy_id"],
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
    "ADD_RESOURCE_INSTANCE": {
        "verb": "POST",
        "description": "Attaches a Resource to a VNF",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}/resourceInstance".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "uri-parameters": ["catalog_resource_id"],
        "payload": "{}/resource_instance_vnf.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "milli_timestamp",
            "new_catalog_resource_id",
            "new_catalog_resource_name",
            "originType",
            "posX",
            "posY",
        ],
        "success_code": 201,
        "return_data": {"catalog_resource_instance_id": ("uniqueId",)},
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
    "ADD_RESOURCE_RELATIONSHIP": {
        "verb": "POST",
        "description": "Creates a relationship between two resources in a VF",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}/resourceInstance/associate".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "uri-parameters": ["catalog_resource_id"],
        "payload": "{}/add_resource_relationship.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "from_node_resource_id",
            "to_node_resource_id",
            "relationship_type",
            "capability_name",
            "capability_owner_id",
            "capability_id",
            "requirement_name",
            "requirement_id",
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
    "GET_CATALOG_RESOURCE": {
        "verb": "GET",
        "description": "Gets a VNF in the SDC catalog",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "uri-parameters": ["catalog_resource_id"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"catalog_resource_name": ("name",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "GET_CATALOG_RESOURCE_METADATA": {
        "verb": "GET",
        "description": "Gets metadata for a VNF in the SDC catalog",
        "uri": partial(
            "{endpoint}{service_path}/{catalog_resource_id}/filteredDataByParams?include=metadata".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_CATALOG_RESOURCES_PATH,
        ),
        "uri-parameters": ["catalog_resource_id"],
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
    "GET_RESOURCES": {
        "verb": "GET",
        "description": "Get all resources in the SDC catalog",
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
        "return_data": {"resources": ("resources",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
}
