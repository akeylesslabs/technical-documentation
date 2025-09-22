---
title: Log Forwarding Configuration
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
To forward your Akeyless audit logs directly from your Gateway, you can set the relevant settings of your target logs server using the [CLI](https://docs.akeyless.io/docs/cli) or directly from the [Gateway Configuration Manager](doc:gateway-configuration-manager).

By default, the log format of all of the commands below is `text` and the pull interval is set to `10` seconds. 

> 📘 Authorized Users
> 
> Only users with [access permission ](https://docs.akeyless.io/docs/gateway-access-permissions) on the gateway to manage log forwarding will authorize to set log forwards using the CLI.

## Syslog

```shell
akeyless gateway update log-forwarding syslog \
--gateway-url 'https://Your-Akeyless-GW-URL:8000' \
--host <syslog host> 
```

> 👍 Note
> 
> The outputted message format conforms to Syslog format and assumes the Syslog server doesn’t add its own formatting to the message.

Default format: `<date > <time> <host name> <log level> <message>`. 

You can find the complete list of additional parameters for this command in the [CLI Reference - Log-Forwarding](https://docs.akeyless.io/docs/cli-reference-log-forwarding#p-stylecolorbluesyslogp) section. 

## Splunk

You can forward the Gateway logs to an existing Splunk [HTTP Event Collector](https://docs.splunk.com/Documentation/Splunk/8.0.4/Data/UsetheHTTPEventCollector) :

```shell
akeyless gateway update log-forwarding splunk \
--gateway-url 'https://Your-Akeyless-GW-URL:8000' \
--splunk-url <server URL> \
--splunk-token <token> \
--source  <source> \
--source-type <source type> \
--index <index>
```

You can find the complete list of additional parameters for this command in the [CLI Reference - Log-Forwarding](https://docs.akeyless.io/docs/cli-reference-log-forwarding#p-stylecolorbluesplunkp) section.

## ELK - Logstash

```shell
akeyless gateway update log-forwarding logstash \
--gateway-url 'https://Your-Akeyless-GW-URL:8000' \
--dns <logstash dns> \
--protocol tcp
```

You can find the complete list of additional parameters for this command in the [CLI Reference - Log-Forwarding](https://docs.akeyless.io/docs/cli-reference-log-forwarding#p-stylecolorbluelogstashp) section.

## ELK - Elasticsearch

```shell
akeyless gateway update log-forwarding elasticsearch \
--gateway-url 'https://Your-Akeyless-GW-URL:8000' \
--index <index> \
--server-type <cloud> \
--cloud-id <your cloud-id> \
--auth-type <api_key \
--api-key <your api_key> 
```

You can find the complete list of additional parameters for this command in the [CLI Reference - Log-Forwarding](https://docs.akeyless.io/docs/cli-reference-log-forwarding#p-stylecolorblueelasticsearchp) section.

## Logz.io

Using Log [Shipping Tokens](https://docs.logz.io/docs/user-guide/admin/authentication-tokens/log-shipping-tokens/):

```shell
akeyless gateway update log-forwarding logz-io \
--gateway-url[=http://localhost:8000] 'https://Your-Akeyless-GW-URL:8000' \
--logz-io-token <logz-io token> \
--protocol <tcp>
```

You can find the complete list of additional parameters for this command in the [CLI Reference - Log-Forwarding](https://docs.akeyless.io/docs/cli-reference-log-forwarding#p-stylecolorbluelogz-iop) section.

## AWS S3

> 🚧 Warning
> 
> Logs will be uploaded to your S3 bucket based on 10 minutes intervals. Keep in mind that in case your pod will scale down or restart, logs that were not uploaded to your bucket will be lost.

The following permissions are required to forward the audit logs to an S3 bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::<bucket_name>/folder_name/*"
    }
  ]
}
```

Run the following CLI command:

```shell
akeyless gateway update log-forwarding aws-s3 \
--gateway-url 'https://Your-Akeyless-GW-URL:8000' \
--log-folder <s3 destination folder> \
--bucket-name <s3 bucker name> \
--auth-type <access_key/cloud_id/assume_role> \
--access-id <aws access-id> \
--access-key <aws access-key> \
--region <aws region> \
--role-arn <aws role-arn>
```

You can find the complete list of additional parameters for this command in the [CLI Reference - Log-Forwarding](https://docs.akeyless.io/docs/cli-reference-log-forwarding#p-stylecolorblueaws-s3p) section.

## Azure Log Analytics

Logs will be sent to a given workspace according to the provided ID.

```shell
akeyless gateway update log-forwarding azure-analytics \
--gateway-url 'https://Your-Akeyless-GW-URL:8000' \
--workspace-id <azure workspace-id> \
--workspace-key <azure workspace-key> 
```

You can find the complete list of additional parameters for this command in the [CLI Reference - Log-Forwarding](https://docs.akeyless.io/docs/cli-reference-log-forwarding#p-stylecolorblueazure-analyticsp) section.

## STDOUT

Setting log forwarding to stdout: 

```shell
akeyless gateway update log-forwarding stdout \
--gateway-url 'https://Your-Akeyless-GW-URL:8000>' 
```

You can find the complete list of additional parameters for this command in the [CLI Reference - Log-Forwarding](https://docs.akeyless.io/docs/cli-reference-log-forwarding#p-stylecolorbluestdoutp) section.

## DataDog

Setting log forwarding to DataDog system: 

```shell
akeyless gateway update log-forwarding datadog \
--gateway-url 'https://Your-Akeyless-GW-URL:8000' \
--host <datadog host> \
--api-key <datadog api-key> \
--log-source <datadog log source> \
--log-tags <logs tags [key:value]> \
--log-service <datadog log service>
```

You can find the complete list of additional parameters for this command in the [CLI Reference - Log-Forwarding](https://docs.akeyless.io/docs/cli-reference-log-forwarding#p-stylecolorbluedatadogp) section.

## Sumo Logic

Setting log forwarding to Sumo Logic:

```shell
akeyless gateway update log-forwarding sumologic \
--gateway-url 'https://Your-Akeyless-GW-URL:8000' \
--endpoint <endpoint url> \
--sumologic-tags <sumologic tags> \
--host <sumologic host>
```

You can find the complete list of additional parameters for this command in the [CLI Reference - Log-Forwarding](https://docs.akeyless.io/docs/cli-reference-log-forwarding#p-stylecolorbluesumologicp) section.

## Google Chronicle

Setting log forwarding to Google Chronicle:

```shell
akeyless gateway update log-forwarding google-chronicle \
--gateway-url 'https://Your-Akeyless-GW-URL:8000' \
--gcp-key <Base64-encoded service account private key> \
--customer-id <customer-id> \
--region <eu_multi_region/london/us_multi_region/singapore/tel_aviv> \
--log-type <log type>
```

You can find the complete list of additional parameters for this command in the [CLI Reference - Log-Forwarding](https://docs.akeyless.io/docs/cli-reference-log-forwarding#p-stylecolorbluegoogle-chroniclep) section.