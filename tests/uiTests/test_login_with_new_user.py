
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
from wheel.signatures import assertTrue
from iceci.decorator.exception_decor import exception
from services.constants import Constants
from services.frontend.base_actions.click import Click
from services.frontend.base_actions.enter import Enter
from services.frontend.base_actions.get import Get
from services.frontend.base_actions.wait import Wait
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.types import API, Frontend, DB
from tests.uiTests.test_ui_base import TestUiBase

logger = LoggingServiceFactory.get_logger()


class TestLoginPageWithNewUser(TestUiBase):

    @exception()
    def test_login_positive(self):
        ''' Create new user login. '''
        user_content = API.User.create_new_user()
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT, Constants.Toast.ID)
        logger.debug("Resend Activation Email Page Opened ")
        Wait.text_by_id(
            Constants.Toast.ID, Constants.ActivateAccount.Toast.TEXT)

    @exception()
    def test_login_negative(self):
        ''' Negative: Type wrong password in login page. '''
        user_content = API.User.create_new_user(activate=True)
        Frontend.User.login(
            user_content['email'], Helper.rand_string("randomString"), Constants.Toast.ID)
        Wait.text_by_id(Constants.Toast.ID, Constants.Login.Toast.TEXT)
        logger.debug(
            "Message Error(APIUser or Password does not match) Displayed")

    @exception()
    def test_login_negative_email_valid(self):
        ''' Negative: Type wrong password in login page. '''
        user_content = API.User.create_new_user(activate=True)
        Frontend.User.login(
            user_content['email'] + "s", Constants.Default.Password.TEXT, Constants.Toast.ID)
        Wait.text_by_id(Constants.Toast.ID, Constants.Login.Toast.TEXT)
        logger.debug(
            "Message Error(APIUser or Password does not match) Displayed")

    @exception()
    def test_login_negative_required_password(self):
        ''' Check that password is a required field on login page. '''
        user_content = API.User.create_new_user()
        logger.debug("Verifying and Insert Login page elements:")
        Enter.text_by_name(Constants.Login.Email.NAME, user_content['email'])
        Enter.text_by_name(Constants.Login.Password.NAME, "1")
        Enter.text_by_name(Constants.Login.Password.NAME, "")
        Wait.text_by_css(
            Constants.Login.Password.Error.CSS, Constants.Login.Password.Error.TEXT)

    @exception()
    def test_login_page_dont_have_accaunt_button(self):
        ''' Go to login page, click_on on "Don't have an account", verify user is redirected to signup page. '''
        Click.id(Constants.Login.DontHaveAccount.ID)
        Wait.text_by_css(
            Constants.Signup.Title.CSS, Constants.Signup.Title.TEXT)

    @exception()
    def test_login_page_home_button(self):
        ''' Open login page, verify home button works correctly. '''
        Click.id(Constants.Home.Logo.ID)
        Wait.text_by_id(Constants.Home.Title.ID, Constants.Home.Title.TEXT)

    @exception()
    def test_create_and_activate_user(self):
        ''' Create user and activate by log-in. '''
        user_content = API.User.create_new_user()
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT, Constants.Toast.ID)
        '''  Resend Activation Email Page Opened '''
        Wait.text_by_id(
            Constants.Toast.ID, Constants.ActivateAccount.Toast.TEXT)
        activationUrl = DB.User.get_activation_url(user_content['email'])
        Frontend.General.re_open(activationUrl)
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)
        Wait.text_by_id(
            Constants.Toast.ID, Constants.Dashboard.ActivateMsg.Success.TEXT)

    @exception()
    def test_invite_existing_user(self):
        ''' Create user and VF, login, invite existing user, login with second user and verify user has joined to engagement '''
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        second_user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        activationUrl = DB.User.get_activation_url(user_content['email'])
        Frontend.General.re_open(activationUrl)
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)
        vfFullName = user_content[
            'engagement_manual_id'] + ": " + user_content['vfName']
        actualVfNameid = "clickable-" + vfFullName
        Click.id(actualVfNameid, wait_for_page=True)
        Wait.id(Constants.Dashboard.Overview.TeamMember.ID)
        Frontend.Wizard.invite_team_members_modal(second_user_content['email'])
        enguuid = DB.General.select_where("uuid", "ice_engagement", "engagement_manual_id", user_content[
                                          'engagement_manual_id'], 1)  # Fetch one is_service_provider_contact user ID.
        invitation_token = DB.User.select_invitation_token("invitation_token", "ice_invitation", "engagement_uuid",
                                                           enguuid, second_user_content['email'], 1)
        inviterURL = Constants.Default.InviteURL.Login.TEXT + invitation_token
        Frontend.General.re_open(inviterURL)
        actualVfNameid = "clickable-" + vfFullName
        Frontend.User.login(
            second_user_content['email'], Constants.Default.Password.TEXT, actualVfNameid)
        Wait.modal_to_dissappear()
        Frontend.Overview.click_on_vf(user_content)
        Wait.text_by_id(Constants.Dashboard.Overview.Title.ID, vfFullName)

    @exception()
    def test_invite_new_user_of_service_provider_internal(self):
        '''
        TC Name: test_invite_new_user_aservice_provider_internal
        Steps:
        Create new NOT-MainServiceProvider APIUser via SignUp request-->Login with This One--> build "activationUrl"-->
        Validation of successful activate-->
        close Wizard --> Logout from Dashboard -->login-->Open Wizard--> fill all fields in all Tab's(4)-->
        validate second Tab is a "add_service_provider_internal"-->
        build inviteURL from email--> reopen browser with inviteURL-->
        Validate Login Form opened -->
        Login--> Validate Dashboard Form opened
        '''
        user_content = API.User.create_new_user(company="Amdocs")
        uuid = DB.General.select_where_email(
            "uuid", "ice_user_profile", user_content['email'])
        activationUrl = DB.User.get_activation_url(user_content['email'])
        Frontend.General.re_open(activationUrl)
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)  # new
        Wait.text_by_id(
            Constants.Toast.ID, Constants.Dashboard.ActivateMsg.Success.TEXT)
        Click.id(Constants.Dashboard.Wizard.CloseButton.ID)
        Wait.modal_to_dissappear()
        Frontend.User.logout()
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)
        Wait.text_by_css(
            Constants.Dashboard.LeftPanel.Title.CSS, Constants.Dashboard.LeftPanel.Title.TEXT)
        Wait.id(Constants.Dashboard.Statuses.Title.ID)
        Click.id(Constants.Dashboard.LeftPanel.AddEngagement.ID)
        # Wizard
        vfName = Frontend.Wizard.add_vf()
        service_provider_internal = Frontend.Wizard.add_service_provider_internal()
        inviteEmail = Helper.rand_invite_email()
        Frontend.Wizard.invite_team_members(inviteEmail)
        Frontend.Wizard.add_ssh_key()
        enguuid = DB.General.select_where("uuid", "ice_vf", "name", vfName, 1)
        invitation_token = DB.User.select_invitation_token("invitation_token", "ice_invitation", "engagement_uuid",
                                                           enguuid, inviteEmail, 1)
        inviterURL = Constants.Default.InviteURL.Signup.TEXT + \
            invitation_token + "&email=" + inviteEmail

        Frontend.General.re_open(inviterURL)
        actualInvitedEmail = Get.value_by_name(Constants.Signup.Email.NAME)
        Helper.internal_assert(inviteEmail, actualInvitedEmail)
        signUpURLforContact = DB.User.get_contact_signup_url(invitation_token, uuid, service_provider_internal["email"],
                                                             service_provider_internal["full_name"], service_provider_internal["phone"], service_provider_internal["company"])
        Frontend.General.re_open(signUpURLforContact)
        actualInvitedEmail = Get.value_by_name(Constants.Signup.Email.NAME)
        Helper.internal_assert(
            service_provider_internal["email"], actualInvitedEmail)
        Helper.internal_assert(
            "+" + service_provider_internal["phone"], Get.value_by_name(Constants.Signup.Phone.NAME))
        Helper.internal_assert(
            service_provider_internal["full_name"], Get.value_by_name(Constants.Signup.FullName.NAME))
        signupCompany = Get.value_by_name(Constants.Signup.Company.NAME, True)
        Helper.internal_assert(
            service_provider_internal["company"], signupCompany)

    @exception()
    def test_create_2_new_users(self):
        '''
        Login and activate new user, than reopen browser and loging with new other user -
        check wizard appears for both Frontend.User.
        '''
        # First APIUser
        user_content = API.User.create_new_user()
        logger.debug(user_content['email'])
        activationUrl = DB.User.get_activation_url(user_content['email'])
        logger.debug(activationUrl)
        Frontend.General.re_open(activationUrl)
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)
        Wait.text_by_id(
            Constants.Toast.ID, Constants.Dashboard.ActivateMsg.Success.TEXT)
        Click.id(Constants.Dashboard.Wizard.CloseButton.ID)
        Wait.modal_to_dissappear()
        Frontend.User.logout()
        # Second APIUser
        user_content = API.User.create_new_user()
        logger.debug(user_content['email'])
        activationUrl2 = DB.User.get_activation_url(user_content['email'])
        logger.debug(activationUrl2)
        Frontend.General.re_open_not_clean_cache(activationUrl2)
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)  # new
        Wait.text_by_id(
            Constants.Toast.ID, Constants.Dashboard.ActivateMsg.Success.TEXT)
        Click.id(Constants.Dashboard.Wizard.CloseButton.ID)
        Wait.modal_to_dissappear()
        Click.id(Constants.Dashboard.Avatar.ID)

    @exception()
    def test_validate_account_form(self):
        '''Go to Account page and validate details.'''
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        ssh_key = API.User.set_ssh(user_content)
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)
        Frontend.User.go_to_account()
        Frontend.User.validate_account_details(
            user_content['full_name'], user_content['phone_number'], ssh_key)

    @exception()
    def test_add_vendor_contact(self):
        '''
        TC Name: test_add_vendor_contact
        Steps:
        Invite vendor contact and activate the invited user. Validate the invited user has the right VF.
        '''
        user_content = API.User.create_new_user()
        # Fetch one user ID.
        uuid = DB.General.select_where_email(
            "uuid", "ice_user_profile", user_content['email'])
        activationUrl = DB.User.get_activation_url(user_content['email'])
        Frontend.General.re_open(activationUrl)
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)  # new
        Wait.text_by_id(
            Constants.Toast.ID, Constants.Dashboard.ActivateMsg.Success.TEXT)
        Click.id(Constants.Dashboard.Wizard.CloseButton.ID)
        Wait.modal_to_dissappear()
        Frontend.User.logout()
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)
        Wait.text_by_css(
            Constants.Dashboard.LeftPanel.Title.CSS, Constants.Dashboard.LeftPanel.Title.TEXT)
        Wait.id(Constants.Dashboard.Statuses.Title.ID)
        logger.debug("click_on on + Dashboard")
        Click.id(Constants.Dashboard.LeftPanel.AddEngagement.ID)
        # Wizard
        vfName = Frontend.Wizard.add_vf()
        vendor_contact = Frontend.Wizard.add_vendor_contact()
        inviteEmail = "automationqatt" + \
            Helper.rand_string("randomString") + "@gmail.com"
        Frontend.Wizard.invite_team_members(inviteEmail)
        Frontend.Wizard.add_ssh_key()
        engagement_id = DB.General.select_where(
            "engagement_id", "ice_vf", "name", vfName, 1)
        engLeadEmail = DB.User.select_el_email(vfName)
        engagement_manual_id = DB.General.select_where(
            "engagement_manual_id", "ice_engagement", "uuid", engagement_id, 1)
        invitation_token = DB.User.select_invitation_token("invitation_token", "ice_invitation", "engagement_uuid",
                                                           engagement_id, vendor_contact["email"], 1)
        signUpURLforContact = DB.User.get_contact_signup_url(invitation_token, uuid, vendor_contact["email"],
                                                             vendor_contact["full_name"], vendor_contact["phone"], vendor_contact["company"])
        Frontend.General.re_open(signUpURLforContact)
        actualInvitedEmail = Get.value_by_name(Constants.Signup.Email.NAME)
        Helper.internal_assert(vendor_contact["email"], actualInvitedEmail)
        Helper.internal_assert(
            "+" + vendor_contact["phone"], Get.value_by_name(Constants.Signup.Phone.NAME))
        Helper.internal_assert(
            vendor_contact["full_name"], Get.value_by_name(Constants.Signup.FullName.NAME))
        Helper.internal_assert(
            vendor_contact["company"], Get.value_by_name(Constants.Signup.Company.NAME))
        # SignUp for VendorContact
        user_content['engagement_uuid'] = engagement_id
        user_content['engagement_manual_id'] = engagement_manual_id
        user_content['vfName'] = vfName
        user_content['el_email'] = engLeadEmail
        API.User.signup_invited_user(vendor_contact["company"], vendor_contact["email"], invitation_token,
                                     signUpURLforContact, user_content, True)
        activationUrl2 = DB.User.get_activation_url(vendor_contact["email"])
        # Activate for VendorContact
        myVfName = engagement_manual_id + ": " + vfName
        actualVfNameid = "clickable-" + myVfName
        Frontend.General.re_open(activationUrl2)
        Frontend.User.login(
            vendor_contact["email"], Constants.Default.Password.TEXT, actualVfNameid)
        # Validate opened right VF for VendorContact
        actualVfName = Get.by_id(actualVfNameid)
        Helper.internal_assert(myVfName, actualVfName)

    @exception()
    def test_add_service_provider_internal(self):
        '''
        TC Name: test_add_service_provider_internal
        Steps:
        Invite is_service_provider_contact Sponsor and activate the invited user. Validate sponsor has the right VF.
        '''
        user_content = API.User.create_new_user(company="Amdocs")
        uuid = DB.General.select_where_email(
            "uuid", "ice_user_profile", user_content['email'])
        activationUrl = DB.User.get_activation_url(user_content['email'])
        Frontend.General.re_open(activationUrl)
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)  # new
        Wait.text_by_id(
            Constants.Toast.ID, Constants.Dashboard.ActivateMsg.Success.TEXT)
        Click.id(Constants.Dashboard.Wizard.CloseButton.ID)
        Wait.modal_to_dissappear()
        Frontend.User.logout()
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)
        Wait.text_by_css(
            Constants.Dashboard.LeftPanel.Title.CSS, Constants.Dashboard.LeftPanel.Title.TEXT)
        Wait.id(Constants.Dashboard.Statuses.Title.ID)
        logger.debug("click_on on + Dashboard")
        Click.id(Constants.Dashboard.LeftPanel.AddEngagement.ID)
        # Wizard
        vfName = Frontend.Wizard.add_vf()
        service_provider_internal = Frontend.Wizard.add_service_provider_internal()
        inviteEmail = "automationqatt" + \
            Helper.rand_string("randomString") + "@gmail.com"
        Frontend.Wizard.invite_team_members(inviteEmail)
        Frontend.Wizard.add_ssh_key()
        enguuid = DB.General.select_where("uuid", "ice_vf", "name", vfName, 1)
        invitation_token = DB.User.select_invitation_token("invitation_token", "ice_invitation", "engagement_uuid",
                                                           enguuid, inviteEmail, 1)
        inviterURL = Constants.Default.InviteURL.Signup.TEXT + \
            invitation_token + "&email=" + inviteEmail
        Frontend.General.re_open(inviterURL)
        actualInvitedEmail = Get.value_by_name("email")
        Helper.internal_assert(inviteEmail, actualInvitedEmail)
        signUpURLforContact = DB.User.get_contact_signup_url(invitation_token, uuid, service_provider_internal["email"],
                                                             service_provider_internal["full_name"], service_provider_internal["phone"], service_provider_internal["company"])
        Frontend.General.re_open(signUpURLforContact)
        actualInvitedEmail = Get.value_by_name(Constants.Signup.Email.NAME)
        Helper.internal_assert(
            str("+" + service_provider_internal["phone"]), Get.value_by_name(Constants.Signup.Phone.NAME))
        Helper.internal_assert(
            service_provider_internal["full_name"], Get.value_by_name(Constants.Signup.FullName.NAME))
        Helper.internal_assert(
            service_provider_internal["company"], Get.value_by_name(Constants.Signup.Company.NAME))
        # Fetch one is_service_provider_contact user ID.
        engagement_id = DB.General.select_where(
            "engagement_id", "ice_vf", "name", vfName, 1)
        # SignUp for MainServiceProviderSponsorContact
        engagement_manual_id = DB.General.select_where(
            "engagement_manual_id", "ice_engagement", "uuid", engagement_id, 1)

        invitation_token = DB.User.select_invitation_token("invitation_token", "ice_invitation", "engagement_uuid",
                                                           engagement_id, service_provider_internal["email"], 1)
        engLeadEmail = DB.User.select_el_email(vfName)
        user_content['engagement_uuid'] = engagement_id
        user_content['engagement_manual_id'] = engagement_manual_id
        user_content['vfName'] = vfName
        user_content['el_email'] = engLeadEmail

        API.User.signup_invited_user(service_provider_internal["company"], service_provider_internal["email"], invitation_token,
                                     signUpURLforContact, user_content, True)
        activationUrl2 = DB.User.get_activation_url(
            service_provider_internal["email"])
        # Activate for VendorContact




        engagement_manual_id = DB.General.select_where(
            "engagement_manual_id", "ice_engagement", "uuid", engagement_id, 1)
        # Validate opened right VF for VendorContact
        myVfName = engagement_manual_id + ": " + vfName
        actualVfNameid = "clickable-" + myVfName
        Frontend.General.re_open(activationUrl2)
        Frontend.User.login(
            service_provider_internal["email"], Constants.Default.Password.TEXT, actualVfNameid)
        actualVfName = Get.by_id(actualVfNameid, wait_for_page=True)
        Helper.internal_assert(myVfName, actualVfName)

    @exception()
    def test_Validate_SSHkeyNS(self):
        ''' Insert a valid ssh key in wizard, validate "add ssh key" next step marked as completed. '''
        user_content = API.User.create_new_user()
        activationUrl = DB.User.get_activation_url(user_content['email'])
        Frontend.General.re_open(activationUrl)
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)
        Wait.text_by_id(
            Constants.Toast.ID, Constants.Dashboard.ActivateMsg.Success.TEXT)
        Click.id(Constants.Dashboard.Wizard.CloseButton.ID)
        Wait.modal_to_dissappear()
        Frontend.User.logout()
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)
        Wait.text_by_css(
            Constants.Dashboard.LeftPanel.Title.CSS, Constants.Dashboard.LeftPanel.Title.TEXT)
        logger.debug("click_on on + Dashboard")
        Click.id(Constants.Dashboard.LeftPanel.AddEngagement.ID)
        #    Wizard
        vfName = Frontend.Wizard.add_vf()
        Frontend.Wizard.add_vendor_contact()
        inviteEmail = Helper.rand_invite_email()
        Frontend.Wizard.invite_team_members(inviteEmail)
        sshKey = Frontend.Wizard.add_ssh_key()
        Frontend.User.go_to_account()
        Wait.id(user_content['email'])
        actualFullName = Get.value_by_name(
            Constants.Dashboard.Avatar.Account.FullName.NAME)
        Helper.internal_assert(user_content['full_name'], actualFullName)
        actualSSHkey = Get.value_by_name(
            Constants.Dashboard.Avatar.Account.SSHKey.NAME)
        Helper.internal_assert(sshKey, actualSSHkey)
        Click.id(Constants.Dashboard.Statuses.ID)
        #    VALIDATION FOR CONFIRMED BY ENG. LEAD
        engLeadEmail = DB.User.select_el_email(vfName)
        engagement_id = DB.General.select_where(
            "engagement_id", "ice_vf", "name", vfName, 1)
        engagement_manual_id = DB.General.select_where(
            "engagement_manual_id", "ice_engagement", "uuid", engagement_id, 1)
        myVfName = engagement_manual_id + ": " + vfName
        actualVfNameid = "clickable-" + myVfName
        Click.id(actualVfNameid)
        Click.id("overview-" + myVfName)
        Click.css("span.engagement_detail_menu_name")
        Click.xpath("//span[2]/multiselect/div/button")
        Click.link_text("Completed")
        elFullName = DB.General.select_where(
            "full_name", "ice_user_profile", "email", engLeadEmail, 1)
        idNs = elFullName + "_Completed"
        actualConfirmBy = str(Get.by_id(idNs))
        expectedConfirmBy = "System Next Step  Completed: "
        Helper.internal_assert(expectedConfirmBy, actualConfirmBy)

    @exception()
    def test_current_status(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        vfName = user_content['vfName']
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)  # new
        Frontend.Overview.click_on_vf(user_content)
        Frontend.User.go_to_account()
        Wait.id(user_content['email'])
        actualFullName = Get.value_by_name("fullname")
        Helper.internal_assert(user_content['full_name'], actualFullName)
        Click.id(Constants.Dashboard.Statuses.ID)
        Frontend.Overview.click_on_vf(user_content)
        Helper.internal_assert(
            "Current Status", Get.by_css(Constants.Dashboard.Overview.Status.Header.ID))
        Wait.text_by_id(Constants.Dashboard.Overview.Status.Description.ID,
                        "No status update has been provided yet.")
        Click.id(Constants.Dashboard.Avatar.ID)
        Click.link_text("Logout")
        engLeadEmail = DB.User.select_el_email(vfName)
        Frontend.User.relogin(engLeadEmail, Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        Click.css(Constants.Dashboard.Overview.Status.Add.CSS)
        Helper.internal_assert(
            "Add Status", Get.by_css("h3.modal-title.ng-binding"))
        Helper.internal_assert(
            "Use the form below to add the current status of the engagement.", Get.by_css("span.ng-binding"))
        Click.css("textarea[name=\"description\"]")
        Enter.text_by_css(
            "textarea[name=\"description\"]", "Add new Status", wait_for_page=True)
        Helper.internal_assert(
            "Add status", Get.by_id(Constants.Dashboard.DetailedView.VFC.Save_button.ID))
        Click.id(
            Constants.Dashboard.DetailedView.VFC.Save_button.ID, wait_for_page=True)
        Helper.assertTrue("Last updated" in Get.by_id("status-update-details"))
        Wait.text_by_id(
            Constants.Dashboard.Overview.Status.Description.ID, "Add new Status")
        Wait.css(Constants.Dashboard.Overview.Status.Edit.CSS)
        Wait.modal_to_dissappear()
        Click.css(Constants.Dashboard.Overview.Status.Edit.CSS)
        Helper.internal_assert(
            "Current Status", Get.by_css("h3.modal-title.ng-binding"))
        Click.css("textarea[name=\"description\"]")
        Enter.text_by_css("textarea[name=\"description\"]", "Update Status")
        Click.id(Constants.Dashboard.DetailedView.VFC.Save_button.ID)
        Wait.modal_to_dissappear()
        Wait.text_by_id(
            Constants.Dashboard.Overview.Status.Description.ID, "Update Status")
        Frontend.User.logout()
        Frontend.User.relogin(
            user_content['email'], Constants.Default.Password.TEXT)  # new
        Frontend.Overview.click_on_vf(user_content)
        Helper.internal_assert(
            "Current Status", Get.by_css(Constants.Dashboard.Overview.Status.Header.ID))
        Wait.text_by_id(
            Constants.Dashboard.Overview.Status.Description.ID, "Update Status")

    @exception()
    def test_XSS_script(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        validate = API.User.update_account_injec_script(user_content)
        assertTrue(validate)
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)
        Frontend.User.open_account_form()
        script = "<script>;</script>"
        Enter.text_by_name("fullname", script, wait_for_page=True)
        Wait.text_by_css(Constants.SubmitButton.CSS, "Update")
        Click.css(Constants.SubmitButton.CSS, wait_for_page=True)
        Wait.text_by_css(
            Constants.Toast.CSS, "Account was updated successfully!")

    @exception()
    def test_add_vf(self):
        user_content = API.User.create_new_user_content_login_with_api()
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        # Wizard
        Frontend.Overview.create_and_verify_VF_with_VFversion()
