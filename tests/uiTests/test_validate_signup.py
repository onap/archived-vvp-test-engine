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
from services.types import API, Frontend, DB
from services.helper import Helper
from tests.uiTests.test_ui_base import TestUiBase


class TestValidateSignup(TestUiBase):
    user_content = None

    @classmethod
    def setUpClass(cls):
        super(TestValidateSignup, cls).setUpClass()

        cls.user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)

    @exception()
    def test_create_and_activateUser(self):
        '''Create user with rest API, login and activate.'''
        user_data = API.User.create_new_user()
        Frontend.User.login(
            user_data['email'],
            Constants.Default.Password.TEXT,
            Constants.Toast.ID)
        Frontend.General.verify_toast_message(
            Constants.Dashboard.ActivateMsg.Fail.TEXT)
        activationUrl = DB.User.get_activation_url(user_data['email'])
        Frontend.General.re_open(activationUrl)
        Frontend.User.login(
            user_data['email'],
            Constants.Default.Password.TEXT)
        Frontend.General.verify_toast_message(
            Constants.Dashboard.ActivateMsg.Success.TEXT)

    @exception()
    def test_activate_user_and_validate_account(self):
        '''Go to Account page and validate details after signup and login.'''
        Frontend.User.login(
            self.user_content['email'],
            Constants.Default.Password.TEXT)
        Frontend.User.go_to_account()
        Frontend.General.form_validate_company(self.user_content['vendor'])
        Frontend.General.form_validate_name(self.user_content['full_name'])
        Frontend.General.form_validate_email(self.user_content['email'])
        Frontend.General.form_validate_phone(Constants.Default.Phone.TEXT)
        Frontend.General.form_validate_ssh("")  # No SSH key.

    @exception()
    def test_signup_page_sanity(self):
        '''
        Purpose: Sanity test for sign-up page.
        Steps:
            - Go to sign-up page
            - Verify all approved vendors are listed
            - Verify all form fields exist.
            - Submit form without reCAPTCHA and verify error message.
            - Click on "Already have an account" and verify link.
        '''
        Frontend.General.go_to_signup_from_login()
        vendors_list = DB.General.get_vendors_list()
        for vendor in vendors_list:
            Frontend.General.select_vendor_from_list(vendor)
        Frontend.General.form_enter_name(Helper.rand_string("randomString"))
        Frontend.General.form_enter_email(Helper.rand_string("email"))
        Frontend.General.form_enter_phone(Constants.Default.Phone.TEXT)
        Frontend.General.form_enter_password(
            Helper.rand_string("randomString"))
        Frontend.General.form_check_checkbox(
            Constants.Signup.RegularEmail.XPATH)
        Frontend.General.form_check_checkbox(
            Constants.Signup.AcceptTerms.XPATH)
        Frontend.General.click_on_submit()
        Frontend.General.verify_toast_message(
            Constants.Signup.Toast.Captcha.TEXT)
        Frontend.General.go_to_login_from_signup()
