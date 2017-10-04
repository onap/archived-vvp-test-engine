 
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
import uuid

from iceci.decorator.exception_decor import exception
from services.constants import Constants
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.session import session
from services.types import API, DB, Frontend
from tests.uiTests.test_ui_base import TestUiBase


logger = LoggingServiceFactory.get_logger()


class TestDetailedView(TestUiBase):
    '''
    Name: test_detailed_view
    Steps:
        Create new User via SignUp request-->Login with This One--> build "activationUrl"-->
        Validation of successful activate-->
        close Wizard --> Logout-->login-->Open Wizard--> fill all fields in all Tab's(4)-->
        build inviteURL from email--> reopen browser with inviteURL-->
        Validate fields filled's in SignUp form 
    '''

    user_content = None

    @classmethod
    def setUpClass(cls):
        super(TestDetailedView, cls).setUpClass()
        cls.user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=False)

    @exception()
    def test_detailed_view(self):
        Frontend.User.login(
            self.user_content['el_email'], Constants.Default.Password.TEXT)
        Frontend.DetailedView.search_vf_and_go_to_detailed_view(self.user_content['engagement_manual_id'],
                                                                self.user_content['vfName'])
        Frontend.DetailedView.validate_all_titles_on_dv_form()
        logger.debug("Add Deployment Target")
        Frontend.DetailedView.add_deployment_target(self.user_content)
        logger.debug("Add VFC no.1")
        Frontend.DetailedView.add_vfcs("djoni", "loka")
        Frontend.DetailedView.remove_vfc(self.user_content)

    @exception()
    def test_update_aic_version(self):
        Frontend.User.login(
            self.user_content['email'], Constants.Default.Password.TEXT)
        Frontend.DetailedView.search_vf_and_go_to_detailed_view(
            self.user_content['engagement_manual_id'], self.user_content['vfName'])
        Frontend.DetailedView.update_aic_version()
        Frontend.DetailedView.validate_aic_version()

    @exception()
    def test_update_vf_version(self):
        Frontend.User.login(
            self.user_content['email'], Constants.Default.Password.TEXT)
        Frontend.DetailedView.search_vf_and_go_to_detailed_view(
            self.user_content['engagement_manual_id'], self.user_content['vfName'])
        newVFVersionName = Frontend.DetailedView.update_vf_version()
        Frontend.DetailedView.validate_vf_version(newVFVersionName)

    '''
    Add new ECOMP release to DB, go to detailed view and change ECOMP release and AIC version.
    Verify changes are saved and presented in UI.
    '''
    @exception()
    def test_edit_ecomp_release(self):
        try:
            EcompUuid = uuid.uuid4()
            EcompName = Helper.rand_string("randomString")
            DB.VirtualFunction.insert_ecomp_release(EcompUuid, EcompName)
            Frontend.User.login(
                self.user_content['email'], Constants.Default.Password.TEXT)
            Frontend.DetailedView.search_vf_and_go_to_detailed_view(
                self.user_content['engagement_manual_id'], self.user_content['vfName'])
            Frontend.DetailedView.update_ecomp_release(EcompName)
            Frontend.DetailedView.validate_ecomp_version()
        finally:
            DB.VirtualFunction.delete_ecomp_release(EcompUuid, EcompName)

    @exception()
    def test_role_for_deployment_targets(self):
        users = [self.user_content['pr_email'],
                 self.user_content['el_email'], Constants.Users.Admin.EMAIL]
        Frontend.DetailedView.validate_deployment_targets(
            self.user_content, users)

    @exception()
    def test_add_and_remove_deployment_targets(self):
        users = [self.user_content['el_email'], Constants.Users.Admin.EMAIL]
        Frontend.DetailedView.add_remove_deployment_targets(
            self.user_content, users)

    @exception()
    def test_negative_role_for_deployment_targets(self):
        users = [self.user_content['email'], Constants.Users.AdminRO.EMAIL]
        Frontend.DetailedView.validate_negative_role_for_deployment_targets(
            self.user_content, users)

    @exception()
    def test_change_target_lab_entry(self):
        Frontend.User.login(Constants.Users.Admin.EMAIL,
                            Constants.Default.Password.TEXT)
        Frontend.DetailedView.search_vf_and_go_to_detailed_view(
            self.user_content['engagement_manual_id'], self.user_content['vfName'])
        date = Frontend.DetailedView.update_target_lab_entry()
        Frontend.DetailedView.validate_target_lab_entry(date)

    @exception()
    def test_change_target_lab_entry_via_standard_user(self):
        Frontend.User.login(
            self.user_content['email'], Constants.Default.Password.TEXT)
        Frontend.DetailedView.search_vf_and_go_to_detailed_view(
            self.user_content['engagement_manual_id'], self.user_content['vfName'])
        date = Frontend.DetailedView.update_target_lab_entry()
        Frontend.DetailedView.validate_target_lab_entry(date)

    @exception()
    def test_aic_dropdown_ordering(self):
        new_aic_version = None
        try:
            DB.VirtualFunction.change_aic_version_weight(10, 0)
            new_aic_version = DB.VirtualFunction.insert_aic_version()
            Frontend.User.login(
                self.user_content['el_email'], Constants.Default.Password.TEXT)
            Frontend.DetailedView.search_vf_and_go_to_detailed_view(self.user_content['engagement_manual_id'],
                                                                    self.user_content['vfName'])
            Frontend.DetailedView.click_on_update_aic_version()
            Helper.internal_assert(Frontend.General.get_meta_order_of_element(
                Constants.Dashboard.DetailedView.AIC.Dropdown.UniversalVersion.ID % new_aic_version['version']), 0)
        finally:
            if new_aic_version:
                DB.VirtualFunction.delete_aic_version(new_aic_version['uuid'])
            DB.VirtualFunction.change_aic_version_weight(0, 10)

    @exception()
    def test_ecomp_dropdown_ordering(self):
        new_ecomp_release = None
        try:
            new_ecomp_release = {
                "uuid": uuid.uuid4(), "name": Helper.rand_string()}
            DB.VirtualFunction.change_ecomp_release_weight(10, 0)
            DB.VirtualFunction.insert_ecomp_release(
                new_ecomp_release['uuid'], new_ecomp_release['name'])
            Frontend.User.login(
                self.user_content['el_email'], Constants.Default.Password.TEXT)
            Frontend.DetailedView.search_vf_and_go_to_detailed_view(
                self.user_content['engagement_manual_id'], self.user_content['vfName'])
            Frontend.DetailedView.click_on_update_ecomp_release()
            Helper.internal_assert(Frontend.General.get_meta_order_of_element(
                Constants.Dashboard.DetailedView.ECOMP.Dropdown.UniversalRelease.ID % new_ecomp_release['name']), 0)
        finally:
            if new_ecomp_release:
                DB.VirtualFunction.delete_ecomp_release(
                    new_ecomp_release['uuid'], new_ecomp_release['name'])
            DB.VirtualFunction.change_ecomp_release_weight(0, 10)

    @exception()
    def test_retire_aic_version(self):
        new_aic_version = None
        try:
            new_aic_version = DB.VirtualFunction.insert_aic_version("FALSE")
            Frontend.User.login(
                self.user_content['el_email'], Constants.Default.Password.TEXT)
            Frontend.DetailedView.search_vf_and_go_to_detailed_view(
                self.user_content['engagement_manual_id'], self.user_content['vfName'])
            Frontend.DetailedView.click_on_update_aic_version()
            session.run_negative(lambda: Frontend.General.get_meta_order_of_element(
                Constants.Dashboard.DetailedView.AIC.Dropdown.UniversalVersion.ID % new_aic_version['version']),
                "New AIC version was found in dropdown.")
        finally:
            if new_aic_version:
                DB.VirtualFunction.delete_aic_version(new_aic_version['uuid'])

    @exception()
    def test_retire_ecomp_release(self):
        new_ecomp_release = None
        try:
            new_ecomp_release = {
                "uuid": uuid.uuid4(), "name": Helper.rand_string(), "ui_visibility": "FALSE"}
            DB.VirtualFunction.insert_ecomp_release(
                new_ecomp_release['uuid'], new_ecomp_release['name'], new_ecomp_release['ui_visibility'])
            Frontend.User.login(
                self.user_content['el_email'], Constants.Default.Password.TEXT)
            Frontend.DetailedView.search_vf_and_go_to_detailed_view(
                self.user_content['engagement_manual_id'], self.user_content['vfName'])
            Frontend.DetailedView.click_on_update_ecomp_release()
            session.run_negative(lambda: Frontend.General.get_meta_order_of_element(
                Constants.Dashboard.DetailedView.ECOMP.Dropdown.UniversalRelease.ID % new_ecomp_release['name']), "New ECOMP release was found in dropdown.")
        finally:
            if new_ecomp_release:
                DB.VirtualFunction.delete_ecomp_release(
                    new_ecomp_release['uuid'], new_ecomp_release['name'])

    @exception()
    def test_retire_selected_aic_version(self):
        old_aic_version_uuid = new_aic_version = None
        try:
            old_aic_version_uuid = DB.VirtualFunction.select_aic_version_uuid(
                self.user_content['target_aic'])
            new_aic_version = DB.VirtualFunction.insert_aic_version("FALSE")
            self.user_content['session_token'] = "token " + \
                API.User.login_user(self.user_content['el_email'])
            API.VirtualFunction.update_aic_version(
                self.user_content['engagement_uuid'], new_aic_version['uuid'], self.user_content['session_token'])
            Frontend.User.login(
                self.user_content['el_email'], Constants.Default.Password.TEXT)
            Frontend.DetailedView.search_vf_and_go_to_detailed_view(
                self.user_content['engagement_manual_id'], self.user_content['vfName'])
            Frontend.DetailedView.compare_aic_selected_version(
                new_aic_version['version'])
            Frontend.DetailedView.click_on_update_aic_version()
            Frontend.DetailedView.validate_deprecated_aic_version_in_dropdown(
                new_aic_version['version'])
        finally:
            if old_aic_version_uuid:
                API.VirtualFunction.update_aic_version(
                    self.user_content['engagement_uuid'], old_aic_version_uuid, self.user_content['session_token'])
                if new_aic_version:
                    DB.VirtualFunction.delete_aic_version(
                        new_aic_version['uuid'])

    @exception()
    def test_retire_selected_ecomp_release(self):
        old_ecomp_release_uuid = new_ecomp_release = None
        try:
            old_ecomp_release_uuid = DB.VirtualFunction.select_ecomp_release_uuid(
                self.user_content['ecomp_release'])
            new_ecomp_release = {"uuid": str(
                uuid.uuid4()), "name": Helper.rand_string(), "ui_visibility": "FALSE"}
            DB.VirtualFunction.insert_ecomp_release(
                new_ecomp_release['uuid'], new_ecomp_release['name'], new_ecomp_release['ui_visibility'])
            self.user_content['session_token'] = "token " + \
                API.User.login_user(self.user_content['el_email'])
            API.VirtualFunction.update_ecomp_release(
                self.user_content['engagement_uuid'], new_ecomp_release['uuid'], self.user_content['session_token'])
            Frontend.User.login(
                self.user_content['el_email'], Constants.Default.Password.TEXT)
            Frontend.DetailedView.search_vf_and_go_to_detailed_view(
                self.user_content['engagement_manual_id'], self.user_content['vfName'])
            Frontend.DetailedView.compare_selected_ecomp_release(
                new_ecomp_release['name'])
            Frontend.DetailedView.click_on_update_ecomp_release()
            Frontend.DetailedView.validate_deprecated_ecomp_release_in_dropdown(
                new_ecomp_release['name'])
        finally:
            if self.user_content and old_ecomp_release_uuid:
                API.VirtualFunction.update_ecomp_release(
                    self.user_content['engagement_uuid'], old_ecomp_release_uuid, self.user_content['session_token'])
                DB.VirtualFunction.delete_ecomp_release(
                    new_ecomp_release['uuid'], new_ecomp_release['name'])
