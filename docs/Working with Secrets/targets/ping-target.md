---
title: Ping Target
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
You can define a Ping target to be used with [Ping Dynamic Secrets](https://docs.akeyless.io/docs/ping-dynamic-secrets).

# Working with Ping Targets in the CLI

## Create a Ping Target in the CLI

To create a Ping target from the CLI, run the following command:

```shell
akeyless target create ping \
--name <Target name> \
--ping-url <Ping url> \
--privileged-user <Username> \
--password <Password>
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `ping-url`: The Ping service URL.

* `privileged-user`: A username of a user on your Ping service that may create `OAuth` Clients through Ping Federate Administrative API.

* `password`: The password of the privileged user.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorbluepingp) section.

## Update a Ping Target in the CLI

You may update the target information using the same parameters with the following command:

```shell
akeyless update-ping-target
```

If you wish to change the target name, add a `new-name` parameter.

# Create a Ping Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Infra (Ping)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.\
   For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

4. Define the remaining parameters as follows:

* **Ping URL:** A URL address related to the Ping service.

* **Privileged User:** A username of a user on your Ping service that may create OAuth Clients through Ping Federate Administrative API.

* **Password:** Password related to the privileged user.

* **Administrative Port:** Ping Federate administrative port, default is `9999`.

* **Authorization Port:** Ping Federate authorization port, default is `9031`.

5. Click **Finish**.
