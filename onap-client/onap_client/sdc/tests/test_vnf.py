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
from onap_client.sdc.vnf import VNF
from onap_client.sdc.vnf import (
    instance_ids_for_property,
    network_role_property_for_instance,
)


@responses.activate
def test_vnf_create():
    oc = Client()

    SOFTWARE_PRODUCT_NAME = "software_product_name"
    SOFTWARE_PRODUCT_ID = "software_product_id"
    SOFTWARE_PRODUCT_VERSION_ID = "software_product_version_id"
    VNF_NAME = "vnf_name"
    RESOURCE_TYPE = "VF"
    CATALOG_RESOURCE_ID = "catalog_resource_id"

    return_data = {
        "uniqueId": CATALOG_RESOURCE_ID,
        "componentInstancesInputs": {
            "instance_id1": [
                {"name": "vm_type_tag", "value": "red"},
                {"name": "nf_role", "value": "dfankafd"},
            ]
        },
        "name": VNF_NAME,
    }
    mockup_catalog_item(
        oc.sdc.vsp.catalog_items["GET_SOFTWARE_PRODUCTS"],
        override_return_data={
            "results": [{"name": SOFTWARE_PRODUCT_NAME, "id": SOFTWARE_PRODUCT_ID}]
        },
    )
    mockup_catalog_item(
        oc.sdc.vsp.catalog_items["GET_SOFTWARE_PRODUCT_VERSIONS"],
        override_return_data={
            "results": [
                {"name": SOFTWARE_PRODUCT_NAME, "id": SOFTWARE_PRODUCT_VERSION_ID}
            ]
        },
        override_uri_params={"software_product_id": SOFTWARE_PRODUCT_ID},
    )
    mockup_catalog_item(
        oc.sdc.vsp.catalog_items["GET_SOFTWARE_PRODUCT"],
        override_return_data={
            "vendorName": "vendor_name",
            "category": "resourceNewCategory.application l4+",
            "subCategory": "resourceNewCategory.application l4+.web server",
        },
        override_uri_params={
            "software_product_id": SOFTWARE_PRODUCT_ID,
            "software_product_version_id": SOFTWARE_PRODUCT_VERSION_ID,
        },
    )
    mockup_catalog_item(
        oc.sdc.vnf.catalog_items["GET_RESOURCES"],
        override_return_data={"resources": []},
    )
    mockup_catalog_item(
        oc.sdc.vnf.catalog_items["ADD_CATALOG_RESOURCE"],
        override_return_data=return_data,
    )
    mockup_catalog_item(
        oc.sdc.vnf.catalog_items["GET_CATALOG_RESOURCE"],
        override_return_data=return_data,
        override_uri_params={"catalog_resource_id": CATALOG_RESOURCE_ID},
    )
    mockup_catalog_item(
        oc.sdc.vnf.catalog_items["CERTIFY_CATALOG_RESOURCE"],
        override_return_data=return_data,
        override_uri_params={"catalog_resource_id": CATALOG_RESOURCE_ID},
    )
    mockup_catalog_item(
        oc.sdc.vnf.catalog_items["ADD_CATALOG_RESOURCE_PROPERTY"],
        override_uri_params={
            "catalog_resource_id": CATALOG_RESOURCE_ID,
            "catalog_resource_instance_id": "instance_id1",
        },
    )
    mockup_catalog_item(
        oc.sdc.catalog_items["GET_RESOURCE_CATEGORIES"],
        override_return_data=[
            {
                "name": "Application L4+",
                "normalizedName": "application l4+",
                "uniqueId": "resourceNewCategory.application l4+",
                "icons": False,
                "subcategories": [
                    {
                        "name": "Call Control",
                        "normalizedName": "call control",
                        "uniqueId": "resourceNewCategory.application l4+.call control",
                        "icons": ["call_controll"],
                        "groupings": False,
                        "version": False,
                        "ownerId": False,
                        "empty": False,
                        "type": False
                    }
                ]
            }
        ],
    )

    vnf = VNF(
        software_product_name=SOFTWARE_PRODUCT_NAME,
        vnf_name=VNF_NAME,
        resource_type=RESOURCE_TYPE,
        vm_types=[{"vm_type": "red", "properties": {"nf_role": "blue"}}],
    )
    vnf.create()
    vnf._submit()

    assert "componentInstancesInputs" in vnf.tosca


def test_instance_ids_for_property():
    vnf_model = {
        "componentInstancesInputs": {
            "item1id": [
                {"name": "vm_type", "value": "db"},
                {"name": "otherprop", "value": "otherval"},
            ],
            "item2id": [
                {"name": "vm_type", "value": "db"},
                {"name": "otherprop", "value": "otherval"},
            ],
        }
    }

    ids = instance_ids_for_property(vnf_model, "vm_type", "db")

    assert "item1id" in ids and "item2id" in ids


def test_network_role_property_for_instance():
    vnf_model = {
        "componentInstancesInputs": {
            "item1id": [
                {"name": "vm_type", "value": "db"},
                {"name": "item1id.port123.oam.network_role_tag", "value": "oam"},
                {
                    "name": "item1id.port123.oam.network_role",
                    "value": "ACTUALNETWORKROLE",
                },
            ],
            "item2id": [
                {"name": "vm_type", "value": "db"},
                {"name": "otherprop", "value": "otherval"},
            ],
        }
    }

    prop = network_role_property_for_instance("oam", vnf_model, "item1id")

    assert "item1id.port123.oam.network_role" in prop
