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
import logging
import os
import yaml
from importlib_resources import files

from onap_client import etc


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
        if isinstance(item, (str, bool)):
            return item
        elif isinstance(item, dict):
            return self.ConfigClient(item)
        else:
            return None

    def load(self, *keys):
        config_data = {}

        if self.config_file and self.config_file != "NONE":
            try:
                with open(self.config_file, "r") as f:
                    config_data = yaml.safe_load(f)
            except FileNotFoundError:
                logging.debug(
                    "Config file {} not found, using default.".format(self.config_file)
                )

        if not config_data:
            with open(os.path.join(files(etc), "config.example.yaml"), "r") as f:
                config_data = yaml.safe_load(f)

        self.config = config_data
        for key in keys:
            self.config = self.config.get(key, {})

    @property
    def payload_directory(self):
        return os.path.join(files(etc), "payloads")

    @property
    def application_id(self):
        return "robot-ete"


def load_config(config_file, *config_args):
    config = Config(config_file)
    config.load(*config_args)

    return config
