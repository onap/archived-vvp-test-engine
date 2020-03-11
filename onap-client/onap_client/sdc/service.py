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

from onap_client.lib import generate_dummy_string
from onap_client.resource import Resource
from onap_client import exceptions
from onap_client.client.clients import Client as SDCClient
from onap_client.sdc.vnf import get_vnf_id
from onap_client import sdc
from onap_client.sdc import SDC_PROPERTIES
from onap_client.util import utility

import time
import json
import random

service_client = SDCClient().sdc.service
sdc_properties = sdc.SDC_PROPERTIES


def normalize_category_icon(category_name):
    if category_name == "Network L1-3":
        return "network_l_4"
    elif category_name == "Mobility":
        return "mobility"
    elif category_name == "E2E Service":
        return "network_l_1-3"
    elif category_name == "Network L1-3":
        return "network_l_1-3"
    elif category_name == "Network Service":
        return "network_l_1-3"
    elif category_name == "Network 4+":
        return "network_l_4"
    elif category_name == "VoIP Call Control":
        return "call_controll"
    else:
        return "network_l_1-3"


class Service(Resource):
    resource_name = "SERVICE"
    spec = {
        "instantiation_type": {
            "type": str,
            "required": False,
            "default": "A-la-carte",
        },
        "service_name": {
            "type": str,
            "required": False,
            "default": generate_dummy_string("test_service_"),
        },
        "contact_id": {"type": str, "required": False, "default": "cs0008"},
        "category_name": {"type": str, "required": False, "default": "Network L1-3"},
        "tag": {"type": str, "required": False, "default": "robot-ete"},
        "project_code": {"type": str, "required": False, "default": "123456"},
        "environment_context": {
            "type": str,
            "required": False,
            "default": "General_Revenue-Bearing",
        },
        "ecomp_generated_naming": {"type": str, "required": False, "default": "true"},
        "description": {
            "type": str,
            "required": False,
            "default": "Brand New Service",
        },
        "service_type": {"type": str, "required": False, "default": ""},
        "service_role": {"type": str, "required": False, "default": ""},
        "naming_policy": {"type": str, "required": False, "default": ""},
        "resources": {
            "type": list,
            "list_item": dict,
            "required": False,
            "default": [],
            "nested": {
                "resource_name": {"type": str, "required": True},
                "resource_id": {"type": str, "required": False},
                "catalog_resource_name": {"type": str, "required": False},
                "origin_type": {"type": str, "required": False, "default": "VF"},
                "properties": {"type": dict, "required": False, "default": {}},
            },
        },
        "wait_for_distribution": {"type": bool, "required": False, "default": False},
    }

    def __init__(
        self,
        instantiation_type,
        service_name,
        contact_id,
        category_name,
        tag,
        project_code,
        environment_context,
        ecomp_generated_naming,
        description,
        service_type,
        service_role,
        naming_policy,
        resources=[],
        wait_for_distribution=False,
    ):
        service_input = {}

        category_name_lower = category_name.lower()
        category_name_icon = normalize_category_icon(category_name)
        category_id = "serviceNewCategory.{}".format(category_name_lower)

        service_input["service_name"] = service_name
        service_input["instantiation_type"] = instantiation_type
        service_input["contact_id"] = contact_id
        service_input["category_name"] = category_name
        service_input["category_id"] = category_id
        service_input["category_name_lower"] = category_name_lower
        service_input["category_name_icon"] = category_name_icon
        service_input["tag"] = tag
        service_input["project_code"] = project_code
        service_input["environment_context"] = environment_context
        service_input["ecomp_generated_naming"] = ecomp_generated_naming
        service_input["description"] = description
        service_input["service_type"] = service_type
        service_input["service_role"] = service_role
        service_input["naming_policy"] = naming_policy
        service_input["resources"] = resources
        service_input["wait_for_distribution"] = wait_for_distribution

        super().__init__(service_input)

    def _create(self, service_input):
        """Creates a service object in SDC"""
        service = None

        if get_service_id(service_input.get("service_name")) is None:
            service = create_service(service_input)
        else:
            raise exceptions.ResourceAlreadyExistsException(
                "Service resource {} already exists".format(
                    service_input.get("service_name")
                )
            )

        return service

    def _post_create(self):
        resources = self.resources

        for resource in resources:
            resource_name = resource.get("resource_name")
            catalog_resource_name = resource.get("catalog_resource_name")
            resource_id = resource.get("resource_id")
            resource_properties = resource.get("properties")
            if not resource_id:
                resource_id = get_vnf_id(catalog_resource_name)
                if not resource_id:
                    raise exceptions.ResourceIDNotFoundException(
                        "resource ID was not passed, and resource lookup by name was not found {}".format(
                            resource_name
                        )
                    )
            resource_origin = resource.get("origin_type")
            self.add_resource(resource_id, resource_name, origin_type=resource_origin)
            for k, v in resource_properties.items():
                if isinstance(v, dict):
                    v = json.dumps(v).replace('"', '\\"')
                self.add_property_value(resource_name, k, v)

    def _submit(self):
        """Submits the service in SDC and distributes the model"""
        DISTRIBUTION_STEPS = sdc_properties.SERVICE_DISTRIBUTION or []

        service_client.checkin_service(**self.attributes, user_remarks="checking in")

        if (
            not DISTRIBUTION_STEPS
            or "request_service_certification" in DISTRIBUTION_STEPS
        ):
            service_client.request_service_certification(
                **self.attributes, user_remarks="requesting certification"
            )

        if (
            not DISTRIBUTION_STEPS
            or "start_service_certification" in DISTRIBUTION_STEPS
        ):
            service_client.start_service_certification(
                **self.attributes, user_remarks="certifying"
            )

        if (
            not DISTRIBUTION_STEPS
            or "finish_service_certification" in DISTRIBUTION_STEPS
        ):
            catalog_service = service_client.finish_service_certification(
                **self.attributes, user_remarks="certified"
            )
            self.attributes["catalog_service_id"] = catalog_service.catalog_service_id

        if (
            not DISTRIBUTION_STEPS
            or "approve_service_certification" in DISTRIBUTION_STEPS
        ):
            service_client.approve_service_certification(
                **self.attributes, user_remarks="approved"
            )

        service_client.distribute_sdc_service(**self.attributes)

        if self.wait_for_distribution:
            poll_distribution(self.service_name)

        self._refresh()

    def add_resource(
        self, catalog_resource_id, catalog_resource_name, origin_type="VF"
    ):
        """Attaches a resource to a Service in SDC

        :catalog_resource_id: ID of a resource in the SDC catalog
        :catalog_resource_name: name to give to the resource when attaching to service
        :origin_type: specifies the origin of the attached resource

        """
        milli_timestamp = int(time.time() * 1000)

        resource_instance = service_client.add_resource_instance(
            **self.attributes,
            posX=random.randrange(150, 550),  # nosec
            posY=random.randrange(150, 450),  # nosec
            milli_timestamp=milli_timestamp,
            catalog_resource_id=catalog_resource_id,
            catalog_resource_name=catalog_resource_name,
            originType=origin_type,
        )

        response = {
            "id": resource_instance.catalog_resource_instance_id,
            "tosca": resource_instance.response_data,
        }
        self.attributes[catalog_resource_name] = response

        self._refresh()

    def add_property_value(self, resource_name, property_name, input_value):
        """Updates an property value on a resource attached to a Service

        :resource_name: Name of a resource attached to a service
        :property_name: property name to update
        :input_value: value to update property with

        """
        resource = self.attributes.get(resource_name)
        if not resource:
            raise exceptions.ResourceNotFoundException(
                "Resource {} was not found on Service {}".format(
                    resource_name, self.service_name
                )
            )
        resource_id = resource["id"]

        instance_inputs = self.tosca.get("componentInstancesProperties", {}).get(
            resource_id, []
        )
        for prop in instance_inputs:
            if prop.get("name") == property_name:
                unique_id = prop.get("uniqueId")
                parent_unique_id = prop.get("parentUniqueId")
                owner_id = prop.get("ownerId")
                schemaType = prop.get("schemaType", "")
                property_type = prop.get("type")
                return service_client.add_catalog_service_property(
                    **self.attributes,
                    unique_id=unique_id,
                    parent_unique_id=parent_unique_id,
                    owner_id=owner_id,
                    catalog_resource_instance_id=resource_id,
                    input_name=property_name,
                    input_value=input_value,
                    schema_type=schemaType,
                    property_type=property_type,
                )

        raise exceptions.PropertyNotFoundException(
            "Property {} was not found in VF Instance {}".format(
                property_name, resource_id
            )
        )

    def _refresh(self):
        self.tosca = service_client.get_sdc_service(
            catalog_service_id=self.catalog_service_id
        ).response_data


def create_service(service_input):
    """Creates a service object in SDC

    :service_input: dictionary with values to input for service creation

    :return: dictionary of updated values for created service
    """
    kwargs = service_input

    service = service_client.add_catalog_service(**kwargs)

    kwargs["catalog_service_id"] = service.catalog_service_id
    kwargs["tosca"] = service.response_data

    return kwargs


@utility
def get_service(service_name):
    """Queries SDC for the TOSCA model for a service"""
    return service_client.get_sdc_service(
        catalog_service_id=get_service_id(service_name)
    ).response_data


@utility
def get_service_id(service_name):
    """Queries SDC for the uniqueId of a service model"""
    response = service_client.get_services()
    results = response.response_data.get("services", [])
    for service in results:
        if service.get("name") == service_name:
            return service["uniqueId"]
    return None


def get_service_uuid(service_name):
    return get_service(service_name).get("uuid")


def get_service_distribution(service_name):
    distribution_id = get_distribution_id(service_name)

    if distribution_id:
        return service_client.get_service_distribution_details(
            distribution_id=distribution_id
        ).response_data

    return None


def get_distribution_id(service_name):
    distribution = service_client.get_service_distribution(
        distribution_service_id=get_service_uuid(service_name)
    ).response_data
    if distribution:
        details = distribution.get("distributionStatusOfServiceList", [])
        for entry in details:
            return entry.get("distributionID")

    return None


@utility
def poll_distribution(service_name):
    """Polls a distributed service until distribution is complete"""
    poll_interval = SDC_PROPERTIES.POLL_INTERVAL or 30
    x = 0
    while x < 30:
        distribution = get_service_distribution(service_name)
        if not distribution:
            raise exceptions.DistributionNotFound(
                "Could not determine distribution status for {}".format(service_name)
            )
        distribution_list = distribution.get("distributionStatusList")
        for component in distribution_list:
            status = component.get("status")
            component_name = component.get("omfComponentID")
            if status == "DISTRIBUTION_COMPLETE_ERROR":
                raise exceptions.DistributionFailure(
                    "Distribution failure for service {}, component details {}".format(
                        service_name, component
                    )
                )
            elif status == "COMPONENT_DONE_ERROR" and component_name == "aai-ml":
                raise exceptions.DistributionFailure(
                    "Distribution failure for service {}, component details {}".format(
                        service_name, component
                    )
                )
            elif status == "DISTRIBUTION_COMPLETE_OK":
                return "Distribution Successful"
        x += 1
        time.sleep(poll_interval)

    raise exceptions.DistributionTimeout(
        "Distribution polling timed out waiting for {}".format(service_name)
    )
