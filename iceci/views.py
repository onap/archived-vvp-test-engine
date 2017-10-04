 
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
import logging
from string import Template

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from iceci import mail
from iceci.mail import testsResults_mail_body
from services.constants import Constants
from services.logging_service import LoggingServiceFactory

from .models import TestResults
from .serializers import TestResultsModelSerializer


LAST_BUILD_REPORT_NUM = None
# from django.core.mail import send_mail
# from . import mail
logger = LoggingServiceFactory.get_logger()

def index(request):
    return HttpResponse("Hello, world. You're at the "+Constants.FEGeneral.ProgramName.name+" ci index.")

@csrf_exempt
def testResult_list(request):  # List all tests, or create a new test.
    if (request.method == 'DELETE' or request.method == 'PUT'):
        return HttpResponse(status=405)
    
    if request.method == 'GET':
        testResult = TestResults.objects.all()
        serializer = TestResultsModelSerializer(testResult, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TestResultsModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
@csrf_exempt
def testResultStr(request,param):  # List all tests, or create a new test.
    try:
        testResults = TestResults.objects.filter(build_id=param)
        pass_counter, total_counter, statisticData, fail_counter = strReportForTestResults(testResults)
        evaultaion = as_percentage_of(pass_counter, total_counter)
    except Exception as e:
        msg = "Something went wrong while trying to send Test Results "  + str(e)
        return HttpResponse(msg, status=500)

    msg = "Total Tests: " + str(total_counter) +" Pass Tests: " + str(pass_counter)+" Fail Tests: "+ str(fail_counter) + " Statistics : " + str(evaultaion) + " BUILD_REPORT_NUM : "+str(param)
    return HttpResponse(msg, status=200)

@csrf_exempt
def testResult_detail(request, param):  # Retrieve, update or delete a test.
    if request.method == 'POST':
        return HttpResponse(status=405)
    
    param = param.strip("/")
    
    try:
        testResult = TestResults.objects.get(name=param)
    except TestResults.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TestResultsModelSerializer(testResult)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TestResultsModelSerializer(testResult, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        testResult.delete()
        return HttpResponse(status=204)

#===============================================================================
# def testResult_post_action(request, data):
#     
#     logger.debug("about to send mail to " + data['email'])
#     
#     html_msg = mail.mail_body.substitute(data)
#     #send mail with template           
#     send_mail(mail.mail_subject, 
#               '', 
#               mail.mail_from,
#               mail.mail_to, 
#               fail_silently=False,
#               html_message=html_msg)
#===============================================================================
def createHtmlStrReportForTestResults(testResults):
    total_counter = 0
    fail_counter = 0
    pass_counter = 0
    statisticData = ""
    str2 = "<tr class='row1'>" + "<th class='field-testTotal'>@Total</th>" + "<td class='field-testPass'>@Pass</td>" + "<td class='field-tesFail'>@Fail</td>" + "<td class='field-testEvaultaion'>@Evaultaion</td>" + "</tr>"
    paramData = ""
    str3 = "<tr class='row2'>" + "<th class='field-testTotal'>@Version</th>" + "</tr>"
    allData = ""
    str = "<tr class='row1'>" + "<th class='field-testType'>@TestType</th>" + "<td class='field-testFeature'>@TestFeature</td>" + "<td class='field-testName'>@TestName</td>" + "<td class='field-testResult'>@TestResult</td>" + "<td class='field-notes'>@Notes</td>" + "<td class='field-create_time nowrap'>@Creation_time</td>" + "</tr>"
    for res in testResults: # testResults
        allData += str.replace("@TestType", str(res.testType)).replace("@TestFeature", str(res.testFeature)).replace("@TestName", str(res.testName)).replace("@TestResult", str(res.testResult)).replace("@Notes", str(res.notes)).replace("@Creation_time", str(res.create_time))
        total_counter += 1
        if (res.testResult == "PASS"):
            pass_counter += 1
        else:
            fail_counter += 1
    
    return pass_counter, total_counter, statisticData, str2, fail_counter, paramData, str3, allData

def strReportForTestResults(testResults):
    total_counter = 0
    fail_counter = 0
    pass_counter = 0
    statisticData = ""
    for res in testResults: # testResults
        total_counter += 1
        if (res.testResult == "PASS"):
            pass_counter += 1
        else:
            fail_counter += 1
    
    return pass_counter, total_counter, statisticData, fail_counter

@csrf_exempt
def testResult_list_to_mail(request,param):   # List all tests, or create a new test.
    if (request.method == 'DELETE' or request.method == 'PUT' or request.method == 'POST'):
        return HttpResponse(status=405)

    data = dict()

    print("BUILD_REPORT_NUM = "+settings.ICE_BUILD_REPORT_NUM)

    testResults = TestResults.objects.filter(build_id=param)

    pass_counter, total_counter, statisticData, str2, fail_counter, paramData, str3, allData = createHtmlStrReportForTestResults(testResults)
    
    evaultaion = as_percentage_of(pass_counter, total_counter)
    statisticData += str2.replace("@Total", str(total_counter)).replace("@Pass", str(pass_counter)).replace("@Fail", str(fail_counter)).replace("@Evaultaion", str(evaultaion))
    paramData += str3.replace("@Version", str(param))
    data['email'] = "rgafiulin@interwise.com"
    data['allData'] = str(allData) 
    data['statisticData'] = str(statisticData) 
    data['paramData'] = str(paramData)
    
    mail.testsResults_mail_to = data['email']
    try:
        mail.sendMail(param,data['email'], data, mail.testsResults_mail_body, mail.testsResults_mail_subject) 
    except Exception as e:
        msg = "Something went wrong while trying to send Test Report mail to " + data['email'] + str(e)
        return HttpResponse(msg, status=500)

    serializer = TestResultsModelSerializer(testResults, many=True)
    return JSONResponse(serializer.data)

@csrf_exempt
def testResult_list_to_html_file(request,param):
    if (request.method == 'DELETE' or request.method == 'PUT' or request.method == 'POST'):
        return HttpResponse(status=405)

    data = dict()

    print("BUILD_REPORT_NUM = "+settings.ICE_BUILD_REPORT_NUM)

    testResults = TestResults.objects.filter(build_id=settings.ICE_BUILD_REPORT_NUM)

    pass_counter, total_counter, statisticData, str2, fail_counter, paramData, str3, allData = createHtmlStrReportForTestResults(testResults)
    
    evaultaion = as_percentage_of(pass_counter, total_counter)
    statisticData += str2.replace("@Total", str(total_counter)).replace("@Pass", str(pass_counter)).replace("@Fail", str(fail_counter)).replace("@Evaultaion", str(evaultaion))
    paramData += str3.replace("@Version", str(param))

    data['allData'] = str(allData) 
    data['statisticData'] = str(statisticData) 
    data['paramData'] = str(paramData)
    
    html_msg = testsResults_mail_body.substitute(data)
    fileName = settings.LOGS_PATH+"Test_Results_"+settings.ICE_BUILD_REPORT_NUM+".html"
    try:
        with open(fileName, "w") as text_file:
            text_file.write(html_msg)
    except Exception as e:
        msg = "Something went wrong while trying to write the tet results to html file " +fileName +" "+ str(e)
        return HttpResponse(msg, status=500)

    serializer = TestResultsModelSerializer(testResults, many=True)
    return JSONResponse(serializer.data)

def as_percentage_of(part, whole):
    try:
        return "%d%%" % (float(part) / whole * 100)
    except (ValueError, ZeroDivisionError):
        return "" 

class JSONResponse(HttpResponse):  # An HttpResponse that renders its content into JSON.
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
