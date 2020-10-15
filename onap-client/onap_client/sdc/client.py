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
from frozendict import frozendict

from functools import partial

from onap_client.client.clients import Client
from onap_client.auth import auth_handler


class SDCClient(Client):
    @property
    def namespace(self):
        return "sdc"

    @property
    def catalog_resources(self):
        return {
            "HEALTH_CHECK": {
                "verb": "GET",
                "description": "Queries SDC health check endpoint",
                "uri": partial(
                    "{endpoint}{service_path}".format,
                    endpoint=self.config.sdc.SDC_HC_ENDPOINT,
                    service_path=self.config.sdc.SDC_HEALTH_CHECK_PATH,
                ),
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.config.sdc.SDC_DESIGNER_USER_ID,
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": self.auth,
            },
            "GET_RESOURCE_CATEGORIES": {
                "verb": "GET",
                "description": "Queries SDC for resource categories",
                "uri": partial(
                    "{endpoint}{service_path}".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_RESOURCE_CATEGORIES_PATH,
                ),
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_designer_user_id,
                },
                "auth": self.auth,
            },
            "ADD_USER": {
                "verb": "POST",
                "description": "Add a user to SDC.",
                "uri": partial(
                    "{endpoint}{service_path}".format,
                    endpoint=self.config.sdc.SDC_BE_ENDPOINT,
                    service_path=self.config.sdc.SDC_USER_PATH,
                ),
                "payload": "{}/sdc_add_user.jinja".format(self.config.payload_directory),
                "payload-parameters": ["first_name", "last_name", "user_id", "email", "role"],
                "success_code": 201,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "USER_ID": self.sdc_ops_user_id,
                },
                "auth": self.auth,
            },
        }

    @property
    @Client.override("global_sdc_username")
    def global_sdc_username(self):
        """Username to authenticate to SDC"""
        return self.config.sdc.GLOBAL_SDC_USERNAME

    @property
    @Client.override("global_sdc_password")
    def global_sdc_password(self):
        """Password to authenticate to SDC"""
        return self.config.sdc.GLOBAL_SDC_PASSWORD

    @property
    @Client.override("sdc_designer_user_id")
    def sdc_designer_user_id(self):
        """Designer role User ID"""
        return self.config.sdc.SDC_DESIGNER_USER_ID

    @property
    @Client.override("sdc_tester_user_id")
    def sdc_tester_user_id(self):
        """Tester role User ID"""
        return self.config.sdc.SDC_TESTER_USER_ID

    @property
    @Client.override("sdc_ops_user_id")
    def sdc_ops_user_id(self):
        """Ops role User ID"""
        return self.config.sdc.SDC_OPS_USER_ID

    @property
    @Client.override("sdc_governor_user_id")
    def sdc_governor_user_id(self):
        """Ops role User ID"""
        return self.config.sdc.SDC_GOVERNOR_USER_ID

    @property
    def auth(self):
        return auth_handler(
            frozendict(self.config.sdc.AUTH_PLUGIN) if self.config.sdc.AUTH_PLUGIN else None,
            self.global_sdc_username,
            self.global_sdc_password,
        )
