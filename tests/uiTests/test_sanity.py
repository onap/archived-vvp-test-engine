
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
from services.frontend.base_actions.click import Click
from services.frontend.base_actions.get import Get
from services.frontend.base_actions.wait import Wait
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.types import Frontend, DB, API
from tests.uiTests.test_ui_base import TestUiBase


logger = LoggingServiceFactory.get_logger()


class TestSanity(TestUiBase):

    user_content = None
    user_content_api = None

    @classmethod
    def setUpClass(cls):
        super(TestSanity, cls).setUpClass()

        cls.user_content_api = API.User.create_new_user_content_login_with_api()
        cls.user_content = API.VirtualFunction.create_engagement()

    @exception()
    def test_e2e_checklist_add_next_step(self):
        newObj, user_content = API.User.create_new_user_content()
        newObjWithChecklist = Frontend.Checklist.create_new_checklist(newObj)
        checklistUuid = newObjWithChecklist[0]
        engLeadEmail = newObjWithChecklist[1]
        engagement_manual_id = newObjWithChecklist[2]
        actualVfNameid = newObjWithChecklist[3]
        checklistName = newObjWithChecklist[5]
        DB.Checklist.state_changed(
            "uuid", checklistUuid, Constants.ChecklistStates.Review.TEXT)
        DB.Checklist.update_decisions(checklistUuid, checklistName)

        Frontend.User.relogin(
            engLeadEmail, Constants.Default.Password.TEXT, engagement_manual_id)
        Frontend.Checklist.click_on_checklist(user_content, checklistName)
        Frontend.Checklist.validate_reject_is_enabled()
        Frontend.Checklist.review_state_actions_and_validations(
            checklistName, user_content['vfName'], Constants.ChecklistStates.Review.TEXT)

        Frontend.Checklist.cl_to_next_stage(actualVfNameid)
        engPreeRiviewerLeadEmail = DB.Checklist.get_pr_email(checklistUuid)
        Frontend.User.relogin(engPreeRiviewerLeadEmail,
                              Constants.Default.Password.TEXT)
        Frontend.Checklist.click_on_checklist(user_content, checklistName)
        Frontend.Checklist.validate_reject_is_enabled()
        Frontend.Checklist.review_state_actions_and_validations(
            checklistName, user_content['vfName'], "PEER")

        Frontend.Checklist.cl_to_next_stage(actualVfNameid)
        engPreeRiviewerLeadEmail = DB.Checklist.get_admin_email(checklistUuid)
        Frontend.User.relogin(engPreeRiviewerLeadEmail,
                              Constants.Default.Password.TEXT)
        Frontend.Checklist.search_by_vfname_for_not_local(user_content)
        Frontend.Checklist.click_on_checklist(user_content, checklistName)
        Frontend.Checklist.validate_reject_is_enabled()
        Frontend.Checklist.approval_state_actions_and_validations(
            checklistName, newObj, "APPROVAL")
        Frontend.Checklist.add_next_step(checklistName, newObj)
        Frontend.Overview.click_on_vf(user_content)

    @exception()
    def test_admin_set_stage(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        stages = [Constants.EngagementStages.INTAKE, Constants.EngagementStages.ACTIVE,
                  Constants.EngagementStages.VALIDATED, Constants.EngagementStages.COMPLETED]
        Frontend.User.login(
            Constants.Users.Admin.EMAIL, Constants.Default.Password.TEXT)
        Frontend.Dashboard.statuses_search_vf(
            user_content['engagement_manual_id'], user_content['vfName'])
        for idx, stage in enumerate(stages[:-1]):
            next_stage = stages[(idx + 1) % len(stages)]
            Frontend.Overview.check_stage_next_steps(
                stage, user_content['engagement_uuid'])
            Frontend.Overview.change_engagement_stage(next_stage)

    @exception()
    def test_invite_new_user(self):
        """
        Name:
            test_invite_new_user
        Steps:
            Create new APIUser via SignUp request-->Login with This One--> build "activationUrl"-->
            Validation of successful activate-->
            close Wizard --> Logout-->login-->Open Wizard--> fill all fields in all Tab's(4)-->
            build inviteURL from email--> reopen browser with inviteURL-->
            Validate fields filled's in SignUp form
        """
        user_content = API.User.create_new_user()
        # Fetch one user ID.
        uuid = DB.General.select_where_email(
            "uuid", "ice_user_profile", user_content['email'])
        Frontend.User.activate_and_login(
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
        # Wizard
        vfName = Frontend.Wizard.add_vf()
        vendor_contact = Frontend.Wizard.add_vendor_contact()
        inviteEmail = Helper.rand_invite_email()
        Frontend.Wizard.invite_team_members(inviteEmail)
        Frontend.Wizard.add_ssh_key()
        enguuid = DB.General.select_where("uuid", "ice_vf", "name", vfName, 1)
        inviterURL = Constants.Default.InviteURL.Signup.TEXT + \
            enguuid + "&inviter_uuid=" + uuid + "&email=" + inviteEmail
        Frontend.General.re_open(inviterURL)
        actualInvitedEmail = Get.value_by_name("email")
        Helper.internal_assert(inviteEmail, actualInvitedEmail)
        signUpURLforContact = DB.User.get_contact_signup_url(enguuid, uuid, vendor_contact["email"],
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
