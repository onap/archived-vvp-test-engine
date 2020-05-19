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

from onap_client.lib import generate_dummy_string, generate_dummy_date
from onap_client.resource import Resource
from onap_client.client.clients import Client


class LicenseModel(Resource):
    resource_name = "LICENSE_MODEL"
    spec = {
        "vendor_name": {
            "type": str,
            "required": False,
            "default": generate_dummy_string("test_vendor_"),
        },
        "mfr_ref_number": {
            "type": str,
            "required": False,
            "default": generate_dummy_string("mfref"),
        },
        "entitlement_pool_name": {
            "type": str,
            "required": False,
            "default": generate_dummy_string("test_kg_"),
        },
        "key_group_name": {
            "type": str,
            "required": False,
            "default": generate_dummy_string("test_ep_"),
        },
        "feature_group_name": {
            "type": str,
            "required": False,
            "default": generate_dummy_string("test_fg_"),
        },
        "license_agreement_name": {
            "type": str,
            "required": False,
            "default": generate_dummy_string("test_la_"),
        },
        "license_start_date": {
            "type": str,
            "required": False,
            "default": generate_dummy_date(days=1),
        },
        "license_end_date": {
            "type": str,
            "required": False,
            "default": generate_dummy_date(days=365),
        },
    }

    def __init__(
        self,
        vendor_name,
        mfr_ref_number,
        entitlement_pool_name,
        key_group_name,
        feature_group_name,
        license_agreement_name,
        license_start_date,
        license_end_date,
    ):
        self.oc = Client()

        license_input = {}
        license_input["vendor_name"] = vendor_name
        license_input["manufacturer_reference_number"] = mfr_ref_number
        license_input["entitlement_pool_name"] = entitlement_pool_name
        license_input["key_group_name"] = key_group_name
        license_input["feature_group_name"] = feature_group_name
        license_input["license_agreement_name"] = license_agreement_name
        license_input["license_start_date"] = license_start_date
        license_input["license_end_date"] = license_end_date

        super().__init__(license_input)

    def _create(self, license_input):
        """Creates a license model object in SDC"""
        return create_license_model(license_input)

    def _post_create(self):
        pass

    def _submit(self):
        """Submits the license model in SDC"""

        self.oc.sdc.license_model.submit_license_model(**self.attributes, action="Submit")

        license_model = self.oc.sdc.license_model.get_license_model(**self.attributes)
        self.attributes["tosca"] = license_model.response_data


# TODO
# Break this up into class funcs?
def create_license_model(license_input):
    """Creates a license model object in SDC

    :license_input: dictionary with values to input for lm creation

    :return: dictionary of updated values for created lm
    """
    oc = Client()

    kwargs = license_input
    license_model = oc.sdc.license_model.add_license_model(**kwargs)

    kwargs["license_model_id"] = license_model.license_model_id
    kwargs["license_model_version_id"] = license_model.license_model_version_id

    key_group = oc.sdc.license_model.add_key_group(**kwargs)
    key_group_id = key_group.key_group_id

    entitlement_pool = oc.sdc.license_model.add_entitlement_pool(**kwargs)
    entitlement_pool_id = entitlement_pool.entitlement_pool_id

    kwargs["entitlement_pool_id"] = entitlement_pool_id
    kwargs["key_group_id"] = key_group_id

    feature_group = oc.sdc.license_model.add_feature_group(**kwargs)
    feature_group_id = feature_group.feature_group_id

    kwargs["feature_group_id"] = feature_group_id

    license_agreement = oc.sdc.license_model.add_license_agreement(**kwargs)
    kwargs["license_agreement_id"] = license_agreement.license_agreement_id

    license_model = oc.sdc.license_model.get_license_model(**kwargs)
    kwargs["tosca"] = license_model.response_data

    return kwargs


def get_license_model_id(license_model_name):
    """GETs license model UUID from SDC

    :license_model_name: name of license model in SDC

    :return: uuid of lm or None
    """
    oc = Client()

    response = oc.sdc.license_model.get_license_models()
    results = response.response_data.get("results")
    for license_model in results:
        if license_model.get("name") == license_model_name:
            return license_model.get("id")
    return None


def get_license_model_version_id(license_model_id):
    """GETs license model version UUID from SDC

    :license_model_id: uuid of license model in SDC

    :return: uuid of lm version id or None
    """
    oc = Client()

    license_model_version_id = None
    creation_time = -1
    response = oc.sdc.license_model.get_license_model_versions(
        license_model_id=license_model_id
    )
    results = response.response_data.get("results")
    for version in results:
        if version.get("creationTime", 0) > creation_time:
            creation_time = version.get("creationTime")
            license_model_version_id = version.get("id")

    return license_model_version_id


def get_license_model_attribute(license_model_id, license_model_version_id, attribute):
    """GETs license model attribute from SDC

    :license_model_id: uuid of license model in SDC
    :license_model_version_id: uuid of license model version in SDC
    :attribute: attribute to GET (license-agreements, feature-groups, entitlement-pools, license-key-groups)

    :return: uuid of attribute of license-model
    """
    oc = Client()

    response = oc.sdc.license_model.get_license_model_version_attribute(
        license_model_id=license_model_id,
        license_model_version_id=license_model_version_id,
        attribute=attribute,
    )
    return response.response_data.get("results")[0]
