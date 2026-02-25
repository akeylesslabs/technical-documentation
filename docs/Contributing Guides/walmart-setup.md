---
title: WMT Setup
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
The Akeyless Gateway is a stateless Docker container, provided as a standalone or cluster. In order for the Akeyless Gateway to function properly, it requires public network connectivity to the Akeyless SaaS CORE.

## Docker

A basic deployment would preferably require a Linux Server (VM) with Docker Engine installed.  
You may download the latest Docker Engine on [Docker website](https://docs.docker.com/get-docker/).

## Network Connectivity

1. Network access to pull a Docker image from: [https://hub.docker.com](https://hub.docker.com)
2. Outgoing network access to Akeyless SaaS Core Services by way of the following URLs:

```http WMT tenant network
https://console.wmt.akeyless.io
https://zerotrust.wmt.akeyless.io
https://vault.wmt.akeyless.io
https://vault-ro.wmt.akeyless.io
https://auth.wmt.akeyless.io
https://auth-ro.wmt.akeyless.io
https://kfm1.wmt.akeyless.io
https://kfm1-ro.wmt.akeyless.io
https://kfm2.wmt.akeyless.io
https://kfm2-ro.wmt.akeyless.io
https://kfm3.wmt.akeyless.io
https://kfm3-ro.wmt.akeyless.io
https://audit.wmt.akeyless.io
https://audit-ro.wmt.akeyless.io
https://bis.wmt.akeyless.io
https://gator.wmt.akeyless.io
https://gator-ro.wmt.akeyless.io
amqps://mq.wmt.akeyless.io
tcp://log.wmt.akeyless.io:9997
tcp://log.wmt.akeyless.io:9443
```

Outgoing network access to Akeyless WMT SaaS Core Services by way of the following IPs:

| Service Name | Description |
| --- | --- |
| **Console**: `https://console.wmt.akeyless.io` | Akeyless SaaS platform. |
| **SRA Portal**: `https://zerotrust.wmt.akeyless.io` | Akeyless Secure Remote Access portal |
| **Vault**: `https://vault.wmt.akeyless.io` | User Account Management, managing user account, items, and roles. |
| **Auth**: `https://auth.wmt.akeyless.io` | Akeyless Authentication service. |
| **Audit**: `https://audit.wmt.akeyless.io` | Audit log main service, enables log forwarding from the Gateway and Bastions. |
| **BIS**: `https://bis.wmt.akeyless.io` | Billing Infrastructure Service. |
| **Gator**: `https://gator.wmt.akeyless.io` | Main service to sync gateways instances, and connections with Akeyless SaaS. |
| **MQ**: `amqps://mq.wmt.akeyless.io` | Message queue between Akeyless micro-services. |
| **KFM**: `https://kfm1.wmt.akeyless.io`, `https://kfm2.wmt.akeyless.io`, `https://kfm3.wmt.akeyless.io` | Key Fragments Services, enabling full DFC encryption. |
| **Logs**: `tcp://log.wmt.akeyless.io:9997`, `tcp://log.wmt.akeyless.io:9443` | Gateway logs, mainly to be reflected during failure scenarios. |

## Command Line Interface (CLI)

There are a handful of ways to interact with Akeyless Vault for managing, creating, and fetching multiple types of supported [secrets](https://docs.akeyless.io/docs/manage-your-secrets-overview). One of them is our Command Line Interface (CLI), which is purpose-built to serve your custom automation scripts (usually within a CI/CD pipeline or backup process), as well as human DevOps/Software engineers.

> **Info:**
>
> For a full list of the available CLI command, see the [CLI reference](https://docs.akeyless.io/docs/cli-reference).

Akeyless Vault CLI has a pre-compiled binary version for Linux, macOS, and Windows which can be easily installed by way of an installation script.

## Download and Install

Run the following command with Admin privileges to download and install the CLI binary.

```shell Linux
curl -o akeyless https://storage.googleapis.com/akeyless-cli/cli/latest/cli-linux-amd64
chmod +x akeyless
./akeyless
```
```shell macOS
curl -o akeyless https://storage.googleapis.com/akeyless-cli/cli/latest/cli-darwin-amd64
chmod +x akeyless
./akeyless
```
```shell Windows
curl -o akeyless.exe https://storage.googleapis.com/akeyless-cli/cli/latest/cli-windows-amd64.exe
akeyless.exe
```

During the initial installation of CLI you will be asked to provide Akeyless URL, set the Akeyless URL to: `vault.wmt.akeyless.io`:

```shell Set Akeyless URL
./akeyless   

$ AKEYLESS-CLI, first use detected
$ For more info please visit: https://docs.akeyless.io/docs/cli
$ Enter Akeyless URL (Default: vault.akeyless.io) vault.wmt.akeyless.io
```

At the prompt `Would you like to configure a profile (Y/n)` line, type `Y`. Then, type a name to rename the default profile, or press `Enter` to leave the name as `default`.

You can configure different types of authentication methods with the CLI:

1. [API Key](https://docs.akeyless.io/docs/auth-with-api-key) (`access_key`)
2. [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws) (`aws_iam`)
3. [Azure Active Directory](https://docs.akeyless.io/docs/auth-with-azure) (`azure_ad`)
4. [SAML](https://docs.akeyless.io/docs/auth-with-saml) (`saml`)
5. [LDAP](https://docs.akeyless.io/docs/auth-with-ldap) (`ldap`)
6. Password (`email/password`)
7. [OIDC](https://docs.akeyless.io/docs/auth-with-oidc) (`oidc`)
8. [Kubernetes](https://docs.akeyless.io/docs/auth-with-kubernetes) (`k8s`)
9. [GCP](https://docs.akeyless.io/docs/auth-with-gcp) (`GCP`)

Use the authentication mode that you also used when you signed up and signed in to the UI, use your username and password credentials, or use the API Key Akeyless assigned to you when you signed in for the first time.

If you're not sure what authentication method to use, consult your administrator.  
For more information about authentication methods, see [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods).

In the following example, you'll find both the API-key and the LDAP authentication methods: API-Key and LDAP.

```shell API-Key
#configure a profile
akeyless configure
Access ID: p-abc12de
Access Key: <type your access key here>
```
```shell LDAP
akeyless configure --access-type ldap
Access ID: p-abc12de
Ldap Proxy URL: https://Akeyless.GW
Profile ldap successfully configured
```

> **Warning (No validation of credentials):**
> If you don’t enter the correct credentials, the CLI will not give you an error message, and it will just tell you that everything is configured. You will only receive an error message when you attempt to run commands.

At the prompt `Would you like to add AKEYLESS-CLI to PATH (...)? (Y/n)` line, type `Y`.

You are now ready to use the CLI.

## Install Akeyless Gateway

Run the following to install Akeyless Gateway:

```shell Docker
docker run -d -p 8000:8000 \
  -p 8200:8200 -p 18888:18888 \
  -p 8080:8080 \
  -p 5696:5696 \
  -e AKEYLESS_URL=https://vault.wmt.akeyless.io \
  --name akeyless-gw akeyless/base
```

## Status Page

Service health dashboard

[https://status.wmt.akeyless.io](https://status.wmt.akeyless.io)
