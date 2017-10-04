 
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
from services.types import API, Frontend
from tests.uiTests.test_ui_base import TestUiBase


logger = LoggingServiceFactory.get_logger()


class TestProgressBar(TestUiBase):
    user_content = None

    @exception()
    def test_progress_bar_ui(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        Frontend.User.login(
            user_content['el_email'], Constants.Default.Password.TEXT)
        logger.debug("Validate and check progress with engagement lead")
        Frontend.Overview.click_on_vf(user_content)
        Frontend.Overview.change_engagement_stage(
            Constants.EngagementStages.ACTIVE)
        Frontend.Overview.check_progress(
            Constants.Dashboard.Overview.Progress.Percent.TEXT)
        Frontend.Overview.set_progress(
            Constants.Dashboard.Overview.Progress.Change.NUMBER)
        Frontend.Overview.check_progress(
            Constants.Dashboard.Overview.Progress.Change.TEXT)
        logger.debug("Validate progress with standard user")
        Frontend.User.relogin(
            user_content['email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        Frontend.Overview.check_progress(
            Constants.Dashboard.Overview.Progress.Change.TEXT)

    @exception()
    def test_vnf_version_with_value_appears_in_overview_progress_bar(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        Frontend.User.login(
            user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        Frontend.Overview.change_engagement_stage(
            Constants.EngagementStages.ACTIVE)
        Frontend.Overview.check_vnf_version(user_content['vnf_version'])

    @exception()
    def test_vnf_version_with_value_appears_in_dashboard_progress_bar(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        Frontend.User.login(
            user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        Frontend.Overview.change_engagement_stage(
            Constants.EngagementStages.ACTIVE)
        Frontend.Dashboard.search_by_vf(user_content)
        Frontend.Dashboard.check_vnf_version(user_content)
