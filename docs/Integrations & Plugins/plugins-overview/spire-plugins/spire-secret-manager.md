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
## Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) `v3.35.0` or later
* An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) attached to a role with the following permissions: `Create`,`Update` for **Items**

## Authentication

The following Authentication Methods can be used: 

* [API Key](https://docs.akeyless.io/docs/api-key)
* [AWS IAM](https://docs.akeyless.io/docs/aws-iam)
* [Azure](https://docs.akeyless.io/docs/azure-ad)
* [GCP](https://docs.akeyless.io/docs/gcp-auth-method)
* [K8S](https://docs.akeyless.io/docs/kubernetes-auth)

> 👍 Note
>
> In this guide, we will use an API Key Authentication Method for simplicity and we are only using Linux machines. For MacOS, please see the guide [here](https://spiffe.io/docs/latest/try/getting-started-linux-macos-x/#building-spire-on-macosdarwin).

Create a new [API Key Authentication Method](https://docs.akeyless.io/docs/api-key) using the CLI:

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
--capability create --capability update
```

## Configuration

Run the following command to download and unpack pre-built `spire-server` and `spire-agent` executables and example configuration files in a spire-1.7.0 directory.

```Text Shell
curl -s -N -L https://github.com/spiffe/spire/releases/download/v1.7.0/spire-1.7.0-linux-amd64-glibc.tar.gz | tar xz
```

Next, [download](https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/agent/) the **AkeylessSecretManager** plugin, by running the following command:

```shell AMD64
curl -o AkeylessSecretManager https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/agent/spire-sm-amd64-linux-v0.0.6
chmod +x AkeylessSecretManager
```
```shell ARM64
curl -o AkeylessSecretManager https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/agent/spire-sm-arm64-linux-v0.0.6
chmod +x AkeylessSecretManager
```

Validate the **SHA256 CHECKSUM**:

```shell
sha256sum AkeylessSecretManager
```

The `sha256sum` command generates a unique, fixed-size hash value (256 bits) for the **binary** file, ensuring that data remains unchanged.

Open the SPIRE Agent config file in the `spire-` directory in `conf/agent/agent.conf`, and add the **SVIDStore** Plugin under `plugins` as follows:

```shell
SVIDStore "akeyless_secretsmanager" {
    plugin_cmd = "/path/to/plugin_cmd"
    plugin_checksum = "sha256 of the plugin binary"
    plugin_data {
     akeyless_gateway_url = 'https://<Your-Akeyless-GW-URL:8000/api/v2>' # or use port 8081
     access_id = "<Your_Access_ID>"
     access_key = "<Your_Access_KEY>"
     target_folder = "/SPIRE/SVID/"     
   }
}
```

Where:

* `plugin_cmd` - The location of the binary file that was created.

* `plugin_checksum` - sha256 of the binary.

* `akeyless_gateway_url` - Akeyless Gateway URL API v2 endpoint.

* `access_id` - The **Auth Method** `AccessID`

* `access_key` - Optional, the `AccessKey`. Relevant only for **API Key**

* `target_folder` - A path to save all items inside Akeyless where the generated `SVIDs` will be stored

For **K8s**,**GCP** or **AzureAD** Auth method set the following settings as well: 

* `k8s_auth_config_name`- K8s Auth Config name as created under your Gateway

* `gcp_audience`-  The audience to verify the JWT received by the client. By default, `akeyless.io`

* `azure_object_id` - Optional for Azure, `objectID`

## SPIRE Agent Initialization

> 📘 Info
>
> **SPIRE Server**
>
> You are required to start the [SPIRE server](https://docs.akeyless.io/docs/keymanager#spire-server-initialization) before running the Agent commands.

In order to attest the SPIRE agent to the server, create a join token:

```shell
bin/spire-server token generate -spiffeID spiffe://example.org/myagent
Token: <token_string>
```

Make a note of the token, you will need it in the next step to attest the agent on initial startup.

### Attest the SPIRE agent to the SPIRE server:

```shell
bin/spire-agent run -config conf/agent/agent.conf -joinToken <token_string> &
```

### Create a registration policy

```shell
bin/spire-server entry create -parentID spiffe://example.org/myagent \
-spiffeID spiffe://example.org/myservice -selector akeyless_secretsmanager:secretname:<Secret Name> -storeSVID
```

Upon successful registration of the workload, a secret will be created in Akeyless in the `/SPIRE/SVID/` folder, which will contain the following information:

* SpiffeID
* Certificate
* x509SVIDKey

> 📘 Info
>
> **SPIFFE/SPIRE**
>
> For the full configuration steps, visit the official [Quickstart for Linux and MacOS X](https://spiffe.io/docs/latest/try/getting-started-linux-macos-x/) guide
