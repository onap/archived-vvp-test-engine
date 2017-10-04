 
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
from django.conf import settings

from iceci.decorator.exception_decor import exception
from services.constants import Constants
from services.logging_service import LoggingServiceFactory
from services.session import session
from services.types import API, DB, Frontend
from tests.uiTests.test_ui_base import TestUiBase

logger = LoggingServiceFactory.get_logger()


class TestAdminDropdown(TestUiBase):
    user_content = None

    @classmethod
    def setUpClass(cls):
        super(TestAdminDropdown, cls).setUpClass()

        cls.user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)

    @exception()
    def test_archive_engagement(self):
        Frontend.User.login(
            Constants.Users.Admin.EMAIL, Constants.Default.Password.TEXT)
        # Creating new engagement because we will archive it
        user_content = API.Bridge.create_engagement()
        API.VirtualFunction.set_eng_stage(
            user_content, Constants.EngagementStages.ACTIVE)
        # Verify users were added to git (only after git finishes its work on
        # the engagement we are able to archive the engagement)
        path_with_namespace = user_content[
            'engagement_manual_id'] + "%2F" + user_content['vfName']
        if not API.GitLab.validate_git_project_members(path_with_namespace, user_content['email']):
            raise Exception(
                "Couldn't find the engagement lead user (%s) in GitLab." % user_content['email'])
        Frontend.Dashboard.statuses_search_vf(
            user_content['engagement_manual_id'], user_content['vfName'])
        Frontend.Overview.click_on_archeive_engagement_from_dropdown()
        Frontend.Overview.archive_engagement_modal(
            user_content['engagement_manual_id'], user_content['vfName'])

    @exception()
    def test_change_reviewer(self):
        try:
            Frontend.User.login(
                Constants.Users.Admin.EMAIL, Constants.Default.Password.TEXT)
            user_content = API.VirtualFunction.create_engagement(
                wait_for_gitlab=False)
            other_user = DB.User.select_el_not_in_engagement(
                user_content['el_name'], user_content['pr_name'])
            Frontend.Dashboard.statuses_search_vf(
                user_content['engagement_manual_id'], user_content['vfName'])
            Frontend.Overview.click_on_change_reviewer_from_dropdown()
            Frontend.Overview.change_engagement_lead_modal(other_user)
        finally:
            DB.User.rollback_for_el_not_in_engagement()

    @exception()
    def test_change_peer_reviewer(self):
        try:
            Frontend.User.login(
                Constants.Users.Admin.EMAIL, Constants.Default.Password.TEXT)
            other_user = DB.User.select_el_not_in_engagement(
                self.user_content['el_name'], self.user_content['pr_name'])
            Frontend.Dashboard.statuses_search_vf(
                self.user_content['engagement_manual_id'], self.user_content['vfName'])
            Frontend.Overview.click_on_change_peer_reviewer_from_dropdown()
            Frontend.Overview.change_engagement_lead_modal(
                other_user, is_reviewer=False)
        finally:
            DB.User.rollback_for_el_not_in_engagement()

    @exception()
    def test_update_status(self):
        Frontend.User.login(
            Constants.Users.Admin.EMAIL, Constants.Default.Password.TEXT)
        Frontend.Dashboard.statuses_search_vf(
            self.user_content['engagement_manual_id'], self.user_content['vfName'])
        Frontend.Overview.click_on_update_status_from_dropdown()
        Frontend.Overview.fill_update_status_form_admin_dropdown()

    @exception()
    def test_update_status_via_EL(self):
        Frontend.User.login(
            self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Dashboard.statuses_search_vf(
            self.user_content['engagement_manual_id'], self.user_content['vfName'])
        Frontend.Overview.click_on_update_status_from_dropdown()
        Frontend.Overview.fill_update_status_form_admin_dropdown()

    @exception()
    def test_update_status_via_peer_reviewer(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        Frontend.User.login(
            user_content['pr_email'], Constants.Default.Password.TEXT)
        Frontend.Dashboard.statuses_search_vf(
            user_content['engagement_manual_id'], user_content['vfName'])
        Frontend.Overview.click_on_update_status_from_dropdown()
        Frontend.Overview.fill_update_status_form_admin_dropdown()

    @exception()
    def test_update_status_via_other_el(self):
        try:
            Frontend.User.login(
                Constants.Users.Admin.EMAIL, Constants.Default.Password.TEXT)
            other_el = DB.User.select_el_not_in_engagement(
                self.user_content['el_name'], self.user_content['pr_name'])
            other_el_email = DB.User.get_email_by_full_name(other_el)
            Frontend.Dashboard.statuses_search_vf(
                self.user_content['engagement_manual_id'], self.user_content['vfName'])
            engName = self.user_content[
                'engagement_manual_id'] + ": " + self.user_content['vfName']
            vf_left_nav_id = "clickable-" + engName
            Frontend.User.open_invite_team_member_form(vf_left_nav_id)
            Frontend.User.invite_single_user_to_team(other_el_email)
            Frontend.General.re_open(Constants.Default.LoginURL.TEXT)
            Frontend.Overview.invite_and_reopen_link(
                self.user_content, other_el_email)
            Frontend.User.login(other_el_email, Constants.Default.Password.TEXT,
                                Constants.Dashboard.Default.DASHBOARD_ID)
            Frontend.Overview.click_on_update_status_from_dropdown()
            Frontend.Overview.fill_update_status_form_admin_dropdown()
        finally:
            DB.User.rollback_for_el_not_in_engagement()

    @exception()
    def test_remove_standard_users_after_archive_engagement(self):
        Frontend.User.login(
            Constants.Users.Admin.EMAIL, Constants.Default.Password.TEXT)
        # Creating new engagement because we will archive it
        user_content = API.Bridge.create_engagement()
        API.VirtualFunction.set_eng_stage(
            user_content, Constants.EngagementStages.ACTIVE)
        path_with_namespace = user_content[
            'engagement_manual_id'] + "%2F" + user_content['vfName']
        if not API.GitLab.validate_git_project_members(path_with_namespace, user_content['email']):
            raise Exception(
                "Couldn't find the inviter user (%s) in GitLab." % user_content['email'])
        if settings.DATABASE_TYPE != 'local':
            git_user = API.GitLab.get_git_user(user_content['email'])
            git_user_id = str(git_user['id'])
            Frontend.Dashboard.statuses_search_vf(
                user_content['engagement_manual_id'], user_content['vfName'])
            Frontend.Overview.click_on_archeive_engagement_from_dropdown()
            Frontend.Overview.archive_engagement_modal(
                user_content['engagement_manual_id'], user_content['vfName'])
            API.GitLab.negative_validate_git_project_member(
                path_with_namespace, user_content['email'], git_user_id)
