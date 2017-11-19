
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
from datetime import datetime

from selenium.webdriver.support.ui import Select

from services.constants import Constants, ServiceProvider
from services.frontend.base_actions.click import Click
from services.frontend.base_actions.enter import Enter
from services.frontend.base_actions.wait import Wait
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()


class FEWizard:

    E2Edate = None

    @staticmethod
    def add_vf():
        try:
            logger.debug("Tab Add Virtual Functions")
            Wait.text_by_css(
                Constants.Dashboard.Wizard.Title.CSS,
                Constants.Dashboard.Wizard.AddVF.Title.TEXT,
                wait_for_page=True)
            vfName = "newVF" + Helper.rand_string("randomString")
            vfVersion = "newVFVersion" + \
                Helper.rand_string(
                    "randomNumber") + Helper.rand_string("randomString")
            Enter.text_by_name("virtualFunction", vfName)
            Enter.text_by_name("VFversion", vfVersion, wait_for_page=True)
            FEWizard.date_picker_wizard()
            Select(session.ice_driver.find_element_by_id(
                Constants.Dashboard.Wizard.AddVF.AIC_Version.TEXT
            )).select_by_visible_text("AIC 3.5")
            Select(session.ice_driver.find_element_by_id(
                Constants.Dashboard.Wizard.AddVF.ECOMP_Release.TEXT
            )).select_by_visible_text("Unknown")
            session.E2Edate = FEWizard.get_lab_entry_date()
            Click.css(Constants.SubmitButton.CSS, wait_for_page=True)
            Wait.page_has_loaded()
            Wait.name_to_dissappear("Add Virtual Function")
            return vfName
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "Failed to add a Virtual Function via modal window. " +\
                "Exception " +\
                str(e)
            raise Exception(errorMsg)

    @staticmethod
    def get_lab_entry_date():
        E2Edate = session.ice_driver.find_element_by_id(
            "add-vf-hidden-target-lab-date").get_attribute("value")
        return str(E2Edate)

    @staticmethod
    def add_vendor_contact():
        logger.debug("Tab Add Vendor Contact")
        Wait.text_by_css(
            Constants.Dashboard.Wizard.Title.CSS,
            Constants.Dashboard.Wizard.AddVendorContact.Title.TEXT,
            wait_for_page=True)
        Select(session.ice_driver.find_element_by_name(
            "company")).select_by_visible_text("Ericsson")
        fullname = Helper.rand_string(
            "randomString") + Helper.rand_string("randomString")
        Enter.text_by_name("fullname", fullname)
        email = Helper.rand_string("randomString") + "@ericson.com"
        Enter.text_by_name("email", email)
        phone = "201" + Helper.rand_string("randomNumber", 6)
        Enter.text_by_name("phone", phone)
        Click.css(Constants.SubmitButton.CSS, wait_for_page=True)
        Wait.name_to_dissappear("Add Vendor Contact", wait_for_page=True)
        vendor = {"company": "Ericsson", "full_name": fullname,
                  "email": email, "phone": phone}
        return vendor

    @staticmethod
    def add_service_provider_internal():
        logger.debug(
            "Tab Add " + ServiceProvider.MainServiceProvider + " Sponsor")
        Wait.text_by_css(
            Constants.Dashboard.Wizard.Title.CSS,
            "Add " +
            ServiceProvider.MainServiceProvider +
            " Sponsor")
        fullname = Helper.rand_string(
            "randomString") + Helper.rand_string("randomString")
        Enter.text_by_name("fullname", fullname)
        email = Helper.rand_string(
            "randomString") + "@" + ServiceProvider.email
        Enter.text_by_name("email", email)
        phone = "201" + Helper.rand_string("randomNumber", 6)
        logger.debug(phone)
        Enter.text_by_name("phone", phone)
        Click.css(Constants.SubmitButton.CSS)
        Wait.name_to_dissappear("Add AT&T Sponsor")
        sponsor = {"company": ServiceProvider.MainServiceProvider,
                   "full_name": fullname, "email": email, "phone": phone}
        return sponsor

    @staticmethod
    def invite_team_members(email):
        try:
            logger.debug("Tab Invite Team Members")
            Wait.text_by_name(
                Constants.Dashboard.Wizard.InviteTeamMembers.Title.NAME,
                Constants.Dashboard.Wizard.InviteTeamMembers.Title.TEXT)
            Enter.text_by_name("email", email)
            Wait.text_by_css(
                Constants.SubmitButton.CSS,
                Constants.Dashboard.Wizard.InviteTeamMembers.Button.TEXT)
            Click.css(Constants.SubmitButton.CSS)
            Wait.name_to_dissappear(
                Constants.Dashboard.Wizard.InviteTeamMembers.Title.NAME)
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "FAILED in Tab Invite Team Members. Exception = %s" % e
            raise Exception(errorMsg)

    @staticmethod
    def add_ssh_key(is_negative=False):
        logger.debug("About to add an SSH Key in modal window")
        try:  # Add SSH Key from modal window and return key value.
            Wait.text_by_name(Constants.Dashboard.Wizard.AddSSHKey.Title.NAME,
                              Constants.Dashboard.Wizard.AddSSHKey.Title.TEXT)
            # Generate an SSH Public Key.
            sshKey = Helper.generate_sshpub_key()
            if is_negative:
                sshKey = sshKey[8:]
            Enter.text_by_name("key", sshKey)

            # Check that the submit button exists.
            Wait.text_by_css(
                Constants.SubmitButton.CSS,
                Constants.Dashboard.Wizard.AddSSHKey.Title.TEXT)

            Click.css(Constants.SubmitButton.CSS)  # Click on submit button.
            if is_negative:
                Wait.text_by_id(
                    Constants.Toast.ID,
                    Constants.Dashboard.Avatar.Account
                    .SSHKey.UpdateFailed.TEXT)
            else:
                Wait.name_to_dissappear(
                    Constants.Dashboard.Wizard.AddSSHKey.Title.NAME)
                logger.debug("SSH Key added via modal window.")
            return sshKey
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "Failed to add an SSH Key in " +\
                "the modal window. Exception=" + \
                str(e)
            raise Exception(errorMsg)

    @staticmethod
    def invite_team_members_modal(email, wait_modal_to_disappear=True):
        try:
            Click.id(
                Constants.Dashboard.Overview.TeamMember.ID,
                wait_for_page=True)
            Wait.text_by_css(
                Constants.Dashboard.Wizard.Title.CSS,
                Constants.Dashboard.Wizard.InviteTeamMembers.Title.TEXT)
            Enter.text_by_name("email", email)
            Wait.text_by_css(
                Constants.SubmitButton.CSS,
                Constants.Dashboard.Wizard.InviteTeamMembers.Button.TEXT)
            Click.css(".inviteMembers-form button.btn.btn-primary", True)
            if wait_modal_to_disappear:
                Wait.modal_to_dissappear()
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "FAILED in PopUp Invite Team Members. Exception=" + \
                str(e)
            raise Exception(errorMsg)

    @staticmethod
    def date_picker_add_ns(count):
        try:
            session.ice_driver.execute_script(
                "var el = angular.element(document.querySelector" +
                "('.addNextSteps')); el.scope().vm.nextSteps[" +
                str(count) +
                "].duedate = new Date('" +
                str(
                    datetime.today().isoformat()) +
                "')")
            Click.css("div.modal-content", wait_for_page=True)
        except Exception as e:
            errorMsg = "Failed to select date with datePicker."

            raise Exception(errorMsg, str(e))

    @staticmethod
    def date_picker_wizard():
        Enter.date_picker('#e2e-lab-entry-date', 'choice.TargetLab')
        Click.css('input[name="virtualFunction"]', wait_for_page=True)
