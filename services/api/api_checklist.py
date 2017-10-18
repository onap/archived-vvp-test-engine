
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
import datetime
import logging

import requests

from services.api.api_gitlab import APIGitLab
from services.api.api_user import APIUser
from services.constants import Constants
from services.database.db_general import DBGeneral
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.database.db_checklist import DBChecklist


logger = LoggingServiceFactory.get_logger()


class APIChecklist:

    @staticmethod
    def create_checklist(user_content, files=["file0", "file1"], return_negative_response=False):
        r1 = None
        postURL = Constants.Default.URL.Checklist.TEXT + \
            user_content['engagement_uuid'] + '/checklist/new/'
        logger.debug("Post create checklist URL: " + postURL)
        headers = dict()
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = user_content['session_token']
        data = dict()
        data['checkListAssociatedFiles'] = files
        data['checkListName'] = "checklistAPI" + \
            Helper.rand_string('randomString')
        data['checkListTemplateUuid'] = DBGeneral.select_where(
            "uuid", "ice_checklist_template", "name", Constants.Template.Heat.TEXT, 1)
        try:
            if not APIGitLab.is_gitlab_ready(user_content):
                raise Exception(
                    "Gitlab is not ready and because of that the test is failed.")

            r1 = requests.post(postURL, json=data,
                               headers=headers, verify=False)

            Helper.internal_assert_boolean(r1.status_code, 200)
            logger.debug("Checklist was created successfully!")
            cl_content = r1.json()
            return cl_content
        except:
            if return_negative_response:
                return r1
            if r1 is None:
                logger.error(
                    "Failed to create checklist for VF " + user_content['vfName'])
            else:
                logger.error("Failed to create checklist for VF " + user_content[
                             'vfName'] + ", see response >>> %s %s.\nContent: %s" % (r1.status_code, r1.reason, str(r1.content, 'utf-8')))
            raise

    @staticmethod
    def update_checklist(user_content, cl_uuid):
        r1 = None
        postURL = Constants.Default.URL.Checklist.Update.TEXT + '/' + cl_uuid
        logger.debug("Post create checklist URL: " + postURL + '/' + cl_uuid)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = user_content['session_token']
        data = dict()  # Create JSON data for post request.
        data['checklistUuid'] = cl_uuid
        data['checkListAssociatedFiles'] = ["file1", "file2"]
        data['checkListName'] = "UpdateChecklistAPI" + \
            Helper.rand_string('randomString')
        data['checkListTemplateUuid'] = DBGeneral.select_where(
            "uuid", "ice_checklist_template", "name", Constants.Template.Heat.TEXT, 1)
        try:
            r1 = requests.put(
                postURL, json=data, headers=headers, verify=False)
            Helper.internal_assert(r1.status_code, 200)
            logger.debug("DBChecklist was created successfully!")
            cl_content = r1.json()
            return cl_content['uuid']
        except:
            if r1 is None:
                logger.error(
                    "Failed to create checklist for VF " + user_content['vfName'])
            else:
                logger.error("Failed to create checklist for VF " + user_content[
                             'vfName'] + ", see response >>> %s %s.\nContent: %s" % (r1.status_code, r1.reason, str(r1.content, 'utf-8')))
            raise

    @staticmethod
    def add_checklist_audit_log(user_content, cl_uuid):
        r1 = None
        postURL = Constants.Default.URL.Checklist.Update + \
            cl_uuid + '/auditlog/'
        logger.debug("Post checklist audit log URL: " + postURL)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = user_content['session_token']
        data = dict()  # Create JSON data for post request.
        data['description'] = "API audit log test " + \
            Helper.rand_string('randomString')
        try:
            r1 = requests.post(
                postURL, json=data, headers=headers, verify=False)
            Helper.internal_assert_boolean(r1.status_code, 200)
            logger.debug("Audit log was added successfully!")
        except:
            if r1 is None:
                logger.error(
                    "Failed to add audit log for checklist uuid: " + cl_uuid)
            else:
                logger.error("Failed to add audit log for checklist uuid: " + cl_uuid +
                             ", see response >>> %s %s.\nContent: %s" % (r1.status_code, r1.reason, str(r1.content, 'utf-8')))
            raise

    @staticmethod
    def add_checklist_next_step(user_content, cl_uuid):
        r1 = None
        postURL = Constants.Default.URL.Checklist.TEXT + \
            user_content['engagement_uuid'] + \
            '/checklist/' + cl_uuid + '/nextstep/'
        logger.debug("Post checklist next step URL: " + postURL)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = user_content['session_token']
        data = dict()  # Create JSON data for post request.
        data['files'] = ["file0"]
        data['assigneesUuids'] = [user_content['uuid']]
        data['duedate'] = str(datetime.date.today())
        data['description'] = "API next step test " + \
            Helper.rand_string('randomString')
        list_data = []
        list_data.append(data)
        try:
            r1 = requests.post(
                postURL, json=list_data, headers=headers, verify=False)
            Helper.internal_assert(r1.status_code, 200)
            logger.debug("Next step was added successfully!")
            ns_uuid = r1.json()
            return ns_uuid[0]['uuid']
        except:
            if r1 is None:
                logger.error(
                    "Failed to add next step for checklist uuid: " + cl_uuid)
            else:
                logger.error("Failed to add next step for checklist uuid: " + cl_uuid +
                             ", see response >>> %s %s.\nContent: %s" % (r1.status_code, r1.reason, str(r1.content, 'utf-8')))
            raise

    @staticmethod
    def jump_state(checklistUUID, engLeadEmail):
        token = APIUser.login_user(engLeadEmail)
        stateURL = Constants.Default.URL.Checklist.Rest.TEXT + \
            str(checklistUUID) + '/state/'
        APIChecklist.go_to_next_state(stateURL, token)

    @staticmethod
    def go_to_next_state(url, token):
        headers = {"Authorization": "token " + token}
        body = dict()
        body['description'] = ""
        body['decline'] = "False"
        r = requests.put(url, headers=headers, json=body, verify=False)
        if (r.status_code == 201 or r.status_code == 200):
            logger.debug("go_to_next_state put request result status: %s" %
                         r.status_code)
        else:
            logger.error(
                "PUT request failed to change checklist state >>> " + str(r.status_code) + " " + r.reason)
            raise Exception("PUT request failed to change checklist state")

    @staticmethod
    def move_cl_to_closed(cl_uuid, vf_staff_emails):
        api_checklist_obj = APIChecklist()
        states = [Constants.ChecklistStates.PeerReview.TEXT,
                  Constants.ChecklistStates.Approval.TEXT,
                  Constants.ChecklistStates.Handoff.TEXT,
                  Constants.ChecklistStates.Closed.TEXT]
        for i in range(len(vf_staff_emails)):
            logger.debug(
                "Trying to jump state for %s [%s]" % (vf_staff_emails[i], i))
            DBChecklist.update_all_decisions_to_approve(cl_uuid)
            api_checklist_obj.jump_state(cl_uuid, vf_staff_emails[i])
            logger.debug("Checking state changed to %s" % states[i])
            DBChecklist.state_changed("uuid", cl_uuid, states[i])

        # Move CL to closed state.
        logger.debug("Trying to jump state 'closed' for %s" %
                     vf_staff_emails[0])
        api_checklist_obj.jump_state(cl_uuid, vf_staff_emails[0])
        logger.debug("Checking state changed to %s" % states[-1])
        DBChecklist.state_changed("uuid", cl_uuid, states[-1])
