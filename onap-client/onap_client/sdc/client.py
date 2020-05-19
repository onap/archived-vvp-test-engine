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
from onap_client import sdc
from onap_client.client.clients import Client
from onap_client import config

sdc_properties = sdc.SDC_PROPERTIES
application_id = config.APPLICATION_ID


class SDCClient(Client):
    @property
    def namespace(self):
        return "sdc"

    @property
    def catalog_resources(self):
        return CATALOG_RESOURCES


CATALOG_RESOURCES = {
    "HEALTH_CHECK": {
        "verb": "GET",
        "description": "Queries SDC health check endpoint",
        "uri": partial(
            "{endpoint}{service_path}".format,
            endpoint=sdc_properties.SDC_HC_ENDPOINT,
            service_path=sdc_properties.SDC_HEALTH_CHECK_PATH,
        ),
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
            "X-TransactionId": str(uuid.uuid4()),
            "X-FromAppId": application_id,
        },
        "auth": (
            sdc_properties.SDC_DESIGNER_USER_ID,
            sdc_properties.SDC_DESIGNER_PASSWORD,
        ),
    },
    "GET_RESOURCE_CATEGORIES": {
        "verb": "GET",
        "description": "Queries SDC for resource categories",
        "uri": partial(
            "{endpoint}{service_path}".format,
            endpoint=sdc_properties.SDC_BE_ENDPOINT,
            service_path=sdc_properties.SDC_RESOURCE_CATEGORIES_PATH,
        ),
        "success_code": 200,
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "USER_ID": sdc_properties.SDC_DESIGNER_USER_ID,
        },
        "auth": (
            sdc_properties.GLOBAL_SDC_USERNAME,
            sdc_properties.GLOBAL_SDC_PASSWORD,
        ),
    },
}
