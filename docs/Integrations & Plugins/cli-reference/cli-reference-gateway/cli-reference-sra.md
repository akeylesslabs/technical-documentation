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
This page lists Secure Remote Access (SRA) commands for gateway configuration and SRA file transfer flows.

<CLIGeneralFlags />

## Command Families

SRA CLI commands in this page are grouped into two families:

* **Gateway configuration** commands under `gateway update` (also available as alias commands)
* **File transfer** commands under `file` for upload and download through SRA

### Gateway Configuration Family

Gateway SRA configuration commands are available under the `gateway update` command group and by alias commands.

Example:

```shell Command group
akeyless gateway update remote-access
```
```shell Alias
akeyless gateway-update-remote-access
```

## File Transfer Commands (CLI 1.145+)

The Akeyless CLI supports SRA file transfer with `file upload` and `file download`.

These commands run locally and use the local `scp` client over an SRA tunnel.

```shell Command group
akeyless file upload
```
```shell Alias
akeyless file-upload
```

### `file upload`

Uploads a local file to a remote target through SRA.

```shell
akeyless file upload \
  --target <user@remote-server[:port]> \
  --source-path </full/local/path/file> \
  --destination-path </remote/path/file> \
  --tunnel "-L :5555:0.0.0.0:5555"
```

#### Key flags

`-t, --target`: Required. Target resource in the format `user@ssh-server[:port]`

`--source-path`: Required. Local source file path

`--destination-path`: Required. Remote destination file path

`-T, --tunnel`: Required. SSH tunnel parameter (IPv4 only), for example `-L :5555:0.0.0.0:5555`

`-c, --cert-issuer-name`: Certificate issuer name. If omitted, the CLI profile value is used

`-v, --via-sra`: SRA bastion host and port. If omitted, the CLI profile value is used

`-g, --gateway-url`: Gateway configuration-management URL. If omitted, the CLI profile value is used

> ℹ️ **RBAC capability:** `sra_upload_files`
> ℹ️ **Alias:** `akeyless file-upload`

### `file download`

Downloads a remote file to the local machine through SRA.

```shell
akeyless file download \
  --target <user@remote-server[:port]> \
  --source-path </remote/path/file> \
  --destination-path </full/local/path/file> \
  --tunnel "-L :5555:0.0.0.0:5555"
```

#### Key flags

`-t, --target`: Required. Target resource in the format `user@ssh-server[:port]`

`--source-path`: Required. Remote source file path

`--destination-path`: Required. Local destination file path

`-T, --tunnel`: Required. SSH tunnel parameter (IPv4 only), for example `-L :5555:0.0.0.0:5555`

`-c, --cert-issuer-name`: Certificate issuer name. If omitted, the CLI profile value is used

`-v, --via-sra`: SRA bastion host and port. If omitted, the CLI profile value is used

`-g, --gateway-url`: Gateway configuration-management URL. If omitted, the CLI profile value is used

> ℹ️ **RBAC capability:** `sra_download_files`
> ℹ️ **Alias:** `akeyless file-download`

## Core SRA Commands

### `gateway-update-remote-access`

Configures global SRA behavior for the gateway: which bastion redirect URLs and SSH tunnel URLs are allowed, the default session time-to-live, SSH certificate signing settings (legacy algorithm and key exchange algorithms), the RDP/SSH username sub-claim mapping used for externally provided usernames, keyboard layout for web sessions, and whether the session recording indicator is shown to users.

```shell Alias
akeyless gateway-update-remote-access
```
```shell Command group
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
akeyless gateway-update-remote-access \
  --allowed-urls https://bastion.example.com \
  --default-session-ttl-minutes 60 \
  --gateway-url https://my-gw.example.com:8000
```

### `gateway-update-remote-access-rdp-recording`

Configures video recording of RDP sessions on this gateway. Controls whether recording is enabled, the storage backend (local gateway storage, AWS S3, or Azure Blob Storage), recording quality, optional compression, and optional encryption of uploaded recordings.

```shell Alias
akeyless gateway-update-remote-access-rdp-recording
```
```shell Command group
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
akeyless gateway-update-remote-access-rdp-recording \
  --rdp-session-recording true \
  --rdp-session-storage aws \
  --aws-storage-region us-east-1 \
  --aws-storage-bucket-name <your-s3-bucket-name> \
  --gateway-url https://my-gw.example.com:8000
```

### `gateway-update-remote-access-desktop-app`

Configures the Akeyless Desktop App's connection settings for this gateway. Sets the default SSH certificate issuer used when the desktop app initiates sessions, the secure web access URL users are directed to, and the secure web proxy URL.

```shell Alias
akeyless gateway-update-remote-access-desktop-app
```
```shell Command group
akeyless gateway update remote-access-desktop-app
```

#### Key flags

`--desktop-app-ssh-cert-issuer`: Default SSH certificate issuer name (resolved to issuer ID)

`--desktop-app-secure-web-access-url`: Secure web access URL for desktop application

`--desktop-app-secure-web-proxy`: Secure web proxy URL for desktop application

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

#### Example

```shell
akeyless gateway-update-remote-access-desktop-app \
  --desktop-app-ssh-cert-issuer /SRA/my-ssh-cert-issuer \
  --gateway-url https://my-gw.example.com:8000
```

### `gateway-update-remote-access-session-forwarding-<provider>`

Configures forwarding of SRA session logs to an external logging system. Session logs capture CLI input and output from SSH and database sessions. Each provider variant targets a specific logging backend. Settings include connection credentials for the target system, the log format, and a pull interval. Changes apply per-gateway and per-provider.

```shell Command group
akeyless gateway update remote-access-session-forwarding <provider>
```
```shell Alias
akeyless gateway-update-remote-access-session-forwarding-<provider>
```

#### Common flags (all providers)

`--enable[=true]`: Enable or disable forwarding

`--output-format[=text]`: Log format (`text` or `json`)

`--pull-interval[=10]`: Pull interval in seconds

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

#### Example

```shell
akeyless gateway-update-remote-access-session-forwarding-splunk \
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

## Get Command

### `gateway-get-remote-access`

Returns the current SRA configuration for the gateway as a JSON object with four sub-objects: `global` (allowed URLs, session TTL, keyboard layout, and legacy SSH settings), `ssh_bastion` (SSH-specific settings), `web_bastion` (web access and RDP recording settings), and `desktop_app` (desktop application settings).

```shell Alias
akeyless gateway-get-remote-access
```
```shell Command group
akeyless gateway get remote-access
```

#### Key flags

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

#### Example

```shell
akeyless gateway-get-remote-access --gateway-url https://my-gw.example.com:8000
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
* [List SRA Sessions](https://docs.akeyless.io/reference/listsrasessions)
* [List SRA Bastions](https://docs.akeyless.io/reference/listsrabastions)
* For `gateway-update-remote-access-session-forwarding-<provider>` REST endpoints, see the [Akeyless API Reference](https://docs.akeyless.io/reference) and search for `gateway-update-remote-access-session-forwarding`.
