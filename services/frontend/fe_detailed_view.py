
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
import time

from selenium.webdriver.support.ui import Select

from services.constants import Constants, ServiceProvider
from services.database.db_general import DBGeneral
from services.frontend.base_actions.click import Click
from services.frontend.base_actions.enter import Enter
from services.frontend.base_actions.get import Get
from services.frontend.base_actions.wait import Wait
from services.frontend.fe_dashboard import FEDashboard
from services.frontend.fe_general import FEGeneral
from services.frontend.fe_user import FEUser
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()


class FEDetailedView:

    @staticmethod
    def search_vf_and_go_to_detailed_view(engagement_manual_id, vf_name):
        engName = engagement_manual_id + ": " + vf_name
        detailed_view_id = Constants.Dashboard.DetailedView.ID + engName
        FEDashboard.statuses_search_vf(engagement_manual_id, vf_name)
        Click.id(detailed_view_id, wait_for_page=True)
        return detailed_view_id

    @staticmethod
    def update_aic_version():
        Click.id(
            Constants.Dashboard.DetailedView.ValidationDetails.PLUS, wait_for_page=True)
        Wait.text_by_id(Constants.Dashboard.Modal.TITLE_ID,
                        Constants.Dashboard.DetailedView.ValidationDetails.TITLE, wait_for_page=True)
        Select(session.ice_driver.find_element_by_id(Constants.Dashboard.DetailedView.AIC.Dropdown.ID)
               ).select_by_visible_text(Constants.Dashboard.DetailedView.ValidationDetails.TargetAICVersion.AIC3)
        Click.xpath("//option[3]", wait_for_page=True)
        Click.id(
            Constants.Dashboard.DetailedView.ValidationDetails.SAVE, wait_for_page=True)

    @staticmethod
    def open_validation_details():
        Click.id(
            Constants.Dashboard.DetailedView.ValidationDetails.PLUS, wait_for_page=True)
        Wait.text_by_id(Constants.Dashboard.Modal.TITLE_ID,
                        Constants.Dashboard.DetailedView.ValidationDetails.TITLE, wait_for_page=True)

    @staticmethod
    def save_validation_details():
        Click.id(
            Constants.Dashboard.DetailedView.ValidationDetails.SAVE, wait_for_page=True)

    @staticmethod
    def update_target_lab_entry():
        Click.id(
            Constants.Dashboard.DetailedView.TargetLabEntry.CHANGE, wait_for_page=True)
        Enter.date_picker(
            '#lab-entry-date', 'vm.targetLabDate', wait_for_page=True)
        Click.css(
            Constants.Dashboard.DetailedView.TargetLabEntry.INPUT_CSS, wait_for_page=True)
        Click.css(Constants.SubmitButton.CSS, wait_for_page=True)
        actualDate = Get.by_css(
            Constants.Dashboard.DetailedView.TargetLabEntry.CONTENT_CSS, wait_for_page=True)
        return str(actualDate)

    @staticmethod
    def validate_target_lab_entry(date):
        Wait.text_by_css(Constants.Dashboard.DetailedView.TargetLabEntry.CSS,
                         Constants.Dashboard.DetailedView.TargetLabEntry.TEXT, wait_for_page=True)
        actualDate = Get.by_css(
            Constants.Dashboard.DetailedView.TargetLabEntry.CONTENT_CSS)
        Helper.internal_assert(actualDate, date)

    @staticmethod
    def update_ecomp_release(EcompName):
        count = 0
        try:
            Click.id(Constants.Dashboard.DetailedView.ValidationDetails.PLUS)
            Wait.text_by_id(Constants.Dashboard.Modal.TITLE_ID,
                            Constants.Dashboard.DetailedView.ValidationDetails.TITLE, wait_for_page=True)
            Click.id(
                Constants.Dashboard.DetailedView.ECOMP.Dropdown.ID, wait_for_page=True)
            Select(session.ice_driver.find_element_by_id(
                Constants.Dashboard.DetailedView.ECOMP.Dropdown.ID)).select_by_visible_text(EcompName)
            Click.id(Constants.Dashboard.DetailedView.ValidationDetails.ECOMPRelease.ID_ECOMP +
                     EcompName, wait_for_page=True)
            count += 1
            Wait.id(Constants.Dashboard.DetailedView.ValidationDetails.ECOMPRelease.ID_ECOMP +
                    Constants.Dashboard.DetailedView.ValidationDetails.ECOMPRelease.UNKNOW, wait_for_page=True)
            Select(session.ice_driver.find_element_by_id(Constants.Dashboard.DetailedView.ECOMP.Dropdown.ID)
                   ).select_by_visible_text(Constants.Dashboard.DetailedView.ValidationDetails.ECOMPRelease.UNKNOW)
            Click.id(Constants.Dashboard.DetailedView.ValidationDetails.ECOMPRelease.ID_ECOMP +
                     Constants.Dashboard.DetailedView.ValidationDetails.ECOMPRelease.UNKNOW, wait_for_page=True)
            count += 1
            Click.id(
                Constants.Dashboard.DetailedView.ValidationDetails.SAVE, wait_for_page=True)
            Helper.internal_assert(count, 2)
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "Failed in update_ecomp_release ."
            raise Exception(errorMsg)

    @staticmethod
    def update_vf_version():
        try:
            Click.id(
                Constants.Dashboard.DetailedView.ValidationDetails.PLUS, wait_for_page=True)
            Wait.text_by_id(Constants.Dashboard.Modal.TITLE_ID,
                            Constants.Dashboard.DetailedView.ValidationDetails.TITLE, wait_for_page=True)
            newVFVersionName = "newVFVersionName-" + \
                Helper.rand_string("randomString")
            Click.id(
                Constants.Dashboard.DetailedView.ValidationDetails.VFVersion.ID_VERSION)
            Enter.text_by_id(
                Constants.Dashboard.DetailedView.ValidationDetails.VFVersion.ID_VERSION, newVFVersionName, wait_for_page=True)
            Click.id(
                Constants.Dashboard.DetailedView.ValidationDetails.SAVE, wait_for_page=True)
            return newVFVersionName
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "Failed in update_ecomp_release ."
            raise Exception(errorMsg)

    @staticmethod
    def validate_aic_version():
        FEGeneral.refresh()
        Wait.id(
            Constants.Dashboard.DetailedView.AIC.ID + "3.0", wait_for_page=True)

    @staticmethod
    def validate_ecomp_version():
        FEGeneral.refresh()
        Wait.id(Constants.Dashboard.DetailedView.ECOMP.ID +
                Constants.Dashboard.DetailedView.ValidationDetails.ECOMPRelease.UNKNOW, wait_for_page=True)

    @staticmethod
    def validate_vf_version(newVFVersionName):
        FEGeneral.refresh()
        Wait.id(Constants.Dashboard.DetailedView.ValidationDetails.VFVersion.VF_VERSION_ID +
                newVFVersionName, wait_for_page=True)

    @staticmethod
    def validate_all_titles_on_dv_form():
        Wait.text_by_id(Constants.Dashboard.DetailedView.DeploymentTarget.ID,
                        Constants.Dashboard.DetailedView.DeploymentTarget.TEXT, wait_for_page=True)
        Wait.text_by_id(Constants.Dashboard.DetailedView.VirtualFunctionComponents.ID,
                        Constants.Dashboard.DetailedView.VirtualFunctionComponents.TEXT)
        Wait.text_by_id(Constants.Dashboard.DetailedView.TargetLabEntry.ID,
                        Constants.Dashboard.DetailedView.TargetLabEntry.TEXT)
        Wait.text_by_id(Constants.Dashboard.DetailedView.ValidationDetails.ID,
                        Constants.Dashboard.DetailedView.ValidationDetails.TEXT)
        Wait.text_by_id(Constants.Dashboard.DetailedView.ValidationDetails.TargetAICVersion.ID,
                        Constants.Dashboard.DetailedView.ValidationDetails.TargetAICVersion.TEXT)
        Wait.text_by_id(Constants.Dashboard.DetailedView.ValidationDetails.ECOMPRelease.ID,
                        Constants.Dashboard.DetailedView.ValidationDetails.ECOMPRelease.TEXT)
        Wait.text_by_id(Constants.Dashboard.DetailedView.ValidationDetails.VFVersion.ID,
                        Constants.Dashboard.DetailedView.ValidationDetails.VFVersion.TEXT, wait_for_page=True)

    @staticmethod
    def add_deployment_target(user_content):
        Click.id(Constants.Dashboard.DetailedView.TargetLabEntry.Add.ID)
        Wait.text_by_id(Constants.Dashboard.Modal.TITLE_ID,
                        Constants.Dashboard.DetailedView.DeploymentTarget.TITLE)
        # FIXME: empty drop-down, tests will fail.
        Select(session.ice_driver.find_element_by_xpath(
            "//select")).select_by_visible_text("Lisle (DPA3)")
        Click.id(
            Constants.Dashboard.DetailedView.DeploymentTarget.SAVE, wait_for_page=True)
        Wait.text_by_css(
            Constants.Dashboard.DetailedView.DeploymentTarget.CSS, "Lisle (DPA3)", wait_for_page=True)
        Wait.text_by_id(Constants.Dashboard.DetailedView.AIC.ID +
                        user_content['target_aic'], user_content['target_aic'])
        e2edate = FEGeneral.date_short_formatter()
        Wait.text_by_css(
            Constants.Dashboard.DetailedView.TargetLabEntry.CONTENT_CSS, e2edate)

    @staticmethod
    def remove_deployment_target(user_content):
        Wait.text_by_id(
            "visible-dts-Lisle (DPA3)", "Lisle (DPA3)", wait_for_page=True)
        dt_site_id = DBGeneral.select_query(
            "SELECT uuid FROM public.ice_deployment_target_site where name = 'Lisle (DPA3)'")
        Click.id("visible-dts-Lisle (DPA3)")
        Wait.id(
            Constants.Dashboard.DetailedView.DeploymentTarget.ID_REMOVE_DTS + dt_site_id)
        Click.id(Constants.Dashboard.DetailedView.DeploymentTarget.ID_REMOVE_DTS +
                 dt_site_id, wait_for_page=True)
        session.run_negative(lambda: Wait.text_by_id(
            "visible-dts-Lisle (DPA3)", "Lisle (DPA3)", wait_for_page=True), "Negative test failed at wait text Lisle (DPA3)")

    @staticmethod
    def add_vfc():
        vfcName = "VFC-" + Helper.rand_string("randomString")
        Click.id(Constants.Dashboard.DetailedView.VFC.Add.ID)
        Enter.text_by_name("name", vfcName)
        session.ice_driver.find_element_by_name("extRefID").click()
        Enter.text_by_name("extRefID", Helper.rand_string("randomNumber"))
        Select(session.ice_driver.find_element_by_id(
            Constants.Dashboard.DetailedView.VFC.Choose_Company.ID)).select_by_visible_text(ServiceProvider.MainServiceProvider)
        Click.id(Constants.Dashboard.DetailedView.VFC.Save_button.ID)
        return vfcName

    @staticmethod
    def add_vfcs(name, extRefID):
        Click.id(
            Constants.Dashboard.DetailedView.VFC.Add.ID, wait_for_page=True)
        Wait.text_by_id(Constants.Dashboard.Modal.TITLE_ID,
                        "Add Virtual Function Components (VFCs)")
        Enter.text_by_name("name", name)
        Click.name("extRefID", wait_for_page=True)
        Enter.text_by_name("extRefID", extRefID, wait_for_page=True)
        Select(session.ice_driver.find_element_by_id(
            Constants.Dashboard.DetailedView.VFC.Choose_Company.ID)).select_by_visible_text("Amdocs")
        Wait.text_by_css("span.add-text", "Add VFC", wait_for_page=True)
        Click.css("span.add-text", wait_for_page=True)
        logger.debug("Add VFC no.2")
        Enter.text_by_xpath(
            "//div[2]/ng-form/div/input", "djoni2", wait_for_page=True)
        Enter.text_by_xpath("//div[2]/ng-form/div[2]/input", "loka2")
        Enter.text_by_xpath("//div[2]/ng-form/div[4]/input", "companyManual2")
        Click.id(
            Constants.Dashboard.DetailedView.VFC.Save_button.ID, wait_for_page=True)

    @staticmethod
    def remove_vfc(user_content):
        vf_id = DBGeneral.select_where(
            "uuid", "ice_vf", "name", user_content['vfName'], 1)
        djoni_uuid = None
        counter = 0
        while not djoni_uuid and counter <= Constants.DBConstants.RETRIES_NUMBER:
            time.sleep(session.wait_until_time_pause_long)
            djoni_uuid = DBGeneral.select_where_and(
                "uuid", "ice_vfc", "vf_id", vf_id, "name", "djoni", 1)
            logger.debug("Checklist state not changed yet  (%s of %s)" % (
                counter, Constants.DBConstants.RETRIES_NUMBER))
            counter += 1
        logger.debug("VFC_UUID was successfully selecteded : " +
                     djoni_uuid + ", and was verified over the DB")
        Wait.text_by_id(Constants.Dashboard.DetailedView.VFC.ID +
                        "djoni", "djoni (loka)", wait_for_page=True)
        Wait.text_by_id(Constants.Dashboard.DetailedView.VFC.ID +
                        "djoni2", "djoni2 (loka2)", wait_for_page=True)
        Click.id(
            Constants.Dashboard.DetailedView.VFC.ID + "djoni", wait_for_page=True)
        Click.id(Constants.Dashboard.DetailedView.VFC.Remove.ID +
                 djoni_uuid, wait_for_page=True)

    @staticmethod
    def validate_deployment_targets(user_content, users):
        for user in users:
            FEGeneral.re_open(Constants.Default.LoginURL.TEXT)
            logger.debug("Login with user " + user)
            FEUser.login(user, Constants.Default.Password.TEXT)
            FEDetailedView.search_vf_and_go_to_detailed_view(
                user_content['engagement_manual_id'], user_content['vfName'])
            Wait.id(
                Constants.Dashboard.DetailedView.DeploymentTarget.AddDeploymentTargetButton.ID)

    @staticmethod
    def add_remove_deployment_targets(user_content, users):
        for user in users:
            FEGeneral.re_open(Constants.Default.LoginURL.TEXT)
            logger.debug("Login with user " + user)
            FEUser.login(user, Constants.Default.Password.TEXT)
            FEDetailedView.search_vf_and_go_to_detailed_view(
                user_content['engagement_manual_id'], user_content['vfName'])
            FEDetailedView.add_deployment_target(user_content)
            FEDetailedView.remove_deployment_target(user_content)

    @staticmethod
    def validate_negative_role_for_deployment_targets(user_content, users):
        for user in users:
            FEGeneral.re_open(Constants.Default.LoginURL.TEXT)
            logger.debug("Login with user " + user)
            FEUser.login(user, Constants.Default.Password.TEXT)
            FEDetailedView.search_vf_and_go_to_detailed_view(
                user_content['engagement_manual_id'], user_content['vfName'])
            session.run_negative(lambda: Click.id(Constants.Dashboard.DetailedView.DeploymentTarget.AddDeploymentTargetButton.ID),
                                 "Negative test failed at click_on_ deployment-targets with user  %s" % user)

    @staticmethod
    def click_on_update_aic_version():
        Click.id(
            Constants.Dashboard.DetailedView.ValidationDetails.PLUS, wait_for_page=True)
        Wait.text_by_id(Constants.Dashboard.Modal.TITLE_ID,
                        Constants.Dashboard.DetailedView.ValidationDetails.TITLE, wait_for_page=True)

    @staticmethod
    def click_on_update_ecomp_release():
        Click.id(
            Constants.Dashboard.DetailedView.ValidationDetails.PLUS, wait_for_page=True)
        Wait.text_by_id(Constants.Dashboard.Modal.TITLE_ID,
                        Constants.Dashboard.DetailedView.ValidationDetails.TITLE, wait_for_page=True)

    @staticmethod
    def select_aic_version_from_list(aic_version):
        Select(session.ice_driver.find_element_by_id(
            Constants.Dashboard.DetailedView.AIC.Dropdown.ID)).select_by_visible_text(aic_version)

    @staticmethod
    def compare_aic_selected_version(expected_aic_version):
        Helper.internal_assert(Get.by_id(
            Constants.Dashboard.DetailedView.AIC.ID + expected_aic_version), expected_aic_version)

    @staticmethod
    def compare_selected_ecomp_release(expected_ecomp_release):
        Helper.internal_assert(Get.by_id(
            Constants.Dashboard.DetailedView.ECOMP.ID + expected_ecomp_release), expected_ecomp_release)

    @staticmethod
    def validate_deprecated_aic_version_in_dropdown(expected_aic_version):
        Helper.internal_assert(Get.by_id(Constants.Dashboard.DetailedView.AIC.Dropdown.UniversalVersion.ID %
                                         expected_aic_version), "AIC " + expected_aic_version + " - Deprecated")

    @staticmethod
    def validate_deprecated_ecomp_release_in_dropdown(expected_ecomp_release):
        Helper.internal_assert(Get.by_id(Constants.Dashboard.DetailedView.ECOMP.Dropdown.UniversalRelease.ID %
                                         expected_ecomp_release), expected_ecomp_release + " - Deprecated")
