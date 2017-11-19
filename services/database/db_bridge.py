
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


class DBBridge:

    """
    This class helps to use functions inside classes
    with circular import (dependencies).
    Use this class only when there is circular
    import in one of the DB services.
    """

    @staticmethod
    def select_personal_next_step(user_email):
        """select_personal_next_step: Originally """ +\
            """can be found under DBUser class."""
        from services.database.db_user import DBUser
        return DBUser.select_personal_next_step(user_email)

    @staticmethod
    def helper_rand_string(type, num=""):
        from services.helper import Helper
        return Helper.rand_string(type, num)

    @staticmethod
    def helper_internal_assert(arg1, arg2):
        from services.helper import Helper
        return Helper.internal_assert(arg1, arg2)
