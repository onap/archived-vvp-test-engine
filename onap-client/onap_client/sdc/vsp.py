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
from onap_client.client.clients import get_client as Client
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
        "update_message": {
            "type": str,
            "required": False,
            "default": "New VSP Version",
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

    def _create(self, vsp_input):
        """Creates a vsp object in SDC"""
        vsp = None

        existing = get_vsp(vsp_input.get("software_product_name"), oc=self.oc)
        if not existing:
            vsp = create_vsp(vsp_input, oc=self.oc)
        elif vsp_input.get("allow_update"):
            vsp = update_vsp(existing, vsp_input, oc=self.oc)
        else:
            raise ResourceAlreadyExistsException(
                "VSP resource {} already exists".format(
                    vsp_input.get("software_product_name")
                )
            )

        return vsp

    def _post_create(self):
        vsp_permissions = self.oc.sdc.vsp.get_vsp_permissions(
            software_product_id=self.software_product_id
        ).response_data.get("results", [])
        requestor_id = self.oc.sdc.vsp.catalog_resources["MODIFY_VSP_OWNER"].get("headers").get("USER_ID")

        if user_exists(requestor_id, vsp_permissions, permission="Owner"):
            tmp_list = []
            for contributer in self.contributers:
                if (
                    not user_exists(contributer, vsp_permissions, permission="Contributor")
                    and contributer != requestor_id
                ):
                    tmp_list.append(contributer)

            if len(tmp_list):
                self.oc.sdc.vsp.add_vsp_contributer(
                    user_id=tmp_list, software_product_id=self.software_product_id
                )

            if self.owner and self.owner != requestor_id:
                self.oc.sdc.vsp.modify_vsp_owner(
                    user_id=self.owner, software_product_id=self.software_product_id
                )

    def _submit(self):
        """Submits the vsp in SDC"""
        self.oc.sdc.vsp.submit_software_product(**self.attributes, action="Submit")
        self.oc.sdc.vsp.package_software_product(**self.attributes, action="Create_Package")

        vsp = self.oc.sdc.vsp.get_software_product(**self.attributes)
        self.attributes["tosca"] = vsp.response_data

        self.oc.cache("vsp", self.software_product_name, "tosca", self.tosca)
        self.oc.cache("vsp", self.software_product_name, "owner", self.owner)

    def _output(self):
        return self.tosca


def update_vsp(existing_vsp, vsp_input, oc=None):
    if not oc:
        oc = Client()

    existing_vsp_id = existing_vsp.get("id")
    existing_vsp_version_id = existing_vsp.get("version")

    if get_vsp_version_id(existing_vsp_id, search_key="status", oc=oc) == "Certified":
        response_data = oc.sdc.vsp.update_software_product(
            software_product_id=existing_vsp_id,
            software_product_version_id=existing_vsp_version_id,
            description=vsp_input.get("update_message", "New VSP Version")
        ).response_data
        oc.cache("vsp", existing_vsp.get("name"), "csar_version", response_data.get("name"))
        existing_vsp_version_id = response_data.get("id")

    vsp_input["software_product_id"] = existing_vsp_id
    vsp_input["software_product_version_id"] = existing_vsp_version_id

    oc.sdc.vsp.upload_heat_package(**vsp_input)
    oc.sdc.vsp.validate_software_product(**vsp_input)

    vsp = oc.sdc.vsp.get_software_product(**vsp_input)
    vsp_input["tosca"] = vsp.response_data

    return vsp_input


def create_vsp(vsp_input, oc=None):
    """Creates a VSP object in SDC

    :vsp_input: dictionary with values to input for vsp creation

    :return: dictionary of updated values for created vsp
    """
    if not oc:
        oc = Client()

    license_model_id = sdc.license_model.get_license_model_id(
        vsp_input.get("license_model_name"),
        oc=oc
    )

    license_model_version_id = sdc.license_model.get_license_model_version_id(
        license_model_id,
        oc=oc
    )

    feature_group = sdc.license_model.get_license_model_attribute(
        license_model_id,
        license_model_version_id,
        "feature-groups",
        oc=oc
    )

    license_agreement = sdc.license_model.get_license_model_attribute(
        license_model_id,
        license_model_version_id,
        "license-agreements",
        oc=oc
    )

    vsp_input["license_model_id"] = license_model_id
    vsp_input["license_model_version_id"] = license_model_version_id
    vsp_input["feature_group_id"] = feature_group["id"]
    vsp_input["license_agreement_id"] = license_agreement["id"]

    vsp = oc.sdc.vsp.add_software_product(**vsp_input)

    vsp_input["software_product_id"] = vsp.software_product_id
    vsp_input["software_product_version_id"] = vsp.software_product_version_id

    oc.sdc.vsp.upload_heat_package(**vsp_input)
    oc.sdc.vsp.validate_software_product(**vsp_input)

    vsp = oc.sdc.vsp.get_software_product(**vsp_input)
    vsp_input["tosca"] = vsp.response_data

    return vsp_input


def get_vsp_id(vsp_name, oc=None):
    """GETs vsp model ID from SDC

    :vsp_name: name of vsp model in SDC

    :return: id of vsp or None
    """
    if not oc:
        oc = Client()

    response = oc.sdc.vsp.get_software_products()
    results = response.response_data.get("results", {})
    for vsp in results:
        if vsp.get("name") == vsp_name:
            return vsp["id"]
    return None


def get_vsp_version_id(vsp_id, search_key="id", oc=None):
    """GETs vsp model version UUID from SDC

    :vsp_id: uuid of vsp model in SDC

    :return: uuid of vsp version id or None
    """
    if not oc:
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


def get_vsp_model(vsp_id, vsp_version_id, oc=None):
    if not oc:
        oc = Client()

    return oc.sdc.vsp.get_software_product(
        software_product_id=vsp_id, software_product_version_id=vsp_version_id,
    ).response_data


def get_vsp_owner(vsp_id, oc=None):
    if not oc:
        oc = Client()

    vsps = oc.sdc.vsp.get_software_products().response_data.get("results", [])
    for vsp in vsps:
        if vsp.get("id") == vsp_id:
            return vsp.get("owner")
    return None


@utility
def get_vsp(vsp_name, oc=None):
    """Queries SDC for the tosca model for a VSP"""
    if not oc:
        oc = Client()

    vsp_id = get_vsp_id(vsp_name, oc=oc)
    if vsp_id is None:
        return None
    vsp_version_id = get_vsp_version_id(vsp_id, oc=oc)
    return get_vsp_model(vsp_id, vsp_version_id, oc=oc)


def user_exists(contributer, vsp_permissions, permission="Contributor"):
    for user in vsp_permissions:
        if contributer == user.get("userId") and permission == user.get("permission"):
            return True
    return False
