---
title: Sync a Rotated Secret
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
[Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets) can be configured with a **sync** setting, ensuring that upon manual or automatic rotation, the latest value of your secret will be **synced** by way of the relevant [Universal Secrets Connector](https://docs.akeyless.io/docs/universal-secrets-connector) automatically.

## Syncing a Rotated Secret with the CLI

Run the following command to sync a rotated secret to an external Secret Management solution using the CLI:

```shell
akeyless rotated-secret sync \
--name <Rotated Secret name> \
--usc-name <USC name> \
--remote-secret-name <remote secret name>
---filter-secret-value <jq expression>
```

Where:

* `name`: The Rotated Secret name.

* `usc-name`: The name of the Universal Secret Connector.

* `remote-secret-name`: Remote Secret Name that will be created on the remote endpoint. If the secret already exists, sync updates the secret value.

> ℹ️ **Note (AWS metadata):**
>
> For AWS Universal Secrets Connector, Akeyless-initiated sync keeps existing AWS-side custom tags and description unless those fields are explicitly updated.

* `filter-secret-value`: Optional, to filter the value of the rotated secret, to sync only specific fields, or to manipulate the value using a jq expression, for example, `.password` and so on.

> ℹ️ **Note (Format restrictions):**
>
> Kubernetes and HashiCorp targets enforce that secrets are in JSON format, which means a valid jq filter could be, for example: `{"password": .password}`

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#sync) section.

## Syncing a Rotated Secret from the Console

1. Log in to the Akeyless Console, and navigate to the [Rotated Secret](https://docs.akeyless.io/docs/rotated-secrets) item.
2. Go to the **Sync** tab on the secret item and click **Attach**.
3. Set the following settings:

* **Universal Secret Connector Name:** Choose the target **Universal Secret Connector**.

* **Remote Secret Name:** Enter the name of the secret that will be created or updated on the remote endpoint.

* **Filter secret value (jq)**: Optional, to filter the value of the rotated secret, to sync only specific fields, or to manipulate the value using a jq expression, for example, `.password` and so on.

> ℹ️ **Note (Format restrictions):**
>
> Kubernetes and HashiCorp targets enforce that secrets are in JSON format, which means a valid jq filter could be, for example: `{"password": .password}`

Click **Save** to synchronize the rotated secret.

If an automatic sync fails, an event is triggered. In that case, you can perform a **manual sync** from this tab.
