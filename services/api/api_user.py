
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
import re

from django.conf import settings
import requests

from services.api.api_bridge import APIBridge
from services.api.api_gitlab import APIGitLab
from services.constants import Constants, ServiceProvider
from services.helper import Helper
from services.logging_service import LoggingServiceFactory


logger = LoggingServiceFactory.get_logger()


class APIUser:

    @staticmethod
    # Update account API - only adds new SSH key!
    def update_account(user_content):
        r1 = None
        token = APIUser.login_user(user_content['email'])
        user_content['session_token'] = 'token ' + token
        sshKey = Helper.generate_sshpub_key()
        putURL = settings.ICE_EM_URL + '/v1/engmgr/users/account'
        logger.debug("Put user URL: " + putURL)
        headers = dict()  # Create header for put request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = user_content['session_token']
    #   headers['Authorization'] = user_content['activation_token']
        put_data = dict()  # Create JSON data for put request.
        user_content['vendor'] = user_content['company']['name']
        if user_content['vendor'] == "AT&amp;T":
            put_data['company'] = "AT&T"
        else:
            put_data['company'] = user_content['vendor']
        put_data['email'] = user_content['email']
        put_data['full_name'] = user_content['full_name']
        put_data['password'] = ""
        put_data['phone_number'] = "+1201" + \
            Helper.rand_string("randomNumber", 6)
        put_data['ssh_key'] = sshKey
        try:
            r1 = requests.put(
                putURL, json=put_data, headers=headers, verify=False)
            Helper.internal_assert(r1.status_code, 200)
            logger.debug(
                "SSH Key was added successfully to user " +
                user_content['full_name'])
            if not APIBridge.is_gitlab_ready(user_content):
                raise
            return sshKey
        except BaseException:
            if r1 is None:
                logger.error("Failed to add public SSH key to user.")
            else:
                logger.error(
                    "PUT request failed to add SSH key to user, see " +
                    "response >>> %s %s \n %s" %
                    (r1.status_code, r1.reason, str(
                        r1.content, 'utf-8')))
            raise

    @staticmethod
    # Update account API - only adds new SSH key!
    def update_account_injec_script(user_content):
        r1 = None
        putURL = settings.ICE_EM_URL + '/v1/engmgr/users/account'
        logger.debug("Put user URL: " + putURL)
        headers = dict()  # Create header for put request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = user_content['session_token']
        put_data = dict()  # Create JSON data for put request.
        if user_content['vendor'] == "AT&amp;T":
            put_data['company'] = "AT&T"
        else:
            put_data['company'] = user_content['vendor']
        put_data['email'] = user_content['email']
        script = "<script>;</script>"
        put_data['full_name'] = script
        put_data['password'] = ""
        put_data['phone_number'] = "+1201" + \
            Helper.rand_string("randomNumber", 6)
        try:
            r1 = requests.put(
                putURL, json=put_data, headers=headers, verify=False)
            Helper.internal_assert(r1.status_code, 200)
            msg = "Testing for Cross site scripting successfully : " + \
                user_content['full_name'] + \
                "stattus Code = " + str(r1.status_code)
            logger.debug(msg)
            if not APIBridge.is_gitlab_ready(user_content):
                raise
            return True
        except BaseException:
            if r1 is None:
                logger.error("Failed to add public SSH key to user.")
            else:
                logger.error(
                    "PUT request failed to add SSH key to user, " +
                    "see response >>> %s %s \n %s" %
                    (r1.status_code, r1.reason, str(
                        r1.content, 'utf-8')))
            raise

    @staticmethod
    def create_new_user(company=False, activate=False):
        signupUrl = settings.EM_REST_URL + "signup/"
        signupParams = APIUser.create_signup_param(company)
        r1 = requests.post(signupUrl, json=signupParams, verify=False)
        if (r1.status_code == 201 or r1.status_code == 200):
            logger.debug("Moving to next test case. status=" +
                         str(r1.status_code))
            pass  # Need to break here.
        try:
            user_data = r1.json()
        except Exception as e:
            logger.error("=========== json error ========")
            logger.error("r1.content = " + str(r1.content) +
                         ", status=" + str(r1.status_code))
            logger.error("=========== json error end ========")
            raise e
        if activate:
            APIUser.activate_user(
                user_data['uuid'], user_data["user"]["activation_token"])
        return user_data

    @staticmethod
    def login_user(email):
        postUrl = settings.EM_REST_URL + "login"
        user_data = dict()  # Create JSON data for post request.
        user_data['email'] = email
        user_data['password'] = "iceusers"
        try:
            headers = {'Content-type': 'application/json'}
            r = requests.post(
                postUrl, json=user_data, headers=headers, verify=False)
            logger.debug(str(r.status_code) + " " + r.reason)
            decoded_response = r.json()
            return decoded_response['token']
        except BaseException:
            logger.debug("Failed to login.")
            raise

    @staticmethod
    def set_ssh(user_content, sshKey=None):  # Set SSH key to user.
        r1 = None
        if sshKey is None:
            logger.debug("About to generate an ssh key for the user: %s" %
                         user_content['email'])
            sshKey = Helper.generate_sshpub_key()
        postURL = settings.ICE_EM_URL + '/v1/engmgr/users/ssh'
        logger.debug("Post user URL: " + postURL)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = user_content['session_token']
        post_data = dict()  # Create JSON data for post request.
        post_data['ssh_key'] = sshKey
        try:
            r1 = requests.post(
                postURL, json=post_data, headers=headers, verify=False)
            Helper.internal_assert(r1.status_code, 200)
            logger.debug(
                "SSH Key was added successfully")
            if not APIBridge.is_gitlab_ready(user_content):
                raise
            return sshKey
        except BaseException:
            if r1 is None:
                logger.error("Failed to add public SSH key.")
            else:
                logger.error(
                    "POST request failed to add SSH key to user, " +
                    "see response >>> %s %s" %
                    (r1.status_code, r1.reason))
            raise

    @staticmethod
    def create_signup_param(company=False):
        try:  # Click on element in UI, by xPath locator.
            if not company:
                company = ServiceProvider.MainServiceProvider
                email_domain = ServiceProvider.email
            else:
                email_domain = company.lower() + ".com"  #
            data = {
                "company": company,
                "full_name": Helper.rand_string("randomString"),
                "email": Helper.rand_string("randomString") +
                "@" + email_domain,
                "phone_number": Constants.Default.Phone.TEXT,
                "password": Constants.Default.Password.TEXT,
                "regular_email_updates": "True"}

            return data
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "Could not create Sign Up parametrs"
            raise Exception(errorMsg, e)

    @staticmethod
    def activate_user(userUuid, activationToken):
        postUrl = settings.ICE_EM_URL + "/v1/engmgr/users/activate/" + \
            userUuid + "/" + activationToken
        logger.debug(postUrl)
        r1 = requests.get(postUrl, verify=False)
        if (r1.status_code == 200):
            logger.debug("APIUser activated successfully!")
            return True
        else:
            raise Exception(
                "Failed to activate user >>> %s %s" %
                (r1.status_code, r1.reason))

    @staticmethod
    def signup_invited_user(
            company,
            invited_email,
            invite_token,
            invite_url,
            user_content,
            is_contact_user="false",
            activate=False,
            wait_for_gitlab=True):
        r1 = None
        postURL = settings.ICE_EM_URL + '/v1/engmgr/signup'
        logger.debug("Post signup URL: " + postURL)
        if is_contact_user == "true":
            fullName = re.sub("http.*full_name=", "", invite_url)
            fullName = re.sub("&.*", "", fullName)
            logger.debug(
                "Invited contact full name is (according to url): " + fullName)
        else:
            fullName = Helper.rand_string('randomString')

        post_data = dict()  # Create JSON data for post request.
        post_data['company'] = company
        post_data['email'] = invited_email
        post_data['full_name'] = fullName
        post_data['invitation'] = invite_token
        post_data['is_contact_user'] = is_contact_user
        post_data['password'] = "iceusers"
        post_data['phone_number'] = "+1201" + \
            Helper.rand_string("randomNumber", 6)
        post_data['regular_email_updates'] = "False"
        post_data['terms'] = "True"
        try:
            requests.get(invite_url, verify=False)
            r1 = requests.post(
                postURL, json=post_data, verify=False)
            Helper.internal_assert(r1.status_code, 200)
            logger.debug("Invited user signed-up successfully!")

            user_data = r1.json()
            if activate:
                APIUser.activate_user(
                    user_data['uuid'], user_data["user"]["activation_token"])

            if wait_for_gitlab:
                if not APIBridge.is_gitlab_ready(user_content):
                    raise
            return post_data
        except BaseException:
            if r1 is None:
                logger.error("Failed to sign up the invited team member.")
            else:
                logger.error(
                    "POST request failed to sign up the invited " +
                    "team member, see response >>> %s %s \n %s" %
                    (r1.status_code, r1.reason, str(
                        r1.content, 'utf-8')))
            raise

    @staticmethod
    def create_new_user_content():
        user_content = APIBridge.create_engagement()
        APIGitLab.git_clone_push(user_content)
        APIBridge.frontend_login(
            user_content['email'], Constants.Default.Password.TEXT)
        vfName = user_content['vfName']
        uuid = user_content['uuid']
        inviteEmail = Helper.rand_invite_email()
        newObj = [vfName, uuid, inviteEmail]
        return newObj, user_content

    @staticmethod
    def create_new_user_content_login_with_api():
        user_content = APIBridge.create_engagement()
        APIGitLab.git_clone_push(user_content)
        token = "token " + APIBridge.login_user(user_content['el_email'])
        user_content['session_token'] = token
        return user_content
