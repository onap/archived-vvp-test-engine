# ONAP-Client

## License

Copyright 2020 AT&T Intellectual Property. All rights reserved.

This file is licensed under the CREATIVE COMMONS ATTRIBUTION 4.0 INTERNATIONAL LICENSE

Full license text at https://creativecommons.org/licenses/by/4.0/legalcode

## About


ONAP Client is an api-client written in python for interacting with various ONAP applications. 

There are three interfaces for using the client.
- cli
- spec-engine
- programmatically

More details regarding usage is given below.


## Installation


Either use pip or setup.py to install.

```
$ cd /path/to/onap-client
$ pip install -r requirements.txt
$ pip install . --upgrade
```

### Config File


After installation, you need to create a configuration file for your ONAP installation. Use the file ``etc/config.example.yaml`` from this repo as a starter config file, and replace the values with those specific to your environment.

The config file needs to be located at ``/etc/onap_client/config.yaml``. If you don't have permissions to move it there, or you have multiple ONAP environments to interact with, you can also set the environment variable ``OC_CONFIG`` to the full-path of your config file.


```
$ export OC_CONFIG=/path/to/config.yaml
```


## Usage


### CLI


Use ``onap-client [options]`` to interact with the command-line client. The command-line options that are ONAP applications are created dynamically, and all follow the same pattern. Use ``--help`` to show more details about what options are available.

```
$ onap-client --help
+-------------+-------------------------------------------+---------------------+---------------------+
| name        | description                               | required parameters | optional parameters |
+-------------+-------------------------------------------+---------------------+---------------------+
| aai         | Various actions available for aai         | --help              |                     |
|             |                                           |                     |                     |
| sdc         | Various actions available for sdc         | --help              |                     |
|             |                                           |                     |                     |
| sdnc        | Various actions available for sdnc        | --help              |                     |
|             |                                           |                     |                     |
| so          | Various actions available for so          | --help              |                     |
|             |                                           |                     |                     |
| vid         | Various actions available for vid         | --help              |                     |
|             |                                           |                     |                     |
| spec-engine | Various actions available for spec-engine | --help              |                     |
|             |                                           |                     |                     |
| utility     | Various actions available for utility     | --help              |                     |
|             |                                           |                     |                     |
+-------------+-------------------------------------------+---------------------+---------------------+
```

To view all of the options available for SDC, use ``onap-client sdc --help``

```
$ onap-client sdc --help
+---------------+---------------------------------------------+---------------------+---------------------+
| name          | description                                 | required parameters | optional parameters |
+---------------+---------------------------------------------+---------------------+---------------------+
| health-check  | Queries SDC health check endpoint           |                     | --keys, --search    |
|               |                                             |                     |                     |
| license_model | Various actions available for license_model | --help              |                     |
|               |                                             |                     |                     |
| service       | Various actions available for service       | --help              |                     |
|               |                                             |                     |                     |
| vnf           | Various actions available for vnf           | --help              |                     |
|               |                                             |                     |                     |
| vsp           | Various actions available for vsp           | --help              |                     |
|               |                                             |                     |                     |
+---------------+---------------------------------------------+---------------------+---------------------+
```


From here, you can invoke the SDC health check, or view the other options available for SDC.


```
$ onap-client sdc license-model --help
+-------------------------------------+----------------------------------------------------------------------------------------+---------------------------------+---------------------+
| name                                | description                                                                            | required parameters             | optional parameters |
+-------------------------------------+----------------------------------------------------------------------------------------+---------------------------------+---------------------+
| add-license-model                   | creates a license model in the SDC catalog                                             | --vendor-name                   | --keys, --search    |
|                                     |                                                                                        |                                 |                     |
| add-key-group                       | Adds a key group to a license model                                                    | --license-start-date            | --keys, --search    |
|                                     |                                                                                        | --license-end-date              |                     |
|                                     |                                                                                        | --key-group-name                |                     |
|                                     |                                                                                        | --license-model-id              |                     |
|                                     |                                                                                        | --license-model-version-id      |                     |
|                                     |                                                                                        |                                 |                     |
...
...
...
```

From here, there are a lot of different actions available for license-model. To invoke one, just pass the action name as well as all the required parameters.

```
$ onap-client sdc license-model add-license-model --vendor-name "thisisatestvendor123"

2020-03-02 12:29:37,848 {
    "method": "POST",
    "auth": "***********",
    "url": "https://vvp-onap-elalto.westus2.cloudapp.azure.com:30600/onboarding-api/v1.0/vendor-license-models",
    "headers": {
        "Accept": "application/json",
...
...
```


### Python


To use the onap-client in a script, create an instance of the Client class:

```
from onap_client.client.clients import Client

c = Client()

```

Each request follows the same pattern as using the cli, and parameters are passed as ``**kwargs``. You can check the required parameters by using the cli with the ``--help`` flag. Each request will return a ``RequestHandler`` object.

For example, to create a license model in the same way as shown above:

```
from onap_client.client.clients import Client

c = Client()

license_model = c.sdc.license_model.add_license_model(vendor_name="MyNewVendor")

status = license_model.status_code
raw_api_response = license_model.response_data
```


### Utility CLI


The utility CLI is more handcrafted than the other cli options. A developer has to mark a function in the codebase as a ``utility`` function for it to show up as available from the cli.

These functions are more for quality of life activities. For example, to retrieve the tosca model for a service from SDC, you have to: 
- query SDC for a list of all services
- find the service ID for the service you're looking for
- query SDC for the tosca model for that service ID

That can be cumbersome, especially if there are a lot of services created. Instead, there's a utility function for it:

```
$ onap-client utility get-service "testservice"
```


#### View all available utility functions


```
$ onap-client utility --help
+--------------------------+-----------------------------------------------+----------------+
| name                     | description                                   | parameters     |
+--------------------------+-----------------------------------------------+----------------+
| --help                   |                                               |                |
|                          |                                               |                |
| get-service              | Queries SDC for the TOSCA model for a service | <service_name> |
|                          |                                               |                |
| get-service-distribution | None                                          | <service_name> |
|                          |                                               |                |
| get-service-id           | None                                          | <service_name> |
|                          |                                               |                |
| poll-distribution        | None                                          | <service_name> |
|                          |                                               |                |
| get-vnf                  | Queries SDC for the TOSCA model for a VNF     | <vnf_name>     |
|                          |                                               |                |
| get-vsp                  | None                                          | <vsp_name>     |
|                          |                                               |                |
+--------------------------+-----------------------------------------------+----------------+
``` 

### Spec-Engine CLI


The spec engine CLI is a simple templating engine that you can feed JSON files into in order to interact with ONAP applications. A JSON spec file will have various ONAP resource definitions, and by loading the file into the engine it will create the resources in ONAP. For a simple comparison, think of it like writing a heat-template, but for ONAP.


```
$ onap-client spec-engine --help
usage: onap-client [-h] [--load-spec LOAD_SPEC]
                   [--validate-spec VALIDATE_SPEC]
                   [--show-resource-spec SHOW_RESOURCE_SPEC]
                   [--list-spec-resources]

Spec Engine CLI

optional arguments:
  -h, --help            show this help message and exit
  --load-spec LOAD_SPEC
                        Load a local spec file into the ONAP client spec
                        engine.
  --validate-spec VALIDATE_SPEC
                        Validates a local spec file for the spec engine.
  --show-resource-spec SHOW_RESOURCE_SPEC
                        Show spec for a given resource.
  --list-spec-resources
                        List available spec resources.
```


#### Loading a spec.json file


```
$ onap-client spec-engine --load-spec 
```


#### Creating a spec file


The structure of a JSON spec file is:

Must be a JSON Dictionary

- optional key: ``parameters``
    - Value is key-pairs dictionary that is used prior to interacting with ONAP. The spec-engine uses a simple string-replace operation performed over the rest of the input JSON file.

- required key: ``spec``
    * Value is a list of dictionaries that have the various specs for creating and interacting with objects in ONAP.
    * requires two keys:
        - ``type``: value must be an available ``spec`` type (see below for how to find available spec types)
        - ``resource_spec``: key/value dict with input properties and values (see below for how to find required and optional properties)


#### View the available ``spec`` types


```
$ onap-client spec-engine --list-spec-resources
VNF_INSTANCE
SERVICE_INSTANCE
MODULE_INSTANCE
PRELOAD
VSP
VNF
SERVICE
LICENSE_MODEL
```


#### View the required and optional properties for a spec type:


```
$ onap-client spec-engine --show-resource-spec SERVICE_INSTANCE
{
    "service_instance_name": {
        "type": "<class 'str'>",
        "required": false,
        "default": "SI_9cde"
    },
    "requestor_id": {
        "type": "<class 'str'>",
        "required": false,
        "default": "cs0008"
    },
    "model_name": {
        "type": "<class 'str'>",
        "required": true
    },
    "model_version": {
        "type": "<class 'str'>",
        "required": false,
        "default": "1.0"
    },
    "tenant_id": {
        "type": "<class 'str'>",
        "required": true
    },
    "cloud_owner": {
        "type": "<class 'str'>",
        "required": true
    },
    "cloud_region": {
        "type": "<class 'str'>",
        "required": true
    },
    "api_type": {
        "type": "<class 'str'>",
        "required": false,
        "default": "GR_API"
    },
    "service_type": {
        "type": "<class 'str'>",
        "required": true
    },
    "customer_name": {
        "type": "<class 'str'>",
        "required": true
    },
    "project_name": {
        "type": "<class 'str'>",
        "required": true
    },
    "owning_entity_name": {
        "type": "<class 'str'>",
        "required": true
    }
}
```


#### Example spec


Here is a complete example spec to create a service model for a VNF:


```
{
  "parameters": {
    "vendor_name": "TestVendor",
    "service_name": "TestService",
    "software_product_name": "TestVSP",
    "vnf_name": "TestVNF",
    "heat_zip_path": "/path/to/heat.zip"
  },
  "spec": [
    {
      "type": "LICENSE_MODEL",
      "resource_spec": {
        "vendor_name": "{{vendor_name}}",
        "license_agreement_name": "{{vendor_name}}"
      }
    },
    {
      "type": "VSP",
      "resource_spec": {
        "software_product_name": "{{software_product_name}}",
        "license_model_name": "{{vendor_name}}",
        "vendor_name": "{{vendor_name}}",
        "file_path": "{{heat_zip_path}}",
        "category": "Application L4+",
        "sub_category": "Web Server",
        "description": "My New VSP"
      }
    },
    {
      "type": "VNF",
      "resource_spec": {
        "vnf_name": "{{vnf_name}}",
        "software_product_name": "{{software_product_name}}"
      }
    },
    {
      "type": "SERVICE",
      "resource_spec": {
        "service_name": "{{service_name}}",
        "instantiation_type": "A-la-carte",
        "contact_id": "cs0008",
        "category_name": "Network L4+",
        "tag": "evo",
        "project_code": "123457",
        "environment_context": "General_Revenue-Bearing",
        "ecomp_generated_naming": "false",
        "description": "Brand New Service",
        "service_type": "abcd",
        "service_role": "1234",
        "resources": [{
          "resource_name": "{{vnf_name}}",
          "catalog_resource_name": "{{vnf_name}}",
          "origin_type": "VF"
        }],
        "wait_for_distribution": true
      }
    }
  ]
}
```
