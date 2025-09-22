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
[Rotated Secrets](doc:rotated-secrets) can be configured with a **sync** setting, ensuring that upon manual or automatic rotation, the latest value of your secret will be **synced** via the relevant [Universal Secrets Connector](doc:universal-secrets-connector) automatically.

# Syncing a Rotated Secret from the CLI

Run the following command to sync a rotated secret to an external Secret Management solution using the CLI:

```shell
akeyless rotated-secret sync \
--name <Rotated Secret name> \
--usc-name <USC name> \
--remote-secret-name <remote secret name>
---filter-secret-value <jq expression>
```

Where:

- `name`: The Rotated Secret name.

- `usc-name`: The name of the Universal Secret Connector.

- `remote-secret-name`: Remote Secret Name that will be created on the remote endpoint. If the secret already exists, sync will override its value and tags.

- `filter-secret-value`: Optional, to filter the value of the rotated secret, to sync only specific fields, or to manipulate the value using a jq expression, e.g. `.password` etc.

> 👍 Format restrictions
> 
> K8s & Hashicorp target enforces that secrets will be in a JSON format, meaning that a valid JQ filter would be for example:  `{"password": .password}`

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#sync) section.

# Syncing a Rotated Secret from the Console

1. Log in to the Akeyless Console, and navigate to the [Rotated Secret](doc:rotated-secrets) item.
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