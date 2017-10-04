
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
import datetime

from django.utils import timezone
from selenium.webdriver.support.select import Select

from services.constants import Constants
from services.database.db_general import DBGeneral
from services.database.db_user import DBUser
from services.database.db_virtual_function import DBVirtualFunction
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

class FEOverview:

    @staticmethod
    def click_on_vf(user_content):
        vfFullName = user_content[
            'engagement_manual_id'] + ": " + user_content['vfName']
        Enter.text_by_id(Constants.Dashboard.LeftPanel.SearchBox.ID, user_content[
                         'vfName'])
        Click.id(Constants.Dashboard.LeftPanel.SearchBox.Results.ID %
                 user_content['vfName'])
        Wait.text_by_id(
            Constants.Dashboard.Overview.Title.ID, vfFullName)

    @staticmethod
    def go_to_eng_overview_by_clicking_on_the_created_NS(user_content):
        logger.debug(
            "Go to engagement's overview by clicking on the created Next Step")
        Click.name(user_content['engagement_manual_id'], wait_for_page=True)
        Wait.text_by_id(
            Constants.Dashboard.Overview.Title.ID, user_content['engagement_manual_id'] + ":", wait_for_page=True)
        FEGeneral.re_open(Constants.Default.LoginURL.TEXT)
        logger.debug("Login with EL user " + user_content['el_email'])
        FEUser.login(user_content['el_email'], Constants.Default.Password.TEXT)
        # Query to select all assigned next steps on TODO state    #
        el_native_id = str(DBGeneral.select_where(
            "id", "ice_user_profile", "email", user_content['el_email'], 1))
        queryStr = "SELECT count(*) FROM ice_user_profile AS users, ice_next_step_assignees AS assignees, ice_next_step AS ns WHERE users.id=" + \
            el_native_id + \
            " AND users.id=assignees.iceuserprofile_id AND assignees.nextstep_id=ns.uuid AND ns.state='Incomplete';"
        el_assigned_ns = str(DBGeneral.select_query(queryStr))
        logger.debug("el_assigned_ns=" + el_assigned_ns)
        Wait.page_has_loaded()
        if (int(el_assigned_ns) >= 5):
            logger.debug(
                "EL has 5 or more assigned next steps, checking that only 5 are shown")
            ns_list = Get.by_id("next-steps-list")
            if (ns_list.count("Engagement - ") > 5):
                logger.error("More than 5 next steps are listed in dashboard.")
                raise

    @staticmethod
    def complete_defaults_nextsteps(engagement_id):
        #    NEXT STEP ID
        next_steps = DBVirtualFunction.select_next_steps_uuids_by_stage(
            engagement_id, Constants.EngagementStages.INTAKE)
        for next_step in next_steps:
            Wait.id(next_step)
            Click.id(next_step, wait_for_page=True)

    @staticmethod
    def check_stage_notifications(stage):
        activityLogID = "activity-log-0"
        activityLogMsg = "Engagement stage is now %s" % stage
        uiActivityLog = Get.by_id(activityLogID)
        if activityLogMsg not in uiActivityLog:
            return False
        return True

    @staticmethod
    def check_stage_next_steps(stage, engagement_uuid):
        ns_list = DBGeneral.select_where_and("description", "ice_next_step",
                                             "engagement_id", engagement_uuid,
                                             "engagement_stage", stage, 0)  # List of next steps from DB.
        logger.debug("Got list of Next Steps for current stage " + stage)
        for i in range(len(ns_list)):
            ns_description = ns_list[i]     # Value number i from the list.
            ns_uuid = DBGeneral.select_where_and("uuid", "ice_next_step",
                                                 "engagement_id", engagement_uuid,
                                                 "description", ns_description, 1)
            logger.debug(
                "Compare presented text of next step with the text from DB.")
            portal_ns = Get.by_id("step-" + ns_uuid)
            # Get from UI the text of relevant next step.
            if ns_description not in portal_ns:
                logger.error("Next step wasn't found in stage " + stage)
                raise

    @staticmethod
    def change_engagement_stage(next_stage, is_negative=False):
        # Click on next stage.
        Click.id(Constants.Dashboard.Overview.Stage.Set.ID + next_stage)
        txtLine2ID = "modal-message-" + next_stage
        if is_negative:
            session.run_negative(
                lambda: Wait.id(txtLine2ID), "Error: modal window opened.")
        else:
            Wait.text_by_id(
                txtLine2ID, "Are you sure you want to set the Engagement's stage to " + next_stage + "?")
            # Click on Approve (after validations inside window).
            Click.xpath(
                Constants.Dashboard.Overview.Stage.Approve.XPATH, wait_for_page=True)

    @staticmethod
    def check_progress(expected_progress):
        currentProgress = Get.by_id(
            Constants.Dashboard.Overview.Progress.Percent.ID)
        Helper.internal_assert(currentProgress, expected_progress)

    @staticmethod
    def check_vnf_version(expected_progress):
        current_vnf_value = Get.by_css(
            "." + Constants.Dashboard.Overview.Progress.VnfVersion.CLASS)
        Helper.internal_assert(current_vnf_value, expected_progress)

    @staticmethod
    def set_progress(new_value):
        Click.id(Constants.Dashboard.Overview.Progress.Change.ID)
        Helper.internal_assert(Constants.Dashboard.Overview.Progress.Wizard.Title.TEXT,
                               Get.by_id(Constants.Dashboard.Modal.TITLE_ID))
        Enter.text_by_name(
            Constants.Dashboard.Overview.Progress.Wizard.NAME, new_value)
        Wait.text_by_css(Constants.SubmitButton.CSS,
                         Constants.Dashboard.Overview.Progress.Wizard.Button.TEXT)
        Click.css(Constants.SubmitButton.CSS)
        Wait.modal_to_dissappear()

    @staticmethod
    def delete_next_step(next_step_uuid):
        Click.id("step-" + next_step_uuid, wait_for_page=True)
        Click.id("delete-" + next_step_uuid, wait_for_page=True)
        Wait.text_by_id(
            Constants.Dashboard.GeneralPrompt.Title.ID, "Delete Step")
        Click.id(
            Constants.Dashboard.GeneralPrompt.ApproveButton.ID, wait_for_page=True)
        Wait.id_to_dissappear("test_" + next_step_uuid)

    @staticmethod
    def click_on_admin_dropdown():
        Click.id(
            Constants.Dashboard.Overview.AdminDropdown.ID, wait_for_page=True)

    @staticmethod
    def click_on_archeive_engagement_from_dropdown():
        FEOverview.click_on_admin_dropdown()
        Click.link_text(
            Constants.Dashboard.Overview.AdminDropdown.ArchiveEngagement.LINK_TEXT, wait_for_page=True)

    @staticmethod
    def archive_engagement_modal(engagement_manual_id, vf_name):
        Wait.text_by_id(Constants.Dashboard.Overview.AdminDropdown.ArchiveEngagement.Wizard.Title.ID,
                        Constants.Dashboard.Overview.AdminDropdown.ArchiveEngagement.Wizard.Title.TEXT)
        random_reason = Helper.rand_string()
        Enter.text_by_name(Constants.Dashboard.Overview.AdminDropdown.ArchiveEngagement.Wizard.Reason.NAME,
                           random_reason)
        Click.id(Constants.SubmitButton.ID)
        Wait.text_by_id(Constants.Toast.ID, "Engagement '%s: %s' archived successfully." %
                        (engagement_manual_id, vf_name))
        query = "select archived_time,archive_reason from ice_engagement where engagement_manual_id='{engagement_manual_id}'".format(
            engagement_manual_id=engagement_manual_id)
        archived_time, db_reason = DBGeneral.select_query(query, "list")
        Helper.assertTrue(archived_time != None)
        Helper.internal_assert(random_reason, db_reason)

    @staticmethod
    def click_on_change_reviewer_from_dropdown():
        FEOverview.click_on_admin_dropdown()
        Click.link_text(
            Constants.Dashboard.Overview.AdminDropdown.ChangeReviewer.LINK_TEXT)

    @staticmethod
    def select_engagement_lead_from_list(el_name):
        Wait.name(
            Constants.Dashboard.Overview.AdminDropdown.ChangeReviewer.Wizard.Select.NAME, wait_for_page=True)
        Select(session.ice_driver.find_element_by_name(
            Constants.Dashboard.Overview.AdminDropdown.ChangeReviewer.Wizard.Select.NAME)).select_by_visible_text(el_name)

    @staticmethod
    def change_engagement_lead_modal(el_name, is_reviewer=True):
        Wait.text_by_id(Constants.Dashboard.Overview.AdminDropdown.ChangeReviewer.Wizard.Title.ID,
                        Constants.Dashboard.Overview.AdminDropdown.ChangeReviewer.Wizard.Title.TEXT)
        FEOverview.select_engagement_lead_from_list(el_name)
        if is_reviewer:
            Wait.text_by_id(
                Constants.Toast.ID, Constants.Dashboard.Overview.AdminDropdown.ChangeReviewer.Toast.TEXT)
        else:
            Wait.text_by_id(
                Constants.Toast.ID, Constants.Dashboard.Overview.AdminDropdown.ChangePeerReviewer.Toast.TEXT)

    @staticmethod
    def click_on_change_peer_reviewer_from_dropdown():
        FEOverview.click_on_admin_dropdown()
        Click.link_text(
            Constants.Dashboard.Overview.AdminDropdown.ChangePeerReviewer.LINK_TEXT)
        Wait.text_by_id(Constants.Dashboard.Overview.AdminDropdown.ChangePeerReviewer.Wizard.Title.ID,
                        Constants.Dashboard.Overview.AdminDropdown.ChangePeerReviewer.Wizard.Title.TEXT)

    @staticmethod
    def click_on_update_status_from_dropdown():
        FEOverview.click_on_admin_dropdown()
        Click.link_text(
            Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.LINK_TEXT)
        Wait.text_by_id("update-engagement-status-title", "Update Status")

    @staticmethod
    def fill_update_status_form_admin_dropdown():
        random_string = Helper.rand_string()
        Enter.text_by_name(
            Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.PROGRESS, str(50))
        Enter.date_picker(Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.PROGRESS_CSS,
                          Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.TARGET)
        Enter.date_picker(Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.PROGRESS_CSS,
                          Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.HEAT)
        Enter.date_picker(Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.PROGRESS_CSS,
                          Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.IMAGE_SACN)
        Enter.date_picker(Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.PROGRESS_CSS,
                          Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.AIC)
        Enter.date_picker(Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.PROGRESS_CSS,
                          Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.ASDC)
        Enter.text_by_name(
            Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.STATUS, random_string)
        Click.css(
            Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.SUBMIT, wait_for_page=True)
        Wait.text_by_id(
            Constants.Toast.ID, Constants.Dashboard.Overview.AdminDropdown.UpdateStatus.SUCCESS_MSG, wait_for_page=True)
        Wait.text_by_id(
            Constants.Dashboard.Overview.Status.Description.ID, random_string)

    @staticmethod
    def get_next_step_description(idx):
        return str(Get.by_id("step-description-%s" % idx, wait_for_page=True))

    @staticmethod
    def get_list_of_next_steps():
        i = 0
        ns_list = []
        steps_length = len(
            session.ice_driver.find_elements_by_css_selector(".step-indication > li"))
        while i < steps_length:
            ns_list.append(FEOverview.get_next_step_description(i))
            i += 1
        return ns_list

    @staticmethod
    def validate_next_steps_order(steps_uuids):
        ui_steps = FEOverview.get_list_of_next_steps()
        for idx, step_uuid in enumerate(steps_uuids):
            db_step_text = DBVirtualFunction.select_next_step_description(
                step_uuid)
            Wait.text_by_id(Constants.Dashboard.Overview.NextSteps.Add.Description.STEP_DESC_ID +
                            str(idx), ui_steps[idx], wait_for_page=True)
            if db_step_text != ui_steps[idx]:
                raise AssertionError("Next step is not located in expected index. db_step_text = "
                                     + db_step_text + " ui_steps[idx] = " + ui_steps[idx] + "|| uuid = " + step_uuid)

    @staticmethod
    def next_steps_filter_by_files():
        Click.id(
            Constants.Dashboard.Overview.NextSteps.FilterByFileDropDown.ID)
        Click.link_text(
            Constants.Dashboard.Overview.NextSteps.FilterByFileDropDown.ANY_FILE_LINK_TEXT)
        Click.link_text(
            Constants.Dashboard.Overview.NextSteps.FilterByFileDropDown.FILE0_LINK_TEXT)
        Click.id(
            Constants.Dashboard.Overview.NextSteps.FilterByFileDropDown.ID)

    @staticmethod
    def complete_next_step(step_uuid):
        Click.id(step_uuid)

    @staticmethod
    def complete_next_step_and_wait_for_it_to_disappear(step_uuid):
        Click.id(step_uuid)
        Wait.id_to_dissappear(step_uuid)

    @staticmethod
    def next_steps_filter_by_states():
        Click.id(Constants.Dashboard.Overview.NextSteps.StateDropDown.ID)
        Click.link_text(
            Constants.Dashboard.Overview.NextSteps.StateDropDown.INCOMPLETE_LINK_TEXT)
        Click.link_text(
            Constants.Dashboard.Overview.NextSteps.StateDropDown.COMPLETED_LINK_TEXT)
        Click.id(Constants.Dashboard.Overview.NextSteps.StateDropDown.ID)

    @staticmethod
    def add_next_step():
        Click.id(Constants.Dashboard.Overview.NextSteps.Add.ID)
        Wait.text_by_css(Constants.Dashboard.Overview.NextSteps.Add.Title.CSS,
                         Constants.Dashboard.Overview.NextSteps.Add.Title.TEXT)
        ns_description = "New next step - " + \
            Helper.rand_string("randomString")
        Click.id(Constants.Dashboard.Overview.NextSteps.Add.Description.ID)
        Enter.text_by_id(
            Constants.Dashboard.Overview.NextSteps.Add.Description.ID, ns_description)
        FEWizard.date_picker_add_ns(0)
        Wait.text_by_css(Constants.SubmitButton.CSS,
                         Constants.Dashboard.Overview.NextSteps.Add.Button.TEXT)
        Click.css(Constants.SubmitButton.CSS)
        Wait.modal_to_dissappear()

    @staticmethod
    def click_on_team_member(full_name):
        Click.id(Constants.Dashboard.Overview.TeamMember.MEMBER_ID % full_name)
        Wait.id(Constants.Dashboard.Overview.TeamMember.Title.ID)

    @staticmethod
    def remove_user_from_eng_team(full_name, is_negative=False):
        FEOverview.click_on_team_member(full_name)
        if is_negative:
            Wait.id_to_dissappear(
                Constants.Dashboard.Overview.TeamMember.RemoveUser.ID)
        else:
            Click.id(Constants.Dashboard.Overview.TeamMember.RemoveUser.ID)
            Wait.text_by_id(Constants.Dashboard.GeneralPrompt.UpperTitle.ID,
                            Constants.Dashboard.Overview.TeamMember.RemoveUser.Title.TEXT % full_name)
            Wait.text_by_id(Constants.Dashboard.GeneralPrompt.Title.ID,
                            Constants.Dashboard.Overview.TeamMember.RemoveUser.Message.TEXT)
            Click.id(Constants.Dashboard.GeneralPrompt.ApproveButton.ID)
            FEGeneral.refresh()
            Wait.id_to_dissappear(
                Constants.Dashboard.Overview.TeamMember.MEMBER_ID % full_name)

    @staticmethod
    def invite_and_reopen_link(user_content, other_el_email):
        enguuid = DBGeneral.select_where(
            "uuid", "ice_engagement", "engagement_manual_id", user_content['engagement_manual_id'], 1)
        invitation_token = DBUser.select_invitation_token(
            "invitation_token", "ice_invitation", "engagement_uuid", enguuid, other_el_email, 1)
        inviterURL = Constants.Default.InviteURL.Login.TEXT + invitation_token
        FEGeneral.re_open(inviterURL)

    @staticmethod
    def create_and_verify_VF_with_VFversion():
        Click.id(
            Constants.Dashboard.LeftPanel.AddEngagement.ID, wait_for_page=True)
        vfName = FEWizard.add_vf()
        version_name = DBVirtualFunction.select_vf_version_by_vf_name(vfName)
        vfNameDb = DBVirtualFunction.select_vf_name_by_vf_version(version_name)
        Helper.internal_assert(vfNameDb, vfName)

    @staticmethod
    def validate_empty_associated_files():
        FEOverview.add_next_step()
        Click.id(Constants.Dashboard.Overview.NextSteps.AssociatedFiles.ID)
        Wait.text_by_id(Constants.Dashboard.Overview.NextSteps.AssociatedFiles.EmptyMsgID,
                        Constants.Dashboard.Overview.NextSteps.AssociatedFiles.EmptyMsg)

    @staticmethod
    def validate_associated_files(file_name):
        Click.id(Constants.Dashboard.Overview.NextSteps.AssociatedFiles.ID)
        Wait.text_by_id(
            Constants.Dashboard.Overview.NextSteps.AssociatedFiles.FileId, file_name)

    @staticmethod
    def validate_bucket_url(eng_manual_id, vf_name):
        expected_text = Constants.Dashboard.Overview.BucketURL.TEXT + \
            eng_manual_id + "_" + vf_name.lower()
        Wait.text_by_id(
            Constants.Dashboard.Overview.BucketURL.ID, expected_text, True)

    @staticmethod
    def verify_validation_dates():
        validation_date = Get.by_id(
            Constants.Dashboard.Overview.Progress.ValidationsDates.AIC_ID, True)
        validation_date = datetime.datetime.strptime(
            validation_date, "%m/%d/%y").date()
        current_date = timezone.now().date()
        Helper.internal_assert(validation_date, current_date)

    @staticmethod
    def open_add_next_step_modal_from_overview():
        Click.id(Constants.Dashboard.Overview.NextSteps.Add.ID,
                 wait_for_page=True)
        Wait.text_by_css(Constants.Dashboard.Checklist.AddNS.CSS,
                         Constants.Dashboard.Overview.NextSteps.Add.TITLE)
        Helper.internal_assert(
            Constants.Dashboard.Checklist.AddNS.TITLE,
            Get.by_css(Constants.FEGeneral.CSS.H2))
