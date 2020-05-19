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

import responses
from onap_client.client.clients import Client
from onap_client.sdc.license_model import LicenseModel
from onap_client.tests.utils import mockup_catalog_item


@responses.activate
def test_license_model_create():
    oc = Client()

    LICENSE_MODEL_ID = "license_model_id"
    LICENSE_MODEL_VERSION_ID = "license_model_version_id"
    FEATURE_GROUP_ID = "feature_group_id"
    KEYGROUP_ID = "key_group_id"
    ENTITLEMENT_POOL_ID = "entitlement_pool_id"
    LICENSE_AGREEMENT_ID = "license_agreement_id"
    VENDOR_NAME = "vendor_name"
    ID = "id"
    DESCRIPTION = "description"

    mockup_catalog_item(
        oc.sdc.license_model.catalog_items["ADD_LICENSE_MODEL"],
        override_return_data={
            "itemId": LICENSE_MODEL_ID,
            "version": {"id": LICENSE_MODEL_VERSION_ID},
        },
    )

    mockup_catalog_item(
        oc.sdc.license_model.catalog_items["ADD_KEY_GROUP"],
        override_return_data={"value": KEYGROUP_ID},
        override_uri_params={
            "license_model_id": LICENSE_MODEL_ID,
            "license_model_version_id": LICENSE_MODEL_VERSION_ID,
        },
    )

    mockup_catalog_item(
        oc.sdc.license_model.catalog_items["ADD_ENTITLEMENT_POOL"],
        override_return_data={"value": ENTITLEMENT_POOL_ID},
        override_uri_params={
            "license_model_id": LICENSE_MODEL_ID,
            "license_model_version_id": LICENSE_MODEL_VERSION_ID,
        },
    )

    mockup_catalog_item(
        oc.sdc.license_model.catalog_items["ADD_FEATURE_GROUP"],
        override_return_data={"value": FEATURE_GROUP_ID},
        override_uri_params={
            "license_model_id": LICENSE_MODEL_ID,
            "license_model_version_id": LICENSE_MODEL_VERSION_ID,
        },
    )

    mockup_catalog_item(
        oc.sdc.license_model.catalog_items["ADD_LICENSE_AGREEMENT"],
        override_return_data={"value": LICENSE_AGREEMENT_ID},
        override_uri_params={
            "license_model_id": LICENSE_MODEL_ID,
            "license_model_version_id": LICENSE_MODEL_VERSION_ID,
        },
    )

    return_data = {"vendorName": VENDOR_NAME, "id": ID, "description": DESCRIPTION}
    mockup_catalog_item(
        oc.sdc.license_model.catalog_items["GET_LICENSE_MODEL"],
        override_return_data=return_data,
        override_uri_params={
            "license_model_id": LICENSE_MODEL_ID,
            "license_model_version_id": LICENSE_MODEL_VERSION_ID,
        },
    )

    lm = LicenseModel(
        VENDOR_NAME,
        "abc123",
        "entitlement_pool_name",
        "key_group_name",
        "feature_group_name",
        "license_agreement_name",
        "license_start_date",
        "license_end_date",
    )

    assert lm.tosca == return_data
