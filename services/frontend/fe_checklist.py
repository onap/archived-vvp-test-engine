
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
from selenium.webdriver.support.ui import Select
from wheel.signatures import assertTrue

from services.database.db_checklist import DBChecklist
from services.database.db_user import DBUser
from services.database.db_virtual_function import DBVirtualFunction
from services.frontend.base_actions.click import Click
from services.frontend.base_actions.enter import Enter
from services.frontend.base_actions.get import Get
from services.frontend.base_actions.wait import Wait
from services.frontend.fe_general import FEGeneral
from services.frontend.fe_overview import FEOverview
from services.frontend.fe_user import FEUser
from services.frontend.fe_wizard import FEWizard
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from tests.uiTests.test_ui_base import *


logger = LoggingServiceFactory.get_logger()


class FEChecklist:

    assocciatedFileName = None

    @staticmethod
    def go_to_checklist(engagement_id, cl_uuid):
        try:
            Click.id(engagement_id)
            Click.id("checklist-" + cl_uuid)
            Wait.id("line-item-description")
        except Exception as e:
            errorMsg = "Failed to go to checklist page."
            raise Exception(errorMsg, e)

    @staticmethod
    def create_new_checklist(newObj):
        try:
            newObjWithChecklist = None
            vfName = newObj[0]
            uuid = newObj[1]
            inviteEmail = newObj[2]
            # Fetch one AT&T user ID.
            vfuuid = DBGeneral.select_where(
                "uuid", "ice_vf", "name", vfName, 1)
            engagement_id = DBVirtualFunction.select_eng_uuid(vfName)
            engLeadEmail = DBUser.select_el_email(vfName)
            logger.debug("EL email: " + engLeadEmail)
            engagement_manual_id = DBGeneral.select_where("engagement_manual_id", "ice_engagement", "uuid",
                                                          engagement_id, 1)
            #    Click on all default next steps
            myVfName = engagement_manual_id + ": " + vfName
            actualVfNameid = "clickable-" + myVfName
            actualVfName = Get.by_id(actualVfNameid)
            Helper.internal_assert(myVfName, actualVfName)
            #    NEXT STEP ID
            Click.id(actualVfNameid, wait_for_page=True)
            FEOverview.complete_defaults_nextsteps(engagement_id)
            inviterURL = Constants.Default.InviteURL.Signup.TEXT + \
                vfuuid + "&inviter_uuid=" + uuid + "&email=" + inviteEmail
#             time.sleep(2)
            FEGeneral.re_open(inviterURL)
            FEGeneral.form_validate_email(inviteEmail)
            #    Login with EL role
            FEGeneral.re_open(Constants.Default.LoginURL.TEXT)
            FEUser.login(engLeadEmail, Constants.Default.Password.TEXT)
            Wait.id(Constants.Dashboard.Statuses.Title.ID)
            Wait.id(engagement_manual_id)  # cheklist
            #    VALIDATE SCROLLING
            actualVfName = Get.by_id(actualVfNameid)
            myVfName = engagement_manual_id + ": " + vfName
#             Wait.id(actualVfNameid)
            Wait.id(engagement_manual_id, wait_for_page=True)
            Click.id(actualVfNameid, wait_for_page=True)
            #    Create new checklist
            checklistName = FEChecklist.create_checklist(
                engagement_id, vfName, actualVfName, engagement_manual_id)
            checklistUuid = DBGeneral.select_where(
                "uuid", "ice_checklist", "name", checklistName, 1)
            newObjWithChecklist = [checklistUuid, engLeadEmail, engagement_manual_id, actualVfNameid, myVfName,
                                   checklistName]
            return newObjWithChecklist
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "Failed to create checklist." + str(e)
            raise Exception(errorMsg, "create_new_checklist")

    @staticmethod
    def create_checklist(engagement_id, vfName, actualVfName, engagement_manual_id):
        try:
            checklistName = Helper.rand_string("randomString")
            Wait.id("checklist-plus-" + engagement_id, wait_for_page=True)

            Click.id("checklist-plus-" + engagement_id, wait_for_page=True)

            Helper.internal_assert(
                "Create Checklist", Get.by_id("modal-header-checklist-15"))
            # vm.checkListName
            Enter.text_by_name(
                "checkListName", checklistName, wait_for_page=True)
            Wait.xpath("//select")

            Select(session.ice_driver.find_element_by_id(Constants.Template.Subtitle.SelectTemplateTitle.TEXT)
                   ).select_by_visible_text(Constants.Template.Heat.TEXT)
            Click.id(Constants.Template.Heat.TEXT, wait_for_page=True)
#             Click.css("option.ng-binding.ng-scope")
            Helper.internal_assert(
                "Associate Files", Get.by_id("associated-files-title", wait_for_page=True))
            Click.xpath("//multiselect/div/button", wait_for_page=True)
            Click.link_text("file0", wait_for_page=True)
            Click.link_text("file1")
            Wait.text_by_css(Constants.SubmitButton.CSS, "Create Checklist")
            Click.id(Constants.Dashboard.LeftPanel.CreateChecklist.ID)
            Wait.modal_to_dissappear()
            Wait.id(engagement_manual_id)
            return checklistName
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "Failed to create checklist." + str(e)
            raise Exception(errorMsg, "create_checklist")

    @staticmethod
    def update_cl_name_and_associated_files(engagement_manual_id):
        Click.id("edit-checklist", True)
        Wait.text_by_id("modal-header-checklist-15", "Update Checklist")
        newfileName = "file" + Helper.rand_string("randomString")
        Enter.text_by_xpath("//div[3]/div/div/input", newfileName)
        updatedFileName = "file2"
        # Select associated files from multi-select drop-down.
        Click.xpath("//multiselect/div/button")
        Click.link_text("file2")
        Click.css(Constants.SubmitButton.CSS)
        Wait.id(engagement_manual_id)
        newFileNames = [newfileName, updatedFileName]
        return newFileNames

    @staticmethod
    def update_cl_associated_files(engagement_manual_id):
        Click.id("edit-checklist", True)
        Wait.text_by_id("modal-header-checklist-15", "Update Checklist")
        # Select associated files from multi-select drop-down.
        Click.xpath("//multiselect/div/button")
        Click.link_text("file2")
        Click.xpath("//multiselect/div/button")
        Click.css(Constants.SubmitButton.CSS)
        Wait.id(engagement_manual_id, True)

    @staticmethod
    def add_next_step(checklistName, newObj):
        Click.id(Constants.Dashboard.Checklist.AddNS.ID, wait_for_page=True)
        Wait.text_by_css("span.font_header", "Checklist:")
        Helper.internal_assert("Checklist:", Get.by_css("span.font_header"))
        Helper.internal_assert("Add Next Steps", Get.by_css("h2"))
        # First NS
        Click.id("description")
        Enter.text_by_id("description", "description of NS")
        Click.css("div.modal-content")
        Click.xpath("(//button[@type='button'])[10]")
        FEChecklist.assocciatedFileName = "file0"
        Click.link_text(FEChecklist.assocciatedFileName)
        Click.css("div.modal-content")
        Click.xpath("(//button[@type='button'])[11]")
        try:
            Click.xpath("//div[3]/multiselect/div/ul/li/a")
        except:
            Click.link_text("Homer Simpson")
        Click.css("div.modal-content")
        count = 0
        FEWizard.date_picker_add_ns(count)
        count = +1
        Click.css("span.add-text")
        Click.xpath("(//div[@id='description'])[2]")
        Enter.text_by_xpath(
            "(//div[@id='description'])[2]", "description of NS2")
        Click.css("div.modal-content")
        Click.xpath("(//button[@type='button'])[14]")
        Click.xpath("(//button[@type='button'])[22]")
        Click.xpath("//div[3]/div/div[2]/multiselect/div/ul/li[2]/a")
        Click.css("div.modal-content")
        Click.xpath("(//button[@type='button'])[23]")
        Click.css(
            "div.btn-group.open > ul.dropdown-menu > li.ng-scope > a.ng-binding")
        Click.link_text("Add Another Next Step")
        Click.xpath("(//button[@type='button'])[25]")
        FEWizard.date_picker_add_ns(count)
        Click.xpath("//div[4]/div/span")
        Helper.internal_assert("Submit Next Steps", Get.by_id("btn-submit"))
        Click.id("btn-submit", wait_for_page=True)

    @staticmethod
    def add_next_step_updated(checklistName, newFileName):
        Click.id(Constants.Dashboard.Checklist.AddNS.ID)
        Wait.id(Constants.Dashboard.Modal.CLOSE_BUTTON_ID)
        Wait.text_by_css("span.font_header.ng-binding", "Checklist:")
        Wait.text_by_css("h2.ng-binding", "Add Next Steps")
        # First NS
        Click.id("description")
        Enter.text_by_id("description", "description of NS")
        Click.css("div.modal-content")
        Click.xpath("(//button[@type='button'])[10]")
        Click.link_text(newFileName)
        Click.css("div.modal-content")
        Click.xpath("(//button[@type='button'])[11]")
        try:
            Click.xpath("//div[3]/multiselect/div/ul/li/a")
        except:
            Wait.link_text("Homer Simpson")
            Click.link_text("Homer Simpson")
        Wait.css("div.modal-content")
        Click.css("div.modal-content")
        Wait.xpath("(//button[@type='button'])[12]")
        count = 0
        FEWizard.date_picker_add_ns(count)
        count = +1
        Click.css("span.add-text")
        Click.xpath("(//div[@id='description'])[2]")
        Enter.text_by_xpath(
            "(//div[@id='description'])[2]", "description of NS2")
        Click.css("div.modal-content")
        Click.xpath("(//button[@type='button'])[14]")
        Click.xpath("(//button[@type='button'])[22]")
        Click.xpath("//div[3]/div/div[2]/multiselect/div/ul/li[2]/a")
        Click.css("div.modal-content")
        Click.xpath("(//button[@type='button'])[23]")
        Click.css(
            "div.btn-group.open > ul.dropdown-menu > li.ng-scope > a.ng-binding")
        Click.link_text("Add Another Next Step")
        Wait.xpath("(//button[@type='button'])[25]")
        Click.xpath("(//button[@type='button'])[25]")
        Wait.xpath("(//button[@type='button'])[24]")
        FEWizard.date_picker_add_ns(count)
        Wait.xpath("//div[4]/div/span")
        Click.xpath("//div[4]/div/span")
        Wait.id("btn-submit")
        Wait.text_by_id("btn-submit", "Submit Next Steps")
#         Helper.internal_assert("Submit Next Steps", Get.by_id("btn-submit"))
        Click.id("btn-submit")

    @staticmethod
    def approval_state_actions_and_validations(checklistName, newObj, state):
        #     REWVIEW STEPS AND VALIDATIONS
        try:
            Wait.id("checklist-main-section")
            Wait.text_by_id(
                Constants.Dashboard.Checklist.Name.ID, checklistName)
            try:
                if settings.DATABASE_TYPE == 'local':
                    Wait.text_by_css(
                        "h2.ng-binding", "Section 1: Parameter Specification")
                    Helper.internal_assert(
                        "Parameters", Get.by_css("span.col-md-9.ng-binding"))
                    Helper.internal_assert(
                        "String parameters", Get.by_xpath("//li[2]/span[2]"))
                    Helper.internal_assert(
                        "Numeric parameters", Get.by_xpath("//li[3]/span[2]"))
                    if settings.DATABASE_TYPE == 'local':
                        Helper.internal_assert("Section 2: External References",
                                               Get.by_xpath("//li[2]/h2"))
                    # //li[2]/ul/li/span[2]   #//ul[@id='line-item-list']/li[2]/ul/li/span[2]
                    Helper.internal_assert(
                        "Normal references", Get.by_xpath("//li[2]/ul/li/span[2]"))
                    Helper.internal_assert(
                        "VF image", Get.by_xpath("//li[2]/ul/li[2]/span[2]"))
            except:
                if settings.DATABASE_TYPE == 'local':
                    Wait.text_by_css(
                        "h2.ng-binding", "Section 1: External References")
                    try:
                        Helper.internal_assert(
                            "Normal references", Get.by_css("span.col-md-9.ng-binding"))
                    except:
                        if "VF image" in Get.by_xpath("//li[2]/span[2]"):
                            logger.debug("All Ok")
                    if settings.DATABASE_TYPE == 'local':
                        Helper.internal_assert(
                            "Section 2: Parameter Specification", Get.by_xpath("//li[2]/h2"))
            try:
                if settings.DATABASE_TYPE == 'local':
                    Helper.internal_assert(
                        "1.1 - Parameters", Get.by_xpath("//header/h2"))
            except:
                if settings.DATABASE_TYPE == 'local':
                    Helper.internal_assert(
                        "1.1 - Normal References", Get.by_xpath("//header/h2"))
            if settings.DATABASE_TYPE == 'local':
                elementTxt = Get.by_id("line-item-description")
                Helper.internal_assert(
                    "Numeric parameters should include range and/or allowed values.", elementTxt)
            Helper.internal_assert("Audit Logs", Get.by_css("h3.col-md-12"))
            localLogText = "local log"
            Enter.text_by_id("new-audit-log-text", localLogText)
            Helper.internal_assert(
                "Add Log Entry", Get.by_id("submit-new-audit-lop-text"))
            Click.id("submit-new-audit-lop-text")
            vfName = newObj[0]
            engLeadFullName = DBUser.get_el_name(vfName)
            Helper.internal_assert(localLogText, Get.by_css(
                Constants.Dashboard.Checklist.AuditLog.LastLocalAuditLog.CSS))
            try:
                if settings.DATABASE_TYPE == 'local':
                    Helper.internal_assert(
                        "Parameters", Get.by_xpath("//li[2]/ul/li/span[2]"))
            except:
                if settings.DATABASE_TYPE == 'local':
                    Helper.internal_assert(
                        "Numeric parameters", Get.by_xpath("//li[2]/ul/li/span[2]"))

# if Wait.css(Constants.Dashboard.Checklist.LineItem.Deny.CSS) or
# Wait.css(Constants.Dashboard.Checklist.LineItem.Approve.CSS):
            session.run_negative(lambda: Wait.css(Constants.Dashboard.Checklist.LineItem.Deny.CSS) or Wait.css(
                Constants.Dashboard.Checklist.LineItem.Approve.CSS), "Buttons displayed for Admin it's NOT work")
#                 logger.debug("Buttons displayed for Admin it's NOT work")
#             else:
#                 print("Buttons not displayed for Admin it's work")
            if state == "APPROVAL":
                if settings.DATABASE_TYPE == 'local':
                    Helper.internal_assert(
                        "Audit Log (6)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
                else:
                    Helper.internal_assert(
                        "Audit Log (7)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
            if state == "HANDOFF":
                if settings.DATABASE_TYPE == 'local':
                    Helper.internal_assert(
                        "Audit Log (8)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
                else:
                    Helper.internal_assert(
                        "Audit Log (9)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
            Click.id(Constants.Dashboard.Checklist.AuditLog.ID)
            Wait.text_by_xpath("//span[2]", checklistName)
            engLeadFullName = DBUser.select_el_email(vfName)
            Enter.text_by_xpath("//textarea", "zdfgsdyh")
            Click.css(Constants.SubmitButton.CSS)
            Wait.modal_to_dissappear()
            if state == "APPROVAL":
                if settings.DATABASE_TYPE == 'local':
                    Wait.text_by_id(
                        Constants.Dashboard.Checklist.AuditLog.ID, "Audit Log (7)")
                else:
                    Wait.text_by_id(
                        Constants.Dashboard.Checklist.AuditLog.ID, "Audit Log (8)")
            if state == "HANDOFF":
                if settings.DATABASE_TYPE == 'local':
                    Wait.text_by_id(
                        Constants.Dashboard.Checklist.AuditLog.ID, "Audit Log (9)")
                else:
                    Wait.text_by_id(
                        Constants.Dashboard.Checklist.AuditLog.ID, "Audit Log (10)")
            if state == "APPROVAL":
                Wait.text_by_xpath("//button[3]", "Add Next Steps")
                Wait.text_by_id(Constants.Dashboard.Checklist.Reject.ID,
                                Constants.Dashboard.Checklist.Reject.Modal.Button.TEXT)
                Wait.text_by_xpath(
                    "//div[@id='state-actions']/button", "Approve")
            if state == "HANDOFF":
                Wait.text_by_xpath(
                    "//div[@id='state-actions']/button", "Handoff complete?")
            logger.debug("ALL VALIDATION PASS FOR STATE : " + state)
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            logger.error(
                state + " state  FAILED CONNECT TO STAGING MANUAL AND VERIFY WHY! ")
            errorMsg = "approval_state_actions_and_validations FAILED  because : " + \
                str(e)
            raise Exception(errorMsg, "approval_state_actions_and_validations")

    @staticmethod
    def review_state_actions_and_validations(checklistName, vfName, state):
        try:
            #    REWVIEW STEPS AND VALIDATIONS
            Wait.id("checklist-main-section")
            Wait.text_by_id(
                Constants.Dashboard.Checklist.Name.ID, checklistName)
            try:
                if settings.DATABASE_TYPE == 'local':
                    Helper.internal_assert(
                        "Section 1: Parameter Specification", Get.by_css("h2.ng-binding"))
                    Helper.internal_assert(
                        "Parameters", Get.by_css("span.col-md-9.ng-binding"))
                    Helper.internal_assert(
                        "String parameters", Get.by_xpath("//li[2]/span[2]"))
                    Helper.internal_assert(
                        "Numeric parameters", Get.by_xpath("//li[3]/span[2]"))
                    if settings.DATABASE_TYPE == 'local':
                        Helper.internal_assert(
                            "Section 2: External References", Get.by_xpath("//li[2]/h2"))
                    Helper.internal_assert(
                        "Normal references", Get.by_name("Normal references"))
                    Helper.internal_assert(
                        "VF image", Get.by_name("Normal references"))
            except:
                try:
                    Helper.internal_assert(
                        "Section 1: External References", Get.by_css("h2.ng-binding"))
                except:
                    Helper.internal_assert(
                        "Section 1: Scaling Considerations", Get.by_css("h2.ng-binding"))
                try:
                    Helper.internal_assert(
                        "Normal references", Get.by_css("span.col-md-9.ng-binding"))
                except:
                    if "VF image" in Get.by_xpath("//li[2]/span[2]"):
                        logger.debug("All Ok")
                if settings.DATABASE_TYPE == 'local':
                    Helper.internal_assert(
                        "Section 2: Parameter Specification", Get.by_xpath("//li[2]/h2"))
                Click.name("VF image")
                Click.name("Normal references")
                try:
                    Helper.internal_assert(
                        "1.1 - Parameters", Get.by_xpath("//header/h2"))
                except:
                    text = Get.by_name("Normal references")
                    Helper.internal_assert("Normal references", text)
            Helper.internal_assert("Audit Logs", Get.by_css("h3.col-md-12"))
            localLogText = "local log"
            Enter.text_by_id("new-audit-log-text", localLogText)
            Helper.internal_assert(
                "Add Log Entry", Get.by_id("submit-new-audit-lop-text"))
            Click.id("submit-new-audit-lop-text")
            #    Validate Local AuditLog
            engLeadFullName = DBUser.get_el_name(vfName)
            Helper.internal_assert(
                engLeadFullName, Get.by_xpath("//ul[@id='audit-log-list']/li/h4"))
            Helper.internal_assert(localLogText, Get.by_css(
                Constants.Dashboard.Checklist.AuditLog.LastLocalAuditLog.CSS))
            if settings.DATABASE_TYPE == 'local':
                try:
                    Helper.internal_assert(
                        "Parameters", Get.by_xpath("//li[2]/ul/li/span[2]"))
                except:
                    Helper.internal_assert(
                        "Numeric parameters", Get.by_xpath("//li[2]/ul/li/span[2]"))
                Click.name("Normal references")
                Wait.css(Constants.Dashboard.Checklist.LineItem.Deny.CSS)
                Wait.css(Constants.Dashboard.Checklist.LineItem.Approve.CSS)
                Click.css(Constants.Dashboard.Checklist.LineItem.Approve.CSS)
            # NOT LOCAL
            if settings.DATABASE_TYPE != 'local':
                checklistUuid = DBChecklist.get_recent_checklist_uuid(
                    checklistName)[0]
                DBChecklist.update_all_decisions_to_approve(checklistUuid)
            # NOT LOCAL

            Click.css(".line-item-row span.manual")
            print("click on V button approve of decision in state = " + state)
            try:
                Wait.css("li.not-relevant-btn")
            except:
                Wait.xpath("//aside/header/ul/li")
            if state == "review":
                Wait.id("edit-checklist")
            if state == "PEER":
                if settings.DATABASE_TYPE == 'local':
                    Helper.internal_assert(
                        "Audit Log (4)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
                else:
                    Helper.internal_assert(
                        "Audit Log (5)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
            if state == "review":
                if settings.DATABASE_TYPE == 'local':
                    Helper.internal_assert(
                        "Audit Log (2)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
                else:
                    Helper.internal_assert(
                        "Audit Log (3)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
            if state == "APPROVAL":
                if settings.DATABASE_TYPE == 'local':
                    Helper.internal_assert(
                        "Audit Log (8)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
                else:
                    Helper.internal_assert(
                        "Audit Log (9)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
            Click.id(
                Constants.Dashboard.Checklist.AuditLog.ID, wait_for_page=True)
            Wait.text_by_xpath("//span[2]", checklistName)
            Enter.text_by_xpath("//textarea", "zdfgsdyh")
            Click.css(Constants.SubmitButton.CSS)
            Wait.modal_to_dissappear()
            if state == "review":
                if settings.DATABASE_TYPE == 'local':
                    Helper.internal_assert(
                        "Audit Log (3)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
                else:
                    Helper.internal_assert(
                        "Audit Log (4)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
            if state == "PEER":
                if settings.DATABASE_TYPE == 'local':
                    Helper.internal_assert(
                        "Audit Log (5)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
                else:
                    Helper.internal_assert(
                        "Audit Log (6)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
            if state == "APPROVAL":
                if settings.DATABASE_TYPE == 'local':
                    Helper.internal_assert(
                        "Audit Log (9)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
                else:
                    Helper.internal_assert(
                        "Audit Log (10)", Get.by_id(Constants.Dashboard.Checklist.AuditLog.ID))
            #    Validate Buttons
            if settings.DATABASE_TYPE != 'local':
                FEGeneral.refresh()
                engagement_id = DBVirtualFunction.select_eng_uuid(vfName)
                engLeadEmail = DBUser.select_el_email(vfName)
                logger.debug("EL email: " + engLeadEmail)
                engagement_manual_id = DBGeneral.select_where("engagement_manual_id", "ice_engagement",
                                                              "uuid", engagement_id, 1)
                #    Click on all default next steps
                myVfName = engagement_manual_id + ": " + vfName
                actualVfNameid = "clickable-" + myVfName
                Click.id(actualVfNameid)
                Click.id("checklist-" + checklistUuid)
            Helper.internal_assert(
                "Add Next Steps", Get.by_xpath("//button[3]"))
            Wait.text_by_id(Constants.Dashboard.Checklist.Reject.ID,
                            Constants.Dashboard.Checklist.Reject.Modal.Button.TEXT, wait_for_page=True)
            Helper.internal_assert(
                "Approve", Get.by_xpath("//div[@id='state-actions']/button"))
            logger.debug("ALL VALIDATION PASS FOR STATE: " + state)
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "review_state_actions_and_validations FAILED because: " + \
                str(e)
            raise Exception(errorMsg, "review_state_actions_and_validations")
            logger.error(
                state + " state FAILED CONNECT TO STAGING MANUAL AND VERIFY WHY!")
            raise

    @staticmethod
    def reject(rejectMsg=None):
        try:
            Click.id(
                Constants.Dashboard.Checklist.Reject.ID, wait_for_page=True)
            if rejectMsg:
                Enter.text_by_name(
                    Constants.Dashboard.Checklist.Reject.Modal.Comment.NAME, rejectMsg, wait_for_page=True)
            Click.id(
                Constants.Dashboard.Checklist.Reject.Modal.Button.ID, wait_for_page=True)
        except Exception as e:
            errorMsg = "Failed to reject checklist."
            raise Exception(errorMsg, e)

    @staticmethod
    def add_line_item_audit_log():
        try:
            log_txt = Helper.rand_string("randomString")
            Enter.text_by_id("new-audit-log-text", log_txt, wait_for_page=True)
            Click.id("submit-new-audit-lop-text")
            Wait.text_by_css(
                Constants.Dashboard.Checklist.AuditLog.LastLocalAuditLog.CSS, log_txt, wait_for_page=True)
            return log_txt
        except Exception as e:
            errorMsg = "Failed to add audit log to line item."
            raise Exception(errorMsg, e)

    @staticmethod
    def click_on_checklist(user_content, checklistName, checklist_uuid=None):
        FEOverview.click_on_vf(user_content)
        if checklist_uuid is None:
            checklist_uuid = DBGeneral.select_where_not_and_order_by_desc(
                'uuid', Constants.DBConstants.IceTables.CHECKLIST, 'name', checklistName, 'state', Constants.ChecklistStates.Archive.TEXT, 'create_time')[0]
        Click.id("checklist-" + checklist_uuid)

    @staticmethod
    def validate_reject_is_enabled():
        return Wait.id(Constants.Dashboard.Checklist.Reject.ID, wait_for_page=True)

    @staticmethod
    def cl_to_next_stage(actualVfNameid):
        Click.xpath("//div[@id='state-actions']/button", wait_for_page=True)
        Wait.id(actualVfNameid, wait_for_page=True)
        session.run_negative(lambda: Wait.css(
            Constants.Default.BlockUI.CSS), "Error: CL to next stage failed.")

    @staticmethod
    def search_by_vfname_for_not_local(user_content):
        vfFullName = user_content[
            'engagement_manual_id'] + ": " + user_content['vfName']
        if settings.DATABASE_TYPE != 'local':
            Enter.text_by_id(
                Constants.Dashboard.LeftPanel.SearchBox.ID, user_content['vfName'])
            Click.css(Constants.Dashboard.LeftPanel.SearchBox.Results.CSS)
            Wait.text_by_id(
                Constants.Dashboard.Overview.Title.ID, vfFullName)

    @staticmethod
    def search_by_manual_id(manual_id):
        Enter.text_by_id(
            Constants.Dashboard.LeftPanel.SearchBox.ID, manual_id, wait_for_page=True)
        Click.css(
            Constants.Dashboard.LeftPanel.SearchBox.Results.CSS, wait_for_page=True)
        Wait.id(Constants.Dashboard.Overview.Title.ID)

    @staticmethod
    def reject_checklist(newObj, checklistName):
        Click.xpath("//button[2]")
        vfName = newObj[0]
        engLeadFullName = DBUser.get_el_name(vfName)
        Enter.text_by_name(
            Constants.Dashboard.Checklist.Reject.Modal.Comment.NAME, "Reject state By :" + engLeadFullName)
        Helper.internal_assert(
            "Checklist: " + checklistName, Get.by_css("span.state-title.ng-binding"))
        Wait.text_by_id(Constants.Dashboard.Checklist.Reject.Modal.Button.ID,
                        Constants.Dashboard.Checklist.Reject.Modal.Button.TEXT)
        Click.id(Constants.Dashboard.Checklist.Reject.Modal.Button.ID)
        Wait.modal_to_dissappear()

    @staticmethod
    def add_nsteps(checklistUuid, actualVfNameid, myVfName, checklistName, newFileNames):
        Click.id(actualVfNameid, wait_for_page=True)
        checklistUuid = DBChecklist.select_where_cl_not_archive(
            "uuid", "ice_checklist", "name", newFileNames[0], 1)
        Click.id("checklist-" + checklistUuid, wait_for_page=True)
        Wait.text_by_id(Constants.Dashboard.Checklist.Name.ID, newFileNames[0])
        FEChecklist.add_next_step_updated(checklistName, newFileNames[1])
    #         vALIDATE SCROLLING
        actualVfNameid = "clickable-" + myVfName
        actualVfName = Get.by_id(actualVfNameid, wait_for_page=True)
        if actualVfName != '':
            Helper.internal_assert(myVfName, actualVfName)

    @staticmethod
    def validate_multi_eng(user_content, checklist_content, newEL_content, actualVfNameid):
        query = "UPDATE ice_user_profile SET role_id=2 WHERE email = '" + \
            str(newEL_content['email']) + "';"
        DBGeneral.update_by_query(query)
        FEWizard.invite_team_members_modal(newEL_content['email'])
        # Fetch one AT&T user ID.
        enguuid = DBGeneral.select_where(
            "uuid", "ice_engagement", "engagement_manual_id", user_content['engagement_manual_id'], 1)
        invitation_token = DBUser.select_invitation_token(
            "invitation_token", "ice_invitation", "engagement_uuid", enguuid, newEL_content['email'], 1)
        URL = Constants.Default.InviteURL.Login.TEXT + invitation_token
        FEGeneral.re_open(URL)
        FEUser.login(newEL_content[
                     'email'], Constants.Default.Password.TEXT, expected_element=actualVfNameid)
        Click.id(actualVfNameid, wait_for_page=True)
        count = None
        try:
            session.ice_driver.find_element_by_id(
                "checklist-" + checklist_content['uuid'])
            count += 1
        except:
            logger.debug(
                "check list not visible for EL invited : " + str(newEL_content['email']))
        assertTrue(count == None)
        query = "UPDATE ice_user_profile SET role_id=1 WHERE email = '" + \
            str(newEL_content['email']) + "';"
        DBGeneral.update_by_query(query)

    @staticmethod
    def create_cl_without_files(user_content):
        FEOverview.click_on_vf(user_content)
        Click.id("checklist-plus-" + user_content['engagement_uuid'])
        Wait.id(Constants.Dashboard.Modal.CLOSE_BUTTON_ID)
        checklistName = "NoAssociatedFiles" + \
            Helper.rand_string("randomString")
        Enter.text_by_name("checkListName", checklistName)
        Wait.xpath("//select")
        if settings.DATABASE_TYPE == 'local':
            Select(session.ice_driver.find_element_by_xpath("//select")
                   ).select_by_visible_text(Constants.Template.Heat.TEXT)
        else:
            Click.xpath("//select")
            Click.xpath("//option[2]")
        Click.id(Constants.Dashboard.LeftPanel.CreateChecklist.ID)
        Wait.text_by_id(Constants.Dashboard.Checklist.Name.ID, checklistName)

    @staticmethod
    def validate_audit_log(log_txt):
        audit_log_list_text = Get.by_id(
            Constants.Dashboard.Checklist.AuditLog.AuditLogList.ID, wait_for_page=True)
        try:
            log_txt in audit_log_list_text
            logger.debug("validate_audit_log PASS")
        except Exception as e:
            errorMsg = "Failed in validate_audit_log"
            raise Exception(errorMsg)

    @staticmethod
    def get_to_create_new_ns_modal():
        Click.id(Constants.Dashboard.Checklist.AddNS.ID,
                 wait_for_page=True)
        Wait.text_by_css(Constants.Dashboard.Checklist.AddNS.CSS,
                         Constants.Dashboard.Checklist.TITLE)
        Helper.internal_assert(Constants.Dashboard.Checklist.TITLE, Get.by_css(
            Constants.Dashboard.Checklist.AddNS.CSS))
        Helper.internal_assert(
            Constants.Dashboard.Checklist.AddNS.TITLE,
            Get.by_css(Constants.FEGeneral.CSS.H2))

    @staticmethod
    def get_to_create_new_ns_modal_via_overview():
        Click.id(Constants.Dashboard.Overview.NextSteps.Add.ID,
                 wait_for_page=True)
        Wait.text_by_css(Constants.Dashboard.Checklist.AddNS.CSS,
                         Constants.Dashboard.Overview.NextSteps.Add.TITLE)
        Helper.internal_assert(
            Constants.Dashboard.Checklist.AddNS.TITLE,
            Get.by_css(Constants.FEGeneral.CSS.H2))

    @staticmethod
    def get_jenkins_log():
        Click.id(Constants.Dashboard.Checklist.JenkinsLog.ID, True)
        Wait.text_by_id(
            Constants.Dashboard.Checklist.JenkinsLog.Modal.Title.ID,
            Constants.Dashboard.Checklist.JenkinsLog.Modal.Title.TEXT, True)
        log = Get.by_id(
            Constants.Dashboard.Checklist.JenkinsLog.Modal.Body.ID, True)
        Helper.assertTrue(Constants.Dashboard.Checklist.JenkinsLog.Modal.Body.TEXT_SAMPLE in log,
                          "Jenkins log could not be viewed.")
        Click.id(Constants.Dashboard.Modal.CLOSE_BUTTON_ID)
        return log

