 
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
'''
 Created on Sep 19, 2016
 @author: Tomer Cohen
 
 Purpose: Test SSH Public Key validation, positive and negative.
 Steps:
     - Create user and activate the user account.
     - Modal window: add VF, add vendor contact, invite team member, add a valid SSH key.
     - Go to account page.
     - Clear SSH key text-box and add an invalid SSH key.
     - Verify error message.
     - Change the invalid key to a valid one (RSA).
     - Verify success message.
'''

from iceci.decorator.exception_decor import exception
from services.constants import Constants
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.types import API, Frontend
from tests.uiTests.test_ui_base import TestUiBase


logger = LoggingServiceFactory.get_logger()


class TestSSHKey(TestUiBase):
    user_content = None

    @classmethod
    def setUpClass(cls):
        super(TestSSHKey, cls).setUpClass()

        cls.user_content = API.Bridge.create_engagement(wait_for_gitlab=False)

    def setUp(self):
        super(TestSSHKey, self).setUp()
        Frontend.User.login(self.user_content['email'], Constants.Default.Password.TEXT)

    @exception()
    def test_ssh_key_valid(self):
        validSSHKey = Helper.generate_sshpub_key()
        logger.debug(validSSHKey)
        Frontend.User.set_ssh_key_from_account(validSSHKey)

    @exception()
    def test_ssh_key_invalid(self):
        Frontend.Overview.click_on_vf(self.user_content)
        validSSHKey = Helper.generate_sshpub_key()
        invalidSSHKey = validSSHKey[8:]
        logger.debug(invalidSSHKey)
        Frontend.User.set_ssh_key_from_account(invalidSSHKey, is_negative=True)

    @exception()
    def test_set_invalid_ssh_key_in_wizard(self):
        Frontend.Dashboard.click_on_create_vf()
        Frontend.Wizard.add_vf()
        Frontend.Wizard.add_vendor_contact()
        Frontend.Wizard.invite_team_members(Helper.rand_invite_email())
        Frontend.Wizard.add_ssh_key(is_negative=True)
