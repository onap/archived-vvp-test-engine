 
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
Created on 20 Jul 2017
'''
from services.constants import Constants
from services.frontend.base_actions.click import Click
from services.frontend.base_actions.wait import Wait


class FENextStep(object):

    @staticmethod
    def check_select_deselect_all_files():
        Click.id(Constants.Dashboard.Overview.NextSteps.Add.AssociatedFiles.ID)
        Click.link_text(
            Constants.Dashboard.Overview.NextSteps.Add.AssociatedFiles.SELECT_ALL_FILES_NAME)
        Wait.text_by_id(
            Constants.Dashboard.Overview.NextSteps.Add.AssociatedFiles.ID,
            Constants.Dashboard.Overview.NextSteps.Add.AssociatedFiles.ALL_FILES_SELECTED)
