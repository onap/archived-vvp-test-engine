
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

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from services.constants import Constants
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()


class Wait:

    @staticmethod
    def text_by_xpath(xpath, text, wait_for_page=False):
        try:  # Wait 4 seconds for element and compare to expected result.
            if wait_for_page:
                Wait.page_has_loaded()
            WebDriverWait(
                session.ice_driver, session.wait_until_retires).until(
                expected_conditions.text_to_be_present_in_element(
                    (By.XPATH, xpath), text))
        # If failed - count the failure and add the error to list of errors.
        except Exception:
            error_msg = "Text - " + text + " not found in xPath " + xpath
            raise Exception(error_msg, xpath)

    @staticmethod
    def text_by_id(element_id, text, wait_for_page=False):
        try:  # Wait 4 seconds for element and compare to expected result.
            if wait_for_page:
                Wait.page_has_loaded()
            WebDriverWait(
                session.ice_driver, session.wait_until_retires).until(
                expected_conditions.text_to_be_present_in_element(
                    (By.ID, element_id), text))
        # If failed - count the failure and add the error to list of errors.
        except Exception:
            error_msg = "Text - " + text + " not found in ID " + element_id
            raise Exception(error_msg, element_id)

    @staticmethod
    def text_by_css(css, text, wait_for_page=False):
        try:  # Wait 4 seconds for element and compare to expected result.
            if wait_for_page:
                Wait.page_has_loaded()
            WebDriverWait(
                session.ice_driver, session.wait_until_retires).until(
                expected_conditions.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, css), text))
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            error_msg = "Text - " + text + " not found in CSS - " + css
            raise Exception(error_msg, e)

    @staticmethod
    def text_by_name(name, text, wait_for_page=False):
        try:  # Wait 4 seconds for element and compare to expected result.
            if wait_for_page:
                Wait.page_has_loaded()
            WebDriverWait(
                session.ice_driver, session.wait_until_retires).until(
                expected_conditions.text_to_be_present_in_element(
                    (By.NAME, name), text))
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            error_msg = "Text - " + text + " not found by NAME - " + name
            raise Exception(error_msg, e)

    @staticmethod
    def id(element_id, wait_for_page=False):
        try:  # Wait 4 seconds for element and compare to expected result.
            if wait_for_page:
                Wait.page_has_loaded()
            WebDriverWait(session.ice_driver,
                          session.wait_until_retires).until(
                expected_conditions.visibility_of_element_located(
                    (By.ID, element_id))
            )
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            error_msg = "Didn't find ID " + element_id
            raise Exception(error_msg, e)

    @staticmethod
    def css(element_css, wait_for_page=False):
        try:  # Wait 4 seconds for element and compare to expected result.
            if wait_for_page:
                Wait.page_has_loaded()
            WebDriverWait(
                session.ice_driver, session.wait_until_retires).until(
                expected_conditions.visibility_of_element_located(
                    (By.CSS_SELECTOR, element_css)))
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            error_msg = "Didn't find CSS Selector " + element_css
            raise Exception(error_msg, e)

    @staticmethod
    def is_css_exists(element_css, wait_for_page=False):
        try:  # Wait 4 seconds for element and compare to expected result.
            if wait_for_page:
                Wait.page_has_loaded()
            WebDriverWait(session.ice_driver,
                          session.wait_until_implicit_time).until(
                expected_conditions.visibility_of_element_located(
                    (By.CSS_SELECTOR, element_css))
            )
            return True
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            error_msg = "Didn't find CSS Selector " + element_css
            return False

    @staticmethod
    def link_text(link_inner_text, wait_for_page=False):
        try:
            if wait_for_page:
                Wait.page_has_loaded()
            WebDriverWait(
                session.ice_driver, session.wait_until_retires).until(
                expected_conditions.visibility_of_element_located(
                    (By.LINK_TEXT, link_inner_text)))
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            error_msg = "Didn't find LINK TEXT " + link_inner_text
            raise Exception(error_msg, e)

    @staticmethod
    def name(element_name, wait_for_page=False):
        try:
            if wait_for_page:
                Wait.page_has_loaded()
            WebDriverWait(
                session.ice_driver, session.wait_until_retires).until(
                expected_conditions.visibility_of_element_located(
                    (By.NAME, element_name)))
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            error_msg = "Didn't find NAME " + element_name
            raise Exception(error_msg, e)

    @staticmethod
    def xpath(element_xpath, wait_for_page=False):
        try:
            if wait_for_page:
                Wait.page_has_loaded()
            WebDriverWait(
                session.ice_driver, session.wait_until_retires).until(
                expected_conditions.visibility_of_element_located(
                    (By.XPATH, element_xpath)))
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            error_msg = "Didn't find XPath " + element_xpath
            raise Exception(error_msg, e)

    @staticmethod
    def page_has_loaded():
        for _ in range(Constants.FEConstants.RETRIES_NUMBER):
            try:
                httpRequests = session.ice_driver.execute_script(
                    'return window.angular ? window.angular.element("body").' +
                    'injector().get("$http").pendingRequests.length : 1;')
                if(str(httpRequests) == "0"):
                    time.sleep(session.wait_until_time_pause)
                    return
                logger.debug(
                    "Checking if {} page is loaded. ".format(
                        session.ice_driver.current_url))
                time.sleep(session.wait_until_time_pause)
            except Exception as exception:
                time.sleep(session.wait_until_time_pause)
                continue

        raise Exception("Page loading took too much time")

    @staticmethod
    def modal_to_dissappear():
        session.ice_driver.implicitly_wait(0)
        i = 0
        not_found = False
        while i < session.wait_until_retires:
            try:
                session.ice_driver.find_element_by_css_selector(
                    Constants.Dashboard.Wizard.Open.CSS)
            except NoSuchElementException:
                not_found = True
                try:
                    session.ice_driver.find_element_by_class_name(
                        Constants.Dashboard.Wizard.Open.CLASS_NAME)
                    not_found = False
                except NoSuchElementException:
                    not_found = True

            if not_found:
                break

            else:
                time.sleep(session.wait_until_time_pause)
                i += 1

        session.ice_driver.implicitly_wait(session.wait_until_implicit_time)
        if not_found:
            return True
        else:
            raise Exception("waitForModalToDissapper")

    @staticmethod
    def id_to_dissappear(id_element, wait_for_page=False):
        if wait_for_page:
            Wait.page_has_loaded()
        session.ice_driver.implicitly_wait(0)
        i = 0
        not_found = False
        while i < session.wait_until_retires:
            try:
                session.ice_driver.find_element_by_id(id_element)
            except NoSuchElementException:
                not_found = True

            if not_found:
                break
            else:
                time.sleep(session.wait_until_time_pause)
                i += 1

        session.ice_driver.implicitly_wait(session.wait_until_implicit_time)
        if not_found:
            return True
        else:
            raise Exception(
                "id_to_dissappear " +
                id_element +
                " num of retries = " +
                str(i))

    @staticmethod
    def name_to_dissappear(name_element, wait_for_page=False):
        if wait_for_page:
            Wait.page_has_loaded()
        session.ice_driver.implicitly_wait(0)
        i = 0
        not_found = False
        while i < session.wait_until_retires:
            try:
                session.ice_driver.find_element_by_name(name_element)
            except NoSuchElementException:
                not_found = True

            if not_found:
                break
            else:
                time.sleep(session.wait_until_time_pause)
                i += 1

        session.ice_driver.implicitly_wait(session.wait_until_implicit_time)
        if not_found:
            return True
        else:
            raise Exception(
                "name_to_dissappear " +
                name_element +
                " num of retries = " +
                str(i))

    @staticmethod
    def css_to_dissappear(css_element):
        session.ice_driver.implicitly_wait(0)
        i = 0
        not_found = False
        while i < session.wait_until_retires:
            try:
                session.ice_driver.find_element_by_css_selector(css_element)
            except NoSuchElementException:
                not_found = True

            if not_found:
                break
            else:
                time.sleep(session.wait_until_time_pause)
                i += 1

        session.ice_driver.implicitly_wait(session.wait_until_implicit_time)
        if not_found:
            return True
        else:
            raise Exception("css_to_dissappear" + css_element)

    @staticmethod
    def bucket_to_create(bucket_id):
        logger.debug("Waiting for %s bucket to be created" % bucket_id)
        time.sleep(session.positive_timeout)
