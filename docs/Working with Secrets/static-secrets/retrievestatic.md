---
title: Retrieve a Static Secret Value
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
You can retrieve a static secret value directly from the [Akeyless CLI](doc:retrievestatic#retrieve-a-static-secret-value-from-the-akeyless-cli) or from the [Akeyless Console](doc:retrievestatic#retrieve-a-static-secret-value-from-the-akeyless-console).

> 👍 Note
>
> You can also retrieve secret values directly from within a context you choose, such as from Kubernetes, Jenkins, Azure, or another of our integrations, or with the help of any of our SDKs. For details, see [Akeyless Plugins](doc:plugins) and [SDKs](doc:sdks).

# Retrieve a Static Secret Value from the Akeyless CLI

Let’s retrieve a static secret value using the Akeyless CLI. If you’d prefer, see how to do this from the [Akeyless Console](doc:retrievestatic#retrieve-a-static-secret-value-from-the-akeyless-console) instead.

The CLI command to retrieve a Static Secret value is:

```shell Shell
akeyless get-secret-value --name <secret name> --version <version number>
```

where:

* `--name`: The name of the static secret whose value to retrieve.

* `--version`: Optional, the version number of the secret value to retrieve. If you do not include this argument, the latest version of the secret value will be retrieved.

For example, to retrieve the value of the **MyFirstSecret** static secret, type:

```shell Shell
akeyless get-secret-value --name MyFirstSecret
```

# Retrieve a Static Secret Value from the Akeyless Console

Let’s retrieve a static secret value from the Akeyless Console. If you’d prefer, see how to do this from the [Akeyless CLI](doc:retrievestatic#retrieve-a-static-secret-value-from-the-akeyless-cli) instead.

1. Log in to the Akeyless Console and go to **Items**.

2. Select the static secret.

3. By default, the secret value is encrypted. To the right of the **Value** field, select the eye icon. The decrypted secret value appears.

> 👍 Note
>
> Select **copy to clipboard** to decrypt the secret value and copy it to the clipboard.
