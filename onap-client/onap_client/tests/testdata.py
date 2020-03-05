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
from os.path import dirname, abspath

from onap_client.client.clients import Client

TEST_URI = "http://this.is.a.test.com"
THIS_DIR = dirname(abspath(__file__))


class TestClient(Client):
    @property
    def namespace(self):
        return "test"

    @property
    def catalog_resources(self):
        return CATALOG_RESOURCES


CATALOG_RESOURCES = {
    "MAKE_TEST_REQUEST": {
        "verb": "POST",
        "description": "Test Catalog Request",
        "uri": partial("{endpoint}/{test_uri_parameter}".format, endpoint=TEST_URI),
        "uri-parameters": ["test_uri_parameter"],
        "payload": "{}/test_payload.jinja".format(THIS_DIR),
        "payload-parameters": ["test_item_parameter"],
        "success_code": 200,
        "headers": {"Accept": "application/json", "Content-Type": "application/json"},
        "return_data": {
            "return_data_1": ("return_parameter_1",),
            "return_data_2": ("return_parameter_2",),
        },
        "auth": ("abc", "123"),
    },
    "MAKE_FILES_REQUEST": {
        "verb": "POST",
        "description": "Test Catalog Request With Files",
        "uri": partial("{endpoint}/{test_uri_parameter}".format, endpoint=TEST_URI),
        "uri-parameters": ["test_uri_parameter"],
        "files-parameters": ["file_path", "file_type"],
        "payload": "{}/test_payload.jinja".format(THIS_DIR),
        "payload-parameters": ["test_item_parameter"],
        "success_code": 200,
        "headers": {"Accept": "application/json", "Content-Type": "application/json"},
        "return_data": {
            "return_data_1": ("return_parameter_1",),
            "return_data_2": ("return_parameter_2",),
        },
        "auth": ("abc", "123"),
    },
}


RETURN_DATA = {"return_parameter_1": "abc", "return_parameter_2": "123"}
