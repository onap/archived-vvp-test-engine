 
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
# This file is being processed when you create the dockerized env and run: sudo docker build -t att/d2-ice-ci:1.0 .
FROM python:alpine

RUN apk add --no-cache \
    autoconf \
    gcc \
    libffi \
    libffi-dev \
    libpq \
    linux-headers \
    musl-dev \
    postgresql-dev \
    alsa-lib \
    bash \
    binutils \
    bzip2 \
    ca-certificates \
    dbus \
    dbus-glib \
    firefox-esr \
    fontconfig \
    git \
    gtk+3.0 \
    libxcomposite \
    openssh \
    py-psycopg2 \
    py-setuptools \
    sqlite \
    ttf-freefont \
    wget \
    xvfb \
    && :

COPY . /app
ENV PATH=$PATH:/firefox:/usr/bin
WORKDIR /app

RUN ln -s -f /opt/configmaps/settings/__init__.py /app/web/settings/__init__.py

RUN pip install --upgrade setuptools && \
#    pip install uwsgi && \
    pip install gunicorn && \
    pip install -r requirements.txt

RUN apk del \
    autoconf \
    gcc \
    libffi-dev \
    linux-headers \
    musl-dev \
    postgresql-dev \
    && :

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["/usr/local/bin/gunicorn", "-c", "/opt/configmaps/settings/gunicorn.ini" , "web.wsgi:application"]
