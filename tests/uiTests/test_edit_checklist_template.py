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
from services.types import Frontend, DB
from tests.uiTests.test_ui_base import TestUiBase


logger = LoggingServiceFactory.get_logger()


class TestChecklistTemplate(TestUiBase):
    one_web_driver_enabled = False

    @classmethod
    def setUpClass(cls):
        super(TestChecklistTemplate, cls).setUpClass()
        DB.Checklist.create_editing_cl_template_if_not_exist()

    @exception()
    def test_save_checklist_template_without_changes(self):
        Frontend.ChecklistTemplate.basic_admin_navigation()
        Frontend.ChecklistTemplate.click_on_template_name_on_navigation(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT,
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT)
        Frontend.ChecklistTemplate.save_with_no_changes()

    @exception()
    def test_discard_checklist_template_with_changes(self):
        Frontend.ChecklistTemplate.basic_admin_navigation()
        Frontend.ChecklistTemplate.click_on_template_name_on_navigation(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT,
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT)
        Frontend.ChecklistTemplate.discard_checklist_after_modification()

    @exception()
    def test_save_checklist_template_after_edit_section_name(self):
        Frontend.ChecklistTemplate.basic_admin_navigation()
        Frontend.ChecklistTemplate.click_on_template_name_on_navigation(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT,
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT)
        Frontend.ChecklistTemplate.edit_template_and_save()

    @exception()
    def test_save_checklist_template_after_lineitem_delete(self):
        Frontend.ChecklistTemplate.basic_admin_navigation()
        Frontend.ChecklistTemplate.click_on_template_name_on_navigation(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT,
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT)
        Frontend.ChecklistTemplate.del_lineitem_and_save()

    @exception()
    def test_save_checklist_template_after_lineitem_added(self):
        Frontend.ChecklistTemplate.basic_admin_navigation()
        Frontend.ChecklistTemplate.click_on_template_name_on_navigation(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT,
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT)
        Frontend.ChecklistTemplate.add_lineitem_and_save()

    @exception()
    def test_lineitem_added_and_verify_cl_changed(self):
        Frontend.ChecklistTemplate.basic_admin_navigation()
        Frontend.ChecklistTemplate.click_on_template_name_on_navigation(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT,
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT)
        Frontend.ChecklistTemplate.add_lineitem_and_check_db()

    @exception()
    def test_save_checklist_template_after_edit_lineitem(self):
        Frontend.ChecklistTemplate.basic_admin_navigation()
        Frontend.ChecklistTemplate.click_on_template_name_on_navigation(
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT,
            Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT)
        Frontend.ChecklistTemplate.edit_description_lineitem_and_save()
