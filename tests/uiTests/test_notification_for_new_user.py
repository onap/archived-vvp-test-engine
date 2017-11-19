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

from iceci.decorator.exception_decor import exception
from services.constants import Constants
from services.logging_service import LoggingServiceFactory
from services.types import API, DB, Frontend
from tests.uiTests.test_ui_base import TestUiBase


logger = LoggingServiceFactory.get_logger()


class TestNotificationForNewUser(TestUiBase):
    user_content = None

    @classmethod
    def setUpClass(cls):
        super(TestNotificationForNewUser, cls).setUpClass()

        cls.user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)

    @exception()
    def test_notification_page_sanity(self):
        Frontend.User.login(
            self.user_content['email'], Constants.Default.Password.TEXT)
        logger.debug("Go to notifications page")
        Frontend.User.go_to_notifications()
        logger.debug("Remove one notification")
        notificationIDs = DB.User.get_notification_id_by_email(
            self.user_content['email'])
        Frontend.User.delete_notification(notificationIDs[0])

    @exception()
    def test_validate_notifications(self):
        user_content = API.VirtualFunction.create_engagement()
        user_content['session_token'] = "token " + \
            API.User.login_user(user_content['el_email'])
        Frontend.User.relogin(
            user_content['email'], Constants.Default.Password.TEXT)
        Frontend.User.go_to_notifications()
        notificationIDs = DB.User.get_notification_id_by_email(
            user_content['email'])
        notification_list = [
            user_content['full_name'] +
            " joined " +
            user_content['vfName'],
            user_content['el_name'] +
            " joined " +
            user_content['vfName'],
            user_content['pr_name'] +
            " joined " +
            user_content['vfName']]
        Frontend.User.validate_notifications(
            notificationIDs, notification_list)

    @exception()
    def test_num_of_notifications_for_user(self):
        Frontend.User.login(
            self.user_content['el_email'], Constants.Default.Password.TEXT)
        notifications_num = DB.User.get_not_seen_notifications_number_by_email(
            self.user_content['el_email'])
        Frontend.User.compare_notifications_count_for_user(notifications_num)

    @exception()
    def test_zero_notifications_for_user(self):
        Frontend.User.login(
            self.user_content['pr_email'], Constants.Default.Password.TEXT)
        Frontend.User.go_to_notifications()
        notifications_num = DB.User.get_not_seen_notifications_number_by_email(
            self.user_content['pr_email'], is_negative=True)
        assert(notifications_num == "0")
        Frontend.User.check_notification_number_is_not_presented()
