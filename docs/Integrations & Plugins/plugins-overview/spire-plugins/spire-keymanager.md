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
## Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) `v3.35.0` or later
* An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) attached to a role with `create` and `read` permissions for **Items**, as well as [Gateway Access Permission](https://docs.akeyless.io/docs/gateway-access-permissions) to manage [Classic Keys](https://docs.akeyless.io/docs/classic-keys).

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
--capability read --capability create 
```

### Grant Access Permissions on the Gateway

Log into the console using a Gateway admin account, navigate to the **Gateways** tab, and choose the relevant **Gateway**.

Click on **Access Permissions** and click on  **New**: 

Give it a meaningful **Name**, choose the **Auth Method**, and click next.

Set the relevant permissions for this **Auth Method**:

 **Admin** - grant full permissions on the **Gateway** or

**Custom** - grant specific permissions for at least **Classic Keys**.

## Configuration

Run the following command to download and unpack pre-built `spire-server` and `spire-agent` executables and example configuration files in a spire-1.7.0 directory.

```Text Shell
curl -s -N -L https://github.com/spiffe/spire/releases/download/v1.7.0/spire-1.7.0-linux-amd64-glibc.tar.gz | tar xz
```

Next, [download](https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/) the **AkeylessKeyManager** plugin, by running the following command:

```shell AMD64
curl -o AkeylessKeyManager https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/spire-kms-amd64-linux-v0.0.8
chmod +x AkeylessKeyManager
```
```shell ARM64
curl -o AkeylessKeyManager https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/spire-kms-arm64-linux-v0.0.6
chmod +x AkeylessKeyManager
```

Validate the **SHA256 CHECKSUM**:

```shell
sha256sum AkeylessKeyManager
```

The `sha256sum` command generates a unique, fixed-size hash value (256 bits) for the **binary** file, ensuring that data remains unchanged.

Open your SPIRE Server Conf file which you will find in the `spire-` directory at `/conf/server/server.conf`, and edit the **KeyManager** Plugin section as follows:

```shell
KeyManager "akeyless_kms" {
    plugin_cmd = "/path/to/plugin_cmd"
    plugin_checksum = "sha256 of the plugin binary"
  	plugin_data {
         akeyless_gateway_url = 'https://<Your-Akeyless-GW-URL:8000/api/v2>' # or use port 8081
  	 access_id = "<Your_Access_ID>"
         access_key = "<Your_Access_KEY>"
         key_metadata_file = "./key_metadata"
         target_folder = "/SPIRE/Keys/"
	}
}
```

Where:

* `plugin_cmd` - The location of the binary file that was created.

* `plugin_checksum` - sha256 of the binary.

* `akeyless_gateway_url` -  Akeyless Gateway URL API v2 endpoint.

* `access_id` - The **Auth Method** `AccessID` 

* `access_key` - Optional, The `AccessKey`. Relevant only for **API Key**. 

* `key_metadata_file` - A file path location where information about generated keys will be persisted

* `target_folder` - A path to save all items inside Akeyless where the generated `KEY-ID` will be stored using the following form `/SPIRE/Keys/{TRUST_DOMAIN}/{SERVER_ID}/{KEY_ID}`

For **K8s**,**GCP** or **AzureAD** Auth methods set the following settings as well: 

* `k8s_auth_config_name`- K8s Auth Config name as created under your Gateway

* `gcp_audience`-  The audience to verify the JWT received by the client. By default, `akeyless.io`

* `azure_object_id` - Optional for Azure, `objectID`

## SPIRE Server Initialization

> 📘 Info
>
> **Key Type**
>
> In order to set a key type for the spire server, inside the `server` section, add the following parameter.
>
> For example, if we would want to use a key type of `RSA-2048` we will add:\
> `ca_key_type` = `rsa-2048`. The default Key Type is: `ec-p256`

To initialize the server, run the following command:

```shell
bin/spire-server run -config conf/server/server.conf &
```

With a successful server initialization, 2 **Classic keys** will be created in your Akeyless account and you can find them in the console in the `SPIRE/Keys` folder:

* **JWT-Signer-A** - Uses **JSON Web Tokens (JWT)** signed by an identity provider for authentication and authorization of clients.
* **X509-CA-A** - Relies on **X.509** certificates issued by a trusted Certificate Authority.

> 📘 Info
>
> **SPIFFE/SPIRE**
>
> For the full configuration steps, visit the official [Quickstart for Linux and MacOS X](https://spiffe.io/docs/latest/try/getting-started-linux-macos-x/) guide
