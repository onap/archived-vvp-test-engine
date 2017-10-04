 
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
##################################################################################################
'''
Created on Apr 20, 2016

@author: ya107f
'''
import socket
from string import Template
import traceback

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from services.constants import Constants
from services.logging_service import LoggingServiceFactory


admin_mail_from = settings.ICE_CONTACT_FROM_ADDRESS
# lastBuild = ""
param = "1"
logger = LoggingServiceFactory.get_logger()

def sendMail(param,email, data, mail_body, mail_subject, mail_from=admin_mail_from):
    logger.debug("about to send mail to " + email)
    
    try: 
#         lastBuild = param
        html_msg = mail_body.substitute(data)
        mail_subject = mail_subject.substitute(data)
        #send mail with template           
        send_mail(mail_subject, '', Constants.FEGeneral.ProgramName.name +"-CI Report Test Team <" + mail_from + ">",settings.ICE_CONTACT_EMAILS , fail_silently=False, html_message=html_msg)
        logger.debug("Looks like email delivery to "+email+" has succeeded")
    except Exception:
        traceback.print_exc()
        raise

##########################
# For Contact Request    #
##########################
lastBuild= param
dt = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
#envIP = str(socket.gethostbyname(socket.gethostname()))
envIP = str(socket.gethostname())
testsResults_mail_subject = Template("""CI Testing results """+ str(dt))
testsResults_mail_to = settings.ICE_CONTACT_EMAILS
testsResults_mail_body = Template("""
<html>
    <head>
        <title>CI Test Report</title>
        <meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
    </head>
    <body style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space; color: rgb(0, 0, 0); font-size: 14px; font-family: Calibri, sans-serif;">
        <a href="http://172.20.31.59:9090/">Jenkins Link for Build</a>
        <h3>Environment name : """+ settings.ICE_CI_ENVIRONMENT_NAME + """</h3> 
        <h3>Environment IP : """ + envIP + """</h3> 
        <h2>Tests summary</h2>
        
        <table id="versions" style="border:1px solid black">
            <tr>
                <th scope="col"  class="sortable column-testVersion"> 
                   <div class="text"><a href="#">Last Build Version</a></div>
                   <div class="clear"></div>
                </th>
            </tr>
            <tbody>
                $paramData
            </tbody>
        </table>
        
        <table id="statistics" style="border:1px solid black">
            <tr>
                <th scope="col"  class="sortable column-testTotal"> 
                   <div class="text"><a href="#">Total</a></div>
                   <div class="clear"></div>
                </th>
                <th scope="col"  class="sortable column-testPass">
                   <div class="text"><a href="#">Pass</a></div>
                   <div class="clear"></div>
                </th>
                <th scope="col"  class="sortable column-tesFail">
                   <div class="text"><a href="#">Fail</a></div>
                   <div class="clear"></div>
                </th>
                <th scope="col"  class="sortable column-testEvaultaion">
                   <div class="text"><a href="#">Successful</a></div>
                   <div class="clear"></div>
                </th>
            </tr>
            <tbody>
                $statisticData
            </tbody>
        </table>
            
        <table id="result_list" style="border:1px solid blue">
            <tr>
                <th scope="col"  class="sortable column-testType">
                   <div class="text"><a href="#">TestType</a></div>
                   <div class="clear"></div>
                </th>
                <th scope="col"  class="sortable column-testFeature">
                   <div class="text"><a href="#">TestFeature</a></div>
                   <div class="clear"></div>
                </th>
                <th scope="col"  class="sortable column-testName">
                   <div class="text"><a href="#">TestName</a></div>
                   <div class="clear"></div>
                </th>
                <th scope="col"  class="sortable column-testResult">
                   <div class="text"><a href="#">TestResult</a></div>
                   <div class="clear"></div>
                </th>
                <th scope="col"  class="sortable column-notes">
                   <div class="text"><a href="#">Notes</a></div>
                   <div class="clear"></div>
                </th>
                <th scope="col"  class="sortable column-duration">
                   <div class="text"><a href="#">Duration</a></div>
                   <div class="clear"></div>
                </th>
                <th scope="col"  class="sortable column-create_time">
                   <div class="text"><a href="#">Creation time</a></div>
                   <div class="clear"></div>
                </th>
            </tr>
            <tbody>
                $allData
            </tbody>
        </table>
        
    </body>
</html>

""")

