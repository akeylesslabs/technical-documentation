---
title: Create a Static Secret
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: >-
    Assign the Static Secret to an Access Role that defines who can access the
    secret, and with what kind of permissions.
  pages:
    - type: basic
      slug: add-a-static-secret-to-an-access-role
      title: Add a Static Secret to an Access Role
---
When you create a static secret, you need to name it and provide the secret value. All secret values are encrypted using patented Akeyless Distributed Fragment Cryptography™ (DFC) technology.

# Create a Static Secret from the Akeyless CLI

Let’s create a static secret using the Akeyless CLI. If you’d prefer, see how to do this from the [Akeyless Console](doc:create-secret#create-a-static-secret-from-the-akeyless-console) instead.

The CLI command to create a static secret is:

```shell Akeyless CLI
akeyless create-secret --name &lt;secret name&gt; --value &lt;secret value&gt;
```

where:

* `name`: A unique name for the secret. The name can include the path to the virtual folder in which you want to create the new secret, using slash `/` separators. If the folder does not exist, it will be created together with the secret.

* `value`: The value of the secret. The secret value maximum size is 16KB.

For example, to create a secret in the **Admin** folder called **AdminCredentials** with the value **Admin101!**, type:

```shell Akeyless CLI
akeyless create-secret --name /Admin/AdminCredentials --value Admin101!
```

The response should be like this:

```shell
$ A new secret named /Admin/AdminCredentials was successfully created
```

> 👍 Note
>
> For details about these CLI command options, see the [CLI Command Reference](https://docs.akeyless.io/docs/cli-reference-static-secrets).

Next, assign the static secret to an access role that defines who can access the secret value, and with what permissions. For details, see [Add a Static Secret to an Access Role](doc:add-a-static-secret-to-an-access-role).

# Create a Static Secret from the Akeyless Console

Let’s create a static secret using the Akeyless Console. If you’d prefer, see how to do this from the [Akeyless CLI](doc:create-secret#create-a-static-secret-from-the-akeyless-cli) instead.

1. Log in to the Akeyless Console and go to **Items > New > Static Secret**.

2. Define a **Name** for the secret, and optionally specify the **Location** as a path to the virtual folder in which you want to create the new secret, using slash `/` separators. If the folder does not exist, it will be created together with the secret.

3. Define the remaining parameters as follows:

* **Description:** Optional, enter a description of the secret.

* **Tags:** Optional, select one or more tags for the secret, or enter the name of a new tag to be added as part of the secret creation.

* **Delete Protection:** Prevent accidental deletion.

* **Protection Key:**  Select the encryption key with which to encrypt the secret (if your system includes multiple encryption keys). Otherwise, select `Default`.

* **Format:** The format type of the value either **Text** , **JSON** or **Key/Value**.

* **Value:** Enter the value of the secret. The value length should be 16KB.

* **Change Event** Optional, trigger an event when the value is changed.

3. Select **Save**.

# Tutorial

Check out our tutorial video on [Creating and Updating a Static Secret](https://tutorials.akeyless.io/docs/creating-a-static-secret) .
