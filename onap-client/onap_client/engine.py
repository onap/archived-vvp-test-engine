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
import json

from onap_client.resource import Resource
from onap_client.config import LOG as logger
from onap_client.client.clients import import_submodules
from onap_client.exceptions import InvalidSpecException, ResourceTypeNotFoundException


def dumper(obj):
    try:
        return obj.toJSON()
    except:  # noqa: E722
        return str(obj)


def list_spec_resources():
    for subclass in Resource.__subclasses__():
        print(subclass.resource_name)


def show_resource_spec(resource_name):
    for subclass in Resource.__subclasses__():
        if resource_name == subclass.resource_name:
            print(json.dumps(subclass.spec, default=dumper, indent=4))
            return subclass.spec

    print(
        "Resource {} not found. This is the list of available resources:".format(
            resource_name
        )
    )
    list_spec_resources()


def load_spec(input_spec, validate_only=False):
    try:
        with open(input_spec, "r") as f:
            jdata = json.loads(f.read())
    except json.decoder.JSONDecodeError:
        print("{} is not valid json, exiting...".format(input_spec))
        raise

    engine = SpecEngine()
    return engine.load_spec(jdata, validate_only=validate_only)


def spec_cli(args):
    parser = argparse.ArgumentParser(description="Spec Engine CLI")

    parser.add_argument(
        "--load-spec",
        required=False,
        help="Load a local spec file into the ONAP client spec engine.",
    )

    parser.add_argument(
        "--validate-spec",
        required=False,
        help="Validates a local spec file for the spec engine.",
    )

    parser.add_argument(
        "--show-resource-spec", required=False, help="Show spec for a given resource."
    )

    parser.add_argument(
        "--list-spec-resources",
        action="store_true",
        required=False,
        help="List available spec resources.",
    )

    arguments = parser.parse_args(args)

    if arguments.list_spec_resources:
        list_spec_resources()
    elif arguments.show_resource_spec:
        show_resource_spec(arguments.show_resource_spec)
    elif arguments.validate_spec:
        print(json.dumps(load_spec(arguments.validate_spec, validate_only=True), indent=4))
    elif arguments.load_spec:
        load_spec(arguments.load_spec)


class SpecEngine:
    def __init__(self):
        self.initialize()
        self.spec = {}

    def initialize(self):
        import_submodules("onap_client")

    def load_spec(self, spec, distribute=True, validate_only=False):
        # print("loading spec {}".format(spec))
        self.spec = resolve_spec(spec)
        self.validate(self.spec.get("spec", {}))

        if not validate_only:
            self._create(self.spec.get("spec", {}), distribute)

        return self.spec

    def validate(self, spec):
        if not isinstance(spec, list):
            raise InvalidSpecException(
                "Input spec to spec engine must be a list, but is type {}".format(
                    type(spec)
                )
            )

        for item_spec in spec:
            if not isinstance(item_spec, dict):
                raise InvalidSpecException(
                    "Items in input spec to engine must be dict, but is type {}".format(
                        type(item_spec)
                    )
                )
            resource_type = item_spec.get("type")
            if not resource_type:
                raise InvalidSpecException(
                    "Items in input spec must contain key/value item for 'type:'"
                )
            resource_spec = item_spec.get("resource_spec")
            if not resource_spec:
                raise InvalidSpecException(
                    "Items in input spec must contain key/value item for 'resource_spec:'"
                )
            subclass = get_resource_subclass(resource_type)
            if not subclass:
                raise ResourceTypeNotFoundException(
                    "Resource type {} was not found".format(resource_type)
                )
            subclass.validate(resource_spec)

    def _create(self, spec, distribute):
        full_engine_spec = []
        for item_spec in spec:
            resource_type = item_spec.get("type")
            resource_spec = item_spec.get("resource_spec")
            subclass = get_resource_subclass(resource_type)
            if not subclass:
                raise ResourceTypeNotFoundException(
                    "Resource type {} was not found".format(resource_type)
                )
            full_spec = subclass.validate(resource_spec)
            logger.debug(json.dumps(full_spec, indent=4))
            subclass.create_from_spec(full_spec, submit=distribute)
            full_engine_spec.append({"type": resource_type, "resource_spec": full_spec})

        logger.info(json.dumps(full_engine_spec, indent=4))


def resolve_spec(spec_dict):
    specs = spec_dict.get("spec")
    parameters = spec_dict.get("parameters", {})

    for param_name, param_val in parameters.items():
        specs = replace(specs, "{{{{{}}}}}".format(param_name), param_val)

    spec_dict["spec"] = specs
    return spec_dict


def replace(data, match, repl):
    if isinstance(data, dict):
        return {k: replace(v, match, repl) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace(i, match, repl) for i in data]
    else:
        return repl if data == match else data


def get_resource_subclass(subclass_name):
    for subclass in Resource.__subclasses__():
        if subclass.resource_name == subclass_name:
            return subclass

    return None
