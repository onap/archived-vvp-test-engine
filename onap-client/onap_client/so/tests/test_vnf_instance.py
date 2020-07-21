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
from onap_client.so.vnf_instance import VNFInstance


@responses.activate
def test_vnf_instance():
    oc = Client()

    SERVICE_MODEL_NAME = "service_model_name"
    SERVICE_MODEL_ID = "service_model_id"
    SERVICE_MODEL_INVARIANT_ID = "service_model_invariant_id"
    SERVICE_INSTANCE_NAME = "service_instance_name"
    SERVICE_INSTANCE_ID = "service_instance_id"
    SERVICE_INSTANCE_INVARIANT_ID = "service_instance_invariant_id"
    SERVICE_INSTANCE_VERSION = "service_instance_version"
    SERVICE_INSTANCE_UUID = "service_instance_uuid"

    VNF_MODEL_NAME = "vnf_model_name"
    VNF_INSTANCE_NAME = "vnf_instance_name"
    VNF_CUSTOMIZATION_UUID = "vnf_customization_uuid"
    VNF_INVARIANT_ID = "vnf_invariant_id"
    VNF_ACTUAL_UUID = "vnf_actual_uuid"
    VNF_VERSION = "vnf_version"

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
                    "lastUpdateDate": 123456,
                }
            ]
        },
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
        oc.sdc.service.catalog_items["GET_SDC_SERVICE"],
        override_uri_params={"catalog_service_id": SERVICE_MODEL_ID},
        override_return_data={
            "invariantUUID": SERVICE_MODEL_INVARIANT_ID,
            "uniqueId": SERVICE_MODEL_ID,
            "componentInstances": [
                {
                    "componentName": VNF_MODEL_NAME,
                    "customizationUUID": VNF_CUSTOMIZATION_UUID,
                    "actualComponentUid": VNF_ACTUAL_UUID,
                    "componentVersion": VNF_VERSION
                }
            ]
        }
    )
    mockup_catalog_item(
        oc.sdc.vnf.catalog_items["GET_CATALOG_RESOURCE"],
        override_return_data={
            "invariantUUID": VNF_INVARIANT_ID
        },
        override_uri_params={"catalog_resource_id": VNF_ACTUAL_UUID},
    )
    mockup_catalog_item(
        oc.sdnc.config.catalog_items["GET_SERVICE_INSTANCES"],
        override_return_data={
            "services": {
                "service": [
                    {
                        "service-data": {
                            "service-request-input": {
                                "service-instance-name": SERVICE_INSTANCE_NAME
                            },
                            "service-information": {
                                "onap-model-information": {
                                    "model-invariant-uuid": SERVICE_INSTANCE_INVARIANT_ID,
                                    "model-uuid": SERVICE_INSTANCE_UUID,
                                    "model-version": SERVICE_INSTANCE_VERSION,
                                    "model-name": SERVICE_MODEL_NAME,
                                }
                            }
                        },
                        "service-instance-id": SERVICE_INSTANCE_ID
                    }
                ]
            }
        },
    )
    mockup_catalog_item(
        oc.so.service_instantiation.catalog_items["CREATE_VNF_INSTANCE"],
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

    vnfi = VNFInstance(
        vnf_instance_name=VNF_INSTANCE_NAME,
        service_instance_name=SERVICE_INSTANCE_NAME,
        requestor_id="cs0008",
        model_name=VNF_MODEL_NAME,
        tenant_name=TENANT_NAME,
        cloud_owner=CLOUD_OWNER,
        cloud_region=CLOUD_REGION,
        api_type="GR_API",
        platform="platform",
        line_of_business="lob"
    )
    vnfi.create()

    assert vnfi.vnf_instance_name == VNF_INSTANCE_NAME
