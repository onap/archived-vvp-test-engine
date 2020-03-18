#!/bin/bash
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
set -x

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
NAMESPACE=$1
PODNAME=$2
OUTPUT_DIR=$3
BUILD_TAG=$4

kubectl -n $NAMESPACE cp $DIR/stack-validation.py $PODNAME:/tmp/stack-validation.py

kubectl -n $NAMESPACE exec $PODNAME -- sh -c "python /tmp/stack-validation.py --vnf-manifest /tmp/$BUILD_TAG/vnf-details.json --vnf-name $BUILD_TAG  --vnf-deployment-details /tmp/vnf-deployment-details-$BUILD_TAG.json"
if [ $? -ne 0 ]; then
  kubectl -n $NAMESPACE cp $PODNAME:tmp/stack-validation.json "$OUTPUT_DIR/stack-validation.json"
  echo "Stack validation failed, exiting..."
  exit 1
fi

kubectl -n $NAMESPACE cp $PODNAME:tmp/stack-validation.json "$OUTPUT_DIR/stack-validation.json"
