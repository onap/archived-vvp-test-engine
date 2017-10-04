 
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
import logging
import platform
import sys
from timeit import default_timer as timer
import unittest

from pyvirtualdisplay import Display  # For Linux only
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium.webdriver.common.action_chains import ActionChains

from iceci.decorator.logFuncEntry import logFuncEntry
from services.constants import Constants
from services.database.db_general import DBGeneral
from services.logging_service import LoggingServiceFactory
from services.session import session

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logger = LoggingServiceFactory.get_logger()
stream_handler = logging.StreamHandler(sys.stdout)


class TestUiBase(unittest.TestCase):
    windows = []
    one_web_driver_enabled = True

    @classmethod
    def setUpClass(cls):
        super(TestUiBase, cls).setUpClass()
        cls.display = None
        if platform.system() == 'Linux':
            cls.display = Display(visible=0, size=(1920, 1080))
            cls.display.start()

        if cls.one_web_driver_enabled:
            session.setup_driver()

    def go_to_web_page(self, address):
        self.websiteUrl = address

        session.ice_driver.get("about:blank")
        session.ice_driver.get(self.websiteUrl)

    @logFuncEntry
    def setUp(self):
        logger.addHandler(stream_handler)

        self.fullClassName = __name__
        self.className = self.__class__.__name__
        logger.debug("---------------------- TestCase - Start - Class " +
                     self.className + " Function " + self._testMethodName + " ----------------------")

        self.ice_driver = session.get_driver()

        if not self.one_web_driver_enabled:
            self.ice_driver = session.setup_driver()
        elif self.ice_driver is None:
            self.ice_driver = session.setup_driver()

        self.go_to_web_page(Constants.Default.LoginURL.TEXT)

        session.ice_driver.implicitly_wait(session.wait_until_implicit_time)
        self.actions = ActionChains(self.ice_driver)
        self.windows.append(session.ice_driver.window_handles[0])
        session.ice_driver.maximize_window()

        self.startTime = timer()
        self.funcName = self._testMethodName
        self.testName = self.funcName

    @logFuncEntry
    def tearDown(self):
        self.endTime = timer()
        self.testDuration = str(self.endTime - self.startTime)
        self.results()
        if self.one_web_driver_enabled is None or not self.one_web_driver_enabled:
            session.ice_driver.quit()
        else:
            self.go_to_web_page(Constants.Default.LoginURL.TEXT)
        logger.debug("---------------------- TestCase - End - Class " + self.className +
                     " Function " + self._testMethodName + " ----------------------\n")
        try:
            logging.getLogger().info("BB")
        finally:
            logger.removeHandler(stream_handler)
            session.errorList = ""
            session.errorCounter = 0

    @classmethod
    def tearDownClass(cls):
        session.close_driver()
        if cls.display:
            cls.display.stop()
        super(TestUiBase, cls).tearDownClass()

    @logFuncEntry
    def results(self):
        params = {"testType": "E2E Test", "testFeature": self.className,
                  "testResult": "PASS", "testName": self.funcName, "duration": self.testDuration}
        if (session.errorCounter == 0):
            DBGeneral.insert_results(params["testType"], params["testFeature"], params[
                                     "testResult"], params["testName"], params['duration'])
        else:
            params["testResult"] = "FAIL"  # Mark test as fail.
            # Add the errors to notes column in table.
            params["notes"] = session.errorList
            DBGeneral.insert_results(params["testType"], params["testFeature"], params[
                                     "testResult"], params["testName"], params['duration'], params["notes"])
