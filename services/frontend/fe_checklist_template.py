 
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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from services.api.api_virtual_function import APIVirtualFunction
from services.constants import Constants
from services.database.db_checklist import DBChecklist
from services.database.db_user import DBUser
from services.frontend.base_actions.click import Click
from services.frontend.base_actions.enter import Enter
from services.frontend.base_actions.get import Get
from services.frontend.base_actions.wait import Wait
from services.frontend.fe_checklist import FEChecklist
from services.frontend.fe_general import FEGeneral
from services.frontend.fe_overview import FEOverview
from services.frontend.fe_user import FEUser
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()

class FEChecklistTemplate:

    @staticmethod
    def basic_admin_navigation():
        FEUser.login(
            Constants.Users.Admin.EMAIL, Constants.Default.Password.TEXT)
        FEUser.go_to_admin()

    @staticmethod
    def click_on_template_name_on_navigation(template_name, text):
        Wait.text_by_name(template_name, text, wait_for_page=True)
        Click.name(template_name, wait_for_page=True)

    @staticmethod
    def click_on_save_and_assert_success_msg():
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.SAVE_BTN_ID, wait_for_page=True)
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.APPROVE_BTN_ID, wait_for_page=True)
        Wait.text_by_id(Constants.Dashboard.LeftPanel.EditChecklistTemplate.SUCCESS_ID,
                        Constants.Dashboard.LeftPanel.EditChecklistTemplate.SUCCESS_SAVE_MSG)

    @staticmethod
    def click_on_disabled_save_and_assert_for_promp_msg():
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.SAVE_BTN_ID)
        session.run_negative(lambda: Click.id(Constants.Dashboard.LeftPanel.EditChecklistTemplate.APPROVE_BTN_ID),
                             "Ooops modal window is opened although 'Save' button should have been disabled")

    @staticmethod
    def save_with_no_changes():
        Wait.text_by_id(Constants.Dashboard.LeftPanel.EditChecklistTemplate.SAVE_BTN_ID,
                        Constants.Dashboard.LeftPanel.EditChecklistTemplate.SAVE_BTN)
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.SAVE_BTN_ID, wait_for_page=True)
        Wait.text_by_name(Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT,
                          Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT)
        Wait.text_by_id(Constants.Dashboard.LeftPanel.EditChecklistTemplate.APPROVE_BTN_TITLE_ID,
                        Constants.Dashboard.LeftPanel.EditChecklistTemplate.APPROVE_BTN_TITLE_TEXT)
        Wait.text_by_id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.APPROVE_BTN_ID, "Yes")
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.APPROVE_BTN_ID, wait_for_page=True)
        Wait.text_by_id(Constants.Dashboard.LeftPanel.EditChecklistTemplate.SUCCESS_ID,
                        Constants.Dashboard.LeftPanel.EditChecklistTemplate.CL_TEMPLATE_SAVED_TXT)

    @staticmethod
    def discard_checklist_after_modification():
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.FIRST_SECTION_ID, wait_for_page=True)
        Enter.text_by_id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.FIRST_SECTION_INPUT_ID, "ttttttt", wait_for_page=True)
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.FIRST_SECTION_ID)
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.REJECT_BTN_ID)
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.APPROVE_BTN_ID, wait_for_page=True)
        Wait.text_by_id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.SUCCESS_ID, "All changes discarded.")

    @staticmethod
    def edit_template_and_save():
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.FIRST_SECTION_ID)
        Enter.text_by_id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.FIRST_SECTION_INPUT_ID, "Ros Is My Mentor")
        FEChecklistTemplate.click_on_save_and_assert_success_msg()

    @staticmethod
    def del_lineitem_and_save():
        Click.id(Constants.Dashboard.LeftPanel.EditChecklistTemplate.FIRST_SECTION_ID, wait_for_page=True)
        Enter.text_by_id(Constants.Dashboard.LeftPanel.EditChecklistTemplate.FIRST_SECTION_INPUT_ID,
                         "Ros Is My Mentor", wait_for_page=True)
        Click.id(Constants.Dashboard.LeftPanel.EditChecklistTemplate.FIRST_SECTION_ID)
        FEChecklistTemplate.click_on_save_and_assert_success_msg()

    @staticmethod
    def add_lineitem_and_save():
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.ADD_LINE_ITEM_BTN, wait_for_page=True)
        Click.xpath("//li[@id='select-lineitem-btn-0.1']/span[2]")
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.EDIT_LINE_ITEM_BTN)
        Enter.text_by_id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.EDIT_LINE_ITEM_NAME, "xxx")
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.EDIT_LINE_ITEM_BTN, wait_for_page=True)
        FEChecklistTemplate.click_on_save_and_assert_success_msg()

    @staticmethod
    def edit_description_lineitem_and_save():
        isBold = False
        desc = Helper.rand_string("randomString")
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.FIRST_LINE_ITEM_ID)
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.EDIT_LINE_ITEM_BTN)
        Enter.text_by_id(Constants.Dashboard.LeftPanel.EditChecklistTemplate.EDIT_LINE_ITEM_NAME,
                         Helper.rand_string("randomString"))
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.EDIT_LINE_ITEM_DESC)
        editor_element = Get.wysiwyg_element_by_id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.LINE_ITEM_DESC_TEXT_BOX)
        editor_element.clear()
        editor_element.send_keys(desc)
        Wait.page_has_loaded()
        actionChains = ActionChains(session.ice_driver)
        actionChains.double_click(editor_element).perform()
        Wait.page_has_loaded()
        Click.xpath(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.WYSIWYG_BUTTON_BOLD)
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.EDIT_LINE_ITEM_BTN, wait_for_page=True)
        isBold = Wait.is_css_exists("b")
        while not isBold:
            Click.id(
                Constants.Dashboard.LeftPanel.EditChecklistTemplate.EDIT_LINE_ITEM_BTN, wait_for_page=True)
            actionChains.double_click(editor_element).perform()
            Click.xpath(
                Constants.Dashboard.LeftPanel.EditChecklistTemplate.WYSIWYG_BUTTON_BOLD, wait_for_page=True)
            Click.id(
                Constants.Dashboard.LeftPanel.EditChecklistTemplate.EDIT_LINE_ITEM_BTN, wait_for_page=True)
            isBold = Wait.is_css_exists("b")
        if isBold:
            FEChecklistTemplate.click_on_save_and_assert_success_msg()
        FEGeneral.refresh()
        Click.name(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT, wait_for_page=True)
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.FIRST_LINE_ITEM_ID, wait_for_page=True)
        Wait.css("b")
        Wait.text_by_css("b", desc, wait_for_page=True)

    @staticmethod
    def rollback_add_lineitem_and_save():
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.DELETE_LINE_ITEM)
        FEChecklistTemplate.click_on_save_and_assert_success_msg()
        FEChecklistTemplate.rollback_to_heat_teampleate()

    @staticmethod
    def add_lineitem_and_check_db():
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.FIRST_SECTION_ID)
        Enter.text_by_id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.FIRST_SECTION_INPUT_ID, "Ros Is My Mentor")
        FEChecklistTemplate.click_on_save_and_assert_success_msg()
        result = DBChecklist.checkChecklistIsUpdated()
        Helper.internal_not_equal(result, None)

    @staticmethod
    def check_cl_after_lineitem_added():
        template_name = Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT
        user_content = APIVirtualFunction.create_engagement()
        FEUser.login(
            Constants.Users.Admin.EMAIL, Constants.Default.Password.TEXT)
        vfName = user_content['vfName']
        engagement_id = DBChecklist.fetchEngByVfName(vfName)
        engLeadEmail = DBUser.select_el_email(vfName)
        engagement_manual_id = DBChecklist.fetchEngManIdByEngUuid(
            engagement_id)
        myVfName = engagement_manual_id + ": " + vfName
        FEOverview.click_on_vf(user_content)
        FEGeneral.re_open(Constants.Default.LoginURL.TEXT)
        FEUser.login(
            engLeadEmail, Constants.Default.Password.TEXT, engagement_manual_id)
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.DASHBOARD_ID)
        Enter.text_by_id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.SEARCH_ENG_ID, vfName)
        Click.id("test_" + vfName)
        checklistName = FEChecklist.create_checklist(
            engagement_id, vfName, None, engagement_manual_id)
        FEUser.go_to_admin()
        result = DBChecklist.fetchChecklistByName(checklistName)
        FEUser.go_to_admin()
        FEChecklistTemplate.click_on_template_name_on_navigation(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT, template_name)
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.EDIT_LINE_ITEM_BTN)
        Enter.text_by_id(Constants.Dashboard.LeftPanel.EditChecklistTemplate.EDIT_LINE_ITEM_NAME,
                         "test_lineitem_added_and_audit_log_on_dupl_cl-NAME")
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.EDIT_LINE_ITEM_BTN)
        FEChecklistTemplate.click_on_save_and_assert_success_msg()
        Click.id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.DASHBOARD_ID)
        Enter.text_by_id(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.SEARCH_ENG_ID, vfName)
        Click.id("test_" + vfName)
        Click.id("checklist-" + str(result))
        Helper.internal_assert(
            "1. automation", session.ice_driver.find_element_by_xpath("//li[@id='']").text)
