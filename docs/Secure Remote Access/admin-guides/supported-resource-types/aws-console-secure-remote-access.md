---
title: AWS Console Access
excerpt: Secure remote access to the AWS Console
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
You can enable secure remote access to AWS with a Dynamic Secret that generates ephemeral credentials for AWS or a Rotated Secret. Users can then access AWS from the Secure Remote Access Portal, either over the web or using the native AWS CLI.

> 👍 Note
>
> Use [Akeyless Connect](https://docs.akeyless.io/docs/akeyless-connect) command to access the AWS Console from any UNIX terminal.

# Prerequisites

To enable secure remote access to AWS you need:

* The [Secure Remote Access](https://docs.akeyless.io/docs/remote-access-setup-overview) deployed.

* The [Akeyless Browser Extension](https://docs.akeyless.io/docs/browser-extensions).

In addition, for users to access the AWS Console using the CLI, you need:

* An [SSH Certificate](https://docs.akeyless.io/docs/ssh-certificates) for certificate authentication.

# Create an AWS Secret

If you don't already have an AWS secret, see the following docs to either create a [Dynamic Secret](https://docs.akeyless.io/docs/aws-producer) or [Rotated Secret](https://docs.akeyless.io/docs/create-an-aws-rotated-secret) that specifies the AWS account details and access credentials.

If you already have a relevant secret, continue below.

# Set Up Remote Access to the AWS Console from the Akeyless CLI

Let's set up remote access to the AWS Console using the Akeyless CLI. If you’d prefer, see how to do this from the [Akeyless Console](https://docs.akeyless.io/docs/aws-console-secure-remote-access#set-up-remote-access-to-the-aws-console-from-the-akeyless-console) instead.

Run the relevant command to define the following fields to the secret that specifies the AWS account details and access credentials:

```shell Dynamic Secret
akeyless dynamic-secret update aws \
--name <dynamic secret name> \
--secure-access-enable true \
--secure-access-aws-account-id <AWS account id> \
--secure-access-aws-native-cli <true/false> \
--secure-access-certificate-issuer </Path/to/SSH/Cert/Issuer>
```
```shell Rotated Secret
akeyless rotated-secret update aws \
--name <rotated secret name> \
--secure-access-enable true \
--secure-access-aws-account-id <AWS account id> \
--secure-access-aws-native-cli <true/false> \
--secure-access-certificate-issuer </Path/to/SSH/Cert/Issuer> \
--rotate-after-disconnect <true|false>
```

where:

* **secure-access-aws-account-id:** The AWS account ID, as defined in the dynamic secret.
* **secure-access-aws-region:** Optional, only required to enable CLI access.  the AWS region the user is permitted to access.
* **secure-access-aws-native-cli:** Optional, specifies to use the native AWS CLI wrapper.
* **secure-access-certificate-issuer:** Optional, only required to enable CLI access. The path to the SSH certificate issuer that should be used for certificate authentication.
* **rotate-after-disconnect:** Optional for Rotated Secret. Rotate the secret value when the SRA session ends.

By default, access to the AWS portal will use a direct network access mode. To work with Akeyless [Web Access](https://docs.akeyless.io/docs/web-access-bastion) for session isolation or as a secure proxy entry point, please set **one** of the following:

* **secure-access-web-browsing:** Optional, secure browser via Akeyless Web Access Zero trust Web Access.

Alternatively, in case you prefer to work with the Akeyless bastions as a proxy entry point, set this parameter as true:

* **secure-access-web-proxy:** Optional, web-proxy via Akeyless Zero trust Web Access.
* **secure-access-delay:** The delay duration, in seconds, to wait after generating just-in-time credentials. Accepted range: 0-120 seconds

# Set Up Remote Access to the AWS Console from the Akeyless Console

Let's set up remote access to the AWS Console from the Akeyless Console. If you'd prefer, see how to do this from the [Akeyless CLI](https://docs.akeyless.io/docs/aws-console-secure-remote-access#set-up-remote-access-to-the-aws-console-from-the-akeyless-cli) instead.

1. Log in to the Akeyless Console and go to **Items**.

2. Select the dynamic secret that specifies the AWS details and access credentials.

3. Click on the **Secure Remote Access** tab, select the pencil icon and enable **Secure Remote Access**, then fill in the following fields:

* `AWS Account ID `: The AWS account ID, as defined in the dynamic secret.
* `Rotate after disconnection`: Optional for Rotated Secret. Rotate the secret value when the SRA session ends.

For **Web Access**, choose one of the following modes:

* `Direct connection`: Default, using a direct connection to AWS portal via Akeyless Secure Remote Access.

* `Secure Web Browsing`: Optional, secure web browsing over an isolated web browser **available only with** [Zero Trust Web Access](https://docs.akeyless.io/docs/web-access-bastion).

* `Secure Web Proxy`: Optional, secure web proxy mode **available only with** [Zero Trust Web Access](https://docs.akeyless.io/docs/web-access-bastion).

For **CLI Access**:

* `Default Region`: Optional, only required to enable CLI access, the AWS region the user is permitted to access.
* `Bastion Issuer`: Optional, only required to enable CLI access. The path to the SSH certificate issuer that should be used for certificate authentication.
* `AWS Native CLI`: Optional, specifies to use AWS CLI native wrapper.

4. To the right of the **Enable Secure Remote Access** field, select the tick mark icon to save your changes.

> 📘 Custom Delay
>
> You can specify a custom delay, measured in seconds [0 - 120], before a newly generated dynamic secret becomes usable. This additional wait time helps target systems complete their sync process with the updated credentials

# Access the AWS Console over the Web from the Secure Remote Access Portal

1. [Log in](https://docs.akeyless.io/docs/access-resources-remotely#connect-from-the-secure-remote-access-portal) to the Secure Remote Access Portal and select **AWS Console**.

2. Select the required target, then select **Web**.
   A new tab opens to the AWS Console sign-in page, and Akeyless injects the credentials generated by the dynamic secret for the temporary user.

> 📘 Info
>
> The temporary user is created when you request access to the AWS Console. As this may take a few seconds, please wait a few seconds for the credentials to be injected before you try sign in.

# Access the AWS Console Using CLI from the Secure Remote Access Portal

1. [Log in](https://docs.akeyless.io/docs/access-resources-remotely#connect-from-the-secure-remote-access-portal) to the Secure Remote Access Portal and select **AWS Console**.

2. Select the required target, then select **CLI**.
   A new tab opens, showing that you are connected to the AWS Console.

# Access the AWS Console using Akeyless connect command

[Akeyless Connect](https://docs.akeyless.io/docs/akeyless-connect) command enables application native CLI access:

```shell
akeyless connect -t <AWS Region> -g <your-gateway-ip[:port]> -n "/path/to/AWS-dynamic-secret"
```

<br />
