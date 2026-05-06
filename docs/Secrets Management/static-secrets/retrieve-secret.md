---
title: Retrieve a Secret Value
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
You can retrieve a secret value directly from the [Akeyless CLI](https://docs.akeyless.io/docs/retrieve-secret#retrieve-a-secret-value-from-the-akeyless-cli) or from the [Akeyless Console](https://docs.akeyless.io/docs/retrieve-secret#retrieve-a-secret-value-from-the-akeyless-console).

> ℹ️ **Note:**
>
> You can also retrieve secret values directly from within a context you choose, such as from Kubernetes, Jenkins, Azure, or another of our integrations, or with the help of any of our SDKs. For details, see [Akeyless Plugins](https://docs.akeyless.io/docs/plugins-overview) and [SDKs](https://docs.akeyless.io/docs/sdks).

## Retrieve a Secret Value from the Akeyless CLI

Let’s retrieve a secret value using the Akeyless CLI. If you’d prefer, see how to do this from the [Akeyless Console](https://docs.akeyless.io/docs/retrieve-secret#retrieve-a-secret-value-from-the-akeyless-console) instead.

The CLI command to retrieve a Secret value is:

```shell
akeyless get-secret-value --name <secret name> --version <version number>
```

where:

* `--name`: The name of the secret whose value to retrieve.

* `--version`: Optional, the version number of the secret value to retrieve. If you do not include this argument, the latest version of the secret value will be retrieved.

For example, to retrieve the value of the **MyFirstSecret** secret, type:

<!-- secret-stdout-scan:ok -->
```shell
akeyless get-secret-value --name MyFirstSecret
```

## Retrieve a Secret Value from the Akeyless Console

Let’s retrieve a secret value from the Akeyless Console. If you’d prefer, see how to do this from the [Akeyless CLI](https://docs.akeyless.io/docs/retrieve-secret#retrieve-a-secret-value-from-the-akeyless-cli) instead.

1. Log in to the Akeyless Console and go to **Items**.

2. Select the secret.

3. By default, the secret value is encrypted. To the right of the **Value** field, select the eye icon. The decrypted secret value appears.

> ℹ️ **Note:**
>
> Select **copy to clipboard** to decrypt the secret value and copy it to the clipboard.
