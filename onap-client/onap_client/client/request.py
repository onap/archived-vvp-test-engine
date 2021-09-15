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

import jinja2
import requests
import json
import os
import copy
import logging as logger

from onap_client.client.response import ResponseHandler
from onap_client.exceptions import FilesRequestFailure
from jinja2 import exceptions as jinja_exceptions
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class RequestHandler:
    """Handles a APICatalogRequestObject to make a request
    and returns a ResponseHandler object"""

    def __init__(self, request_object):
        """
        :request_object: APICatalogRequestObject
        """
        self.request_object = request_object

    def make_request(self, attempts, verify, proxies):
        r = Request(self.request_object)

        logger.info("Submitting request: {}".format(self.request_object.description))
        # TODO
        # Add verify to config file
        return ResponseHandler(r.request(attempts, proxies, verify=verify), self.request_object)


class Request:
    """Parses a APICatalogRequestObject to fill out the
    kwargs to send to the requests library"""

    def __init__(self, request_object):
        """
        :request_object: APICatalogRequestObject
        """
        self.request_object = request_object
        self.kwargs = {}
        self.response = None

        self.build_request()

    def build_request(self):
        request_object = self.request_object

        if request_object.verb:
            self.kwargs["method"] = request_object.verb

        if request_object.auth:
            self.kwargs["auth"] = request_object.auth

        if request_object.uri:
            self.kwargs["url"] = request_object.uri

        if request_object.headers:
            self.kwargs["headers"] = request_object.headers

        if request_object.payload:
            logger.info(self.kwargs.get("data"))
            self.kwargs["data"] = request_object.payload

        if request_object.files:
            self.kwargs["files"] = request_object.files

        debug_request = copy.deepcopy(self.kwargs)
        if "auth" in debug_request:
            debug_request["auth"] = "***********"

        try:
            logger.info(json.dumps(debug_request, indent=4))
        except TypeError:
            logger.info(debug_request)

    def request(self, attempts, proxies, verify=True):
        http = requests.Session()
        retry_strategy = Retry(
            total=attempts,
            backoff_factor=5,
            status_forcelist=[404, 429, 500, 501, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"],
            raise_on_status=False
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        logger.info(f"Using http proxy for request: {proxies}")

        return http.request(**self.kwargs, proxies=proxies, verify=verify, timeout=(6.05, int(os.environ.get("ONAP_CLIENT_TIMEOUT", 120))))


class APICatalogRequestObject:
    """Fills a APICatalogResource object with request-specific data"""

    def __init__(self, api_catalog_resource, **kwargs):
        """
        :api_catalog_resource: APICatalogResource object
        :kwargs: key/value to fill in APICatalogResource parameters
        """
        self.api_catalog_resource = api_catalog_resource
        self.payload_parameters = kwargs.get("payload_parameters", {})
        self.uri_parameters = kwargs.get("uri_parameters", {})
        self.header_parameters = kwargs.get("header_parameters", {})
        self.file_parameters = kwargs.get("file_parameters", {})
        if api_catalog_resource.payload_path:
            self.payload_path = kwargs.get("payload_path", {}).get(
                api_catalog_resource.payload_path[0]
            )

        self.uri = ""
        self.files = None
        self.payload = None
        self.verb = api_catalog_resource.verb
        self.headers = api_catalog_resource.headers
        self.success_code = api_catalog_resource.success_code
        self.return_data = api_catalog_resource.return_data
        self.auth = api_catalog_resource.auth
        self.description = api_catalog_resource.description

        if api_catalog_resource.payload or api_catalog_resource.payload_path:
            self.resolve_payload()

        if api_catalog_resource.file_parameters:
            self.resolve_files()

        if isinstance(self.headers, dict):
            for k, v in self.header_parameters.items():
                self.headers[k] = v

        self.resolve_uri()

    def resolve_files(self):
        file_type = self.file_parameters.get("file_type", "application/zip")
        file_path = self.file_parameters.get("file_path")
        if not file_path:
            raise FilesRequestFailure("File path was not provided")

        try:
            with open(file_path, "rb") as f:
                data = f.read()
        except IOError:
            logger.error("file {} was not found".format(file_path))
            raise

        file_name = os.path.basename(file_path)

        self.files = {"upload": [file_name, data, file_type]}

    def resolve_payload(self):
        try:
            if self.api_catalog_resource.payload_path:
                with open(self.payload_path, "r") as f:
                    self.payload = f.read()
            else:
                with open(self.api_catalog_resource.payload, "r") as f:
                    self.payload = jinja2.Template(f.read()).render(
                        **self.payload_parameters
                    )
        except jinja_exceptions.TemplateNotFound:
            logger.error(
                "{} file not found. Check payloads directory.".format(self.payload)
            )
            raise
        except FileNotFoundError:
            logger.error(
                "{} file not found. Check payloads directory.".format(self.payload)
            )
            raise

    def resolve_uri(self):
        try:
            self.uri = self.api_catalog_resource.uri(**self.uri_parameters)
        except KeyError:
            logger.error("invalid uri keys {}.".format(self.uri_parameters))
            raise
