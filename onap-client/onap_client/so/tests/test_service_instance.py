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
from onap_client.tests.utils import mockup_catalog_item
from onap_client.so.service_instance import ServiceInstance


@responses.activate
def test_service_instance():
    oc = Client()

    SERVICE_MODEL_NAME = "service_model"
    SERVICE_MODEL_ID = "service_model_id"
    SERVICE_MODEL_INVARIANT_ID = "service_model_invariant_id"
    SERVICE_INSTANCE_NAME = "SERVICE_INSTANCE_NAME"
    OWNING_ENTITY_NAME = "owning_entity"
    OWNING_ENTITY_ID = "owning_entity_id"
    CLOUD_OWNER = "cloud_owner"
    CLOUD_REGION = "cloud_region"
    TENANT_NAME = "tenant_name"
    TENANT_ID = "tenant_id"
    REQUEST_ID = "request_id"

    mockup_catalog_item(
        oc.sdc.service.catalog_items["GET_SERVICES"],
        override_return_data={
            "services": [
                {
                    "name": SERVICE_MODEL_NAME,
                    "uniqueId": SERVICE_MODEL_ID,
                    "lastUpdateDate": 123456
                }
            ]
        },
    )
    mockup_catalog_item(
        oc.sdc.service.catalog_items["GET_SDC_SERVICE"],
        override_uri_params={"catalog_service_id": SERVICE_MODEL_ID},
        override_return_data={"invariantUUID": SERVICE_MODEL_INVARIANT_ID, "uniqueId": SERVICE_MODEL_ID}
    )
    mockup_catalog_item(
        oc.aai.cloud_infrastructure.catalog_items["GET_CLOUD_REGION_TENANTS"],
        override_uri_params={"cloud_owner": CLOUD_OWNER, "cloud_region": CLOUD_REGION},
        override_return_data={
            "tenant": [
                {
                    "tenant-name": TENANT_NAME,
                    "tenant-id": TENANT_ID
                }
            ],
        }
    )
    mockup_catalog_item(
        oc.vid.maintenance.catalog_items["GET_CATEGORY_PARAMETERS"],
        override_return_data={
            "categoryParameters": {
                "owningEntity": [
                    {
                        "name": OWNING_ENTITY_NAME,
                        "id": OWNING_ENTITY_ID
                    }
                ]
            },
        }
    )
    mockup_catalog_item(
        oc.so.service_instantiation.catalog_items["CREATE_SERVICE_INSTANCE"],
        override_return_data={
            "requestReferences": {
                "requestId": REQUEST_ID
            }
        }
    )
    mockup_catalog_item(
        oc.so.service_instantiation.catalog_items["GET_REQUEST_STATUS"],
        override_uri_params={"request_id": REQUEST_ID},
        override_return_data={
            "request": {
                "requestStatus": {
                    "requestState": "COMPLETE"
                }
            }
        }
    )

    si = ServiceInstance(
        service_instance_name=SERVICE_INSTANCE_NAME,
        requestor_id="cs0008",
        model_name=SERVICE_MODEL_NAME,
        model_version="1.0",
        tenant_name=TENANT_NAME,
        cloud_owner=CLOUD_OWNER,
        cloud_region=CLOUD_REGION,
        api_type="GR_API",
        service_type="ONAPSERVICE",
        customer_name="ONAPCUSTOMER",
        project_name="ONAPPROJECT",
        owning_entity_name=OWNING_ENTITY_NAME
    )
    si.create()

    assert si.service_instance_name == SERVICE_INSTANCE_NAME
