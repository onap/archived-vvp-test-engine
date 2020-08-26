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

import importlib
import logging
import onap_client
import pkgutil
import inspect
import sys

from onap_client.client.catalog import Catalog
from onap_client import config

CACHED_CLIENT = None


def get_client(config_file=None, **kwargs):
    clients = sys.modules[__name__]
    if not clients.CACHED_CLIENT or config_file:
        clients.CACHED_CLIENT = Client(config_file, **kwargs)
    return clients.CACHED_CLIENT


class Client(Catalog):
    """Base class for the ONAP client. Subclasses are dynamically
    loaded and added as attributes. Instantiate and use this class
    to interact with ONAP."""
    def __init__(self, config_file=None, **kwargs):
        self.config = config.APP_CONFIG
        self.modules = import_submodules(onap_client)
        self._config_overrides = kwargs

        super().__init__(**kwargs)

        if config_file:
            logging.debug("Overriding ONAP Client configuration: {}".format(config_file))
            self.set_config(config_file)

    @property
    def namespace(self):
        return "onap"

    @property
    def catalog_resources(self):
        return {}

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
        for attr_name, attr in self.__dict__.items():
            if isinstance(attr, Client):
                logging.debug("Reloading {} {}".format(attr_name, attr))
                attr.set_config(config_file)
                for k, v in attr.catalog_resources.items():
                    attr.load(k, v)

    def override(override_key):
        def decorator(func):
            def override_check(self):
                o = self._config_overrides.get(override_key)
                return o if o else func(self)
            return override_check
        return decorator


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
