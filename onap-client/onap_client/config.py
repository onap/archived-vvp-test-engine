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

import distutils.sysconfig
import logging as logger
import os
import yaml

PATH = "{}/onap_client".format(distutils.sysconfig.PREFIX)
PAYLOADS_DIR = "{}/payloads".format(PATH)
APPLICATION_ID = "robot-ete"
CONFIG_ENV = os.environ.get("OC_CONFIG")
CONFIG_FILE = CONFIG_ENV or "/etc/onap_client/config.yaml"


class Config:
    class ConfigClient:
        def __init__(self, config_dict):
            self.config = config_dict

        def __getattr__(self, attr):
            return self.config.get(attr, None)

    def __init__(self, config_file):
        self.config = {}
        self.config_file = config_file

    def __getattr__(self, attr):
        item = self.config.get(attr, None)
        if isinstance(item, str):
            return item
        elif isinstance(item, dict):
            return self.ConfigClient(item)
        else:
            return None

    def load(self, *keys):
        if self.config_file and self.config_file != "NONE":
            try:
                with open(self.config_file, "r") as f:
                    config_data = yaml.safe_load(f)
            except FileNotFoundError:
                logger.warn(
                    "Config file {} not found, using default".format(self.config_file)
                )
        else:
            with open("{}/config.yaml.example".format(PATH), "r") as f:
                config_data = yaml.safe_load(f)

        self.config = config_data
        for key in keys:
            self.config = self.config.get(key, {})


def load_config(config_file, *config_args):
    config = Config(config_file)
    config.load(*config_args)

    return config


APP_CONFIG = load_config(CONFIG_FILE, "onap_client")
LOG = logger
log_level = getattr(LOG, APP_CONFIG.LOG_LEVEL.upper())
LOG.basicConfig(format="%(asctime)s %(message)s", level=log_level)
