---
title: CLI Reference - Gateway Secure Remote Access
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
This page lists Secure Remote Access (SRA) commands for gateway update flows and SRA inventory commands.

<CLIGeneralFlags />

## Command Options

Gateway SRA update commands are available under the `gateway update` command group and by alias commands.

Examples:

```shell Command group
akeyless gateway update remote-access
```
```shell Alias
akeyless gateway-update-remote-access
```

## Core SRA Commands

### `gateway update remote-access`

Configures global SRA behavior for the gateway: which bastion redirect URLs and SSH tunnel URLs are allowed, the default session time-to-live, SSH certificate signing settings (legacy algorithm and key exchange algorithms), the RDP/SSH username sub-claim mapping used for externally provided usernames, keyboard layout for web sessions, and whether the session recording indicator is shown to users.
Accepted alias: `gateway-update-remote-access`.

```shell
akeyless gateway update remote-access
```

#### Key flags

`--allowed-urls[=use-existing]`: Comma-separated list of allowed bastion redirect URLs

`--allowed-ssh-url[=use-existing]`: Allowed SSH tunnel URL

`--default-session-ttl-minutes[=use-existing]`: Default session time to live in minutes

`--legacy-ssh-algorithm`: Use legacy SSH signing algorithm (`true` or `false`)

`--rdp-target-configuration[=use-existing]`: RDP username sub-claim mapping

`--ssh-target-configuration[=use-existing]`: SSH username sub-claim mapping

`--kexalgs[=use-existing]`: SSH key exchange algorithm configuration

`--hide-session-recording`: Show or hide session recording indication (`true` or `false`)

`--keyboard-layout[=use-existing]`: Keyboard layout for web bastion sessions

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

#### Example

```shell
akeyless gateway update remote-access \
  --allowed-urls https://bastion.example.com \
  --default-session-ttl-minutes 60 \
  --gateway-url https://my-gw.example.com:8000
```

### `gateway update remote-access-rdp-recording`

Configures video recording of RDP sessions on this gateway. Controls whether recording is enabled, the storage backend (local gateway storage, AWS S3, or Azure Blob Storage), recording quality, optional compression, and optional encryption of uploaded recordings.
Accepted alias: `gateway-update-remote-access-rdp-recording`.

```shell
akeyless gateway update remote-access-rdp-recording
```

#### Key flags

`--rdp-session-recording`: Required. Enable or disable RDP recording (`true` or `false`)

`--rdp-session-storage`: Required when recording is enabled. Supported values: `local`, `aws`, `azure`

`--rdp-session-recording-quality[=medium]`: Recording quality (`low`, `medium`, `high`)

`--rdp-session-recording-compress`: Compress recordings before upload

`--rdp-session-recording-encryption-key`: Encryption key item name for uploaded recordings

`--aws-storage-region`: AWS region where the S3 bucket is located

`--aws-storage-bucket-name`: S3 bucket name

`--aws-storage-bucket-prefix`: Folder path inside the S3 bucket

`--aws-storage-access-key-id`: AWS access key ID (explicit credentials)

`--aws-storage-secret-access-key`: AWS secret access key (explicit credentials)

`--aws-storage-endpoint-url`: Custom endpoint URL for S3-compatible storage

`--azure-storage-account-name`: Azure Storage account name

`--azure-storage-container-name`: Azure Storage container name

`--azure-storage-client-id`: Azure client ID (explicit credentials)

`--azure-storage-client-secret`: Azure client secret (explicit credentials)

`--azure-storage-tenant-id`: Azure tenant ID (explicit credentials)

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

#### Example

```shell
akeyless gateway update remote-access-rdp-recording \
  --rdp-session-recording true \
  --rdp-session-storage aws \
  --aws-storage-region us-east-1 \
  --aws-storage-bucket-name <your-s3-bucket-name> \
  --gateway-url https://my-gw.example.com:8000
```

### `gateway update remote-access-desktop-app`

Configures the Akeyless Desktop App's connection settings for this gateway. Sets the default SSH certificate issuer used when the desktop app initiates sessions, the secure web access URL users are directed to, and the secure web proxy URL.
Accepted alias: `gateway-update-remote-access-desktop-app`.

```shell
akeyless gateway update remote-access-desktop-app
```

#### Key flags

`--desktop-app-ssh-cert-issuer`: Default SSH certificate issuer name (resolved to issuer ID)

`--desktop-app-secure-web-access-url`: Secure web access URL for desktop application

`--desktop-app-secure-web-proxy`: Secure web proxy URL for desktop application

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

#### Example

```shell
akeyless gateway update remote-access-desktop-app \
  --desktop-app-ssh-cert-issuer /SRA/my-ssh-cert-issuer \
  --gateway-url https://my-gw.example.com:8000
```

### `gateway update remote-access-session-forwarding <provider>`

Configures forwarding of SRA session logs to an external logging system. Session logs capture CLI input and output from SSH and database sessions. Each provider variant targets a specific logging backend. Settings include connection credentials for the target system, the log format, and a pull interval. Changes apply per-gateway and per-provider.
Accepted alias: `gateway-update-remote-access-session-forwarding-<provider>`.

```shell
akeyless gateway update remote-access-session-forwarding <provider>
```

#### Common flags (all providers)

`--enable[=true]`: Enable or disable forwarding

`--output-format[=text]`: Log format (`text` or `json`)

`--pull-interval[=10]`: Pull interval in seconds

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

#### Example

```shell
akeyless gateway update remote-access-session-forwarding splunk \
  --splunk-url https://splunk.example.com:8088 \
  --splunk-token <your-splunk-hec-token> \
  --index main \
  --gateway-url https://my-gw.example.com:8000
```

##### `aws-s3`

`--bucket-name`: Required. Target S3 bucket name

`--auth-type`: Required. AWS auth type (`access_key`, `cloud_id`, `assume_role`)

`--region`: AWS region

`--log-folder[=use-existing]`: Destination folder in the S3 bucket

`--access-id`: Required when `--auth-type access_key`

`--access-key`: Required when `--auth-type access_key`

`--role-arn`: Required when `--auth-type assume_role`

##### `azure-analytics`

`--workspace-id`: Required. Azure workspace ID

`--workspace-key`: Required. Azure workspace key

`--enable-batch[=true]`: Enable or disable batch forwarding

##### `datadog`

`--host`: Required. Datadog host

`--api-key`: Required. Datadog API key

`--log-source[=use-existing]`: Datadog source field

`--log-tags[=use-existing]`: Comma-separated tags (`key:value`)

`--log-service[=use-existing]`: Datadog service field

##### `elasticsearch`

`--index`: Required. Elasticsearch index

`--server-type`: Required. Server type (`nodes` or `cloud`)

`--auth-type`: Required. Auth type (`api_key` or `password`)

`--nodes`: Required when `--server-type nodes`

`--cloud-id`: Required when `--server-type cloud`

`--api-key`: Required when `--auth-type api_key`

`--user-name`: Required when `--auth-type password`

`--password`: Required when `--auth-type password`

`--enable-tls`: Enable or disable TLS

`--certificate-file`: Path to a PEM certificate file

`--tls-certificate[=use-existing]`: Base64 PEM certificate value

##### `google-chronicle`

`--customer-id`: Required. Google Chronicle customer ID

`--region`: Required. Region (`eu_multi_region`, `london`, `us_multi_region`, `singapore`, `tel_aviv`)

`--log-type`: Required. Chronicle log type

`--gcp-key-file-path`: Path to a GCP service-account private key file (alternative to `--gcp-key`)

`--gcp-key`: Required. Base64-encoded GCP service-account private key text (or supply via `--gcp-key-file-path`)

##### `logstash`

`--dns`: Required. Logstash DNS or host endpoint

`--protocol`: Required. Protocol (`tcp` or `udp`)

`--enable-tls`: Enable or disable TLS

`--certificate-file`: Path to a PEM certificate file

`--tls-certificate[=use-existing]`: Base64 PEM certificate value

##### `logz-io`

`--logz-io-token`: Required. Logz.io token

`--protocol`: Required. Protocol (`tcp` or `https`)

##### `splunk`

`--splunk-url`: Required. Splunk server URL

`--splunk-token`: Required. Splunk token

`--index`: Required. Splunk index

`--source[=use-existing]`: Splunk source

`--source-type[=use-existing]`: Splunk source type

`--enable-batch[=true]`: Enable or disable batch forwarding

`--enable-tls`: Enable or disable TLS

`--certificate-file`: Path to a PEM certificate file

`--tls-certificate[=use-existing]`: Base64 PEM certificate value

##### `stdout`

The `stdout` provider writes session logs directly to the gateway process standard output. It requires no provider-specific connection or credential flags; only the common flags (`--enable`, `--output-format`, `--pull-interval`, `--gateway-url`) apply.

##### `sumologic`

`--endpoint`: Required. Sumo Logic endpoint URL

`--sumologic-tags[=use-existing]`: Comma-separated Sumo Logic tags

`--host[=use-existing]`: Sumo Logic host

##### `syslog`

`--host`: Syslog host

`--network[=tcp]`: Network (`tcp` or `udp`)

`--formatter[=text]`: Formatter (`text` or `cef`)

`--target-tag[=use-existing]`: Syslog target tag

`--enable-tls`: Enable or disable TLS (TCP only)

`--certificate-file`: Path to a PEM certificate file

`--tls-certificate[=use-existing]`: Base64 PEM certificate value

## Gateway SRA Get Command

### `gateway get remote-access`

Returns the current SRA configuration for the gateway as a JSON object with four sub-objects: `global` (allowed URLs, session TTL, keyboard layout, and legacy SSH settings), `ssh_bastion` (SSH-specific settings), `web_bastion` (web access and RDP recording settings), and `desktop_app` (desktop application settings).
Accepted alias: `gateway-get-remote-access`.

```shell
akeyless gateway get remote-access
```

#### Key flags

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

#### Example

```shell
akeyless gateway get remote-access --gateway-url https://my-gw.example.com:8000
```

## Session and Bastion Inventory Commands

The following commands are top-level CLI commands and are not under `gateway update`.

### `list-sra-sessions`

Lists SRA connection sessions associated with the authenticated user. Returns session metadata including resource type, connection status, and session identifiers. Useful for auditing active or recent connections. Results can be filtered by connection status and resource type.

#### Usage

```shell
akeyless list-sra-sessions
```

#### Key flags

`--status-type`: Session status types. If omitted, defaults to active statuses only (`connecting`, `connected`). Options: `connecting`, `connected`, `failed`, `completed`, `terminated`

`--resource-type`: Connection type filter. Options: `aws`, `eks`, `gke`, `k8s`, `mongodb`, `mssql`, `mysql`, `postgres`, `rdp`, `ssh`

#### Example

```shell
akeyless list-sra-sessions --status-type connected --resource-type ssh
```

#### Behavior notes

By default, this command is own-only scoped in the command implementation.

This command does not appear in `akeyless --help` output; invoke it directly by name.

### `list-sra-bastions`

Lists gateways registered to serve SRA connections (bastions), including their allowed URL configuration.

#### Usage

```shell
akeyless list-sra-bastions
```

#### Key flags

`--allowed-urls-only[=false]`: Show only bastion allowed URL configuration

#### Example

```shell
akeyless list-sra-bastions --allowed-urls-only true
```

#### Behavior notes

`--allowed-urls-only` defaults to `false`.

## Related API Reference

For HTTP endpoint details that map to these commands, see:

* [Get Gateway Remote Access](https://docs.akeyless.io/reference/gatewaygetremoteaccess)
* [Update Gateway Remote Access](https://docs.akeyless.io/reference/gatewayupdateremoteaccess)
* [Update Gateway Remote Access RDP Recordings](https://docs.akeyless.io/reference/gatewayupdateremoteaccessrdprecordings)
* [Update Gateway Remote Access Desktop App](https://docs.akeyless.io/reference/gatewayupdateremoteaccessdesktopapp)
* [Update Gateway Remote Access Session Forwarding AWS S3](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsawss3)
* [Update Gateway Remote Access Session Forwarding Azure Log Analytics](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsazureanalytics)
* [Update Gateway Remote Access Session Forwarding Datadog](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsdatadog)
* [Update Gateway Remote Access Session Forwarding Elasticsearch](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogselasticsearch)
* [Update Gateway Remote Access Session Forwarding Google Chronicle](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsgooglechronicle)
* [Update Gateway Remote Access Session Forwarding Logstash](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogslogstash)
* [Update Gateway Remote Access Session Forwarding Logz.io](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogslogzio)
* [Update Gateway Remote Access Session Forwarding Splunk](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogssplunk)
* [Update Gateway Remote Access Session Forwarding stdout](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsstdout)
* [Update Gateway Remote Access Session Forwarding Sumo Logic](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogssumologic)
* [Update Gateway Remote Access Session Forwarding Syslog](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogssyslog)
* [List SRA Sessions](https://docs.akeyless.io/reference/listsrasessions)
* [List SRA Bastions](https://docs.akeyless.io/reference/listsrabastions)
