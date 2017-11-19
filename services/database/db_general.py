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
from datetime import datetime
import sqlite3

from django.conf import settings
from django.db import transaction
import psycopg2

from services.logging_service import LoggingServiceFactory


logger = LoggingServiceFactory.get_logger()


class DBGeneral:

    @staticmethod
    # desigredDB: Use 'default' for CI General and 'em_db' for EM General
    # (according to settings.DATABASES).
    def return_db_native_connection(desigredDB):
        dbConnectionStr = "dbname='" + str(
            settings.SINGLETONE_DB[desigredDB]['NAME']) + \
            "' user='" + str(settings.SINGLETONE_DB[desigredDB]['USER']) + \
            "' host='" + str(settings.SINGLETONE_DB[desigredDB]['HOST']) + \
            "' password='" + str(
                settings.SINGLETONE_DB[desigredDB]['PASSWORD']) + \
            "' port='" + \
            str(settings.SINGLETONE_DB[desigredDB]['PORT']) + "'"
        return dbConnectionStr

    @staticmethod
    def insert_results(
            testType,
            testFeature,
            testResult,
            testName,
            testDuration,
            notes=" "):
        try:
            if settings.DATABASE_TYPE == 'sqlite':
                dbfile = str(settings.DATABASES['default']['TEST_NAME'])
                dbConn = sqlite3.connect(dbfile)
                cur = dbConn.cursor()
            else:
                # Connect to General 'default'.
                dbConn = psycopg2.connect(
                    DBGeneral.return_db_native_connection("default"))
                dbConn = dbConn
                cur = dbConn.cursor()
        except Exception as e:
            errorMsg = "Failed to create connection to General." + str(e)
            raise Exception(errorMsg)
        try:  # Create INSERT query.
            if settings.DATABASE_TYPE == 'sqlite':
                query_str = 'INSERT INTO ice_test_results ' +\
                    '(testType, testFeature, testResult, testName, notes,'\
                            'create_time, build_id, duration) VALUES ' +\
                            '(?, ?, ?, ?, ?, ?, ?, ?);'
            else:
                query_str = 'INSERT INTO ice_test_results ("testType", ' +\
                    '"testFeature", "testResult", "testName", notes,'\
                            'create_time, build_id, duration) VALUES ' +\
                            '(%s, %s, %s, %s, %s, %s, %s, %s);'
            cur.execute(query_str, (testType, testFeature, testResult,
                                    testName, notes,
                                    str(datetime.now()),
                                    settings.ICE_BUILD_REPORT_NUM,
                                    testDuration))
            dbConn.commit()
            logger.debug("Test result in DB - " + testResult)
        except Exception as e:
            logger.error(e)
            errorMsg = "Failed to insert results to DB." + str(e)
            raise Exception(errorMsg)
        dbConn.close()

    @staticmethod
    def select_query(queryStr, return_type="str", fetch_num=1):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            logger.debug("Query: " + queryStr)
            cur.execute(queryStr)
            if return_type == "str":
                if fetch_num == 1:
                    result = str(cur.fetchone())
                else:
                    result = str(cur.fetchall())
                if result != 'None':
                    # formatting strings e.g uuid
                    if(result.find("',)") != -1):
                        result = result.partition('\'')[-1].rpartition('\'')[0]
                    elif(result.find(",)") != -1):  # formatting ints e.g id
                        result = result.partition('(')[-1].rpartition(',')[0]
            if return_type == "list":
                if fetch_num == 1:
                    result = list(cur.fetchone())
                else:
                    result = [item[0] for item in cur.fetchall()]
            dbConn.close()
            logger.debug("Query result: " + str(result))
            return result
        except BaseException:
            raise Exception("Couldn't fetch answer using the given query.")

    @staticmethod
    def insert_query(queryStr):
        try:
            nativeIceDb = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = nativeIceDb
            cur = dbConn.cursor()
            logger.debug("Query: " + queryStr)
            cur.execute(queryStr)
            dbConn.commit()
            dbConn.close()
            logger.debug("Insert query success!")
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            logger.error(e)
            transaction.rollback()
            raise Exception("Couldn't fetch answer using the given query.")

    @staticmethod
    def update_query(queryStr):
        try:
            nativeIceDb = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = nativeIceDb
            cur = dbConn.cursor()
            logger.debug("Query: " + queryStr)
            cur.execute(queryStr)
            dbConn.commit()
            dbConn.close()
            logger.debug("Update query success!")
        # If failed - count the failure and add the error to list of errors.
        except Exception as e:
            logger.error(e)
            transaction.rollback()
            raise Exception("Couldn't fetch answer using the given query.")

    @staticmethod
    def select_where_email(queryColumnName, queryTableName, email):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "select %s from %s WHERE Email = '%s';" % (
                queryColumnName, queryTableName, email)
            logger.debug("Query : " + queryStr)
            cur.execute(queryStr)
            result = str(cur.fetchone())
            if(result.find("',)") != -1):  # formatting strings e.g uuid
                result = result.partition('\'')[-1].rpartition('\'')[0]
            elif(result.find(",)") != -1):  # formatting ints e.g id
                result = result.partition('(')[-1].rpartition(',')[0]
            dbConn.close()
            logger.debug("Query result: " + str(result))
            return result
        # If failed - count the failure and add the error to list of errors.
        except BaseException:
            errorMsg = "select_where_email FAILED "
            raise Exception(errorMsg, "select_where_email")
            raise

    @staticmethod
    def select_from(queryColumnName, queryTableName, fetchNum):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            cur = dbConn.cursor()
            queryStr = "select %s from %s;" % (queryColumnName, queryTableName)
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
        except Exception as e:
            errorMsg = "select_from FAILED " + str(e)
            raise Exception(errorMsg, "select_from")

    @staticmethod
    def select_where(
            queryColumnName,
            queryTableName,
            whereParametrType,
            whereParametrValue,
            fetchNum):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            cur = dbConn.cursor()
            queryStr = "select %s from %s Where %s = '%s';" % (
                queryColumnName, queryTableName, whereParametrType,
                whereParametrValue)
            logger.debug("Query : " + queryStr)
            cur.execute(queryStr)
            if (fetchNum == 0):
                result = list(cur.fetchall())
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
        except BaseException:
            errorMsg = "select_where FAILED "
            raise Exception(errorMsg, "select_where")

    @staticmethod
    def select_where_order_by_desc(
            queryColumnName,
            queryTableName,
            whereParametrType,
            whereParametrValue,
            order_by):
        dbConn = psycopg2.connect(
            DBGeneral.return_db_native_connection('em_db'))
        cur = dbConn.cursor()
        queryStr = \
            "select %s from %s " % (queryColumnName, queryTableName,) +\
            "Where %s = '%s' " % (whereParametrType, whereParametrValue) +\
            "order by %s desc limit 1;" % order_by
        logger.debug("Query : " + queryStr)
        cur.execute(queryStr)
        result = str(cur.fetchall())
        result = DBGeneral.list_format(result)
        dbConn.close()
        return result

    @staticmethod
    def select_where_dict(queryColumnName, queryTableName, whereParametrType):
        dbConn = psycopg2.connect(
            DBGeneral.return_db_native_connection('em_db'))
        cur = dbConn.cursor()
        x = ""
        count = 0
        for key, val in whereParametrType.items():
            x += "%s='%s'" % (key, val)
            if len(whereParametrType.items()) - count > 1:
                x += ' and '
                count += 1
        queryStr = "select %s from %s Where %s;" \
            % (queryColumnName, queryTableName, x)
        logger.debug("Query : " + queryStr)
        cur.execute(queryStr)
        result = str(cur.fetchall())
        result = DBGeneral.list_format(result)
        dbConn.close()
        return result

    @staticmethod
    def select_where_not_and_order_by_desc(
            queryColumnName,
            queryTableName,
            whereParametrType,
            whereParametrValue,
            parametrTypeAnd,
            parametrAnd,
            order_by):
        dbConn = psycopg2.connect(
            DBGeneral.return_db_native_connection('em_db'))
        cur = dbConn.cursor()
        queryStr = \
            "select %s from %s " % (queryColumnName, queryTableName) +\
            "Where %s = '%s' " % (whereParametrType, whereParametrValue) +\
            "and %s != '%s' " % (parametrTypeAnd, parametrAnd) +\
            "order by %s desc limit 1;" % order_by
        logger.debug("Query : " + queryStr)
        cur.execute(queryStr)
        result = str(cur.fetchall())
        result = DBGeneral.list_format(result)
        dbConn.close()
        return result

    @staticmethod
    def select_where_and(
            queryColumnName,
            queryTableName,
            whereParametrType,
            whereParametrValue,
            parametrTypeAnd,
            parametrAnd,
            fetchNum):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "select %s from %s Where %s = '%s' and %s = '%s';" % (
                queryColumnName, queryTableName, whereParametrType,
                whereParametrValue, parametrTypeAnd, parametrAnd)
            logger.debug("Query : " + queryStr)
            cur.execute(queryStr)
            if (fetchNum == 0):
                result = str(cur.fetchall())
                result = DBGeneral.list_format(result)
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
        except BaseException:
            errorMsg = "select_where_and FAILED "
            raise Exception(errorMsg, "select_where_and")

    @staticmethod
    def select_where_is_bigger(
            queryColumnName,
            queryTableName,
            whereParametrType,
            whereParametrValue,
            parametrTypeAnd,
            parametrAnd,
            fetchNum):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "select %s from %s Where %s = '%s' and %s > %s;" % (
                queryColumnName, queryTableName, whereParametrType,
                whereParametrValue, parametrTypeAnd, parametrAnd)
            logger.debug("Query : " + queryStr)
            cur.execute(queryStr)
            if (fetchNum == 0):
                result = cur.fetchall()
            elif (fetchNum == 1):
                result = cur.fetchone()
                if(result.find("',)") != -1):  # formatting strings e.g uuid
                    result = result.partition('\'')[-1].rpartition('\'')[0]
                elif(result.find(",)") != -1):  # formatting ints e.g id
                    result = result.partition('(')[-1].rpartition(',')[0]
            dbConn.close()
            return result
        # If failed - count the failure and add the error to list of errors.
        except BaseException:
            errorMsg = "select_where_is_bigger FAILED "
            raise Exception(errorMsg, "select_where_is_bigger")

    @staticmethod
    def update_where(
            queryTableName,
            setParametrType,
            setparametrValue,
            whereParametrType,
            whereParametrValue):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "UPDATE %s SET %s  = '%s' Where  %s = '%s';" % (
                queryTableName, setParametrType, setparametrValue,
                whereParametrType, whereParametrValue)
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
    def update_by_query(queryStr):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            logger.debug("Query : " + queryStr)
            cur.execute(queryStr)
            dbConn.commit()
            dbConn.close()
        # If failed - count the failure and add the error to list of errors.
        except BaseException:
            errorMsg = "Could not Update User"
            raise Exception(errorMsg, "Update")

    @staticmethod
    def update_where_and(
            queryTableName,
            setParametrType,
            parametrValue,
            changeToValue,
            whereParametrType,
            setParametrType2,
            setParametrValue2,
            whereParametrType2,
            whereParametrValue2):
        try:
            dbConn = psycopg2.connect(
                DBGeneral.return_db_native_connection('em_db'))
            dbConn = dbConn
            cur = dbConn.cursor()
            queryStr = "UPDATE %s SET " % queryTableName +\
                "%s  = '%s', " % (setParametrType, changeToValue) +\
                "%s  = '%s' Where  " % (setParametrType2, setParametrValue2) +\
                "%s = '%s' " % (whereParametrType, parametrValue) +\
                "and %s = '%s';" % (whereParametrType2, whereParametrValue2)
            logger.debug("Query : " + queryStr)
            cur.execute(queryStr)
            dbConn.commit()
            dbConn.close()
        # If failed - count the failure and add the error to list of errors.
        except BaseException:
            errorMsg = "Could not Update User"
            raise Exception(errorMsg, "Update")

    @staticmethod
    def list_format(un_listed):
        un_listed = un_listed[1:-1]
        un_listed = un_listed.replace("',), ('", "|||")
        un_listed = un_listed.replace("(u'", "")  # Format list
        un_listed = un_listed[1:-1].replace("('", "")  # Format list
        un_listed = un_listed.replace("',)", "")  # Format list
        listed = un_listed[1:-2].split("|||")
        return listed

    @staticmethod
    def get_vendors_list():
        # Select approved vendors from db.
        vendors_list = DBGeneral.select_where(
            "name", "ice_vendor", "public", "TRUE", 0)
        return vendors_list
