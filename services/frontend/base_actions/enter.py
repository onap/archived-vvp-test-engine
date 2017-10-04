 
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
from datetime import datetime
import time

from services.frontend.base_actions.wait import Wait
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()
class Enter:
    
    @staticmethod
    def text_by_name(attr_name_value, typed_text, wait_for_page=False):
        try:  # Send keys to element in UI, by name locator (e.g. type something in text box).
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.name(attr_name_value)
            session.ice_driver.find_element_by_name(attr_name_value).clear()
            session.ice_driver.find_element_by_name(attr_name_value).send_keys(typed_text[:-1])
            time.sleep(session.wait_until_time_pause)
            session.ice_driver.find_element_by_name(attr_name_value).send_keys(typed_text[-1:])
        except Exception as e:  # If failed - count the failure and add the error to list of errors.
            errorMsg = "Failed to type " + typed_text + " in text box" 
            raise Exception(errorMsg, e)
    
    @staticmethod
    def text_by_xpath(attr_xpath_value, typed_text, wait_for_page=False):
        try:  # Send keys to element in UI, by name locator (e.g. type something in text box).
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.xpath(attr_xpath_value)
            session.ice_driver.find_element_by_xpath(attr_xpath_value).clear()
            session.ice_driver.find_element_by_xpath(attr_xpath_value).send_keys(typed_text[:-1])
            time.sleep(session.wait_until_time_pause)
            session.ice_driver.find_element_by_xpath(attr_xpath_value).send_keys(typed_text[-1:])
        except Exception as e:  # If failed - count the failure and add the error to list of errors.
            errorMsg = "Failed to type " + typed_text + " in text box" 
            raise Exception(errorMsg, attr_xpath_value)
    
    @staticmethod
    def text_by_id(attr_id_value, typed_text, wait_for_page=False):
        try:  # Send keys to element in UI, by ID locator (e.g. type something in text box).
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.id(attr_id_value)
            session.ice_driver.find_element_by_id(attr_id_value).clear()
            session.ice_driver.find_element_by_id(attr_id_value).send_keys(typed_text[:-1])
            time.sleep(session.wait_until_time_pause)
            session.ice_driver.find_element_by_id(attr_id_value).send_keys(typed_text[-1:])
        except Exception as e:  # If failed - count the failure and add the error to list of errors.
            errorMsg = "Failed to type " + typed_text + " in text box" 
            raise Exception(errorMsg, attr_id_value)
    
    @staticmethod
    def clear(attr_id_value):
        try:
            Wait.id(attr_id_value)
            session.ice_driver.find_element_by_id(attr_id_value).clear()
        except Exception as e:
            errorMsg = "Failed to clear text box" 
            raise Exception(errorMsg, attr_id_value)
    
    @staticmethod
    def text_by_css(attr_css_value, typed_text, wait_for_page=False):
        try:  # Send keys to element in UI, by CSS locator (e.g. type something in text box).
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.css(attr_css_value)
            session.ice_driver.find_element_by_css_selector(attr_css_value).clear()
            session.ice_driver.find_element_by_css_selector(attr_css_value).send_keys(typed_text[:-1])
            time.sleep(session.wait_until_time_pause)
            session.ice_driver.find_element_by_css_selector(attr_css_value).send_keys(typed_text[-1:])
        except Exception as e:  # If failed - count the failure and add the error to list of errors.
            errorMsg = "Failed to type " + typed_text + " in text box" 
            raise Exception(errorMsg, attr_css_value)
    
    @staticmethod
    def text_by_link_text(attr_link_text_value, typed_text, wait_for_page=False):
        try:  # Send keys to element in UI, by name locator (e.g. type something in text box).
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.link_text(attr_link_text_value)
            session.ice_driver.find_element_by_link_text(attr_link_text_value).clear()
            session.ice_driver.find_element_by_link_text(attr_link_text_value).send_keys(typed_text[:-1])
            time.sleep(session.wait_until_time_pause)
            session.ice_driver.find_element_by_link_text(attr_link_text_value).send_keys(typed_text[-1:])
        except Exception as e:  # If failed - count the failure and add the error to list of errors.
            errorMsg = "Failed to type " + typed_text + " in text box" 
            raise Exception(errorMsg, attr_link_text_value)

    @staticmethod
    def date_picker(selector, property_name, wait_for_page=False):
        try:
            if wait_for_page:
                Wait.page_has_loaded()
            session.ice_driver.execute_script(
                "var element = angular.element(document.querySelector('" + selector + "')); element.scope()." +
                property_name + " = new Date('" + str(datetime.today().isoformat()) + "')")
        except Exception as e:
            errorMsg = "Failed to select date with datePicker."
            raise Exception(errorMsg, str(e))
