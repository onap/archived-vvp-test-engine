 
# ============LICENSE_START========================================== 
# org.onap.vvp/test-engine
# ===================================================================
# Copyright © 2017 AT&T Intellectual Property. All rights reserved.
# ===================================================================
#
# Unless otherwise specified, all software contained herein is licensed
# under the Apache License, Version 2.0 (the “License”);
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
# under the Creative Commons License, Attribution 4.0 Intl. (the “License”);
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
#
# ECOMP is a trademark and service mark of AT&T Intellectual Property.
from selenium.common.exceptions import TimeoutException

from iceci.decorator.exception_decor import exception
from services.constants import Constants
from services.logging_service import LoggingServiceFactory
from services.types import API, Frontend
from tests.uiTests.test_ui_base import TestUiBase


logger = LoggingServiceFactory.get_logger()


class TestFeatureExportToExcel(TestUiBase):
    user_content = None

    @classmethod
    def setUpClass(cls):
        super(TestFeatureExportToExcel, cls).setUpClass()

        cls.user_content = API.VirtualFunction.create_engagement(wait_for_gitlab=False)

    @exception()
    def test_validate_export_to_csv(self):
        Frontend.User.login(self.user_content['email'], Constants.Default.Password.TEXT)
        Frontend.User.click_on_export_excel(self.user_content)
        try:
            token = "token " + API.Bridge.login_user(self.user_content['email'])
            content = API.VirtualFunction.get_export_dasboard_excel(token)
            if not content:
                raise Exception("content is empty.")
        except TimeoutException:
            logger.error("TimeoutException Not Appear")
