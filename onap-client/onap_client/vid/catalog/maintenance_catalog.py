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

from onap_client.vid.client import VIDClient


class MaintenanceClient(VIDClient):
    @property
    def namespace(self):
        return "maintenance"

    @property
    def catalog_resources(self):
        return {
            "CREATE_OWNING_ENTITY": {
                "verb": "POST",
                "description": "Creates an owning entity in VID",
                "uri": partial(
                    "{endpoint}{service_path}/category_parameter/owningEntity".format,
                    endpoint=self.config.vid.VID_ENDPOINT,
                    service_path=self.config.vid.VID_MAINTENANCE_PATH,
                ),
                "payload-parameters": ["name"],
                "payload": "{}/vid_maintenance.jinja".format(self.config.payload_directory),
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (self.config.vid.VID_USERNAME, self.config.vid.VID_PASSWORD,),
            },
            "CREATE_LINE_OF_BUSINESS": {
                "verb": "POST",
                "description": "Creates a line of business in VID",
                "uri": partial(
                    "{endpoint}{service_path}/category_parameter/lineOfBusiness".format,
                    endpoint=self.config.vid.VID_ENDPOINT,
                    service_path=self.config.vid.VID_MAINTENANCE_PATH,
                ),
                "payload-parameters": ["name"],
                "payload": "{}/vid_maintenance.jinja".format(self.config.payload_directory),
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (self.config.vid.VID_USERNAME, self.config.vid.VID_PASSWORD,),
            },
            "CREATE_PLATFORM": {
                "verb": "POST",
                "description": "Creates a platform in VID",
                "uri": partial(
                    "{endpoint}{service_path}/category_parameter/platform".format,
                    endpoint=self.config.vid.VID_ENDPOINT,
                    service_path=self.config.vid.VID_MAINTENANCE_PATH,
                ),
                "payload-parameters": ["name"],
                "payload": "{}/vid_maintenance.jinja".format(self.config.payload_directory),
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (self.config.vid.VID_USERNAME, self.config.vid.VID_PASSWORD,),
            },
            "CREATE_PROJECT": {
                "verb": "POST",
                "description": "Creates a project in VID",
                "uri": partial(
                    "{endpoint}{service_path}/category_parameter/project".format,
                    endpoint=self.config.vid.VID_ENDPOINT,
                    service_path=self.config.vid.VID_MAINTENANCE_PATH,
                ),
                "payload-parameters": ["name"],
                "payload": "{}/vid_maintenance.jinja".format(self.config.payload_directory),
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (self.config.vid.VID_USERNAME, self.config.vid.VID_PASSWORD,),
            },
            "GET_CATEGORY_PARAMETERS": {
                "verb": "GET",
                "description": "Returns the category parameters currently stored in VID",
                "uri": partial(
                    "{endpoint}{service_path}/category_parameter?familyName=PARAMETER_STANDARDIZATION".format,
                    endpoint=self.config.vid.VID_ENDPOINT,
                    service_path=self.config.vid.VID_MAINTENANCE_PATH,
                ),
                "success_code": 200,
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "X-TransactionId": str(uuid.uuid4()),
                    "X-FromAppId": self.config.application_id,
                },
                "auth": (self.config.vid.VID_USERNAME, self.config.vid.VID_PASSWORD,),
            },
        }
