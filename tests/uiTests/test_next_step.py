
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
from services.frontend.base_actions.wait import Wait
from services.frontend.fe_general import FEGeneral
from services.frontend.fe_next_step import FENextStep
from services.frontend.fe_overview import FEOverview
from services.frontend.fe_user import FEUser
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.types import API, DB, Frontend
from tests.uiTests.test_ui_base import TestUiBase


logger = LoggingServiceFactory.get_logger()


class TestNextStep(TestUiBase):
    user_content = None

    @classmethod
    def setUpClass(cls):
        super(TestNextStep, cls).setUpClass()

        cls.user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)

    @exception()
    def test_add_next_step(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        Frontend.User.login(
            user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        Frontend.Overview.add_next_step()

    @exception()
    def test_add_next_step_via_pr(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        Frontend.User.login(
            user_content['pr_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        Frontend.Overview.add_next_step()

    @exception()
    def test_complete_next_steps(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        steps_uuids = DB.VirtualFunction.return_expected_steps(user_content['engagement_uuid'],
                                                               Constants.EngagementStages.INTAKE, user_content['email'])
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        for step_uuid in steps_uuids:
            Frontend.Overview.complete_next_step_and_wait_for_it_to_disappear(
                step_uuid)
        Helper.internal_assert(Frontend.Overview.get_list_of_next_steps(), [])

    @exception()
    def test_filter_next_steps_by_associated_files(self):
        user_content = API.VirtualFunction.create_engagement()
        API.GitLab.git_clone_push(user_content)
        user_content['session_token'] = "token " + \
            API.User.login_user(user_content['el_email'])

        # Create a checklist in order for the files to be viewed in the Overview. when
        # we want to filter next steps by files in the Overview  - EM shows us
        # files that relate to the VF's CLs)
        API.Checklist.create_checklist(user_content)
        next_step_uuid = API.VirtualFunction.add_next_step(
            user_content, [Constants.Dashboard.Overview.NextSteps.FilterByFileDropDown.FILE0_LINK_TEXT])
        Frontend.User.login(
            user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        Frontend.Overview.next_steps_filter_by_files()
        Helper.internal_assert(Frontend.Overview.get_next_step_description(0),
                               DB.VirtualFunction.select_next_step_description(next_step_uuid))

    @exception()
    def test_filter_next_steps_by_associated_files_via_pr(self):
        user_content = API.VirtualFunction.create_engagement()
        API.GitLab.git_clone_push(user_content)
        user_content['session_token'] = "token " + \
            API.User.login_user(user_content['el_email'])
        API.Checklist.create_checklist(user_content)
        next_step_uuid = API.VirtualFunction.add_next_step(
            user_content, [Constants.Dashboard.Overview.NextSteps.FilterByFileDropDown.FILE0_LINK_TEXT])
        Frontend.User.login(
            user_content['pr_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        Frontend.Overview.next_steps_filter_by_files()
        Helper.internal_assert(Frontend.Overview.get_next_step_description(0),
                               DB.VirtualFunction.select_next_step_description(next_step_uuid))

    @exception()
    def test_delete_next_step(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        Frontend.User.login(
            user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        steps_uuids = DB.VirtualFunction.select_next_steps_uuids_by_stage(user_content['engagement_uuid'],
                                                                          Constants.EngagementStages.INTAKE)
        for idx, step_uuid in enumerate(steps_uuids):
            Frontend.Overview.delete_next_step(step_uuid)
            logger.debug("Next step deleted! (%s of %s)" %
                         (idx + 1, len(steps_uuids)))

    @exception()
    def test_delete_next_step_via_pr(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        Frontend.User.login(
            user_content['pr_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        steps_uuids = DB.VirtualFunction.select_next_steps_uuids_by_stage(user_content['engagement_uuid'],
                                                                          Constants.EngagementStages.INTAKE)
        for idx, step_uuid in enumerate(steps_uuids):
            Frontend.Overview.delete_next_step(step_uuid)
            logger.debug("Next step deleted! (%s of %s)" %
                         (idx + 1, len(steps_uuids)))

    @exception()
    def test_next_steps_ordering(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        user_content['session_token'] = "token " + \
            API.User.login_user(user_content['email'])
        steps_uuids = DB.VirtualFunction.return_expected_steps(user_content['engagement_uuid'],
                                                               Constants.EngagementStages.INTAKE, user_content['email'])
        Frontend.User.login(
            user_content['email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        Click.id(Constants.Dashboard.Overview.NextSteps.StateDropDown.ID)
        Click.link_text(
            Constants.Dashboard.Overview.NextSteps.StateDropDown.COMPLETED_LINK_TEXT)
        Click.id(Constants.Dashboard.Overview.NextSteps.StateDropDown.ID,
                 wait_for_page=True)
        Frontend.Overview.validate_next_steps_order(steps_uuids)
        for idx, step_uuid in enumerate(steps_uuids):
            DB.VirtualFunction.update_next_step_position(
                step_uuid, len(steps_uuids) - idx)
        Frontend.General.refresh()
        Click.id(Constants.Dashboard.Overview.NextSteps.StateDropDown.ID,
                 wait_for_page=True)
        Click.link_text(
            Constants.Dashboard.Overview.NextSteps.StateDropDown.COMPLETED_LINK_TEXT, wait_for_page=True)
        Click.id(Constants.Dashboard.Overview.NextSteps.StateDropDown.ID,
                 wait_for_page=True)
        Frontend.Overview.validate_next_steps_order(
            list(reversed(steps_uuids)))

    @exception()
    def test_next_step_with_empty_associated_files(self):
        Frontend.User.login(
            self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(self.user_content)
        Frontend.Overview.validate_empty_associated_files()

    @exception()
    def test_next_step_with_associated_files(self):
        user_content = API.VirtualFunction.create_engagement()
        API.GitLab.git_clone_push(user_content)
        user_content['session_token'] = "token " + \
            API.User.login_user(user_content['el_email'])
        Wait.page_has_loaded()
        cl_content = API.Checklist.create_checklist(user_content)
        DB.Checklist.state_changed(
            "name", cl_content['name'], Constants.ChecklistStates.Review.TEXT)
        new_cl_uuid = DB.Checklist.get_recent_checklist_uuid(cl_content['name'])[
            0]
        API.Checklist.add_checklist_next_step(user_content, new_cl_uuid)
        Frontend.User.login(
            user_content['pr_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        Frontend.Overview.next_steps_filter_by_files()
        Frontend.Overview.validate_associated_files(
            Constants.Dashboard.Overview.NextSteps.FilterByFileDropDown.FILE0_LINK_TEXT)

    @exception()
    def test_all_vf_gitlab_repo_files_can_be_chosen_in_new_ns(self):
        newObj, user_content = API.User.create_new_user_content()
        user_content['session_token'] = "token " + \
            API.User.login_user(user_content['el_email'])
        checklist = API.Checklist.create_checklist(user_content)
        DB.Checklist.state_changed(
            "uuid", checklist['uuid'], Constants.ChecklistStates.Review.TEXT)
        Frontend.User.relogin(
            user_content['el_email'], 'iceusers')
        eng_id = "clickable-%s: %s" % (
            user_content['engagement_manual_id'], user_content['vfName'])
        Frontend.Checklist.go_to_checklist(eng_id, checklist['uuid'])
        Frontend.Checklist.get_to_create_new_ns_modal()
        files = API.VirtualFunction.get_engagement(user_content)["files"]
        FEGeneral.verify_existing_files_in_list(
            files, 'associated-files-list')

    @exception()
    def test_ns_choose_all_vf_gitlab_repo_files_via_select_all(self):
        self.user_content['session_token'] = "token " + \
            API.User.login_user(self.user_content['el_email'])
        API.GitLab.git_clone_push(self.user_content)
        cl_content = API.Checklist.create_checklist(self.user_content)
        FEUser.login(self.user_content['el_email'],
                     Constants.Default.Password.TEXT)
        FEOverview.click_on_vf(self.user_content)
        Frontend.Checklist.get_to_create_new_ns_modal_via_overview()
        FENextStep.check_select_deselect_all_files()
