# -*- coding: utf8 -*-
# ============LICENSE_START=======================================================
# org.onap.vvp/validation-scripts
# ===================================================================
# Copyright © 2020 AT&T Intellectual Property. All rights reserved.
# ===================================================================
#
# Unless otherwise specified, all software contained herein is licensed
# under the Apache License, Version 2.0 (the "License");
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
# under the Creative Commons License, Attribution 4.0 Intl. (the "License");
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
import datetime
import hashlib
import json
import os
import argparse
import time
import uuid

from copy import deepcopy
from zipfile import ZipFile

OUTPUT_DATA = {
    "vnf_checksum": "",
    "build_tag": str(uuid.uuid4()),
    "version": "2019.12",
    "test_date": "",
    "duration": "",
    "vnf_type": "heat",
    "testcases_list": [
        {
            "mandatory": "true",
            "name": "onap-vvp.validate.heat",
            "result": "NOT_STARTED",
            "objective": "onap heat template validation",
            "sub_testcase": [],
            "portal_key_file": "report.json",
        },
        {
            "mandatory": "true",
            "name": "onap-vvp.lifecycle_validate.heat",
            "result": "NOT_STARTED",
            "objective": "onap vnf lifecycle validation",
            "sub_testcase": [
                {"name": "model-and-distribute", "result": "NOT_STARTED"},
                {"name": "instantiation", "result": "NOT_STARTED"},
            ],
            "portal_key_file": "log.txt",
        },
        {
            "mandatory": "true",
            "name": "stack_validation",
            "result": "NOT_STARTED",
            "objective": "onap vnf openstack validation",
            "sub_testcase": [],
            "portal_key_file": "stack-validation.json",
        },
    ],
}


class OVPListener:
    def __init__(
        self,
        template_directory,
        start_time,
        test_date
    ):
        self.report = deepcopy(OUTPUT_DATA)
        self.test_date = test_date
        self.build_directory = template_directory
        self.output_directory = "/tmp"
        self.start_time = int(start_time)

        self.initialize()

    def initialize(self):
        self.template_directory = self.build_directory
        self.report["vnf_checksum"] = sha256(self.template_directory)
        self.report["test_date"] = self.test_date
        self.report["duration"] = (int(time.time()) - self.start_time)

    def update_validation_scripts(self, status):
        self.report["testcases_list"][0]["result"] = status

    def update_model_and_distribute(self, status):
        self.report["testcases_list"][1]["sub_testcase"][0]["result"] = status
        self.report["testcases_list"][1]["sub_testcase"][1]["result"] = status
        self.report["testcases_list"][1]["result"] = status

    def update_stack_validation(self, status):
        self.report["testcases_list"][2]["result"] = status

    def close(self):
        with open("{}/results.json".format(self.output_directory), "w") as f:
            json.dump(self.report, f, indent=4)


def sha256(template_directory):
    heat_sha = None

    if os.path.exists(template_directory):
        zip_file = "{}/tmp_heat.zip".format(template_directory)
        with ZipFile(zip_file, "w") as zip_obj:
            for folder_name, subfolders, filenames in os.walk(template_directory):
                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)
                    zip_obj.write(file_path)

        with open(zip_file, "rb") as f:
            bytes = f.read()
            heat_sha = hashlib.sha256(bytes).hexdigest()

        os.remove(zip_file)

    return heat_sha

def main(
        template_directory,
        start_time,
        test_date,
        validation_scripts="NOT_STARTED",
        stack_validation="NOT_STARTED",
        model_and_distribute="NOT_STARTED",
    ):
    t = OVPListener(template_directory, start_time, test_date)
    t.update_validation_scripts(validation_scripts)
    t.update_model_and_distribute(model_and_distribute)
    t.update_stack_validation(stack_validation)
    t.close()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Stack Validation Script")

  parser.add_argument(
      "--validation-scripts",
      required=False,
      choices=["SUCCESS", "FAIL", "NOT_STARTED"],
      default="NOT_STARTED",
      help="Validation Script Status.",
  )

  parser.add_argument(
      "--model-and-distribute",
      required=False,
      choices=["SUCCESS", "FAIL", "NOT_STARTED"],
      default="NOT_STARTED",
      help="Modeling Script Status.",
  )

  parser.add_argument(
      "--stack-validation",
      required=False,
      choices=["SUCCESS", "FAIL", "NOT_STARTED"],
      default="NOT_STARTED",
      help="Stack Validation Script Status.",
  )

  parser.add_argument(
      "--test-date",
      required=True,
      help="Test Date.",
  )

  parser.add_argument(
      "--template-directory",
      required=True,
      help="Heat Template Directory.",
  )

  parser.add_argument(
      "--start-time",
      required=True,
      help="Epoch start time.",
  )

  arguments = parser.parse_args()

  status = main(
    arguments.template_directory,
    arguments.start_time,
    arguments.test_date,
    validation_scripts=arguments.validation_scripts,
    stack_validation=arguments.stack_validation,
    model_and_distribute=arguments.model_and_distribute,
  )
