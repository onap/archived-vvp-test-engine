
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
import json
import time

from django.conf import settings
import requests

from services.api.api_user import APIUser
from services.constants import Constants, ServiceProvider
from services.database.db_general import DBGeneral
from services.helper import Helper
from services.logging_service import LoggingServiceFactory


logger = LoggingServiceFactory.get_logger()


class APIVirtualFunction:

    @staticmethod
    def add_next_step(user_content, files=[]):
        r1 = None
        postURL = settings.ICE_EM_URL + '/v1/engmgr/engagements/' + \
            user_content['engagement_uuid'] + '/nextsteps'
        logger.debug("Post add next step URL: " + postURL)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = user_content['session_token']
        data = dict()  # Create JSON data for post request.
        files_list = list()
        if isinstance(files, list):
            for file in files:
                files_list.append(file)
        else:
            files_list.append(files)
        data['files'] = files_list
        data['assigneesUuids'] = [user_content['uuid']]
        data['duedate'] = str(datetime.date.today())
        data['description'] = "API test - add next step."
        list_data = []
        list_data.append(data)
        try:
            r1 = requests.post(
                postURL, json=list_data, headers=headers, verify=False)
            Helper.internal_assert(r1.status_code, 200)
            logger.debug("Next step was added to the engagement!")
            ns_uuid = r1.json()
            return ns_uuid[0]['uuid']
        except BaseException:
            if r1 is None:
                logger.error(
                    "Failed to add next step to VF " + user_content['vfName'])
            else:
                logger.error("Failed to add next step to VF " +
                             user_content['vfName'] +
                             ", see response >>> %s %s.\nContent: %s" %
                             (r1.status_code, r1.reason, str(
                                 r1.content, 'utf-8')))
            raise

    @staticmethod
    def create_vf(token):
        r1 = None
        postUrl = settings.EM_REST_URL + "vf/"
        targetVersion = DBGeneral.select_from(
            "uuid", "ice_deployment_target", 1)
        ecompRelease = DBGeneral.select_from("uuid", "ice_ecomp_release", 1)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = 'token ' + token
        jdata = [
            {
                "virtual_function": Helper.rand_string("randomString"),
                "version": Helper.rand_string("randomString") +
                Helper.rand_string("randomNumber"),
                "target_lab_entry_date": time.strftime("%Y-%m-%d"),
                "target_aic_uuid": targetVersion,
                "ecomp_release": ecompRelease,
                "is_service_provider_internal": False}]
        try:
            r1 = requests.post(
                postUrl, json=jdata, headers=headers, verify=False)
            Helper.internal_assert(r1.status_code, 200)
            logger.debug("Virtual Function created successfully!")
            content = r1.content[1:-1]
            return content
        except BaseException:
            if r1 is None:
                logger.debug("Failed to create VF >>> request failed!")
            else:
                logger.debug(
                    "Failed to create VF >>> %s %s \n %s" %
                    (r1.status_code, r1.reason, str(
                        r1.content, 'utf-8')))
            raise

    @staticmethod
    def get_engagement(user_content):
        r1 = None
        postUrl = settings.EM_REST_URL + 'single-engagement/' + \
            str(user_content['engagement_uuid'],)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = user_content['session_token']
        try:
            r1 = requests.get(
                postUrl, headers=headers, verify=False)
            Helper.internal_assert(r1.status_code, 200)
            logger.debug("Retrieved the Engagement successfully!")
            content = r1.content
            return json.loads(content)
        except BaseException:
            if r1 is None:
                logger.debug(
                    "Failed to Retrieve the Engagement >>> request failed!")
            else:
                logger.debug(
                    "Failed to Retrieve the Engagement >>> %s %s \n %s" %
                    (r1.status_code, r1.reason, str(
                        r1.content, 'utf-8')))
            raise

    @staticmethod
    def invite_team_member(user_content):
        r1 = None
        postURL = settings.ICE_EM_URL + '/v1/engmgr/invite-team-members/'
        logger.debug("Post invite user URL: " + postURL)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = user_content['session_token']
        data = dict()  # Create JSON data for post request.
        data['email'] = Helper.rand_string(
            'randomString') + "@" + ServiceProvider.email
        data['eng_uuid'] = user_content['engagement_uuid']
        list_data = []
        list_data.append(data)
        try:
            r1 = requests.post(
                postURL, json=list_data, headers=headers, verify=False)
            Helper.internal_assert_boolean(r1.status_code, 200)
            logger.debug("Invite sent successfully to email " + data['email'])
            invite_token = DBGeneral.select_where_and(
                "invitation_token",
                "ice_invitation",
                "email",
                data['email'],
                "engagement_uuid",
                user_content['engagement_uuid'],
                1)
            invite_url = settings.ICE_PORTAL_URL + "/#/signUp?invitation=" + \
                invite_token + "&email=" + data['email']
            logger.debug("Invitation URL is: " + invite_url)
            return data['email'], invite_token, invite_url
        except BaseException:
            if r1 is None:
                logger.error("Failed to invite team member.")
            else:
                logger.error(
                    "POST request failed to invite team member, " +
                    "see response >>> %s %s" % (r1.status_code, r1.reason))
            raise

    @staticmethod
    def add_contact(user_content):
        r1 = None
        postURL = settings.ICE_EM_URL + '/v1/engmgr/add-contact/'
        logger.debug("Post invite vendor contact URL: " + postURL)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = user_content['session_token']
        data = dict()  # Create JSON data for post request.
        data['company'] = user_content['vendor_uuid']
        data['email'] = Helper.rand_string(
            'randomString') + "@" + ServiceProvider.email
        data['eng_uuid'] = user_content['engagement_uuid']
        data['full_name'] = Helper.rand_string('randomString')
        data['phone_number'] = "+1201" + Helper.rand_string("randomNumber", 6)
        try:
            r1 = requests.post(
                postURL, json=data, headers=headers, verify=False)
            Helper.internal_assert_boolean(r1.status_code, 200)
            logger.debug("Invite sent successfully to email " + data['email'])
            invite_token = DBGeneral.select_where_and(
                "invitation_token",
                "ice_invitation",
                "email",
                data['email'],
                "engagement_uuid",
                user_content['engagement_uuid'],
                1)
            invite_url = settings.ICE_PORTAL_URL + "/#/signUp?invitation=" +\
                invite_token + "&email=" + data['email'] +\
                "&full_name=" + data['full_name'] + \
                "&phone_number=" + data['phone_number'] + "&company=" + \
                data['company'] + "&is_contact_user=true"
            logger.debug("Invitation URL is: " + invite_url)
            return data['email'], invite_token, invite_url
        except BaseException:
            if r1 is None:
                logger.error("Failed to invite vendor contact.")
            else:
                logger.error(
                    "POST request failed to invite vendor contact, " +
                    "see response >>> %s %s \n %s" %
                    (r1.status_code, r1.reason, str(
                        r1.content, 'utf-8')))
            raise

    @staticmethod
    def edit_next_step(user_content, ns_uuid):
        r1 = None
        postURL = settings.ICE_EM_URL + '/v1/engmgr/nextsteps/' + ns_uuid + \
            '/engagement/' + user_content['engagement_uuid'] + '/modify/'
        logger.debug("Put next step URL: " + postURL)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = user_content['session_token']
        data = dict()  # Create JSON data for post request.
        data['files'] = []
        data['assigneesUuids'] = [user_content['uuid']]
        data['duedate'] = str(datetime.date.today())
        data['description'] = "API edit next step test " + \
            Helper.rand_string('randomString')
        try:
            r1 = requests.put(
                postURL, json=data, headers=headers, verify=False)
            Helper.internal_assert_boolean(r1.status_code, 202)
            logger.debug("Next step was edited successfully!")
        except BaseException:
            if r1 is None:
                logger.error("Failed to edit next step uuid: " + ns_uuid)
            else:
                logger.error(
                    "Failed to edit next step uuid: " +
                    ns_uuid +
                    ", see response >>> %s %s" %
                    (r1.status_code,
                     r1.reason))
            raise

    @staticmethod
    def get_export_dasboard_excel(token, keywords=""):
        postUrl = settings.EM_REST_URL + \
            "engagement/export/?stage=All&keyword=" + keywords
        headers = {"Authorization": token}
        r1 = requests.get(postUrl, headers=headers, verify=False)
        Helper.internal_assert(r1.status_code, 200)
        if (r1.status_code == 200):
            logger.debug("APIUser activated successfully!")
            return r1.content
        else:
            raise Exception(
                "Failed to activate user >>> %s %s" %
                (r1.status_code, r1.reason))
            return False

    @staticmethod
    def create_engagement(wait_for_gitlab=True):
        user_content = APIUser.create_new_user()
        APIUser.activate_user(
            user_content['uuid'], user_content['user']['activation_token'])
        token = APIUser.login_user(user_content['email'])
        vf_content = json.loads(APIVirtualFunction.create_vf(token))
        user_content['vfName'] = vf_content['name']
        user_content['vf_uuid'] = vf_content['uuid']
        user_content['target_aic'] = vf_content['deployment_target']['version']
        # <-- ECOMP RELEASE
        user_content['ecomp_release'] = vf_content[
            'ecomp_release']['name']
        user_content['vnf_version'] = vf_content['version']
        if(vf_content['vendor']['name'] == "AT&amp;T"):
            user_content['vendor'] = "AT&T"
        else:
            user_content['vendor'] = vf_content['vendor']['name']
        user_content['vendor_uuid'] = vf_content['vendor']['uuid']
        user_content['engagement_manual_id'] = vf_content[
            'engagement']['engagement_manual_id']
        user_content['target_lab_entry_date'] = vf_content[
            'target_lab_entry_date']
        user_content['el_email'] = vf_content[
            'engagement']['reviewer']['email']
        user_content['el_name'] = vf_content[
            'engagement']['reviewer']['full_name']
        user_content['pr_email'] = vf_content[
            'engagement']['peer_reviewer']['email']
        user_content['pr_name'] = vf_content[
            'engagement']['peer_reviewer']['full_name']
        user_content['engagement_uuid'] = vf_content['engagement']['uuid']
        user_content['session_token'] = 'token ' + token
        user_content['engagement'] = vf_content['engagement']
        user_content['vfStage'] = vf_content['engagement']['engagement_stage']

        return user_content

    @staticmethod
    def set_eng_stage(user_content, requested_stage):
        token = APIUser.login_user(user_content['el_email'])
        r1 = None
        putUrl = Constants.Default.URL.Engagement.SingleEngagement.TEXT + \
            user_content['engagement_uuid'] + "/stage/" + str(requested_stage)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = 'token ' + token
        try:
            r1 = requests.put(
                putUrl, headers=headers, verify=False)
            Helper.internal_assert(r1.status_code, 202)
            logger.debug(
                "Engagement stage was successfully changed to " +
                str(requested_stage) +
                "!")
            content = r1.content[1:-1]
            return content
        except BaseException:
            if r1 is None:
                logger.debug("Failed to set eng stage >>> request failed!")
            else:
                logger.debug(
                    "Failed to set eng stage >>> %s %s \n %s" %
                    (r1.status_code, r1.reason, str(
                        r1.content, 'utf-8')))
            raise

    @staticmethod
    def update_aic_version(eng_uuid, aic_version_uuid, session_token):
        r1 = None
        putURL = Constants.Default.URL.Engagement.EngagementOperations.TEXT + \
            eng_uuid + '/deployment-targets/' + aic_version_uuid
        logger.debug("Put next step URL: " + putURL)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = session_token
        try:
            r1 = requests.put(putURL, headers=headers, verify=False)
            Helper.internal_assert_boolean(r1.status_code, 200)
            logger.debug("AIC version has changed!")
        except BaseException:
            if r1 is None:
                msg = "Failed to edit AIC version"
            else:
                msg = "Failed to edit AIC version, see response >>> %s %s" % (
                    r1.status_code, r1.reason)
            raise msg

    @staticmethod
    def update_ecomp_release(eng_uuid, ecomp_release_uuid, session_token):
        r1 = None
        putURL = Constants.Default.URL.Engagement.EngagementOperations.TEXT + \
            eng_uuid + '/ecomp-releases/' + ecomp_release_uuid
        logger.debug("Put next step URL: " + putURL)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = session_token
        try:
            r1 = requests.put(putURL, headers=headers, verify=False)
            Helper.internal_assert_boolean(r1.status_code, 200)
            logger.debug("AIC version has changed!")
        except BaseException:
            if r1 is None:
                msg = "Failed to update ECOMP release"
            else:
                msg = "Failed to update ECOMP release," +\
                    " see response >>> %s %s" % (
                        r1.status_code, r1.reason)
            raise msg
