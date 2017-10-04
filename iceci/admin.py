 
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
from django.contrib import admin
from .models import TestResults
from django.conf import settings


def export_csv(modeladmin, request, queryset):
    import csv
#     import xlwt
    from django.utils.encoding import smart_str
    from django.http import HttpResponse
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=ci_Test_Results.csv'
    writer = csv.writer(response, csv.excel)
    # BOM (optional...Excel needs it to open UTF-8 file properly)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"testType"),
        smart_str(u"testFeature"),
        smart_str(u"testName"),
        smart_str(u"testResult"),
        smart_str(u"notes"),
        smart_str(u"duration"),
        smart_str(u"build_id"),
        smart_str(u"create_time"),
    ])

    total_counter = 0
    fail_counter = 0
    pass_counter = 0
    for obj in queryset:
        total_counter += 1
        if obj.testResult == 'FAIL':
            fail_counter += 1
        elif obj.testResult == 'PASS':
            pass_counter += 1

        writer.writerow([
            smart_str(obj.testType),
            smart_str(obj.testFeature),
            smart_str(obj.testName),
            smart_str(obj.testResult),
            smart_str(obj.notes),
            smart_str(obj.duration),
            smart_str(obj.build_id),
            smart_str(obj.create_time),
        ])
    # calsl evaluation
    evaultaion = as_percentage_of(pass_counter, total_counter)
    # title
    writer.writerow([
        smart_str(u"total_counter"),
        smart_str(u"fail_counter"),
        smart_str(u"pass_counter"),
        smart_str(u"evaultaion"),
    ])
    # values
    writer.writerow([
        smart_str(total_counter),
        smart_str(fail_counter),
        smart_str(pass_counter),
        smart_str(evaultaion),
    ])

    return response
# export_csv.short_description = u"Export CSV"  ### Check this action meaning.


def as_percentage_of(part, whole):
    try:
        return "%d%%" % (float(part) / whole * 100)
    except (ValueError, ZeroDivisionError):
        return ""


@admin.register(TestResults)
class TestResultsModelAdmin(admin.ModelAdmin):

    list_display = ["testType", "testFeature", "testName",
                    "testResult", "notes", "duration", "build_id", "create_time"]
    list_filter = ["testResult", "testType", "testFeature",
                   "testName", "notes", "duration", "build_id", "create_time"]
    search_fields = ["testResult", "testType", "testFeature", "testName",
                     "notes", "duration", "build_id", "create_time"]
    actions = [export_csv]
    list_per_page = settings.NUMBER_OF_TEST_RESULTS
