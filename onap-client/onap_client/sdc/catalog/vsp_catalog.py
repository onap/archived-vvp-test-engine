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


class VSPCatalog(SDCClient):
    @property
    def catalog_resources(self):
        return CATALOG_RESOURCES

    @property
    def namespace(self):
        return "vsp"


CATALOG_RESOURCES = {
    "ADD_SOFTWARE_PRODUCT": {
        "verb": "POST",
        "description": "Creates a VSP in the SDC catalog",
        "uri": partial(
            "{endpoint}{service_path}".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_SOFTWARE_PRODUCT_PATH,
        ),
        "payload": "{}/software_product.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "software_product_name",
            "feature_group_id",
            "license_agreement_id",
            "vendor_name",
            "license_model_id",
            "license_model_version_id",
            "description",
            "category",
            "sub_category",
        ],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {
            "software_product_id": ("itemId",),
            "software_product_version_id": ("version", "id"),
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "UPDATE_SOFTWARE_PRODUCT": {
        "verb": "POST",
        "description": "Updates a VSP to a new version",
        "uri": partial(
            "{endpoint}{service_path}/{software_product_id}/versions/{software_product_version_id}".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_ITEMS_PATH,
        ),
        "payload": "{}/software_product_update.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "description",
        ],
        "uri-parameters": ["software_product_id", "software_product_version_id"],
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
    "UPLOAD_HEAT_PACKAGE": {
        "verb": "POST",
        "description": "Uploads a heat zip to a VSP",
        "uri": partial(
            "{endpoint}{service_path}/{software_product_id}/versions/{software_product_version_id}/orchestration-template-candidate".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_SOFTWARE_PRODUCT_PATH,
        ),
        "uri-parameters": ["software_product_id", "software_product_version_id"],
        "files-parameters": ["file_path", "file_type"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "multipart/form-data",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "VALIDATE_SOFTWARE_PRODUCT": {
        "verb": "PUT",
        "description": "Validates VSP with Heat Zip",
        "uri": partial(
            "{endpoint}{service_path}/{software_product_id}/versions/{software_product_version_id}/orchestration-template-candidate/process".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_SOFTWARE_PRODUCT_PATH,
        ),
        "uri-parameters": ["software_product_id", "software_product_version_id"],
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
    "SUBMIT_SOFTWARE_PRODUCT": {
        "verb": "PUT",
        "description": "Submits Heat Zip to VSP",
        "uri": partial(
            "{endpoint}{service_path}/{software_product_id}/versions/{software_product_version_id}/actions".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_SOFTWARE_PRODUCT_PATH,
        ),
        "uri-parameters": ["software_product_id", "software_product_version_id"],
        "payload": "{}/action.jinja".format(PAYLOADS_DIR),
        "payload-parameters": ["action"],
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
    "PACKAGE_SOFTWARE_PRODUCT": {
        "verb": "PUT",
        "description": "Packages VSP (description needs to be better??)",
        "uri": partial(
            "{endpoint}{service_path}/{software_product_id}/versions/{software_product_version_id}/actions".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_SOFTWARE_PRODUCT_PATH,
        ),
        "uri-parameters": ["software_product_id", "software_product_version_id"],
        "payload": "{}/action.jinja".format(PAYLOADS_DIR),
        "payload-parameters": ["action"],
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
    "GET_SOFTWARE_PRODUCT": {
        "verb": "GET",
        "description": "Gets VSP from Catalog",
        "uri": partial(
            "{endpoint}{service_path}/{software_product_id}/versions/{software_product_version_id}".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_SOFTWARE_PRODUCT_PATH,
        ),
        "uri-parameters": ["software_product_id", "software_product_version_id"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"name": ("name",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "GET_SOFTWARE_PRODUCT_INFORMATION": {
        "verb": "GET",
        "description": "Gets Information for a VSP from Catalog",
        "uri": partial(
            "{endpoint}{service_path}/{software_product_id}/versions/{software_product_version_id}/questionnaire".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_SOFTWARE_PRODUCT_PATH,
        ),
        "uri-parameters": ["software_product_id", "software_product_version_id"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"name": ("name",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "GET_SOFTWARE_PRODUCT_VERSIONS": {
        "verb": "GET",
        "description": "Returns a list of vsp versions",
        "uri": partial(
            "{endpoint}{service_path}/{software_product_id}/versions".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_ITEMS_PATH,
        ),
        "uri-parameters": ["software_product_id"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {
            "software_product_version_id": ("id",),
            "description": ("description",),
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "GET_SOFTWARE_PRODUCTS": {
        "verb": "GET",
        "description": "Returns a list of vsps",
        "uri": partial(
            "{endpoint}{service_path}?&itemType=vsp".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_ITEMS_PATH,
        ),
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"results": ("results",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "ADD_VSP_CONTRIBUTER": {
        "verb": "PUT",
        "description": "Adds a user to a VSP as a contributer",
        "uri": partial(
            "{endpoint}{service_path}/{software_product_id}/permissions/Contributor".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_ITEMS_PATH,
        ),
        "uri-parameters": ["software_product_id"],
        "payload": "{}/add_vsp_contributer.jinja".format(PAYLOADS_DIR),
        "payload-parameters": ["user_id"],
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
