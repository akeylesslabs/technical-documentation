---
title: Rotated Secrets
slug: rotated-secrets
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
Rotated Secrets enable you to protect the credentials for privileged-user accounts such as an _Administrator_ account on a Windows Server, a **root** account on a Linux server, or an **Admin** account on a network device, by resetting its password.

Setting up Rotated Secrets requires the **Rotated Secret** permission on the Gateway. You can also set the **Rotate Secret Value** permission to allow rotation of the secret value without granting edit rights (this also requires **Read** permission on the rotated secret item).

![Illustration for: Setting up Rotated Secrets requires the Rotated Secret permission on the Gateway. You can also set the Rotate Secret Value permission to allow rotation of the secret…](https://files.readme.io/f32a578-Rotated_Secret.png)

The Akeyless Platform generates a new password, resets it on the target machine, and stores the updated secret value so that it can be retrieved when required.

You can define a rotated secret to automatically update the password at defined intervals, or manually trigger a password update with the CLI or from the Akeyless Console. You can also configure password policy settings (such as length and complexity requirements) for supported rotated secret types. For details, see [Password Policy for Dynamic and Rotated Secrets](https://docs.akeyless.io/docs/secrets-password-policy).

You can configure:

* [AWS Rotated Secret](https://docs.akeyless.io/docs/create-an-aws-rotated-secret)
* [Azure Rotated Secret](https://docs.akeyless.io/docs/create-an-azure-rotated-secret)
* [Database Rotated Secret](https://docs.akeyless.io/docs/create-a-database-rotated-secret)
* [Docker Hub Rotated Secret](https://docs.akeyless.io/docs/create-a-docker-hub-rotated-secret)
* [GCP Rotated Secret](https://docs.akeyless.io/docs/gcp-rotated-secret)
* [HashiCorp Vault Rotated Secret](https://docs.akeyless.io/docs/create-a-hashicorp-vault-rotated-secret)
* [LDAP Rotated Secret](https://docs.akeyless.io/docs/create-an-ldap-rotated-secret)
* [Linked Target Rotated Secret](https://docs.akeyless.io/docs/linked-target-rotated-secret)
* [Splunk Rotated Secret](https://docs.akeyless.io/docs/splunk-rotated-secret)
* [SSH Rotated Secret](https://docs.akeyless.io/docs/create-an-ssh-rotated-secret)
* [Windows Rotated Secret](https://docs.akeyless.io/docs/windows-rotated-secret)
* [Custom Rotated Secret](https://docs.akeyless.io/docs/create-a-custom-rotated-secret)

The typical flow for working with Rotated Secrets is:

1. [Create a Target for a Rotated Secret](https://docs.akeyless.io/docs/targets): Get started by defining the target. The rotated secret itself is a user account on the target, for which the password needs to be rotated every `X` days.

2. [Create an SSH Rotated Secret](https://docs.akeyless.io/docs/create-an-ssh-rotated-secret) or [Create an AWS Rotated Secret](https://docs.akeyless.io/docs/create-an-aws-rotated-secret): When you create a rotated secret, you need to name it and define the secret settings, such as how often the secret should be rotated, and the secret target. All secret values are encrypted using patented Akeyless Distributed Fragment Cryptography (DFC) technology.

3. [Add a Rotated Secret to a Role](https://docs.akeyless.io/docs/add-a-static-secret-to-an-access-role): Enable clients to access the rotated secret by adding it to a role, with the appropriate permissions.

4. [Retrieve a Rotated Secret Value](https://docs.akeyless.io/docs/retrieve-secret): Get the value of a rotated secret when you need it.

If required, you can manually rotate a secret. When a rotated secret becomes obsolete, you can delete it.

## Tutorial

Check out our tutorial video on [Creating and Using Rotated Secrets](https://tutorials.akeyless.io/docs/creating-and-using-rotated-secrets).
