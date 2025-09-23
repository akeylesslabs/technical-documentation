---
title: CLI Reference - Log-Forwarding
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
This section outlines the CLI commands relevant to the Gateway Log-Forwarding.

General Flags:

`--profile, --token`:  Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

> 👍 Tip
> 
> Flags with a default value of `use-existing` indicate that the field's value will remain unchanged unless explicitly modified.

To forward your Akeyless audit logs directly from your Gateway, you can set the relevant settings of your target logs server using the CLI.

## <p style="color:blue">_update_</p>

Command to update log forwarding configuration

##### Flags

`aws-s3`

`azure-analytics`

`datadog`

`elasticsearch`

`google-chronicle`

`logstash`

`logz-io`

`splunk`

`stdout`

`sumologic`

`syslog`

### <p style="color:blue">_AWS S3_</p>

Updates Log Forwarding config for aws-s3

##### Usage

```shell
akeyless gateway update log-forwarding aws-s3 \
--enable 'true'|'false' \
--output-format 'text'|'json' \
--pull-interval '10' \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--log-folder <AWS Folder> \
--bucket-name <Bucket Name> \
--auth-type [access_key/cloud_id/assume_role] \
--access-id <AWS access id> \
--access-key <AWS access key> \
--region <AWS-Region> \
--role-arn <AWS role arn>
```

##### Flags

`--enable[=true]`: Enable Log Forwarding [`true`/`false`]

`--output-format[=text]`: Logs format [`text`/`json`]

`--pull-interval[=10]`: Pull interval in seconds

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

`--log-folder[=use-existing]`: AWS S3 destination folder for logs

`--bucket-name`: AWS S3 bucket name

`--auth-type`: AWS auth type [`access_key`/`cloud_id`/`assume_role`]

`--access-id`: AWS access id relevant for `access_key` auth-type

`--access-key`: AWS access key relevant for `access_key` auth-type

`--region`: AWS region

`--role-arn`: AWS role arn relevant for `assume_role` auth-type

### <p style="color:blue">_Azure Log Analytics_</p>

Updates Log Forwarding config for azure-analytics

##### Usage

```shell
akeyless gateway update log-forwarding azure-analytics \
--enable 'true'/'false' \
--output-format 'text'/'json' \
--pull-interval '10' \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--workspace-id <Azure workspace id> \
--workspace-key <Azure workspace key>
```

##### Flags

`--enable[=true]`: Enable Log Forwarding [`true`/`false`]

`--output-format[=text]`: Logs format [`text`/`json`]

`--pull-interval[=10]`: Pull interval in seconds

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

`--workspace-id`: Azure workspace id

`--workspace-key`: Azure workspace key

### <p style="color:blue">_Datadog_</p>

Updates Log Forwarding config for datadog

##### Usage

```shell
akeyless gateway update log-forwarding datadog \
--enable 'true'/'false' \
--output-format 'text'/'json' \
--pull-interval '10' \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--host <datadog host> \
--api-key <Datadog api key> \
--log-source <Datadog log source> \
--log-tags <log tags formatted as "key:value"> \
--log-service <Datadog log service>
```

##### Flags

`--enable[=true]`: Enable Log Forwarding [`true`/`false`]

`--output-format[=text]`: Logs format [`text`/`json`]

`--pull-interval[=10]`: Pull interval in seconds

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

`--host`: Datadog host

`--api-key`: Datadog api key

`--log-source[=use-existing]`: Datadog log source

`--log-tags[=use-existing]`: A comma-separated list of Datadog log tags formatted as "`key`:`value`" strings

`--log-service[=use-existing]`: Datadog log service

### <p style="color:blue">_ELK - Elasticsearch_</p>

Updates Log Forwarding config for elasticsearch

##### Usage

```shell
akeyless gateway update log-forwarding elasticsearch \
--enable 'true'/'false' \
--output-format 'text'/'json' \
--pull-interval '10' \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--index <Elasticsearch index> \
--server-type [nodes/cloud] \
--nodes <Elasticsearch nodes> \
--cloud-id <Elasticsearch cloud id> \
--auth-type <Elasticsearch auth type> \
--api-key <Elasticsearch api key> \
--user-name <Elasticsearch user name> \                            
--password <Elasticsearch password> \                              
--enable-tls <enable tls> \                             
--certificate-file <path/to/certificate> \                      
--tls-certificate <Elasticsearch tls certificate>        
```

##### Flags

`--enable[=true]`: Enable Log Forwarding [`true`/`false`]

`--output-format[=text]`: Logs format [`text`/`json`]

`--pull-interval[=10]`: Pull interval in seconds

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

`--index`: Elasticsearch index

`--server-type`: Elasticsearch server type [`nodes`/`cloud`]

`--nodes`: Elasticsearch nodes relevant only for `nodes` server-type

`--cloud-id`: Elasticsearch cloud id relevant only for `cloud` server-type

`--auth-type`: Elasticsearch auth type [`api_key`/`password`]

`--api-key`: Elasticsearch api key relevant only for `api_key` auth-type

`--user-name`: Elasticsearch user name relevant only for `password` auth-type

`--password`: Elasticsearch password relevant only for `password` auth-type

`--enable-tls`: enable-tls

`--certificate-file`: Path to a file that contain elasticsearch certificate in `PEM` format

`--tls-certificate[=use-existing]`: Elasticsearch tls certificate (`PEM format`) in a Base64 format

### <p style="color:blue">_Google Chronicle_</p>

Updates Log Forwarding config for google-chronicle

##### Usage

```shell
akeyless gateway update log-forwarding google-chronicle \
--enable 'true'/'false' \
--output-format 'text'/'json' \
--pull-interval '10' \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--gcp-key-file-path <path/to/sa/private-key> \
--gcp-key <Base64-encoded service account private key text> \
--customer-id <customer id> \
--region <Google chronicle region> \
--log-type <log type>
```

##### Flags

`--enable[=true]`: Enable Log Forwarding [`true`/`false`]

`--output-format[=text]`: Logs format [`text`/`json`]

`--pull-interval[=10]`: Pull interval in seconds

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

`--gcp-key-file-path`: Path to file with the service account private key

`--gcp-key`: Base64-encoded service account private key text

`--customer-id`: Google chronicle `customer id`

`--region`: Google chronicle region [`eu_multi_region`/`london`/`us_multi_region`/`singapore`/`tel_aviv`]

`--log-type`: Google chronicle log type

### <p style="color:blue">_ELK - Logstash_</p>

Updates Log Forwarding config for logstash

##### Usage

```shell
akeyless gateway update log-forwarding logstash \
--enable 'true'/'false' \
--output-format 'text'/'json' \
--pull-interval '10' \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--dns <Logstash dns> \
--protocol [tcp / udp] \
--enable-tls <enabe-tls> \
--certificate-file <path/to/certificate> \
--tls-certificate <logstash tls certificate>
```

##### Flags

`--enable[=true]`: Enable Log Forwarding [`true`/`false`]

`--output-format[=text]`: Logs format [`text`/`json`]

`--pull-interval[=10]`: Pull interval in seconds

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

`--dns`: Logstash dns

`--protocol`: Logstash protocol [`tcp`/`udp`]

`--enable-tls`: Enable-tls

`--certificate-file`: Path to a file that contain logstash certificate in `PEM` format

`--tls-certificate[=use-existing]`: Logstash tls certificate (PEM format) in a Base64 format

### <p style="color:blue">_Logz.io_</p>

Updates Log Forwarding config for logz-io

##### Usage

```shell
akeyless gateway update log-forwarding logz-io \
--enable 'true'/'false' \
--output-format 'text'/'json' \
--pull-interval '10' \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--logz-io-token <Logz-io token> \
--protocol [tcp/https]
```

##### Flags

`--enable[=true]`: Enable Log Forwarding [`true`/`false`]

`--output-format[=text]`: Logs format [`text`/`json`]

`--pull-interval[=10]`: Pull interval in seconds

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

`--logz-io-token`: Logz-io token

`--protocol`: Logz-io protocol [tcp/https]

### <p style="color:blue">_Splunk_</p>

Updates Log Forwarding config for splunk

##### Usage

```shell
akeyless gateway update log-forwarding splunk \
--enable 'true'/'false' \
--output-format 'text'/'json' \
--pull-interval '10' \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--splunk-url <URL>
--splunk-token <splunk-token> \
--source <Splunk source> \
--source-type <Splunk source type>
--index <Splunk index> \ 
--enable-tls <enable tls> \                             
--certificate-file <path/to/certificate> \                      
--tls-certificate <Elasticsearch tls certificate>
```

##### Flags

`--enable[=true]`: Enable Log Forwarding [`true`/`false`]

`--output-format[=text]`: Logs format [`text`/`json`]

`--pull-interval[=10]`: Pull interval in seconds

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

`--splunk-url`: Splunk server URL

`--splunk-token`: splunk-token

`--source[=use-existing]`: Splunk source

`--source-type[=use-existing]`: Splunk source type

`--index`: Splunk index

`--enable-tls`: Enable-tls

`--certificate-file`: Path to a file that contain logstash certificate in `PEM` format

`--tls-certificate[=use-existing]`: Logstash tls certificate (PEM format) in a Base64 format

### <p style="color:blue">_STDOUT_</p>

Updates Log Forwarding config for standard output

##### Usage

```shell
akeyless gateway update log-forwarding stdout \
--enable 'true'/'false' \
--output-format 'text'/'json' \
--pull-interval '10' \ \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

##### Flags

`--enable[=true]`: Enable Log Forwarding [`true`/`false`]

`--output-format[=text]`: Logs format [`text`/`json`]

`--pull-interval[=10]`: Pull interval in seconds

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

### <p style="color:blue">_Sumo Logic_</p>

Updates Log Forwarding config for sumologic

##### Usage

```shell
akeyless gateway update log-forwarding sumologic \
--enable 'true'/'false' \
--output-format 'text'/'json' \
--pull-interval '10' \ \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--endpoint <endpoint URL> \
--sumologic-tags <Sumologic tags> \
--host <SumoLoginc host>
```

##### Flags

`--enable[=true]`: Enable Log Forwarding [`true`/`false`]

`--output-format[=text]`: Logs format [`text`/`json`]

`--pull-interval[=10]`: Pull interval in seconds

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

`--endpoint`: Sumologic endpoint URL

`--sumologic-tags[=use-existing]`: A comma-separated list of Sumologic tags

`--host[=use-existing]`: Sumologic host

### <p style="color:blue">_Syslog_</p>

Updates Log Forwarding config for syslog

##### Usage

```shell
akeyless gateway update log-forwarding syslog \
--enable 'true'/'false' \
--output-format 'text'/'json' \
--pull-interval '10' \ \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--network [tcp/udp] \
--host <host> \
--target-tag <Syslog target tag> \
--formatter [text/cef] \
--enable-tls <enable tls> \                             
--certificate-file <path/to/certificate> \                      
--tls-certificate <Elasticsearch tls certificate>
```

##### Flags

`--enable[=true]`: Enable Log Forwarding [`true`/`false`]

`--output-format[=text]`: Logs format [`text`/`json`]

`--pull-interval[=10]`: Pull interval in seconds

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

`--network`: Syslog network [`tcp`/`udp`]

`--host`: Syslog host

`--target-tag[=use-existing]`: Syslog target tag

`--formatter[=text]`: Syslog formatter [`text`/`cef`]

`--enable-tls`: Enable-tls

`--certificate-file`: Path to a file that contain logstash certificate in `PEM` format

`--tls-certificate[=use-existing]`: Logstash tls certificate (PEM format) in a Base64 format

### <p style="color:blue">_get_</p>

Command to get log forwarding configuration

```shell
akeyless gateway get log-forwarding \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```