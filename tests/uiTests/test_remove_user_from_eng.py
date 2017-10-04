 
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
from services.constants import Constants, ServiceProvider
from services.logging_service import LoggingServiceFactory
from services.types import API, Frontend
from tests.uiTests.test_ui_base import TestUiBase


logger = LoggingServiceFactory.get_logger()


class TestRemoveUserFromEng(TestUiBase):
    user_content = None

    @classmethod
    def setUpClass(cls):
        super(TestRemoveUserFromEng, cls).setUpClass()

        cls.user_content = API.VirtualFunction.create_engagement(wait_for_gitlab=False)
    
    @exception()
    def test_remove_user_with_admin(self):
        second_user_email, invite_token, invite_url = API.VirtualFunction.invite_team_member(self.user_content)
        invited_user = API.User.signup_invited_user(ServiceProvider.MainServiceProvider, second_user_email, invite_token, invite_url,
                                                    self.user_content)
        Frontend.User.login(Constants.Users.Admin.EMAIL, Constants.Default.Password.TEXT)
        Frontend.Dashboard.statuses_search_vf(self.user_content['engagement_manual_id'], self.user_content['vfName'])
        Frontend.Overview.remove_user_from_eng_team(invited_user["full_name"])
    
    
    @exception()
    def test_remove_user_with_reviewer(self):
        second_user_email, invite_token, invite_url = API.VirtualFunction.invite_team_member(self.user_content)
        invited_user = API.User.signup_invited_user(ServiceProvider.MainServiceProvider, second_user_email, invite_token, invite_url,
                                                    self.user_content)
        Frontend.User.login(self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(self.user_content)
        Frontend.Overview.remove_user_from_eng_team(invited_user["full_name"])
    
    
    @exception()
    def test_remove_user_with_peer_reviewer(self):
        second_user_email, invite_token, invite_url = API.VirtualFunction.invite_team_member(self.user_content)
        invited_user = API.User.signup_invited_user(ServiceProvider.MainServiceProvider, second_user_email, invite_token, invite_url,
                                                    self.user_content)
        Frontend.User.login(self.user_content['pr_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(self.user_content)
        Frontend.Overview.remove_user_from_eng_team(invited_user["full_name"])
    
    
    @exception()
    def test_negative_remove_reviewer_from_eng(self):
        Frontend.User.login(self.user_content["pr_email"], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(self.user_content)
        Frontend.Overview.remove_user_from_eng_team(self.user_content["el_name"], True)
        
    
    @exception()
    def test_negative_remove_peer_reviewer_from_eng(self):
        Frontend.User.login(self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(self.user_content)
        Frontend.Overview.remove_user_from_eng_team(self.user_content["pr_name"], True)
        
    
    @exception()
    def test_negative_remove_creator_from_eng(self):
        Frontend.User.login(self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(self.user_content)
        Frontend.Overview.remove_user_from_eng_team(self.user_content["full_name"], True)
        
    
    @exception()
    def test_negative_remove_contact_user_from_eng(self):
        second_user_email, invite_token, invite_url = API.VirtualFunction.add_contact(self.user_content)
        invited_user = API.User.signup_invited_user(ServiceProvider.MainServiceProvider, second_user_email, invite_token, invite_url,
                                                    self.user_content, "true", True)
        Frontend.User.login(second_user_email, Constants.Default.Password.TEXT)
        Frontend.Overview.click_on_vf(self.user_content)
        Frontend.Overview.remove_user_from_eng_team(invited_user["full_name"], True)
