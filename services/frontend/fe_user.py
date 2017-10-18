
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
from selenium.webdriver.support.select import Select

from services.api.api_user import APIUser
from services.api.api_virtual_function import APIVirtualFunction
from services.constants import Constants
from services.database.db_general import DBGeneral
from services.database.db_user import DBUser
from services.frontend.base_actions.click import Click
from services.frontend.base_actions.enter import Enter
from services.frontend.base_actions.get import Get
from services.frontend.base_actions.wait import Wait
from services.frontend.fe_general import FEGeneral
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()


class FEUser:

    @staticmethod
    def login(email, password, expected_element=Constants.Dashboard.Statuses.Title.ID, element_type="id"):
        try:
            logger.debug("Verifying and Insert Login page elements:")
            logger.debug("Insert Email " + email)
            Wait.name(Constants.Login.Email.NAME, wait_for_page=True)
            Enter.text_by_name(Constants.Login.Email.NAME, email)
            logger.debug("Insert Password")
            Enter.text_by_name(Constants.Login.Password.NAME, password)
            logger.debug("Click Login Button")
            Click.css(Constants.SubmitButton.CSS)
            logger.debug("Login Button clicked")
            if element_type == 'id':
                Wait.id(expected_element, True)
            elif element_type == 'css':
                Wait.css(expected_element, True)
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "Login FAILED: email=%s password=%s" % (email, password)
            logger.error(errorMsg)
            raise Exception(errorMsg, e)

    @staticmethod
    def relogin(email, password, expected_element=Constants.Dashboard.Statuses.Title.ID, element_type="id"):
        FEGeneral.re_open(Constants.Default.LoginURL.TEXT)
        FEUser.login(email, password, expected_element, element_type)

    @staticmethod
    def logout():
        Click.id(Constants.Dashboard.Avatar.ID)
        Click.link_text(Constants.Dashboard.Avatar.Logout.LINK_TEXT)

    @staticmethod
    def activate_and_login(email, password, expected_element=Constants.Dashboard.Statuses.Title.ID, element_type="id"):
        activationUrl = DBUser.get_activation_url(email)
        FEGeneral.re_open(activationUrl)
        FEUser.login(email, password, expected_element, element_type)

    @staticmethod
    def open_account_form():
        Click.id(Constants.Dashboard.Avatar.ID, wait_for_page=True)
        Click.link_text(
            Constants.Dashboard.Avatar.Account.LINK_TEXT, wait_for_page=True)

    @staticmethod
    # Update account API - only adds new SSH key!
    def update_account_and_return_changes():
        try:
            Select(session.ice_driver.find_element_by_name(
                "company")).select_by_visible_text("Nokia")
            randomName = Helper.rand_string("randomString")
            Enter.text_by_name("fullname", randomName)
            phone = "97258" + Helper.rand_string("randomNumber", 6)
            Enter.text_by_name("phone", phone)
            password = Constants.Default.Password.NewPass.TEXT
            Enter.text_by_name("password", password)
            Enter.text_by_name("confirm_password", password)
            Wait.text_by_css("button.btn.btn-primary", "Update")
            Click.css("button.btn.btn-primary")
            Wait.text_by_id(
                Constants.Toast.ID, "Account was updated successfully!")
            Click.id(Constants.Dashboard.Statuses.ID)

            accountObj = [randomName, phone, password]
            return accountObj
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "Failed in update accaunt ."
            raise Exception(errorMsg)
            raise

    @staticmethod
    def go_to_account():
        try:
            FEUser.click_on_avatar()
            FEUser.click_on_account()
        except Exception as e:
            errorMsg = "Failed to go to Account page."
            raise Exception(errorMsg, e)

    @staticmethod
    def go_to_notifications():
        try:
            FEUser.click_on_avatar()
            FEUser.click_on_notifications()
            Wait.page_has_loaded()
        except Exception as e:
            errorMsg = "Failed to go to Notifications page."
            raise Exception(errorMsg, e)

    @staticmethod
    def click_on_avatar():
        try:
            Click.id(Constants.Dashboard.Avatar.ID, wait_for_page=True)
        except Exception as e:
            errorMsg = "Failed to click_on on Avatar."
            raise Exception(errorMsg, e)

    @staticmethod
    def click_on_admin():
        try:
            Click.id(
                Constants.Dashboard.Avatar.Admin.Title.ID, wait_for_page=True)
        except Exception as e:
            errorMsg = "Failed to click_on on Admin."
            raise Exception(errorMsg, e)

    @staticmethod
    def click_on_feedback():
        Click.id(Constants.Dashboard.Feedback.ID, wait_for_page=True)
        Wait.id(
            Constants.Dashboard.Feedback.FeedbackModal.SAVE_BTN_ID, wait_for_page=True)

    @staticmethod
    def validate_feedback(description, user_email):
        query = "SELECT user_id FROM ice_feedback where description = '{desc}'".format(
            desc=description)
        feedback_user_uuid = DBGeneral.select_query(query)
        query = "SELECT id FROM ice_user_profile  where email = '{email}'".format(
            email=user_email)
        user_uuid = DBGeneral.select_query(query)
        Helper.internal_assert(user_uuid, feedback_user_uuid)

    @staticmethod
    def add_feedback():
        Wait.css("textarea[name=\"description\"]", wait_for_page=True)
        description = Helper.rand_string("randomString")
        Enter.text_by_css("textarea[name=\"description\"]", description)
        Click.id(
            Constants.Dashboard.Feedback.FeedbackModal.SAVE_BTN_ID,  wait_for_page=True)
        Wait.text_by_id(Constants.Toast.ID,
                        "Feedback was sent successfully.", wait_for_page=True)
        return description

    @staticmethod
    def click_on_account():
        try:
            Click.link_text(Constants.Dashboard.Avatar.Account.LINK_TEXT)
            Wait.text_by_css(Constants.Dashboard.Avatar.Account.Title.CSS,
                             Constants.Dashboard.Avatar.Account.Title.TEXT)
        except Exception as e:
            errorMsg = "Failed to click_on on Admin."
            raise Exception(errorMsg, e)

    @staticmethod
    def click_on_notifications():
        try:
            Click.link_text(
                Constants.Dashboard.Avatar.Notifications.LINK_TEXT, wait_for_page=True)
            Wait.text_by_id(Constants.Dashboard.Avatar.Notifications.Title.ID,
                            Constants.Dashboard.Avatar.Notifications.Title.TEXT, wait_for_page=True)
        except Exception as e:
            errorMsg = "Failed to click_on on Admin."
            raise Exception(errorMsg, e)

    @staticmethod
    def go_to_admin():
        try:
            FEUser.click_on_avatar()
            FEUser.click_on_admin()
        except Exception as e:
            errorMsg = "Failed to go to Admin page."
            raise Exception(errorMsg, e)

    @staticmethod
    def assigned_one_NS_to_user(user_content):
        nextStepsNumber = int(
            Get.by_id("next-steps-header").split('(')[1][:-1])
        if (nextStepsNumber != 0):
            logger.error("assigned ns: " + str(nextStepsNumber))
            logger.error(
                "APIUser should not have assigned next steps at first login.")
            raise
        if (Get.by_id("next-steps-list") != "No next steps are assigned to you."):
            logger.error(
                "No assigned next steps and text 'No next steps are assigned to you.' was not found.")
            raise
        token = "token " + APIUser.login_user(user_content['el_email'])
        user_content['session_token'] = token
        logger.debug(
            "Adding new next step (via api) and assigning it to user " + user_content['full_name'])
        APIVirtualFunction.add_next_step(user_content)
        logger.debug(
            "Refresh page and look for changes in assigned next steps section:")
        FEGeneral.refresh()
        logger.debug("    > Check if number has changed in 'Assigned To You'")
        Wait.text_by_id(
            "next-steps-header", "Assigned To You (1)", wait_for_page=True)

    @staticmethod
    def set_ssh_key_from_account(key, is_negative=False):
        FEUser.go_to_account()
        Enter.text_by_name(Constants.Dashboard.Avatar.Account.SSHKey.NAME, key)
        Click.css(Constants.SubmitButton.CSS)
        if is_negative:
            Wait.text_by_id(
                Constants.Toast.ID, Constants.Dashboard.Avatar.Account.SSHKey.UpdateFailed.TEXT)
        else:
            Wait.text_by_id(
                Constants.Toast.ID, Constants.Dashboard.Avatar.Account.Update.Success.TEXT)

    @staticmethod
    def reset_password():
        Wait.text_by_css(
            Constants.UpdatePassword.Title.CSS, Constants.UpdatePassword.Title.TEXT)
        Wait.text_by_css(
            Constants.UpdatePassword.SubTitle.CSS, Constants.UpdatePassword.SubTitle.TEXT)
        Wait.text_by_css(
            Constants.SubmitButton.CSS, Constants.UpdatePassword.Button.TEXT)
        Enter.text_by_name(
            Constants.UpdatePassword.Password.NAME, Constants.Default.Password.NewPass.TEXT)
        Enter.text_by_name(
            Constants.UpdatePassword.ConfirmPassword.NAME, Constants.Default.Password.NewPass.TEXT)
        Click.css(Constants.SubmitButton.CSS)
        Wait.text_by_id(
            Constants.Toast.ID, Constants.UpdatePassword.Toast.TEXT)

    @staticmethod
    def delete_notification(notificationID):
        if isinstance(notificationID, tuple):
            notificationID = notificationID[0]
        delete_button = Constants.Dashboard.Avatar.Notifications.DeleteNotification.ID + \
            notificationID
        # Click on delete button.
        Click.id(delete_button, wait_for_page=True)
        Wait.id_to_dissappear(delete_button)

    @staticmethod
    def validate_notifications(notificationIDs, notification_list):
        ui_list = []
        for notifID in notificationIDs:
            if isinstance(notifID, tuple):
                notifID = notifID[0]
            ui_list.append(str(Get.by_id(
                Constants.Dashboard.Avatar.Notifications.NotificationColumn.ID + notifID)))
        for activity in notification_list:
            if not any(activity in s for s in ui_list):
                raise AssertionError(
                    "Activity: \"" + activity + "\" not appears in UI")

    @staticmethod
    def click_on_export_excel(user_content):
        Enter.text_by_id(
            Constants.Dashboard.Statuses.SearchBox.ID, user_content['vfName'])
        engName = user_content[
            'engagement_manual_id'] + ": " + user_content['vfName']
        engSearchID = "eng-" + engName
        Wait.id(engSearchID)
        # Find the download link and click it
        Click.id(Constants.Dashboard.Statuses.ExportExcel.ID)

    @staticmethod
    def open_invite_team_member_form(vf_left_nav_id):
        Click.id(vf_left_nav_id)
        Click.id(Constants.Dashboard.Overview.TeamMember.ID)
        Wait.text_by_name(Constants.Dashboard.Wizard.InviteTeamMembers.Title.NAME,
                          Constants.Dashboard.Wizard.InviteTeamMembers.Title.TEXT)

    @staticmethod
    def invite_single_user_to_team(email):
        Enter.text_by_name("email", email, wait_for_page=True)
        Click.css(Constants.SubmitButton.CSS, wait_for_page=True)

    @staticmethod
    def go_to_user_profile_settings():
        FEUser.go_to_account()
        Click.id(
            Constants.Dashboard.Avatar.Account.UserProfileSettings.ID, wait_for_page=True)
        Wait.text_by_id(Constants.Dashboard.Avatar.Account.UserProfileSettings.TitleID,
                        Constants.Dashboard.Avatar.Account.UserProfileSettings.TitleText, wait_for_page=True)

    @staticmethod
    def check_user_profile_settings_checkboxes():
        Click.id(
            Constants.Dashboard.Avatar.Account.UserProfileSettings.ReceiveEmailsID, wait_for_page=True)
        Click.id(
            Constants.Dashboard.Avatar.Account.UserProfileSettings.ReceiveEmailEveryTimeID, wait_for_page=True)
        Click.id(
            Constants.Dashboard.Avatar.Account.UserProfileSettings.ReceiveDigestEmailID, wait_for_page=True)
        Click.id(
            Constants.Dashboard.Avatar.Account.UserProfileSettings.UpdateButtonID, wait_for_page=True)

    @staticmethod
    def validate_user_profile_settings_checkboxes(checked):
        Wait.page_has_loaded()
        receive_emails = Get.is_selected_by_id(
            Constants.Dashboard.Avatar.Account.UserProfileSettings.ReceiveEmailsID, True)
        Helper.internal_assert(receive_emails, checked)
        receive_notifications = \
            Get.is_selected_by_id(
                Constants.Dashboard.Avatar.Account.UserProfileSettings.ReceiveNotificationsID, True)
        receive_email_every_time = \
            Get.is_selected_by_id(
                Constants.Dashboard.Avatar.Account.UserProfileSettings.ReceiveEmailEveryTimeID, True)
        Helper.internal_assert(receive_email_every_time, checked)
        receive_digest_email = \
            Get.is_selected_by_id(
                Constants.Dashboard.Avatar.Account.UserProfileSettings.ReceiveDigestEmailID, True)
        Helper.internal_assert(receive_digest_email, not checked)

    @staticmethod
    def compare_notifications_count_for_user(expected_count):
        Wait.text_by_id(
            Constants.Dashboard.Avatar.Notifications.Count.ID, expected_count, True)

    @staticmethod
    def check_notification_number_is_not_presented():
        FEGeneral.refresh()
        Wait.id_to_dissappear(
            Constants.Dashboard.Avatar.Notifications.Count.ID, wait_for_page=True)

    @staticmethod
    def validate_account_details(full_name, phone_number, ssh_key):
        Helper.internal_assert(full_name, Get.value_by_name(
            Constants.Dashboard.Avatar.Account.FullName.NAME))
        Helper.internal_assert(phone_number, Get.value_by_name(
            Constants.Dashboard.Avatar.Account.Phone.NAME))
        Helper.internal_assert(
            ssh_key, Get.value_by_name(Constants.Dashboard.Avatar.Account.SSHKey.NAME))

    @staticmethod
    def check_rgwa_access_key(my_key):
        Wait.text_by_id(
            Constants.Dashboard.Avatar.Account.RGWA.Key.KEY_ID, my_key)

    @staticmethod
    def check_rgwa_access_secret(my_secret):
        Click.id(Constants.Dashboard.Avatar.Account.RGWA.Secret.BUTTON_ID)
        Wait.text_by_id(
            Constants.Dashboard.Avatar.Account.RGWA.Secret.SECRET_ID, my_secret)

    @staticmethod
    def get_rgwa_access_secret():
        Click.id(Constants.Dashboard.Avatar.Account.RGWA.Secret.BUTTON_ID,
                 wait_for_page=True)
        secret = Get.by_id(
            Constants.Dashboard.Avatar.Account.RGWA.Secret.SECRET_ID, wait_for_page=True)
        return secret

    @staticmethod
    def check_rgwa_access_secret_not_presented():
        Wait.text_by_id(
            Constants.Dashboard.Avatar.Account.RGWA.Secret.SECRET_ID,
            Constants.Dashboard.Avatar.Account.RGWA.Secret.SECRET_TEXT)
