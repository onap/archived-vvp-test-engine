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

import uuid

from datetime import datetime, timedelta

from onap_client import exceptions
from onap_client.client.request import RequestHandler, APICatalogRequestObject


def make_request(catalog_item, attempts, verify_request, **kwargs):
    """Makes a request using by merging an APICatalogResource and
    kwargs to fill in the required parameters

    :catalog_item: APICatalogResource
    :kwargs: key/value to fill in data for APICatalogResource parameters

    :return: ResponseHandler object with response data from request
    """
    catalog_request = get_request_object(catalog_item, **kwargs)

    request_handler = RequestHandler(catalog_request)

    return request_handler.make_request(attempts, verify_request)


def get_request_object(catalog_item, **kwargs):
    request_input = validate_request(catalog_item, kwargs)

    return APICatalogRequestObject(catalog_item, **request_input)


def validate_request(catalog_item, kwargs):
    request_input = {}

    request_input["payload_parameters"] = validate_parameters(
        catalog_item.payload_parameters, kwargs
    )
    request_input["uri_parameters"] = validate_parameters(
        catalog_item.uri_parameters, kwargs
    )
    request_input["file_parameters"] = validate_parameters(
        catalog_item.file_parameters, kwargs
    )
    request_input["header_parameters"] = validate_parameters(
        catalog_item.header_parameters, kwargs
    )
    request_input["payload_path"] = validate_parameters(
        catalog_item.payload_path, kwargs
    )

    return request_input


def validate_parameters(catalog_item_parameters, kwargs):
    values = {}

    if not valid_input(catalog_item_parameters, kwargs.keys()):
        raise exceptions.MissingAttributeException(
            "Missing parameters for request {}".format(
                set(catalog_item_parameters) - set(kwargs.keys())
            )
        )
    else:
        for param in catalog_item_parameters:
            values[param] = kwargs.get(param)

    return values


def valid_input(required_attributes, input_attributes):
    return set(required_attributes).issubset(input_attributes)


def generate_dummy_string(start="", random_length=4):
    rand_string = str(uuid.uuid4())[0:random_length]
    return "{}{}".format(start, rand_string)


def generate_dummy_date(days=0):
    tmpdate = datetime.now() + timedelta(days=days)
    return "{}/{}/{}".format(
        "{:02d}".format(tmpdate.month), "{:02d}".format(tmpdate.day), tmpdate.year
    )
