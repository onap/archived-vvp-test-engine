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
import inspect
from prettytable import PrettyTable


def utility_cli(onap_client, cli_arguments):
    functions = onap_client.utility_functions

    if len(cli_arguments) == 0 or cli_arguments[0] == "--help":
        help(functions)
    else:
        while cli_arguments:
            argument = cli_arguments.pop(0)

            if argument == "--help":
                help(functions)
                return

            argument = convert_to_underscores(argument)
            functions = functions.get(argument)
            if not functions:
                print("Invalid argument {}. Try --help.".format(argument))
                return

            if callable(functions):
                cf = CallableFunction(functions)
                if cf.required_arg_count != len(cli_arguments):
                    print(
                        "Function requires {} arguments, but {} were passed. Try --help.".format(
                            cf.required_arg_count, len(cli_arguments)
                        )
                    )
                    return

                if cli_arguments[0] == "--help":
                    help(functions)
                    return

                return_data = functions(*cli_arguments[0:])
                if isinstance(return_data, str):
                    print(return_data)
                elif isinstance(return_data, dict) or isinstance(return_data, list):
                    print(json.dumps(return_data, indent=4))

                return


def convert_to_underscores(argument):
    return argument.replace("-", "_")


def convert_to_dash(argument):
    return argument.replace("_", "-")


def help(functions):
    actions = get_actions(functions)

    print(help_table(actions))


def get_actions(functions):
    actions = {}
    actions["--help"] = ("", "")
    if isinstance(functions, dict):
        for k, v in functions.items():
            cf = CallableFunction(v)
            actions[convert_to_dash(k)] = (
                cf.doc_string,
                cf.required_arguments,
            )
    elif callable(functions):
        cf = CallableFunction(functions)
        actions[convert_to_dash(cf.name)] = (
            cf.doc_string,
            cf.required_arguments,
        )

    return actions


def help_table(actions):
    x = PrettyTable()

    x.field_names = [
        "name",
        "description",
        "parameters",
    ]
    x.align["name"] = "l"
    x.align["description"] = "l"
    x.align["parameters"] = "l"

    for action, data in actions.items():
        name = action
        description = data[0]
        parameters = []
        parameters.extend("<{}>".format(x) for x in data[1])
        x.add_row([name, description, "\n".join(parameters)])
        x.add_row(["", "", ""])

    return x


def utility(func):
    func.utility_function = True
    return func


class CallableFunction:
    def __init__(self, function):
        self.function = function
        self.required_arguments = []

        for param in inspect.signature(self.function).parameters.values():
            if param.default == param.empty:
                self.required_arguments.append(param.name)

    @property
    def required_arg_count(self):
        return len(self.required_arguments)

    @property
    def doc_string(self):
        return self.function.__doc__

    @property
    def name(self):
        return self.function.__name__
