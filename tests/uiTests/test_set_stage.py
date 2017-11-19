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


class TestSetStage(TestUiBase):
    @exception()
    def test_set_eng_stages(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        Frontend.User.login(
            user_content['el_email'],
            Constants.Default.Password.TEXT)
        stages = [
            Constants.EngagementStages.INTAKE,
            Constants.EngagementStages.ACTIVE,
            Constants.EngagementStages.VALIDATED,
            Constants.EngagementStages.COMPLETED]
        Frontend.Overview.click_on_vf(user_content)
        for idx, stage in enumerate(stages[:-1]):
            next_stage = stages[(idx + 1) % len(stages)]
            Frontend.Overview.check_stage_next_steps(
                stage, user_content['engagement_uuid'])
            Frontend.Overview.change_engagement_stage(next_stage)
            Frontend.General.refresh()
            if Frontend.Overview.check_stage_notifications(
                    next_stage) is False:
                raise Exception(
                    "Activity log for set stage wasn't found for stage %s" %
                    next_stage)

    @exception()
    def test_set_eng_stages_via_pr_reviewer(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        Frontend.User.login(
            user_content['pr_email'],
            Constants.Default.Password.TEXT)
        stages = [
            Constants.EngagementStages.INTAKE,
            Constants.EngagementStages.ACTIVE,
            Constants.EngagementStages.VALIDATED,
            Constants.EngagementStages.COMPLETED]
        Frontend.Overview.click_on_vf(user_content)
        for idx, stage in enumerate(stages[:-1]):
            next_stage = stages[(idx + 1) % len(stages)]
            Frontend.Overview.check_stage_next_steps(
                stage, user_content['engagement_uuid'])
            Frontend.Overview.change_engagement_stage(next_stage)
            Frontend.General.refresh()
            if Frontend.Overview.check_stage_notifications(
                    next_stage) is False:
                raise Exception(
                    "Activity log for set stage wasn't found for stage %s" %
                    next_stage)

    @exception()
    def test_admin_ro_set_stage_negative(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        stages = [
            Constants.EngagementStages.INTAKE,
            Constants.EngagementStages.ACTIVE,
            Constants.EngagementStages.VALIDATED,
            Constants.EngagementStages.COMPLETED]
        Frontend.User.login(
            Constants.Users.AdminRO.EMAIL,
            Constants.Default.Password.TEXT)
        Frontend.Dashboard.statuses_search_vf(
            user_content['engagement_manual_id'],
            user_content['vfName'])
        for idx, stage in enumerate(stages[:-1]):
            next_stage = stages[(idx + 1) % len(stages)]
            Frontend.Overview.change_engagement_stage(
                next_stage, is_negative=True)
            logger.debug("Admin_ro failed to change stage to %s" % stage)

    @exception()
    def test_set_eng_stages_negative(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        stages = [
            Constants.EngagementStages.INTAKE,
            Constants.EngagementStages.ACTIVE,
            Constants.EngagementStages.VALIDATED,
            Constants.EngagementStages.COMPLETED]
        Frontend.User.login(
            user_content['email'],
            Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        for idx, stage in enumerate(stages[:-1]):
            next_stage = stages[(idx + 1) % len(stages)]
            Frontend.Overview.change_engagement_stage(
                next_stage, is_negative=True)
            logger.debug(
                "User %s failed to change stage to %s" %
                (user_content['email'], stage))

    @exception()
    def test_set_eng_stages_negative_via_pr(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)
        stages = [
            Constants.EngagementStages.INTAKE,
            Constants.EngagementStages.ACTIVE,
            Constants.EngagementStages.VALIDATED,
            Constants.EngagementStages.COMPLETED]
        Frontend.User.login(
            user_content['pr_email'],
            Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(user_content)
        for idx, stage in enumerate(stages[:-1]):
            next_stage = stages[(idx + 1) % len(stages)]
            Frontend.Overview.change_engagement_stage(
                next_stage, is_negative=False)
            logger.debug(
                "User %s failed to change stage to %s" %
                (user_content['pr_email'], stage))
