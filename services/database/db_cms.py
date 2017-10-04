 
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
import psycopg2
from wheel.signatures import assertTrue

from services.constants import Constants
from services.database.db_general import DBGeneral
from services.frontend.base_actions.click import Click
from services.frontend.base_actions.enter import Enter
from services.frontend.base_actions.wait import Wait
from services.frontend.fe_dashboard import FEDashboard
from services.frontend.fe_general import FEGeneral
from services.frontend.fe_user import FEUser
from services.helper import Helper
from services.logging_service import LoggingServiceFactory
from services.session import session


logger = LoggingServiceFactory.get_logger()


class DBCMS:

    @staticmethod
    def insert_query(queryStr):
        try:
            nativeIceDb = psycopg2.connect(
                DBGeneral.return_db_native_connection('cms_db'))
            dbConn = nativeIceDb
            cur = dbConn.cursor()
            logger.debug("Query: " + queryStr)
            cur.execute(queryStr)
            dbConn.commit()
            dbConn.close()
            logger.debug("Insert query success!")
        # If failed - count the failure and add the error to list of errors.
        except:
            raise Exception("Couldn't fetch answer using the given query.")

    @staticmethod
    def update_query(queryStr):
        try:
            nativeIceDb = psycopg2.connect(
                DBGeneral.return_db_native_connection('cms_db'))
            dbConn = nativeIceDb
            cur = dbConn.cursor()
            logger.debug("Query: " + queryStr)
            cur.execute(queryStr)
            dbConn.commit()
            dbConn.close()
            logger.debug("Update query success!")
        # If failed - count the failure and add the error to list of errors.
        except:
            raise Exception("Couldn't fetch answer using the given query.")

    @staticmethod
    def select_query(queryStr):
        try:
            nativeIceDb = psycopg2.connect(
                DBGeneral.return_db_native_connection('cms_db'))
            dbConn = nativeIceDb
            cur = dbConn.cursor()
            logger.debug("Query: " + queryStr)
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
        except:
            raise Exception("Couldn't fetch answer using the given query.")

    @staticmethod
    def get_cms_category_id(categoryName):
        logger.debug("Get DBCMS category id for name: " + categoryName)
        queryStr = "SELECT id FROM public.blog_blogcategory WHERE title = '%s' LIMIT 1;" % (
            categoryName)
        logger.debug("Query : " + queryStr)
        result = DBCMS.select_query(queryStr)
        return result

    @staticmethod
    def insert_cms_new_post(title, description, categoryName):
        logger.debug("Insert new post : " + title)
        queryStr = "INSERT INTO public.blog_blogpost" \
            "(comments_count, keywords_string, rating_count, rating_sum, rating_average, title, slug, _meta_title, description, gen_description, created, updated, status, publish_date, expiry_date, short_url, in_sitemap, content, allow_comments, featured_image, site_id, user_id) "\
            "VALUES (0, '', 0, 0, 0, '%s', '%s-slug', '', '%s', true, current_timestamp - interval '1 day', current_timestamp - interval '2 day', 2, current_timestamp - interval '1 day', NULL, '', true, '<p>%s</p>', true, '', 1, 1);" % (
                title, title, description, description)
        logger.debug("Query : " + queryStr)
        DBCMS.insert_query(queryStr)
        post_id = DBCMS.get_last_added_post_id()
        categoryId = DBCMS.get_cms_category_id(categoryName)
        DBCMS.add_category_to_post(post_id, categoryId)
        return post_id

    @staticmethod
    def get_last_added_post_id():
        logger.debug("Get the id of the post inserted")
        queryStr = "select MAX(id) FROM public.blog_blogpost;"
        logger.debug("Query : " + queryStr)
        result = DBCMS.select_query(queryStr)
        return result

    @staticmethod
    def update_days(xdays, title):
        logger.debug("Get the id of the post inserted")
#         queryStr = "select MAX(id) FROM public.blog_blogpost;"
        queryStr = "UPDATE public.blog_blogpost SET created=current_timestamp - interval '%s day' WHERE title='%s';" % (
            xdays, title)
        logger.debug("Query : " + queryStr)
        result = DBCMS.update_query(queryStr)
        return result

    @staticmethod
    def add_category_to_post(postId, categoryId):
        logger.debug("bind category into inserted post: " + postId)
        queryStr = "INSERT INTO public.blog_blogpost_categories(blogpost_id, blogcategory_id) VALUES (%s, %s);" % (
            postId, categoryId)
        logger.debug("Query : " + queryStr)
        DBCMS.insert_query(queryStr)

    @staticmethod
    def get_documentation_page_id():
        logger.debug("Retrive id of documentation page: ")
        queryStr = "SELECT id FROM public.pages_page WHERE title = 'Documentation' LIMIT 1;"
        logger.debug("Query : " + queryStr)
        result = DBCMS.select_query(queryStr)
        return result

    @staticmethod
    def get_last_inserted_page_id():
        logger.debug("Retrive id of last page inserted: ")
        queryStr = "select MAX(id) FROM public.pages_page;"
        logger.debug("Query : " + queryStr)
        result = DBCMS.select_query(queryStr)
        return result

    @staticmethod
    def delete_old_tips_of_the_day():
        logger.debug("Delete all posts ")
        queryStr = "DELETE FROM public.blog_blogpost_categories WHERE id>0;"
        logger.debug("Query : " + queryStr)
        DBCMS.insert_query(queryStr)
        queryStr = "DELETE FROM public.blog_blogpost WHERE id>0;;"
        logger.debug("Query : " + queryStr)
        DBCMS.insert_query(queryStr)

    @staticmethod
    def insert_page(title, content, parent_id=None):
        logger.debug("Retrive id of documentation page: ")
        if parent_id is None:
            parent_id = DBCMS.get_documentation_page_id()
        queryStr = "INSERT INTO public.pages_page(" \
            "keywords_string, title, slug, _meta_title, description, gen_description, created, updated, status, publish_date, expiry_date, short_url, in_sitemap, _order, in_menus, titles, content_model, login_required, parent_id, site_id)" \
            "VALUES ('', '%s', '%s-slug', '', '%s', true, current_timestamp - interval '1 day', current_timestamp - interval '1 day', 2, current_timestamp - interval '1 day', NULL, '', true, 0, '1,2,3', '%s', 'richtextpage', true, %s, 1);" % (
                title, title, content, title, parent_id)
        logger.debug("Query : " + queryStr)
        DBCMS.insert_query(queryStr)

        createdPageId = DBCMS.get_last_inserted_page_id()
        logger.debug(
            "Bind the page with the rich text content related to this page")
        queryStr = "INSERT INTO public.pages_richtextpage(page_ptr_id, content)    VALUES (%s, '<p>%s</p>');" % (
            createdPageId, content)
        logger.debug("Query : " + queryStr)
        DBCMS.insert_query(queryStr)
        return createdPageId

    @staticmethod
    def create_faq():
        title = "title_FAQ" + Helper.rand_string("randomString")
        description = "description_FAQ_" + Helper.rand_string("randomString")
        DBCMS.delete_old_tips_of_the_day()
        postId = DBCMS.insert_cms_new_post(title, description, "FAQ")
        assertTrue(len(postId) > 0 and not None)
        return title, description

    @staticmethod
    def create_news():
        title = "title_News" + Helper.rand_string("randomString")
        description = "description_News" + Helper.rand_string("randomString")
        postId = DBCMS.insert_cms_new_post(title, description, "News")
        assertTrue(len(postId) > 0 and not None)
        return title, description

    @staticmethod
    def create_announcement():
        title = "title_Announcement_" + Helper.rand_string("randomString")
        description = "description_Announcement_" + \
            Helper.rand_string("randomString")
        postId = DBCMS.insert_cms_new_post(title, description, "Announcement")
        assertTrue(len(postId) > 0 and not None)
        return title, description

    @staticmethod
    def create_page(parent_id=None):
        title = "title_Of_Page_" + Helper.rand_string("randomString")
        description = "description_Of_Page_" + \
            Helper.rand_string("randomString")
        createdPageId = DBCMS.insert_page(title, description)
        assertTrue(len(createdPageId) > 0 and not None)
        return title, description

    @staticmethod
    def update_X_days_back_post(title, xdays):
        logger.debug("Get the id of the post inserted")
        queryStr = "UPDATE blog_blogpost SET created = current_timestamp - interval '%s day', publish_date=current_timestamp - interval '%s day' WHERE title= '%s' ;" % (
            xdays, xdays, title)
        logger.debug("Query : " + queryStr)
        DBCMS.update_query(queryStr)

    @staticmethod
    def create_announcements(x):
        listOfTitleAnDescriptions = []
        for _ in range(x):
            #             print x ->str
            title = "title_Announcement_" + Helper.rand_string("randomString")
            description = "description_Announcement_" + \
                Helper.rand_string("randomString")
            postId = DBCMS.insert_cms_new_post(
                title, description, "Announcement")
            assertTrue(len(postId) > 0 and not None)
            xList = [title, description]
            listOfTitleAnDescriptions.append(xList)
        return listOfTitleAnDescriptions
