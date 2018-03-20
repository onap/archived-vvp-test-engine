
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
from services.constants import Constants
from services.database.db_cms import DBCMS
from services.frontend.base_actions.click import Click
from services.frontend.base_actions.enter import Enter
from services.frontend.base_actions.wait import Wait
from services.frontend.fe_dashboard import FEDashboard
from services.frontend.fe_user import FEUser
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()


class FECms:

    @staticmethod
    def validate_5_last_announcement_displayed(
            listOfTitleAnDescriptions, user_content, last_title):
        last_description = listOfTitleAnDescriptions[
            len(listOfTitleAnDescriptions) - 1][1]
        Wait.text_by_id(Constants.Toast.CMS_ID, last_title + ".")
        FEDashboard.open_announcement()
        Wait.text_by_id(Constants.Cms.Toast_title_id, last_title)
        Wait.text_by_id(Constants.Cms.Toast_description, last_description)
        DBCMS.update_X_days_back_post(last_title, xdays=3)
        Click.id(Constants.Cms.Test_addDT_close_modal_button)
        FEUser.logout()
        # Validate Announcement TOAST not displayed
        FEUser.login(user_content['email'], Constants.Default.Password.TEXT)
        session.run_negative(
            lambda: Wait.text_by_id(
                Constants.Cms.Toast_title_id,
                last_title),
            "Last Announcement displayed in News & Announcements sections %s" %
            last_title)

    @staticmethod
    def validate_grandchild_page(
            parent_title,
            child_title,
            grand_child_title,
            description):
        Click.id(Constants.Cms.Documentation)
        Click.id(parent_title)
        Click.id(child_title)
        Click.id(grand_child_title)
        Wait.text_by_id("center-" + grand_child_title, grand_child_title)
        page_id = DBCMS.get_last_inserted_page_id()
        Wait.text_by_id(page_id, description)

    @staticmethod
    def announcement_validate_toast(title, description, user_content):
        Wait.text_by_id(Constants.Toast.CMS_ID, title + ".")
        FEDashboard.open_announcement()
        Wait.text_by_id(Constants.Cms.Toast_title_id, title)
        Wait.text_by_id(Constants.Cms.Toast_description, description)
        Click.id(Constants.Cms.Test_addDT_close_modal_button)
        Click.css("button.close")
        FEUser.logout()
        FEUser.login(user_content['email'], Constants.Default.Password.TEXT)
        # Validate Announcement displayed in News & Announcements sections
        session.run_negative(lambda: FEDashboard.open_announcement(
        ), "Announcement toast disappear after 2 days %s" % title)
        Wait.text_by_id(title, title)
        Wait.text_by_id(description, description)

    @staticmethod
    def search_documentation_title(title, user_content):
        FEDashboard.open_documentation(title)
        Wait.text_by_id(title, title)
        logger.debug("Search Documentation by title")
        Enter.text_by_id(
            Constants.Cms.SearchDocumentation,
            title,
            wait_for_page=True)
        Wait.text_by_id(title, title)
        Click.id(title, wait_for_page=True)
        Wait.text_by_id(title, title)
        logger.debug("Documentation found (searched by title)")

    @staticmethod
    def search_documentation_content(title, content):
        FEDashboard.open_documentation(title)
        Wait.text_by_id(title, title)
        logger.debug("Search Documentation by content")
        Enter.text_by_id(
            Constants.Cms.SearchDocumentation,
            content,
            wait_for_page=True)
        Wait.text_by_id(title, title)
        Click.id(title, wait_for_page=True)
        Wait.text_by_css(Constants.Cms.DocumentationPageContent, content)
        logger.debug("Documentation found (searched by content)")

    @staticmethod
    def validate_expired_post_Announcement(email, title, description):
        title2 = Constants.Toast.TEXT + title + "."
        Wait.text_by_id(
            Constants.Toast.CMS_ID,  title2, True)
        FEDashboard.open_announcement()
        Wait.text_by_id(Constants.Cms.Toast_title_id, title)
        Wait.text_by_id(Constants.Cms.Toast_description, description)
        DBCMS.update_X_days_back_post(title, xdays=3)
        Click.id(Constants.Cms.Test_addDT_close_modal_button)
        FEUser.logout()
        FEUser.login(email, Constants.Default.Password.TEXT)
        session.run_negative(
            lambda: Wait.text_by_id(
                Constants.Toast.CMS_ID,
                title2),
            "Announcement toast not disappear after 2 days %s" %
            title)

    @staticmethod
    def validate_page(title, description):
        Click.id(Constants.Cms.Documentation)
        Click.id(title)
        Wait.text_by_id("center-" + title, title)
        page_id = DBCMS.get_last_inserted_page_id()
        Wait.text_by_id(page_id, description)

    @staticmethod
    def validate_FAQ(description):
        Wait.text_by_id(Constants.Cms.Tooltip_title, "Did you know?", True)
        Wait.text_by_id(Constants.Cms.Tooltip_description, description, True)

    @staticmethod
    def validate_news(title, description):
        Wait.text_by_id(title, title)
        Wait.text_by_id(description, description)
        Click.id(title)
        Wait.text_by_id(Constants.Cms.Toast_title_id, title)
        Wait.text_by_id(Constants.Cms.Toast_description, description)

    @staticmethod
    def validae_announcement(title, description):
        Wait.text_by_id(Constants.Toast.CMS_ID, title + ".")
        FEDashboard.open_announcement()
        Wait.text_by_id(Constants.Cms.Toast_title_id, title)
        Wait.text_by_id(Constants.Cms.Toast_description, description)
