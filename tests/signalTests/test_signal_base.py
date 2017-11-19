
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
Created on 15 Nov 2016

@author: tomerc
'''
import sys
from timeit import default_timer as timer
import unittest
import logging
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from iceci.decorator.logFuncEntry import logFuncEntry
from services.database.db_general import DBGeneral
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.session import session


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


logger = LoggingServiceFactory.get_logger()
stream_handler = logging.StreamHandler(sys.stdout)


class TestSignalBase(unittest.TestCase, Helper):

    def setUp(self):
        logger.addHandler(stream_handler)
        self.fullClassName = __name__
        self.className = self.__class__.__name__
        logger.debug("---------------------- TestCase " +
                     self.className + " ----------------------")

        self.startTime = timer()
        self.funcName = self._testMethodName
        self.testName = self.funcName

    def tearDown(self):
        self.endTime = timer()
        self.testDuration = str(self.endTime - self.startTime)
        self.results()
        logger.debug("---------------------- TestCase " +
                     self.className + " ----------------------\n\n")
        try:
            logging.getLogger().info("BB")
        finally:
            logger.removeHandler(stream_handler)
            session.errorList = ""
            session.errorCounter = 0

    @logFuncEntry
    def results(self):
        params = {
            "testType": "E2E Test",
            "testFeature": self.className,
            "testResult": "PASS",
            "testName": self.funcName,
            "duration": self.testDuration}
        if (session.errorCounter == 0):
            DBGeneral.insert_results(
                params["testType"],
                params["testFeature"],
                params["testResult"],
                params["testName"],
                params['duration'])
        else:
            params["testResult"] = "FAIL"  # Mark test as fail.
            # Add the errors to notes column in table.
            params["notes"] = session.errorList
            DBGeneral.insert_results(
                params["testType"],
                params["testFeature"],
                params["testResult"],
                params["testName"],
                params['duration'],
                params["notes"])
