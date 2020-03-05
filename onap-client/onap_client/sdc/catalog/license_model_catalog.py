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


class LicenseModelClient(SDCClient):
    @property
    def catalog_resources(self):
        return CATALOG_RESOURCES

    @property
    def namespace(self):
        return "license_model"


CATALOG_RESOURCES = {
    "ADD_LICENSE_MODEL": {
        "verb": "POST",
        "description": "creates a license model in the SDC catalog",
        "uri": partial(
            "{endpoint}{service_path}".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_LICENSE_MODEL_PATH,
        ),
        "payload": "{}/license_model.jinja".format(PAYLOADS_DIR),
        "payload-parameters": ["vendor_name"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {
            "license_model_id": ("itemId",),
            "license_model_version_id": ("version", "id"),
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "ADD_KEY_GROUP": {
        "verb": "POST",
        "description": "Adds a key group to a license model",
        "uri": partial(
            "{endpoint}{service_path}/{license_model_id}/versions/{license_model_version_id}/license-key-groups".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_LICENSE_MODEL_PATH,
        ),
        "uri-parameters": ["license_model_id", "license_model_version_id"],
        "payload": "{}/key_group.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "license_start_date",
            "license_end_date",
            "key_group_name",
        ],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"key_group_id": ("value",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "ADD_ENTITLEMENT_POOL": {
        "verb": "POST",
        "description": "Adds an entitlement pool to a license model",
        "uri": partial(
            "{endpoint}{service_path}/{license_model_id}/versions/{license_model_version_id}/entitlement-pools".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_LICENSE_MODEL_PATH,
        ),
        "uri-parameters": ["license_model_id", "license_model_version_id"],
        "payload": "{}/entitlement_pool.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "license_start_date",
            "license_end_date",
            "entitlement_pool_name",
        ],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"entitlement_pool_id": ("value",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "ADD_FEATURE_GROUP": {
        "verb": "POST",
        "description": "Adds an feature group to a license model",
        "uri": partial(
            "{endpoint}{service_path}/{license_model_id}/versions/{license_model_version_id}/feature-groups".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_LICENSE_MODEL_PATH,
        ),
        "uri-parameters": ["license_model_id", "license_model_version_id"],
        "payload": "{}/feature_group.jinja".format(PAYLOADS_DIR),
        "payload-parameters": [
            "feature_group_name",
            "key_group_id",
            "entitlement_pool_id",
            "manufacturer_reference_number",
        ],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"feature_group_id": ("value",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "ADD_LICENSE_AGREEMENT": {
        "verb": "POST",
        "description": "Adds an license agreement to a license model",
        "uri": partial(
            "{endpoint}{service_path}/{license_model_id}/versions/{license_model_version_id}/license-agreements".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_LICENSE_MODEL_PATH,
        ),
        "uri-parameters": ["license_model_id", "license_model_version_id"],
        "payload": "{}/license_agreement.jinja".format(PAYLOADS_DIR),
        "payload-parameters": ["feature_group_id", "license_agreement_name"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {"license_agreement_id": ("value",)},
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "SUBMIT_LICENSE_MODEL": {
        "verb": "PUT",
        "description": "Submits a license model",
        "uri": partial(
            "{endpoint}{service_path}/{license_model_id}/versions/{license_model_version_id}/actions".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_LICENSE_MODEL_PATH,
        ),
        "uri-parameters": ["license_model_id", "license_model_version_id"],
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
    "GET_LICENSE_MODEL": {
        "verb": "GET",
        "description": "Returns a license model",
        "uri": partial(
            "{endpoint}{service_path}/{license_model_id}/versions/{license_model_version_id}".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_LICENSE_MODEL_PATH,
        ),
        "uri-parameters": ["license_model_id", "license_model_version_id"],
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "return_data": {
            "vendor_name": ("vendorName",),
            "license_model_id": ("id",),
            "description": ("description",),
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
    "GET_LICENSE_MODEL_VERSION_ATTRIBUTE": {
        "verb": "GET",
        "description": "Returns an attribute for a license model (license-agreements, features-groups, etc...)",
        "uri": partial(
            "{endpoint}{service_path}/{license_model_id}/versions/{license_model_version_id}/{attribute}".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_LICENSE_MODEL_PATH,
        ),
        "uri-parameters": ["license_model_id", "license_model_version_id", "attribute"],
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
    "GET_LICENSE_MODEL_VERSIONS": {
        "verb": "GET",
        "description": "Returns the version list for a license model",
        "uri": partial(
            "{endpoint}{service_path}/{license_model_id}/versions".format,
            endpoint=sdc_properties.SDC_BE_ONBOARD_ENDPOINT,
            service_path=sdc_properties.SDC_VENDOR_ITEMS_PATH,
        ),
        "uri-parameters": ["license_model_id"],
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
    "GET_LICENSE_MODELS": {
        "verb": "GET",
        "description": "Returns the full list of license models from SDC",
        "uri": partial(
            "{endpoint}{service_path}?&itemType=vlm".format,
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
}
