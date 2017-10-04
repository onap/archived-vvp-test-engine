# ICE CI Container (Automat Testing):
In order to run the container, follow the below steps:


## DataBase:  
The CI container uses internal `Sqlite` database.
It creates its own database tables in order to store the tests results.
The CI Container needs also the main ICE database configuration (see below).

## Environment: 
The CI container requires the following Environment variables:

 >#### General  
 >* DJANGO_SETTINGS_MODULE=settings
 >* PYTHONPATH=/app
 >* DISPLAY=:99
  
>#### ICE-CI Database Settings  
>* CI_DB_NAME=ice_ci_db
>* CI_DB_USER=iceci
  
>#### ICE-EM Database Settings  
>* ICE_DB_NAME=icedb
>* ICE_DB_USER=_\<ice db user name\>_
>* ICE_DB_PASSWORD=_\<ice db user password\>_
>* ICE_DB_HOST=_<ice db host name>_
>* ICE_DB_PORT=5432

>#### ICE-CI Contact Mail Settings for sending results report
>* NUMBER_OF_TEST_RESULTS=30

>#### Mail setting
>* ICE_CI_ENVIRONMENT_NAME=Staging
>* ICE_EMAIL_HOST=_\<email host name\>_
>* ICE_CONTACT_FROM_ADDRESS=noreply-ci@d2ice.att.io

>#### Recipients for CI report
>* ICE_CONTACT_EMAILS=_'\<user mail\>, \<…\> '_

>#### URL of ICE portal (used by Selenium)
>* ICE_PORTAL_URL=_\<url of ice portal\>_   (e.g: http://development.d2ice.att.io/)

## DB Migration:
Migrations should be run in the standard way

## Test Execution:
In order to invoke the test session, run the following ansible playbook.
It will run the tests and record their results inside the CI dedicated database.
``` 
$ ansible-playbook scripts/playbooks/run_ci_test.yml --extra-vars='test_num=<id_number>'
```

## Report Only:
Run the command using the additional tag "ci_report":
```
$ ansible-playbook scripts/playbooks/run_ci_test.yml --extra-vars='test_num=<id_number>' --tags ci_report
```

## Trigger Sending Test Report to mail recipients:
```
 GET  http://<ci-django-app-host-and-port>/ice-ci/v1/testresultstomail/<identification-number>
``` 
 \<identification-number\> means an arbitrary identifier for the generated report mail.
 
  
  
  
  
