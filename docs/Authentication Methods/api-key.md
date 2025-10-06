---
title: API Key
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: API Key
  description: ''
  robots: index
next:
  description: >-
    Make sure to associate your new Authentication Method with an Access Role to
    grant the relevant permissions within Akeyless.
---
API Key is a simple [Authentication Method](doc:access-and-authentication-methods) supported by the Akeyless Platform. API Keys are very popular primarily for testing or staging environments.

<Image align="center" border={false} src="https://files.readme.io/574347a-API_key_auth.png" />

# Create an API Key Authentication Method from the CLI

Let's create a new API Key authentication method using the Akeyless CLI. (You can do this also from the [Akeyless Console](https://docs.akeyless.io/docs/api-key#create-an-api-key-authentication-method-in-the-akeyless-console).)

To create an API Key authentication method from the CLI, run the following command:

```shell Create API Key
akeyless auth-method create api-key --name MyFirstAPIKey
```

Where:

* `name`: A unique name for the authentication method. The name can include the path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

> 🚧 Note
>
> Akeyless API Key is displayed only once.

You can find the complete list of additional parameters for this command in the [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#p-stylecolorblueapi-keyp) section.

# Configure Akeyless CLI with the API Key authentication method

To configure your CLI to work with API Key authentication, run the following command:

```shell Akeyless CLI
akeyless configure --profile default --access-id <AccessID>  --access-key < API Key>
```

# Create an API Key authentication method in the Akeyless Console

1. Log in to the Akeyless Console and go to **Users & Auth Methods > New > API Key**.

2. Define a **Name** for the authentication method, and specify the **Location** as a path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

3. Define the remaining parameters as follows:

* **Expiration Date:** Select the access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.

* **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean CURL, SDK, etc. This parameter is optional. Leave it empty for unrestricted access.

* **Allowed Trusted Gateway IPs:** Comma separated CIDR blocks. If specified, the Gateway using this IP range will be trusted to forward the original client IP. If empty, the Gateway's IP address will be used.

* **Audit Log Sub Claims:** Enter a comma-separated list of sub-claims keys to be included in the audit logs.

4. Click **Finish**.

5. Download a CSV file with the **Access ID** and **Access Key**.

# Tutorial

Check out our tutorial video on [Authentication Methods and API Key Authentication](https://tutorials.akeyless.io/docs/authentication-methods-and-api-key-authentication).
