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
from functools import partial

from onap_client.sdnc.client import SDNCClient


class ConfigClient(SDNCClient):
    @property
    def namespace(self):
        return "configuration"

    @property
    def catalog_resources(self):
        return {
            "GET_SERVICE_INSTANCES": {
                "verb": "GET",
                "description": "Get a list of all service instances",
                "uri": partial(
                    "{endpoint}{service_path}/GENERIC-RESOURCE-API:services".format,
                    endpoint=self.config.sdnc.SDNC_ENDPOINT,
                    service_path=self.config.sdnc.SDNC_CONFIG_PATH,
                ),
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": self.auth,
            },
            "GET_SERVICE_INSTANCE": {
                "verb": "GET",
                "description": "Get details for a service instance",
                "uri": partial(
                    "{endpoint}{service_path}/GENERIC-RESOURCE-API:services/service/{service_instance_id}".format,
                    endpoint=self.config.sdnc.SDNC_ENDPOINT,
                    service_path=self.config.sdnc.SDNC_CONFIG_PATH,
                ),
                "uri-parameters": ["service_instance_id"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": self.auth,
            },
            "GET_VNF_INSTANCE": {
                "verb": "GET",
                "description": "Get details for a vnf instance",
                "uri": partial(
                    "{endpoint}{service_path}/GENERIC-RESOURCE-API:services/service/{service_instance_id}/service-data/vnfs/vnf/{vnf_instance_id}".format,
                    endpoint=self.config.sdnc.SDNC_ENDPOINT,
                    service_path=self.config.sdnc.SDNC_CONFIG_PATH,
                ),
                "uri-parameters": ["service_instance_id", "vnf_instance_id"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": self.auth,
            },
        }
