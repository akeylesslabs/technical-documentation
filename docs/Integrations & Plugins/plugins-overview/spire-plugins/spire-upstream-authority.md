---
title: SPIRE Upstream Authority
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

* [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) `v3.40.0` or later
* An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) attached to a role with the following permissions: `Create`,`List` for **Items**

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

Set `Create, list` permissions for **Secret & Keys** for the Access Role:

```shell
akeyless set-role-rule --role-name /Dev/Spire-Role \
--path /SPIRE/SVID/'*' \
--capability create --capability list
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

Next, create a **Classic Key** that will generate a self-signed certificate:

```shell
akeyless create-classic-key \
--name <Key Name> \
--alg <RSA2048 / RSA4096 / EC256 / EC384> \
--generate-self-signed-certificate <True> \
--gateway-url <http://<Your-Akeyless-GW-URL:8000> \
--certificate-ttl <TTL>
```

Where:

* `name` - Name of the Classic Key.

* `alg` - Type of Classic Key: Upstream Authority Plugin supports - `RSA2048`, `RSA4096`, `EC256`, or `EC384`

* `generate-self-signed-certificate` - Whether to generate a self-signed certificate with the key

* `gateway-url` - API Gateway URL

* `--certificate-ttl` - TTL in days for the generated certificate

Then, create a PKI Certificate Issuer:

```shell
akeyless create-pki-cert-issuer \
--name <Issuer name> \
--signer-key-name <Key Name> \
--ttl <TTL> \
--is-ca <Default=True> \
--allowed-uri-sans <URIs> \
--key-usage <certsign,crlsign> #can be one of them
```

Where:

* `name` - Name of the PKI Certificate Issuer.

* `signer-key-name` - A key to sign the certificate with (in our example, the key that was created in the previous step).

* `ttl` - The maximum requested Time To Live for issued certificates, in seconds.

* `is-ca` - Adds the basic constraints extension to the certificate.

* `allowed-uri-sans` - A list of the allowed URIs that clients can request to be included in the certificate as part of the URI Subject Alternative Names.

* `key-usage` - A comma-separated string or list of key usages. Needs to be either **certsign**, **crlsign** or both

Once the Classic Key and the PKI Issuer are created, a certificate needs to be generated:

> 📘 Certificate Signing Request
>
> In order to generate a certificate using the PKI Cert Issuer, a Certificate Signing Request (CSR) is required.
>
> If a CSR is provided along with a private key using the `--key-file-path` option, the provided key will be stored alongside the issued certificate.

The following command will generate a certificate using the PKI Cert Issuer that was created earlier: 

```shell
akeyless get-pki-certificate --cert-issuer-name <cert_issuer_name> --csr-file-path <csr_file_path> --key-file-path <key_file_path>
```

Where:

* `cert-issuer-name` - **Required**, Name of the PKI Certificate Issuer that was created in the previous step.

* `csr-file-path` - **Required**, Path to the CSR file. 

* `key-file-path` - Optional, Path to the Private key.

**Note**: The output of the command above will print a chain of certificates. Save the last certificate as a file as it will be used in the next steps. 

Next, [download](https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/) the **AkeylessUpstreamAuthority** plugin, by running the following command:

```shell AMD64
curl -o AkeylessUpstreamAuthority https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/spire-upstream-amd64-linux-v0.0.4
```
```shell ARM64
curl -o AkeylessUpstreamAuthority https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/spire-upstream-arm64-linux-v0.0.4
```

Validate the **SHA256 CHECKSUM**:

```shell
sha256sum AkeylessUpstreamAuthority
```

The `sha256sum` command generates a unique, fixed-size hash value (256 bits) for the **binary** file, ensuring that data remains unchanged.

Open your SPIRE Server Conf file which you will find in the `spire-` directory at `conf/server/server.conf`, and edit the **UpstreamAuthority** Plugin section as follows:

```shell
UpstreamAuthority  "akeyless_upstream" {
     plugin_cmd = "/path/to/plugin_cmd"
     plugin_checksum = "sha256 of the plugin binary"
     plugin_data {
       akeyless_gateway_url = '<https://<Your-Akeyless-GW-URL:8000/api/v2>'
       access_id = "<Your_Access_ID>"
       access_key = "<Your_Access_KEY>"
       pki_cert_issuer_name	= "<PKI_ISSUER_NAME>"
    }
}  
```

Where: 

* `plugin_cmd` - The location of the binary file that was created.

* `plugin_checksum` - sha256 of the binary.

* `akeyless_gateway_url` - Akeyless Gateway URL API v2 endpoint

* `access_id` - The Auth Method **Access-ID**

* `access_key` - Optional, The AccessKey. Relevant only for API Key.

* `pki_cert_issuer_name` - Name of the PKI Certificate Issuer. 

For **K8s, GCP** or **AzureAD** Auth methods set the following settings as well:

* `k8s_auth_config_name` - K8s Auth Config name as created under your Gateway

* `gcp_audience` - The audience to verify the JWT received by the client. By default, akeyless.io

* `azure_object_id` - Optional for Azure, objectID

> 🚧 Warning
>
> **TTL Configuration**
>
> The requested TTL in `conf/server/server.conf` file should be lower than the TTL that is configured in the PKI Certificate Issuer.

## SPIRE Server Initialization

In order to initialize the server, run the following command:

```shell
bin/spire-server run -config conf/server/server.conf &
```

Once the server is running, the Agent needs to be configured as well, in the `conf/agent/agent.conf` file. Open the Agent conf file and add the following line in the `agent` section in order set the path to the SPIRE server CA bundle:

```shell
trust_bundle_path = "/Path/To/certificate/file" #The file that holds the certificate from the previous step
```

Once the `conf/agent/agent.conf` file is configured, we will start the agent: 

```shell
bin/spire-server token generate -spiffeID spiffe://example.org/myagent
```

The output of this command will print a token that will be used to start the Agent.

## SPIRE Agent Initialization

```shell
bin/spire-agent run -config conf/agent/agent.conf -joinToken <token_string> &
```

> 📘 Info
>
> **SPIFFE/SPIRE**
>
> For the full configuration steps, visit the official [Quickstart for Linux and MacOS X](https://spiffe.io/docs/latest/try/getting-started-linux-macos-x/) guide
