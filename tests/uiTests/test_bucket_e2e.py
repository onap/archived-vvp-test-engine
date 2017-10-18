
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
from pprint import pprint

from wheel.signatures import assertTrue

from iceci.decorator.exception_decor import exception
from services.constants import Constants
from services.database.db_user import DBUser
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.types import API
from tests.uiTests.test_ui_base import TestUiBase
from utils.cryptography import CryptographyText


logger = LoggingServiceFactory.get_logger()


class TestBucketE2E(TestUiBase):

    def create_bucket_and_validate_users(self):
        user_content = API.VirtualFunction.create_engagement(
            wait_for_gitlab=True)
        API.VirtualFunction.set_eng_stage(
            user_content, Constants.EngagementStages.ACTIVE)
        bucket_id = user_content[
            'engagement_manual_id'] + "_" + user_content['vfName'].lower()
        bucket = API.Rados.get_bucket(bucket_id)
        assertTrue(API.Rados.is_bucket_ready(bucket_id))
        assertTrue(bucket != "None")
        assertTrue(API.Rados.users_of_bucket_ready_after_created(
            bucket_id, user_content['full_name']))
        # validate users added to bucket
        grants = API.Rados.get_bucket_grants(bucket_id)
        count = 0
        for g in grants:
            if g.id == user_content['full_name']:
                count = +1

        assertTrue(count > 0)
        return bucket, user_content

    @exception()
    def test_validate_bucket_created(self):
        bucket, user_content = self.create_bucket_and_validate_users()
        # create upload file
        str_content = Helper.rand_string(
            "randomString") + Helper.rand_string("randomNumber")
        fileName = Helper.rand_string("randomString")
        bucket_id = user_content[
            'engagement_manual_id'] + "_" + user_content['vfName'].lower()
        bucket = API.Rados.get_bucket(bucket_id)
        assertTrue(API.Rados.is_bucket_ready(bucket_id))
        key = bucket.new_key(fileName + '.dat')
        key.set_contents_from_string(str_content)
        pprint(key.generate_url(expires_in=400))
#         DOWNLOAD AN OBJECT (TO A FILE)
        key = bucket.get_key(fileName + '.dat')
        key.get_contents_to_filename('/home/' + fileName + '.dat')
        key.delete()

    @exception()
    def test_validate_bucket_removed(self):
        bucket, user_content = self.create_bucket_and_validate_users()
        # set Completed Stage
        API.VirtualFunction.set_eng_stage(
            user_content, Constants.EngagementStages.COMPLETED)
        # validate users removed from bucket
        bucket_id = user_content[
            'engagement_manual_id'] + "_" + user_content['vfName'].lower()
        assertTrue(API.Rados.users_of_bucket_ready_after_complete(
            bucket_id, user_content['full_name']))
        assertTrue(API.Rados.is_bucket_ready(bucket_id))
        assertTrue(bucket != "None")
        # try create upload file - must failed
        str_content = Helper.rand_string(
            "randomString") + Helper.rand_string("randomNumber")
        fileName = Helper.rand_string("randomString")
        bucket = API.Rados.get_bucket(bucket_id)
        assertTrue(API.Rados.is_bucket_ready(bucket_id))
        key = bucket.new_key(fileName + '.dat')
        key.set_contents_from_string(str_content)
        pprint(key.generate_url(expires_in=400))
#         DOWNLOAD AN OBJECT (TO A FILE)
        key = bucket.get_key(fileName + '.dat')
        key.get_contents_to_filename('/home/' + fileName + '.dat')
        key.delete()

    @exception()
    def test_validate_upload_download_image_with_bucket_user(self):
        bucket, user_content = self.create_bucket_and_validate_users()
        # connect to bucket with specific user
        bucket_id = user_content[
            'engagement_manual_id'] + "_" + user_content['vfName'].lower()
        access_key = DBUser.get_access_key(user_content['uuid'])
        secret_key = DBUser.get_access_secret(user_content['uuid'])
        secret = CryptographyText.decrypt(secret_key)
        bucket_for_specific_user = API.Rados.get_bucketfor_specific_user(
            bucket_id, access_key, secret)
        assertTrue(bucket_for_specific_user != None)
        # create upload file with user
        str_content = Helper.rand_string(
            "randomString") + Helper.rand_string("randomNumber")
        fileName = Helper.rand_string("randomString")
        key = bucket_for_specific_user.new_key(fileName + '.dat')
        key.set_contents_from_string(str_content)
        pprint(key.generate_url(expires_in=3600))
#         DOWNLOAD AN OBJECT (TO A FILE)
        key = bucket_for_specific_user.get_key(fileName + '.dat')
        key.get_contents_to_filename('/home/' + fileName + '.dat')
        key.delete()
