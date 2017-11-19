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
from wheel.signatures import assertTrue

from iceci.decorator.exception_decor import exception
from services.constants import Constants
from services.logging_service import LoggingServiceFactory
from tests.uiTests.test_ui_base import TestUiBase
from services.types import API, Frontend, DB
logger = LoggingServiceFactory.get_logger()


class TestCMSNewsAndAnnoucements(TestUiBase):
    user_content = None

    @classmethod
    def setUpClass(cls):
        super(TestCMSNewsAndAnnoucements, cls).setUpClass()

        cls.user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        logger.debug("user_conntent = " + str(cls.user_content))

    def setUp(self):
        super(TestCMSNewsAndAnnoucements, self).setUp()
        Frontend.User.login(
            self.user_content['email'],
            Constants.Default.Password.TEXT)

    @exception()
    def test_announcements(self):
        categoryId = DB.Cms.get_cms_category_id('News')
        assertTrue(len(categoryId) > 0 and not None)

    @exception()
    def test_insert_post_Announcement(self):
        title, description = DB.Cms.create_announcement()
        Frontend.User.logout()
        Frontend.User.login(
            self.user_content['email'], Constants.Default.Password.TEXT)
        Frontend.Cms.validae_announcement(title, description)

    @exception()
    def test_insert_post_News(self):
        title, description = DB.Cms.create_news()
        Frontend.User.logout()
        Frontend.User.login(
            self.user_content['email'], Constants.Default.Password.TEXT)
        Frontend.Cms.validate_news(title, description)

    @exception()
    def test_insert_post_FAQ(self):
        title, description = DB.Cms.create_faq()
        Frontend.User.logout()
        Frontend.User.login(
            self.user_content['email'], Constants.Default.Password.TEXT)
        Frontend.Cms.validate_FAQ(description)

    @exception()
    def test_insert_page(self):
        title, description = DB.Cms.create_page()
        Frontend.Cms.validate_page(title, description)

    @exception()
    def test_search_documentation_title(self):
        title, description = DB.Cms.create_page()
        logger.debug("About to login with EL and add VFC")
        users = [
            self.user_content['el_email'],
            self.user_content['pr_email'],
            Constants.Users.AdminRO.EMAIL,
            Constants.Users.Admin.EMAIL,
            self.user_content['email']]
        for user in users:
            logger.debug("Login with user " + user)
            Frontend.User.relogin(
                user,
                Constants.Default.Password.TEXT,
                "documentation")
            Frontend.Cms.search_documentation_title(title, self.user_content)

    @exception()
    def test_search_documentation_content(self):
        title, description = DB.Cms.create_page()
        Frontend.Cms.search_documentation_content(title, description)

    '''
    Announcement toast should stay for 2 days after it was published
    '''
    @exception()
    def test_validate_expired_post_Announcement(self):
        title, description = DB.Cms.create_announcement()
        Frontend.User.logout()
        Frontend.User.login(
            self.user_content['email'], Constants.Default.Password.TEXT)
        Frontend.Cms.validate_expired_post_Announcement(
            self.user_content['email'], title, description)

    '''
    Announcement toast should stay was published if the user closes the message
    '''
    @exception()
    def test_Announcement_validate_toast(self):
        title, description = DB.Cms.create_announcement()
        Frontend.User.relogin(
            self.user_content['email'],
            Constants.Default.Password.TEXT,
            Constants.Toast.CMS_ID)
        Frontend.Cms.announcement_validate_toast(
            title, description, self.user_content)

    '''
    Announcement toast is shown for users even after the entry has disappeared
     from the widget on the Dashboard
    '''
    @exception()
    def test_validate_5_last_Announcement_displayed(self):
        listOfTitleAnDescriptions = DB.Cms.create_announcements(6)
        Frontend.User.relogin(
            self.user_content['email'],
            Constants.Default.Password.TEXT)
        last_title = listOfTitleAnDescriptions[len(
            listOfTitleAnDescriptions) - 1][0]
        Frontend.Cms.validate_5_last_announcement_displayed(
            listOfTitleAnDescriptions, self.user_content, last_title)

    @exception()
    def test_insert_grandchild_page(self):
        parent_title, parent_description = DB.Cms.create_page()
        parent_id = DB.Cms.get_last_inserted_page_id()
        child_title, child_description = DB.Cms.create_page(parent_id)
        child_id = DB.Cms.get_last_inserted_page_id()
        grand_child_title, grand_child_description = DB.Cms.create_page(
            child_id)
        Frontend.Cms.validate_grandchild_page(
            parent_title,
            child_title,
            grand_child_title,
            grand_child_description)
