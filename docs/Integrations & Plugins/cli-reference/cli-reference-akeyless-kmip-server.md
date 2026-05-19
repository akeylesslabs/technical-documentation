---
title: CLI Reference - KMIP
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
This page documents Key Management Interoperability Protocol (KMIP) commands in the Akeyless CLI.

<CLIGeneralFlags />

## Command Groups

KMIP commands are grouped by lifecycle:

* **Environment lifecycle**: Create, inspect, update, move, renew, enable or disable, and delete a KMIP server environment.
* **Client lifecycle**: Create, inspect, update, renew, and delete KMIP clients.
* **Authorization lifecycle**: Add and remove KMIP client RBAC rules.

> ℹ️ **Note (CLI and API operation names):**
>
> `kmip-server-update` and `kmip-client-update` are valid CLI commands and also appear in REST API schemas. Use update commands to manage certificate expiration-event settings. Use renew commands to issue new certificates.

## Environment Lifecycle Commands

### `kmip-server-setup`

Create a new KMIP server environment.

#### Usage

```shell
akeyless kmip-server-setup \
--hostname <KMIP_SERVER_HOSTNAME> \
--certificate-ttl <CERTIFICATE_TTL_DAYS> \
--root <KMIP_ROOT_PATH> \
--gateway-url <GATEWAY_URL>:8000
```

#### Flags

`-n, --hostname`: **Required**, hostname of this KMIP server

`-t, --certificate-ttl[=90]`: server certificate TTL in days

`-r, --root`: **Required**, root path for KMIP objects

`-p, --output-file-folder`: folder path where the CA certificate file is saved (for example, `.`). A new `ca.cert` file is created in this folder.

`-e, --expiration-event-in`: number of days before certificate expiration to notify. Repeat the flag to set multiple events (for example, `--expiration-event-in 1 --expiration-event-in 5`).

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `kmip-describe-server`

Show KMIP server environment details.

#### Usage

```shell
akeyless kmip-describe-server \
--gateway-url <GATEWAY_URL>:8000
```

#### Flags

`-u, --gateway-url[=http://localhost:8000]`: gateway URL (Configuration Management port)

### `kmip-server-update`

Update KMIP server configuration.

#### Usage

```shell
akeyless kmip-server-update \
--expiration-event-in <DAYS_BEFORE_EXPIRATION> \
--gateway-url <GATEWAY_URL>:8000
```

#### Flags

`-e, --expiration-event-in`: number of days before certificate expiration to notify. Repeat the flag to set multiple events (for example, `--expiration-event-in 1 --expiration-event-in 5`).

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `kmip-server-move`

Move the KMIP environment root and associated items to a new root path.

#### Usage

```shell
akeyless kmip-server-move \
--new-root <NEW_KMIP_ROOT_PATH> \
--gateway-url <GATEWAY_URL>:8000
```

#### Flags

`-n, --new-root`: **Required**, new root path for the KMIP environment

`-u, --gateway-url[=http://localhost:8000]`: gateway URL (Configuration Management port)

### `kmip-renew-server-certificate`

Renew the KMIP server certificate.

#### Usage

```shell
akeyless kmip-renew-server-certificate \
--gateway-url <GATEWAY_URL>:8000
```

#### Flags

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `kmip-set-server-state`

Set the KMIP server state to `enabled` or `disabled`.

#### Usage

```shell
akeyless kmip-set-server-state \
--state <enabled|disabled> \
--gateway-url <GATEWAY_URL>:8000
```

#### Flags

`-s, --state`: **Required**, server state (`enabled` or `disabled`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `kmip-server-delete`

Delete the KMIP server environment. Deletion is allowed only when no clients or associated items remain.

#### Usage

```shell
akeyless kmip-server-delete \
--gateway-url <GATEWAY_URL>:8000
```

#### Flags

`-u, --gateway-url[=http://localhost:8000]`: gateway URL (Configuration Management port)

## Client Lifecycle Commands

### `kmip-create-client`

Create a new KMIP client.

#### Usage

```shell
akeyless kmip-create-client \
--name <KMIP_CLIENT_NAME> \
--certificate-ttl <CERTIFICATE_TTL_DAYS> \
--gateway-url <GATEWAY_URL>:8000
```

#### Flags

`-n, --name`: **Required**, KMIP client name

`-t, --certificate-ttl[=90]`: client certificate TTL in days

`-p, --output-file-folder`: folder path where client certificate files are saved (for example, `.`). Two files are created: `<client-name>.key` and `<client-name>.cert`.

`-a, --activate-keys-on-creation[=false]`: if set to `true`, newly created keys on this client are set to `active`

`-e, --expiration-event-in`: number of days before certificate expiration to notify. Repeat the flag to set multiple events (for example, `--expiration-event-in 1 --expiration-event-in 5`).

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `kmip-describe-client`

Show KMIP client details.

#### Usage

```shell
akeyless kmip-describe-client \
--name <KMIP_CLIENT_NAME> \
--gateway-url <GATEWAY_URL>:8000
```

Use `--client-id <KMIP_CLIENT_ID>` instead of `--name` when needed.

#### Flags

`-n, --name`: KMIP client name (either `name` or `client-id` is required)

`-i, --client-id`: KMIP client ID (either `name` or `client-id` is required)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `kmip-client-update`

Update KMIP client configuration.

#### Usage

```shell
akeyless kmip-client-update \
--name <KMIP_CLIENT_NAME> \
--expiration-event-in <DAYS_BEFORE_EXPIRATION> \
--gateway-url <GATEWAY_URL>:8000
```

Use `--client-id <KMIP_CLIENT_ID>` instead of `--name` when needed.

#### Flags

`-n, --name`: KMIP client name (either `name` or `client-id` is required)

`-i, --client-id`: KMIP client ID (either `name` or `client-id` is required)

`-e, --expiration-event-in`: number of days before certificate expiration to notify. Repeat the flag to set multiple events (for example, `--expiration-event-in 1 --expiration-event-in 5`).

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `kmip-list-clients`

List existing KMIP clients.

#### Usage

```shell
akeyless kmip-list-clients \
--gateway-url <GATEWAY_URL>:8000
```

#### Flags

`-u, --gateway-url[=http://localhost:8000]`: gateway URL (Configuration Management port)

### `kmip-renew-client-certificate`

Renew a KMIP client certificate.

#### Usage

```shell
akeyless kmip-renew-client-certificate \
--name <KMIP_CLIENT_NAME> \
--output-file-folder <OUTPUT_FOLDER> \
--gateway-url <GATEWAY_URL>:8000
```

Use `--client-id <KMIP_CLIENT_ID>` instead of `--name` when needed.

#### Flags

`-n, --name`: KMIP client name (either `name` or `client-id` is required)

`-i, --client-id`: KMIP client ID (either `name` or `client-id` is required)

`-p, --output-file-folder`: folder path where client certificate files are saved (for example, `.`). Two files are created: `<client-name>.key` and `<client-name>.cert`.

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `kmip-delete-client`

Delete a KMIP client.

#### Usage

```shell
akeyless kmip-delete-client \
--name <KMIP_CLIENT_NAME> \
--gateway-url <GATEWAY_URL>:8000
```

Use `--client-id <KMIP_CLIENT_ID>` instead of `--name` when needed.

#### Flags

`-n, --name`: KMIP client name (either `name` or `client-id` is required)

`-i, --client-id`: KMIP client ID (either `name` or `client-id` is required)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

## Authorization Commands

### `kmip-client-delete-rule`

Delete an RBAC rule from a KMIP client.

#### Usage

```shell
akeyless kmip-client-delete-rule \
--path <ACCESS_PATH> \
--name <KMIP_CLIENT_NAME> \
--gateway-url <GATEWAY_URL>:8000
```

Use `--client-id <KMIP_CLIENT_ID>` instead of `--name` when needed.

#### Flags

`-p, --path`: **Required**, access path (for example, `/*` or `/some-key`)

`-n, --name`: KMIP client name (either `name` or `client-id` is required)

`-i, --client-id`: KMIP client ID (either `name` or `client-id` is required)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `kmip-client-set-rule`

Add an RBAC rule to a KMIP client.

Supported capabilities:
`DENY`
`CREATE`
`REGISTER`
`REKEY`
`LOCATE`
`GET`
`GET_ATTRIBUTES`
`ACTIVATE`
`REVOKE`
`DESTROY`

#### Usage

```shell
akeyless kmip-client-set-rule \
--path <ACCESS_PATH> \
--capability <ACCESS_CAPABILITY> \
--name <KMIP_CLIENT_NAME> \
--gateway-url <GATEWAY_URL>:8000
```

Use `--client-id <KMIP_CLIENT_ID>` instead of `--name` when needed.

#### Flags

`-p, --path`: **Required**, access path (for example, `/*` or `/some-key`)

`-c, --capability`: **Required**, access capability (see supported values above)

`-n, --name`: KMIP client name (either `name` or `client-id` is required)

`-i, --client-id`: KMIP client ID (either `name` or `client-id` is required)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

> ℹ️ **Info (Writing commands - generating secrets):**
>
> The default Akeyless Vault behavior is that the write commands (generate secrets) are performed in the main region of Akeyless Vault, while the read commands (fetch secrets) are performed in the nearest region to you to minimize latency.
> If you wish to change that and work only with the main region, please add
> `optimize_dns_disable=true` in the settings file.
