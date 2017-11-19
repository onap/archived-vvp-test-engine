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
from services.session import session
from services.types import API, DB, Frontend
from tests.uiTests.test_ui_base import TestUiBase


logger = LoggingServiceFactory.get_logger()


class TestDashboardFeature(TestUiBase):
    user_content = None

    @classmethod
    def setUpClass(cls):
        super(TestDashboardFeature, cls).setUpClass()

        cls.user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)

    @exception()
    def test_validate_filtering_by_stage_intake(self):
        Frontend.User.login(
            self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Dashboard.validate_filtering_by_stage(
            self.user_content, Constants.EngagementStages.INTAKE)

    @exception()
    def test_validate_filtering_by_stage_active(self):
        Frontend.User.login(
            self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Dashboard.validate_filtering_by_stage_with_page_ids(
            self.user_content, Constants.EngagementStages.ACTIVE)

    @exception()
    def test_validate_filtering_by_stage_validated(self):
        query = "UPDATE ice_engagement SET engagement_stage='Validated'" \
                " WHERE engagement_manual_id ='" + \
            str(self.user_content['engagement_manual_id']) + "';"
        DB.General.update_by_query(query)
        Frontend.User.login(
            self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Dashboard.validate_filtering_by_stage_with_page_ids(
            self.user_content, Constants.EngagementStages.VALIDATED)

    @exception()
    def test_validate_filtering_by_stage_completed(self):
        Frontend.User.login(
            self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Dashboard.validate_filtering_by_stage_with_page_ids(
            self.user_content, Constants.EngagementStages.COMPLETED)

    @exception()
    def test_validate_filtering_by_stage_all(self):
        Frontend.User.login(
            self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Dashboard.validate_filtering_by_stage_with_page_ids(
            self.user_content, Constants.EngagementStages.ALL)

    @exception()
    def test_validate_statistics_by_stages(self):
        Frontend.User.login(
            self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Dashboard.validate_statistics_by_stages(self.user_content)

    @exception()
    def test_assigned_next_steps(self):
        Frontend.User.login(
            self.user_content['email'], Constants.Default.Password.TEXT)
        Frontend.User.assigned_one_NS_to_user(self.user_content)
        Frontend.Dashboard.check_if_the_eng_of_NS_is_the_correct_one(
            self.user_content)
        Frontend.Dashboard.check_if_creator_of_NS_is_the_EL(self.user_content)
        Frontend.Overview.go_to_eng_overview_by_clicking_on_the_created_NS(
            self.user_content)

    @exception()
    def test_search_engagement(self):
        Frontend.User.login(
            self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.DetailedView.search_vf_and_go_to_detailed_view(
            self.user_content['engagement_manual_id'],
            self.user_content['vfName'])
        vfcName = Frontend.DetailedView.add_vfc()
        users = [self.user_content['el_email'], self.user_content['pr_email'],
                 self.user_content['email'],
                 Constants.Users.Admin.EMAIL, Constants.Users.AdminRO.EMAIL]
        session.wait_until_retires = 20
        Frontend.Dashboard.search_in_dashboard(
            self.user_content, vfcName, users)
        session.wait_until_retires = session.positive_wait_until_retires

    @exception()
    def test_validate_statistics_modal_appears_for_peer_re(self):
        Frontend.User.login(
            self.user_content['pr_email'], Constants.Default.Password.TEXT)
        Frontend.Dashboard.click_on_dashboard_and_validate_statistics(
            is_negative=False)

    @exception()
    def test_validate_statistics_modal_appears_for_el(self):
        Frontend.User.login(
            self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Dashboard.click_on_dashboard_and_validate_statistics(
            is_negative=False)

    @exception()
    def test_validate_statistics_modal_appears_for_standart_user(self):
        Frontend.User.login(
            self.user_content['email'], Constants.Default.Password.TEXT)
        Frontend.Dashboard.click_on_dashboard_and_validate_statistics(
            is_negative=True)

    @exception()
    def test_validate_statistics_modal_appears_for_admin(self):
        Frontend.User.login(
            Constants.Users.Admin.EMAIL, Constants.Default.Password.TEXT)
        Frontend.Dashboard.click_on_dashboard_and_validate_statistics(
            is_negative=False)

    @exception()
    def test_validate_statistics_modal_appears_for_admin_ro(self):
        Frontend.User.login(
            Constants.Users.AdminRO.EMAIL, Constants.Default.Password.TEXT)
        Frontend.Dashboard.click_on_dashboard_and_validate_statistics(
            is_negative=False)
