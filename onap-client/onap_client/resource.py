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

import inspect

from abc import ABC, abstractmethod
from onap_client.exceptions import InvalidSpecException


class Resource(ABC):
    resource_name = "abstract"
    spec = {}

    def __init__(self, input):
        self.attributes = {}

        attributes = self._create(input)
        self.resolve_attributes(attributes)

        self._post_create()

    def __getattr__(self, attr):
        return self.attributes.get(attr, None)

    @abstractmethod
    def _create(self, input):
        pass

    @abstractmethod
    def _post_create(self):
        pass

    @abstractmethod
    def _submit(self):
        pass

    @classmethod
    def validate(cls, input, spec=None):
        """Validates that an input dictionary spec
        is valid according to a provided class spec.

        Recursively walksdown and checks if all required attributes are present, and
        attribute types match spec types.

        Returns complete spec with all attributes.
        """
        valid_spec = {}

        if not isinstance(input, dict):
            raise InvalidSpecException("input spec was not a dictionary")

        if not spec:
            spec = cls.spec

        for k, v in input.items():
            if not spec.get(k):
                raise InvalidSpecException("Unknown property found: {}".format(k))

        for k, v in spec.items():
            property_name = k
            property_type = v.get("type")
            property_required = v.get("required")
            property_default = v.get("default", default_empty_value(property_type))

            input_property = validate_property(
                input, property_name, property_required, property_default, property_type
            )

            if (
                property_type == dict
                and input_property != property_default
                and v.get("nested")
            ):
                property_value = cls.validate(input_property, v.get("nested"))
            elif property_type == list:
                list_property_type = v.get("list_item")
                list_spec = []
                for item in input_property:
                    if type(item) != list_property_type:
                        raise InvalidSpecException(
                            "list item {} not match type {}".format(
                                item, list_property_type
                            )
                        )
                    if list_property_type == str:
                        list_spec.insert(0, item)
                    else:
                        list_spec.insert(0, cls.validate(item, v.get("nested", {})))

                property_value = list_spec
            else:
                property_value = input_property

            valid_spec[property_name] = property_value

        return valid_spec

    @classmethod
    def create_from_spec(cls, spec, submit=True):
        input_args = []

        arguments = inspect.getfullargspec(cls).args
        arguments.pop(0)

        for argument in arguments:
            input_args.append(spec.get(argument))

        instance = cls(*input_args)

        if submit:
            instance._submit()

        return instance

    def resolve_attributes(self, attributes):
        for key, val in attributes.items():
            self.attributes[key] = val

    def print(self):
        for k, v in self.attributes.items():
            val = str(v)
            value = val[:50] + "..." if len(val) > 50 else val
            print("{}: {}".format(k, value))


def validate_property(
    input_spec, property_name, property_required, property_default, property_type
):
    input_property = input_spec.get(property_name)
    if not input_property:
        if property_required:
            raise InvalidSpecException(
                "required property {} not found in input spec".format(property_name)
            )
        else:
            input_property = property_default
    elif type(input_property) != property_type:
        raise InvalidSpecException(
            "input property {} not match type {}".format(property_name, property_type)
        )

    return input_property


def default_empty_value(property_type):
    if property_type == str:
        return None
    elif property_type == list:
        return []
    elif property_type == dict:
        return {}
    elif property_type == bool:
        return False
    else:
        return None
