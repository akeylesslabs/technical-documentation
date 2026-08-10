---
title: Aerospike Dynamic Secrets
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define an Aerospike dynamic secret to generate user credentials dynamically based on configured roles.

## Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview)

- An [Aerospike Target]()

## Create a Dynamic Aerospike Secret with the CLI

To create an Aerospike dynamic secret with the CLI using an existing [Aerospike Target](https://docs.akeyless.io/docs/aerospike-target), run the following command:

```shell
akeyless dynamic-secret create aerospike \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--aerospike-roles <Comma-separated list of Aerospike roles> \
--password-length 16
```

Where:

- `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

- `target-name`: A name of the target that enables connection to the Aerospike cluster. The name can include the path to the virtual folder where this target resides.

- `gateway-url`: Akeyless Gateway URL (port `8000`).

- `aerospike-roles`: Comma-separated list of built-in or custom Aerospike roles to assign to the temporary user, for example: `read-write,sys-admin`.

- `password-length`: **Optional** The temporary user password length.

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#aerospike) section.

## Create a Dynamic Aerospike Secret in the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the Aerospike secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

- **Delete Protection:** When enabled, it protects the secret from accidental deletion.

- **Target:** Select an existing [Aerospike Target](https://docs.akeyless.io/docs/aerospike-target).&#x20;

- **Aerospike** **Roles:** Select one or more Aerospike roles to assign to the temporary user, either built-in roles (for example, `read`, `read-write`, `read-write-udf`, `data-admin`, `sys-admin`, `user-admin`, `udf-admin`, `sindex-admin`) or custom roles already defined on the cluster.

- **Password Policy:** Set the password policy.&#x20;

- **User TTL:** Provide a time-to-live value for a dynamic secret. When TTL expires, the temporary user is removed.

- **Gateway:** Select the Gateway through which the dynamic secret will create users.

- **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

5. Click **Finish**.

##
