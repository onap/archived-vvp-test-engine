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
import json
import os
import sys

from io import StringIO

from onap_client.client.clients import Client
from onap_client.client.request import APICatalogRequestObject

from onap_client.tests.testdata import (
    THIS_DIR,
    RETURN_DATA,
)
from onap_client.tests.testdata import TestClient  # noqa: F401
from onap_client.cli import main

DUMMY_PARAM = "dummy_param"


def test_request_uri():
    c = Client()

    resource = c.test.catalog_items.get("MAKE_FILES_REQUEST")

    request_object = create_request_object(resource)

    assert request_object.uri == "http://this.is.a.test.com/{}".format(DUMMY_PARAM)


def test_payload():
    c = Client()

    resource = c.test.catalog_items.get("MAKE_FILES_REQUEST")

    request_object = create_request_object(resource)

    assert json.loads(request_object.payload) == {"test_item_parameter": DUMMY_PARAM}


def test_files():
    c = Client()

    resource = c.test.catalog_items.get("MAKE_FILES_REQUEST")

    request_object = create_request_object(resource)

    file_path = "{}/test.zip".format(THIS_DIR)
    with open(file_path, "rb") as f:
        data = f.read()
    file_name = os.path.basename(file_path)
    files = {"upload": [file_name, data, "application/zip"]}
    assert request_object.files == files


@responses.activate
def test_make_request():
    responses.add(
        responses.POST,
        "http://this.is.a.test.com/{}".format(DUMMY_PARAM),
        json=RETURN_DATA,
    )

    c = Client()

    params = {"test_item_parameter": DUMMY_PARAM, "test_uri_parameter": DUMMY_PARAM}

    resp = c.test.make_test_request(**params)

    assert resp.response_data == RETURN_DATA


def test_cli():
    cli_string = ["test", "--help"]
    temp_out = StringIO()
    sys.stdout = temp_out

    main(*cli_string)

    sys.stdout.seek(0)
    output = sys.stdout.read()

    sys.stdout = sys.__stdout__

    assert output.find("make-test-request") != -1


def test_cli_request_help():
    cli_string = ["test", "make-test-request", "--help"]
    temp_out = StringIO()
    sys.stdout = temp_out

    main(*cli_string)
    sys.stdout.seek(0)
    output = sys.stdout.read()

    sys.stdout = sys.__stdout__

    assert output.find("--test-item-parameter") != -1


@responses.activate
def test_cli_request():
    temp_out = StringIO()
    sys.stdout = temp_out

    responses.add(
        responses.POST,
        "http://this.is.a.test.com/{}".format(DUMMY_PARAM),
        json=RETURN_DATA,
    )

    cli_string = [
        "test",
        "make-test-request",
        "--test-item-parameter",
        DUMMY_PARAM,
        "--test-uri-parameter",
        DUMMY_PARAM,
    ]

    main(*cli_string)

    sys.stdout.seek(0)
    output = sys.stdout.read()

    sys.stdout = sys.__stdout__

    assert json.loads(output) == RETURN_DATA


def create_request_object(catalog_item):
    payload_input = {}
    uri_input = {}
    file_input = {}

    for param in catalog_item.payload_parameters:
        payload_input[param] = DUMMY_PARAM

    for param in catalog_item.uri_parameters:
        uri_input[param] = DUMMY_PARAM

    file_input["file_path"] = "{}/test.zip".format(THIS_DIR)

    return APICatalogRequestObject(
        catalog_item,
        payload_parameters=payload_input,
        uri_parameters=uri_input,
        file_parameters=file_input,
    )
