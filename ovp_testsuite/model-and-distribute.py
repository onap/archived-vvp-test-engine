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
import copy
import json
import sys

from onap_client.engine import SpecEngine
from onap_client.exceptions import ResourceAlreadyExistsException
from zipfile import ZipFile
from os import listdir
from os.path import isfile, join


def run_engine(spec):
  engine = SpecEngine()

  engine.load_spec(spec)

  return engine.spec

def load_spec(spec):
  with open(spec, "r") as f:
    jdata = json.loads(f.read())

  return jdata

def create_heat_zip(filepath, output_path):
  onlyfiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]

  with ZipFile(output_path, 'w') as zipObj:
    for filename in onlyfiles:
      zipObj.write(join(filepath, filename), arcname=filename)

def resolve_spec(vnf_details, blank_spec, build_tag, heat_zip, vnf_folder):
  blank_spec["parameters"]["vendor_name"] = "vendor{}".format(build_tag)
  blank_spec["parameters"]["software_product_name"] = "vsp{}".format(build_tag)
  blank_spec["parameters"]["file_path"] = heat_zip
  blank_spec["parameters"]["vnf_name"] = "vnf{}".format(build_tag)
  blank_spec["parameters"]["service_name"] = "service{}".format(build_tag)
  blank_spec["parameters"]["service_instance_name"] = "SI{}".format(build_tag)
  blank_spec["parameters"]["vnf_instance_name"] = "SI_VNF{}".format(build_tag)
  blank_spec["parameters"]["tenant_name"] = vnf_details.get("tenant_name")
  blank_spec["parameters"]["cloud_owner"] = vnf_details.get("cloud_owner")
  blank_spec["parameters"]["cloud_region"] = vnf_details.get("region_id")
  blank_spec["parameters"]["api_type"] = vnf_details.get("api_type").upper()
  blank_spec["parameters"]["service_type"] = vnf_details.get("service_type")
  blank_spec["parameters"]["customer_name"] = vnf_details.get("customer")
  blank_spec["parameters"]["project_name"] = vnf_details.get("project_name")
  blank_spec["parameters"]["platform"] = vnf_details.get("platform")
  blank_spec["parameters"]["owning_entity_name"] = vnf_details.get("owning_entity")
  blank_spec["parameters"]["line_of_business"] = vnf_details.get("line_of_business")

  for module in vnf_details.get("modules"):
    blank_spec["spec"].append(resolve_module(module, vnf_folder, build_tag))
  
  return blank_spec


def resolve_module(module, vnf_folder, build_tag):
  module_spec = {"type": "MODULE_INSTANCE", "resource_spec": {}}
  module_spec["resource_spec"]["module_instance_name"] = "SI_VNF_{}_{}".format(build_tag, module.get("filename").split(".")[0])
  module_spec["resource_spec"]["heat_template_name"] = module.get("filename")
  module_spec["resource_spec"]["preload_path"] = "{}/preloads/{}".format(vnf_folder, module.get("preload"))
  module_spec["resource_spec"]["vnf_instance_name"] = "{{vnf_instance_name}}"
  module_spec["resource_spec"]["service_instance_name"] = "{{service_instance_name}}"
  module_spec["resource_spec"]["tenant_name"] = "{{tenant_name}}"
  module_spec["resource_spec"]["cloud_owner"] = "{{cloud_owner}}"
  module_spec["resource_spec"]["cloud_region"] = "{{cloud_region}}"
  module_spec["resource_spec"]["api_type"] = "{{api_type}}"

  return module_spec


def create_stack_details(full_spec, vnf_folder, build_tag):
  resources = full_spec.get("spec")
  stack_data = []
  for resource in resources:
    if resource.get("type") == "MODULE_INSTANCE":
      module_data = {}
      module = resource.get("resource_spec")
      module_data["template_name"] = "{}/templates/{}".format(vnf_folder, module.get("heat_template_name"))
      module_data["preload_name"] = "{}".format(module.get("preload_path"))
      module_data["stack_name"] = "{}".format(module.get("module_instance_name"))
      stack_data.append(module_data)

  with open("/tmp/vnf-deployment-details-{}.json".format(build_tag), "w") as f:
    json.dump(stack_data, f, indent=4)

def main(vnf_folder, spec, build_tag):
  modeling_spec = load_spec(spec)
  vnf_details = load_spec("{}/vnf-details.json".format(vnf_folder))
  heat_zip = "/tmp/heat{}.zip".format(build_tag)
  create_heat_zip("{}/templates".format(vnf_folder), heat_zip)

  spec = resolve_spec(vnf_details, modeling_spec, build_tag, heat_zip, vnf_folder)

  print(json.dumps(spec, indent=4))

  full_spec = run_engine(spec)

  return full_spec

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="VNF Modeling Script")

  parser.add_argument(
      "--vnf-folder",
      required=True,
      help="Full path to the folder containing preloads, templates, and vnf-details.json.",
  )

  parser.add_argument(
      "--spec",
      required=True,
      help="Full path to the blank spec for modeling and instantiating a VNF.",
  )

  parser.add_argument(
      "--build-tag",
      required=True,
      help="Unique build tag.",
  )

  arguments = parser.parse_args()

  vnf_folder = arguments.vnf_folder
  spec = arguments.spec
  build_tag = arguments.build_tag

  full_spec = main(vnf_folder, spec, build_tag)

  create_stack_details(full_spec, vnf_folder, build_tag)
