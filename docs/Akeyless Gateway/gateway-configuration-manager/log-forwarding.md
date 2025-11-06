---
title: Log Forwarding
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
You can export the audit logs from the Akeyless Gateway to any of the following log services:

* [Amazon S3](https://docs.akeyless.io/docs/log-forwarding#amazon-s3)

* [Azure Log Analytics](https://docs.akeyless.io/docs/log-forwarding#azure-log-analytics)

* [Datadog](https://docs.akeyless.io/docs/log-forwarding#datadog)

* [Elasticsearch](https://docs.akeyless.io/docs/log-forwarding#elasticsearch)

* [Google Chronicle](https://docs.akeyless.io/docs/log-forwarding#google-chronicle)

* [Logstash](https://docs.akeyless.io/docs/log-forwarding#logstash)

* [Logz.io](https://docs.akeyless.io/docs/log-forwarding#logzio)

* [Splunk](https://docs.akeyless.io/docs/log-forwarding#splunk)

* [STDOUT](https://docs.akeyless.io/docs/log-forwarding#stdout)

* [Sumo Logic ](https://docs.akeyless.io/docs/log-forwarding-2#sumo-logic)

* [Syslog](https://docs.akeyless.io/docs/log-forwarding#syslog)

> 🚧 Warning
>
> The log forwarding mechanism can only fetch logs from the previous 24 hours. Please ensure that your Gateway default Authentication Method has an [Access Role ](https://docs.akeyless.io/docs/rbac) that allows viewing **all** audit logs in the account.

# Amazon S3

When you export the audit logs from the Akeyless Gateway to Amazon S3, the logs are stored in a specified S3 bucket under:

**\{root_folder_name} / \{year} / \{month} / \{day}**

> 📘 Info
>
> The default root folder is `akeyless-log`. You can change this when you set up the log file export in the Akeyless Gateway.

The log files include log records from a ten-minute window, where the file name includes the start time of the logs. For example:

**akeyless-log/2021/05/25/akeyless-audit_2021-05-25T16:30.log**

This file contains records from 16:30:00 to 16:39:59. Each entry is a JSON file that can be parsed individually.

1. Create a bucket in S3, and generate an access key with permission to write to the bucket.

2. Log in to the Akeyless Gateway and go to **Log Forwarding**.

3. Select the **Enable** checkbox.

4. Choose the log format - `Text` or `JSON`.

5. Audit Log Server insert: `https://audit.akeyless.io/`.

6. From the **Log Service** dropdown list, select `Amazon S3`.

7. Choose the authentication mode either using **Credentials**, **Gateway Cloud ID**or using **Assume Role**.

8. For **Credentials** Define the **Access ID**, **Access Key**, and **Bucket Name** for the bucket you created in the first step. For **Assume Role** provide the **AWS Role ARNs**

9. From the **Region** dropdown list, select the region in which your S3 bucket is defined.

10. Optionally, define a **Folder Prefix**, which is the root location in the S3 bucket under which the log files will be stored. The default value is `akeyless-log`.

11. Select **Save Changes**.

> 🚧 Warning
>
> Logs will be uploaded to your S3 bucket based on 10 minutes intervals. Keep in mind that in case your pod will scale down or restart, logs that were not uploaded to your bucket will be lost.

# Azure Log Analytics

When you export the audit logs from the Akeyless Gateway to Azure Log Analytics, the logs are stored in the specified workspace in the **AkeylessAudit_CL** table. The **TimeGenerated** is the time the log was created in Akeyless, and **msg_s** is textual information for the log.

1. Create a new Log Analytics workspace in the Azure Portal, then select **Agent Management**.

2. Log in to the Akeyless Gateway and go to **Log Forwarding**.

3. Select the **Enable** checkbox.

4. Choose the log format - `Text` or `JSON`.

5. Audit Log Server insert: `https://audit.akeyless.io/`.

6. From the **Log Service** dropdown list, select `Azure Log Analytics`.

7. For the **Workspace ID**, copy the value of the **Workspace ID** from the **Agent Management** options in the Azure Portal.

8. For the **Workspace Key**, copy the value of either the **Primary key** or the **Secondary key** from the **Agent Management** options in the Azure Portal.

9. Select **Save Changes**.

# Elasticsearch

1. Log in to the Akeyless Gateway and go to **Log Forwarding**.

2. Select the **Enable** checkbox.

3. Choose the log format - `Text` or `JSON`.

4. Audit Log Server insert: `https://audit.akeyless.io/`.

5. From the **Log Service** dropdown list, select `Elasticsearch`.

6. Define the **Elasticsearch Server**. It can be set either as **Node** or **Cloud ID**.

7. Define the **Elasticsearch Authentication**. It can be set as **Api Key** or **Username & Password**.

8. Define the **Elasticsearch Index**.

9. Optional, check **TLS** and upload the **TLS Certificate** of your log server.

10. Select **Save Changes**.

# Logstash

1. Log in to the Akeyless Gateway and go to **Log Forwarding**.

2. Select the **Enable** checkbox.

3. Choose the log format - `Text` or `JSON`.

4. Audit Log Server insert: `https://audit.akeyless.io/`.

5. From the **Log Service** dropdown list, select `Logstash`.

6. Define the **Logstash Host**.

7. From the **Logstash Protocol** options, select the network protocol used to connect to the Logstash server.

8. Optional, check **TLS** and upload the **TLS Certificate** of your log server.

9. Select **Save Changes**.

10. To configure your Logstash to use the same port and protocol, add the following to the **logstash.conf** file:

```shell
input {
	tcp {
	    port => 8911
      codec => json
	}
}
```

# Logz.io

1. Log in to the Akeyless Gateway and go to **Log Forwarding**.

2. Select the **Enable** checkbox.

3. Choose the log format - `Text` or `JSON`.

4. Audit Log Server insert: `https://audit.akeyless.io/`.

5. From the **Log Service** dropdown list, select `Logz.io`.

6. Define the **Logz.io Token** as the token for your Logz.io account. For details on finding this token, see [here](https://docs.logz.io/user-guide/tokens/log-shipping-tokens/).

7. From the **Logz.io Network** options, select the network protocol to connect to Logz.io.

8. Select **Save Changes**.

# Splunk

1. Log in to the Akeyless Gateway and go to **Log Forwarding**.

2. Select the **Enable** checkbox.

3. Choose the log format - `Text` or `JSON`.

4. Audit Log Server insert: `https://audit.akeyless.io/`.

5. Select' Splunk' from the **Log Service** dropdown list.

6. Define the **Splunk Server URL**.

7. Define the **Splunk Token**.

8. Define the **Splunk Index**.

9. Optional, check **TLS** and upload the **TLS Certificate** of your Splunk server.

10. Select **Save Changes**.

# Syslog

1. Log in to the Akeyless Gateway and go to **Log Forwarding**.

2. Select the **Enable** checkbox.

3. Choose the log format - `Text` or `JSON`.

4. Audit Log Server insert: `https://audit.akeyless.io/`.

5. Select' Syslog' from the **Log Service** dropdown list.

6. From the **Syslog Network** options, select the network protocol used by the Syslog server.

7. Define the **Syslog Host** as the hostname or IP address of the Syslog server.

8. Optionally, define the **Syslog Tag** as the tag with which audit logs are sent to the Syslog server. The default value is `audit-export`.

9. Select the **Syslog Formatter** either `Text` or `CEF`.

10. Optional, check **TLS** and upload the **TLS Certificate** of your log server.

11. Select **Save Changes**.

# Datadog

1. Log in to the Akeyless Gateway and go to **Log Forwarding**.

2. Select the **Enable** checkbox.

3. Choose the log format - `Text` or `JSON`.

4. Audit Log Server insert: `https://audit.akeyless.io/`.

5. From the **Log Service** dropdown list, select `Datadog`.

6. Define the **Datadog host**.

7. Define the **Datadog API Key**.

8. Optional - Define **Log Source**. Default value `akeyless`.

9. Optional - Define **Log Tags** - using `key`:`value` format.

10. Optional - Define **Log Service** , default value `akeyless-gateway`.

# Sumo Logic

1. Log in to the Akeyless Gateway and go to **Log Forwarding**.

2. Select the **Enable** checkbox.

3. Choose the log format - `Text` or `JSON`.

4. Audit Log Server insert: `https://audit.akeyless.io/`.

5. From the **Log Service** dropdown list, select  `Sumo Logic`.

6. Insert the [Endpoint address ](https://help.sumologic.com/docs/send-data/hosted-collectors/http-source/logs-metrics/).

7. Optional - Define **Tags** - `tag1`,`tag2`.

8. Optional - Define **Host** of your choice.

# Google Chronicle

1. Log in to the Akeyless Gateway and go to **Log Forwarding**.

2. Select the **Enable** checkbox.

3. Choose the log format - `Text` or `JSON`.

4. **Audit Log Server** - Insert `https://audit.akeyless.io/`

5. From the **Log Service** dropdown list, select  `Google Chronicle`.

6. **Service Account Key** - A JSON file holding service account credentials.

7. **Customer ID** - Unique identifier for the Chronicle instance.

8. **Region** - The region where your customer account is provisioned.

9. **Log Type** - A log type to identify the log entries

# STDOUT

1. Log in to the Akeyless Gateway and go to **Log Forwarding**.

2. Select the **Enable** checkbox.

3. Choose the log format - `Text` or `JSON`.

4. **Audit Log Server** - Insert `https://audit.akeyless.io/`

5. From the **Log Service** dropdown list, select  `Standard Output`.

<br />
