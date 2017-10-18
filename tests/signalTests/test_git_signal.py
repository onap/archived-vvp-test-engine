
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
Created on 16 Nov 2016

'''
from django.conf import settings
from iceci.decorator.exception_decor import exception
from services.api.api_virtual_function import APIVirtualFunction
from services.constants import Constants, ServiceProvider
from services.logging_service import LoggingServiceFactory
from services.types import API
from tests.signalTests.test_signal_base import TestSignalBase
from services.helper import Helper


logger = LoggingServiceFactory.get_logger()


class TestGitSignal(TestSignalBase):

    @exception()
    def test_create_eng(self):

        if settings.DATABASE_TYPE == 'local':
            logger.debug("Local environment, skipping test...")
        else:
            user_content = API.VirtualFunction.create_engagement()
            path_with_namespace = user_content[
                'engagement_manual_id'] + "%2F" + user_content['vfName']
            API.GitLab.get_git_project(path_with_namespace)
            if not API.GitLab.validate_git_project_members(path_with_namespace, user_content['el_email']):
                logger.error("Couldn't find user in GitLab response.")
                raise
            logger.debug(
                "Project was created successfully on GitLab. ELs included")
            try:
                job_name = user_content[
                    'vfName'] + "_" + user_content['engagement_manual_id']
                API.Jenkins.get_jenkins_job(job_name)
            except Exception as e:
                logger.error(
                    "_-_-_-_-_- Unexpected error in test_create_eng: " + str(e))
                raise Exception("Job wasnt created on APIJenkins." + str(e))

    @exception()
    def test_update_account(self):

        if settings.DATABASE_TYPE == 'local':
            logger.debug("Local environment, skipping test...")
        else:
            user_content = API.VirtualFunction.create_engagement()
            sshKey = API.User.update_account(user_content)
            git_user = API.GitLab.get_git_user(user_content['email'])
            git_user_pub_key = API.GitLab.get_git_user_ssh_key(git_user['id'])
            if sshKey != git_user_pub_key:
                logger.error(
                    "The SSH Key received does not equal to the one provided! The key from GitLab:\n" + git_user_pub_key)
                raise
            logger.debug(
                "SSH Key for user " + user_content['full_name'] + " added to GitLab.")

    @exception()
    def test_set_ssh(self):

        if settings.DATABASE_TYPE == 'local':
            logger.debug("Local environment, skipping test...")
        else:
            user_content = API.VirtualFunction.create_engagement()
            sshKey = API.User.set_ssh(user_content)
            git_user = API.GitLab.get_git_user(user_content['email'])
            git_user_pub_key = API.GitLab.get_git_user_ssh_key(git_user['id'])
            if sshKey != git_user_pub_key:
                logger.error(
                    "The SSH Key received does not equal to the one provided! The key from GitLab:\n" + git_user_pub_key)
                raise
            logger.debug(
                "SSH Key for user " + user_content['full_name'] + " added to GitLab.")

    @exception()
    def test_invite_member(self):
        if settings.DATABASE_TYPE == 'local':
            logger.debug("Local environment, skipping test...")
        else:
            user_content = API.VirtualFunction.create_engagement()
            invited_email, invite_token, invite_url = API.VirtualFunction.invite_team_member(
                user_content)
            second_user = API.User.signup_invited_user(
                user_content[
                    'vendor'], invited_email, invite_token, invite_url,
                user_content, activate=True)
            APIVirtualFunction.set_eng_stage(
                user_content, Constants.EngagementStages.ACTIVE)
            path_with_namespace = user_content[
                'engagement_manual_id'] + "%2F" + user_content['vfName']
            if not API.GitLab.validate_git_project_members(path_with_namespace, user_content['email']):
                raise Exception(
                    "Couldn't find the inviter user (%s) in GitLab." % user_content['email'])
            if not API.GitLab.validate_git_project_members(path_with_namespace, second_user['email']):
                raise Exception(
                    "Couldn't find the inviter user (%s) in GitLab." % second_user['email'])
            logger.debug(
                "Inviter and invited users were created successfully on GitLab!")

    @exception()
    def test_add_contact(self):
        if settings.DATABASE_TYPE == 'local':
            logger.debug("Local environment, skipping test...")
        else:
            user_content = API.VirtualFunction.create_engagement()
            APIVirtualFunction.set_eng_stage(
                user_content, Constants.EngagementStages.ACTIVE)
            path_with_namespace = user_content[
                'engagement_manual_id'] + "%2F" + user_content['vfName']
            API.GitLab.get_git_project(path_with_namespace)
            if not API.GitLab.validate_git_project_members(path_with_namespace, user_content['email']):
                raise Exception(
                    "Couldn't find the inviter user (%s) in GitLab." % user_content['email'])
            second_user_email, invite_token, invite_url = API.VirtualFunction.add_contact(
                user_content)
            second_user = API.User.signup_invited_user(ServiceProvider.MainServiceProvider, second_user_email, invite_token, invite_url,
                                                       user_content, "true", True)
            if API.GitLab.validate_git_project_members(path_with_namespace, second_user_email):
                logger.debug(
                    "Invited contact user " + second_user['full_name'] + " found in GitLab.")
            else:
                raise Exception("Couldn't find the invited user in GitLab.")
            logger.debug(
                "Inviter and invited users were created successfully on GitLab!")

    @exception()
    def test_join_of_staff_users_to_new_gitlab_repo(self):
        if settings.DATABASE_TYPE == 'local':
            logger.debug("Local environment, skipping test...")
        else:
            user_content = API.VirtualFunction.create_engagement()
            path_with_namespace = user_content[
                'engagement_manual_id'] + "%2F" + user_content['vfName']
            eng_team_users_emails = [
                user_content['el_email'], user_content['pr_email'], Constants.Users.Admin.EMAIL]
            API.GitLab.are_all_list_users_registered_as_project_members(
                eng_team_users_emails, path_with_namespace)
            logger.debug("Staff users were added successfully to GitLab repo!")

    @exception()
    def test_join_of_stn_users_to_new_rep_after_active(self):
        if settings.DATABASE_TYPE == 'local':
            logger.debug("Local environment, skipping test...")
        else:
            user_content = API.VirtualFunction.create_engagement()
            path_with_namespace = user_content[
                'engagement_manual_id'] + "%2F" + user_content['vfName']
            # invite 2 new users in order to join standard users in the eng
            # team
            invited_email_address, invite_token, invite_url = API.VirtualFunction.invite_team_member(
                user_content)
            invited_email_address = API.User.signup_invited_user(user_content['vendor'], invited_email_address,
                                                                 invite_token, invite_url, user_content)

            second_invited_email, second_invite_token, second_invite_url = API.VirtualFunction.invite_team_member(
                user_content)
            second_invited_email = API.User.signup_invited_user(user_content['vendor'], second_invited_email,
                                                                second_invite_token, second_invite_url, user_content)

            API.VirtualFunction.set_eng_stage(
                user_content, Constants.EngagementStages.ACTIVE)
            eng_team_users_emails = [invited_email_address['email'], second_invited_email['email'],
                                     user_content['email'], user_content[
                                         'el_email'], user_content['pr_email'],
                                     Constants.Users.Admin.EMAIL]

            API.GitLab.are_all_list_users_registered_as_project_members(
                eng_team_users_emails, path_with_namespace)
            logger.debug(
                "Staff, Inviter and invited users were added successfully to GitLab repo!")

    @exception()
    def test_rem_users_from_repo_after_active_and_validated(self):
        if settings.DATABASE_TYPE == 'local':
            logger.debug("Local environment, skipping test...")
        else:
            user_content = API.VirtualFunction.create_engagement()
            # invite 2 new users in order to join standard users in the eng
            # team
            invited_email_address, invite_token, invite_url = API.VirtualFunction.invite_team_member(
                user_content)
            invited_email_address = API.User.signup_invited_user(
                user_content['vendor'], invited_email_address, invite_token, invite_url, user_content)

            second_invited_email, second_invite_token, second_invite_url = API.VirtualFunction.invite_team_member(
                user_content)
            second_invited_email = API.User.signup_invited_user(
                user_content['vendor'], second_invited_email, second_invite_token, second_invite_url, user_content)

            # change eng stage in order to include all standard users in the
            # eng git lab repo
            API.VirtualFunction.set_eng_stage(
                user_content, Constants.EngagementStages.ACTIVE)
            API.VirtualFunction.set_eng_stage(
                user_content, Constants.EngagementStages.VALIDATED)
            path_with_namespace = user_content[
                'engagement_manual_id'] + "%2F" + user_content['vfName']

            # check that all standard users, staff users and admin are in the
            # git lab repo
            API.GitLab.get_git_project(path_with_namespace)
            eng_team_users_emails = [user_content['el_email'],
                                     user_content['pr_email'], Constants.Users.Admin.EMAIL]
            should_not_be_in_repo_users_list = [
                invited_email_address['email'], user_content['email']]
            for email in eng_team_users_emails:
                if not API.GitLab.validate_git_project_members(path_with_namespace, email):
                    if email not in should_not_be_in_repo_users_list:
                        raise Exception(
                            "Couldn't find the invited users: " + email + " in GitLab.")

                logger.debug(
                    "Invited user: " + email + " and" + second_invited_email['full_name'] + " found in GitLab.")
            logger.debug(
                "Inviter and invited users were created successfully on GitLab!")

    @exception()
    def test_rem_users_from_repo_after_completed(self):
        if settings.DATABASE_TYPE == 'local':
            logger.debug("Local environment, skipping test...")
        else:
            user_content = API.VirtualFunction.create_engagement()
            # invite 2 new users in order to join standard users in the eng
            # team
            invited_email, invite_token, invite_url = API.VirtualFunction.invite_team_member(
                user_content)
            invited_email = API.User.signup_invited_user(
                user_content['vendor'], invited_email, invite_token, invite_url, user_content)

            second_invited_email, second_invite_token, second_invite_url = API.VirtualFunction.invite_team_member(
                user_content)
            second_invited_email = API.User.signup_invited_user(
                user_content['vendor'], second_invited_email, second_invite_token, second_invite_url, user_content)

            # change eng stage in order to include all standard users in the
            # eng git lab repo
            API.VirtualFunction.set_eng_stage(
                user_content, Constants.EngagementStages.ACTIVE)
            API.VirtualFunction.set_eng_stage(
                user_content, Constants.EngagementStages.VALIDATED)
            API.VirtualFunction.set_eng_stage(
                user_content, Constants.EngagementStages.COMPLETED)
            path_with_namespace = user_content[
                'engagement_manual_id'] + "%2F" + user_content['vfName']

            # check that all standard users, staff users and admin are in the
            # git lab repo
            API.GitLab.get_git_project(path_with_namespace)
            eng_team_users_emails = [user_content['el_email'],
                                     user_content['pr_email'], Constants.Users.Admin.EMAIL]
            should_not_be_in_repo_users_list = [
                invited_email['email'], user_content['email']]
            for email in eng_team_users_emails:
                if not API.GitLab.validate_git_project_members(path_with_namespace, email):
                    if email not in should_not_be_in_repo_users_list:
                        raise Exception(
                            "Couldn't find the user: " + email + " in GitLab.")

                logger.debug(
                    "Invited user: " + email + " and" + second_invited_email['full_name'] + " found in GitLab.")
            logger.debug(
                "Inviter and invited users were created successfully on GitLab!")
