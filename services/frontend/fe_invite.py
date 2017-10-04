 
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
from asyncio.tasks import wait

from selenium.webdriver.support.select import Select

from services.api.api_user import APIUser
from services.api.api_virtual_function import APIVirtualFunction
from services.constants import Constants, ServiceProvider
from services.database.db_general import DBGeneral
from services.database.db_user import DBUser
from services.frontend.base_actions.click import Click
from services.frontend.base_actions.enter import Enter
from services.frontend.base_actions.get import Get
from services.frontend.base_actions.wait import Wait
from services.frontend.fe_general import FEGeneral
from services.frontend.fe_user import FEUser
from services.frontend.fe_wizard import FEWizard
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()

class FEInvite:

    @staticmethod
    def invite_users(user_content):
        engName = user_content[0][
            'engagement_manual_id'] + ": " + user_content[0]['vfName']
        vf_left_nav_id = "clickable-" + engName
        Click.id(vf_left_nav_id)
        FEWizard.invite_team_members_modal(user_content[1]['email'])
    #         self.sleep(1)   # TODO need to wait until modal window is closed.
        invitation_token = DBUser.select_invitation_token("invitation_token", "ice_invitation", "engagement_uuid",
                                                          user_content[0]['engagement_uuid'], user_content[1]['email'], 1)
        inviterURL = Constants.Default.InviteURL.Login.TEXT + invitation_token
        FEGeneral.re_open(inviterURL)
    #    Login with 2nd user    #
        title_id = "title-id-" + engName
        FEUser.login(
            user_content[1]['email'], Constants.Default.Password.TEXT, title_id)
        Click.id(vf_left_nav_id)
        actualVfName = Get.by_id(vf_left_nav_id)
        Helper.internal_assert(engName, actualVfName)
        Wait.text_by_id(Constants.Dashboard.Overview.Title.ID, engName)
        FEUser.logout()
        return vf_left_nav_id

    @staticmethod
    def invite_x_users(user_content, vf_left_nav_id, x):
        for _ in range(x):  # Invites 2-5
            Click.id(vf_left_nav_id)
            Click.id(Constants.Dashboard.LeftPanel.AddEngagement.ID)
            FEWizard.add_vf()
            Click.id(
                Constants.Dashboard.Wizard.CloseButton.ID, wait_for_page=True)
            FEWizard.invite_team_members_modal(user_content[1]['email'])
            FEGeneral.refresh()

    @staticmethod
    def invite_and_validate_limit(user_content, vf_left_nav_id):
        Click.id(Constants.Dashboard.LeftPanel.AddEngagement.ID)
        FEWizard.add_vf()
        Click.id(Constants.Dashboard.Wizard.CloseButton.ID, wait_for_page=True)
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

    @staticmethod
    def invite_x_users_from_tm(list_of_invite_emails, countofUser, countOfem, num):
        Enter.text_by_name(
            "email", list_of_invite_emails[countofUser], wait_for_page=True)
        for _ in range(num):
            try:
                session.run_negative(
                    lambda: Click.css("span.add-icon"), "css appears")
                break
            except:  # button exists
                pass
            countofUser += 1
#             Click.css("span.add-icon")
            Wait.xpath("//fieldset[" + str(countOfem) + "]/div/input")
            Enter.text_by_xpath(
                "//fieldset[" + str(countOfem) + "]/div/input", list_of_invite_emails[countofUser])
            countOfem += 1
        Click.css(Constants.SubmitButton.CSS, wait_for_page=True)

    @staticmethod
    def create_x_vfs(user_content, engName, x):
        vflist = []
        FEUser.login(user_content['email'], Constants.Default.Password.TEXT)
        for _ in range(x):
            vf_left_nav_id = "clickable-" + engName
            Click.id(vf_left_nav_id)
            Click.id(Constants.Dashboard.LeftPanel.AddEngagement.ID)
            vfName = FEWizard.add_vf()
            vflist.append(vfName)
            Click.id(
                Constants.Dashboard.Wizard.CloseButton.ID, wait_for_page=True)
        return vflist

    @staticmethod
    def validations_for_user2(user_content, inviteEmail, vflist):
        # Fetch one AT&T user ID.
        engagement_id = DBGeneral.select_where(
            "engagement_id", "ice_vf", "name", vflist[0], 1)
        engagement_manual_id = DBGeneral.select_where(
            "engagement_manual_id", "ice_engagement", "uuid", engagement_id, 1)
        engLeadEmail = DBUser.select_el_email(vflist[0])
        user_content['engagement_uuid'] = engagement_id
        user_content['el_email'] = engLeadEmail
        uuid = DBGeneral.select_where_email(
            "uuid", "ice_user_profile", user_content['email'])
        sponsor = ["AT&T", 'aaaaaa', inviteEmail, '3058000000']
        invitation_token = DBUser.select_invitation_token(
            "invitation_token", "ice_invitation", "engagement_uuid", engagement_id, inviteEmail, 1)
        signUpURLforContact = DBUser.get_contact_signup_url(
            invitation_token, uuid, sponsor[2], sponsor[1], sponsor[3], sponsor[0])
        APIUser.signup_invited_user(
            sponsor[0], inviteEmail, invitation_token, signUpURLforContact, user_content, True, wait_for_gitlab=False)
        activationUrl2 = DBUser.get_activation_url(sponsor[2])
        FEGeneral.re_open(activationUrl2)  # Login with 2nd user    #
        engName = engagement_manual_id + ": " + vflist[0]
        title_id = "clickable-" + engName
        FEUser.login(inviteEmail, Constants.Default.Password.TEXT, title_id)
        for vfName in vflist:
            # Fetch one AT&T user ID.
            engagement_id = DBGeneral.select_where(
                "engagement_id", "ice_vf", "name", vfName, 1)
            engagement_manual_id = DBGeneral.select_where(
                "engagement_manual_id", "ice_engagement", "uuid", engagement_id, 1)
            engName = engagement_manual_id + ": " + vfName
            vf_left_nav_id = "clickable-" + engName
            Click.id(vf_left_nav_id, wait_for_page=True)

    @staticmethod
    def invite_x_users_and_verify_VF_appers_for_invited(user_content, engName):
        inviteEmail = Helper.rand_string('randomString') + "@intl." + ServiceProvider.email
        vflist = FEInvite.create_x_vfs(user_content, engName, x=3)
        for vfName in vflist:
            # Fetch one AT&T user ID.
            engagement_id = DBGeneral.select_where(
                "engagement_id", "ice_vf", "name", vfName, 1)
            engagement_manual_id = DBGeneral.select_where(
                "engagement_manual_id", "ice_engagement", "uuid", engagement_id, 1)
            engName = engagement_manual_id + ": " + vfName
            vf_left_nav_id = "clickable-" + engName
            Click.id(vf_left_nav_id)
            FEWizard.invite_team_members_modal(inviteEmail)
            FEGeneral.refresh()
            # validations
        FEInvite.validations_for_user2(user_content, inviteEmail, vflist)
