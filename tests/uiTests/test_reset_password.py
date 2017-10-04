 
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
from iceci.decorator.exception_decor import exception
from services.constants import Constants
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.types import API, Frontend, DB
from tests.uiTests.test_ui_base import TestUiBase


logger = LoggingServiceFactory.get_logger()


class TestResetPassword(TestUiBase):
    user_content = None

    @classmethod
    def setUpClass(cls):
        super(TestResetPassword, cls).setUpClass()

        cls.user_content = API.VirtualFunction.create_engagement(wait_for_gitlab=False)
    
    @exception()
    def test_reset_password(self):
        Frontend.General.send_reset_password(self.user_content['email'])
        DB.User.set_new_temp_password(self.user_content['email'])
        resetPasswURL = Helper.get_reset_passw_url(self.user_content['email'])
        Frontend.General.re_open(resetPasswURL)
        Frontend.User.login(self.user_content['email'], Constants.Default.Password.TEXT,
                            Constants.UpdatePassword.Title.CSS, "css")
        logger.debug("\nReset URL: %s \nTemp Password: %s \nUser Email: %s" % (resetPasswURL,
                                                        Constants.Default.Password.TEXT, self.user_content['email']))
        Frontend.User.reset_password()
        logger.debug("Logout and verify new password works")
        Frontend.User.logout()
        logger.debug("Login with updated password")
        Frontend.User.login(self.user_content['email'], Constants.Default.Password.NewPass.TEXT)
        Frontend.User.logout()
        logger.debug("Logout and change password back to 'iceusers'")
        DB.User.set_password_to_default(self.user_content['email'])
        Frontend.User.login(self.user_content['email'], Constants.Default.Password.TEXT)
