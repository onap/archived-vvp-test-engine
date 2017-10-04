 
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
from selenium.webdriver.support.ui import Select

from services.constants import Constants
from services.database.db_user import DBUser
from services.frontend.base_actions.click import Click
from services.frontend.base_actions.enter import Enter
from services.frontend.base_actions.get import Get
from services.frontend.base_actions.wait import Wait
from services.frontend.fe_general import FEGeneral
from services.frontend.fe_overview import FEOverview
from services.frontend.fe_user import FEUser
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()


class FEDashboard:

    @staticmethod
    def open_announcement():
        try:
            Click.id("read-more-button")
        except Exception as e:
            errorMsg = "Failed to go to Announcement page."
            raise Exception(errorMsg, e)

    @staticmethod
    def open_documentation(title):
        try:
            Click.id("documentation", wait_for_page=True)
            Wait.id("search-doc")
            Wait.text_by_id(title, title, wait_for_page=True)
        except Exception as e:
            errorMsg = "Failed to go to Announcement page."
            raise Exception(errorMsg, e)

    @staticmethod
    def validate_filtering_by_stage(user_content, stage):
        FEGeneral.re_open(Constants.Default.LoginURL.TEXT)
        # Validate Scrolling    #
        FEUser.login(user_content['el_email'], Constants.Default.Password.TEXT)
        FEOverview.click_on_vf(user_content)
        Click.id(Constants.Dashboard.Statuses.ID, wait_for_page=True)
        Wait.text_by_id("dashboard-title", "Statuses", wait_for_page=True)
        Wait.id("search-filter-stage")
        Select(session.ice_driver.find_element_by_id(
            "search-filter-stage")).select_by_visible_text(stage)
        Wait.id(
            Constants.Dashboard.Statuses.ExportExcel.ID, wait_for_page=True)
        engLeadID = DBUser.select_user_native_id(user_content['el_email'])
        # Query for fetching count of rows per stage.
        countOfEngInStagePerUser = DBUser.select_user_engagements_by_stage(
            stage, engLeadID)
    #    Calculate number of pages    #
        NUM_OF_RESULTS_PER_PAGES = 8
        number_of_pages = countOfEngInStagePerUser // NUM_OF_RESULTS_PER_PAGES
        logger.debug("Number of pages: " + str(number_of_pages))
        if (countOfEngInStagePerUser % NUM_OF_RESULTS_PER_PAGES != 0):
            number_of_pages += 1
        logger.debug("number_of_pages " + str(number_of_pages))  # Scroll    #
        Wait.id("engagements-pagination", wait_for_page=True)
        element = session.ice_driver.find_element_by_id(
            "engagements-pagination")
        element.location_once_scrolled_into_view
        Click.link_text(str(number_of_pages), wait_for_page=True)

    @staticmethod
    def validate_filtering_by_stage_with_page_ids(user_content, stage):
        FEOverview.click_on_vf(user_content)
        Click.id(Constants.Dashboard.Statuses.ID)
        # Stage Active Validation    #
        Wait.text_by_id("dashboard-title", "Statuses")
        Wait.id(Constants.Dashboard.Statuses.FilterDropdown.ID)
        Select(session.ice_driver.find_element_by_id(
            Constants.Dashboard.Statuses.FilterDropdown.ID)).select_by_visible_text("Intake")
        Wait.page_has_loaded()
        Select(session.ice_driver.find_element_by_id(
            Constants.Dashboard.Statuses.FilterDropdown.ID)).select_by_visible_text(stage)
        Wait.id(
            Constants.Dashboard.Statuses.ExportExcel.ID, wait_for_page=True)
        countIdsActive = 0
        engLeadID = DBUser.select_user_native_id(user_content['el_email'])
        countOfEngInStagePerUser = DBUser.select_user_engagements_by_stage(
            stage, engLeadID)  # Calculate number of pages    #
        NUM_OF_RESULTS_PER_PAGES = 8
        number_of_pages = countOfEngInStagePerUser // NUM_OF_RESULTS_PER_PAGES
        if countOfEngInStagePerUser <= NUM_OF_RESULTS_PER_PAGES:
            number_of_pages = 1
        if number_of_pages == 1:
            # Count all engagements on current page
            logger.debug("Number of pages: " + str(number_of_pages))
            ids = session.ice_driver.find_elements_by_xpath('//*[@id]')
            for ii in ids:
                if "starred-" in ii.get_attribute('id'):
                    # Print ii.tag_name (id name as string).
                    logger.debug(ii.get_attribute('id'))
                    countIdsActive += 1
        Wait.id(Constants.Dashboard.Statuses.ExportExcel.ID)
        if countIdsActive == countOfEngInStagePerUser:
            logger.debug("result right")
        else:
            if countOfEngInStagePerUser % NUM_OF_RESULTS_PER_PAGES != 0:
                number_of_pages += 1
            logger.debug("number_of_pages " + str(number_of_pages))
            #    Scroll    #
            Wait.id("engagements-pagination")
            element = session.ice_driver.find_element_by_id(
                "engagements-pagination")
            element.location_once_scrolled_into_view
            if number_of_pages > 1:
                Click.link_text(str(number_of_pages), wait_for_page=True)

    @staticmethod
    def validate_statistics_by_stages(user_content):
        #    Validate Scrolling    #
        FEOverview.click_on_vf(user_content)
        Click.id(Constants.Dashboard.Statuses.ID)
        Wait.text_by_id("dashboard-title", "Statuses")
        Wait.css(Constants.Dashboard.Statuses.Statistics.FilterDropdown.CSS)
        Select(session.ice_driver.find_element_by_css_selector(
            Constants.Dashboard.Statuses.Statistics.FilterDropdown.CSS)).select_by_visible_text("All")
        engLeadID = DBUser.select_user_native_id(user_content['el_email'])
        countOfEngInStagePerUser = DBUser.select_all_user_engagements(
            engLeadID)  # Scroll    #
        Wait.text_by_id(
            Constants.Dashboard.Statuses.Statistics.EngagementsNumber.ID,
            str(countOfEngInStagePerUser), wait_for_page=True)
        element = session.ice_driver.find_element_by_id(
            Constants.Dashboard.Statuses.Statistics.EngagementsNumber.ID)
        # Stage Active Validation    #
        element.location_once_scrolled_into_view
        Wait.css(
            Constants.Dashboard.Statuses.Statistics.FilterDropdown.CSS, wait_for_page=True)
        Select(session.ice_driver.find_element_by_css_selector(
            Constants.Dashboard.Statuses.Statistics.FilterDropdown.CSS)).select_by_visible_text("Active")
        countOfEngInStagePerUser = DBUser.select_user_engagements_by_stage(
            "Active", engLeadID)
        Wait.text_by_id(
            Constants.Dashboard.Statuses.Statistics.EngagementsNumber.ID, str(countOfEngInStagePerUser), wait_for_page=True)

    @staticmethod
    def search_by_vf(user_content):
        engName = user_content[
            'engagement_manual_id'] + ": " + user_content['vfName']
        engSearchID = "eng-" + engName
        FEGeneral.re_open_not_clean_cache(Constants.Default.DashbaordURL.TEXT)
        logger.debug("Search engagement by engagement_manual_id")
        Enter.text_by_id(Constants.Dashboard.Statuses.SearchBox.ID,
                         user_content['engagement_manual_id'], wait_for_page=True)
        eng_manual_id = user_content['engagement_manual_id'] + ":"
        Wait.text_by_id(engSearchID, eng_manual_id)

    @staticmethod
    def search_in_left_searchbox_by_param(manual_id, vf_name, param):
        myVfName = manual_id + ": " + vf_name
        Enter.text_by_xpath(
            Constants.Dashboard.LeftPanel.SearchBox.Results.XPATH, param)
        Wait.text_by_css(
            Constants.Dashboard.LeftPanel.SearchBox.Results.CSS, myVfName)
        Click.css(Constants.Dashboard.LeftPanel.SearchBox.Results.CSS)

    @staticmethod
    def check_vnf_version(user_content):
        current_vnf_value = Get.by_css(
            "#progress_bar_" + user_content['engagement_manual_id'] + " ." + Constants.Dashboard.Overview.Progress.VnfVersion.CLASS, wait_for_page=True)
        Helper.internal_assert(current_vnf_value, user_content['vnf_version'])

    @staticmethod
    def search_in_dashboard(user_content, vfcName, users):
        engName = user_content[
            'engagement_manual_id'] + ": " + user_content['vfName']
        engSearchID = "eng-" + engName
        for user in users:
            FEGeneral.re_open(Constants.Default.LoginURL.TEXT)
            logger.debug("Login with user " + user)
            FEUser.login(user, Constants.Default.Password.TEXT)
            logger.debug("Search engagement by engagement_manual_id")
            Enter.text_by_id(
                Constants.Dashboard.Statuses.SearchBox.ID, user_content['engagement_manual_id'])
            eng_manual_id = user_content['engagement_manual_id'] + ":"
            Wait.text_by_id(engSearchID, eng_manual_id)
            logger.debug("Engagement found (searched by engagement_manual_id)")
            FEGeneral.refresh()
            logger.debug("Search engagement by VF name")
            # Search by VF name.
            Enter.text_by_id(
                Constants.Dashboard.Statuses.SearchBox.ID, user_content['vfName'])
            Wait.text_by_id(engSearchID, eng_manual_id)
            logger.debug("Engagement found (searched by VF name)")
            FEGeneral.refresh()
            logger.debug("Search engagement by VFC")
            # Search by VFC.
            Enter.text_by_id(
                Constants.Dashboard.Statuses.SearchBox.ID, vfcName)
            Wait.text_by_id(engSearchID, eng_manual_id)
            logger.debug("Engagement found (searched by VFC)")
            FEGeneral.refresh()
            logger.debug("Negative search: search by random string")
            # Search by VFC.
            Enter.text_by_id(Constants.Dashboard.Statuses.SearchBox.ID,
                             "RND_STR_" + Helper.rand_string("randomString"))
            Wait.text_by_id("search-results", "Export to Excel >>")

    @staticmethod
    def check_if_the_eng_of_NS_is_the_correct_one(user_content):
        logger.debug("    > Check if the engagement of NS is the correct one")
        engName = user_content[
            'engagement_manual_id'] + ": " + user_content['vfName']
        Wait.text_by_name(
            user_content['engagement_manual_id'], "Engagement - " + engName)
        return engName

    @staticmethod
    def check_if_creator_of_NS_is_the_EL(user_content):
        logger.debug(
            "    > Check if creator of NS is the EL " + user_content['el_name'])
        if (user_content['el_name'] not in Get.by_name("creator-full-name-" + user_content['el_name'])):
            logger.error("EL is not the creator of the NS according to UI.")
            raise

    @staticmethod
    def statuses_search_vf(engagement_manual_id, vf_name):
        engName = engagement_manual_id + ": " + vf_name
        # Search by VF name.
        Enter.text_by_id(
            Constants.Dashboard.Statuses.SearchBox.ID, vf_name, wait_for_page=True)
        Wait.id("eng-" + engName, wait_for_page=True)
        Click.id("eng-" + engName, wait_for_page=True)
        Wait.text_by_id(
            Constants.Dashboard.Overview.Title.ID, engName, wait_for_page=True)

    @staticmethod
    def go_to_main_dashboard():
        Click.id(Constants.Dashboard.Statuses.ID)

    @staticmethod
    def click_on_dashboard_and_validate_statistics(is_negative):
        #         Click.id(Constants.Dashboard.Default.DASHBOARD_ID)
        Wait.page_has_loaded()
        if is_negative:
            session.run_negative(lambda: Wait.id(
                Constants.Dashboard.Default.STATISTICS), "Negative test failed at Statistics appears")
        else:
            Wait.id(Constants.Dashboard.Default.STATISTICS)

    @staticmethod
    def click_on_create_vf():
        Click.id(Constants.Dashboard.LeftPanel.AddEngagement.ID)
