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


class MissingAttributeException(Exception):
    pass


class RequestFailure(Exception):
    pass


class FilesRequestFailure(Exception):
    pass


class CatalogItemNotFound(Exception):
    pass


class InputNotFoundException(Exception):
    pass


class PropertyNotFoundException(Exception):
    pass


class MissingInputException(Exception):
    pass


class ResourceNotFoundException(Exception):
    pass


class UnknownGroupException(Exception):
    pass


class UnknownPolicyException(Exception):
    pass


class InvalidSpecException(Exception):
    pass


class ResourceAlreadyExistsException(Exception):
    pass


class ResourceTypeNotFoundException(Exception):
    pass


class ResourceIDNotFoundException(Exception):
    pass


class SORequestStatusUnavailable(Exception):
    pass


class SORequestFailed(Exception):
    pass


class SORequestTimeout(Exception):
    pass


class ServiceInstanceNotFound(Exception):
    pass


class VNFComponentNotFound(Exception):
    pass


class VNFInstanceNotFound(Exception):
    pass


class ModuleInstanceNotFound(Exception):
    pass


class NoArtifactFoundInModel(Exception):
    pass


class ModuleModelNameNotFound(Exception):
    pass


class DistributionNotFound(Exception):
    pass


class DistributionFailure(Exception):
    pass


class DistributionTimeout(Exception):
    pass


class TenantNotFound(Exception):
    pass


class ResourceCreationFailure(Exception):
    pass
