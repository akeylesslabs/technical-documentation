---
title: Sync a Static Secret
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
[Static Secrets](https://docs.akeyless.io/docs/static-secrets) can be configured with a **sync** setting, ensuring that any change to the secret’s value is automatically synced through the relevant [Universal Secrets Connector](https://docs.akeyless.io/docs/universal-secrets-connector).

# Syncing a Static Secret from the CLI

Run the following command to sync a Static secret to an external Secret Management solution using the CLI:

```shell
akeyless static-secret-sync \
--name <Static Secret name> \
--usc-name <USC name> \
--remote-secret-name <remote secret name>
```

Where:

- `name`: The Static Secret name.
- `usc-name`: The name of the Universal Secret Connector.
- `remote-secret-name`: Remote Secret Name that will be created on the remote endpoint. If the secret already exists, sync will override its value and tags.

You can find the complete list of parameters for this command in the [CLI Reference - Static Secrets section](https://docs.akeyless.io/docs/cli-reference-static-secrets#p-stylecolorbluestatic-secret-syncp).

# Syncing a Static Secret from the Console

1. Log in to the Akeyless Console, and navigate to the [Static Secret](https://docs.akeyless.io/docs/cli-reference-static-secrets) item
2. Go to the **Sync** tab on the secret item and click **Attach**.
3. Set the following settings: 

- **Universal Secret Connector Name:** Choose the target **Universal Secret Connector**.

- **Remote Secret Name:** Enter the name of the secret that will be created or updated on the remote endpoint.

- **Filter secret value (jq)**: Optional, to filter the value of the rotated secret, to sync only specific fields, or to manipulate the value using a jq expression, e.g. `.password` etc.

> 👍 Format restrictions
> 
> K8s & Hashicorp target enforces that secrets will be in a JSON format, meaning that a valid JQ filter would be for example:  `{"password": .password}`

Click on **Save** to synchronize the rotated secret. 

In case an automatic sync fails, an event will be triggered. In that case, you will be able to perform a **manual sync** from this tab.