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
This guide covers how to configure the Akeyless SPIRE Upstream Authority plugin for both X.509 SPIFFE Verifiable Identity Document (SVID) issuance and JWT-SVID key publication.

## Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) `v3.40.0` or later
* A running SPIRE Server and SPIRE Agent deployment
* An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) attached to a role with:
    * `Create` and `List` on relevant item paths for X.509 CA operations
    * `Read` on the item used for JWT signing keys (for JWT-SVID support)

## Authentication

The following Authentication Methods are supported:

* [API Key](https://docs.akeyless.io/docs/auth-with-api-key)
* [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws)
* [Azure](https://docs.akeyless.io/docs/auth-with-azure)
* [GCP](https://docs.akeyless.io/docs/auth-with-gcp)
* [K8s](https://docs.akeyless.io/docs/auth-with-kubernetes)

> ℹ️ **Note:**
>
> This guide uses API Key authentication for brevity. For production environments, use a cloud or workload-based Authentication Method where possible.

<ApiKeyWarning />

Create an API Key Authentication Method:

```shell
akeyless create-auth-method --name /Dev/Spire-Auth
```

Create an access role:

```shell
akeyless create-role --name /Dev/Spire-Role
```

Associate the Authentication Method to the role:

```shell
akeyless assoc-role-am --role-name /Dev/Spire-Role \
--am-name /Dev/Spire-Auth
```

Set role permissions for the SPIRE item path:

```shell
akeyless set-role-rule --role-name /Dev/Spire-Role \
--path /SPIRE/SVID/'*' \
--capability create --capability list --capability read
```

### Grant Access Permissions on the Gateway

1. Sign in to the Akeyless Console with a Gateway admin account.
2. Open **Gateways**, and select the target Gateway.
3. Open **Access Permissions**, and select **New**.
4. Select the Authentication Method, and grant:
   * **Admin** permissions, or
   * **Custom** permissions that include the required key and item operations.

## Download the Plugin

Download the latest Akeyless Upstream Authority plugin:

```shell AMD64
curl -o AkeylessUpstreamAuthority https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/spire-upstream/spire-upstream-linux-amd64
```
```shell ARM64
curl -o AkeylessUpstreamAuthority https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/spire-upstream/spire-upstream-linux-arm64
```

Download the checksum file and validate the binary:

```shell
curl -o spire-upstream.sha256 https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/spire-upstream/spire-upstream-linux-amd64-sha256sumfile
sha256sum -c spire-upstream.sha256
```

## Configure SPIRE Server

Edit `conf/server/server.conf`, and configure the `UpstreamAuthority` block:

```shell
UpstreamAuthority "akeyless_upstream" {
    plugin_cmd = "/path/to/AkeylessUpstreamAuthority"
    plugin_checksum = "sha256_of_plugin_binary"
    plugin_data {
        akeyless_gateway_url = "https://<your-gateway-url>:8000/api/v2"
        access_id = "<your_access_id>"
        access_key = "<your_access_key>"
        pki_cert_issuer_name = "<pki_issuer_name>"
        jwt_keys_secret_name = "<jwt_keys_secret_name>"
    }
}
```

Where:

* `plugin_cmd` is the path to the plugin binary.
* `plugin_checksum` is the SHA256 digest of that binary.
* `akeyless_gateway_url` is the Akeyless Gateway API v2 endpoint.
* `access_id` is the Authentication Method Access ID.
* `access_key` is required for API Key authentication.
* `pki_cert_issuer_name` is used for X.509 CA minting.
* `jwt_keys_secret_name` points to the Akeyless item that stores JWT signing keys for JWT-SVID publication.

For K8s, GCP, or Azure Authentication Methods, also set:

* `k8s_auth_config_name`
* `gcp_audience` (default: `akeyless.io`)
* `azure_object_id`

> ⚠️ **Warning (TTL Configuration):**
>
> Ensure the requested SPIRE TTL values are lower than the configured TTL values in the Akeyless PKI Certificate Issuer.

## Prepare Akeyless Resources

For X.509 CA minting, create a Classic Key and PKI Certificate Issuer.

Create a Classic Key:

```shell
akeyless create-classic-key \
--name /SPIRE/SVID/classic-key \
--alg RSA2048 \
--generate-self-signed-certificate true \
--gateway-url "https://<your-gateway-url>:8000" \
--certificate-ttl 7
```

Create a PKI Certificate Issuer:

```shell
akeyless create-pki-cert-issuer \
--name /SPIRE/SVID/pki-issuer \
--signer-key-name /SPIRE/SVID/classic-key \
--ttl 604800 \
--is-ca true \
--allowed-uri-sans spiffe://example.org/* \
--key-usage certsign,crlsign
```

For JWT-SVID support, prepare an Akeyless item that contains the JWT signing keys, and reference that item name in `jwt_keys_secret_name`.

> ℹ️ **Info:**
>
> If the item referenced by `jwt_keys_secret_name` does not contain JWT keys, plugin initialization fails with a missing JWT keys error.

## Initialize SPIRE Server and Agent

Start SPIRE Server:

```shell
bin/spire-server run -config conf/server/server.conf &
```

Set the trust bundle path in `conf/agent/agent.conf`:

```shell
trust_bundle_path = "/path/to/certificate/file"
```

Generate an agent join token:

```shell
bin/spire-server token generate -spiffeID spiffe://example.org/myagent
```

Start SPIRE Agent:

```shell
bin/spire-agent run -config conf/agent/agent.conf -joinToken <token_string> &
```

> ℹ️ **Info (SPIFFE/SPIRE):**
>
> For full SPIRE bootstrap and registration steps, see [Quickstart for Linux and macOS](https://spiffe.io/docs/latest/try/getting-started-linux-macos-x/).
