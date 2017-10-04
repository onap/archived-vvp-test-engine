 
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
import uuid

from django.conf import settings
import psycopg2

from services.constants import Constants
from services.database.db_bridge import DBBridge
from services.database.db_general import DBGeneral
from services.logging_service import LoggingServiceFactory


logger = LoggingServiceFactory.get_logger()

class DBVirtualFunction:

    @staticmethod
    def insert_ecomp_release(uuid, name, ui_visibility="TRUE"):
        try:
            queryTableName = "ice_ecomp_release"
            # Connect to General 'default'.
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection("em_db"))
            dbConn = dbConn
            cur = dbConn.cursor()
            logger.debug("DATABASE_TYPE: " + settings.DATABASE_TYPE)
        except Exception as e:
            errorMsg = "Failed to create connection to General: " + str(e)
            raise Exception(errorMsg)
        try:
            logger.debug("DATABASE_TYPE: " + settings.DATABASE_TYPE)
            # Create INSERT query.
            queryStr = "INSERT INTO %s (""uuid, name, weight, ui_visibility"") VALUES ('%s', '%s', '%s', '%s');" % (
                queryTableName, uuid, name, 0, ui_visibility)
            logger.debug("Query: " + queryStr)
            cur.execute(queryStr)  # Execute query.
            dbConn.commit()
            logger.debug("Test results are in General now.")
        except Exception as e:
            errorMsg = "Failed to insert ECOMP release to General:" + str(e)
            raise Exception(errorMsg)
        dbConn.close()

    @staticmethod
    def delete_ecomp_release(uuid, name):
        try:
            queryTableName = "ice_ecomp_release"
            # Connect to General 'default'.
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection("em_db"))
            dbConn = dbConn
            cur = dbConn.cursor()
        except Exception as e:
            errorMsg = "Failed to create connection to DBGeneral.because :" + \
                str(e)
            raise Exception(errorMsg)
        try:
            # Create INSERT query.
            queryStr = "DELETE FROM %s WHERE uuid = '%s';" % (
                queryTableName, uuid)
            logger.debug("Query: " + queryStr)
            cur.execute(queryStr)  # Execute query.
            dbConn.commit()
            logger.debug("Test results are in General now.")
        except Exception as e:
            errorMsg = "Failed to delete ECOMP release from General . because :" + \
                str(e)
            raise Exception(errorMsg)
            raise
        dbConn.close()

    @staticmethod
    def select_next_steps_ids(engagement_uuid):
        ice_next_steps = DBGeneral.select_where(
            "uuid", "ice_next_step", "engagement_id", engagement_uuid, 0)
        return ice_next_steps

    @staticmethod
    def select_next_steps_uuids_by_stage(engagement_uuid, engagement_stage):
        query = "SELECT uuid FROM %s WHERE engagement_id='%s' AND engagement_stage='%s' ORDER BY position;" % (
            Constants.DBConstants.IceTables.NEXT_STEP, engagement_uuid, engagement_stage)
        return DBGeneral.select_query(query, "list", 0)

    @staticmethod
    def update_next_step_position(next_step_uuid, new_index):
        DBGeneral.update_where(
            "ice_next_step", "position", new_index, "uuid", next_step_uuid)

    @staticmethod
    def select_next_step_description(next_step_uuid):
        return DBGeneral.select_where("description", "ice_next_step", "uuid", next_step_uuid, 1)

    @staticmethod
    def select_eng_uuid(vf_name):
        return DBGeneral.select_where("engagement_id", "ice_vf", "name", vf_name, 1)

    @staticmethod
    def select_engagment_uuid_by_vf_name(vfName):
        engagement_id = DBGeneral.select_where(
            "engagement_id", "ice_vf", "name", vfName, 1)
        engagement_manual_id = DBGeneral.select_where(
            "engagement_manual_id", "ice_engagement", "uuid", engagement_id, 1)
        enguuid = DBGeneral.select_where(
            "uuid", "ice_engagement", "engagement_manual_id", engagement_manual_id, 1)
        return enguuid

    @staticmethod
    def select_vf_version_by_vf_name(vfName):
        queryStr = "SELECT version FROM ice_vf WHERE name= '%s';" % vfName
        version_name = str(DBGeneral.select_query(queryStr))
        return version_name

    @staticmethod
    def select_vf_name_by_vf_version(version_name):
        queryofname = "SELECT name FROM ice_vf WHERE version= '%s';" % version_name
        vfNameDb = str(DBGeneral.select_query(queryofname))
        return vfNameDb

    @staticmethod
    def return_expected_steps(engagement_uuid, stage, user_email):
        steps_uuids = DBVirtualFunction.select_next_steps_uuids_by_stage(
            engagement_uuid, stage)
        personal_step_uuid = DBBridge.select_personal_next_step(user_email)
        DBVirtualFunction.update_next_step_position(personal_step_uuid, 1)
        steps_uuids.insert(0, personal_step_uuid)
        return steps_uuids

    @staticmethod
    def get_engagement():
        """Use this function instead of creating a new engagement where no need to"""
        queryStr = "SELECT DISTINCT ice_engagement.uuid, engagement_manual_id, ice_vf.name, ice_user_profile.full_name, \
                    ice_user_profile.email, reviewer_table.full_name, reviewer_table.email, \
                    ice_deployment_target.version, ice_ecomp_release.name \
                    FROM ice_engagement LEFT JOIN ice_vf ON engagement_id = ice_engagement.uuid \
                    LEFT JOIN ice_user_profile reviewer_table ON reviewer_table.id = ice_engagement.reviewer_id \
                    LEFT JOIN ice_user_profile ON ice_user_profile.id = ice_engagement.peer_reviewer_id \
                    LEFT JOIN ice_deployment_target ON ice_deployment_target.uuid = ice_vf.deployment_target_id \
                    LEFT JOIN ice_ecomp_release ON ice_ecomp_release.uuid = ice_vf.ecomp_release_id \
                    WHERE ice_user_profile.id IS NOT NULL LIMIT 1;"
        list_of_values = DBGeneral.select_query(queryStr, return_type="list")
        list_of_keys = ["engagement_uuid", "engagement_manual_id", "vfName", "pr_name",
                        "pr_email", "el_name", "el_email", "target_aic", "ecomp_release"]
        return dict(zip(list_of_keys, list_of_values))

    @staticmethod
    def insert_aic_version(ui_visibility="TRUE"):
        new_aic_version = {
            "uuid": str(uuid.uuid4()), "name": "AIC", "version": DBBridge.helper_rand_string("randomNumber", 2), "ui_visibility": ui_visibility, "weight": 0}
        queryStr = "INSERT INTO public.ice_deployment_target( \
                    uuid, name, version, ui_visibility, weight) \
                    VALUES ('%s', '%s', '%s', '%s', %s);" % (new_aic_version['uuid'], new_aic_version['name'], new_aic_version['version'], new_aic_version['ui_visibility'], new_aic_version['weight'])
        DBGeneral.insert_query(queryStr)
        return new_aic_version

    @staticmethod
    def delete_aic_version(aic_uuid):
        DBGeneral.insert_query(
            "DELETE FROM public.ice_deployment_target WHERE uuid='%s';" % aic_uuid)

    @staticmethod
    def change_aic_version_weight(new_weight, old_weight):
        DBGeneral.insert_query(
            "UPDATE public.ice_deployment_target SET weight=%s WHERE weight=%s" % (new_weight, old_weight))

    @staticmethod
    def change_ecomp_release_weight(new_weight, old_weight):
        DBGeneral.insert_query(
            "UPDATE public.ice_ecomp_release SET weight=%s WHERE weight=%s" % (new_weight, old_weight))

    @staticmethod
    def select_aic_version_uuid(aic_version):
        return DBGeneral.select_where("uuid", "ice_deployment_target", "version", aic_version, 1)

    @staticmethod
    def select_ecomp_release_uuid(ecomp_release):
        return DBGeneral.select_where("uuid", "ice_ecomp_release", "name", ecomp_release, 1)

    @staticmethod
    def add_admin_to_eng_team(eng_uuid):
        admin_db_id = DBGeneral.select_where(
            'id', Constants.DBConstants.IceTables.USER_PROFILE, 'email', Constants.Users.Admin.EMAIL, 1)
        queryStr = "INSERT INTO public.ice_engagement_engagement_team(engagement_id, iceuserprofile_id) VALUES ('%s', '%s');" % (
            eng_uuid, admin_db_id)
        logger.debug("add_admin_to_eng_team Query: %s" % queryStr)
        DBGeneral.insert_query(queryStr)

    @staticmethod
    def remove_engagement_from_recent(vf_uuid):
        DBGeneral.insert_query(
            "DELETE FROM %s WHERE vf_id='%s'" % (Constants.DBConstants.IceTables.RECENT, vf_uuid))
