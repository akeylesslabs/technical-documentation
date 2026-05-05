---
title: SPIRE Secret Manager
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
This guide covers the Akeyless SPIRE Secret Manager plugin, which stores workload X.509 SPIFFE Verifiable Identity Documents (SVIDs) in Akeyless.

## Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) `v3.40.0` or later
* An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methodss) attached to a role with `Create`, `Update`, and `List` permissions for **Items**

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
akeyless create-auth-method --name /Dev/Spire-Agent-Auth
```

Create an [Access Role](https://docs.akeyless.io/docs/rbac):

```shell
akeyless create-role --name /Dev/Spire-Agent-Role
```

Associate your **API Key** Authentication Method to the Access Role that was created:

```shell
akeyless assoc-role-am --role-name /Dev/Spire-Agent-Role \
--am-name /Dev/Spire-Agent-Auth
```

Set `create, list, update` permissions for **Secret & Keys** for the Access Role:

```shell
akeyless set-role-rule --role-name /Dev/Spire-Agent-Role \
--path /SPIRE/SVID/'*' \
--capability create \
--capability update \
--capability list
```

## Configuration

Run the following command to download and unpack pre-built `spire-server` and `spire-agent` executables and example configuration files in a SPIRE-1.7.0 directory.

```shell
curl -s -N -L https://github.com/spiffe/spire/releases/download/v1.7.0/spire-1.7.0-linux-amd64-glibc.tar.gz | tar xz
```

Next, download the **AkeylessSecretManager** plugin:

```shell AMD64
curl -o AkeylessSecretManager https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/agent/spire-sm-amd64-linux-v0.0.6
chmod +x AkeylessSecretManager
```
```shell ARM64
curl -o AkeylessSecretManager https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/agent/spire-sm-arm64-linux-v0.0.6
chmod +x AkeylessSecretManager
```

Download the checksum file and validate the binary:

```shell
curl -o spire-secretsmanager.sha256 https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/agent/spire-sm-amd64-linux-v0.0.6.checksum
sha256sum -c spire-secretsmanager.sha256
```

The `sha256sum` command generates a unique, fixed-size hash value (256 bits) for the **binary** file, ensuring that data remains unchanged.

Open the SPIRE Agent config file in the `spire-` directory in `conf/agent/agent.conf`, and add the **SVIDStore** Plugin under `plugins` as follows:

```shell
SVIDStore "akeyless_secretsmanager" {
  plugin_cmd = "/path/to/AkeylessSecretManager"
  plugin_checksum = "sha256_of_plugin_binary"
    plugin_data {
    akeyless_gateway_url = "https://<your-gateway-url>:8000/api/v2"
    access_id = "<your_access_id>"
    access_key = "<your_access_key>"
    target_folder = "/SPIRE/SVID/"
  }
}
```

Where:

* `plugin_cmd` - The path to the plugin binary.

* `plugin_checksum` - The SHA256 digest of that binary.

* `akeyless_gateway_url` - Akeyless Gateway URL API v2 endpoint.

* `access_id` - The Authentication Method Access ID.

* `access_key` - Required for API Key authentication.

* `target_folder` - A path to save all items inside Akeyless where the generated X.509-SVIDs will be stored

For **Kubernetes**, **GCP** or **AzureAD** Auth Method set the following settings as well:

* `k8s_auth_config_name` - Kubernetes Auth Config name as created under your Gateway.

* `gcp_audience` - Audience used to verify JWTs from the client. Default: `akeyless.io`.

* `azure_object_id` - Optional for Azure, `objectID`

## SPIRE Agent Initialization

> ℹ️ **Info (SPIRE Server):**
>
> Start SPIRE Server before running the SPIRE Agent commands.

To attest the SPIRE agent to the server, create a join token:

```shell
bin/spire-server token generate -spiffeID spiffe://example.org/myagent
Token: <token_string>
```

Make a note of the token, you will need it in the next step to attest the agent on initial startup.

### Attest the SPIRE Agent to the SPIRE Server

```shell
bin/spire-agent run -config conf/agent/agent.conf -joinToken <token_string> &
```

### Create a Registration Policy

```shell
bin/spire-server entry create -parentID spiffe://example.org/myagent \
-spiffeID spiffe://example.org/myservice -selector akeyless_secretsmanager:secretname:<Secret Name> -storeSVID
```

Upon successful registration of the workload, a secret is created in `/SPIRE/SVID/` in Akeyless, containing X.509-SVID material such as:

* SPIFFE ID
* X.509 certificate chain
* X.509-SVID private key

> ℹ️ **Info (SPIFFE/SPIRE):**
>
> For full bootstrap and registration steps, see [Quickstart for Linux and macOS](https://spiffe.io/docs/latest/try/getting-started-linux-macos-x/).
