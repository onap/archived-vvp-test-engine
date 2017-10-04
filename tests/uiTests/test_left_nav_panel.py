 
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

from iceci.decorator.exception_decor import exception
from services.constants import Constants
from services.frontend.base_actions.click import Click
from services.frontend.base_actions.enter import Enter
from services.frontend.base_actions.get import Get
from services.frontend.base_actions.wait import Wait
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.session import session
from services.types import API, Frontend, DB
from tests.uiTests.test_ui_base import TestUiBase


logger = LoggingServiceFactory.get_logger()


class TestLeftNavPanel(TestUiBase):
    user_content = None

    @classmethod
    def setUpClass(cls):
        super(TestLeftNavPanel, cls).setUpClass()
        cls.user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        cls.eng_title = "%s: %s" % (
            cls.user_content['engagement_manual_id'], cls.user_content['vfName'])
        cls.left_panel_eng_id = "clickable-%s" % (cls.eng_title)

    def setUp(self):
        super(TestLeftNavPanel, self).setUp()
        Frontend.User.login(
            self.user_content['el_email'], Constants.Default.Password.TEXT)

    @exception()
    def test_starred_recent_searchbar(self):
        actualVfName = Get.by_id(self.left_panel_eng_id)
        Helper.internal_assert(self.eng_title, actualVfName)
        Click.id(self.left_panel_eng_id)
        Wait.id("title-id-" + self.eng_title)
        Helper.internal_assert(
            self.user_content['engagement_manual_id'] + ":", Get.by_id("title-id-" + self.eng_title))
        Click.id(Constants.Dashboard.Overview.Star.ID, wait_for_page=True)
        Wait.id("title-id-" + self.eng_title)
        Click.id(Constants.Dashboard.Overview.Star.ID, wait_for_page=True)
        Wait.id("title-id-" + self.eng_title, wait_for_page=True)
        Helper.internal_assert(
            self.eng_title, Get.by_id(self.left_panel_eng_id))
        Enter.text_by_xpath(
            "//input[@type='text']", self.user_content['engagement_manual_id'], wait_for_page=True)
        Wait.text_by_css(
            Constants.Dashboard.LeftPanel.SearchBox.Results.CSS, self.eng_title)
        Click.css(
            Constants.Dashboard.LeftPanel.SearchBox.Results.CSS, wait_for_page=True)

    @exception()
    def test_search_bar(self):
        """ Create user and VF, log in, add VFC, search by EID, VF and VFC """
        vfFullName = self.user_content[
            'engagement_manual_id'] + ": " + self.user_content['vfName']
        try:
            Enter.text_by_id(
                Constants.Dashboard.LeftPanel.SearchBox.ID, self.user_content['vfName'])
            Wait.css(Constants.Dashboard.LeftPanel.SearchBox.Results.CSS)
            Click.css(Constants.Dashboard.LeftPanel.SearchBox.Results.CSS)
            Wait.text_by_id(
                Constants.Dashboard.Overview.Title.ID, vfFullName)
        except:
            errorMsg = "Failed to search by VF name."
            raise Exception(errorMsg)

        try:
            Enter.text_by_id(Constants.Dashboard.LeftPanel.SearchBox.ID, self.user_content[
                             'engagement_manual_id'])
            Enter.text_by_id(Constants.Dashboard.LeftPanel.SearchBox.ID, self.user_content[
                             'engagement_manual_id'])
            Wait.css(Constants.Dashboard.LeftPanel.SearchBox.Results.CSS)
            Click.css(Constants.Dashboard.LeftPanel.SearchBox.Results.CSS)
            Wait.text_by_id(
                Constants.Dashboard.Overview.Title.ID, vfFullName)
        except:
            errorMsg = "Failed to search by Engagement Manual ID."
            raise Exception(errorMsg)
        Frontend.Overview.click_on_vf(self.user_content)
        detailedViewID = Constants.Dashboard.DetailedView.ID + vfFullName
        Wait.text_by_id(detailedViewID, "Detailed View", wait_for_page=True)
        Click.id(detailedViewID, wait_for_page=True)
        Click.id(
            Constants.Dashboard.DetailedView.VFC.Add.ID, wait_for_page=True)
        vfcName = Helper.rand_string("randomString")
        extRefID = Helper.rand_string("randomNumber")
        Enter.text_by_name("name", vfcName)
        Enter.text_by_name("extRefID", extRefID, wait_for_page=True)
        Select(session.ice_driver.find_element_by_id(Constants.Dashboard.DetailedView.VFC.Choose_Company.ID)).select_by_visible_text(
            self.user_content['vendor'])
        Click.id(
            Constants.Dashboard.DetailedView.VFC.Save_button.ID, wait_for_page=True)
        try:
            Enter.text_by_id(
                Constants.Dashboard.LeftPanel.SearchBox.ID, vfcName, wait_for_page=True)
            Click.id(
                "search-" + self.user_content['vfName'], wait_for_page=True)
            Wait.id("clickable-" + vfFullName, wait_for_page=True)
        except Exception as e:
            errorMsg = "Failed to search by VFC name."
            raise Exception(errorMsg + str(e))

    @exception()
    def test_recent_bar_by_last_updated(self):
        countIdsActive = 0
        myVfName = self.user_content[
            'engagement_manual_id'] + ": " + self.user_content['vfName']
        actualVfNameid = "clickable-" + myVfName
        actualVfName = Get.by_id(actualVfNameid)
        Helper.internal_assert(myVfName, actualVfName)
        Click.id(actualVfNameid)
        uuid = DB.General.select_where_email(
            "uuid", "ice_user_profile", self.user_content['el_email'])
        ids2 = DB.User.select_recent_vf_of_user(uuid, 0)
        part_of_id_to_find = "clickable-"
        ids1 = session.ice_driver.find_elements_by_css_selector(
            '[id*="%s"]' % part_of_id_to_find)
        for ii in ids1:
            if "clickable-" in ii.get_attribute('id'):
                logger.debug("Fetched ID: " + ii.get_attribute('id'))
                vf_name = ii.get_attribute('id').split(" ")[1]
                vf_uuid = DB.General.select_where(
                    "uuid", "ice_vf", "name", vf_name, 1)
                if vf_uuid in ids2:
                    countIdsActive += 1
        if(countIdsActive == len(ids2.split())):
            logger.debug("Right result")

    @exception()
    def test_entering_engagement_from_dashboard(self):
        Wait.text_by_id(self.left_panel_eng_id, self.eng_title)
        DB.VirtualFunction.remove_engagement_from_recent(
            self.user_content['vf_uuid'])
        Frontend.General.refresh()
        Wait.id_to_dissappear(self.left_panel_eng_id)
        Frontend.Dashboard.statuses_search_vf(
            self.user_content['engagement_manual_id'], self.user_content['vfName'])
        Wait.text_by_id(self.left_panel_eng_id, self.eng_title)

    @exception()
    def test_search_by_email(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        Frontend.User.relogin(
            user_content['email'], Constants.Default.Password.TEXT)
        Frontend.Dashboard.search_in_left_searchbox_by_param(
            user_content['engagement_manual_id'], user_content['vfName'], user_content['email'])

    @exception()
    def test_search_by_username(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        Frontend.User.relogin(
            user_content['email'], Constants.Default.Password.TEXT)
        Frontend.Dashboard.search_in_left_searchbox_by_param(
            user_content['engagement_manual_id'], user_content['vfName'], user_content['full_name'])
