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
START_TIME=$5
VALIDATION_SCRIPTS=$6
MODEL_AND_DISTRIBUTE=$7
STACK_VALIDATION=$8

DATE=`date '+%Y-%m-%d %H:%M:%S'`
TEMPLATE_DIRECTORY=/tmp/$BUILD_TAG/templates

ARG_LIST="--template-directory $TEMPLATE_DIRECTORY --start-time $START_TIME --test-date '$DATE'"

if [ ! -z "$VALIDATION_SCRIPTS" ]; then
  ARG_LIST="$ARG_LIST --validation-scripts $VALIDATION_SCRIPTS"
fi

if [ ! -z "$MODEL_AND_DISTRIBUTE" ]; then
  ARG_LIST="$ARG_LIST --model-and-distribute $MODEL_AND_DISTRIBUTE"
fi

if [ ! -z "$STACK_VALIDATION" ]; then
  ARG_LIST="$ARG_LIST --stack-validation $STACK_VALIDATION"
fi

kubectl -n $NAMESPACE cp $DIR/ovp-report.py $PODNAME:/tmp/ovp-report.py

kubectl -n $NAMESPACE exec $PODNAME -- sh -c "python /tmp/ovp-report.py $ARG_LIST"

kubectl -n $NAMESPACE cp $PODNAME:tmp/results.json "$OUTPUT_DIR/results.json"
