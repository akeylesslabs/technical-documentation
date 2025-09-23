---
title: Walmart Setup
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
The Akeyless Gateway is a stateless docker container, provided as a standalone or cluster. In order for the Akeyless Gateway to function properly, it requires public network connectivity to the Akeyless SaaS CORE.

**Docker**  
A basic deployment would preferably require a Linux Server (VM) with a docker engine installed.  
You may download the latest docker engine on [Docker website](https://docs.docker.com/get-docker/).

**Network connectivity**

1. Network access to pull a docker image from: <https://hub.docker.com>
2. Outgoing network access to Akeyless SaaS Core Services via the following URLs:

```http Walmart tenant network
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

Outgoing network access to Akeyless Walmart SaaS Core Services via the following IP's:

[block:parameters]
{
  "data": {
    "h-0": "IP",
    "h-1": "Description",
    "h-2": "Region",
    "0-0": "34.102.167.39",
    "0-1": "Akeyless Walmart SaaS Gateway.",
    "0-2": "`us-central1`",
    "1-0": "35.186.234.237",
    "1-1": "Master region Ingress.",
    "1-2": "`us-central1`",
    "2-0": "34.102.251.13",
    "2-1": "Read-only multi-region Ingress.  \nThe same IP address will serve future Regions.",
    "2-2": "`us-central1`  \n`us-west1`",
    "3-0": "104.197.72.117",
    "3-1": "Message Queues.",
    "3-2": "`us-central1`"
  },
  "cols": 3,
  "rows": 4,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


**Akeyless Services Description**

The following table describes the main functionality of Akeyless micro-services:

[block:parameters]
{
  "data": {
    "h-0": "Service Name",
    "h-1": "Description",
    "0-0": "**Console**: <https://console.wmt.akeyless.io>",
    "0-1": "Akeyless SaaS platform.",
    "1-0": "<https://zerotrust.wmt.akeyless.io>",
    "1-1": "Akeyless Secure Remote Access portal",
    "2-0": "**Vault**: <https://vault.wmt.akeyless.io>",
    "2-1": "User Account Management, managing user account, items, and roles.",
    "3-0": "**Auth**: <https://auth.wmt.akeyless.io>",
    "3-1": "Akeyless Authentication service.",
    "4-0": "**Audit** : <https://audit.wmt.akeyless.io>",
    "4-1": "Audit log main service, enables log forwarding from GW & Bastions.",
    "5-0": "**BIS**: <https://bis.wmt.akeyless.io>",
    "5-1": "Billing Infrastructure Service.",
    "6-0": "**Gator**: <https://gator.wmt.akeyless.io>",
    "6-1": "Main service to sync gateways instances, and connections with Akeyless SaaS.",
    "7-0": "**MQ**: amqps://mq.wmt.akeyless.io",
    "7-1": "Message queue between Akeyless micro-services.",
    "8-0": "**KFM**:  \n<https://kfm1.wmt.akeyless.io>,  \n  \n<https://kfm2.wmt.akeyless.io>,  \n  \n<https://kfm3.wmt.akeyless.io>",
    "8-1": "Key Fragments Services, enabling full DFC encryption.",
    "9-0": "**Logs**:  \ntcp://log.wmt.akeyless.io:9997 tcp://log.wmt.akeyless.io:9443",
    "9-1": "GW logs, mainly to be reflected during failure scenarios."
  },
  "cols": 2,
  "rows": 10,
  "align": [
    "left",
    "left"
  ]
}
[/block]


## Command Line Interface (CLI)

There are a handful of ways to interact with Akeyless Vault for managing, creating, and fetching multiple types of supported [secrets](doc:manage-your-secrets-overview). One of them is our Command Line Interface (CLI), which is purpose-built to serve your custom automation scripts (usually within a CI/CD pipeline or backup process), as well as human DevOps/Software engineers.

> 👍 Info
> 
> For a full list of the available CLI command, see the [CLI reference](doc:cli-reference).

Akeyless Vault CLI has a pre-compiled binary version for Linux, macOS, and Windows which can be easily installed via an installation script.

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

At the prompt `Would you like to configure a profile (Y/n)` line, type `Y`.  Then, type a name to rename the default profile, or press `Enter` to leave the name as `default`.

You can configure different types of authentication methods from the CLI:

1. [API Key](https://docs.akeyless.io/docs/api-key) (`access_key`)
2. [AWS IAM](https://docs.akeyless.io/docs/aws-iam) (`aws_iam`)
3. [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad) (`azure_ad`)
4. [SAML](https://docs.akeyless.io/docs/saml) (`saml`)
5. [LDAP](https://docs.akeyless.io/docs/ldap) (`ldap`)
6. Password (`email/password`)
7. [OIDC](doc:openid) (`oidc`)
8. [K8s](doc:kubernetes-auth) (`k8s`)
9. [GCP](doc:gcp-auth-method) (`GCP`)

Use the authentication mode that you also used when you signed up and signed in to the UI, use your username and password credentials, or use the API key Akeyless assigned to you when you signed in for the first time.

If you're not sure what authentication method to use, consult your administrator.  
For more information about authentication methods, see [Authentication Methods](doc:access-and-authentication-methods).

In the following example, you'll find both the API-key and the LDAP authentication methods: API-Key and LDAP.

```shell API-Key
#configure a profile
akeyless configure
Access ID: p-abc12de
Access Key: <type your access key here>
```
```shell LDAP
akeyless configure --access-type ldap
Access ID:  p-abc12de
Ldap Proxy URL: https://Akeyless.GW
Profile ldap successfully configured
```

> 🚧 Warning
> 
> **No validation of credentials**  
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

<https://status.wmt.akeyless.io>