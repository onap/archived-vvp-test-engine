
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
import json
import time

from selenium.webdriver.support.select import Select

from services.constants import Constants
from services.frontend.base_actions.click import Click
from services.frontend.base_actions.enter import Enter
from services.frontend.base_actions.get import Get
from services.frontend.base_actions.wait import Wait
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()


class FEGeneral(Helper):

    @staticmethod
    def date_formatter():
        d = int(time.strftime("%d"))
        if (d == 1 or d == 21 or d == 31):
            d = str(d) + "st"
        elif (d == 2 or d == 22):
            d = str(d) + "nd"
        elif (d == 3 or d == 23):
            d = str(d) + "rd"
        else:
            d = str(d) + "th"
        return time.strftime("%A %B " + d + " %Y")

    @staticmethod
    def date_short_formatter():
        return time.strftime("%-m" + "/" + "%-d" + "/" + "%y")

    @staticmethod
    def re_open(reopen_url):
        try:
            logger.debug("Reopen URL: " + reopen_url)
            session.ice_driver.get('javascript:localStorage.clear();')
            session.ice_driver.get('javascript:sessionStorage.clear();')
            session.ice_driver.delete_all_cookies()
            # Open FireFox with requested URL.
            session.ice_driver.get("about:blank")
            # Open FireFox with requested URL.
            session.ice_driver.get(reopen_url)
            session.ice_driver.maximize_window()
            Wait.page_has_loaded()
        except Exception:
            errorMsg = "Could not reopen requested page"
            raise Exception(errorMsg, reopen_url)

    @staticmethod
    def re_open_not_clean_cache(url):
        try:
            # Open FireFox with requested URL.
            session.ice_driver.get(url)
            session.ice_driver.maximize_window()
        except BaseException:
            errorMsg = "Could not reopen requested page"
            raise Exception(errorMsg, url)
            logger.debug("Moving to next test case")

    @staticmethod
    def refresh():
        try:
            session.ice_driver.refresh()
            Wait.page_has_loaded()
        except Exception as e:
            errorMsg = "Could not refresh the page."
            logger.error(errorMsg)
            raise Exception(errorMsg, e)

    @staticmethod
    def smart_refresh():
        session.ice_driver.refresh()
        i = 0
        success = False
        while not success and i < 2:
            try:
                Wait.page_has_loaded()
                success = True
                break
            except:
                i += 1
                time.sleep(1)
                pass
        if not success:
            raise Exception("Failed to wait for refresh")

    @staticmethod
    def select_vendor_from_list(vendor):
        Wait.name(Constants.Signup.Company.NAME)
        Select(session.ice_driver.find_element_by_name(
            Constants.Signup.Company.NAME)).select_by_visible_text(vendor)

    @staticmethod
    def go_to_signup_from_login():
        Click.link_text(Constants.Login.Signup.LINK_TEXT, wait_for_page=True)
        Wait.text_by_css(
            Constants.Signup.Title.CSS,
            Constants.Signup.Title.TEXT,
            wait_for_page=True)

    @staticmethod
    def form_enter_name(name):
        Enter.text_by_name(Constants.Signup.FullName.NAME, name)

    @staticmethod
    def form_enter_email(email):
        Enter.text_by_name(Constants.Signup.Email.NAME, email)

    @staticmethod
    def form_enter_phone(phone):
        Enter.text_by_name(Constants.Signup.Phone.NAME, phone)

    @staticmethod
    def form_enter_password(password):
        Enter.text_by_name(Constants.Signup.Password.NAME, password)

    @staticmethod
    def form_check_checkbox(xpath):
        Click.xpath(xpath)

    @staticmethod
    def click_on_submit():
        Click.css(Constants.SubmitButton.CSS)

    @staticmethod
    def go_to_login_from_signup():
        Click.link_text(Constants.Signup.HaveAccount.LINK_TEXT)
        Wait.text_by_css(Constants.Login.Title.CSS, Constants.Login.Title.TEXT)

    @staticmethod
    def verify_toast_message(expected_message):
        Wait.text_by_id(
            Constants.Toast.ID, expected_message, wait_for_page=True)

    @staticmethod
    def form_validate_name(name):
        name_in_ui = Get.value_by_name(
            Constants.Dashboard.Avatar.Account.FullName.NAME)
        Helper.internal_assert(name, name_in_ui)

    @staticmethod
    def form_validate_email(email):
        email_in_ui = Get.value_by_name(
            Constants.Dashboard.Avatar.Account.Email.NAME)
        Helper.internal_assert(email, email_in_ui)

    @staticmethod
    def form_validate_phone(phone):
        phone_in_ui = Get.value_by_name(
            Constants.Dashboard.Avatar.Account.Phone.NAME)
        Helper.internal_assert(phone, phone_in_ui)

    @staticmethod
    def form_validate_company(company):
        company_in_ui = Get.value_by_name(
            Constants.Dashboard.Avatar.Account.Company.NAME)
        Helper.internal_assert(company, company_in_ui)

    @staticmethod
    def form_validate_ssh(key):
        key_in_ui = Get.value_by_name(
            Constants.Dashboard.Avatar.Account.SSHKey.NAME)
        Helper.internal_assert(key, key_in_ui)

    @staticmethod
    def go_to_reset_password_from_login():
        Click.link_text(Constants.Login.ResetPassword.LINK_TEXT)

    @staticmethod
    def send_reset_password(email):
        FEGeneral.go_to_reset_password_from_login()
        Wait.text_by_css(
            Constants.ResetPassword.Title.CSS,
            Constants.ResetPassword.Title.TEXT)
        Enter.text_by_name(Constants.ResetPassword.Email.NAME, email)
        Wait.text_by_css(
            Constants.SubmitButton.CSS, Constants.ResetPassword.Button.TEXT)
        Click.css(Constants.SubmitButton.CSS)
        Wait.text_by_id(
            Constants.Toast.ID, Constants.ResetPassword.Toast.Success.TEXT)
        logger.debug(Constants.ResetPassword.Toast.Success.TEXT)

    @staticmethod
    def verify_home_elements():
        Wait.text_by_id(Constants.Home.Title.ID, Constants.Home.Title.TEXT)
        element = session.ice_driver.find_element_by_id(
            Constants.Home.Collaborate.ID)
        element.location_once_scrolled_into_view
        Wait.text_by_xpath(
            Constants.Home.Collaborate.XPATH, Constants.Home.Collaborate.TEXT)
        Wait.text_by_xpath(
            Constants.Home.Validate.XPATH, Constants.Home.Validate.TEXT)
        Wait.text_by_xpath(
            Constants.Home.Incubate.XPATH, Constants.Home.Incubate.TEXT)
        element = session.ice_driver.find_element_by_id(Constants.Home.Logo.ID)
        element.location_once_scrolled_into_view
        Wait.text_by_id(Constants.Home.Title.ID, Constants.Home.Title.TEXT)

    @staticmethod
    def go_to_signup_from_homepage():
        Click.link_text(Constants.Home.GetStarted.LINK_TEXT)
        Wait.text_by_css(
            Constants.Signup.Title.CSS, Constants.Signup.Title.TEXT)

    @staticmethod
    def get_meta_order_of_element(element_id):
        return Get.meta_order_by_id(element_id)

    @staticmethod
    def verify_num_of_existing_ids(requested_num_of_ids, id_prefix):
        existing_id_objects_in_page = 0
        ids = session.ice_driver.find_elements_by_xpath('//*[@id]')
        for id in ids:
            if id_prefix in id.get_attribute('id'):
                # Print id.tag_name (id name as string).
                logger.debug(id.get_attribute('id'))
                existing_id_objects_in_page += 1
        Helper.internal_assert(
            existing_id_objects_in_page, requested_num_of_ids)
        logger.debug("verify_num_of_existing_ids succeeded")

    @staticmethod
    def verify_existing_files_in_list(items_list, id_to_search_for):
        element = session.ice_driver.find_elements_by_id(id_to_search_for)
        element_attribute_items = json.loads(element[0].get_attribute('name'))
        Helper.internal_assert(
            len(items_list), len(element_attribute_items) - 1)
        extracted_files_list = list()
        for file in element_attribute_items:
            extracted_files_list.append(file['File'])
        for item in items_list:
            if item not in extracted_files_list:
                Helper.assertTrue(
                    False, "%s does not exist over the client's side" % item)
        logger.debug(
            "verify_existing_files_in_list succeeded, " +
            "All vf repo files are available for choosing.")
