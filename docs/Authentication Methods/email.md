---
title: Email
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Email
  description: ''
  robots: index
next:
  description: >-
    Make sure to associate your new Authentication Method with an Access Role to
    grant the relevant permissions within Akeyless.
---
When setting up your Akeyless account, you will assign it an email address and a password. This authentication method will allow you to invite your teammates to join your account and utilize the items and resources in it using their email addresses and setting up their own passwords.\
While this flow is simple and easy to use, we recommend you mainly use it for basic onboarding.

# Creating an Email Authentication in the CLI

Let's create a new Email authentication method using the Akeyless CLI. (You can do this also from the Akeyless Console.)

To create an email authentication method from the CLI, run the following command:

```shell
akeyless auth-method create email \
--name <Auth Method Name> \
--email <Email Address>
```

Where:

* `name`:  A unique name for the authentication method. The name can include the path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.
* `email`: The User email address

You can find the complete list of additional parameters for this command in the [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#p-stylecolorblueemailp) section.

# Creating an Email Authentication in the Console

1. Log in to the Akeyless Console and go to **Users & Auth Methods > New > User (Email)**.

2. Define a **Name** for the authentication method, and specify the **Location** as a path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

3. Define the remaining parameters as follows:

* **Expiration Date:** Select the access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.

* **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean CURL, SDK, etc. This parameter is optional. Leave it empty for unrestricted access.

* **Allowed Trusted Gateway IPs:** Comma separated CIDR blocks. If specified, the Gateway using this IP range will be trusted to forward the original client IP. If empty, the Gateway's IP address will be used.

* **Audit Log Sub-Claims:** Include the following sub-claims values in audit logs.

* **JWT TTL (in minutes):** The timespan from acceptance of the invitation to the JWT expiration.

On the **Email Configuration** step define the following:

* **Email:** The email address of the invite recipient.

* **Set Two-Factor Authentication:** Optional, Select to set 2-Factor Authentication.

4. Click **Finish**.

Saving will automatically send an invitation email to the specified address with a link to set a password and log in to the account.
