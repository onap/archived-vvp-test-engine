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
from onap_client import sdc
from onap_client.tests.utils import mockup_client, mockup_catalog_item
from os.path import dirname, abspath

THIS_DIR = dirname(abspath(__file__))


@responses.activate
def test_vsp_create():
    oc = Client()

    LICENSE_MODEL_ID = "license_model_id"
    LICENSE_MODEL_VERSION_ID = "license_model_version_id"
    FEATURE_GROUP_ID = "feature_group_id"
    LICENSE_AGREEMENT_ID = "license_agreement_id"
    LICENSE_MODEL_NAME = "test"
    VSP_MODEL_ID = "software_product_id"
    VSP_MODEL_VERSION_ID = "software_product_version_id"
    VSP_NAME = "software_product_name"

    mockup_catalog_item(
        oc.sdc.license_model.catalog_items["GET_LICENSE_MODELS"],
        override_return_data={
            "results": [{"name": LICENSE_MODEL_NAME, "id": LICENSE_MODEL_ID}]
        },
    )
    mockup_catalog_item(
        oc.sdc.license_model.catalog_items["GET_LICENSE_MODEL_VERSIONS"],
        override_return_data={
            "results": [{"name": LICENSE_MODEL_NAME, "id": LICENSE_MODEL_VERSION_ID}]
        },
    )
    mockup_catalog_item(
        oc.sdc.license_model.catalog_items["GET_LICENSE_MODEL_VERSION_ATTRIBUTE"],
        override_return_data={
            "results": [{"name": LICENSE_MODEL_NAME, "id": FEATURE_GROUP_ID}]
        },
        override_uri_params={"attribute": "feature-groups"},
    )
    mockup_catalog_item(
        oc.sdc.license_model.catalog_items["GET_LICENSE_MODEL_VERSION_ATTRIBUTE"],
        override_return_data={
            "results": [{"name": LICENSE_MODEL_NAME, "id": LICENSE_AGREEMENT_ID}]
        },
        override_uri_params={"attribute": "license-agreements"},
    )

    mockup_catalog_item(
        oc.sdc.vsp.catalog_items["GET_SOFTWARE_PRODUCTS"],
        override_return_data={"results": []},
    )
    mockup_catalog_item(
        oc.sdc.vsp.catalog_items["ADD_SOFTWARE_PRODUCT"],
        override_return_data={
            "itemId": VSP_MODEL_ID,
            "version": {"id": VSP_MODEL_VERSION_ID},
        },
    )
    mockup_catalog_item(
        oc.sdc.vsp.catalog_items["GET_SOFTWARE_PRODUCT"],
        override_return_data={"name": VSP_NAME},
    )
    mockup_client(oc.sdc.vsp)

    vsp = sdc.vsp.VSP(
        "vendor_name",
        LICENSE_MODEL_NAME,
        "{}/test.zip".format(THIS_DIR),
        "application/zip",
        VSP_NAME,
        "description",
        "category",
        "sub_category",
        contributers=["test123"],
    )

    assert vsp.tosca == {"name": VSP_NAME}
