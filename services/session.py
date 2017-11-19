
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
from selenium import webdriver


class SessionSingletone():
    positive_wait_until_retires = 60
    positive_wait_until_time_pause = 0.5
    positive_wait_until_time_pause_long = 1.5
    positive_wait_until_implicit_time = 10
    positive_timeout = 10

    negative_wait_until_retires = 5
    negative_wait_until_time_pause = 0.5
    negative_wait_until_implicit_time = 0.5
    negative_timeout = 5

    errorCounter = 0
    errorList = ""
    createTemplatecount = False

    def __init__(self):
        self.wait_until_retires = self.positive_wait_until_retires
        self.wait_until_time_pause = self.positive_wait_until_time_pause
        self.wait_until_time_pause_long = \
            self.positive_wait_until_time_pause_long
        self.wait_until_implicit_time = self.positive_wait_until_implicit_time
        self.test = '123'
        self.ice_driver = None

    def setup_driver(self):
        self.ice_driver = webdriver.Firefox()
        return self.ice_driver

    def get_driver(self):
        return self.ice_driver

    def close_driver(self):
        self.ice_driver.quit()
        self.ice_driver = None

    def start_negative(self):
        """Changing parameters to reduce negative tests run-time"""
        self.wait_until_retires = self.negative_wait_until_retires
        self.wait_until_time_pause = self.negative_wait_until_time_pause
        self.wait_until_implicit_time = self.negative_wait_until_implicit_time
        self.timeout = self.negative_timeout
        session.ice_driver.implicitly_wait(self.wait_until_implicit_time)

    def end_negative(self):
        """Change back the parameters to suite positive tests"""
        self.wait_until_retires = self.positive_wait_until_retires
        self.wait_until_time_pause = self.positive_wait_until_time_pause
        self.wait_until_implicit_time = self.positive_wait_until_implicit_time
        self.timeout = self.positive_timeout
        session.ice_driver.implicitly_wait(self.wait_until_implicit_time)

    def run_negative(self, run_me, error_msg):
        self.start_negative()
        try:
            run_me()  # click.css
        except BaseException:
            # will run if click does NOT succeed
            self.errorCounter = 0
            self.errorList = ""
        else:
            # will run if click SUCCEED
            raise Exception(error_msg)
        self.end_negative()


session = SessionSingletone()
