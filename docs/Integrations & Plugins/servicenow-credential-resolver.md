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

This project provides a ServiceNow MID external credential resolver that retrieves secrets from Akeyless and maps them to ServiceNow Discovery credential fields. The resolver class is com.snc.discovery.CredentialResolver.

## Prerequisites

* ServiceNow instance (Quebec+ recommended) with Discovery and External Credentials enabled.
* MID Server installed and connected to your instance.
* Network access from the MID Server host to the Akeyless Gateway (default `https://api.akeyless.io`, or your private gateway URL).
* An Akeyless Access ID and one of the supported authentication methods listed below.

## Supported Akeyless Authentication Methods

* `access_key`: Access ID + Access Key
* `aws_iam`: CloudID from AWS
* `azure_ad`: CloudID from Azure
* `gcp`: CloudID from GCP
* `universal_identity` (or alias `uid`): Access ID + UID token
* `cert` (or alias `certificate`): Access ID + client certificate and private key material

For cloud-based methods, the resolver detects CloudID using the cloud environment. Ensure the MID Server is running where a CloudID can be obtained (For example, EC2 with an instance profile, Azure VM with a managed identity, GCP VM with default credentials). For local/dev use, prefer access_key.

## Build the JAR

This is a Maven project. Build a versioned JAR so the filename is stable in MID:

```shell
mvn -Drevision=1.0.0 clean package
```

### Artifacts

* With `-Drevision=1.0.0: target/akeyless-servicenow-credential-resolver-1.0.0.jar`
    * [https://repo1.maven.org/maven2/io/akeyless/akeyless-servicenow-credential-resolver/1.0.0/akeyless-servicenow-credential-resolver-1.0.0.jar](https://repo1.maven.org/maven2/io/akeyless/akeyless-servicenow-credential-resolver/1.0.0/akeyless-servicenow-credential-resolver-1.0.0.jar)

## Install the Resolver on the MID Server

1. Upload the JAR to the MID Server by way of the instance UI
   * Navigate: MID Server → JAR files → New
   * Set a descriptive Name (For example, akeyless-servicenow-credential-resolver)
   * Manage Attachments → upload the built JAR from target/
   * Submit
2. Ensure the MID downloads the JAR

* The MID will sync and place the JAR in its agent lib cache.
* If not picked up, restart the MID service to force a sync.

## Configure MID Properties (Akeyless Parameters)

Set the following MID properties on your instance (System Properties or MID Properties). Property names are case-sensitive.

* `ext.cred.akeyless.gw_url` (string): Akeyless Gateway. Default: `https://api.akeyless.io`
* `ext.cred.akeyless.access_type` (string): One of `access_key`, `aws_iam`, `azure_ad`, `gcp`, `universal_identity` or `uid`, `cert` or `certificate`. Default: `access_key`
* `ext.cred.akeyless.access_id` (string): Your Akeyless Access ID (required)
* `ext.cred.akeyless.access_key` (string): Your Akeyless Access Key (required for `access_key` only)
* `ext.cred.akeyless.uid_token` (string): Required for `universal_identity` or `uid`
* `ext.cred.akeyless.cert_data` (string): Inline certificate PEM content for `cert`
* `ext.cred.akeyless.key_data` (string): Inline private key PEM content for `cert`
* `ext.cred.akeyless.cert_file_name` (string): Path to the certificate PEM file on the MID host for `cert`
* `ext.cred.akeyless.key_file_name` (string): Path to the private key PEM file on the MID host for `cert`

Optional field mapping overrides for JSON secrets (see Mapping section below):

* `ext.cred.akeyless.map.username` (default: `username`)
* `ext.cred.akeyless.map.password` (default: `password`)
* `ext.cred.akeyless.map.private_key` (default: `private_key`)
* `ext.cred.akeyless.map.passphrase` (default: `passphrase`)

Environment/system property alternatives

* The resolver also supports the following system properties or environment variables:
    * `AKEYLESS_GW_URL`
    * `AKEYLESS_ACCESS_TYPE`
    * `AKEYLESS_ACCESS_ID` (required)
    * `AKEYLESS_ACCESS_KEY` (when using `access_key`)
    * `AKEYLESS_UID_TOKEN` (when using `universal_identity` or `uid`)
    * `AKEYLESS_CERT_DATA` and `AKEYLESS_KEY_DATA` (inline certificate authentication)
    * `AKEYLESS_CERT_FILE_NAME` and `AKEYLESS_KEY_FILE_NAME` (file-based certificate authentication)
* As a fallback for any `ext.cred.*` property, an environment variable with the uppercase name and dots replaced by underscores is also read (for example, `EXT_CRED_AKEYLESS_GW_URL`).
* Precedence: MID properties override environment/system variables.

## Configure MID `config.xml` (Secure Local Parameters)

Add sensitive Akeyless credentials in the MID’s `config.xml`.

Edit the file on each MID host:

* Linux: `/opt/agent/config.xml`
* Windows: `C:\ServiceNow\agent\config.xml`

Insert your parameters inside the `<parameters>` block:

```xml
<parameters>
    ...
    <!-- Akeyless secure credentials -->
    <parameter name="ext.cred.akeyless.gw_url" value="https://api.akeyless.io" />
    <parameter name="ext.cred.akeyless.access_type" value="access_key" />
    <parameter name="ext.cred.akeyless.access_id" value="AKEYLESS_ACCESS_ID" />
    <parameter name="ext.cred.akeyless.access_key" value="AKEYLESS_SECRET_KEY" secure="true" />

  <!-- Universal Identity example -->
  <!-- <parameter name="ext.cred.akeyless.access_type" value="uid" /> -->
  <!-- <parameter name="ext.cred.akeyless.uid_token" value="UID_TOKEN" secure="true" /> -->

  <!-- Certificate authentication with inline material -->
  <!-- <parameter name="ext.cred.akeyless.access_type" value="certificate" /> -->
  <!-- <parameter name="ext.cred.akeyless.cert_data" value="-----BEGIN CERTIFICATE-----...-----END CERTIFICATE-----" secure="true" /> -->
  <!-- <parameter name="ext.cred.akeyless.key_data" value="-----BEGIN PRIVATE KEY-----...-----END PRIVATE KEY-----" secure="true" /> -->

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

Then restart the MID service:

```shell
sudo service mid restart
```

Or on Windows (from an elevated Command Prompt):

```shell
net stop mid
net start mid
```

## Configure a Discovery Credential to Use This Resolver

1. Create a new credential
   * Navigate: Discovery → Credentials → New
   * Choose a credential Type (For example, Windows, SSH Password, SSH Private Key, VMware, JDBC, JMS, SNMPv3)
   * Select “External credential store”
   * Fully Qualified Class Name (FQCN): com.snc.discovery.CredentialResolver
   * Credential ID: The Akeyless secret path (For example, /prod/app/db) to fetch
2. Save and test
   * Click “Test credential”, select a MID Server and a target if required by the type.

## What to Store in Akeyless and How It’s Mapped

The resolver accepts either:

* A plain string secret → mapped as a password/token
* A JSON object → fields are mapped to ServiceNow credential fields as per the credential Type

Default mapping (can be overridden by way of `ext.cred.akeyless.map.*`):

* Username field: `username`
* Password field: `password`
* Private key field: `private_key`
* Passphrase field: `passphrase`

Per-Type mapping summary

<!-- cspell:ignore certmgmt infoblox authprotocol authkey privprotocol privkey pswd -->

* Windows, Basic, SSH Password, VMware, JDBC, JMS:
    * Uses JSON fields: username, password (or your overridden names)
* SSH Private Key:
    * Uses JSON fields: username, private_key, passphrase
    * The same mapping also applies to `sn_cfg_ansible`, `sn_disco_certmgmt_certificate_ca`, `cfg_chef_credentials`, `infoblox`, and `api_key`.
* SNMPv3:
    * Uses JSON fields: username, auth_protocol, auth_key, privacy_protocol, privacy_key
    * Mapped to ServiceNow fields: `user`, `authprotocol`, `authkey`, `privprotocol`, `privkey`
* Other unlisted types:
    * Best-effort: username and password if present

Examples

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

Custom field names by way of mapping overrides (example):

* Set `ext.cred.akeyless.map.username = user_name`
* Set `ext.cred.akeyless.map.password = pwd`

Then a JSON like:

```json
{
  "user_name": "alice",
  "pwd": "secret"
}
```

will map to ServiceNow user = alice, pswd = secret.

## CloudID Notes (Aws_iam / Azure_ad / Gcp)

* When ext.cred.akeyless.access_type (or AKEYLESS_ACCESS_TYPE) is aws_iam, azure_ad, or gcp, the resolver fetches a CloudID and sends it to Akeyless during auth.
* Ensure the MID Server host is running in the target cloud with the appropriate identity, or that cloud SDK environment is present to retrieve a CloudID.
* Do not set access_key when using CloudID-based methods.

## Universal Identity and Certificate Authentication Notes

* When `ext.cred.akeyless.access_type` is `universal_identity` or `uid`, set `ext.cred.akeyless.uid_token` or `AKEYLESS_UID_TOKEN`.
* When `ext.cred.akeyless.access_type` is `cert` or `certificate`, provide both the certificate and private key.
* Certificate authentication supports either inline material with `ext.cred.akeyless.cert_data` and `ext.cred.akeyless.key_data`, or file paths with `ext.cred.akeyless.cert_file_name` and `ext.cred.akeyless.key_file_name`.
* The resolver base64-encodes certificate and key material before sending it to Akeyless.

## Troubleshooting

* HTTP 400 “Missing required parameter - timestamp” on /auth:
    * Usually indicates the wrong auth flow or missing parameters. Verify access_type is set correctly. For CloudID flows, do not set an access_key. For access_key flows, ensure both access_id and access_key are set. For `uid`, ensure `uid_token` is set. For `cert`, provide both certificate and key material, either inline or by file path.
* HTTP 404 from /v2/* endpoints:
    * The resolver automatically falls back to the non-/v2 endpoints. If both fail, verify the gateway URL and network reachability.
* “Secret value not found for name …”:
    * Confirm the Credential ID (secret path) is correct and the Akeyless identity has permission to read it.
* JSON secret looks correct but everything maps to a single password field:
    * This can happen when certificate or key content is stored in JSON with literal line breaks inside quoted strings. Prefer `\n` inside the JSON string values.
* Logging:
    * Resolver logs go through Commons Logging. Check the MID Server logs for entries containing “Akeyless resolver”.

## Local/dev Testing (Optional)

You can run unit tests locally:

```shell
mvn test
```

To quickly sanity-check end-to-end against Akeyless, set environment variables and create a Discovery credential that points to a known secret path. For cloud-based auth types, run the MID on a host with a valid cloud identity.
