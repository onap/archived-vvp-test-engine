
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
'''
Created on 25 Jul 2017
'''
from iceci.decorator.exception_decor import exception
from services.constants import Constants
from services.logging_service import LoggingServiceFactory
from services.types import API, Frontend, DB
from tests.uiTests.test_ui_base import TestUiBase

logger = LoggingServiceFactory.get_logger()


class TestOverview(TestUiBase):

    @exception()
    def test_engagement_validation_details_update_when_cl_closed(self):
        user_content = API.VirtualFunction.create_engagement()
        cl_name = Constants.Dashboard.Checklist.ChecklistDefaultNames.AIC_INSTANTIATION
        DB.Checklist.state_changed(
            "name", cl_name, Constants.ChecklistStates.Review.TEXT)
        cl_uuid = DB.Checklist.get_recent_checklist_uuid(cl_name)[0]
        vf_staff_emails = [user_content['el_email'], user_content[
            'pr_email'], Constants.Users.Admin.EMAIL]
        API.Checklist.move_cl_to_closed(cl_uuid, vf_staff_emails)
        Frontend.User.login(
            user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        Frontend.Overview.change_engagement_stage(
            Constants.EngagementStages.ACTIVE)
        Frontend.Overview.verify_validation_dates()
