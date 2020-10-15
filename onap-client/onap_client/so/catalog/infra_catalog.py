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

from onap_client.so.client import SOClient
from onap_client.util import utility
from onap_client.client.clients import get_client as Client


class ServiceInstantiationClient(SOClient):
    @property
    def namespace(self):
        return "infra"

    @property
    def catalog_resources(self):
        return {
            "GET_ACTIVE_REQUESTS": {
                "verb": "GET",
                "description": "Queries for the list of infraActiveRequests",
                "uri": partial(
                    "{endpoint}/infraActiveRequests?size={size}&sort=startTime,DESC".format,
                    endpoint=self.config.so.SO_ENDPOINT,
                ),
                "uri-parameters": ["size"],
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


@utility
def get_all_infra_requests(oc=None):
    if not oc:
        oc = Client()

    infra_data = oc.so.infra.get_active_requests(size="20").response_data

    total_elements = int(infra_data.get("page", {}).get("totalElements", 20))

    return oc.so.infra.get_active_requests(size=total_elements).response_data


@utility
def get_recent_infra_requests(size, oc=None):
    if not oc:
        oc = Client()

    return oc.so.infra.get_active_requests(size=size).response_data

