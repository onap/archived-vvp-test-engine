
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
from requests.auth import HTTPBasicAuth
from services.constants import Constants
from services.helper import Helper
from services.session import session
import logging
import requests
import time


logger = logging.getLogger('ice-ci.logger')


class APIJenkins:

    @staticmethod
    def get_jenkins_job(job_name):
        r1 = None
        counter = 0
        getURL = settings.JENKINS_URL + "job/" + job_name
        logger.debug("Get APIJenkins job URL: " + getURL)
        try:
            r1 = requests.get(getURL, auth=HTTPBasicAuth(
                settings.JENKINS_USERNAME, settings.JENKINS_PASSWORD))
            while r1.status_code != 200 and counter <= \
                    Constants.GitLabConstants.RETRIES_NUMBER:
                r1 = requests.get(getURL, auth=HTTPBasicAuth(
                    settings.JENKINS_USERNAME, settings.JENKINS_PASSWORD))
                time.sleep(session.wait_until_time_pause)
                logger.debug(
                    "try to get jenkins job (try #%s)" % counter)
                counter += 1
            Helper.internal_assert(r1.status_code, 200)
            logger.debug("Job was created on APIJenkins!")
        except BaseException:
            msg = None

            if r1 is None:
                msg = "APIJenkins didn't create job for %s" % job_name
            else:
                msg = "APIJenkins didn't create job for %s, " +\
                    "see response >>> %s %s" % (
                        job_name, r1.status_code, r1.reason)

            logger.error(msg)
            raise Exception(msg)

    @staticmethod
    def find_build_num_out_of_jenkins_log(log):
        lines_array = log.splitlines()
        for line in lines_array:
            if Constants.Dashboard.Checklist.JenkinsLog.\
                    Modal.Body.BUILD_IDENTIFIER in line:
                parts = line.partition('jenkins')
                return parts[2]
