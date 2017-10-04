 
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
from services.frontend.base_actions.enter import Enter
from services.frontend.base_actions.get import Get
from services.frontend.base_actions.wait import Wait
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.types import API, DB, Frontend
from tests.uiTests.test_ui_base import TestUiBase


logger = LoggingServiceFactory.get_logger()


class TestInvitationsLogic(TestUiBase):
    '''
     Check that there is not an invitation entry in the table for a specific
     email and engagement_uuid. If an entry exists, do not send an email.
    '''

    @exception()
    def test_validate_duplicate_invite(self):
        user_content = []
        for _ in range(3):
            user_content.append(
                API.VirtualFunction.create_engagement(wait_for_gitlab=False))
        Frontend.User.login(
            user_content[0]['email'], Constants.Default.Password.TEXT)
        engName = user_content[0][
            'engagement_manual_id'] + ": " + user_content[0]['vfName']
        vf_left_nav_id = "clickable-" + engName
        Click.id(vf_left_nav_id)
        Frontend.Wizard.invite_team_members_modal(user_content[1]['email'])
        enguuid = DB.General.select_where(
            "uuid", "ice_engagement", "engagement_manual_id", user_content[0]['engagement_manual_id'], 1)
        invitation_token = DB.User.select_invitation_token(
            "invitation_token", "ice_invitation", "engagement_uuid", enguuid, user_content[1]['email'], 1)
        inviterURL = Constants.Default.InviteURL.Login.TEXT + invitation_token
        Frontend.General.re_open(inviterURL)
        title_id = "title-id-" + engName
        Frontend.User.login(
            user_content[1]['email'], Constants.Default.Password.TEXT, title_id)
        vf_left_nav_id = "clickable-" + engName
        Click.id(vf_left_nav_id)
        actualVfName = Get.by_id(vf_left_nav_id)
        Helper.internal_assert(engName, actualVfName)
        Wait.text_by_id(Constants.Dashboard.Overview.Title.ID, engName)
        Frontend.User.logout()
        Frontend.User.login(
            user_content[0]['email'], Constants.Default.Password.TEXT)
        engName = user_content[0][
            'engagement_manual_id'] + ": " + user_content[0]['vfName']
        vf_left_nav_id = "clickable-" + engName
        Click.id(vf_left_nav_id)
        Click.id(Constants.Dashboard.Overview.TeamMember.ID)
        Wait.text_by_css(Constants.Dashboard.Wizard.Title.CSS,
                         Constants.Dashboard.Wizard.InviteTeamMembers.Title.TEXT)
        Enter.text_by_name("email", user_content[1]['email'])
        Wait.text_by_css(Constants.SubmitButton.CSS,
                         Constants.Dashboard.Wizard.InviteTeamMembers.Button.TEXT)
        Click.css(Constants.SubmitButton.CSS)
        Wait.id(Constants.Toast.ID)
        Helper.internal_assert(
            Get.by_id(Constants.Toast.ID), "Invite couldn't be created")

    '''
     If there are 5 invitations for a specific email in the last 24 hours for a particular standard user
     and/or email do not send an email. Note: ELs and admins do not have a limit for how many invitations 
     they can get per 24 hours.
    '''
    @exception()
    def test_5_invitations_for_specific_SU_last_24_hours(self):
        user_content = []
        for _ in range(2):
            user_content.append(
                API.Bridge.create_engagement(wait_for_gitlab=False))
        #    Login with 1st user    #
        Frontend.User.login(
            user_content[0]['email'], Constants.Default.Password.TEXT)
        vf_left_nav_id = Frontend.Invite.invite_users(user_content)
        #    Login with 1st user    #
        Frontend.User.login(
            user_content[0]['email'], Constants.Default.Password.TEXT)
        x = 4
        Frontend.Invite.invite_x_users(user_content, vf_left_nav_id, x)
        #    Invite 6    #
        Frontend.Invite.invite_and_validate_limit(user_content, vf_left_nav_id)

    '''
    If there are more than 25 invitations for an invited_by_user_uuid 
    corresponding to an normal standard users and read only admins, 
    do not send the invite.
    '''
    @exception()
    def test_25_invitations_for_an_invited_by_user_uuid(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        list_of_invite_emails = []
        list_of_invite_emails.append(
            Constants.Users.LongEmailLengthStandardUser.EMAIL)
        for _ in range(29):
            list_of_invite_emails.append(Helper.rand_string("email"))
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)
        engName = user_content[
            'engagement_manual_id'] + ": " + user_content['vfName']
        vf_left_nav_id = "clickable-" + engName
        Frontend.User.open_invite_team_member_form(vf_left_nav_id)
        countOfem = 2
        countofUser = 0
        Frontend.Invite.invite_x_users_from_tm(
            list_of_invite_emails, countofUser, countOfem, 9)
        #    Next 10 Users    #
        countOfem2 = 2
        countofUser2 = 10
        Click.id(
            Constants.Dashboard.Overview.TeamMember.ID, wait_for_page=True)
        Wait.text_by_css(Constants.Dashboard.Wizard.Title.CSS,
                         Constants.Dashboard.Wizard.InviteTeamMembers.Title.TEXT)
        Frontend.Invite.invite_x_users_from_tm(
            list_of_invite_emails, countofUser2, countOfem2, 9)
        countOfem3 = 2
        countofUser3 = 20
        Click.id(
            Constants.Dashboard.Overview.TeamMember.ID, wait_for_page=True)
        Wait.text_by_css(Constants.Dashboard.Wizard.Title.CSS,
                         Constants.Dashboard.Wizard.InviteTeamMembers.Title.TEXT)
        Frontend.Invite.invite_x_users_from_tm(
            list_of_invite_emails, countofUser3, countOfem3, 5)
        Wait.text_by_id(Constants.Toast.ID,
                        "Invite couldn't be created", wait_for_page=True)

    def test_3_invitations_new_user_to_3_vfs(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        engName = user_content[
            'engagement_manual_id'] + ": " + user_content['vfName']
        Frontend.Invite.invite_x_users_and_verify_VF_appers_for_invited(
            user_content, engName)
