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
import onap_client
import pkgutil
import inspect
import sys
import os
import importlib

from abc import ABC, abstractmethod
from onap_client.lib import make_request
from onap_client import config

CACHED_MODULES = {}


def get_modules():
    catalog = sys.modules[__name__]
    if not catalog.CACHED_MODULES:
        catalog.CACHED_MODULES = import_submodules(onap_client)
    return catalog.CACHED_MODULES


class Catalog(ABC):
    """Abstract class for an ONAP client, automatically loads
    child classes as attributes."""

    class CallHandle:
        """Attached as an attribute for each catalog entry in a catalog.
        Used to make a request to ONAP."""

        def __init__(self, catalog_resource, verify=False):
            self.resource = catalog_resource
            self.verify_request = verify

        def __call__(self, **kwargs):
            return make_request(self.resource, self.verify_request, **kwargs)

    def __init__(self, config_file=None, **kwargs):
        """Iterates through all child classes and attaches them as attributes, named
        after the namespace property.

        If the child Catalog class has items in the
        catalog_resources property, they will be added as attributes to the child attribute
        as a CallHandle object.
        """
        if not config_file:
            config_file = os.environ.get("OC_CONFIG") or "/etc/onap_client/config.yaml"

        self.catalog_items = {}
        self.modules = get_modules()
        self._config_overrides = kwargs

        for cls in self.__class__.__subclasses__():
            subclass = cls(config_file=config_file, **kwargs)
            namespace = subclass.namespace
            catalog_resources = subclass.catalog_resources

            for k, v in catalog_resources.items():
                subclass.load(k, v)

            setattr(self, namespace, subclass)

        self.set_config(config_file)

    def load(self, item_name, resource_data, verify=False):
        """Consume a catalog resource entry as an APICatalogResource,
        and set it as an attribute on this.class as a CallHandle object"""
        resource = APICatalogResource(item_name, resource_data)

        self.catalog_items[item_name] = resource
        setattr(self, item_name.lower(), self.CallHandle(resource, verify=verify))

    @property
    @abstractmethod
    def namespace(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def catalog_resources(self):
        raise NotImplementedError

    @property
    def utility_functions(self):
        utility_functions = {}
        for module_name, module in self.modules.items():
            all_functions = inspect.getmembers(module, inspect.isfunction)
            for func in all_functions:
                function = func[1]
                if hasattr(function, "utility_function"):
                    utility_functions[func[0]] = func[1]
        return utility_functions

    def set_config(self, config_file):
        self.config = config.load_config(config_file, "onap_client")
        verify = self.config.REQUESTS_VERIFY
        for attr_name, attr in self.__dict__.items():
            if isinstance(attr, Catalog):
                attr.set_config(config_file)
                for k, v in attr.catalog_resources.items():
                    attr.load(k, v, verify=verify)

    def override(override_key):
        def decorator(func):
            def override_check(self):
                o = self._config_overrides.get(override_key)
                return o if o else func(self)
            return override_check
        return decorator


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


def import_submodules(package, recursive=True):
    """Import all the modules in onap-client, except for those starting
    with tests*. This is needed so that the Client object can register child classes"""
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + "." + name
        if full_name.find("tests") == -1:
            results[full_name] = importlib.import_module(full_name)
            if recursive and is_pkg:
                results.update(import_submodules(full_name))

    return results
