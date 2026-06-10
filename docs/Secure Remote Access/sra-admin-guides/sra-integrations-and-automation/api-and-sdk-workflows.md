---
title: API and SDK Workflows
slug: sra-api-and-sdk-workflows
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Use this page as an overview of SRA automation workflows by using the Akeyless API and SDKs.

This page intentionally links to the reference endpoints instead of duplicating request schema detail.

## Core SRA API Endpoints

* [Get Gateway Remote Access](https://docs.akeyless.io/reference/gatewaygetremoteaccess)
* [Update Gateway Remote Access](https://docs.akeyless.io/reference/gatewayupdateremoteaccess)
* [Update Gateway Remote Access RDP Recordings](https://docs.akeyless.io/reference/gatewayupdateremoteaccessrdprecordings)
* [Update Gateway Remote Access Desktop App](https://docs.akeyless.io/reference/gatewayupdateremoteaccessdesktopapp)
* [List SRA Sessions](https://docs.akeyless.io/reference/listsrasessions)
* [List SRA Bastions](https://docs.akeyless.io/reference/listsrabastions)

## Session Forwarding API Variants (11)

* [AWS S3](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsawss3)
* [Azure Log Analytics](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsazureanalytics)
* [Datadog](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsdatadog)
* [Elasticsearch](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogselasticsearch)
* [Google Chronicle](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsgooglechronicle)
* [Logstash](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogslogstash)
* [Logz.io](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogslogzio)
* [Splunk](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogssplunk)
* [stdout](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsstdout)
* [Sumo Logic](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogssumologic)
* [Syslog](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogssyslog)

## SDK Coverage

SDKs with SRA-relevant operations and examples include:

* Go SDK: [https://github.com/akeylesslabs/akeyless-go](https://github.com/akeylesslabs/akeyless-go)
* Python SDK: [https://github.com/akeylesslabs/akeyless-python](https://github.com/akeylesslabs/akeyless-python)
* Java SDK: [https://github.com/akeylesslabs/akeyless-java](https://github.com/akeylesslabs/akeyless-java)

Use API endpoint references above as the canonical source for request and response structure.
