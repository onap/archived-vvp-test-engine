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

import simplejson
import logging

logger = logging.getLogger("ONAP_CLIENT")


class ResponseHandler:
    """Handles a response from the requests library,
    and compares it to the APICatalogRequestObject that was used to make the request.
    If the request object has return_data, then it will parse the response
    object and add the return data as an attribute."""

    def __init__(self, response, request_object):
        """
        :response: requests.response
        :request_object: APICatalogRequestObject
        """
        self.response = response
        self.request_object = request_object
        self.response_data = {}
        self.status_code = None
        self.success = False

        self.validate_response()

    def validate_response(self):
        response = self.response
        if self.request_object.success_code != response.status_code:
            response_data = response.text
            logger.error(
                "Request failed with code {} and data {}".format(
                    response.status_code, response_data
                )
            )
        else:
            logger.info("Request was successful")
            self.success = True
            try:
                response_data = response.json()
                for (
                    response_key,
                    response_items,
                ) in self.request_object.return_data.items():
                    response_value = response_iterator(response_data, *response_items)
                    if response_value:
                        setattr(self, response_key, response_value)
            except simplejson.errors.JSONDecodeError:
                response_data = response.text

        logger.debug("{}\n".format(response_data))

        self.response_data = response_data
        self.status_code = response.status_code


def response_iterator(response_content, *keys):
    """helper function to search a response for return_data keys"""
    props = list(keys)

    key = props.pop(0)
    prop = response_content.get(key, None)

    if isinstance(prop, str) or len(props) <= 0:
        return prop
    elif isinstance(prop, list):
        if isinstance(key, int):
            return response_iterator(prop[key], *props)
        else:
            for x in prop:
                return response_iterator(x, *props)
    elif isinstance(prop, dict):
        return response_iterator(prop, *props)
    else:
        return None
