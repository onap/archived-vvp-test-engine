# VNF Lifecycle Validation (OVP Badging)


## About


This page contains instructions for executing the [VNF Lifecycle Validation](https://wiki.lfnetworking.org/display/LN/VNF+Validation+Minimum+Viable+Product) automation flow for **heat-based** VNFs. The result will be a ``.tar.gz`` file that can be used to submit to the [OVP Portal](https://vnf-verified.lfnetworking.org/#/) to obtain a certification badge for a VNF. The execution is very similar to [running the other ONAP demo VNFs](https://wiki.onap.org/display/DW/Running+the+ONAP+Demos), however there are some additional steps detailed below. 

The OVP VNF testsuite was introduced in the ONAP El Alto release, and used the existing ONAP Robot pod and framework. The code in this repository was introduced in Frankfurt. It will most likely work on ONAP El Alto deployments, however it's recommended to continue to use the original OVP testsuite for El Alto, and use the testsuite here for Frankfurt and beyond.   


## Changes from El Alto Original Release


The testsuite operates the same as in El Alto, but there are a few changes you may need to be aware of before proceeding.
 

- VNF_API is no longer supported. You **MUST** use GR_API.
- The ``subscriber`` field in ``vnf-details.json`` has been replaced with ``customer``. If you are planning to re-use a ``vnf-details.json`` file from El Alto, you need to update that field.
- ONAP Robot pod and framework no longer used.
- ``log.html`` is now ``log.txt``


## Prerequisites


- [ONAP deployed via OOM](https://onap.readthedocs.io/en/latest/submodules/oom.git/docs/oom_quickstart_guide.html).
- An OpenStack deployment.
- kubectl
- bash
- VNF Heat Templates
- Preload json files


After deploying ONAP, you need to configure ONAP with:

- A cloud owner
- A cloud region
- A customer
- A service type
- A project name
- An owning entity
- A platform
- A line of business
- A cloud site


If you're not familiar with how to configure ONAP, there are guides that use [robot](https://onap.readthedocs.io/en/latest/submodules/integration.git/docs/docs_robot.html) or [direct api requests](https://wiki.onap.org/pages/viewpage.action?pageId=25431491) available to help, as well as a [guide for adding a new OpenStack site to ONAP](https://docs.onap.org/en/latest/guides/onap-user/cloud_site/openstack/index.html). 


## Preparing the VNF


The vnf lifecycle validation testsuite requires the VNF to be packaged into a specific directory hierarchy, shown below.

```
vnf_folder
├── /templates
|   └── base.yaml
|   └── base.env
|   └── incremental_0.yaml
|   └── incremental_0.env
|   └── ...
├── /preloads
|   └── base_preload.json
|   └── incremental_0_preload.json
|   └── ...
└── vnf-details.json
```

- The name for ``vnf_folder`` is free-form, and can be located anywhere on your computer. The path to this folder will be passed to the testsuite as an argument.
- ``/templates`` should contain your [VVP-compliant](https://docs.onap.org/en/latest/submodules/vvp/documentation.git/docs/index.html) VNF heat templates.
- ``/preloads`` should contain a preload file for each VNF module in the format for GR_API.
  - ``vnf-name``, ``vnf-type``, ``vf-module-type``, and ``vf-module-name`` should be empty strings.
  - This information will be populated at runtime by the testsuite.
- ``vnf-details`` should be a json file with the information that will be used by ONAP to instantiate the VNF. The structure of vnf-details is shown below.


### Example VNF-Details


```
{
     "vnf_name": "The Vnf Name",
     "description": "Description of the VNF",
     "modules": [
        {
         "filename": "base.yaml",
         "isBase": "true",
         "preload": "base_preload.json"
        },
        {
         "filename": "incremental_0.yaml",
         "isBase": "false",
         "preload": "incremental_0.json"
        },
        ...
     ],
     "api_type": "gr_api", 
     "customer": "<customer name>",
     "service_type": "<service type>",
     "tenant_name": "<name of tenant>",
     "region_id": "<name of region>",
     "cloud_owner": "<name of cloud owner>",
     "project_name": "<name of project>",
     "owning_entity": "<name of owning entity>",
     "platform": "<name of platform>",
     "line_of_business": "<name of line of business>",
     "os_password": "<openstack password>"
}
```

- ``modules`` must contain an entry for each module of the VNF. Only one module can be a base module.
- ``api_type`` should match the format of the preloads that are provided in the package.
- The other information should match what was used to configure ONAP during the pre-requisite section of this guide.


## Running the Testsuite


The script ``instantiate-k8s.sh`` located in this repository is used to execute the testsuite.


**NOTE**: The first time running the testsuite on your K8 cluster will take longer than subsequent runs. The first execution creates a K8 pod and installs required software pre-requisites, which can take five minutes or more. Subsequent executions will re-use the same pod.


### Cloning and Navigating to the Testsuite


```
$ git clone "https://gerrit.onap.org/r/vvp/test-engine"
$ cd test-engine/ovp_testsuite
$ ./instantiate-k8s.sh --help
./instantiate-k8s.sh [options]
 
required:
-n, --namespace <namespace>       namespace that onap is running under.
-f, --folder <folder>             path to folder containing heat templates, preloads, and vnf-details.json.
 
This script executes the OVP VNF instantiation testsuite.
- It creates a container that will contain all of the installation requirements.
- It models, distributes, and instantiates a heat-based VNF.
- It copies the logs to an output directory, and creates a tarball for upload to the OVP portal.
```


### Executing the Testsuite


```
# Execute instantiate-k8s.sh to start the testsuite
$ ./instantiate-k8s.sh --folder /tmp/test-engine/ovp_testsuite/examples/vLB/ --namespace onap
+ check_required_parameter onap --namespace
+ '[' -z onap ']'
+ check_required_parameter /tmp/test-engine/ovp_testsuite/examples/vLB/ --folder
+ '[' -z /tmp/test-engine/ovp_testsuite/examples/vLB/ ']'
+ '[' -z /tmp/VVPQ69g/kubeconfig ']'
+ kubectl -n onap get configmap ovp-test-suite-vol
NAME                 DATA   AGE
ovp-test-suite-vol   1      5d20h
+ '[' 0 -ne 0 ']'
+ kubectl -n onap get pod ovp-test
NAME       READY   STATUS    RESTARTS   AGE
ovp-test   1/1     Running   0          5d20h
+ '[' 0 -ne 0 ']'
+ mkdir /tmp/OVP-b3nx
+ echo ''

+ echo 'Your output directory is /tmp/OVP-b3nx, look here for logs after the test has finished.'
Your output directory is /tmp/OVP-b3nx, look here for logs after the test has finished.
...
...
...
================================================================
OVP Test Case has finished, generating output in /tmp/OVP-b3nx.

--------------------Results--------------------
Test Start Time:                    1585069559
VVP Validation Scripts:             SUCCESS
ONAP Modeling and Instantiation:    SUCCESS
Stack Validation:                   SUCCESS

...
...
```


## Results


Once the testsuite is finished, it will create a directory and tarball in /tmp (the name of the directory and file is shown at the end of the stdout of the script). There will be a ``results.json`` in that directory that has the ultimate outcome of the test, in the structure shown below.


## Log files


The output file will have 4 log files in it.

``results.json``: This is high-level results file of all of the test steps, and is consumed by the OVP portal.
``report.json``: This is the output of the vvp validation scripts.
``stack_report.json``: This is the output from querying openstack to validate the heat modules.
``log.txt``: This stdout log, and contains each execution step of the testcase.


### results.json

```
{
    "vnf_checksum": "a3e66ab6790f40947d7888a45fb5552b6966553c6172538b88accea5bf330a52",
    "build_tag": "eeb98797-722f-423c-bb91-7ff4d2e4d04e",
    "version": "2019.12",
    "test_date": "2020-03-24 10:31:57",
    "duration": 1563,
    "vnf_type": "heat",
    "testcases_list": [
        {
            "mandatory": "true",
            "name": "onap-vvp.validate.heat",
            "result": "SUCCESS",
            "objective": "onap heat template validation",
            "sub_testcase": [],
            "portal_key_file": "report.json"
        },
        {
            "mandatory": "true",
            "name": "onap-vvp.lifecycle_validate.heat",
            "result": "SUCCESS",
            "objective": "onap vnf lifecycle validation",
            "sub_testcase": [
                {
                    "name": "model-and-distribute",
                    "result": "SUCCESS"
                },
                {
                    "name": "instantiation",
                    "result": "SUCCESS"
                }
            ],
            "portal_key_file": "log.txt"
        },
        {
            "mandatory": "true",
            "name": "stack_validation",
            "result": "SUCCESS",
            "objective": "onap vnf openstack validation",
            "sub_testcase": [],
            "portal_key_file": "stack-validation.json"
        }
    ]
}
```


## Cleaning Up The Testsuite


After executing the testsuite, you'll (hopefully) have an instantiated VNF. If you want to delete it, you can use VID BAU to login and delete the Service, VNF, and Module instance(s).

Alternatively, you can use kubectl to login to the OVP pod that was created and delete all the VNF components from the cli. Here's how:

First, you need to figure out the Service instance and VNF instance names that were created. These follow the naming convention ``SI<build_string>`` and ``SI_VNF<build_string>``. Your build string is used to create the output directory at the end of the testsuite. In the example above, the output directory was ``/tmp/OVP-b3nx``, so the build string is ``b3nx``.

Next, you need to figure out each of your module names. These are the same as the heat stack names, but if you don't want to log into openstack to find them, they also follow a naming convention using the build_string: ``SI_VNF_<build_string>_<filename without extension>``. So from the example above, the module names would be: ``SI_VNF_b3nx_base_template``, ``SI_VNF_b3nx_vdns``, ``SI_VNF_b3nx_vpkg``, ``SI_VNF_b3nx_vlb``.

Next, login to the OVP pod and start deleting them, starting with modules first, then VNF instance, then Service Instance. **Make sure that you delete all the other modules before deleting the base module**.

```
# login to the OVP pod
$ kubectl -n onap exec -it ovp-test bash
bash-5.0#

# Activate the virtualenv with the installed pre-reqs
bash-5.0# . /tmp/vvp_env/test_env/bin/activate
(test_env) bash-5.0# 

# Look at the syntax to delete a VNF Module Instance
(test_env) bash-5.0# onap-client utility delete-module-instance --help
+------------------------+----------------------------------+-------------------------+
| name                   | description                      | parameters              |
+------------------------+----------------------------------+-------------------------+
| --help                 |                                  |                         |
|                        |                                  |                         |
| delete-module-instance | Delete a Module Instance from SO | <service_instance_name> |
|                        |                                  | <vnf_instance_name>     |
|                        |                                  | <module_instance_name>  |
|                        |                                  | <api_type>              |
|                        |                                  |                         |
+------------------------+----------------------------------+-------------------------+

(test_env) bash-5.0# onap-client utility delete-module-instance SIb3nx SI_VNFb3nx SI_VNF_b3nx_vlb GR_API
2020-03-24 18:41:40,629 {
    "method": "GET",
    "auth": "***********",
    "url": "https://sdnc:8443/restconf/config/GENERIC-RESOURCE-API:services",
    "headers": {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-TransactionId": "bffbee67-6071-4bb0-9b42-c54c630c51bd",
        "X-FromAppId": "robot-ete"
    }
}
2020-03-24 18:41:40,629 Submitting request: Get a list of all service instances
/usr/local/lib/python3.7/site-packages/urllib3/connectionpool.py:1004: InsecureRequestWarning: Unverified HTTPS request is being made to host 'sdnc'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecureRequestWarning,
2020-03-24 18:41:40,913 Request was successful
2020-03-24 18:41:40,920 {
    "method": "DELETE",
    "auth": "***********",
    "url": "http://so:8080/onap/so/infra/serviceInstantiation/v7/serviceInstances/83f6b4b9-bf5d-4176-a931-a4a0e89d869b/vnfs/8cf4782e-24b6-462e-aac0-edf879444768/vfModules/34cfac51-862a-4455-9d0b-de775c66179d",
    "headers": {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-FromAppId": "robot-ete"
    },
    "data": " {\n  \"requestDetails\": {\n    \"requestInfo\": {\n      \"source\": \"VID\",\n      \"requestorId\": \"cs0008\"\n    },\n    \"modelInfo\": {\n      \"modelType\": \"vfModule\",\n      \"modelInvariantId\": \"633d369c-5557-4690-a920-cffe60b0808d\",\n      \"modelName\": \"Vnfb3nx..vlb..module-2\",\n      \"modelVersion\": \"1\"\n    },\n    \"requestParameters\": {\n      \"testApi\": \"GR_API\"\n    },\n    \"cloudConfiguration\": {\n      \"lcpCloudRegionId\": \"ONAPREGION\",\n      \"tenantId\": \"f9daf5a9a50747429ee786ee9c2b41b3\",\n      \"cloudOwner\": \"ONAPOWNER\"\n    }\n  }\n }"
}
2020-03-24 18:41:40,920 Submitting request: Deletes a VNF Module Instance.
2020-03-24 18:41:42,421 Request was successful
{
    "requestReferences": {
        "requestId": "52944b25-6b82-4954-ba26-40f52a51c65a",
        "instanceId": "34cfac51-862a-4455-9d0b-de775c66179d",
        "requestSelfLink": "http://so:8080/orchestrationRequests/v7/52944b25-6b82-4954-ba26-40f52a51c65a"
    }
}
``` 


**NOTE**: When you send a delete request, it will return a ``requestId``. The ``requestId`` from above is ``52944b25-6b82-4954-ba26-40f52a51c65a``. Use this request ID to poll until the request finishes.


``` 
(test_env) bash-5.0# onap-client utility poll-request 52944b25-6b82-4954-ba26-40f52a51c65a
2020-03-24 18:43:48,174 {
    "method": "GET",
    "auth": "***********",
    "url": "http://so:8080/onap/so/infra/orchestrationRequests/v7/52944b25-6b82-4954-ba26-40f52a51c65a",
    "headers": {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-TransactionId": "5027d330-b38c-4bef-9803-a3f0d5acb386",
        "X-FromAppId": "robot-ete"
    }
}
...
...
...
        "requestStatus": {
            "requestState": "COMPLETE",
            "statusMessage": "STATUS: ALaCarte-VfModule-deleteInstance request was executed correctly. FLOW STATUS: Successfully completed all Building Blocks",
            "percentProgress": 100,
            "timestamp": "Tue, 24 Mar 2020 18:47:18 GMT"
        },
...
...
(test_env) bash-5.0# 
```


Continue to delete each of the modules.


```
(test_env) bash-5.0# onap-client utility delete-module-instance SIb3nx SI_VNFb3nx SI_VNF_b3nx_vpkg GR_API
...
...
{
    "requestReferences": {
        "requestId": "5f16ed41-ef99-4a73-972e-2d8380646fc3",
        "instanceId": "16d9b141-fb31-4489-b39e-457fa3ae2a17",
        "requestSelfLink": "http://so:8080/orchestrationRequests/v7/5f16ed41-ef99-4a73-972e-2d8380646fc3"
    }
}
(test_env) bash-5.0# onap-client utility poll-request 5f16ed41-ef99-4a73-972e-2d8380646fc3
...
...
        "requestStatus": {
            "requestState": "COMPLETE",
            "statusMessage": "STATUS: ALaCarte-VfModule-deleteInstance request was executed correctly. FLOW STATUS: Successfully completed all Building Blocks",
            "percentProgress": 100,
            "timestamp": "Tue, 24 Mar 2020 18:48:50 GMT"
        },
...
...
(test_env) bash-5.0# onap-client utility delete-module-instance SIb3nx SI_VNFb3nx SI_VNF_b3nx_vdns GR_API
...
...
{
    "requestReferences": {
        "requestId": "3e3fa519-a93d-4b5a-bc5b-ba87aff361cf",
        "instanceId": "172dfaac-cbc1-4793-a487-dc3c21ce595b",
        "requestSelfLink": "http://so:8080/orchestrationRequests/v7/3e3fa519-a93d-4b5a-bc5b-ba87aff361cf"
    }
}
(test_env) bash-5.0# onap-client utility poll-request 3e3fa519-a93d-4b5a-bc5b-ba87aff361cf
...
...
        "requestStatus": {
            "requestState": "COMPLETE",
            "statusMessage": "STATUS: ALaCarte-VfModule-deleteInstance request was executed correctly. FLOW STATUS: Successfully completed all Building Blocks",
            "percentProgress": 100,
            "timestamp": "Tue, 24 Mar 2020 18:55:45 GMT"
        },
(test_env) bash-5.0# onap-client utility delete-module-instance SIb3nx SI_VNFb3nx SI_VNF_b3nx_base_template GR_API
...
...
{
    "requestReferences": {
        "requestId": "386cb6f5-019b-45a1-8813-ae80ab3324b9",
        "instanceId": "ef2dffb3-c41d-4072-8634-c7be73ef3caa",
        "requestSelfLink": "http://so:8080/orchestrationRequests/v7/386cb6f5-019b-45a1-8813-ae80ab3324b9"
    }
}
(test_env) bash-5.0# onap-client utility poll-request 386cb6f5-019b-45a1-8813-ae80ab3324b9
...
...
        "requestStatus": {
            "requestState": "COMPLETE",
            "statusMessage": "STATUS: ALaCarte-VfModule-deleteInstance request was executed correctly. FLOW STATUS: Successfully completed all Building Blocks",
            "percentProgress": 100,
            "timestamp": "Tue, 24 Mar 2020 19:08:06 GMT"
        },
```


Now, delete the VNF and Service instance.


```
# View syntax to delete VNF Instance
(test_env) bash-5.0# onap-client utility delete-vnf-instance --help
+---------------------+-------------------------------+-------------------------+
| name                | description                   | parameters              |
+---------------------+-------------------------------+-------------------------+
| --help              |                               |                         |
|                     |                               |                         |
| delete-vnf-instance | Delete a VNF Instance from SO | <service_instance_name> |
|                     |                               | <vnf_instance_name>     |
|                     |                               | <api_type>              |
|                     |                               |                         |
+---------------------+-------------------------------+-------------------------+

# Send delete vnf instance request
(test_env) bash-5.0# onap-client utility delete-vnf-instance SIb3nx SI_VNFb3nx GR_API
...
...
{
    "requestReferences": {
        "requestId": "618e02ce-be72-4722-950b-1d03754a1d2e",
        "instanceId": "8cf4782e-24b6-462e-aac0-edf879444768",
        "requestSelfLink": "http://so:8080/orchestrationRequests/v7/618e02ce-be72-4722-950b-1d03754a1d2e"
    }
}

(test_env) bash-5.0# onap-client utility poll-request 618e02ce-be72-4722-950b-1d03754a1d2e
...
...
        "requestStatus": {
            "requestState": "COMPLETE",
            "statusMessage": "STATUS: ALaCarte-Vnf-deleteInstance request was executed correctly. FLOW STATUS: Successfully completed all Building Blocks",
            "percentProgress": 100,
            "timestamp": "Tue, 24 Mar 2020 19:15:22 GMT"
        },

# View syntax to delete Service instance
(test_env) bash-5.0# onap-client utility delete-service-instance --help
+-------------------------+-----------------------------------+-------------------------+
| name                    | description                       | parameters              |
+-------------------------+-----------------------------------+-------------------------+
| --help                  |                                   |                         |
|                         |                                   |                         |
| delete-service-instance | Delete a Service Instance from SO | <service_instance_name> |
|                         |                                   | <api_type>              |
|                         |                                   |                         |
+-------------------------+-----------------------------------+-------------------------+

# Send request to delete service instance
(test_env) bash-5.0# onap-client utility delete-service-instance SIb3nx GR_API
...
...
    "requestReferences": {
        "requestId": "ee8dc971-66ed-4520-81d1-a6fedd7e0a57",
        "instanceId": "83f6b4b9-bf5d-4176-a931-a4a0e89d869b",
        "requestSelfLink": "http://so:8080/orchestrationRequests/v7/ee8dc971-66ed-4520-81d1-a6fedd7e0a57"
    }

(test_env) bash-5.0# onap-client utility poll-request ee8dc971-66ed-4520-81d1-a6fedd7e0a57
...
...
        "requestStatus": {
            "requestState": "COMPLETE",
            "statusMessage": "STATUS: ALaCarte-Service-deleteInstance request was executed correctly. FLOW STATUS: Successfully completed all Building Blocks",
            "percentProgress": 100,
            "timestamp": "Tue, 24 Mar 2020 19:22:07 GMT"
        },
```

## Examples


In this repository is an example that you can use to try out the testcase, located in the ``examples`` directory. It uses the vLB Heat Templates that are used in various other ONAP use-cases.

