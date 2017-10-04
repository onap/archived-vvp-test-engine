 
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
import time

from django.conf import settings
import psycopg2

from services.constants import Constants
from services.database.db_bridge import DBBridge
from services.database.db_general import DBGeneral
from services.database.db_virtual_function import DBVirtualFunction
from services.frontend.base_actions.wait import Wait
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()

class DBUser:

    @staticmethod
    def get_activation_url(email):
        # Fetch one user ID.
        uuid = DBUser.select_user_uuid(email)
        # Fetch one user ID.
        index = DBGeneral.select_where_email("id", "auth_user", email)
        activation_token = DBGeneral.select_where(
            "activation_token", "ice_custom_user", "user_ptr_id", index, 1)
        # / activate /:userID /:token
        activationUrl = settings.ICE_PORTAL_URL + '/#/activate/' + \
            str(uuid) + '/' + str(activation_token)
        logger.debug("activationUrl :" + activationUrl)
        return activationUrl

    @staticmethod
    def get_contact_signup_url(invite_token, uuid, email, fullName, phoneNum, companyName):
        companyId = DBGeneral.select_where(
            "uuid", "ice_vendor", "name", companyName, 1)
        signUpURLforContact = settings.ICE_PORTAL_URL + "#/signUp?invitation=" + invite_token + \
            "&email=" + email + "&full_name=" + fullName + \
            "&phone_number=" + phoneNum + "&company=" + companyId
        logger.debug("SignUpURLforContact :" + signUpURLforContact)
        return signUpURLforContact

    @staticmethod
    def select_invitation_token(queryColumnName, queryTableName, whereParametrType, whereParametrValue, email, fetchNum):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "select %s from %s Where %s = '%s' and email = '%s' ;" % (
                queryColumnName, queryTableName, whereParametrType, whereParametrValue, email)
            logger.debug("Query : " + queryStr)
            cur.execute(queryStr)
            if (fetchNum == 0):
                result = str(cur.fetchall())
            elif (fetchNum == 1):
                result = str(cur.fetchone())
                if(result.find("',)") != -1):  # formatting strings e.g uuid
                    result = result.partition('\'')[-1].rpartition('\'')[0]
                elif(result.find(",)") != -1):  # formatting ints e.g id
                    result = result.partition('(')[-1].rpartition(',')[0]
            dbConn.close()
            if result == None:
                errorMsg = "select_where_pr_state FAILED "
                logger.error(errorMsg)
                raise
            logger.debug("Query result: " + str(result))
            return result
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "select_where FAILED "
            raise Exception(errorMsg, "select_where")

    @staticmethod
    def get_el_name(vfName):
        try:
            # Fetch one AT&T user ID.
            engagement_id = DBVirtualFunction.select_eng_uuid(vfName)
            engagement_manual_id = DBGeneral.select_where(
                "engagement_manual_id", "ice_engagement", "uuid", engagement_id, 1)
            reviewer_id = DBGeneral.select_where(
                "reviewer_id", "ice_engagement", "engagement_manual_id", engagement_manual_id, 1)
            engLeadFullName = DBGeneral.select_where_and(
                "full_name", "ice_user_profile", "id", reviewer_id, "role_id", "2", 1)
            return engLeadFullName
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "get_el_name FAILED "
            raise Exception(errorMsg, "get_el_name")

    @staticmethod
    def get_email_by_full_name(fullname):
        #         try:
        query_str = "select email from ice_user_profile where full_name = '%s';" % (
            fullname)
        user_email = DBGeneral.select_query(query_str)
        return user_email
#         except:  # If failed - count the failure and add the error to list of errors.
#             errorMsg = "get_email_by_full_name FAILED "
#             raise Exception(errorMsg, "get_el_name")

    @staticmethod
    def select_recent_vf_of_user(user_uuid, fetchNum):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "SELECT vf_id FROM public.ice_recent_engagement where user_uuid = '%s' order by last_update desc limit 20;" % (
                user_uuid)
            logger.debug("Query : " + queryStr)
            cur.execute(queryStr)
            if (fetchNum == 0):
                result = str(cur.fetchall())
            elif (fetchNum == 1):
                result = str(cur.fetchone())
                if(result.find("',)") != -1):  # formatting strings e.g uuid
                    result = result.partition('\'')[-1].rpartition('\'')[0]
                elif(result.find(",)") != -1):  # formatting ints e.g id
                    result = result.partition('(')[-1].rpartition(',')[0]
            dbConn.close()
            logger.debug("Query result: " + str(result))
            return result
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "select_where FAILED "
            raise Exception(errorMsg, "select_where")

    @staticmethod
    def select_el_email(vfName):
        try:
            # Fetch one AT&T user ID.
            engagement_id = DBVirtualFunction.select_eng_uuid(vfName)
            engagement_manual_id = DBGeneral.select_where(
                "engagement_manual_id", "ice_engagement", "uuid", engagement_id, 1)
            reviewer_id = DBGeneral.select_where(
                "reviewer_id", "ice_engagement", "engagement_manual_id", engagement_manual_id, 1)
            engLeadEmail = DBGeneral.select_where_and(
                "email", "ice_user_profile", "id", reviewer_id, "role_id", "2", 1)
            return engLeadEmail
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "select_el_email FAILED "
            raise Exception(errorMsg, "select_el_email")

    @staticmethod
    def select_user_native_id(email):
        try:
            # Fetch one AT&T user ID.
            engLeadId = DBUser.select_user_profile_property(email, "id")
            return engLeadId
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "select_user_native_id FAILED "
            raise Exception(errorMsg, "select_user_native_id")

    @staticmethod
    def select_personal_next_step(email):
        user_id = DBUser.select_user_native_id(email)
        return DBGeneral.select_where("uuid", "ice_next_step", "owner_id", user_id, 1)

    @staticmethod
    def select_pr_email(vfName):
        try:
            # Fetch one AT&T user ID.
            engagement_id = DBVirtualFunction.select_eng_uuid(vfName)
            engagement_manual_id = DBGeneral.select_where(
                "engagement_manual_id", "ice_engagement", "uuid", engagement_id, 1)
            reviewer_id = DBGeneral.select_where(
                "peer_reviewer_id", "ice_engagement", "engagement_manual_id", engagement_manual_id, 1)
            engLeadEmail = DBGeneral.select_where(
                "email", "ice_user_profile", "id", reviewer_id, 1)
            return engLeadEmail
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "select_el_email FAILED "
            raise Exception(errorMsg, "select_el_email")

    @staticmethod
    def get_notification_id_by_email(userEmail):
        uuid = DBGeneral.select_where_email(
            "id", "ice_user_profile", userEmail)
        notifIDs = DBGeneral.select_where(
            "uuid", "ice_notification", "user_id", uuid, 0)
        return notifIDs

    @staticmethod
    def get_not_seen_notifications_number_by_email(user_email, is_negative=False):
        user_id = DBGeneral.select_where_email(
            "id", Constants.DBConstants.IceTables.USER_PROFILE, user_email)
        notifications_number = DBGeneral.select_where_and(
            Constants.DBConstants.Queries.COUNT, Constants.DBConstants.IceTables.NOTIFICATION, "user_id", user_id, "is_read", "False", 1)
        if is_negative:
            counter = 0
            while notifications_number != "0" and counter <= Constants.Dashboard.Avatar.Notifications.Count.RETRIES_NUMBER:
                notifications_number = DBGeneral.select_where_and(
                    Constants.DBConstants.Queries.COUNT, Constants.DBConstants.IceTables.NOTIFICATION, "user_id", user_id, "is_read", "False", 1)
                time.sleep(1)
                counter += 1
        return notifications_number

    @staticmethod
    def get_eng_lead_email_per_enguuid(enguuid):
        reviewer_id = DBGeneral.select_where(
            "reviewer_id", Constants.DBConstants.IceTables.ENGAGEMENT, "uuid", enguuid, 1)
        engLeadEmail = DBGeneral.select_where(
            "email", Constants.DBConstants.IceTables.USER_PROFILE, "id", reviewer_id, 1)
        return engLeadEmail

    @staticmethod
    def select_all_user_engagements(engLeadID):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "select COUNT(*) from ice_engagement_engagement_team Where iceuserprofile_id = %s  and (select engagement_stage from public.ice_engagement where uuid = engagement_id LIMIT 1) != 'Archived';" % (
                engLeadID)
            logger.debug("Query : " + queryStr)
            cur.execute(queryStr)
            result = cur.fetchall()
            dbConn.close()
            logger.debug("Query result: " + str(result))
            logger.debug(result[0][0])
            return result[0][0]
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "select_user_engagements_by_stage FAILED "
            raise Exception(errorMsg, "select_user_engagements_by_stage")

    @staticmethod
    def select_user_engagements_by_stage(stage, engLeadID):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "select count(*) from ice_engagement INNER JOIN ice_engagement_engagement_team ON ice_engagement_engagement_team.engagement_id= ice_engagement.uuid Where (ice_engagement.engagement_stage  = '%s')  and (ice_engagement_engagement_team.iceuserprofile_id =  %s );" % (
                stage, engLeadID)
            logger.debug("Query : " + queryStr)
            cur.execute(queryStr)
            result = cur.fetchall()
            dbConn.close()
            logger.debug("Query result: " + str(result))
            logger.debug(result[0][0])
            return result[0][0]
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "select_user_engagements_by_stage FAILED "
            raise Exception(errorMsg, "select_user_engagements_by_stage")

    @staticmethod
    def set_new_temp_password(email):
        encodePass = DBGeneral.select_where_email(
            "password", "auth_user", Constants.Users.Admin.EMAIL)
        # Fetch one user ID.
        index = DBGeneral.select_where_email("id", "auth_user", email)
        DBGeneral.update_where(
            "ice_custom_user", "temp_password", encodePass, "user_ptr_id", index)

    @staticmethod
    def set_password_to_default(email):
        encodePass = DBGeneral.select_where_email(
            "password", "auth_user", Constants.Users.Admin.EMAIL)
        DBGeneral.update_where(
            "auth_user", "password", encodePass, "email", email)

    @staticmethod
    def select_el_not_in_engagement(el_name, pr_name):
        query_str = "select full_name from ice_user_profile where role_id = 2 and full_name != '%s' and full_name != '%s';" % (
            el_name, pr_name)
        new_user = DBGeneral.select_query(query_str)
        if new_user == 'None':
            new_user = DBUser.update_to_el_not_in_engagement()
        return new_user

    @staticmethod
    def select_user_uuid(email):
        user_uuid = DBUser.select_user_profile_property(email, "uuid")
        return user_uuid
    
    @staticmethod
    def select_access_key(email):
        access_key = DBUser.select_user_profile_property(email, "rgwa_access_key")
        return access_key
    
    @staticmethod
    def select_secret_key(email):
        secret_key = DBUser.select_user_profile_property(email, "rgwa_secret_key")
        return secret_key
    
    @staticmethod
    def update_to_el_not_in_engagement():
        query_str = "select uuid from ice_user_profile where role_id = 1 ;"
        user_uuid = DBGeneral.select_query(query_str)
        updatequery = "UPDATE ice_user_profile SET role_id=2 ,full_name = 'el_for_test' WHERE uuid = '%s' ;" % (
            user_uuid)
        DBGeneral.update_query(updatequery)
        updatequery = "UPDATE ice_user_profile SET role_id=2 WHERE full_name = '%s' ;" % (
            'el_for_test')
        DBGeneral.update_query(updatequery)
        return 'el_for_test'

    @staticmethod
    def rollback_for_el_not_in_engagement():
        query_str = "select uuid from ice_user_profile where full_name = 'el_for_test';"
        user_uuid = DBGeneral.select_query(query_str)
        fullName = DBBridge.helper_rand_string("randomString")
        updatequery = "UPDATE ice_user_profile SET role_id=1,full_name = '%s' WHERE uuid = '%s'  ;" % (
            fullName, user_uuid)
        DBGeneral.update_query(updatequery)

    @staticmethod
    def set_engagement_peer_reviewer(engagement_uuid, email):
        user_uuid = DBUser.select_user_uuid(email)
        update_query = "UPDATE ice_user_profile SET role_id=2 WHERE uuid = '%s';" % user_uuid
        DBGeneral.update_query(update_query)

        user_id = DBGeneral.select_query(
            "SELECT id FROM ice_user_profile WHERE uuid = '%s';" % user_uuid)
        update_query = "UPDATE ice_engagement SET peer_reviewer_id=%s WHERE uuid = '%s';" % (
            user_id, engagement_uuid)
        DBGeneral.update_query(update_query)

    @staticmethod
    def select_user_profile_property(user_email, property_name):
        return DBGeneral.select_where(property_name, "ice_user_profile", "email", user_email, 1)

    @staticmethod
    def validate_user_profile_settings_in_db(user_email, checked):
        Wait.page_has_loaded()
        regular_email_updates = DBUser.select_user_profile_property(
            user_email, 'regular_email_updates')
        DBBridge.helper_internal_assert(regular_email_updates, checked)
        email_updates_on_every_notification = \
            DBUser.select_user_profile_property(
                user_email, 'email_updates_on_every_notification')
        DBBridge.helper_internal_assert(
            email_updates_on_every_notification, checked)
        email_updates_daily_digest = DBUser.select_user_profile_property(
            user_email, 'email_updates_daily_digest')
        DBBridge.helper_internal_assert(
            email_updates_daily_digest, not checked)

    @staticmethod
    def retrieve_admin_ssh_from_db():
        ssh_key = DBGeneral.select_where(
            'ssh_public_key', Constants.DBConstants.IceTables.USER_PROFILE,
            'email', Constants.Users.Admin.EMAIL, 1)
        return ssh_key

    @staticmethod
    def get_access_key(user_uuid):
        counter = 0
        access_key = DBGeneral.select_where(
            "rgwa_access_key", Constants.DBConstants.IceTables.USER_PROFILE, "uuid", user_uuid, 1)
        while access_key == "None" and counter <= Constants.RGWAConstants.RETRIES_NUMBER:
            time.sleep(session.wait_until_time_pause)
            logger.debug(
                "rgwa_access_key are not ready yet, trying again (%s of 20)" % counter)
            access_key = DBGeneral.select_where(
                "rgwa_access_key", Constants.DBConstants.IceTables.USER_PROFILE, "uuid", user_uuid, 1)
            counter += 1
        return access_key

    @staticmethod
    def get_access_secret(user_uuid):
        counter = 0
        access_secret = DBGeneral.select_where(
            "rgwa_secret_key", Constants.DBConstants.IceTables.USER_PROFILE, "uuid", user_uuid, 1)
        while access_secret == "None" and counter <= Constants.RGWAConstants.RETRIES_NUMBER:
            time.sleep(session.wait_until_time_pause)
            logger.debug(
                "rgwa_secret_key are not ready yet, trying again (%s of 100)" % counter)
            access_secret = DBGeneral.select_where(
                "rgwa_secret_key", Constants.DBConstants.IceTables.USER_PROFILE, "uuid", user_uuid, 1)
            
            counter += 1
        return access_secret
