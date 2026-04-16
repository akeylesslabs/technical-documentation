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
This guide covers the Akeyless SPIRE Upstream Authority SM plugin, which uses a certificate item from Akeyless for SPIRE upstream X.509 SPIFFE Verifiable Identity Document (SVID) CA operations.

## Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) `v3.40.0` or later
* A running SPIRE Server and SPIRE Agent deployment
* An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) attached to a role with `Read` permission on the required item path
* A certificate item in Akeyless containing `certificate` and `private_key` in PEM format

> ℹ️ **Note:**
>
> For JWT-SVID key publication support, use [SPIRE Upstream Authority](https://docs.akeyless.io/docs/spire-upstream-authority).

## Authentication

The following Authentication Methods are supported:

* [API Key](https://docs.akeyless.io/docs/auth-with-api-key)
* [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws)
* [Azure](https://docs.akeyless.io/docs/auth-with-azure)
* [GCP](https://docs.akeyless.io/docs/auth-with-gcp)
* [K8s](https://docs.akeyless.io/docs/auth-with-kubernetes)

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

Set role permissions:

```shell
akeyless set-role-rule --role-name /Dev/Spire-Role \
--path /SPIRE/SVID/'*' \
--capability read
```

## Download the Plugin

Download the latest SM plugin:

```shell AMD64
curl -o AkeylessUpstreamAuthority-sm https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/spire-upstream-sm/spire-upstream-sm-linux-amd64
```
```shell ARM64
curl -o AkeylessUpstreamAuthority-sm https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/spire-upstream-sm/spire-upstream-sm-linux-arm64
```

Download the checksum file and validate the binary:

```shell
curl -o spire-upstream-sm.sha256 https://download.akeyless.io/Akeyless_Artifacts/Linux/spire/plugin/server/spire-upstream-sm/spire-upstream-sm-linux-amd64-sha256sumfile
sha256sum -c spire-upstream-sm.sha256
```

## Configure SPIRE Server

Edit `conf/server/server.conf`, and configure the `UpstreamAuthority` block:

```shell
UpstreamAuthority "akeyless_sm" {
    plugin_cmd = "/path/to/AkeylessUpstreamAuthority-sm"
    plugin_checksum = "sha256_of_plugin_binary"
    plugin_data {
        access_id = "<your_access_id>"
        access_key = "<your_access_key>"
        akeyless_gateway_url = "https://<your-gateway-url>:8000/api/v2"
        certificate_name = "/SPIRE/SVID/certificate_name"
    }
}
```

Where:

* `plugin_cmd` is the path to the plugin binary.
* `plugin_checksum` is the SHA256 digest of that binary.
* `access_id` is the Authentication Method Access ID.
* `access_key` is required for API Key authentication.
* `akeyless_gateway_url` is the Akeyless Gateway API v2 endpoint.
* `certificate_name` is the certificate item name in Akeyless.

For K8s, GCP, or Azure Authentication Methods, also set:

* `k8s_auth_config_name`
* `gcp_audience` (default: `akeyless.io`)
* `azure_object_id`

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
