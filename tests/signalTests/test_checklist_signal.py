 
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
from services.constants import Constants
from services.logging_service import LoggingServiceFactory
from services.types import API, DB
from tests.signalTests.test_signal_base import TestSignalBase


logger = LoggingServiceFactory.get_logger()


class TestChecklistSignal(TestSignalBase):

    @exception()
    def test_archive_checklist_after_editing_files(self):
        if settings.DATABASE_TYPE == 'local':
            logger.debug("Local environment, skipping test...")
        else:
            user_content = API.VirtualFunction.create_engagement()
            API.GitLab.git_clone_push(user_content, yaml=True)
            token = "token " + API.User.login_user(user_content['el_email'])
            user_content['session_token'] = token
            cl_content = API.Checklist.retrieve_heat_checklist(user_content)
            API.GitLab.git_push_commit(user_content, yaml=True)
            DB.Checklist.state_changed(
                "uuid", cl_content['uuid'], Constants.ChecklistStates.Archive.TEXT)
