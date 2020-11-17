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
from functools import partial

from onap_client.sdc.client import SDCClient


class LicenseModelClient(SDCClient):
    @property
    def namespace(self):
        return "license_model"

    @property
    def catalog_resources(self):
        return {
            "ADD_LICENSE_MODEL": {
                "verb": "POST",
                "description": "creates a license model in the SDC catalog",
                "uri": partial(
                    "{endpoint}{service_path}".format,
                    endpoint=self.config.sdc.SDC_BE_ONBOARD_ENDPOINT,
                    service_path=self.config.sdc.SDC_VENDOR_LICENSE_MODEL_PATH,
                ),
                "payload": "{}/license_model.jinja".format(self.config.payload_directory),
                "payload-parameters": ["vendor_name"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-FromAppId": self.config.application_id,
                },
                "return_data": {
                    "license_model_id": ("itemId",),
                    "license_model_version_id": ("version", "id"),
                },
                "auth": self.auth,
            },
            "ADD_KEY_GROUP": {
                "verb": "POST",
                "description": "Adds a key group to a license model",
                "uri": partial(
                    "{endpoint}{service_path}/{license_model_id}/versions/{license_model_version_id}/license-key-groups".format,
                    endpoint=self.config.sdc.SDC_BE_ONBOARD_ENDPOINT,
                    service_path=self.config.sdc.SDC_VENDOR_LICENSE_MODEL_PATH,
                ),
                "uri-parameters": ["license_model_id", "license_model_version_id"],
                "payload": "{}/key_group.jinja".format(self.config.payload_directory),
                "payload-parameters": [
                    "license_start_date",
                    "license_end_date",
                    "key_group_name",
                ],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-FromAppId": self.config.application_id,
                },
                "return_data": {"key_group_id": ("value",)},
                "auth": self.auth,
            },
            "ADD_ENTITLEMENT_POOL": {
                "verb": "POST",
                "description": "Adds an entitlement pool to a license model",
                "uri": partial(
                    "{endpoint}{service_path}/{license_model_id}/versions/{license_model_version_id}/entitlement-pools".format,
                    endpoint=self.config.sdc.SDC_BE_ONBOARD_ENDPOINT,
                    service_path=self.config.sdc.SDC_VENDOR_LICENSE_MODEL_PATH,
                ),
                "uri-parameters": ["license_model_id", "license_model_version_id"],
                "payload": "{}/entitlement_pool.jinja".format(self.config.payload_directory),
                "payload-parameters": [
                    "license_start_date",
                    "license_end_date",
                    "entitlement_pool_name",
                ],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-FromAppId": self.config.application_id,
                },
                "return_data": {"entitlement_pool_id": ("value",)},
                "auth": self.auth,
            },
            "ADD_FEATURE_GROUP": {
                "verb": "POST",
                "description": "Adds an feature group to a license model",
                "uri": partial(
                    "{endpoint}{service_path}/{license_model_id}/versions/{license_model_version_id}/feature-groups".format,
                    endpoint=self.config.sdc.SDC_BE_ONBOARD_ENDPOINT,
                    service_path=self.config.sdc.SDC_VENDOR_LICENSE_MODEL_PATH,
                ),
                "uri-parameters": ["license_model_id", "license_model_version_id"],
                "payload": "{}/feature_group.jinja".format(self.config.payload_directory),
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
                    "USER_ID": self.sdc_designer_user_id,
                    "X-FromAppId": self.config.application_id,
                },
                "return_data": {"feature_group_id": ("value",)},
                "auth": self.auth,
            },
            "ADD_LICENSE_AGREEMENT": {
                "verb": "POST",
                "description": "Adds an license agreement to a license model",
                "uri": partial(
                    "{endpoint}{service_path}/{license_model_id}/versions/{license_model_version_id}/license-agreements".format,
                    endpoint=self.config.sdc.SDC_BE_ONBOARD_ENDPOINT,
                    service_path=self.config.sdc.SDC_VENDOR_LICENSE_MODEL_PATH,
                ),
                "uri-parameters": ["license_model_id", "license_model_version_id"],
                "payload": "{}/license_agreement.jinja".format(self.config.payload_directory),
                "payload-parameters": ["feature_group_id", "license_agreement_name"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-FromAppId": self.config.application_id,
                },
                "return_data": {"license_agreement_id": ("value",)},
                "auth": self.auth,
            },
            "SUBMIT_LICENSE_MODEL": {
                "verb": "PUT",
                "description": "Submits a license model",
                "uri": partial(
                    "{endpoint}{service_path}/{license_model_id}/versions/{license_model_version_id}/actions".format,
                    endpoint=self.config.sdc.SDC_BE_ONBOARD_ENDPOINT,
                    service_path=self.config.sdc.SDC_VENDOR_LICENSE_MODEL_PATH,
                ),
                "uri-parameters": ["license_model_id", "license_model_version_id"],
                "payload": "{}/action.jinja".format(self.config.payload_directory),
                "payload-parameters": ["action"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-FromAppId": self.config.application_id,
                },
                "auth": self.auth,
            },
            "GET_LICENSE_MODEL": {
                "verb": "GET",
                "description": "Returns a license model",
                "uri": partial(
                    "{endpoint}{service_path}/{license_model_id}/versions/{license_model_version_id}".format,
                    endpoint=self.config.sdc.SDC_BE_ONBOARD_ENDPOINT,
                    service_path=self.config.sdc.SDC_VENDOR_LICENSE_MODEL_PATH,
                ),
                "uri-parameters": ["license_model_id", "license_model_version_id"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-FromAppId": self.config.application_id,
                },
                "return_data": {
                    "vendor_name": ("vendorName",),
                    "license_model_id": ("id",),
                    "description": ("description",),
                },
                "auth": self.auth,
            },
            "GET_LICENSE_MODEL_VERSION_ATTRIBUTE": {
                "verb": "GET",
                "description": "Returns an attribute for a license model (license-agreements, features-groups, etc...)",
                "uri": partial(
                    "{endpoint}{service_path}/{license_model_id}/versions/{license_model_version_id}/{attribute}".format,
                    endpoint=self.config.sdc.SDC_BE_ONBOARD_ENDPOINT,
                    service_path=self.config.sdc.SDC_VENDOR_LICENSE_MODEL_PATH,
                ),
                "uri-parameters": ["license_model_id", "license_model_version_id", "attribute"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-FromAppId": self.config.application_id,
                },
                "auth": self.auth,
            },
            "GET_LICENSE_MODEL_VERSIONS": {
                "verb": "GET",
                "description": "Returns the version list for a license model",
                "uri": partial(
                    "{endpoint}{service_path}/{license_model_id}/versions".format,
                    endpoint=self.config.sdc.SDC_BE_ONBOARD_ENDPOINT,
                    service_path=self.config.sdc.SDC_VENDOR_ITEMS_PATH,
                ),
                "uri-parameters": ["license_model_id"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-FromAppId": self.config.application_id,
                },
                "auth": self.auth,
            },
            "GET_LICENSE_MODELS": {
                "verb": "GET",
                "description": "Returns the full list of license models from SDC",
                "uri": partial(
                    "{endpoint}{service_path}?&itemType=vlm".format,
                    endpoint=self.config.sdc.SDC_BE_ONBOARD_ENDPOINT,
                    service_path=self.config.sdc.SDC_VENDOR_ITEMS_PATH,
                ),
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                    "X-FromAppId": self.config.application_id,
                },
                "return_data": {"results": ("results",)},
                "auth": self.auth,
            },
        }
