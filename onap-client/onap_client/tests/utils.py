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

import responses
import functools


def mockup_client(client):
    for k, v in client.catalog_items.items():
        mockup_catalog_item(v)


def mockup_return_item(item, item_list):
    items = list(item_list)
    if not items:
        return {item: item}
    new_item = items.pop(0)
    return {item: mockup_return_item(new_item, items)}


def mockup_catalog_item(
    catalog_resource, override_return_data=None, override_uri_params={}, status=None
):
    uri = catalog_resource.uri
    if isinstance(uri, functools.partial):
        params = {}
        for param in catalog_resource.uri_parameters:
            params[param] = param
        params.update(override_uri_params)
        uri = uri(**params)

    return_data = catalog_resource.return_data
    return_items = {}
    for k, v in return_data.items():
        return_items.update(mockup_return_item(k, v))

    if override_return_data:
        return_items = override_return_data

    responses.add(
        getattr(responses, catalog_resource.verb),
        uri,
        json=return_items,
        status=catalog_resource.success_code if not status else status,
    )
