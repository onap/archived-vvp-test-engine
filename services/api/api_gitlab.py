 
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
import logging
import os
import subprocess
import sys
import time

from django.conf import settings
import git
import requests

from services.api.api_bridge import APIBridge
from services.constants import Constants
from services.database.db_virtual_function import DBVirtualFunction
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()

class APIGitLab:

    @staticmethod
    def display_output(p):
        while True:
            out = p.stderr.read(1)
            if out == b'' and p.poll() != None:
                break
            if out != '':
                sys.stdout.write(str(out.decode()))
                sys.stdout.flush()

    @staticmethod
    def get_git_project(path_with_namespace):
        r1 = None
        getURL = Constants.Default.URL.GitLab.Projects.TEXT + \
            path_with_namespace
        logger.debug("Get project URL: " + getURL)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['PRIVATE-TOKEN'] = settings.GITLAB_TOKEN
        try:
            r1 = requests.get(getURL, headers=headers, verify=False)
            Helper.internal_assert(r1.status_code, 200)
            counter = 0
            while r1.content == b'[]' and counter <= Constants.GitLabConstants.RETRIES_NUMBER:
                time.sleep(session.wait_until_time_pause)
                r1 = requests.get(getURL, headers=headers, verify=False)
                Helper.internal_assert(r1.status_code, 200)

            if r1.content == b'[]':
                logger.error("Got an empty list as a response.")
                raise
            logger.debug("Project exists on APIGitLab!")
            content = r1.json()  # Change it from list to dict.
            return content
        except:
            if r1 is None:
                logger.error("Failed to get project from APIGitLab.")
            else:
                logger.error("Failed to get project from APIGitLab, see response >>> %s %s \n %s"
                             % (r1.status_code, r1.reason, str(r1.content, 'utf-8')))
            raise

    def are_all_list_users_registered_as_project_members(self, users_emails_list, project_path_with_namespace):
        for email in users_emails_list:
            if not self.validate_git_project_members(project_path_with_namespace, email):
                raise Exception(
                    "Couldn't find the invited users: " + email + " in GitLab.")
            logger.debug(
                "Invited user: " + email + " found in GitLab.")

    @staticmethod
    def validate_git_project_members(path_with_namespace, user_email):
        if settings.DATABASE_TYPE != 'local':
            r1 = None
            headers = dict()
            git_user = APIGitLab.get_git_user(user_email)
            getURL = Constants.Default.URL.GitLab.Projects.TEXT + \
                path_with_namespace + "/members/" + str(git_user['id'])
            logger.debug("Get project members URL: " + getURL)
            headers['Content-type'] = 'application/json'
            headers['PRIVATE-TOKEN'] = settings.GITLAB_TOKEN
            counter = 0
            while (r1 is None or r1.content == b'[]' or r1.status_code != 200) and counter <= Constants.GitLabConstants.RETRIES_NUMBER:
                logger.debug(
                    "try to get git project members (try #%s)" % counter)
                time.sleep(session.wait_until_time_pause)
                try:
                    r1 = requests.get(getURL, headers=headers, verify=False)
                    counter += 1
                except Exception as e:
                    if counter >= Constants.GitLabConstants.RETRIES_NUMBER:
                        logger.error("Failed to get project's team members from APIGitLab, see response  >>> %s %s \n %s %s"
                                     % (r1.status_code, r1.reason, str(r1.content, 'utf-8'), e.message))
                        return False
            if r1.content == b'[]':
                logger.error("Got an empty list as a response.")
                return False
            elif r1.status_code != 200:
                logger.error("Got %s %s." % (r1.status_code, r1.reason))
                return False
            logger.debug("Got %s %s, user found in project." %
                         (r1.status_code, r1.reason))
        return True

    @staticmethod
    def negative_validate_git_project_member(path_with_namespace, user_email, git_user_id):
        if settings.DATABASE_TYPE != 'local':
            r1 = None
            headers = dict()
            getURL = Constants.Default.URL.GitLab.Projects.TEXT + \
                path_with_namespace + "/members/" + git_user_id
            logger.debug("Get project members URL: " + getURL)
            headers['Content-type'] = 'application/json'
            headers['PRIVATE-TOKEN'] = settings.GITLAB_TOKEN
            counter = 0
            while r1 is None or str.encode(user_email) not in r1.content and counter <= Constants.GitLabConstants.RETRIES_NUMBER:
                logger.debug(
                    "try to get git project members (try #%s)" % counter)
                time.sleep(session.wait_until_time_pause)
                try:
                    r1 = requests.get(getURL, headers=headers, verify=False)
                    counter += 1
                except Exception as e:
                    if counter >= Constants.GitLabConstants.RETRIES_NUMBER:
                        logger.error("Failed to get project's team members from APIGitLab, see response  >>> %s %s \n %s %s"
                                     % (r1.status_code, r1.reason, str(r1.content, 'utf-8'), e.message))
                        return False

            if r1.content == b'[]':
                logger.debug("Got %s %s, user not found in project." %
                             (r1.status_code, r1.reason))
                return True
            else:
                logger.debug("Got %s %s, user found in project." %
                             (r1.status_code, r1.reason))
                return False

    @staticmethod
    def get_git_user(user_email):
        if settings.DATABASE_TYPE != 'local':
            r1 = None
            user_email = user_email.replace("@", "_at_")
            getURL = settings.GITLAB_URL + \
                "api/v3/users?username=" + user_email
            logger.debug("Get user URL: " + getURL)
            headers = dict()  # Create header for post request.
            headers['Content-type'] = 'application/json'
            headers['PRIVATE-TOKEN'] = settings.GITLAB_TOKEN
            try:
                r1 = requests.get(getURL, headers=headers, verify=False)
                Helper.internal_assert(r1.status_code, 200)
                counter = 0
                while r1.content == b'[]' and counter <= 60:
                    logger.info(
                        "Will try to get gitlab user until will be response... #%s" % counter)
                    time.sleep(session.wait_until_time_pause_long)
                    r1 = requests.get(getURL, headers=headers, verify=False)
                    Helper.internal_assert(r1.status_code, 200)
                    counter += 1

                if r1.content == b'[]':
                    logger.error("Got an empty user from gitlab.")
                    raise Exception("Got an empty user from gitlab.")

                logger.debug("Got %s %s and received user data: %s." %
                             (r1.status_code, r1.reason, r1.content))
                content = r1.json()
                return content[0]
            except:
                if r1 is None:
                    logger.error("Failed to get user from APIGitLab.")
                else:
                    logger.error("Failed to get user from APIGitLab, see response >>> %s %s \n %s"
                                 % (r1.status_code, r1.reason, str(r1.content, 'utf-8')))
                    raise

    @staticmethod
    def get_git_user_ssh_key(git_user_id):
        r1 = None
        getURL = Constants.Default.URL.GitLab.Users.TEXT + \
            str(git_user_id) + "/keys"
        logger.debug("Get user URL: " + getURL)
        headers = dict()  # Create header for post request.
        headers['Content-type'] = 'application/json'
        headers['PRIVATE-TOKEN'] = settings.GITLAB_TOKEN
        try:
            r1 = requests.get(getURL, headers=headers, verify=False)
            Helper.internal_assert(r1.status_code, 200)
            if r1.content == '[]':
                logger.error("Got an empty list as a response.")
                raise
            logger.debug("Got %s %s and received user's public key." %
                         (r1.status_code, r1.reason))
            content = r1.json()  # Change it from list to dict.
            gitPubKey = content[0]['key']
            return gitPubKey
        except:
            if r1 is None:
                logger.error("Failed to get user's public key from APIGitLab.")
            else:
                logger.error("Failed to get user's public key from APIGitLab, see response >>> %s %s \n %s"
                             % (r1.status_code, r1.reason, str(r1.content, 'utf-8')))
            raise

    @staticmethod
    def git_clone_push(user_content):
        if settings.DATABASE_TYPE != 'local':
            logger.debug(
                "About to push files into project's repository on the local folder(not over origin).")
            try:
                user_content['session_token'] = "token " + \
                    APIBridge.login_user(Constants.Users.Admin.EMAIL)
                used_email_for_actions = Constants.Users.Admin.EMAIL
                repo_dir = Constants.Paths.LocalGitFolder.PATH + \
                    user_content['vfName']
                if not os.path.exists(repo_dir):
                    os.makedirs(repo_dir)
                    logger.debug("Created the following folder: %s" % repo_dir)
                # Create pair of keys for user.
                user_pub_key = Helper.get_or_create_rsa_key_for_admin()
                DBVirtualFunction.add_admin_to_eng_team(
                    user_content['engagement_uuid'])
                # Set SSH Key for the user.
                APIBridge.set_ssh(user_content, user_pub_key)
                git_user = APIGitLab.get_git_user(used_email_for_actions)

                counter = 0
                git_user_pub_key = None
                while user_pub_key != git_user_pub_key and counter < Constants.GitLabConstants.RETRIES_NUMBER:
                    try:
                        git_user_pub_key = APIGitLab.get_git_user_ssh_key(
                            git_user['id'])
                    except Exception as e:
                        pass

                    counter += 1
                    time.sleep(session.wait_until_time_pause)

                # Check that the SSH key was added to user on APIGitLab.
                if user_pub_key != git_user_pub_key:
                    raise Exception("The SSH Key received does not equal to the"
                                    " one provided! The key from"
                                    "APIGitLab:\n %s  ==<>== %s"
                                    % (git_user_pub_key, user_pub_key))

                gitRepoURL = "git@gitlab:%s/%s.git" % (
                    user_content['engagement_manual_id'], user_content['vfName'])
                logger.debug("Clone repo from: " + gitRepoURL)
                APIGitLab.is_gitlab_ready(user_content)
                cmd = 'cd ' + repo_dir + \
                    '; git config --global user.email \"' + Constants.Users.Admin.EMAIL + \
                    '\"; git config --global user.name \"' + \
                    Constants.Users.Admin.FULLNAME + '\";'
                # Commit all changes.
                p = subprocess_popen = subprocess.Popen(
                    cmd, shell=True, stderr=subprocess.PIPE)
                while subprocess_popen is None:
                    logger.debug(
                        "waiting to subprocess command to complete...")
                APIGitLab.display_output(p)
                # Clone project from APIGitLab.
                repo = git.Repo.clone_from(gitRepoURL, repo_dir)
                logger.debug("Successfully cloned repo to " + repo_dir)
                # Create three files (file0, file1, file2) and add them to git
                # index.
                for i in range(3):
                    fileName = repo_dir + '/file' + str(i)
                    with open(fileName, 'w') as content_file:
                        os.chmod(fileName, 0o600)
                        content_file.write("Test file " + fileName)
                    repo.index.add([fileName])
                    logger.debug(
                        fileName + " was created and added to commit list.")
                cmd = 'cd ' + repo_dir + \
                    '; git commit -a -m \"Create and add 3 files to git.\"'
                # Commit all changes.
                p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
                APIGitLab.display_output(p)
                logger.debug("All files added to commit list.")
                cmd = 'cd ' + repo_dir + '; git push'
                # Push commit to APIGitLab.
                p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
                APIGitLab.display_output(p)
                logger.debug("All files were pushed to APIGitLab.")
            except Exception as e:
                logger.error(
                    "_-_-_-_-_- Unexpected error in git_clone_push: " + str(e))
                raise Exception(e)

    @staticmethod
    def git_push_commit(user_content):
        if settings.DATABASE_TYPE != 'local':
            logger.debug(
                "About to push files into project's repository on APIGitLab")
            try:
                git_work = '/tmp/git_work/'
                repo_dir = git_work + user_content['vfName']
                # Create three files (file0, file1, file2) and add them to git
                # index.
                for i in range(3):
                    fileName = repo_dir + '/file' + str(i)
                    with open(fileName, 'w') as content_file:
                        os.chmod(fileName, 0o600)
                        content_file.write("Edit test file " + fileName)
                    logger.debug(fileName + " was edited.")
                cmd = 'cd ' + repo_dir + \
                    '; git commit -a -m \"Create and add 3 files to git.\"'
                # Commit all changes.
                p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
                APIGitLab.display_output(p)
                logger.debug("All edited files were committed.")
                cmd = 'cd ' + repo_dir + '; git push'
                # Push commit to APIGitLab.
                p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
                APIGitLab.display_output(p)
                logger.debug(
                    "All edited files were commited and pushed to APIGitLab.")
            except Exception as e:
                logger.error(
                    "_-_-_-_-_- Unexpected error in git_push_commit : " + str(e))
                raise Exception(
                    "Something went wrong on git_push_commit function, please check logs.")

    @staticmethod
    def is_gitlab_ready(user_content):
        counter = 1
        gettURL = settings.ICE_EM_URL + '/v1/engmgr/engagement/' + \
            user_content['engagement_uuid'] + '/checklist/new/'
        logger.debug(
            "Get URL to check if GitLab and Jenkins are ready: " + gettURL)
        # Validate with EL
        token = "token " + APIBridge.login_user(user_content['el_email'])
        headers = dict()  # Create header for get request.
        headers['Content-type'] = 'application/json'
        headers['Authorization'] = token
        r1 = requests.get(gettURL, headers=headers, verify=False)
        while (r1.content == b'"Create New checklist is not ready yet"' and counter <=
               Constants.GitLabConstants.RETRIES_NUMBER):
            time.sleep(session.wait_until_time_pause_long)
            logger.debug(
                "GitLab and Jenkins are not ready yet, trying again (%s of %s)" %
                (counter, Constants.GitLabConstants.RETRIES_NUMBER))
            r1 = requests.get(gettURL, headers=headers, verify=False)
            counter += 1
        if r1.status_code != 200:
            if r1.content == "Create New checklist is not ready yet":
                raise Exception("Max retries exceeded, failing test...")
            else:
                raise Exception("Something went wrong while waiting for GitLab and Jenkins. %s %s" % (
                    r1.status_code, r1.reason))
            return False
        elif r1.status_code == 200:
            logger.debug("Gitlab and Jenkins are ready to continue!")
            return True
