 
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
from services.api.api_bridge import APIBridge
from services.api.api_checklist import APIChecklist
from services.api.api_gitlab import APIGitLab
from services.api.api_jenkins import APIJenkins
from services.api.api_user import APIUser
from services.api.api_virtual_function import APIVirtualFunction
from services.database.db_checklist import DBChecklist
from services.database.db_cms import DBCMS
from services.database.db_general import DBGeneral
from services.database.db_user import DBUser
from services.database.db_virtual_function import DBVirtualFunction
from services.frontend.fe_checklist import FEChecklist
from services.frontend.fe_cms import FECms
from services.frontend.fe_dashboard import FEDashboard
from services.frontend.fe_detailed_view import FEDetailedView
from services.frontend.fe_general import FEGeneral
from services.frontend.fe_invite import FEInvite
from services.frontend.fe_overview import FEOverview
from services.frontend.fe_user import FEUser
from services.frontend.fe_wizard import FEWizard
from services.frontend.fe_checklist_template import FEChecklistTemplate
from services.api.api_rados import APIRados


class Frontend:
    User = FEUser()
    Invite = FEInvite()
    Checklist = FEChecklist()
    Dashboard = FEDashboard()
    DetailedView = FEDetailedView()
    General = FEGeneral()
    Overview = FEOverview()
    Wizard = FEWizard()
    Cms = FECms()
    ChecklistTemplate = FEChecklistTemplate()


class API:
    Bridge = APIBridge()
    Checklist = APIChecklist()
    GitLab = APIGitLab()
    Jenkins = APIJenkins()
    Rados = APIRados
    User = APIUser()
    VirtualFunction = APIVirtualFunction()


class DB:
    Checklist = DBChecklist()
    Cms = DBCMS()
    General = DBGeneral()
    User = DBUser()
    VirtualFunction = DBVirtualFunction()
