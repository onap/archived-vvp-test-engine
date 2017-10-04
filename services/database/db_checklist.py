 
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
from uuid import uuid4

from django.utils import timezone
import psycopg2

from services.constants import Constants
from services.database.db_general import DBGeneral
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()

class DBChecklist:

    @staticmethod
    def select_where_approval_state(queryColumnName, queryTableName, whereParametrType, whereParametrValue, fetchNum):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "select %s from %s Where %s = '%s' and state = 'approval';" % (
                queryColumnName, queryTableName, whereParametrType, whereParametrValue)
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
            if result == None:
                errorMsg = "select_where_approval_state FAILED "
                logger.error(errorMsg)
                raise
            return result
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "select_where_approval_state FAILED "
            raise Exception(errorMsg, "select_where_approval_state FAILED")

    @staticmethod
    def select_where_pr_state(queryColumnName, queryTableName, whereParametrType, whereParametrValue, fetchNum):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "select %s from %s Where %s = '%s' and state = 'peer_review';" % (
                queryColumnName, queryTableName, whereParametrType, whereParametrValue)
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
    def select_where_cl_not_archive(queryColumnName, queryTableName, whereParametrType, whereParametrValue, fetchNum):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "select %s from %s Where %s = '%s' and state != 'archive';" % (
                queryColumnName, queryTableName, whereParametrType, whereParametrValue)
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
    def select_native_where(queryColumnName, queryTableName, whereParametrType, whereParametrValue, fetchNum):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "select %s from %s Where %s = '%s';" % (
                queryColumnName, queryTableName, whereParametrType, whereParametrValue)
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
    def update_checklist_to_review_state(queryTableName):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "UPDATE ice_checklist SET state='review' Where name= '%s' and state= 'pending';" % (
                queryTableName)
            logger.debug("Query : " + queryStr)
            cur.execute(queryStr)
            dbConn.commit()
            dbConn.close()
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "Could not Update User"
            raise Exception(errorMsg, "Update")

    @staticmethod
    def update_all_decisions_to_approve(whereParametrValue):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "UPDATE ice_checklist_decision SET review_value='approved' , peer_review_value='approved'  Where checklist_id = '%s';" % (
                whereParametrValue)
            logger.debug(queryStr)
            cur.execute(queryStr)
            dbConn.commit()
            logger.debug("Query : " + queryStr)
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "Could not Update User"
            logger.debug(e)
            raise Exception(errorMsg, "Update")
        finally:
            dbConn.close()

    @staticmethod
    def is_archive(checklistName):
        try:
            result = False
            # Fetch all AT&T user ID.
            checklist_ids = DBGeneral.select_where(
                "uuid", "ice_checklist", "name", checklistName, 0)
#             checklist_ids = DBGeneral.list_format(checklist_ids)
            for checklist_id in checklist_ids:  # Second Example
                if isinstance(checklist_id, tuple):
                    checklist_id = checklist_id[0]
                state = DBGeneral.select_where(
                    "state", "ice_checklist", "uuid", checklist_id, 1)
                if state == "archive":
                    result = True
                    break
            return result
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "is_archive FAILED "
            raise Exception(errorMsg, "is_archive")

    @staticmethod
    def get_pr_email(checklistUuid):
        try:
            # Fetch one AT&T user ID.
            owner_id = DBChecklist.select_where_pr_state(
                "owner_id", "ice_checklist", "uuid", checklistUuid, 1)
            engLeadEmail = DBGeneral.select_where(
                "email", "ice_user_profile", "id", owner_id, 1)
            logger.debug("get_pr_email = " + engLeadEmail)
            return engLeadEmail
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            errorMsg = "get_pr_email FAILED " + str(e)
            raise Exception(errorMsg, "get_pr_email")

    @staticmethod
    def get_admin_email(checklistUuid):
        try:
            owner_id = DBChecklist.select_where_approval_state(
                "owner_id", "ice_checklist", "uuid", checklistUuid, 1)  # Fetch one AT&T user ID.
            engLeadEmail = DBGeneral.select_where(
                "email", "ice_user_profile", "id", owner_id, 1)
            logger.debug("get_admin_email = " + engLeadEmail)
            return engLeadEmail
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "get_admin_email FAILED "
            raise Exception(errorMsg, "get_admin_email")

    @staticmethod
    def get_owner_email(checklistUuid):
        try:
            # Fetch one AT&T user ID.
            owner_id = DBChecklist.select_native_where(
                "owner_id", "ice_checklist", "uuid", checklistUuid, 1)
            engLeadEmail = DBGeneral.select_where(
                "email", "ice_user_profile", "id", owner_id, 1)
            logger.debug("getPreeReviewerEngLeadEmail = " + engLeadEmail)
            return engLeadEmail
        # If failed - count the failure and add the error to list of errors.
        except:
            errorMsg = "get_admin_email FAILED "
            raise Exception(errorMsg, "get_owner_email")

    @staticmethod
    def update_decisions(checklistUuid, checklistName):
        checklistTempid = DBGeneral.select_where(
            "template_id", "ice_checklist", "name", checklistName, 1)
        checklistLineItems = DBGeneral.select_where_and(
            "uuid", "ice_checklist_line_item", "line_type", "auto", "template_id", checklistTempid, 0)
        for lineItem in checklistLineItems:
            setParametrType2 = "peer_review_value"
            setParametrValue2 = "approved"
            whereParametrType2 = "lineitem_id"
            whereParametrValue2 = lineItem
            DBGeneral.update_where_and("ice_checklist_decision", "review_value", checklistUuid, "approved",
                                       "checklist_id", setParametrType2, setParametrValue2, whereParametrType2, whereParametrValue2)

    @staticmethod
    def checkChecklistIsUpdated():
        query = "select uuid from ice_checklist_section where template_id in (select template_id from ice_checklist_template where name='{template_name}') and name='{section_name}'".format(
            template_name=Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT, section_name=Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT)
        return DBGeneral.select_query(query)

    @staticmethod
    def fetchEngByVfName(vfName):
        # Fetch one AT&T user ID.
        return DBGeneral.select_where("engagement_id", "ice_vf", "name", vfName, 1)

    @staticmethod
    def fetchEngManIdByEngUuid(engagement_id):
        return DBGeneral.select_where("engagement_manual_id", "ice_engagement", "uuid", engagement_id, 1)

    @staticmethod
    def fetchChecklistByName(checklistName):
        query = "select uuid from ice_checklist where name='{cl_name}'".format(
            cl_name=checklistName)
        return DBGeneral.select_query(query)

    @staticmethod
    def create_default_heat_teampleate():
        template_query = "INSERT INTO public.ice_checklist_template(uuid, name, category, version, create_time)"\
            "VALUES ('%s', '%s', '%s', '%s', '%s');" % (
                str(uuid4()), 'Editing Heat', 'first category', '1', timezone.now())
        DBGeneral.insert_query(template_query)
        template_id = DBGeneral.select_query(
            "SELECT uuid FROM public.ice_checklist_template where name = 'Editing Heat'")
        # SECTIONS
        section1_query = "INSERT INTO public.ice_checklist_section(uuid, name, weight, description, validation_instructions, create_time, template_id) "\
            "VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s');" % (str(uuid4()), 'External References',
                                                                   '1', 'section descripyion', 'valid instructions', timezone.now(), template_id)
        DBGeneral.insert_query(section1_query)
        section1_id = DBGeneral.select_query(
            ("""SELECT uuid FROM public.ice_checklist_section where name = 'External References' and template_id = '{s}'""").format(s=template_id))
        section2_query = "INSERT INTO public.ice_checklist_section(uuid, name, weight, description, validation_instructions, create_time, template_id) "\
            "VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s');" % (str(uuid4()), 'Parameter Specification',
                                                                   '2', 'section descripyion', 'valid instructions', timezone.now(), template_id)
        DBGeneral.insert_query(section2_query)
        section2_id = DBGeneral.select_query(
            ("""SELECT uuid FROM public.ice_checklist_section where name = 'Parameter Specification' and template_id = '{s}'""").format(s=template_id))
        # Line items
        line_item1 = "INSERT INTO public.ice_checklist_line_item(uuid, name, weight, description, line_type, validation_instructions,create_time,section_id, template_id) "\
            "VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s');" % (str(uuid4()), 'Normal references', '1', 'Numeric parameters should include range and/or allowed values.', 'manual',
                                                                               'Here are some useful tips for how to validate this item in the most awesome way:<br><br><ul><li>Here is my awesome tip 1</li><li>Here is my awesome tip 2</li><li>Here is my awesome tip 3</li></ul>', timezone.now(), section1_id, template_id)
        DBGeneral.insert_query(line_item1)
        line_item2 = "INSERT INTO public.ice_checklist_line_item(uuid, name, weight, description, line_type, validation_instructions,create_time, section_id, template_id) "\
            "VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s');" % (str(uuid4()), 'String parameters', '2', 'Numeric parameters should include range and/or allowed values.', 'auto',
                                                                               'Here are some useful tips for how to validate this item in the most awesome way:<br><br><ul><li>Here is my awesome tip 1</li><li>Here is my awesome tip 2</li><li>Here is my awesome tip 3</li></ul>', timezone.now(), section2_id, template_id)
        DBGeneral.insert_query(line_item2)
        line_item3 = "INSERT INTO public.ice_checklist_line_item(uuid, name, weight, description, line_type, validation_instructions,create_time,section_id, template_id) "\
            "VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s');" % (str(uuid4()), 'Numeric parameters', '3', 'Numeric parameters should include range and/or allowed values.', 'manual',
                                                                               'Here are some useful tips for how to validate this item in the most awesome way:<br><br><ul><li>Here is my awesome tip 1</li><li>Here is my awesome tip 2</li><li>Here is my awesome tip 3</li></ul>', timezone.now(), section2_id, template_id)
        DBGeneral.insert_query(line_item3)
        line_item4 = "INSERT INTO public.ice_checklist_line_item(uuid, name, weight, description, line_type, validation_instructions,create_time, section_id, template_id) "\
            "VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s');" % (str(uuid4()), 'VF image', '2', 'Numeric parameters should include range and/or allowed values.', 'auto',
                                                                               'Here are some useful tips for how to validate this item in the most awesome way:<br><br><ul><li>Here is my awesome tip 1</li><li>Here is my awesome tip 2</li><li>Here is my awesome tip 3</li></ul>', timezone.now(), section1_id, template_id)
        DBGeneral.insert_query(line_item4)
        line_item5 = "INSERT INTO public.ice_checklist_line_item(uuid, name, weight, description, line_type, validation_instructions,create_time,section_id, template_id) "\
            "VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s');" % (str(uuid4()), 'Parameters', '1', 'Numeric parameters should include range and/or allowed values.', 'auto',
                                                                               'Here are some useful tips for how to validate this item in the most awesome way:<br><br><ul><li>Here is my awesome tip 1</li><li>Here is my awesome tip 2</li><li>Here is my awesome tip 3</li></ul>', timezone.now(), section2_id, template_id)
        DBGeneral.insert_query(line_item5)

    @staticmethod
    def create_editing_cl_template_if_not_exist():
        template_id = DBGeneral.select_query(("""SELECT uuid FROM public.ice_checklist_template where name = '{s}'""").format(
            s=Constants.Dashboard.LeftPanel.EditChecklistTemplate.HEAT))
        if template_id == 'None':
            DBChecklist.create_default_heat_teampleate()
            session.createTemplatecount = True

    @staticmethod
    def state_changed(identify_field, field_value, expected_state):
        get_state = str(DBGeneral.select_where(
            "state", Constants.DBConstants.IceTables.CHECKLIST, identify_field, field_value, 1))
        counter = 0
        while get_state != expected_state and counter <= Constants.DBConstants.RETRIES_NUMBER:
            time.sleep(session.wait_until_time_pause_long)
            logger.debug("Checklist state not changed yet , expecting state: %s, current result: %s (attempt %s of %s)" % (
                expected_state, get_state, counter, Constants.DBConstants.RETRIES_NUMBER))
            counter += 1
            get_state = str(DBGeneral.select_where(
                "state", Constants.DBConstants.IceTables.CHECKLIST, identify_field, field_value, 1))

        if get_state == expected_state:
            logger.debug("Checklist state was successfully changed into: " +
                         expected_state + ", and was verified over the DB")
            return expected_state
        raise Exception(
            "Expected checklist state never arrived " + expected_state, get_state)

    @staticmethod
    def get_recent_checklist_uuid(name):
        required_uuid = DBGeneral.select_where_not_and_order_by_desc(
            'uuid', Constants.DBConstants.IceTables.CHECKLIST, 'name', name, 'state', Constants.ChecklistStates.Archive.TEXT, 'create_time')
        return required_uuid
