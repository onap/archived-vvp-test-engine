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
RANDOM_STRING=`cat /dev/urandom | env LC_CTYPE=C tr -cd 'a-zA-Z0-9' | head -c 4`
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
NAMESPACE=
VNF_FOLDER=
OUTPUT_DIR=/tmp/OVP-$RANDOM_STRING
PODNAME="ovp-test"
CONFIGMAP="ovp-test-suite-vol"

function tar_output() {
  OUTPUT=$1
  set +x 

  echo ""
  echo "================================================================"
  echo "OVP Test Case has finished, generating output in $OUTPUT_DIR."
  echo ""
  echo "--------------------Results--------------------"
  echo "Test Start Time:                    $STARTTIME"
  echo "VVP Validation Scripts:             $VVP_STATUS"
  echo "ONAP Modeling and Instantiation:    $MODELING_STATUS"
  echo "Stack Validation:                   $STACK_VALIDATION_STATUS"
  echo ""

  "$DIR/ovp-report.sh" $NAMESPACE $PODNAME $OUTPUT_DIR $RANDOM_STRING $STARTTIME $VVP_STATUS $MODELING_STATUS $STACK_VALIDATION_STATUS
  pushd .
  cd $OUTPUT
  tar -cvzf ovp-test.tar.gz *
  popd
}

function check_required_parameter() {
  # arg1 = parameter
  # arg2 = parameter name
  if [ -z "$1" ]; then
    echo "$2 was not was provided. This parameter is required."
    exit 1
  fi
}

while test $# -gt 0; do
  case "$1" in
    -h|--help)
      echo "./instantiate-k8s.sh [options]"
      echo " "
      echo "required:"
      echo "-n, --namespace <namespace>       namespace that onap is running under."
      echo "-f, --folder <folder>             path to folder containing heat templates, preloads, and vnf-details.json."
      echo " "
      echo "This script executes the OVP VNF instantiation testsuite."
      echo "- It creates a container that will contain all of the installation requirements."
      echo "- It models, distributes, and instantiates a heat-based VNF."
      echo "- It copies the logs to an output directory, and creates a tarball for upload to the OVP portal."
      echo ""
      exit 0
      ;;
    -n|--namespace)
      shift
      NAMESPACE=$1
      shift
      ;;
    -f|--folder)
      shift
      VNF_FOLDER=$1
      shift
      ;;
    *)
      echo "Unknown Argument $1. Try running with --help."
      exit 0
      ;;
  esac
done

set -x 

check_required_parameter "$NAMESPACE" "--namespace"
check_required_parameter "$VNF_FOLDER" "--folder"

if [ -z $KUBECONFIG ]; then
  echo "KUBECONFIG variable not found, exiting..."
  exit 1
fi

kubectl -n $NAMESPACE get configmap $CONFIGMAP
if [ $? -ne 0 ]; then
  "$DIR/create_configmap.sh" $NAMESPACE $CONFIGMAP
  if [ $? -ne 0 ]; then
    echo "Failed to create configmap, exiting..."
    exit 1
  fi
fi

kubectl -n $NAMESPACE get pod $PODNAME
if [ $? -ne 0 ]; then
  "$DIR/create_pod.sh" $NAMESPACE $PODNAME $CONFIGMAP
  if [ $? -ne 0 ]; then
    echo "Failed to create pod, exiting..."
    exit 1
  fi
fi

mkdir "$OUTPUT_DIR"
echo ""
echo "Your output directory is $OUTPUT_DIR, look here for logs after the test has finished."
echo ""
sleep 5

if [ ! -d $VNF_FOLDER ]; then
  echo "VNF Folder $VNF_FOLDER not found, exiting..."
  exit 1
fi

kubectl -n $NAMESPACE cp $VNF_FOLDER $PODNAME:/tmp/$RANDOM_STRING
STARTTIME=`date +%s`

trap 'tar_output "$OUTPUT_DIR"' EXIT

VVP_STATUS=NOT_STARTED
MODELING_STATUS=NOT_STARTED
STACK_VALIDATION_STATUS=NOT_STARTED

"$DIR/validation-scripts.sh" $NAMESPACE $PODNAME $OUTPUT_DIR $RANDOM_STRING
if [ $? -ne 0 ]; then
  VVP_STATUS=FAIL
  exit 1
fi
VVP_STATUS=SUCCESS

"$DIR/model-and-distribute.sh" $NAMESPACE $PODNAME $OUTPUT_DIR $RANDOM_STRING
if [ $? -ne 0 ]; then
  MODELING_STATUS=FAIL
  exit 1
fi
MODELING_STATUS=SUCCESS

"$DIR/stack-validation.sh" $NAMESPACE $PODNAME $OUTPUT_DIR $RANDOM_STRING
if [ $? -ne 0 ]; then
  STACK_VALIDATION_STATUS=FAIL
  exit 1
fi
STACK_VALIDATION_STATUS=SUCCESS
