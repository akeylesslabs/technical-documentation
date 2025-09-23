---
title: SPIRE Upstream Authority SM
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
# Prerequisites

- [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) `v3.40.0` or later
- An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) attached to a role with `Read` permission for **Items**
- **Certificate Item** stored in Akeyless Platform containing the   `certificate` and `private_key` in `pem` format. 

# Authentication

The following Authentication Methods are supported: 

- [API Key](https://docs.akeyless.io/docs/api-key)
- [AWS IAM](https://docs.akeyless.io/docs/aws-iam)
- [Azure](https://docs.akeyless.io/docs/azure-ad)
- [GCP](https://docs.akeyless.io/docs/gcp-auth-method)
- [K8S](https://docs.akeyless.io/docs/kubernetes-auth)

> 👍 Note
> 
> In this guide, we will use an `API Key` Authentication Method for simplicity

Create a new [API Key Authentication Method](https://docs.akeyless.io/docs/api-key) using the CLI:

```shell
akeyless create-auth-method --name /Dev/Spire-Auth
```

Create an [Access Role](https://docs.akeyless.io/docs/rbac):

```shell
akeyless create-role --name /Dev/Spire-Role
```

Associate your **API Key** Authentication Method to the Access Role that was created:

```shell
akeyless assoc-role-am --role-name /Dev/Spire-Role \
--am-name /Dev/Spire-Auth
```

Set `Read` permission for **Secret & Keys** for the Access Role:

```shell
akeyless set-role-rule --role-name /Dev/Spire-Role \
--path /SPIRE/SVID/'*' \
--capability read
```

# Configuration

Run the following command to download and unpack pre-built `spire-server` and `spire-agent` executable and example configuration files in a `spire-1.7.0` directory:

```Text Shell
curl -s -N -L https://github.com/spiffe/spire/releases/download/v1.7.0/spire-1.7.0-linux-amd64-glibc.tar.gz | tar xz
```

Next, run the following command in order to create the `certificate` item in Akeyless:

```shell
akeyless create-certificate \
--name </SPIRE/SVID/certificate_name> \
--certificate <Path/To/certificate.pem> \
--private-key <Path/To/private_Key.pem>
```

 Use the following command to download the **AkeylessUpstreamAuthority SM** plugin:

```Text shell
curl -o AkeylessUpstreamAuthority-sm  https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/spire-upstream-sm-amd64-linux-v0.0.1
```

Change the file permissions so it will be executable:

```shell
chmod +x AkeylessUpstreamAuthority-sm
```

Validate the `SHA256 CHECKSUM`:

```shell
sha256sum AkeylessUpstreamAuthority-sm
```

The `sha256sum` command generates a unique, fixed-size hash value (256 bits) for the **binary** file, ensuring that data remains unchanged.

### Server configuration

Edit the **UpstreamAuthority** Plugin as follows in `spire-1.7.0/conf/server/server.conf` file.

```shell
UpstreamAuthority  "akeyless_sm" {
     plugin_cmd = "/path/to/plugin_cmd"
     plugin_checksum = "sha256 of the plugin binary"
     plugin_data {
       access_id = "<Your_Access_ID>"
       access_key = "<Your_Access_KEY>"
       akeyless_gateway_url = 'https://<Your-Akeyless-GW-URL:8000/api/v2>' # or use port 8081
       certificate_name = "</SPIRE/SVID/certificate_name>"
     }
}
```

Where: 

- `plugin_cmd` - The location of the binary file that was created.

- `plugin_checksum` - sha256 of the binary.

- `access_id` - The Auth Method **Access-ID**

- `access_key` - Optional, The AccessKey. Relevant only for API Key.

- `akeyless_gateway_url` - Akeyless Gateway URL API v2 endpoint.

- `certificate_name` - The `certificate` item that was created earlier in Akeyless. In our example `/SPIRE/SVID/certificate_name`

For **K8s, GCP** or **AzureAD **Auth methods set the following settings as well:

- `k8s_auth_config_name` - K8s Auth Config name as created under your Gateway

- `gcp_audience` - The audience to verify the `JWT` received by the client. By default, `akeyless.io`

- `azure_object_id` - Optional for Azure, `objectID`

## SPIRE Server Initialization

In order to initialize the server, run the following command:

```shell
bin/spire-server run -config conf/server/server.conf &
```

Once the server is running, the Agent needs to be configured as well, add the following line to the `conf/agent/agent.conf` file in the `agent` section in order to set the path to the SPIRE server **CA bundle**:

```shell
trust_bundle_path = "/Path/To/certificate/file" 
```

> 📘 Info
> 
> **trust bundle**
> 
> The `"/Path/To/certificate.pem"` is a path on your machine where a `certificate.pem` file will be exist and the value of the file will be the value of the `certificate` that was created earlier in Akeyless.

Run the following command in order to generate a token that will be used to attest the `agent` to the `server`

```shell
bin/spire-server token generate -spiffeID spiffe://example.org/myagent
```

## SPIRE Agent Initialization

Use the token that was generated in order to attest the `agent` to the `server`

```shell
bin/spire-agent run -config conf/agent/agent.conf -joinToken <token_string> &
```

> 📘 Info
> 
> **SPIFFE/SPIRE**
> 
> For the full configuration steps, visit the official [Quickstart for Linux and MacOS X](https://spiffe.io/docs/latest/try/getting-started-linux-macos-x/) guide