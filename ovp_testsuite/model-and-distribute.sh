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

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

NAMESPACE=$1
PODNAME=$2
OUTPUT_DIR=$3
BUILD_TAG=$4

kubectl -n $NAMESPACE cp $DIR/blank-spec.json $PODNAME:/tmp/blank-spec.json
kubectl -n $NAMESPACE cp $DIR/model-and-distribute.py $PODNAME:/tmp/modeling.py

exec > >(tee -i $OUTPUT_DIR/log.txt)
exec 2>&1

kubectl -n $NAMESPACE exec $PODNAME -- sh -c "python /tmp/modeling.py --vnf-folder /tmp/$BUILD_TAG --spec /tmp/blank-spec.json --build-tag $BUILD_TAG"
if [ $? -ne 0 ]; then
  echo "Failed during modeling/instantiation, exiting..."
  exit 1
fi
