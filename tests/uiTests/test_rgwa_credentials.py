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
from services.logging_service import LoggingServiceFactory
from services.types import API, DB, Frontend
from tests.uiTests.test_ui_base import TestUiBase
from utils.cryptography import CryptographyText


logger = LoggingServiceFactory.get_logger()


class TestRGWACredentials(TestUiBase):
    user_content = None
    access_key = None
    access_secret = None

    @classmethod
    def setUpClass(cls):
        super(TestRGWACredentials, cls).setUpClass()
        cls.user_content = API.User.create_new_user(activate=True)
        cls.access_key = DB.User.get_access_key(cls.user_content['uuid'])
        cls.access_secret = DB.User.get_access_secret(cls.user_content['uuid'])

    def setUp(self):
        super(TestRGWACredentials, self).setUp()
        Frontend.User.login(
            self.user_content['email'], Constants.Default.Password.TEXT)

    @exception()
    def test_access_key(self):
        Frontend.User.go_to_account()
        Frontend.User.check_rgwa_access_key(self.access_key)

    @exception()
    def test_access_secret(self):
        Frontend.User.go_to_account()
        access_secret = CryptographyText.decrypt(self.access_secret)
        Frontend.User.check_rgwa_access_secret(access_secret)

    @exception()
    def test_access_secret_not_presented(self):
        Frontend.User.go_to_account()
        Frontend.User.check_rgwa_access_secret_not_presented()
