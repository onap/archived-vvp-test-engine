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
from onap_client import aai
from onap_client.client.clients import Client
from onap_client import config

aai_properties = aai.AAI_PROPERTIES
application_id = config.APPLICATION_ID


class AAIClient(Client):
    @property
    def namespace(self):
        return "aai"

    @property
    def catalog_resources(self):
        return CATALOG_RESOURCES


CATALOG_RESOURCES = {
    "HEALTH_CHECK": {
        "verb": "GET",
        "description": "Queries AAI health check endpoint",
        "uri": partial(
            "{endpoint}{service_path}".format,
            endpoint=aai_properties.AAI_BE_ENDPOINT,
            service_path=aai_properties.AAI_HEALTH_CHECK_PATH,
        ),
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (aai_properties.AAI_USERNAME, aai_properties.AAI_PASSWORD,),
    },
}
