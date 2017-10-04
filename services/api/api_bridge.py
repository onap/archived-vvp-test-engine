 
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
class APIBridge:

    """
    This class helps to use functions inside classes with circular import (dependencies).
    Use this class only when there is circular import in one of the API services.
    """

    @staticmethod
    def is_gitlab_ready(user_content):
        """is_gitlab_ready: Originally can be found under APIGitLab class."""
        from services.api.api_gitlab import APIGitLab
        return APIGitLab.is_gitlab_ready(user_content)

    @staticmethod
    def login_user(email):
        """login_user: Originally can be found under APIUser class."""
        from services.api.api_user import APIUser
        return APIUser.login_user(email)

    @staticmethod
    def set_ssh(user_content, sshKey):
        """set_ssh: Originally can be found under APIUser class."""
        from services.api.api_user import APIUser
        return APIUser.set_ssh(user_content, sshKey)

    @staticmethod
    def create_engagement(wait_for_gitlab=True):
        """create_engagement: Originally can be found under APIVirtualFunction class."""
        from services.api.api_virtual_function import APIVirtualFunction
        return APIVirtualFunction.create_engagement(wait_for_gitlab)

    @staticmethod
    def frontend_login(email, password):
        """login: Originally can be found under FEUser class."""
        from services.frontend.fe_user import FEUser
        return FEUser.login(email, password)
