
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
import time

from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from django.conf import settings

from rados.rgwa_client_factory import RGWAClientFactory
from services.constants import Constants
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()


class APIRados:

    @staticmethod
    def get_bucket(name):
        """Return the Bucket."""
        boto_conn = RGWAClientFactory.standard()
        try:
            return boto_conn.lookup(name)
        except Exception as e:
            logger.error("Problem on get bucket", e)
            raise e

    @staticmethod
    def get_bucketfor_specific_user(name, access_key_id, secret_access_key):
        """Return the Bucket."""
        boto_conn = APIRados.specific_client(access_key_id, secret_access_key)
        try:
            return boto_conn.lookup(name)
        except Exception as e:
            logger.error("Problem on get bucket for specific user", e)
            raise e

    @staticmethod
    def get_bucket_grants(bucket_name):
        """Return the Grants."""
        for counter in range(Constants.RGWAConstants.BUCKET_RETRIES_NUMBER):
            bucket = APIRados.get_bucket(bucket_name)
            if bucket:
                break
            logger.error("Bucket not found. Retry #%s" % counter+1)
            time.sleep(session.wait_until_time_pause_long)
        else:
            raise TimeoutError("Max retries exceeded, failing test...")
        grants = bucket.list_grants()
        return grants

    @staticmethod
    def is_bucket_ready(bucket_id):
        for counter in range(Constants.RGWAConstants.BUCKET_RETRIES_NUMBER):
            bucket = APIRados.get_bucket(bucket_id)
            if bucket:
                break
            logger.debug(
                "bucket are not ready yet, trying again (%s of %s)" % (
                    counter+1, Constants.RGWAConstants.BUCKET_RETRIES_NUMBER))
            time.sleep(session.wait_until_time_pause_long)
        else:
            raise TimeoutError("Max retries exceeded, failing test...")
        logger.debug("bucket are ready to continue!")
        return True

    @staticmethod
    def users_of_bucket_ready_after_complete(bucket_id, user_name):
        for counter in range(Constants.RGWAConstants.BUCKET_RETRIES_NUMBER):
            grants = APIRados.get_bucket_grants(bucket_id)
            if not any(user_name == g.id for g in grants):
                break
            time.sleep(session.wait_until_time_pause_long)
        else:
            raise Exception("Max retries exceeded, failing test...")
            return False
        logger.debug("users_of_bucket are ready to continue!")
        return True

    @staticmethod
    def users_of_bucket_ready_after_created(bucket_id, user_uuid):
        for counter in range(Constants.RGWAConstants.BUCKET_RETRIES_NUMBER):
            grants = APIRados.get_bucket_grants(bucket_id)
            if any(user_uuid == g.id for g in grants):
                break
            time.sleep(session.wait_until_time_pause_long)
        else:
            raise Exception("Max retries exceeded, failing test...")
        logger.debug("users_of_bucket are ready to continue!")
        return True

    @staticmethod
    def specific_client(access_key_id, secret_access_key):
        boto_conn = S3Connection(
            host=settings.AWS_S3_HOST,
            port=settings.AWS_S3_PORT,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            calling_format=OrdinaryCallingFormat(),
            is_secure=True,)

        boto_conn.num_retries = 0
        return boto_conn
