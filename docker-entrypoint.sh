#!/bin/bash
 
# ============LICENSE_START========================================== 
# org.onap.vvp/test-engine
# ===================================================================
# Copyright © 2017 AT&T Intellectual Property. All rights reserved.
# ===================================================================
#
# Unless otherwise specified, all software contained herein is licensed
# under the Apache License, Version 2.0 (the “License”);
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
# under the Creative Commons License, Attribution 4.0 Intl. (the “License”);
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
#
# ECOMP is a trademark and service mark of AT&T Intellectual Property.

Python=`which python`

checkResault ()
{
  value=$1
  func=$2

  if [ $value -ne "0" ] ; then
    echo "[ ERR ] Function $func failed"
    exit 255
  fi
}

dev_cert=/opt/secrets/site-crt/site.crt
if [ -e "$dev_cert" ]; then
	echo >&2 $0: Updating certificates...
	cp -L "$dev_cert" /usr/local/share/ca-certificates/
	update-ca-certificates
fi



echo >&2 $0: Ensuring logfiles directory...
mkdir -p /app/logs

echo "Checking migration is valid..."
python /app/manage.py check
returnCode=$?
checkResault $returnCode 'check'

echo "Creating Database Tables..."
python /app/manage.py migrate --noinput
returnCode=$?
checkResault $returnCode 'migrate'

#Collect Static files
python manage.py collectstatic --noinput

# Run Firefox web driver
/usr/bin/Xvfb :99 -ac &

#Create DB admin user
echo "import django; \
      django.setup(); \
      from django.contrib.auth import get_user_model; \
      User = get_user_model(); \
      User.objects.create_superuser( '${CI_ADMIN_USER}', '${CI_ADMIN_MAIL}', '${CI_ADMIN_PASSWORD}')\
" | $Python /app/manage.py shell


exec "$@"
