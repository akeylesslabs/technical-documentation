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

## Command Group

Gateway SRA update commands are available under the `gateway update` command group and by alias commands.

Examples:

```shell
akeyless gateway update remote-access
```
```shell
akeyless gateway-update-remote-access
```

## Core SRA Commands

### `gateway-update-remote-access`

Updates core SRA configuration.

#### Alias command

```shell
akeyless gateway-update-remote-access
```

#### Command-group form

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

### `gateway-update-remote-access-rdp-recording`

Updates RDP recording configuration for SRA.

#### Alias command

```shell
akeyless gateway-update-remote-access-rdp-recording
```

#### Command-group form

```shell
akeyless gateway update remote-access-rdp-recording
```

#### Key flags

`--rdp-session-recording`: Required. Enable or disable RDP recording (`true` or `false`)

`--rdp-session-storage`: Required when recording is enabled. Supported values: `local`, `aws`, `azure`

`--rdp-session-recording-quality[=medium]`: Recording quality (`low`, `medium`, `high`)

`--rdp-session-recording-compress`: Compress recordings before upload

`--rdp-session-recording-encryption-key`: Encryption key item name for uploaded recordings

`--aws-storage-*`: AWS storage settings

`--azure-storage-*`: Azure storage settings

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

### `gateway-update-remote-access-desktop-app`

Updates desktop application settings used by SRA.

#### Alias command

```shell
akeyless gateway-update-remote-access-desktop-app
```

#### Command-group form

```shell
akeyless gateway update remote-access-desktop-app
```

#### Key flags

`--desktop-app-ssh-cert-issuer`: Default SSH certificate issuer name (resolved to issuer ID)

`--desktop-app-secure-web-access-url`: Secure web access URL for desktop application

`--desktop-app-secure-web-proxy`: Secure web proxy URL for desktop application

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

### `gateway-update-remote-access-session-forwarding-<provider>`

Updates SRA session log forwarding configuration for a specific provider.

#### Base command-group form

```shell
akeyless gateway update remote-access-session-forwarding <provider>
```

#### Alias form

```shell
akeyless gateway-update-remote-access-session-forwarding-<provider>
```

#### Supported providers

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

#### Common flags (all providers)

`--enable[=true]`: Enable or disable forwarding

`--output-format[=text]`: Log format (`text` or `json`)

`--pull-interval[=10]`: Pull interval in seconds

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

#### Provider flags

`aws-s3`

`--bucket-name`: Target S3 bucket name

`--auth-type`: AWS auth type (`access_key`, `cloud_id`, `assume_role`)

`--region`: AWS region

`--log-folder[=use-existing]`: Destination folder in the S3 bucket

`--access-id`: Required when `--auth-type access_key`

`--access-key`: Required when `--auth-type access_key`

`--role-arn`: Required when `--auth-type assume_role`

`azure-analytics`

`--workspace-id`: Azure workspace ID

`--workspace-key`: Azure workspace key

`--enable-batch[=true]`: Enable or disable batch forwarding

`datadog`

`--host`: Datadog host

`--api-key`: Datadog API key

`--log-source[=use-existing]`: Datadog source field

`--log-tags[=use-existing]`: Comma-separated tags (`key:value`)

`--log-service[=use-existing]`: Datadog service field

`elasticsearch`

`--index`: Elasticsearch index

`--server-type`: Server type (`nodes` or `cloud`)

`--auth-type`: Auth type (`api_key` or `password`)

`--nodes`: Required when `--server-type nodes`

`--cloud-id`: Required when `--server-type cloud`

`--api-key`: Required when `--auth-type api_key`

`--user-name`: Required when `--auth-type password`

`--password`: Required when `--auth-type password`

`--enable-tls`: Enable or disable TLS

`--certificate-file`: Path to a PEM certificate file

`--tls-certificate[=use-existing]`: Base64 PEM certificate value

`google-chronicle`

`--customer-id`: Google Chronicle customer ID

`--region`: Region (`eu_multi_region`, `london`, `us_multi_region`, `singapore`, `tel_aviv`)

`--log-type`: Chronicle log type

`--gcp-key-file-path`: Path to a GCP service-account private key file

`--gcp-key`: Base64-encoded GCP service-account private key text

`logstash`

`--dns`: Logstash DNS or host endpoint

`--protocol`: Protocol (`tcp` or `udp`)

`--enable-tls`: Enable or disable TLS

`--certificate-file`: Path to a PEM certificate file

`--tls-certificate[=use-existing]`: Base64 PEM certificate value

`logz-io`

`--logz-io-token`: Logz.io token

`--protocol`: Protocol (`tcp` or `https`)

`splunk`

`--splunk-url`: Splunk server URL

`--splunk-token`: Splunk token

`--index`: Splunk index

`--source[=use-existing]`: Splunk source

`--source-type[=use-existing]`: Splunk source type

`--enable-batch[=true]`: Enable or disable batch forwarding

`--enable-tls`: Enable or disable TLS

`--certificate-file`: Path to a PEM certificate file

`--tls-certificate[=use-existing]`: Base64 PEM certificate value

`stdout`

No provider-specific flags.

`sumologic`

`--endpoint`: Sumo Logic endpoint URL

`--sumologic-tags[=use-existing]`: Comma-separated Sumo Logic tags

`--host[=use-existing]`: Sumo Logic host

`syslog`

`--host`: Syslog host

`--network[=tcp]`: Network (`tcp` or `udp`)

`--formatter[=text]`: Formatter (`text` or `cef`)

`--target-tag[=use-existing]`: Syslog target tag

`--enable-tls`: Enable or disable TLS (TCP only)

`--certificate-file`: Path to a PEM certificate file

`--tls-certificate[=use-existing]`: Base64 PEM certificate value

## Session and Bastion Inventory Commands

The following commands are top-level CLI commands and are not under `gateway update`.

### `list-sra-sessions`

Lists SRA sessions for the calling user.

#### Usage

```shell
akeyless list-sra-sessions
```

#### Key flags

`--status-type`: Session status types. If omitted, defaults to active statuses only (`connecting`, `connected`)

`--resource-type`: Connection type filter, for example `ssh`, `k8s`, `mysql`, `rdp`

#### Behavior notes

By default, this command is own-only scoped in the command implementation.

### `list-sra-bastions`

Lists SRA bastions.

#### Usage

```shell
akeyless list-sra-bastions
```

#### Key flags

`--allowed-urls-only[=false]`: Show only bastion allowed URL configuration

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
