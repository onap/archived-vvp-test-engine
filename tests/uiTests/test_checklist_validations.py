
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
from asyncio.tasks import sleep
import time

from wheel.signatures import assertTrue

from iceci.decorator.exception_decor import exception
from services.api.api_bridge import APIBridge
from services.api.api_gitlab import APIGitLab
from services.constants import Constants
from services.frontend.base_actions.get import Get
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.types import Frontend, DB, API
from tests.uiTests.test_ui_base import TestUiBase


logger = LoggingServiceFactory.get_logger()


class TestChecklistValidations(TestUiBase):
    '''
    Name: test_Create_New_Checklist
    Steps:

    '''

    user_content = None
    user_content_api = None

    @classmethod
    def setUpClass(cls):
        super(TestChecklistValidations, cls).setUpClass()

        cls.user_content_api = API.User.create_new_user_content_login_with_api()
        cls.user_content = API.VirtualFunction.create_engagement()

    @exception()
    def test_create_new_checklist(self):
        API.GitLab.git_clone_push(self.user_content)
        Frontend.User.login(
            self.user_content['email'], Constants.Default.Password.TEXT)
        vfName = self.user_content['vfName']
        # Fetch one AT&T user ID.
        engagement_id = DB.General.select_where(
            "engagement_id", "ice_vf", "name", vfName, 1)
        engLeadEmail = DB.User.select_el_email(vfName)
        engagement_manual_id = DB.General.select_where(
            "engagement_manual_id", "ice_engagement", "uuid", engagement_id, 1)
        myVfName = engagement_manual_id + ": " + vfName
        actualVfNameid = "clickable-" + myVfName
        Frontend.Overview.click_on_vf(self.user_content)
        Frontend.Overview.complete_defaults_nextsteps(engagement_id)
        Frontend.User.relogin(
            engLeadEmail, Constants.Default.Password.TEXT, engagement_manual_id)
        Frontend.Overview.click_on_vf(self.user_content)
        actualVfName = Get.by_id(actualVfNameid)
        checklistName = Frontend.Checklist.create_checklist(
            engagement_id, vfName, actualVfName, engagement_manual_id)
        Frontend.Checklist.click_on_checklist(self.user_content, checklistName)

    @exception()
    def test_e2e_checklist_positive_test(self):
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
            checklistName, user_content['vfName'], "review")

        Frontend.Checklist.cl_to_next_stage(actualVfNameid)
        engPeerReviewerLeadEmail = DB.Checklist.get_pr_email(checklistUuid)
        Frontend.User.relogin(engPeerReviewerLeadEmail,
                              Constants.Default.Password.TEXT)
        Frontend.Checklist.click_on_checklist(user_content, checklistName)
        Frontend.Checklist.validate_reject_is_enabled()
        Frontend.Checklist.review_state_actions_and_validations(
            checklistName, user_content['vfName'], "PEER")

        Frontend.Checklist.cl_to_next_stage(actualVfNameid)
        engPeerReviewerLeadEmail = DB.Checklist.get_admin_email(checklistUuid)
        Frontend.User.relogin(engPeerReviewerLeadEmail,
                              Constants.Default.Password.TEXT)
        Frontend.Checklist.search_by_vfname_for_not_local(user_content)
        Frontend.Checklist.click_on_checklist(user_content, checklistName)
        Frontend.Checklist.validate_reject_is_enabled()
        Frontend.Checklist.approval_state_actions_and_validations(
            checklistName, newObj, "APPROVAL")

        Frontend.Checklist.cl_to_next_stage(actualVfNameid)
        Frontend.User.relogin(engLeadEmail, Constants.Default.Password.TEXT)
        ownerLeadEmail = DB.Checklist.get_owner_email(checklistUuid)
        Helper.internal_assert(engLeadEmail, ownerLeadEmail)
        Frontend.Checklist.click_on_checklist(user_content, checklistName)
        Frontend.Checklist.approval_state_actions_and_validations(
            checklistName, newObj, "HANDOFF")

        Frontend.Checklist.cl_to_next_stage(actualVfNameid)
        Frontend.Checklist.click_on_checklist(user_content, checklistName)

    @exception()
    def test_e2e_checklist_reject(self):
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
            checklistName, user_content['vfName'], "review")
        Frontend.Checklist.cl_to_next_stage(actualVfNameid)
        engPreeRiviewerLeadEmail = DB.Checklist.get_pr_email(checklistUuid)
        Frontend.User.relogin(engPreeRiviewerLeadEmail,
                              Constants.Default.Password.TEXT)
        Frontend.Checklist.click_on_checklist(user_content, checklistName)
        Frontend.Checklist.validate_reject_is_enabled()
        Frontend.Checklist.review_state_actions_and_validations(
            checklistName, user_content['vfName'], "PEER")

        Frontend.Checklist.reject_checklist(newObj, checklistName)

        archive = DB.Checklist.is_archive(checklistName)
        assertTrue(archive)

    @exception()
    def test_e2e_checklist_update_add_next_step(self):
        newObj, user_content = API.User.create_new_user_content()
        newObjWithChecklist = Frontend.Checklist.create_new_checklist(newObj)
        checklistUuid = newObjWithChecklist[0]
        engLeadEmail = newObjWithChecklist[1]
        engagement_manual_id = newObjWithChecklist[2]
        actualVfNameid = newObjWithChecklist[3]
        myVfName = newObjWithChecklist[4]
        checklistName = newObjWithChecklist[5]
        DB.Checklist.state_changed(
            "uuid", checklistUuid, Constants.ChecklistStates.Review.TEXT)
        DB.Checklist.update_decisions(checklistUuid, checklistName)

        Frontend.User.relogin(
            engLeadEmail, Constants.Default.Password.TEXT, engagement_manual_id)
        Frontend.Checklist.click_on_checklist(user_content, checklistName)
        Frontend.Checklist.validate_reject_is_enabled()

        newFileNames = Frontend.Checklist.update_cl_name_and_associated_files(
            engagement_manual_id)
        DB.Checklist.update_checklist_to_review_state(newFileNames[0])
        Frontend.General.refresh()
        Frontend.Checklist.add_nsteps(
            checklistUuid, actualVfNameid, myVfName, checklistName, newFileNames)

    @exception()
    def test_multi_el(self):
        checklist_content = API.Checklist.create_checklist(
            self.user_content_api)
        newEL_content = API.VirtualFunction.create_engagement()
        Frontend.User.login(
            self.user_content_api['email'], Constants.Default.Password.TEXT)
        myVfName = self.user_content_api['engagement_manual_id'] + \
            ": " + self.user_content_api['vfName']
        actualVfNameid = "clickable-" + myVfName
        DB.Checklist.update_decisions(
            checklist_content['uuid'], checklist_content['name'])
        Frontend.User.relogin(
            self.user_content_api['el_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(self.user_content_api)
        Frontend.Checklist.validate_multi_eng(
            self.user_content_api, checklist_content, newEL_content, actualVfNameid)

    @exception()
    def test_create_checklist_without_files(self):
        Frontend.User.login(
            self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Checklist.create_cl_without_files(self.user_content)

    @exception()
    def test_reject_anytime_checklist(self):
        cl_content = API.Checklist.create_checklist(self.user_content_api)
        DB.Checklist.state_changed(
            "name", cl_content['name'], Constants.ChecklistStates.Review.TEXT)
        Frontend.User.login(
            self.user_content_api['el_email'], Constants.Default.Password.TEXT)
        Frontend.Checklist.search_by_manual_id(
            self.user_content_api['engagement_manual_id'])
        recent_checklist_uuid = DB.Checklist.get_recent_checklist_uuid(
            cl_content['name'])[0]
        Frontend.Checklist.click_on_checklist(
            self.user_content_api, cl_content['name'], recent_checklist_uuid)
        Frontend.Checklist.reject("Reject checklist on review state.")
        DB.Checklist.state_changed(
            "uuid", recent_checklist_uuid, Constants.ChecklistStates.Archive.TEXT)

    @exception()
    def test_clone_decision_auditlogs(self):
        cl_content = API.Checklist.create_checklist(self.user_content_api)
        DB.Checklist.state_changed(
            "name", cl_content['name'], Constants.ChecklistStates.Review.TEXT)
        Frontend.User.login(self.user_content_api['el_email'], Constants.Default.Password.TEXT,
                            self.user_content_api['engagement_manual_id'])
        recent_checklist_uuid = DB.Checklist.get_recent_checklist_uuid(
            cl_content['name'])[0]
        Frontend.Checklist.click_on_checklist(
            self.user_content_api, cl_content['name'], recent_checklist_uuid)
        log_txt = Frontend.Checklist.add_line_item_audit_log()
        Frontend.Checklist.reject(
            'Reject checklist as part of test_clone_decision_auditlogs test')
        DB.Checklist.state_changed(
            "uuid", recent_checklist_uuid, Constants.ChecklistStates.Archive.TEXT)
        recent_checklist_uuid = DB.Checklist.get_recent_checklist_uuid(
            cl_content['name'])[0]
        Frontend.Checklist.click_on_checklist(
            self.user_content_api, cl_content['name'], recent_checklist_uuid)
        Frontend.Checklist.validate_audit_log(log_txt)

    @exception()
    def test_review_jenkins_log(self):
        cl_content = API.Checklist.create_checklist(
            self.user_content_api)
        DB.Checklist.state_changed(
            "name", cl_content['name'], Constants.ChecklistStates.Review.TEXT)
        Frontend.User.login(self.user_content_api['el_email'], Constants.Default.Password.TEXT,
                            self.user_content_api['engagement_manual_id'])
        Frontend.Checklist.click_on_checklist(
            self.user_content_api, cl_content['name'], cl_content['uuid'])
        Frontend.Checklist.get_jenkins_log()

    @exception()
    def test_review_jenkins_after_archiving(self):
        cl_content = API.Checklist.create_checklist(
            self.user_content_api)
        DB.Checklist.state_changed(
            "name", cl_content['name'], Constants.ChecklistStates.Review.TEXT)
        Frontend.User.login(self.user_content_api['el_email'], Constants.Default.Password.TEXT,
                            self.user_content_api['engagement_manual_id'])
        cl_content['uuid'] = DB.Checklist.get_recent_checklist_uuid(
            cl_content['name'])[0]
        Frontend.Checklist.click_on_checklist(
            self.user_content_api, cl_content['name'], cl_content['uuid'])
        log_1 = Frontend.Checklist.get_jenkins_log()
        build_identifier_1 = API.Jenkins.find_build_num_out_of_jenkins_log(
            log_1)
        Frontend.Checklist.reject(
            'Reject checklist as part of test_clone_decision_auditlogs test')
        DB.Checklist.state_changed(
            "uuid", cl_content['uuid'], Constants.ChecklistStates.Archive.TEXT)

        recent_checklist_uuid = DB.Checklist.get_recent_checklist_uuid(
            cl_content['name'])[0]
        Frontend.Checklist.click_on_checklist(
            self.user_content_api, cl_content['name'], recent_checklist_uuid)
        Frontend.Checklist.update_cl_associated_files(
            self.user_content_api['engagement_manual_id'])
        DB.Checklist.state_changed(
            "name", cl_content['name'], Constants.ChecklistStates.Review.TEXT)
        Frontend.General.refresh()
        log_2 = Frontend.Checklist.get_jenkins_log()
        build_identifier_2 = API.Jenkins.find_build_num_out_of_jenkins_log(
            log_2)
        Helper.internal_not_equal(build_identifier_1, build_identifier_2)
