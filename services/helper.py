 
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
import os
import random
import string
import subprocess
import unittest

from cryptography.hazmat.backends import default_backend as crypto_default_backend, \
    default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from django.conf import settings

from services.constants import Constants
from services.database.db_user import DBUser
from services.logging_service import LoggingServiceFactory
from utils.authentication import JWTAuthentication


logger = LoggingServiceFactory.get_logger()

class Helper:

    tc = unittest.TestCase('__init__')

    @staticmethod
    def rand_string(type_of_value='randomString', numberOfDigits=0):
        letters_and_numbers = string.ascii_letters + string.digits
        if type_of_value == 'email':
            myEmail = ''.join(random.choice(letters_and_numbers) for _ in range(
                4)) + "@" + ''.join(random.choice(string.ascii_uppercase) for _ in range(4)) + ".com"
            return "ST" + myEmail
        elif type_of_value == 'randomNumber':
            randomNumber = ''.join("%s" % random.randint(2, 9)
                                   for _ in range(0, (numberOfDigits + 1)))
            return randomNumber
        elif type_of_value == 'randomString':
            randomString = "".join(random.sample(letters_and_numbers, 5))
            return "ST" + randomString
        else:
            raise Exception("invalid rand type")

    @staticmethod
    def rand_invite_email():
        inviteEmail = "automationqatt" + \
            Helper.rand_string("randomString") + "@gmail.com"
        return inviteEmail

    @staticmethod
    def generate_sshpub_key():
        try:
            logger.debug("About to generate SSH Public Key")
            key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            private_key = key.private_bytes(
                encoding=crypto_serialization.Encoding.PEM,
                format=crypto_serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=crypto_serialization.NoEncryption())
            public_key = key.public_key().public_bytes(
                crypto_serialization.Encoding.OpenSSH,
                crypto_serialization.PublicFormat.OpenSSH
            ).decode("utf-8")

            logger.debug("Generated SSH Public Key: " + public_key)
        except Exception as e:  # If failed write to log the error and return 'None'.
            logger.error(e)
            logger.error("Failed to generate SSH Public Key.")
            raise e
        return public_key

    @staticmethod
    def check_admin_ssh_existence(path, admin_ssh):
        if admin_ssh == open(path).read().rstrip('\n'):
            logger.debug(
                "Admin SSH already defined in DB and equal to the one stored on the local system.")
            return True
        return False

    @staticmethod
    def get_or_create_rsa_key_for_admin():
        try:  # Create pair of keys for the given user and return his public key.
            ssh_folder = Constants.Paths.SSH.PATH
            public_file = ssh_folder + "id_rsa.pub"
            privateFile = ssh_folder + "id_rsa"
            admin_ssh_exist_and_equal = False
            admin_ssh = None
            if not os.path.exists(ssh_folder):
                os.makedirs(ssh_folder)
            elif os.path.exists(public_file):
                admin_ssh = DBUser.retrieve_admin_ssh_from_db()
                admin_ssh_exist_and_equal = Helper.check_admin_ssh_existence(
                    public_file, admin_ssh)
            # TODO find pending gitlab bug causing old ssh key not be updated in gitlab cache
            if False and admin_ssh_exist_and_equal:
                return admin_ssh
            else:
                logger.debug("Private key file: " + privateFile +
                             "\nPublice key file: " + public_file)
                key = rsa.generate_private_key(
                    backend=crypto_default_backend(),
                    public_exponent=65537,
                    key_size=2048
                )
                private_key = key.private_bytes(
                    crypto_serialization.Encoding.PEM,
                    crypto_serialization.PrivateFormat.PKCS8,
                    crypto_serialization.NoEncryption()).decode("utf-8")
                public_key = key.public_key().public_bytes(
                    crypto_serialization.Encoding.OpenSSH,
                    crypto_serialization.PublicFormat.OpenSSH
                ).decode("utf-8")

                with open(privateFile, 'w') as content_file:
                    os.chmod(privateFile, 0o600)
                    content_file.write(private_key)  # Save private key to file.
                logger.debug(
                    "Private key created successfully for admin")
                user_pub_key = public_key
                with open(public_file, 'w') as content_file:
                    content_file.write(public_key)  # Save public key to file.
                logger.debug("Public key created successfully for admin")
                cmd = 'ssh-keyscan ' + \
                    settings.GITLAB_URL[7:-1] + ' >> ' + \
                    ssh_folder + 'known_hosts'
                # Create known_hosts file and add GitLab to it.
                subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
                logger.debug("Added GitLab to known_hosts")
                return user_pub_key
        except Exception as error:
            logger.error(
                "_-_-_-_-_- Unexpected error in get_or_create_rsa_key_for_admin: %s" % error)
            raise Exception("Failed to create SSH keys for user admin", error)

    @staticmethod
    def internal_assert(x, y):
        try:
            Helper.tc.assertEqual(str(x), str(y))
        except Exception as e:
            raise Exception("AssertionError: \"" + str(x) +
                            "\" != \"" + str(y) + "\"", e)

    @staticmethod
    def internal_assert_boolean(x, y):
        try:
            Helper.tc.assertEqual(str(x), str(y))
            return True
        except Exception as e:
            raise Exception("AssertionError: \"" + str(x) +
                            "\" != \"" + str(y) + "\"", e)

    @staticmethod
    def internal_not_equal(x, y):
        try:
            Helper.tc.assertNotEqual(x, y)
        except Exception as e:
            raise Exception("AssertionError: \"" + str(x) +
                            "\" != \"" + str(y) + "\"", e)

    @staticmethod
    def get_reset_passw_url(email):
        jwtObj = JWTAuthentication()
        token = jwtObj.createPersonalTokenWithExpiration(email)
        resetPasswURL = Constants.Default.LoginURL.TEXT + "?t=" + token
        return resetPasswURL

    @staticmethod
    def assertTrue(expr, msg=None):
        """Check that the expression is true."""
        if expr != True:
            raise Exception("AssertionError: \"not expr")
