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

from onap_client.tests.utils import mockup_catalog_item
from onap_client.client.clients import Client
from onap_client.sdc.service import Service


@responses.activate
def test_vnf_create():
    oc = Client()

    VNF_NAME = "vnf_name"
    SERVICE_MODEL_ID = "service_model_id"
    VNF_RESOURCE_ID = "vnf_resource_id"
    SERVICE_NAME = "service_name"

    mockup_catalog_item(
        oc.sdc.service.catalog_items["GET_SERVICES"],
        override_return_data={
            "services": []
        },
    )
    mockup_catalog_item(
        oc.sdc.service.catalog_items["ADD_CATALOG_SERVICE"],
        override_return_data={
            "uniqueId": SERVICE_MODEL_ID
        },
    )
    mockup_catalog_item(
        oc.sdc.service.catalog_items["ADD_RESOURCE_INSTANCE"],
        override_uri_params={"catalog_service_id": SERVICE_MODEL_ID},
        override_return_data={
            "uniqueId": VNF_RESOURCE_ID
        },
    )
    mockup_catalog_item(
        oc.sdc.service.catalog_items["CHECKIN_SERVICE"],
        override_uri_params={"catalog_service_id": SERVICE_MODEL_ID},
    )
    mockup_catalog_item(
        oc.sdc.service.catalog_items["REQUEST_SERVICE_CERTIFICATION"],
        override_uri_params={"catalog_service_id": SERVICE_MODEL_ID},
    )
    mockup_catalog_item(
        oc.sdc.service.catalog_items["START_SERVICE_CERTIFICATION"],
        override_uri_params={"catalog_service_id": SERVICE_MODEL_ID},
    )
    mockup_catalog_item(
        oc.sdc.service.catalog_items["FINISH_SERVICE_CERTIFICATION"],
        override_uri_params={"catalog_service_id": SERVICE_MODEL_ID},
        override_return_data={"uniqueId": SERVICE_MODEL_ID}
    )
    mockup_catalog_item(
        oc.sdc.service.catalog_items["APPROVE_SERVICE_CERTIFICATION"],
        override_uri_params={"catalog_service_id": SERVICE_MODEL_ID},
    )
    mockup_catalog_item(
        oc.sdc.service.catalog_items["DISTRIBUTE_SDC_SERVICE"],
        override_uri_params={"catalog_service_id": SERVICE_MODEL_ID},
    )
    mockup_catalog_item(
        oc.sdc.service.catalog_items["GET_SDC_SERVICE"],
        override_uri_params={"catalog_service_id": SERVICE_MODEL_ID},
        override_return_data={
            "uniqueId": SERVICE_MODEL_ID,
        }
    )

    service = Service(
        instantiation_type="A-la-carte",
        service_name=SERVICE_NAME,
        contact_id="cs0008",
        category_name="Network L1-3",
        tag="robot",
        project_code="123456",
        environment_context="General_Revenue-Bearing",
        ecomp_generated_naming="true",
        description="This is a test",
        resources=[{
            "resource_name": VNF_NAME,
            "resource_id": VNF_RESOURCE_ID,
            "catalog_resource_name": VNF_NAME,
            "origin_type": "VF",
            "properties": {}
        }],
        allow_update=False,
        wait_for_distribution=False
    )
    service.create()
    service._submit()

    assert service.service_name == SERVICE_NAME
