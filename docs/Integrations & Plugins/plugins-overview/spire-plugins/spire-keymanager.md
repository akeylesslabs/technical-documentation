---
title: SPIRE Key Manager
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
This guide covers the Akeyless SPIRE Key Manager plugin, which manages signing keys used for X.509 SPIFFE Verifiable Identity Documents (SVIDs) and JWT-SVIDs.

## Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) `v3.40.0` or later
* An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) attached to a role with `Create`, `Read`, and `List` permissions for **Items**, as well as [Gateway Access Permission](https://docs.akeyless.io/docs/gateway-authentication-and-access) to manage [Classic Keys](https://docs.akeyless.io/docs/classic-keys).

## Authentication

The following Authentication Methods can be used:

* [API Key](https://docs.akeyless.io/docs/auth-with-api-key)
* [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws)
* [Azure](https://docs.akeyless.io/docs/auth-with-azure)
* [GCP](https://docs.akeyless.io/docs/auth-with-gcp)
* [K8s](https://docs.akeyless.io/docs/auth-with-kubernetes)

> ℹ️ **Note:**
>
> This guide uses API Key authentication for brevity and Linux-based examples. For macOS, see the [SPIRE quickstart section](https://spiffe.io/docs/latest/try/getting-started-linux-macos-x/#building-spire-on-macosdarwin).

<ApiKeyWarning />

Create a new [API Key Authentication Method](https://docs.akeyless.io/docs/auth-with-api-key) using the CLI:

```shell
akeyless create-auth-method --name /Dev/Spire-Server-Auth
```

Create an [Access Role](https://docs.akeyless.io/docs/rbac):

```shell
akeyless create-role --name /Dev/Spire-Server-Role
```

Associate your **API Key** Authentication Method to the Access Role that was created:

```shell
akeyless assoc-role-am --role-name /Dev/Spire-Server-Role \
--am-name /Dev/Spire-Server-Auth
```

Set `read, create, list` permissions for **Secret & Keys** for the Access Role:

```shell
akeyless set-role-rule --role-name /Dev/Spire-Server-Role \
--path /SPIRE/Keys/'*' \
--capability read \
--capability create \
--capability list
```

### Grant Access Permissions on the Gateway

1. Sign in to the Akeyless Console with a Gateway admin account.
2. Open **Gateways**, and select the target Gateway.
3. Open **Access Permissions**, and select **New**.
4. Select the Authentication Method, and grant either **Admin** permissions or **Custom** permissions that include Classic Key operations.

## Configuration

Run the following command to download and unpack pre-built `spire-server` and `spire-agent` executables and example configuration files in a SPIRE-1.7.0 directory.

```shell
curl -s -N -L https://github.com/spiffe/spire/releases/download/v1.7.0/spire-1.7.0-linux-amd64-glibc.tar.gz | tar xz
```

Next, download the latest **AkeylessKeyManager** plugin:

```shell AMD64
curl -o AkeylessKeyManager https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/spire-kms/spire-kms-linux-amd64
chmod +x AkeylessKeyManager
```
```shell ARM64
curl -o AkeylessKeyManager https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/spire-kms/spire-kms-linux-arm64
chmod +x AkeylessKeyManager
```

Download the checksum file and validate the binary:

```shell
curl -o spire-kms.sha256 https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/spire-kms/spire-kms-linux-amd64-sha256sumfile
sha256sum -c spire-kms.sha256
```

The `sha256sum` command generates a unique, fixed-size hash value (256 bits) for the **binary** file, ensuring that data remains unchanged.

Open your SPIRE Server Conf file which you will find in the `spire-` directory at `/conf/server/server.conf`, and edit the **KeyManager** Plugin section as follows:

```shell
KeyManager "akeyless_kms" {
  plugin_cmd = "/path/to/AkeylessKeyManager"
  plugin_checksum = "sha256_of_plugin_binary"
    plugin_data {
    akeyless_gateway_url = "https://<your-gateway-url>:8000/api/v2"
    access_id = "<your_access_id>"
    access_key = "<your_access_key>"
    key_metadata_file = "./key_metadata"
    target_folder = "/SPIRE/Keys/"
    }
}
```

Where:

* `plugin_cmd` - The path to the plugin binary.

* `plugin_checksum` - The SHA256 digest of that binary.

* `akeyless_gateway_url` - Akeyless Gateway URL API v2 endpoint.

* `access_id` - The Authentication Method Access ID.

* `access_key` - Required for API Key authentication.

* `key_metadata_file` - File path where generated key metadata is persisted.

* `target_folder` - Akeyless path where generated key items are stored in the format `/SPIRE/Keys/{TRUST_DOMAIN}/{SERVER_ID}/{KEY_ID}`.

For **K8s**, **GCP**, or **AzureAD** Auth methods set the following settings as well:

* `k8s_auth_config_name` - Kubernetes Auth Config name as created under your Gateway.

* `gcp_audience` - Audience used to verify JWTs from the client. Default: `akeyless.io`.

* `azure_object_id` - Optional for Azure, `objectID`

## SPIRE Server Initialization

> ℹ️ **Info (Key Type):**
>
> To set a key type for SPIRE Server, add the following parameter in the `server` section.
>
> For example, to use `RSA-2048`, set `ca_key_type = rsa-2048`. The default key type is `ec-p256`.

To initialize the server, run the following command:

```shell
bin/spire-server run -config conf/server/server.conf &
```

With successful server initialization, 2 **Classic Keys** are created in the Akeyless Console under `/SPIRE/Keys/`:

* **JWT-Signer-A** - Used to sign JWT-SVIDs.
* **X509-CA-A** - Used to sign X.509-SVIDs.

> ℹ️ **Info (SPIFFE/SPIRE):**
>
> For full bootstrap and registration steps, see [Quickstart for Linux and macOS](https://spiffe.io/docs/latest/try/getting-started-linux-macos-x/).
