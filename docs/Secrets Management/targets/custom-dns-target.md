---
title: Custom DNS Target
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define a Custom DNS target for **ACME DNS-01** challenges, leveraging DNS providers supported by the [Lego project](https://go-acme.github.io/lego/dns/index.html).

## Create a Custom DNS Target with the CLI

To create a Custom DNS target with the CLI, run the following command:

```shell
akeyless target create custom-dns \
  --name <target name> \
  --provider-type <DNS provider> \
  --dns-parameter <key|value>
```

Where:
- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
- `provider-type`: The DNS provider type. All DNS providers available through the [Lego project](https://go-acme.github.io/lego/dns/index.html) are supported.
- `dns-parameter`: The parameters for the DNS provider.

You can find the complete list of parameters for this command in the CLI Reference - Akeyless Targets section.

## Create a Custom DNS Target in the Console

1. Log in to the Akeyless Console, and go to **Targets** > **New** > **Other (Custom DNS)**.
2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
   For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).
4. Define the remaining parameters as follows:
   - **DNS Provider**: The DNS provider type. All DNS providers available through the [Lego project](https://go-acme.github.io/lego/dns/index.html) are supported.
   - **DNS Parameters**: The parameters for the DNS provider.