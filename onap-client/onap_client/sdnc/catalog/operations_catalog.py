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


class OperationsClient(SDNCClient):
    @property
    def namespace(self):
        return "operations"

    @property
    def catalog_resources(self):
        return {
            "GR_API_PRELOAD": {
                "verb": "POST",
                "description": "Upload a GR API preload to SDNC",
                "uri": partial(
                    "{endpoint}{service_path}/GENERIC-RESOURCE-API:preload-vf-module-topology-operation".format,
                    endpoint=self.config.sdnc.SDNC_ENDPOINT,
                    service_path=self.config.sdnc.SDNC_OPERATIONS_PATH,
                ),
                "payload-path": ["preload_path"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (self.config.sdnc.SDNC_USERNAME, self.config.sdnc.SDNC_PASSWORD,),
            },
            "VNF_API_PRELOAD": {
                "verb": "POST",
                "description": "Upload a VNF API preload to SDNC",
                "uri": partial(
                    "{endpoint}{service_path}/VNF-API:preload-vnf-topology-operation".format,
                    endpoint=self.config.sdnc.SDNC_ENDPOINT,
                    service_path=self.config.sdnc.SDNC_OPERATIONS_PATH,
                ),
                "payload-path": ["preload_path"],
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (self.config.sdnc.SDNC_USERNAME, self.config.sdnc.SDNC_PASSWORD,),
            },
        }
