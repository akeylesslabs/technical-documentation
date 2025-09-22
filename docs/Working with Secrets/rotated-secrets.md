---
title: Rotated Secrets
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
Rotated secrets enable you to protect the credentials for privileged-user accounts such as an _Administrator_ account on a Windows server, a **root** account on a Linux server, or an **Admin** account on a network device, by resetting its password.

Setting up Rotated Secrets requires the **Rotated Secret** permission on the Gateway. You can also set the **Rotate Secret Value** permission to allow rotation of the secret value without granting edit rights (this also requires **Read** permission on the rotated secret item).

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/f32a578-Rotated_Secret.png",
        "rotated-secret.png",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


The Akeyless Platform generates a new password, resets it on the target machine, and stores the updated secret value so that it can be retrieved when required.

You can define a rotated secret to automatically update the password at defined intervals, or manually trigger a password update from the CLI or from the Akeyless Console. You also have the ability to set a custom password length for each individual rotated secret.

You can configure:

- [SSH Rotated Secret](doc:create-an-ssh-rotated-secret) 
- [AWS Rotated Secret](doc:create-an-aws-rotated-secret) 
- [Azure Rotated Secret](doc:create-an-azure-rotated-secret) 
- [GCP Rotated Secret](https://docs.akeyless.io/docs/gcp-rotated-secret)
- [Database Rotated Secret](doc:create-a-database-rotated-secret) 
- [Windows Rotated Secret](https://docs.akeyless.io/docs/windows-rotated-secret)
- [Custom Rotated Secret](doc:create-a-custom-rotated-secret) 
- [LDAP Rotated Secret](doc:create-an-ldap-rotated-secret) 
- [Linked Target Rotated Secret](doc:linked-target-rotated-secret)
- [Docker Hub Rotated Secret](doc:create-a-docker-hub-rotated-secret) 

The typical flow for working with rotated secrets is:

1. [Create a Target for a Rotated Secret](doc:targets): Get started by defining the target. The rotated secret itself is a user account on the target, for which the password needs to be rotated every `X` days.

2. [Create an SSH Rotated Secret](doc:create-an-ssh-rotated-secret) or [Create an AWS Rotated Secret](doc:create-an-aws-rotated-secret): When you create a rotated secret, you need to name it and define the secret settings, such as how often the secret should be rotated, and the secret target. All secret values are encrypted using patented Akeyless Distributed Fragment Cryptography (DFC) technology. 

3. [Add a Rotated Secret to a Role](doc:add-a-rotated-secret-to-a-role):  Enable clients to access the rotated secret by adding it to a role, with the appropriate permissions.

4. [Retrieve a Rotated Secret Value](doc:retrieve-a-rotated-secret-value): Get the value of a rotated secret when you need it.

If required, you can manually rotate a secret. See [Manually Rotate a Secret](doc:manually-rotate-a-secret). 

When a rotated secret becomes obsolete, you can delete it.

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/creating-and-using-rotated-secrets" target="_blank">Creating and Using Rotated Secrets</a>.