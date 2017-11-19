
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
from django.conf import settings

from iceci.decorator.exception_decor import exception
from services.constants import Constants
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.types import API
from tests.apiTests.test_api_base import TestApiBase


logger = LoggingServiceFactory.get_logger()


class TestNegativeRequests(TestApiBase, Helper):

    @exception()
    def test_negative_invite_member(self):
        logger.debug(
            "This negative test will try to invite team " +
            "member to an engagement using other auth token.")
        user_a = API.VirtualFunction.create_engagement()
        user_b = API.VirtualFunction.create_engagement()
        user_a['session_token'] = user_b['session_token']
        try:
            logger.debug(
                "About to invite team member to the engagement of user " +
                user_a['full_name'])
            API.VirtualFunction.invite_team_member(user_a)
            raise Exception(
                user_a['full_name'] +
                " has invited user using other auth token.")
        except BaseException:
            logger.debug(
                "Success! Test failed to invite user using other auth token.")

    @exception()
    def test_negative_add_contact(self):
        logger.debug(
            "This negative test will try to add contact to " +
            "an engagement using other auth token.")
        user_a = API.VirtualFunction.create_engagement()
        user_b = API.VirtualFunction.create_engagement()
        user_a['session_token'] = user_b['session_token']
        try:
            logger.debug(
                "About to invite contact to the engagement of user " +
                user_a['full_name'])
            API.VirtualFunction.add_contact(user_a)
            raise Exception(
                user_a['full_name'] +
                " has invited contact user using other auth token.")
        except BaseException:
            logger.debug(
                "Success! Test failed to invite contact " +
                "user using other auth token.")

    @exception()
    def test_negative_add_next_step(self):
        logger.debug(
            "This negative test will try to add a next step to engagement " +
            "using PR / standard user / admin_ro auth token.")
        user_content = API.VirtualFunction.create_engagement()
        users = [user_content['email'], user_content[
            'pr_email'], Constants.Users.AdminRO.EMAIL]
        for user in users:
            token = "token " + API.User.login_user(user)
            user_content['session_token'] = token
            try:
                logger.debug(
                    "About to add a next step to VF " +
                    user_content['vfName'] +
                    " using " +
                    user +
                    " token.")
                API.VirtualFunction.add_next_step(user_content)
                raise Exception(
                    "Next step was added to VF " +
                    user_content['vfName'] +
                    " using " +
                    user +
                    " token.")
            except BaseException:
                logger.debug(
                    "Success! Test failed to add a new next step to the " +
                    "engagement using other auth token.")

    @exception()
    def test_negative_edit_next_step(self):
        logger.debug(
            "This negative test will try to edit a next step using PR / " +
            "standard user / admin_ro auth token.")
        user_content = API.VirtualFunction.create_engagement()
        token = "token " + API.User.login_user(user_content['el_email'])
        user_content['session_token'] = token
        ns_uuid = API.VirtualFunction.add_next_step(user_content)
        users = [user_content['email'], user_content[
            'pr_email'], Constants.Users.AdminRO.EMAIL]
        for user in users:
            token = "token " + API.User.login_user(user)
            user_content['session_token'] = token
            try:
                logger.debug(
                    "About to edit a next step (ns uuid: " +
                    ns_uuid +
                    ") using " +
                    user +
                    " token.")
                API.VirtualFunction.edit_next_step(user_content, ns_uuid)
                raise Exception(
                    "Next step was edited using " + user + " token.")
            except BaseException:
                logger.debug(
                    "Success! Test failed to edit a next step using " +
                    "other auth token.")

    @exception()
    def test_negative_create_checklist(self):
        user_content = API.VirtualFunction.create_engagement()
        logger.debug(
            "This negative test will try to create a checklist " +
            "using PR / standard user / admin_ro auth token.")
        users = [user_content['email'], user_content[
            'pr_email'], Constants.Users.AdminRO.EMAIL]
        for user in users:
            token = "token " + API.User.login_user(user)
            user_content['session_token'] = token
            try:
                logger.debug(
                    "About to create checklist for VF " +
                    user_content['vfName'])
                API.Checklist.create_checklist(user_content)
                raise Exception(
                    "Checklist was created using " + user + " token.")
            except BaseException:
                logger.debug(
                    "Success! Test failed to create checklist using other " +
                    "auth token.")

    @exception()
    def test_negative_update_checklist(self):
        user_content = API.VirtualFunction.create_engagement()
        API.GitLab.git_clone_push(user_content)
        logger.debug(
            "Create checklist with engagement lead (next: try to edit " +
            "checklist with PR and standard user)")
        token = "token " + API.User.login_user(user_content['el_email'])
        user_content['session_token'] = token
        cl_content = API.Checklist.create_checklist(user_content)
        logger.debug(
            "This negative test will try to create a checklist using PR / " +
            "standard user / admin_ro auth token.")
        users = [user_content['email'], user_content[
            'pr_email'], Constants.Users.AdminRO.EMAIL]
        for user in users:
            token = "token " + API.User.login_user(user)
            user_content['session_token'] = token
            try:
                logger.debug(
                    "About to update checklist for VF " +
                    user_content['vfName'])
                API.Checklist.update_checklist(
                    user_content, cl_content['uuid'])
                raise Exception(
                    "Checklist was created using " + user + " token.")
            except BaseException:
                logger.debug(
                    "Success! Test failed to create checklist using other " +
                    "auth token.")

    @exception()
    def test_negative_set_checklist_state(self):
        user_content = API.VirtualFunction.create_engagement()
        API.GitLab.git_clone_push(user_content)
        logger.debug(
            "Create checklist with engagement lead (next: try to change " +
            "checklist state with PR, standard user and admin_ro)")
        token = "token " + API.User.login_user(user_content['el_email'])
        user_content['session_token'] = token
        cl_content = API.Checklist.create_checklist(user_content)
        logger.debug(
            "This negative test will try to change checklist state using " +
            "PR / standard user / admin_ro auth token.")
        users = [user_content['email'], user_content[
            'pr_email'], Constants.Users.AdminRO.EMAIL]
        for user in users:
            try:
                logger.debug(
                    "About to change checklist state for VF " +
                    user_content['vfName'])
                API.Checklist.jump_state(cl_content['uuid'], user)
                raise Exception(
                    "Checklist state was changed using " + user + " token.")
            except BaseException:
                logger.debug(
                    "Success! Test failed to change checklist state using " +
                    "other auth token.")

    @exception()
    def test_add_checklist_audit_log(self):
        user_content = API.VirtualFunction.create_engagement()
        logger.debug(
            "Create checklist with engagement lead (next: try to add audit " +
            "log to checklist with standard user and admin_ro)")
        token = "token " + API.User.login_user(user_content['el_email'])
        user_content['session_token'] = token
        cl_content = API.Checklist.create_checklist(user_content, files=[])
        logger.debug(
            "This negative test will try to add audit log to checklist " +
            "using standard user / admin_ro auth token.")
        users = [user_content['email'], Constants.Users.AdminRO.EMAIL]
        for user in users:
            token = "token " + API.User.login_user(user)
            user_content['session_token'] = token
            try:
                logger.debug(
                    "About to add audit log to checklist uuid " +
                    cl_content['uuid'])
                API.Checklist.add_checklist_audit_log(
                    user_content, cl_content['uuid'])
                raise Exception(
                    "Audit log was added to checklist using " +
                    user +
                    " token.")
            except BaseException:
                logger.debug(
                    "Success! Test failed to add audit log to checklist " +
                    "using other auth token.")

    @exception()
    def test_add_checklist_next_step(self):
        user_content = API.VirtualFunction.create_engagement()
        API.GitLab.git_clone_push(user_content)
        logger.debug(
            "Create checklist with engagement lead (next: try to add " +
            "checklist next step with PR, standard user and admin_ro)")
        token = "token " + API.User.login_user(user_content['el_email'])
        user_content['session_token'] = token
        cl_content = API.Checklist.create_checklist(user_content)
        logger.debug(
            "This negative test will try to add checklist next step using " +
            "PR / standard user / admin_ro auth token.")
        users = [user_content['email'], user_content[
            'pr_email'], Constants.Users.AdminRO.EMAIL]
        for user in users:
            token = "token " + API.User.login_user(user)
            user_content['session_token'] = token
            try:
                logger.debug(
                    "About to add next step to checklist uuid " +
                    cl_content['uuid'])
                API.Checklist.add_checklist_next_step(
                    user_content, cl_content['uuid'])
                raise Exception(
                    "Next step was added to checklist using " +
                    user +
                    " token.")
            except BaseException:
                logger.debug(
                    "Success! Test failed to add next steps to checklist " +
                    "using other auth token.")

    @exception()
    def test_negative_checklist_files(self):
        # Can't run this test locally since locally we have files by default.
        if settings.DATABASE_TYPE == 'local':
            logger.debug("Local environment, skipping test...")
        else:  # Test starts here #
            user_content = API.VirtualFunction.create_engagement()
            logger.debug(
                "Trying to create checklist with associated files when " +
                "git repo is empty")
            token = "token " + API.User.login_user(user_content['el_email'])
            user_content['session_token'] = token
            try:
                API.Checklist.create_checklist(user_content)
                raise Exception(
                    "Checklist was created with associated files while " +
                    "git repo is empty.")
            except BaseException:
                logger.debug(
                    "Success! Test failed to create checklist with " +
                    "associated files while git repo is empty.")
