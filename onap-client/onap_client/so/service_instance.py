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

import uuid

from onap_client.lib import generate_dummy_string
from onap_client.resource import Resource
from onap_client.client.clients import Client
from onap_client.so import SO_PROPERTIES
from onap_client.exceptions import (
    SORequestStatusUnavailable,
    SORequestFailed,
    SORequestTimeout,
    TenantNotFound,
    ServiceInstanceNotFound,
)
from onap_client import sdc
from onap_client.util import utility
from time import sleep


class ServiceInstance(Resource):
    resource_name = "SERVICE_INSTANCE"
    spec = {
        "service_instance_name": {
            "type": str,
            "required": False,
            "default": generate_dummy_string("SI_"),
        },
        "requestor_id": {"type": str, "required": False, "default": "cs0008"},
        "model_name": {"type": str, "required": True},
        "model_version": {"type": str, "required": False, "default": "1.0"},
        "tenant_name": {"type": str, "required": True},
        "cloud_owner": {"type": str, "required": True},
        "cloud_region": {"type": str, "required": True},
        "api_type": {"type": str, "required": False, "default": "GR_API"},
        "service_type": {"type": str, "required": True},
        "customer_name": {"type": str, "required": True},
        "project_name": {"type": str, "required": True},
        "owning_entity_name": {"type": str, "required": True},
    }

    def __init__(
        self,
        service_instance_name,
        requestor_id,
        model_name,
        model_version,
        tenant_name,
        cloud_owner,
        cloud_region,
        api_type,
        service_type,
        customer_name,
        project_name,
        owning_entity_name,
    ):
        self.oc = Client()

        instance_input = {}

        tenant_id = get_tenant_id(cloud_region, cloud_owner, tenant_name)

        instance_input["service_instance_name"] = service_instance_name
        instance_input["requestor_id"] = requestor_id
        instance_input["model_name"] = model_name
        instance_input["model_version"] = model_version
        instance_input["tenant_id"] = tenant_id
        instance_input["cloud_owner"] = cloud_owner
        instance_input["cloud_region"] = cloud_region
        instance_input["api_type"] = api_type
        instance_input["service_type"] = service_type
        instance_input["customer_id"] = customer_name
        instance_input["project_name"] = project_name
        instance_input["owning_entity_name"] = owning_entity_name

        super().__init__(instance_input)

    def _create(self, instance_input):
        service_model = self.oc.sdc.service.get_sdc_service(
            catalog_service_id=sdc.service.get_service_id(
                instance_input.get("model_name")
            )
        ).response_data

        instance_input["model_invariant_id"] = service_model["invariantUUID"]
        instance_input["model_version_id"] = service_model["uniqueId"]

        category_parameters = self.oc.vid.maintenance.get_category_parameters().response_data
        for entity in category_parameters.get("categoryParameters", {}).get("owningEntity", []):
            if entity.get("name") == instance_input.get("owning_entity_name"):
                instance_input["owning_entity_id"] = entity.get("id")
                break

        return create_service_instance(instance_input)

    def _post_create(self):
        pass

    def _submit(self):
        pass


@utility
def get_service_instance(instance_name):
    """Queries SDNC for a list of all service instances and returns
    The service instance that matches <instance name>"""
    oc = Client()

    service_instances = oc.sdnc.config.get_service_instances().response_data
    for si in service_instances.get("services", {}).get("service", []):
        if si.get("service-data", {}).get("service-request-input", {}).get("service-instance-name") == instance_name:
            return si

    raise ServiceInstanceNotFound("Service Instance {} was not found".format(instance_name))


def get_tenant_id(cloud_region, cloud_owner, tenant_name):
    oc = Client()

    tenants = oc.aai.cloud_infrastructure.get_cloud_region_tenants(
        cloud_owner=cloud_owner,
        cloud_region=cloud_region
    ).response_data

    for tenant in tenants.get("tenant"):
        if tenant.get("tenant-name") == tenant_name:
            return tenant.get("tenant-id")

    raise TenantNotFound("Tenant {} was not found in AAI".format(tenant_name))


def create_service_instance(instance_input):
    oc = Client()

    headers = {"X-TransactionId": str(uuid.uuid4())}
    service_instance = oc.so.service_instantiation.create_service_instance(
        **instance_input, **headers
    )

    request_id = service_instance.response_data.get("requestReferences", {}).get(
        "requestId"
    )

    instance_input["request_info"] = poll_request(request_id)

    return instance_input


@utility
def poll_request(request_id):
    """Poll an SO request until completion"""
    oc = Client()

    poll_interval = SO_PROPERTIES.POLL_INTERVAL or 30
    request = None
    x = 0
    while x < 30:
        request = oc.so.service_instantiation.get_request_status(
            request_id=request_id
        ).response_data
        status = request.get("request", {}).get("requestStatus", {}).get("requestState")
        if not status:
            raise SORequestStatusUnavailable(
                "Could not determine request for {}".format(request_id)
            )
        if status == "FAILED":
            failure_message = (
                request.get("request", {}).get("requestStatus", {}).get("statusMessage")
            )
            raise SORequestFailed(
                "Request {} failed with message {}".format(request_id, failure_message)
            )
        elif status == "COMPLETE":
            return request

        x += 1

        sleep(poll_interval)

    raise SORequestTimeout("Request {} timed out polling for status".format(request_id))


@utility
def delete_service_instance(service_instance_name, api_type="GR_API"):
    """Delete a Service Instance from SO"""
    oc = Client()

    si = get_service_instance(service_instance_name)
    si_id = si.get("service-instance-id")
    invariant_id = si.get("service-data").get("service-information").get("onap-model-information").get("model-invariant-uuid")
    version = si.get("service-data").get("service-information").get("onap-model-information").get("model-version")

    return oc.so.service_instantiation.delete_service_instance(
        service_invariant_id=invariant_id,
        service_name=service_instance_name,
        service_version=version,
        service_instance_id=si_id,
        api_type=api_type,
    ).response_data
