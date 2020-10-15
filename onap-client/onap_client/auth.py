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
from importlib import import_module
from requests.auth import HTTPBasicAuth, AuthBase
from inspect import getmembers, isclass
from functools import lru_cache

from onap_client.exceptions import AuthClassNotFound, AuthModuleNotDefined


@lru_cache()
def auth_handler(auth_plugin_config, username, password):
    if not auth_plugin_config:
        return HTTPBasicAuth(username, password)

    if not auth_plugin_config.get("AUTH_MODULE"):
        raise AuthModuleNotDefined("Property AUTH_MODULE was not defined in configuration file.")

    auth_module = import_module(auth_plugin_config.get("AUTH_MODULE"))

    auth_class = get_auth_class(auth_module)

    return auth_class(username, password, **auth_plugin_config)


def get_auth_class(auth_module):
    """
    Returns first Class definition in auth_module that inherits from AuthBase.
    """
    for name, obj in getmembers(
        auth_module,
        lambda x: isclass(x) and issubclass(x, AuthBase) and x != AuthBase
    ):
        return obj

    raise AuthClassNotFound("No auth class found in module: {}".format(auth_module))
