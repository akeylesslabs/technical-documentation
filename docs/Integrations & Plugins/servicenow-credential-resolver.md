---
title: ServiceNow Credential Resolver
deprecated: false
hidden: false
link:
  new_tab: false
metadata:
  robots: index
---
## Overview

The **Akeyless Credentials Resolver** is Akeyless's official ServiceNow application. It installs a MID Server external credential resolver that retrieves secrets from Akeyless at runtime and maps them to ServiceNow Discovery credential fields, so no static passwords are stored in ServiceNow. The resolver class is `com.snc.discovery.CredentialResolver`.

App listing: [https://store.servicenow.com/store/app/3bad4acf97f98f10cbe2f5411153af6a](https://store.servicenow.com/store/app/3bad4acf97f98f10cbe2f5411153af6a)

If you'd rather build the resolver JAR from source (for example, to customize it or contribute), see the source repository instead: [https://github.com/akeylesslabs/akeyless-servicenow-credential-resolver](https://github.com/akeylesslabs/akeyless-servicenow-credential-resolver). That path isn't covered here.

## Prerequisites

- A ServiceNow instance (Quebec+ recommended) with Discovery and External Credentials enabled.
- A MID Server installed and connected to your instance.
- Network access from the MID Server host to the Akeyless Gateway (default `https://api.akeyless.io`, or your private Gateway URL).
- Access to the ServiceNow Store from your instance, and permission to install/activate applications.
- An Akeyless Access ID and one of the supported authentication methods below.

## Supported Akeyless Authentication Methods

- `access_key`: Access ID + Access Key
- `aws_iam`: CloudID from AWS
- `azure_ad`: CloudID from Azure
- `gcp`: CloudID from GCP
- `universal_identity` (or alias `uid`): Access ID + UID token
- `cert` (or alias `certificate`): Access ID + client certificate and private key material

For cloud-based methods, the resolver detects a CloudID from the cloud environment the MID Server is running in (for example, an EC2 instance profile, an Azure VM managed identity, or GCP default credentials). For Universal Identity, using a **UID token file** is the preferred setup because it supports automatic token rotation without touching MID configuration (see [Automatic UID Rotation](#automatic-uid-rotation) below).

## Install the Akeyless Credentials Resolver App

1. From your ServiceNow instance, open the **ServiceNow Store** app (or navigate to it directly at the [app listing](https://store.servicenow.com/store/app/3bad4acf97f98f10cbe2f5411153af6a)) and install **Akeyless Credentials Resolver**.
2. Once installed, activate the application on your instance if it isn't activated automatically.
3. The app deploys the resolver JAR as a MID Server JAR file record. Confirm it under **MID Server → JAR files**.
4. Make sure your MID Server(s) pick up the JAR:
   - The MID will sync automatically and place the JAR in its agent lib cache.
   - If it isn't picked up, restart the MID service to force a sync (see [Restarting the MID Service](#restarting-the-mid-service) below).

Once the MID Server has the resolver JAR loaded, move on to configuring the Akeyless connection properties.

## Configure MID Properties (Akeyless Parameters)

With the MID Server set up, configure the following properties on your instance (System Properties or MID Properties). Property names are case-sensitive.

- `ext.cred.akeyless.gw_url` (string): Akeyless Gateway. Default: `https://api.akeyless.io`
- `ext.cred.akeyless.access_type` (string): One of `access_key`, `aws_iam`, `azure_ad`, `gcp`, `universal_identity`/`uid`, `cert`/`certificate`. Default: `access_key`
- `ext.cred.akeyless.access_id` (string): Your Akeyless Access ID (required)
- `ext.cred.akeyless.access_key` (string): Your Akeyless Access Key (required for `access_key` only)
- `ext.cred.akeyless.uid_token_file` (string): File path on the MID host containing the UID token, for `universal_identity`/`uid`. **Preferred**, the first non-empty line is read on each use, so an external rotation job can refresh the file's contents without a MID restart.
- `ext.cred.akeyless.uid_token` (string): Inline UID token, for `universal_identity`/`uid`. Used as a fallback only when `uid_token_file` is unset or unreadable.
- `ext.cred.akeyless.cert_data` (string): Inline certificate PEM content, for `cert`
- `ext.cred.akeyless.key_data` (string): Inline private key PEM content, for `cert`
- `ext.cred.akeyless.cert_file_name` (string): Path to the certificate PEM file on the MID host, for `cert`
- `ext.cred.akeyless.key_file_name` (string): Path to the private key PEM file on the MID host, for `cert`
- `ext.cred.akeyless.ignore_cache` (boolean `true`/`false`): For rotated secrets only, passes `ignore-cache` when fetching values. Default: `false`

Optional field mapping overrides for JSON secrets (see [Mapping](#what-to-store-in-akeyless-and-how-its-mapped) below):

- `ext.cred.akeyless.map.username` (default: `username`)
- `ext.cred.akeyless.map.password` (default: `password`)
- `ext.cred.akeyless.map.private_key` (default: `private_key`)
- `ext.cred.akeyless.map.passphrase` (default: `passphrase`)

### Environment and System Property Alternatives

The resolver also reads the following system properties or environment variables:

- `AKEYLESS_GW_URL`
- `AKEYLESS_ACCESS_TYPE`
- `AKEYLESS_ACCESS_ID` (required)
- `AKEYLESS_ACCESS_KEY` (when using `access_key`)
- `AKEYLESS_UID_TOKEN_FILE` (preferred file path, when using `universal_identity`/`uid`)
- `AKEYLESS_UID_TOKEN` (inline fallback, when using `universal_identity`/`uid`)
- `AKEYLESS_CERT_DATA` and `AKEYLESS_KEY_DATA` (inline certificate authentication)
- `AKEYLESS_CERT_FILE_NAME` and `AKEYLESS_KEY_FILE_NAME` (file-based certificate authentication)

As a fallback for any `ext.cred.*` property, an environment variable with the uppercase name and dots replaced by underscores is also read (for example, `EXT_CRED_AKEYLESS_GW_URL`). MID properties take precedence over environment/system variables.

## Configure MID `config.xml` (Secure Local Parameters)

Add sensitive Akeyless credentials to the MID's `config.xml` on each MID host:

- Linux: `/opt/agent/config.xml`
- Windows: `C:\ServiceNow\agent\config.xml`

Insert your parameters inside the `<parameters>` block:

```xml
<parameters>
    ...
    <!-- Akeyless secure credentials -->
    <parameter name="ext.cred.akeyless.gw_url" value="https://api.akeyless.io" />
    <parameter name="ext.cred.akeyless.access_type" value="access_key" />
    <parameter name="ext.cred.akeyless.access_id" value="AKEYLESS_ACCESS_ID" />
    <parameter name="ext.cred.akeyless.access_key" value="AKEYLESS_SECRET_KEY" secure="true" />

    <!-- Universal Identity example (file-based, preferred - supports automatic rotation) -->
    <!-- <parameter name="ext.cred.akeyless.access_type" value="uid" /> -->
    <!-- <parameter name="ext.cred.akeyless.uid_token_file" value="/opt/agent/creds/uid_token.txt" /> -->

    <!-- Universal Identity example (inline fallback) -->
    <!-- <parameter name="ext.cred.akeyless.uid_token" value="UID_TOKEN" secure="true" /> -->

    <!-- Certificate authentication with inline material -->
    <!-- <parameter name="ext.cred.akeyless.access_type" value="certificate" /> -->
    <!-- <parameter name="ext.cred.akeyless.cert_data" value="-----BEGIN CERTIFICATE-----...-----END CERTIFICATE-----" secure="true" /> -->
    <!-- <parameter name="ext.cred.akeyless.key_data" value="<PRIVATE_KEY_PEM_CONTENT>" secure="true" /> -->

    <!-- Certificate authentication with file-based material -->
    <!-- <parameter name="ext.cred.akeyless.cert_file_name" value="/opt/agent/certs/client.crt" /> -->
    <!-- <parameter name="ext.cred.akeyless.key_file_name" value="/opt/agent/certs/client.key" secure="true" /> -->

    <!-- Optional JSON mapping overrides -->
    <parameter name="ext.cred.akeyless.map.username" value="username" />
    <parameter name="ext.cred.akeyless.map.password" value="password" />
    <parameter name="ext.cred.akeyless.map.private_key" value="private_key" />
    <parameter name="ext.cred.akeyless.map.passphrase" value="passphrase" />
</parameters>
```

### Restarting the MID Service

```bash
sudo service mid restart
```

Or on Windows (from an elevated Command Prompt):

```bat
net stop mid
net start mid
```

## Automatic UID Rotation

When using `universal_identity`/`uid`, prefer `ext.cred.akeyless.uid_token_file` (or `AKEYLESS_UID_TOKEN_FILE`) over the inline `uid_token` property:

- The resolver reads the first non-empty line of the file on each use, so a fresh token only needs to be written to that path — no MID property update or restart is required.
- Point the property at a file that an external rotation job keeps up to date (for example, an Akeyless Universal Identity auto-rotation job/scheduled task that periodically calls token rotation and writes the refreshed token to disk).
- The inline `ext.cred.akeyless.uid_token`/`AKEYLESS_UID_TOKEN` value is only used as a fallback if the file is unset or unreadable, so keep it out of your configuration once the file-based setup is working.
- The resolver caches the Akeyless session token in memory for the life of the MID Server's JVM and only re-authenticates when Akeyless returns an authentication failure (HTTP 401), at which point it clears the cache, re-reads the current UID token, and retries once. There's no separate configurable TTL on the resolver side — token freshness comes from keeping the token file itself current.

## Configure a Discovery Credential to Use This Resolver

1. Navigate to **Discovery → Credentials → New**.
2. Choose a credential Type (for example, Windows, SSH Password, SSH Private Key, VMware, JDBC, JMS, or SNMPv3).
3. Select **External credential store**.
4. Set the fully qualified class name (FQCN) to `com.snc.discovery.CredentialResolver`.
5. Set the Credential ID to the Akeyless secret path (for example, `/prod/app/db`).
6. Click **Test credential**, then select a MID Server and a target if required by the type.

## What to Store in Akeyless and How It's Mapped

The resolver accepts either:

- A plain string secret, mapped as a password/token
- A JSON object, where fields are mapped to ServiceNow credential fields per the credential Type

### Item Types (Static, Rotated, Dynamic)

- The resolver first calls `describe-item` to determine `item_type`.
- Based on `item_type`, it then calls:
  - `STATIC_SECRET` → `get-secret-value`
  - `ROTATED_SECRET` → `get-rotated-secret-value` (also sends `ignore-cache` when `ext.cred.akeyless.ignore_cache=true`)
  - `DYNAMIC_SECRET` → `get-dynamic-secret-value`
- If ServiceNow provides an `ip` argument for the credential test or run, the resolver passes it as `host` when fetching rotated secrets.

Default mapping (can be overridden by way of `ext.cred.akeyless.map.*`):

- Username field: `username`
- Password field: `password`
- Private key field: `private_key`
- Passphrase field: `passphrase`

### Per-Type Mapping Summary

- Windows, Basic, SSH Password, VMware, JDBC, JMS: uses JSON fields `username`, `password` (or your overridden names).
- SSH Private Key: uses JSON fields `username`, `private_key`, `passphrase`. The same mapping applies to `sn_cfg_ansible`, `sn_disco_certmgmt_certificate_ca`, `cfg_chef_credentials`, `infoblox`, and `api_key`.
- SNMPv3: uses JSON fields `username`, `auth_protocol`, `auth_key`, `privacy_protocol`, `privacy_key`, mapped to ServiceNow fields `username`, `auth-protocol`, `auth-key`, `privacy-protocol`, `privacy-key`.
- Other unlisted types: the resolver attempts to map `username` and `password` when those fields are present in the secret JSON; if one or both are missing, only the available fields are mapped.

### Examples

Basic / Windows / SSH Password (JSON in Akeyless):

```json
{
  "username": "alice",
  "password": "secret"
}
```

SSH Private Key:

```json
{
  "username": "ssh-user",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "passphrase": "optional"
}
```

SNMPv3:

```json
{
  "username": "snmpu",
  "auth_protocol": "SHA",
  "auth_key": "authKeyHere",
  "privacy_protocol": "AES",
  "privacy_key": "privacyKeyHere"
}
```

Custom field names by way of mapping overrides (example): set `ext.cred.akeyless.map.username = user_name` and `ext.cred.akeyless.map.password = pwd`. A JSON secret like:

```json
{
  "user_name": "alice",
  "pwd": "secret"
}
```

will then map to ServiceNow `username = alice`, `password = secret`.

## CloudID Notes (aws\_iam / azure\_ad / gcp)

- When `ext.cred.akeyless.access_type` (or `AKEYLESS_ACCESS_TYPE`) is `aws_iam`, `azure_ad`, or `gcp`, the resolver fetches a CloudID and sends it to Akeyless during authentication.
- Ensure the MID Server host is running in the target cloud with the appropriate identity, or that the cloud SDK environment is present to retrieve a CloudID.
- Do not set `access_key` when using CloudID-based methods.

## Certificate Authentication Notes

- When `ext.cred.akeyless.access_type` is `cert` or `certificate`, provide both the certificate and private key.
- Certificate authentication supports either inline material with `ext.cred.akeyless.cert_data` and `ext.cred.akeyless.key_data`, or file paths with `ext.cred.akeyless.cert_file_name` and `ext.cred.akeyless.key_file_name`.
- The resolver base64-encodes certificate and key material before sending it to Akeyless.

## Troubleshooting

- **HTTP 400 "Missing required parameter - timestamp" on&#x20;**`/auth`: Usually indicates the wrong auth flow or missing parameters. Verify `access_type` is set correctly. For CloudID flows, do not set an `access_key`. For `access_key` flows, ensure both `access_id` and `access_key` are set. For `uid`, set `uid_token_file` (preferred) or `uid_token` (fallback). For `cert`, provide both certificate and key material, either inline or by file path.
- **HTTP 404 from&#x20;**`/v2/*`**&#x20;endpoints**: The resolver automatically falls back to the non-`/v2` endpoints. If both fail, verify the Gateway URL and network reachability.
- **"Secret value not found for name ..."**: Confirm the Credential ID (secret path) is correct and the Akeyless identity has permission to read it.
- **Everything maps to a single password field (**`pswd`**)**: This usually happens when the secret isn't strict JSON, because PEM or key content was pasted with literal line breaks inside quoted strings. Prefer `\n` inside the JSON string values. If PEM markers are still present, the resolver retries parsing with a lenient Jackson mode.
- **Logging**: Resolver logs go through Commons Logging — check MID Server logs for entries containing "Akeyless resolver". The resolver also writes its own daily-rotated log files under the MID agent `logs/` folder (for example, `/opt/agent/logs/akeyless-resolver-YYYY-MM-DD.log` on Linux, or `C:\ServiceNow\agent\logs\akeyless-resolver-YYYY-MM-DD.log` on Windows). These file logs contain the same safe diagnostic messages as the MID logs (arguments, secret path, item type, resolved field keys) — secret values and tokens are never written to the file.

<br />
