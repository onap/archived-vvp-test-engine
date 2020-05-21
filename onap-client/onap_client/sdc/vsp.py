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
from onap_client.client.clients import Client
from onap_client import sdc
from onap_client.util import utility
from onap_client.exceptions import ResourceAlreadyExistsException


class VSP(Resource):
    resource_name = "VSP"
    spec = {
        "owner": {"type": str, "required": False, "default": ""},
        "vendor_name": {"type": str, "required": True},
        "license_model_name": {"type": str, "required": True},
        "file_path": {"type": str, "required": True},
        "file_type": {"type": str, "required": False, "default": "application/zip"},
        "software_product_name": {
            "type": str,
            "required": False,
            "default": generate_dummy_string("test_vsp_"),
        },
        "description": {
            "type": str,
            "required": False,
            "default": "new software product",
        },
        "category": {"type": str, "required": False, "default": "generic"},
        "sub_category": {"type": str, "required": False, "default": "abstract"},
        "contributers": {
            "type": list,
            "list_item": str,
            "required": False,
            "default": [],
        },
        "allow_update": {"type": bool, "required": False, "default": False},
    }

    def __init__(
        self,
        vendor_name,
        license_model_name,
        file_path,
        file_type,
        software_product_name,
        description,
        category,
        sub_category,
        contributers=[],
        allow_update=False,
        owner="",
    ):
        self.oc = Client()
        vsp_input = {}

        license_model_id = sdc.license_model.get_license_model_id(license_model_name)
        license_model_version_id = sdc.license_model.get_license_model_version_id(
            license_model_id
        )
        feature_group = sdc.license_model.get_license_model_attribute(
            license_model_id, license_model_version_id, "feature-groups"
        )
        license_agreement = sdc.license_model.get_license_model_attribute(
            license_model_id, license_model_version_id, "license-agreements"
        )

        vsp_input["software_product_name"] = software_product_name
        vsp_input["feature_group_id"] = feature_group["id"]
        vsp_input["license_agreement_id"] = license_agreement["id"]
        vsp_input["vendor_name"] = vendor_name
        vsp_input["license_model_id"] = license_model_id
        vsp_input["license_model_version_id"] = license_model_version_id
        vsp_input["file_path"] = file_path
        vsp_input["file_type"] = file_type
        vsp_input["description"] = description
        vsp_input["category"] = category.lower()
        vsp_input["sub_category"] = sub_category.lower()
        vsp_input["contributers"] = contributers
        vsp_input["allow_update"] = allow_update
        vsp_input["owner"] = owner

        super().__init__(vsp_input)

    def _create(self, kwargs):
        """Creates a vsp object in SDC"""
        vsp = None

        existing = get_vsp(kwargs.get("software_product_name"))
        if not existing:
            vsp = create_vsp(kwargs)
        elif kwargs.get("allow_update"):
            vsp = update_vsp(existing, kwargs)
        else:
            raise ResourceAlreadyExistsException(
                "VSP resource {} already exists".format(
                    kwargs.get("software_product_name")
                )
            )

        return vsp

    def _post_create(self):
        for contributer in self.contributers:
            self.oc.sdc.vsp.add_vsp_contributer(
                user_id=contributer, software_product_id=self.software_product_id
            )

        if self.owner:
            self.oc.sdc.vsp.modify_vsp_owner(
                user_id=self.owner, software_product_id=self.software_product_id
            )

    def _submit(self):
        """Submits the vsp in SDC"""
        self.oc.sdc.vsp.submit_software_product(**self.attributes, action="Submit")
        self.oc.sdc.vsp.package_software_product(**self.attributes, action="Create_Package")

        vsp = self.oc.sdc.vsp.get_software_product(**self.attributes)
        self.attributes["tosca"] = vsp.response_data


def update_vsp(existing_vsp, vsp_input):
    oc = Client()

    existing_vsp_id = existing_vsp.get("id")
    existing_vsp_version_id = existing_vsp.get("version")

    if get_vsp_version_id(existing_vsp_id, search_key="status") == "Certified":
        oc.sdc.vsp.update_software_product(
            software_product_id=existing_vsp_id,
            software_product_version_id=existing_vsp_version_id,
            description=vsp_input.get("description", "New VSP Version")
        )

    vsp_input["software_product_id"] = existing_vsp_id
    vsp_input["software_product_version_id"] = get_vsp_version_id(existing_vsp_id)

    oc.sdc.vsp.upload_heat_package(**vsp_input)
    oc.sdc.vsp.validate_software_product(**vsp_input)

    vsp = oc.sdc.vsp.get_software_product(**vsp_input)
    vsp_input["tosca"] = vsp.response_data

    return vsp_input


def create_vsp(vsp_input):
    """Creates a VSP object in SDC

    :vsp_input: dictionary with values to input for vsp creation

    :return: dictionary of updated values for created vsp
    """
    oc = Client()

    kwargs = vsp_input
    vsp = oc.sdc.vsp.add_software_product(**kwargs)

    kwargs["software_product_id"] = vsp.software_product_id
    kwargs["software_product_version_id"] = vsp.software_product_version_id

    oc.sdc.vsp.upload_heat_package(**kwargs)
    oc.sdc.vsp.validate_software_product(**kwargs)

    vsp = oc.sdc.vsp.get_software_product(**kwargs)
    kwargs["tosca"] = vsp.response_data

    return kwargs


def get_vsp_id(vsp_name):
    """GETs vsp model ID from SDC

    :vsp_name: name of vsp model in SDC

    :return: id of vsp or None
    """
    oc = Client()

    response = oc.sdc.vsp.get_software_products()
    results = response.response_data.get("results", {})
    for vsp in results:
        if vsp.get("name") == vsp_name:
            return vsp["id"]
    return None


def get_vsp_version_id(vsp_id, search_key="id"):
    """GETs vsp model version UUID from SDC

    :vsp_id: uuid of vsp model in SDC

    :return: uuid of vsp version id or None
    """
    oc = Client()

    vsp_version_id = None
    creation_time = -1
    response = oc.sdc.vsp.get_software_product_versions(software_product_id=vsp_id)
    results = response.response_data.get("results")
    for version in results:
        if version.get("creationTime", 0) > creation_time:
            creation_time = version.get("creationTime")
            vsp_version_id = version.get(search_key)

    return vsp_version_id


def get_vsp_model(vsp_id, vsp_version_id):
    oc = Client()

    return oc.sdc.vsp.get_software_product(
        software_product_id=vsp_id, software_product_version_id=vsp_version_id,
    ).response_data


def get_vsp_owner(vsp_id):
    oc = Client()
    vsps = oc.sdc.vsp.get_software_products().response_data.get("results", [])
    for vsp in vsps:
        if vsp.get("id") == vsp_id:
            return vsp.get("owner")
    return None


@utility
def get_vsp(vsp_name):
    """Queries SDC for the tosca model for a VSP"""
    vsp_id = get_vsp_id(vsp_name)
    if vsp_id is None:
        return None
    vsp_version_id = get_vsp_version_id(vsp_id)
    return get_vsp_model(vsp_id, vsp_version_id)
