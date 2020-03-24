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
- ``/preloads`` should contain a preload file for each VNF module.
  - For a VNF-API preload: vnf-name, vnf-type, generic-vnf-type, and generic-vnf-name should be empty strings.
  - For a GR-API preload: vnf-name, vnf-type, vf-module-type, and vf-module-name should be empty strings.
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
     "api_type": "[gr_api] or [vnf_api]", 
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


```
(stark_env3) CAML01SS820F:ovp_testsuite stark$ ./instantiate-k8s.sh --folder /tmp/test-engine/ovp_testsuite/examples/vLB/ --namespace onap
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


## Examples


In this repository is an example that you can use to try out the testcase, located in the ``examples`` directory. It uses the vLB Heat Templates that are used in various other ONAP use-cases.

