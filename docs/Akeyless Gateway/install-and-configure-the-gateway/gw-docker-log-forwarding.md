---
title: Log Forwarding Configuration
excerpt: Standalone Gateway
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
# Log Forwarding

To forward all Akeyless audit logs directly from your Akeyless Gateway, create a local configuration file specifying a target logs server.

To start your Akeyless Gateway with this setting, please mount a local config file at this path: `/home/akeyless/.akeyless/logand.conf`.

```shell
docker run -d -p 8000:8000 -v {path-to}/log_forwarding_conf_file:/home/akeyless/.akeyless/logand.conf -e ADMIN_ACCESS_ID="p-xxxxxxx" -e ADMIN_ACCESS_KEY="<YourAccessKey" --name akeyless-gw  akeyless/base:latest-akeyless
```

## Amazon S3

The following permissions are required to forward the audit logs to an Amazon S3 bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:<your_partition>:s3:::<bucket_name>/folder_name/*"
    }
  ]
}
```

```yaml
enable="true"
target_log_type="aws_s3"
target_s3_folder_prefix=""  # default value "akeyless-log"
target_s3_bucket_name=""
target_s3_aws_auth_type="" # aws_auth_type_access_key|aws_auth_type_cloud_id|aws_auth_type_assume_role
target_s3_aws_access_id="" # aws_auth_type_access_key
target_s3_aws_access_key="" # aws_auth_type_access_key
aws_auth_type_assume_role="" # Relevant for aws_auth_type_assume_role
target_s3_aws_region=""
```

<Callout icon="❗️" theme="error">
  _**Warning:** Logs will be uploaded to an Amazon S3 bucket on ten minute intervals. Pods that terminate before this interval will not upload logs._
</Callout>

## Azure Log Analytics

Logs will be sent to a given workspace according to provided ID.

```yaml
enable="true"
target_log_type="azure_log_analytics"
azure_workspace_id=""
azure_workspace_key="" # can be "Primary key" or "Secondary key"
```

## DataDog

Setting log forwarding to DataDog system:

````yaml
enable="true"
target_log_type="datadog"
target_datadog_host="<datadog host e.g. datadoghq.com>" (required)
target_datadog_api_key="<datadog api key>"(required)
target_datadog_log_source="<The integration name associated with your log>" (optional. Default value: akeyless)
target_datadog_log_tags="<Tags associated with your logs in the form of key:val,key:val... e.g. env:test,version:1>"(optional)
target_datadog_log_service="<The name of the application or service generating the log events>"(optional. Default value: akeyless-gateway)

## Elasticsearch

```yaml
enable="true"
target_log_type="elasticSearch"
"Elasticsearch server - requires one of the following:"
  target_elasticsearch_server_type="elastic-server-nodes"
  target_elasticsearch_nodes="https://host1:9200,https://host2:9200"  
# OR 
  target_elasticsearch_server_type="elastic-server-cloudId"
  target_elasticsearch_cloud_id="<your_cloudId>"

"Elasticsearch authentication - requires one of the following:"
  target_elasticsearch_auth_type="elastic-auth-apiKey"
  target_elasticsearch_api_key="<your_apiKey>"
# OR
  target_elasticsearch_auth_type="elastic-auth-usrPwd"
  target_elasticsearch_user_name="<your_user>"
  target_elasticsearch_password="<your_pwd>"

target_elasticsearch_index="<your_index>" (required)
#TLS Optional
target_elasticsearch_enable_tls="true"
target_elasticsearch_tls_certificate="<Based64 PEM encoded Cert>"
````

## Google Chronicle

Setting log forwarding to Google Chronicle system:

```yaml
target_log_type="google_chronicle"
target_google_chronicle_service_account_key="<Base64 json service account key file content>" (required if "target_google_chronicle_service_account_key_file" is empty)
target_google_chronicle_service_account_key_file="<Path to the json service account key file>" (required if "target_google_chronicle_service_account_key" is empty)
target_google_chronicle_customer_id="<Unique identifier for the Chronicle instance>"(required)
target_google_chronicle_region="<Region where the customer account is provisioned, possible value: "eu_multi_region", "london", "us_multi_region", "singapore", "tel_aviv">" (required)
target_google_chronicle_log_type="<Log type>"(required)
```

## Logstash

```yaml
enable="true"
target_log_type="logstash"
target_logstash_dns="localhost:8911"
target_logstash_protocol="tcp"
#TLS Optional
target_logstash_enable_tls="true"
target_logstash_tls_certificate="<Based64 PEM encoded Cert>"
```

Configure your Logstash to use the same port and protocol:
Add the following to the `logstash.conf` file:\ `input { tcp { port => 8911 codec => json } }`

## Logz.io

```yaml Shell
enable="true"
target_log_type="logz_io"
target_logz_io_token="<TOKEN>"
target_logz_io_protocol="tcp"
# OR 
target_logz_io_protocol="https"
```

For details about log tokens, see [here](https://docs.logz.io/user-guide/tokens/log-shipping-tokens/).

## Splunk

Prerequisites: [Splunk HTTP Event Collector](https://docs.splunk.com/Documentation/Splunk/8.0.4/Data/UsetheHTTPEventCollector)

```yaml
enable="true"
target_log_type="splunk"
target_splunk_sourcetype="<your_sourcetype>"
target_splunk_source="<your_source>"
target_splunk_index="<your_index>"
target_splunk_token="<your_token>"
target_splunk_url="<your_splunk_host_address>"
#TLS Optional
target_splunk_enable_tls="true"
target_splunk_tls_certificate="<Based64 PEM encoded Cert>"
```

## STDOUT

Setting log forwarding to stdout:

```yaml
enable="true"
target_log_type="std_out"
```

## Sumo Logic

Setting log forwarding to Sumo Logic system:

```yaml
target_log_type="sumo_logic"
target_sumologic_endpoint_url="<sumo logic endpoint>"(required)
target_sumologic_tags="<Tags associated with your logs in the form of tag1,tag2...>"(optional)
target_sumologic_host="<Host associated with your logs>"(optional)
```

## Syslog

Set the following settings inside your local config file:

```yaml
enable="true"
target_syslog_tag="ssh-audit-export"
target_log_type="syslog"
target_syslog_network="udp"
target_syslog_host="<host>:<port>"
target_syslog_formatter="[default=text]|cef"
#TLS Optional
target_syslog_enable_tls="true"
target_syslog_tls_certificate="<Based64 PEM encoded Cert>"
```

<Callout icon="📘" theme="info">
  The message format conforms to the Syslog format and assumes that the Syslog server does not add its own formatting to the message.

  Default format: `<date > <time> <host name> <log level> <message>`.

  The variable `target_syslog_formatter` controls the output message format: either `text` or `cef`.
</Callout>


