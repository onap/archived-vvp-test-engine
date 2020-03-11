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

from abc import ABC, abstractmethod
from onap_client.lib import make_request


class Catalog(ABC):
    """Abstract class for an ONAP client, automatically loads
    child classes as attributes."""

    class CallHandle:
        """Attached as an attribute for each catalog entry in a catalog.
        Used to make a request to ONAP."""

        def __init__(self, catalog_resource):
            self.resource = catalog_resource

        def __call__(self, **kwargs):
            return make_request(self.resource, **kwargs)

    def __init__(self):
        """Iterates through all child classes and attaches them as attributes, named
        after the namespace property.

        If the child Catalog class has items in the
        catalog_resources property, they will be added as attributes to the child attribute
        as a CallHandle object.
        """
        self.catalog_items = {}

        for cls in self.__class__.__subclasses__():
            subclass = cls()
            namespace = subclass.namespace
            catalog_resources = subclass.catalog_resources

            for k, v in catalog_resources.items():
                subclass.load(k, v)

            setattr(self, namespace, subclass)

    def load(self, item_name, resource_data):
        """Consume a catalog resource entry as an APICatalogResource,
        and set it as an attribute on this.class as a CallHandle object"""
        resource = APICatalogResource(item_name, resource_data)

        self.catalog_items[item_name] = resource
        setattr(self, item_name.lower(), self.CallHandle(resource))

    @property
    @abstractmethod
    def namespace(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def catalog_resources(self):
        raise NotImplementedError


class APICatalogResource:
    """Class representation of a single catalog entry"""

    def __init__(self, catalog_resource_name, resource_data):
        """
        :catalog_resource_name: name of the catalog resource
        :resource_data: dictionary containing catalog resource attributes
        """
        self.catalog_resource_name = catalog_resource_name
        self.catalog_resource_data = resource_data

    @property
    def verb(self):
        return self.catalog_resource_data.get("verb", None)

    @property
    def description(self):
        return self.catalog_resource_data.get("description", None)

    @property
    def uri(self):
        return self.catalog_resource_data.get("uri", None)

    @property
    def payload(self):
        return self.catalog_resource_data.get("payload", None)

    @property
    def uri_parameters(self):
        return self.catalog_resource_data.get("uri-parameters", [])

    @property
    def payload_parameters(self):
        return self.catalog_resource_data.get("payload-parameters", [])

    @property
    def payload_path(self):
        return self.catalog_resource_data.get("payload-path", [])

    @property
    def file_parameters(self):
        return self.catalog_resource_data.get("files-parameters", [])

    @property
    def header_parameters(self):
        return self.catalog_resource_data.get("header_parameters", [])

    @property
    def success_code(self):
        return self.catalog_resource_data.get("success_code", None)

    @property
    def headers(self):
        return self.catalog_resource_data.get("headers", None)

    @property
    def return_data(self):
        return self.catalog_resource_data.get("return_data", {})

    @property
    def auth(self):
        return self.catalog_resource_data.get("auth", None)
