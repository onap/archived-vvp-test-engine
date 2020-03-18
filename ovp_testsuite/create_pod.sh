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
CONFIGMAP=$3

cat  <<EOF | kubectl -n $NAMESPACE create -f -
apiVersion: v1
kind: Pod
metadata:
  name: $PODNAME
spec:
  containers:
  - name: $PODNAME
    image: python:3.7-alpine
    volumeMounts:
    - name: $CONFIGMAP
      mountPath: /etc/onap_client
    command: ["/bin/sh"]
    args:
      - -c
      - apk update && \
        apk add bash && \
        apk add git && \
        apk add gcc && \
        apk add python3-dev && \
        apk add musl-dev && \
        apk add libffi-dev && \
        apk add openssl-dev && \
        apk add libxml2-dev && \
        apk add libxml2 && \
        apk add libxslt-dev && \
        apk add tk && \
        sh -c 'pip install virtualenv; while true; do sleep 60; done;'
  restartPolicy: Never
  volumes:
    - name: $CONFIGMAP
      configMap:
        name: $CONFIGMAP
        defaultMode: 0755
EOF

podstatus=""
COUNTER=0

while [ "$podstatus" != "Error" ] && [ "$podstatus" != "Running" ] && [ $COUNTER -lt 60 ]; do
  podstatus=`kubectl -n $NAMESPACE get pods | grep $PODNAME | head -1 | awk '{print $3}'`
  echo "$PODNAME is $podstatus"
  COUNTER=$((COUNTER +1))
  if [ "$podstatus" = "Running" ]; then
    break
  fi
  sleep 30
done

if [ "$podstatus" = "Error" ]; then
  echo "failed creating pod to execute test, exiting..."
  exit 1
fi

kubectl -n $NAMESPACE cp "$DIR/../onap-client" "$PODNAME:/tmp/onap_client"
kubectl exec -n $NAMESPACE $PODNAME -- sh -c "cd /tmp/onap_client; pip install -r requirements.txt; pip install . --upgrade"
if [ $? -ne 0 ]; then
  echo "Failed to create pod, exiting..."
  exit 1
fi
