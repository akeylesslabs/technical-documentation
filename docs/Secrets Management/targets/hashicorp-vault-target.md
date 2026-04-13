---
title: HashiCorp Vault Target
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
You can define a HashiCorp Vault target to be used with [HashiCorp Vault Universal Secrets Connector](https://docs.akeyless.io/docs/hc-vault-universal-secrets-connector)

## Create a HashiCorp Vault Target with the CLI

To create an **HashiCorp Vault** target with the CLI, run the following command:

```shell
akeyless target create hashi-vault \
--name <target name> \
--hashi-url 'https://<your-vault-api-url>:8200' \
--vault-token <Access Token> \
--namespace <Namespace Name>
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `hashi-url`: HashiCorp Vault URL, for example, `https://vault-mgr01:8200`.

* `vault-token`: Vault access token with sufficient permissions.

* `namespace`: List of vault namespaces. To specify multiple namespaces use the argument multiple times: `--namespace ns1` `--namespace ns2`

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#hashi-vault) section.

## Create a HashiCorp Vault Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Other > HashiCorp Vault**

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

4. Set the maximum versions for the target.

5. Define the remaining parameters as follows:

    * **Token:** Vault access token with [sufficient permissions](https://developer.hashicorp.com/vault/docs/concepts/policies) that will be used for authentication.

    * **URL:** Vault URL.

    * **Namespace:** Enter the [Namespace](https://developer.hashicorp.com/vault/docs/enterprise/namespaces) in which your vault resources are located.

6. Click **Finish**.
