 
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
from wheel.signatures import assertTrue

from iceci.decorator.exception_decor import exception
from services.constants import Constants
from services.logging_service import LoggingServiceFactory
from services.types import API
from tests.uiTests.test_ui_base import TestUiBase

logger = LoggingServiceFactory.get_logger()


class TestRadosPermissions(TestUiBase):
    
    def create_bucket_and_validate_users(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=True)

        print("***********STAGE = ",user_content['vfStage'])
        API.VirtualFunction.set_eng_stage(user_content, Constants.EngagementStages.ACTIVE)
        bucket_id = user_content['engagement_manual_id'] + "_" + user_content['vfName'].lower()
        bucket = API.Rados.get_bucket(bucket_id)
        assertTrue(API.Rados.is_bucket_ready(bucket_id))
        assertTrue(bucket != "None")
        #validate users added to bucket
        grants = API.Rados.get_bucket_grants(bucket_id)
        count = 0
        for g in grants:
            if g.id == user_content['full_name']: 
                count = +1
        
        assertTrue(count > 0)
        return bucket, user_content

    @exception()
    def test_permissions_stage_validated(self):
        bucket, user_content = self.create_bucket_and_validate_users()
        API.VirtualFunction.set_eng_stage(user_content, Constants.EngagementStages.VALIDATED)
        bucket_id = user_content['engagement_manual_id'] + "_" + user_content['vfName'].lower()
        assertTrue(API.Rados.users_of_bucket_ready_after_complete(bucket_id, user_content['full_name']))
        bucket = API.Rados.get_bucket(bucket_id)
        assertTrue(API.Rados.is_bucket_ready(bucket_id))
        assertTrue(bucket != "None")
        assertTrue(API.Rados.is_bucket_ready(bucket_id))
        bucket = API.Rados.get_bucket(bucket_id)
        grants = API.Rados.get_bucket_grants(bucket_id)
        print("\nBucket:", bucket)
        print("\nBucket Type:", type(bucket))
        print("\nGrants:", grants)
        print("\nGrants Type:", type(grants))
        print("done")

    @exception()
    def test_permissions_stage_completed(self):
        bucket, user_content = self.create_bucket_and_validate_users()
        API.VirtualFunction.set_eng_stage(
            user_content, Constants.EngagementStages.COMPLETED)
        bucket_id = user_content['engagement_manual_id'] + "_" + user_content['vfName'].lower()
        assertTrue(API.Rados.users_of_bucket_ready_after_complete(bucket_id, user_content['full_name']))
        assertTrue(API.Rados.is_bucket_ready(bucket_id))
        bucket = API.Rados.get_bucket(bucket_id)
        grants = API.Rados.get_bucket_grants(bucket_id)
        print("\nBucket:", bucket)
        print("\nBucket Type:", type(bucket))
        print("\nGrants:", grants)
        print("\nGrants Type:", type(grants))
        print("done")
