---
title: Log Forwarding Configuration
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
# Log Forwarding

To forward your Akeyless audit logs directly from your Gateway, you can set the relevant settings of your target logs server directly inside the `values.yaml` file of your Gateway deployment.

On the `values.yaml` file, enable the `logandConf` section and provide the relevant settings as described below:

```yaml values.yaml
logandConf: |
 enable="true"
```

Or using an explicit environment variable:

```yaml
env:
  - name: LOG_FORWARDING
    value: "enable=\"true\"\ntarget_syslog_tag=\"ssh-audit-export\"\ntarget_log_type=\"syslog\"\ntarget_syslog_network=\"udp\"\ntarget_syslog_host=\"my-syslog:514\"\ntarget_syslog_formatter=\"text\""
```

Alternatively, you can specify the entire settings within a `K8s` secret base64 encoded:

```yaml
# Specifies an existing secret for logand should be in yaml syntax, and include:
# - logand-conf field (base64). The content the same as above.
logandExistingSecretName:
```

## Syslog

Edit the `values.yaml` file under the `logForwarding` section:

```yaml
target_syslog_tag="ssh-audit-export"
target_log_type="syslog"
target_syslog_network="udp"
target_syslog_host="<host>:<port>"
target_syslog_formatter="[default=text]|cef"
#TLS Optional
target_syslog_enable_tls="true"
target_syslog_tls_certificate="<Based64 PEM encoded Cert>"
```

> 👍 Note
> 
> The outputted message format conforms to Syslog format and assumes the Syslog server doesn’t add its own formatting to the message.

Default format: `<date > <time> <host name> <log level> <message>`.

The variable `target_syslog_formatter` controls the format of the outputted message either `text` or `cef` - for **CEF**  format.

## Splunk

Prerequisites: [Splunk HTTP Event Collector](https://docs.splunk.com/Documentation/Splunk/8.0.4/Data/UsetheHTTPEventCollector) 

```yaml
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

## ELK - Logstash

```yaml
target_log_type="logstash"
target_logstash_dns="localhost:8911"
target_logstash_protocol="tcp"
#TLS Optional
target_logstash_enable_tls="true"
target_logstash_tls_certificate="<Based64 PEM encoded Cert>"
```

Configure your Logstash to use the same port and protocol:  
Add the following to the `logstash.conf` file:  
`input { tcp { port => 8911 codec => json } }`

## ELK - Elasticsearch

```yaml
logandConf: |
  enable="true"
  target_log_type="elasticSearch"
# "Elasticsearch server - requires one of the following:"
  target_elasticsearch_server_type="elastic-server-nodes"
  target_elasticsearch_nodes="https://host1:9200,https://host2:9200"  
# OR 
# target_elasticsearch_server_type="elastic-server-cloudId"
# target_elasticsearch_cloud_id="<your_cloudId>"

# "Elasticsearch authentication - requires one of the following:"
  target_elasticsearch_auth_type="elastic-auth-apiKey"
  target_elasticsearch_api_key="<your_apiKey>"
# OR
# target_elasticsearch_auth_type="elastic-auth-usrPwd"
# target_elasticsearch_user_name="<your_user>"
# target_elasticsearch_password="<your_pwd>"

  target_elasticsearch_index="<your_index>"  # (required !)

#TLS Optional
  target_elasticsearch_enable_tls="true"
  target_elasticsearch_tls_certificate="<Based64 PEM encoded Cert>"
```

## Logz.io

```yaml Shell
target_log_type="logz_io"
target_logz_io_token="<TOKEN>"
target_logz_io_protocol="tcp"
# OR 
target_logz_io_protocol="https"
```

For details about log tokens, see [here](https://docs.logz.io/user-guide/tokens/log-shipping-tokens/).

## AWS S3

> 🚧 Warning
> 
> Logs will be uploaded to your S3 bucket based on 10 minutes intervals. Keep in mind that in case your pod will scale down or restart, logs that were not uploaded to your bucket will be lost.

```yaml
target_log_type="aws_s3"
target_s3_folder_prefix=""  # default value "akeyless-log"
target_s3_bucket_name=""
target_s3_aws_auth_type="" # aws_auth_type_access_key|aws_auth_type_cloud_id|aws_auth_type_assume_role
target_s3_aws_access_id="" # aws_auth_type_access_key
target_s3_aws_access_key="" # aws_auth_type_access_key
aws_auth_type_assume_role="" # Relevant for aws_auth_type_assume_role
target_s3_aws_region=""
```

## Azure Log Analytics

Logs will be sent to a given workspace according to provided ID.

```yaml
target_log_type="azure_log_analytics"
target_azure_workspace_id=""
target_azure_workspace_key="" # can be "Primary key" or "Secondary key"
```

## STDOUT

Setting log forwarding to stdout: 

```yaml
target_log_type="std_out"
```

## DataDog

Setting log forwarding to DataDog system: 

```yaml
target_log_type="datadog"
target_datadog_host="<datadog host e.g. datadoghq.com>" (required)
target_datadog_api_key="<datadog api key>"(required)
target_datadog_log_source="<The integration name associated with your log>" (optional. Default value: akeyless)
target_datadog_log_tags="<Tags associated with your logs in the form of key:val,key:val... e.g. env:test,version:1>"(optional)
target_datadog_log_service="<The name of the application or service generating the log events>"(optional. Default value: akeyless-gateway)
```

## Sumo Logic

Setting log forwarding to Sumo Logic:

```yaml
target_log_type="sumo_logic"
target_sumologic_endpoint_url="<sumo logic endpoint>"(required)
target_sumologic_tags="<Tags associated with your logs in the form of tag1,tag2...>"(optional)
target_sumologic_host="<Host associated with your logs>"(optional)
```

## Google Chronicle

Setting log forwarding to Google Chronicle:

```yaml
target_log_type="google_chronicle"
target_google_chronicle_service_account_key="<Base64 json service account key file content>" (required if "target_google_chronicle_service_account_key_file" is empty)
target_google_chronicle_service_account_key_file="<Path to the json service account key file>" (required if "target_google_chronicle_service_account_key" is empty)
target_google_chronicle_customer_id="<Unique identifier for the Chronicle instance>"(required)
target_google_chronicle_region="<Region where the customer account is provisioned, possible value: "eu_multi_region", "london", "us_multi_region", "singapore", "tel_aviv">" (required)
target_google_chronicle_log_type="<Log type>"(required)
```