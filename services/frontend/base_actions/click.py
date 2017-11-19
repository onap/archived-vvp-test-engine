
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

from services.frontend.base_actions.wait import Wait
from services.session import session


class Click:

    @staticmethod
    def id(element_id, wait_for_page=False):
        try:
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.id(element_id)
            session.ice_driver.find_element_by_id(element_id).click()
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "Failed to click_on on ID " + element_id
            raise Exception(errorMsg, e)

    @staticmethod
    def name(element_name, wait_for_page=False):
        try:
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.name(element_name)
            session.ice_driver.find_element_by_name(element_name).click()
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "Failed to click_on on ID " + element_name
            raise Exception(errorMsg, e)

    @staticmethod
    def link_text(link_inner_text, wait_for_page=False):
        try:
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.link_text(link_inner_text)
            session.ice_driver.find_element_by_link_text(
                link_inner_text).click()
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "Failed to click_on on LINK TEXT " + link_inner_text
            raise Exception(errorMsg, e)

    @staticmethod
    def css(element_css, wait_for_page=False):
        try:
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.css(element_css)
            session.ice_driver.find_element_by_css_selector(
                element_css).click()
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "Failed to click_on on CSS Selector " + element_css
            raise Exception(errorMsg, e)

    @staticmethod
    def xpath(element_xpath, wait_for_page=False):
        try:
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.xpath(element_xpath)
            session.ice_driver.find_element_by_xpath(element_xpath).click()
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "Failed to click_on on XPATH " + element_xpath
            raise Exception(errorMsg, e)

    @staticmethod
    def drag_and_drop_by_css(source_css, xoffset, yoffset):
        ns = session.ice_driver.find_element_by_id("step-description-1")
        ActionChains(session.ice_driver).move_to_element(ns).perform()
        Wait.css(source_css)
        source_element = session.ice_driver.find_element_by_css_selector(
            source_css)
        ActionChains(
            session.ice_driver).drag_and_drop_by_offset(
            source_element,
            xoffset,
            yoffset).perform()
