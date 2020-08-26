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

import json
import logging

from prettytable import PrettyTable
from onap_client.client.clients import get_client as Client
from onap_client.client.catalog import Catalog
from onap_client.engine import spec_cli
from onap_client.util import utility_cli, get_actions


def main(*args):
    cli_arguments = list(args)
    request_arguments = {}

    oc = Client()
    configure_logging()

    if len(args) > 0 and args[0] == "spec-engine":
        # use engine cli instead
        spec_cli(cli_arguments[1:])
    elif len(args) > 0 and convert_to_underscores(args[0]) in oc.utility_functions:
        # use utility cli instead
        utility_cli(oc, cli_arguments)
    elif len(args) == 0 or args[0] == "--help":
        print(help(oc, extra_clients=["spec-engine"], include_utility=True))
    else:
        while cli_arguments:
            arg = cli_arguments.pop(0)

            if arg == "--help":
                print(help(oc))
                return

            if is_argument(arg):
                arg = convert_to_underscores(arg)
                arg = sanitize_argument(arg)
                try:
                    value = get_value(cli_arguments.pop(0))
                    if is_argument(value):
                        print(
                            "No Value passed for argument: {}. Try --help".format(arg)
                        )
                        return
                except IndexError:
                    print("No Value passed for argument: {}. Try --help".format(arg))
                    return

                request_arguments[arg] = value
            else:
                arg = convert_to_underscores(arg)
                oc = getattr(oc, arg, None)
                if not oc:
                    print("Invalid Argument: {}. Try --help".format(arg))
                    return

        if isinstance(oc, Catalog.CallHandle):
            data = oc(**request_arguments)

            output_data = data.response_data

            if isinstance(output_data, dict) or isinstance(output_data, list):
                print(json.dumps(output_data, indent=4))
            else:
                print(output_data)
        else:
            print("Command Invalid: {}. Try --help".format(args))


def is_argument(argument):
    return argument.startswith("--")


def sanitize_argument(argument):
    return argument.replace("__", "")


def convert_to_underscores(argument):
    return argument.replace("-", "_")


def parameterize(argument):
    return "--{}".format(argument.replace("_", "-"))


def get_value(value):
    if value in ["True", "true"]:
        return True
    elif value in ["False", "false"]:
        return False

    return value


def help(client, extra_clients=[], include_utility=False):
    namespaces = []
    actions = []
    utility_data = {}

    if isinstance(client, Catalog):

        for attr, item in client.__dict__.items():
            if isinstance(item, Catalog):
                namespaces.append(attr)

        for item_name, catalog_item in client.catalog_items.items():
            actions.append(get_catalog_item_data(catalog_item))

    elif isinstance(client, Catalog.CallHandle):
        actions.append(get_catalog_item_data(client.resource))

    data = {"clients": namespaces, "actions": actions}
    data["clients"].extend(extra_clients)

    if include_utility:
        utility_data = get_actions(client.utility_functions)

    return help_table(data, utility_data)


def help_table(data, utility_data={}):
    x = PrettyTable()

    x.field_names = [
        "name",
        "description",
        "required parameters",
    ]
    x.align["name"] = "l"
    x.align["description"] = "l"
    x.align["required parameters"] = "l"

    for item in data.get("actions"):
        name = item.get("name").lower().replace("_", "-")
        description = item.get("description")
        parameters = []
        for param in item.get("parameters"):
            if isinstance(param, str):
                parameters.append(parameterize(param))
            elif isinstance(param, list):
                for param2 in param:
                    parameters.append(parameterize(param2))
        x.add_row([name, description, "\n".join(parameters)])
        x.add_row(["", "", ""])

    for item in data.get("clients"):
        name = item
        description = "Various actions available for {}".format(name)
        parameters = ["--help"]
        x.add_row([name, description, "\n".join(parameters)])
        x.add_row(["", "", ""])

    for action, data in utility_data.items():
        name = action
        description = data[0]
        parameters = []
        parameters.extend("<{}>".format(x) for x in data[1])
        x.add_row([name, description, "\n".join(parameters)])
        x.add_row(["", "", ""])

    return x


def get_catalog_item_data(catalog_item):
    item = {}
    item["parameters"] = []
    item["name"] = catalog_item.catalog_resource_name.lower()
    item["parameters"].extend(x for x in catalog_item.file_parameters)
    item["parameters"].extend(
        x for x in catalog_item.payload_parameters if x not in item["parameters"]
    )
    item["parameters"].extend(
        x for x in catalog_item.uri_parameters if x not in item["parameters"]
    )
    item["parameters"] += (
        [catalog_item.payload_path] if catalog_item.payload_path else []
    )
    item["description"] = catalog_item.description

    return item


def configure_logging():
    oc = Client()
    LOG_LEVEL = oc.config.LOG_LEVEL if oc.config.LOG_LEVEL else "INFO"

    LOG = logging.getLogger()
    log_level = getattr(logging, LOG_LEVEL.upper())
    ch = logging.StreamHandler()
    LOG.setLevel(log_level)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s %(message)s')
    ch.setFormatter(formatter)
    LOG.addHandler(ch)
