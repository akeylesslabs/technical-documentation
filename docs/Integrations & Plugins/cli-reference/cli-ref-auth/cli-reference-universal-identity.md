---
title: CLI Reference - Universal Identity
excerpt: Akeyless Universal Identity Auth Method
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
This section outlines the CLI commands relevant to Universal Identity authentication.

<CLIGeneralFlags />

## `create`

Create a new Auth Method that can authenticate using Akeyless Universal Identity

### Usage

```shell
akeyless auth-method create universal-identity \
--name <Auth method name> \
--ttl <Token TTL>
```

### Flags

`-n, --name`: **Required** Auth Method name

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--deny-rotate`: Deny from the token to rotate

`--deny-inheritance`: Deny from root to create children

`--ttl[=60]`: Token TTL (has the value that configured in Akeyless Console > Authentication settings)

## `uid-auto-rotate`

Configure automatic UID token rotation

### Usage

```shell
akeyless uid-auto-rotate <init|rotate|status|uninstall>
```

The `init` subcommand initializes rotation and stores the token file. The `rotate`, `status`, and `uninstall` subcommands use the stored token file and the configured gateway URL.

### `init`

Initialize automatic UID token rotation.
Accepted alias: `uid-auto-rotate-init`.

#### Usage

```shell
akeyless uid-auto-rotate init \
--rotation-interval <1|15|60|240|1440> \
--uid-token <UID Token>
```

#### Flags

`-t, --uid-token`: Optional. Universal Identity token. If omitted, use the `AKEYLESS_UID_TOKEN` environment variable.

`--rotation-interval`: **Required** for `init`. Rotation interval in minutes. Supported values: `1`, `15`, `60`, `240`, `1440`.

`-i, --token-file-path`: Optional. Path to store the rotated UID token file. If omitted, Akeyless uses `~/.akeyless/uid_rotator/uid-token` on Unix-like systems or `PROGRAMDATA\akeyless\uid_rotator\uid-token` on Windows.

`--gateway-api-url`: Optional. Gateway URL for rotation requests. If omitted, Akeyless uses the configured `AKEYLESS_GATEWAY_URL` value.

`--scheduling-mode[=cron]`: Scheduler mode. Supported values: `cron`, `systemd`, `windows-task`.

`--cron-mode[=user]`: Cron installation mode when `--scheduling-mode=cron`. Supported values: `user`, `system`.

### `rotate`

Rotate the current UID token on demand.
Accepted alias: `uid-auto-rotate-rotate`.

#### Usage

```shell
akeyless uid-auto-rotate rotate
```

#### Flags

`-i, --token-file-path`: Optional. Path to the rotated UID token file. If omitted, Akeyless uses `~/.akeyless/uid_rotator/uid-token` on Unix-like systems or `PROGRAMDATA\akeyless\uid_rotator\uid-token` on Windows.

`--gateway-api-url`: Optional. Gateway URL for rotation requests. If omitted, Akeyless uses the configured `AKEYLESS_GATEWAY_URL` value.

### `status`

Check the current UID auto-rotate setup.
Accepted alias: `uid-auto-rotate-status`.

#### Usage

```shell
akeyless uid-auto-rotate status
```

#### Flags

`-i, --token-file-path`: Optional. Path to the rotated UID token file. If omitted, Akeyless uses `~/.akeyless/uid_rotator/uid-token` on Unix-like systems or `PROGRAMDATA\akeyless\uid_rotator\uid-token` on Windows.

### `uninstall`

Remove the UID auto-rotate setup and scheduled entry.
Accepted alias: `uid-auto-rotate-uninstall`.

#### Usage

```shell
akeyless uid-auto-rotate uninstall
```

#### Flags

`-i, --token-file-path`: Optional. Path to the rotated UID token file. If omitted, Akeyless uses `~/.akeyless/uid_rotator/uid-token` on Unix-like systems or `PROGRAMDATA\akeyless\uid_rotator\uid-token` on Windows.

## `uid-create-child-token`

Create a new child token using Akeyless Universal Identity

### Usage

```shell
akeyless uid-create-child-token \
--child-deny-rotate \
--child-deny-inheritance
```

### Flags

`--child-deny-rotate`: Deny from new child to rotate

`--child-deny-inheritance`: Deny from new child to create their own children

`--child-ttl`: New child token TTL

`-n, --auth-method-name`: The universal identity Auth Method name, required only when uid-token is not provided

`--tid, --uid-token-id`: The ID of the uid-token, required only when uid-token is not provided

`--profile` or `--token`: Use a specific Akeyless profile (located at `$HOME/.akeyless/profiles`) or a temporary access token

`--uid-token`: The universal identity token. It is required only for universal_identity authentication

## `uid-generate-token`

Generate a new token using Akeyless Universal Identity

### Usage

```shell
akeyless uid-generate-token --auth-method-name <Auth method name>
```

## `uid-list-children`

List the token children ids of Akeyless Universal Identity

### Usage

```shell
akeyless uid-list-children --auth-method-name <UID Auth Method Name>
```

## `uid-revoke-token`

Revoke token using Akeyless Universal Identity

### Usage

```shell
akeyless uid-revoke-token \
--revoke-type <revokeSelf/revokeAll> \
--revoke-token <UID Token ID> \
--auth-method-name <UID Name>
```

### Flags

`-r, --revoke-type`: **Required**, revokeSelf/revokeAll (delete only this token/this token and his children)

`-t, --revoke-token`: **Required**, the universal identity token ID to revoke

`-n, --auth-method-name`: **Required**, the universal identity Auth Method name

## `uid-rotate-token`

Rotate Akeyless Universal Identity token
Accepted aliases: `rotate-token`, `uid-send-manual-rotate-ack`.

### Flags

`-t, --token, --uid-token`: The Universal identity token to rotate

`--fork`: Create a new child token with default Flags

`--send-manual-ack-token`: The new rotated token to send manual ack for (with uid-token=the-orig-token)

`--with-manual-ack`: Disable automatic ack

`-o, --output-file`: Path to the output file

`-i, --input-file`: Path to the input file

## `update`

Update a new Auth Method that can authenticate using Akeyless Universal Identity

### Usage

```shell
akeyless auth-method update universal-identity \
--name <Auth method name> \
--new-name <Auth method new name>
```

### Flags

`--new-name`: Auth Method new name

`-n, --name`: **Required**, Auth Method name

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--deny-rotate`: Deny from the token to rotate

`--deny-inheritance`: Deny from root to create children

`--ttl[=60]`: Token TTL (in minutes)
