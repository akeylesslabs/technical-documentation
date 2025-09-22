---
title: Session Log Forwarding
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
Remote Access supports the forwarding of SSH, Database, and Kubernetes session logs.

These terminal-based sessions provide a full transcript of input commands and output responses which can be forwarded to any Log Management / SIEM solution (such as Splunk, ElasticSearch, or just using Syslog).

# Configure

From the Console, click on "Gateways" in the left-side menu.

Choose the Gateway you want to update and then click the "Manage Gateway" button. If you don't have enough permissions, the button will be greyed out and you should check with your Admin for permissions.

From the Manage Gateway section, choose "Remote Access" -> "Session Forwarding" -> "Session Forwarding", click the slider to Enable, and add the log forwarder information. Once done, click "Save".

This can also be done via the CLI as follows:

```shell AWS S3
akeyless gateway update remote-access-session-forwarding aws-s3 \
--enable \
--gateway-url https://<your-gateway-url>:8000 \
--output-format <text|json> \
--pull-interval <in seconds> \
--log-folder <s3-folder> \
--bucket-name <s3-bucket-name> \
--auth-type <access_key/cloud_id/assume_role> \
--access-id <aws-access-id> \ # relevant only for access_key auth-type
--access-key <aws-access-key> \ # relevant only for access_key auth-type
--region <aws-region> \
--role-arn <aws-role-arn> # relevant only for assume_role auth-type
```
```shell Azure Analytics
akeyless gateway update remote-access-session-forwarding azure-analytics \
--enable \
--gateway-url https://<your-gateway-url>:8000 \
--output-format <text|json> \
--pull-interval <in seconds> \
--workspace-id <azure-workspace-id> \
--workspace-key <azure-workspace-key>
```
```shell Datadog
akeyless gateway update remote-access-session-forwarding datadog \
--enable \
--gateway-url https://<your-gateway-url>:8000 \
--output-format <text|json> \
--pull-interval <in seconds> \
--host <datadog-host> \
--api-key <datadog-api-key> \
--log-source <datadog-log-source> \
--log-tags <comma-separated-list of "key:value" strings> \
--log-service <datadog-log-service>
```
```shell Elastic
akeyless gateway update remote-access-session-forwarding elasticsearch \
--enable \
--gateway-url https://<your-gateway-url>:8000 \
--output-format <text|json> \
--pull-interval <in seconds> \
--index <elasticsearch-index> \
--server-type <nodes/cloud> \
--nodes <nodes> \ # relevant only for nodes server-type
--cloud-id <elasticsearch-cloud-id> \ # relevant only for cloud server-type
--auth-type <elasticsearch: api_key/password> \
--api-key <api-key> \ # relevant only for api_key auth-type
--user-name <user-name> \ # relevant only for password auth-type
--password <password> \ # relevant only for password auth-type
--enable-tls <true|false>
--certificate-file <path-to-file \ # elasticsearch certificate in PEM format
--tls-certificate <tls-certificate> # PEM in a Base64 format
```
```shell Google Chronicle
akeyless gateway update remote-access-session-forwarding google-chronicle \
--enable \
--gateway-url https://<your-gateway-url>:8000 \
--output-format <text|json> \
--pull-interval <in seconds> \
--gcp-key-file-path <path-to-service-account-private-key> \
--gcp-key <Base64-encoded service account private key text> \
--customer-id <google-chronicle-customer-id> \
--region <eu_multi_region/london/us_multi_region/singapore/tel_aviv> \
--log-type <log-type>
```
```shell Logstash
akeyless gateway update remote-access-session-forwarding logstash \
--enable \
--gateway-url https://<your-gateway-url>:8000 \
--output-format <text|json> \
--pull-interval <in seconds> \
--dns  <logstash-dns> \
--protocol <tcp/udp> \
--enable-tls <true|false> \
--certificate-file <path-to-file> \ # logstash certificate in PEM format
--tls-certificate <tls-certificate< \ # PEM in a Base64 format
```
```shell Logz.io
akeyless gateway update remote-access-session-forwarding logz-io \
--enable \
--gateway-url https://<your-gateway-url>:8000 \
--output-format <text|json> \
--pull-interval <in seconds> \
--logz-io-token <logz-io-token> \
--protocol <tcp/https>
```
```shell Splunk
akeyless gateway update remote-access-session-forwarding splunk \
--enable \
--gateway-url https://<your-gateway-url>:8000 \
--output-format <text|json> \
--pull-interval <in seconds> \
--splunk-url <splunk-server-url> \
--splunk-token <splunk-token> \
--source <splunk-source> \
--source-type <splunk-source-type> \
--index <splunk-index> \
--enable-tls <true|false> \
--certificate-file <path-to-file> \ # splunk certificate in PEM format
--tls-certificate <tls-certificate> \ # PEM in a Base64 format
```
```shell Stdout
akeyless gateway update remote-access-session-forwarding stdout \
--enable \
--gateway-url https://<your-gateway-url>:8000 \
--output-format <text|json> \
--pull-interval <in seconds> \
```
```shell Sumo Logic
akeyless gateway update remote-access-session-forwarding sumologic \
--enable \
--gateway-url https://<your-gateway-url>:8000 \
--output-format <text|json> \
--pull-interval <in seconds> \
--endpoint <sumologic-endpoint-url> \
--sumologic-tags <comma-separated-list> \
--host <sumologic-host>
```
```shell Syslog
akeyless gateway update remote-access-session-forwarding syslog \
--enable true \
--output-format <text/json> \
--pull-interval <interval-in-seconds> \
--gateway-url https://<your-gateway-url>:8000 \
--network <tcp/udp> \
--host <syslog-host> \
--target-tag <syslog-target-tag> \
--formatter <text/cef>
--enable-tls <true|false> \ # relevant only for network type tcp
--certificate-file <path-to-file \ # syslog certificate in PEM format
--tls-certificate <tls-certificate> \ # PEM in a Base64 format
```
