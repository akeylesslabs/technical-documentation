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

**Docker**\
A basic deployment would preferably require a Linux Server (VM) with a docker engine installed.\
You may download the latest docker engine on [Docker website](https://docs.docker.com/get-docker/).

**Network connectivity**

1. Network access to pull a docker image from: [https://hub.docker.com](https://hub.docker.com)
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

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th>
        IP
      </th>

      <th>
        Description
      </th>

      <th>
        Region
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        34.102.167.39
      </td>

      <td>
        Akeyless Walmart SaaS Gateway.
      </td>

      <td>
        `us-central1`
      </td>
    </tr>

    <tr>
      <td>
        35.186.234.237
      </td>

      <td>
        Master region Ingress.
      </td>

      <td>
        `us-central1`
      </td>
    </tr>

    <tr>
      <td>
        34.102.251.13
      </td>

      <td>
        Read-only multi-region Ingress.\
        The same IP address will serve future Regions.
      </td>

      <td>
        `us-central1`\
        `us-west1`
      </td>
    </tr>

    <tr>
      <td>
        104.197.72.117
      </td>

      <td>
        Message Queues.
      </td>

      <td>
        `us-central1`
      </td>
    </tr>
  </tbody>
</Table>

**Akeyless Services Description**

The following table describes the main functionality of Akeyless micro-services:

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Service Name
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        * \*Console\*\*: [https://console.wmt.akeyless.io](https://console.wmt.akeyless.io)
      </td>

      <td>
        Akeyless SaaS platform.
      </td>
    </tr>

    <tr>
      <td>
        [https://zerotrust.wmt.akeyless.io](https://zerotrust.wmt.akeyless.io)
      </td>

      <td>
        Akeyless Secure Remote Access portal
      </td>
    </tr>

    <tr>
      <td>
        * \*Vault\*\*: [https://vault.wmt.akeyless.io](https://vault.wmt.akeyless.io)
      </td>

      <td>
        User Account Management, managing user account, items, and roles.
      </td>
    </tr>

    <tr>
      <td>
        * \*Auth\*\*: [https://auth.wmt.akeyless.io](https://auth.wmt.akeyless.io)
      </td>

      <td>
        Akeyless Authentication service.
      </td>
    </tr>

    <tr>
      <td>
        * \*Audit\*\* : [https://audit.wmt.akeyless.io](https://audit.wmt.akeyless.io)
      </td>

      <td>
        Audit log main service, enables log forwarding from GW & Bastions.
      </td>
    </tr>

    <tr>
      <td>
        * \*BIS\*\*: [https://bis.wmt.akeyless.io](https://bis.wmt.akeyless.io)
      </td>

      <td>
        Billing Infrastructure Service.
      </td>
    </tr>

    <tr>
      <td>
        * \*Gator\*\*: [https://gator.wmt.akeyless.io](https://gator.wmt.akeyless.io)
      </td>

      <td>
        Main service to sync gateways instances, and connections with Akeyless SaaS.
      </td>
    </tr>

    <tr>
      <td>
        * \*MQ\*\*: amqps\://mq.wmt.akeyless.io
      </td>

      <td>
        Message queue between Akeyless micro-services.
      </td>
    </tr>

    <tr>
      <td>
        * \*KFM\*\*:\
          [https://kfm1.wmt.akeyless.io](https://kfm1.wmt.akeyless.io),\
            

        [https://kfm2.wmt.akeyless.io](https://kfm2.wmt.akeyless.io),  

        [https://kfm3.wmt.akeyless.io](https://kfm3.wmt.akeyless.io)
      </td>

      <td>
        Key Fragments Services, enabling full DFC encryption.
      </td>
    </tr>

    <tr>
      <td>
        * \*Logs\*\*:\
          tcp\://log.wmt.akeyless.io:9997 tcp\://log.wmt.akeyless.io:9443
      </td>

      <td>
        GW logs, mainly to be reflected during failure scenarios.
      </td>
    </tr>
  </tbody>
</Table>

## Command Line Interface (CLI)

There are a handful of ways to interact with Akeyless Vault for managing, creating, and fetching multiple types of supported [secrets](https://docs.akeyless.io/docs/manage-your-secrets-overview). One of them is our Command Line Interface (CLI), which is purpose-built to serve your custom automation scripts (usually within a CI/CD pipeline or backup process), as well as human DevOps/Software engineers.

> 👍 Info
>
> For a full list of the available CLI command, see the [CLI reference](https://docs.akeyless.io/docs/cli-reference).

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
7. [OIDC](https://docs.akeyless.io/docs/openid) (`oidc`)
8. [K8s](https://docs.akeyless.io/docs/kubernetes-auth) (`k8s`)
9. [GCP](https://docs.akeyless.io/docs/gcp-auth-method) (`GCP`)

Use the authentication mode that you also used when you signed up and signed in to the UI, use your username and password credentials, or use the API key Akeyless assigned to you when you signed in for the first time.

If you're not sure what authentication method to use, consult your administrator.\
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
Access ID:  p-abc12de
Ldap Proxy URL: https://Akeyless.GW
Profile ldap successfully configured
```

> 🚧 Warning
>
> **No validation of credentials**\
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
