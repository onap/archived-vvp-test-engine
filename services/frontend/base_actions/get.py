
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
from services.frontend.base_actions.wait import Wait
from services.helper import Helper
from services.session import session


class Get:

    @staticmethod
    def by_id(attr_id_value, wait_for_page=False):
        try:
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.id(attr_id_value)
            return session.ice_driver.find_element_by_id(attr_id_value).text
        # If failed - count the failure and add the error to list of errors.
        except Exception:
            errorMsg = "Failed to get text of element " + attr_id_value
            raise Exception(errorMsg, attr_id_value)

    @staticmethod
    def by_css(attr_css_value, wait_for_page=False):
        try:
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.css(attr_css_value)
            return session.ice_driver.find_element_by_css_selector(
                attr_css_value).text
        # If failed - count the failure and add the error to list of errors.
        except Exception:
            errorMsg = "Failed to get text of element " + attr_css_value
            raise Exception(errorMsg, attr_css_value)

    @staticmethod
    def wysiwyg_element_by_id(attr_id_value):
        try:
            Wait.id(attr_id_value)
            return session.ice_driver.find_element_by_css_selector(
                "#" + attr_id_value + ".wysiwyg-textarea")
        # If failed - count the failure and add the error to list of errors.
        except Exception:
            errorMsg = "Failed to get element by id " + attr_id_value
            raise Exception(errorMsg, attr_id_value)

    @staticmethod
    def by_name(attr_name_value):
        try:
            Wait.name(attr_name_value)
            return session.ice_driver.find_element_by_name(
                attr_name_value).text
        # If failed - count the failure and add the error to list of errors.
        except Exception:
            errorMsg = "Failed to get text of element " + attr_name_value
            raise Exception(errorMsg, attr_name_value)

    @staticmethod
    def by_xpath(attr_name_value):
        try:
            Wait.xpath(attr_name_value)
            return session.ice_driver.find_element_by_xpath(
                attr_name_value).text
        # If failed - count the failure and add the error to list of errors.
        except Exception:
            errorMsg = "Failed to get text of element " + attr_name_value
            raise Exception(errorMsg, attr_name_value)

    @staticmethod
    def value_by_name(attr_name_value, wait_for_page=False):
        try:
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.name(attr_name_value)
            return session.ice_driver.find_element_by_name(
                attr_name_value).get_attribute("value")
        except Exception:
            errorMsg = "Failed to get value by name:" + attr_name_value
            raise Exception(errorMsg, attr_name_value)

    @staticmethod
    def meta_order_by_id(attr_id_value):
        try:
            Wait.id(attr_id_value)
            return session.ice_driver.find_element_by_id(
                attr_id_value).get_attribute("meta-order")
        except Exception:
            errorMsg = "Failed to get meta order by id:" + attr_id_value
            raise Exception(errorMsg, attr_id_value)

    @staticmethod
    def is_selected_by_id(attr_id_value, wait_for_page=False):
        try:
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.id(attr_id_value)
            return session.ice_driver.find_element_by_id(
                attr_id_value).is_selected()
        except Exception:
            errorMsg = "Failed to get if it's selected by id:" + attr_id_value
            raise Exception(errorMsg, attr_id_value)

    @staticmethod
    def is_checkbox_selected_by_id(attr_id_value, wait_for_page=False):
        try:
            if wait_for_page:
                Wait.page_has_loaded()
            Wait.id(attr_id_value)
            return Helper.internal_assert_boolean_true_false(
                session.ice_driver.find_element_by_id(
                    attr_id_value).get_attribute("value"), "on")
        except Exception:
            errorMsg = "Failed to get if it's selected by id:" + attr_id_value
            raise Exception(errorMsg, attr_id_value)
