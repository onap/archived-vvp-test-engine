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
import argparse
import os
import subprocess
import sys

VVP_BRANCH = "master"
VVP_URL = "https://gerrit.onap.org/r/vvp/validation-scripts"


# use this to import and run validation from robot
class HeatValidationScripts:
    def __init__(self):
        pass

    def validate(self, build_dir, template_directory, output_directory):
        """
        :build_dir:                 directory to install virtualenv
                                    and clone validation scripts
        :template_directory:        directory with heat templates
        :output_directory:          directory to store output files
        """
        t = VVP(build_dir, template_directory, output_directory)
        t.install_requirements()
        status = t.run_vvp()

        return status


class VVP:
    def __init__(self, build_dir, template_directory, output_directory):
        self._build_dir = build_dir
        self.initialize()

        self.virtualenv = "{}/test_env".format(build_dir)
        self.vvp = "{}/validation_scripts".format(build_dir)
        self.template_directory = template_directory
        self.output_directory = output_directory

    def initialize(self):
        self.create_venv(self._build_dir)
        self.clone_vvp(self._build_dir)

    def create_venv(self, build_dir):
        if not os.path.exists("{}/test_env".format(build_dir)):
            try:
                subprocess.call(
                    ["python3.7", "-m", "virtualenv", "--clear", "{}/test_env".format(build_dir)]
                )
            except OSError as e:
                print("error creating virtual environment for vvp {}".format(e))
                raise

    def clone_vvp(self, build_dir):
        if not os.path.exists("{}/validation_scripts".format(build_dir)):
            try:
                subprocess.call(
                    [
                        "git",
                        "clone",
                        "-b",
                        VVP_BRANCH,
                        VVP_URL,
                        "{}/validation_scripts".format(build_dir),
                    ]
                )
            except OSError as e:
                print("error cloning vvp validation scripts {}".format(e))
                raise

    def install_requirements(self):
        try:
            subprocess.call(
                [
                    "{}/bin/python".format(self.virtualenv),
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    "pip",
                    "wheel",
                ]
            )
            subprocess.call(
                [
                    "{}/bin/python".format(self.virtualenv),
                    "-m",
                    "pip",
                    "install",
                    "wheel",
                    "-r",
                    "{}/requirements.txt".format(self.vvp),
                ]
            )
        except OSError as e:
            print("error installing vvp requirements {}".format(e))
            raise

    def run_vvp(self):
        try:
            ret = subprocess.call(
                [
                    "{}/bin/python".format(self.virtualenv),
                    "-m",
                    "pytest",
                    "--rootdir={}/ice_validator/".format(self.vvp),
                    "--template-directory={}".format(self.template_directory),
                    "--output-directory={}".format(self.output_directory),
                    "--category=environment_file",
                    "--category=openstack",
                    "{}/ice_validator/tests/".format(self.vvp),
                ]
            )
        except OSError as e:
            print("error running vvp validation scripts {}".format(e))
            raise

        if ret != 0:
            raise ValueError("Validation Script error detected")

def main(build_directory, template_directory, output_directory):
    t = HeatValidationScripts()
    t.validate(build_directory, template_directory, output_directory)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--template-directory",
        required=True,
        help="Directory that contains heat templates.",
    )

    parser.add_argument(
        "--output-directory",
        required=True,
        help="Directory to store output.",
    )

    parser.add_argument(
        "--build-directory",
        required=False,
        default="/tmp/vvpbuild",
        help="Directory to store install venv.",
    )

    arguments = parser.parse_args()

    main(arguments.build_directory, arguments.template_directory, arguments.output_directory)
