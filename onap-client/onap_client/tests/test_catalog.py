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

from onap_client.client.clients import Client
from onap_client.tests.testdata import TestClient, CATALOG_RESOURCES, THIS_DIR  # noqa: F401


def test_catalog_items():
    c = Client()

    assert "MAKE_TEST_REQUEST" in c.test.catalog_items


def test_client_namespace():
    c = Client()

    assert hasattr(c, "test")


def test_client_catalog_resources():
    c = Client()

    assert c.test.catalog_resources == CATALOG_RESOURCES


def test_catalog_item_verb():
    c = Client()

    resource = c.test.catalog_items.get("MAKE_TEST_REQUEST")

    assert resource.verb == "POST"


def test_catalog_item_description():
    c = Client()

    resource = c.test.catalog_items.get("MAKE_TEST_REQUEST")

    assert resource.description == "Test Catalog Request"


def test_catalog_item_payload():
    c = Client()

    resource = c.test.catalog_items.get("MAKE_TEST_REQUEST")

    assert resource.payload == "{}/test_payload.jinja".format(THIS_DIR)


def test_catalog_item_uri_parameter():
    c = Client()

    resource = c.test.catalog_items.get("MAKE_TEST_REQUEST")

    assert "test_uri_parameter" in resource.uri_parameters


def test_catalog_item_payload_parameter():
    c = Client()

    resource = c.test.catalog_items.get("MAKE_TEST_REQUEST")

    assert "test_item_parameter" in resource.payload_parameters


def test_catalog_item_headers():
    c = Client()

    resource = c.test.catalog_items.get("MAKE_TEST_REQUEST")

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    assert resource.headers == headers


def test_catalog_item_auth():
    c = Client()

    resource = c.test.catalog_items.get("MAKE_TEST_REQUEST")

    auth = ("abc", "123")

    assert resource.auth == auth


def test_catalog_item_return_data():
    c = Client()

    resource = c.test.catalog_items.get("MAKE_TEST_REQUEST")

    assert "return_data_1" in resource.return_data
