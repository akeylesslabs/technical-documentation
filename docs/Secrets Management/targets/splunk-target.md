---
title: Splunk Target
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define a [Splunk](https://www.splunk.com/en_us/download/splunk-enterprise.html) target to be used with [Splunk Rotated Secret](https://docs.akeyless.io/docs/splunk-rotated-secret).

## Create a Splunk Target with the CLI

To create a Splunk target with the CLI, run the following command:

```shell
akeyless target create splunk \
--name <Target Name> \
--url <Server URL> \
--use-tls[=true] \
--username <Splunk Username> \
--password <Splunk Password> \
--splunk-token <Splunk Token> \
--token-owner <Splunk token owner> \
--audience <Splunk token audience>
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `url`: The Splunk server URL.

* `username`:  The Splunk Username.

* `password`: The Splunk Password.

* `splunk-token`: The Splunk Token.

* `token-owner`: The Splunk token owner username (relevant when using token authentication for rotation).

* `audience`: The Splunk token audience (relevant when using token authentication for rotation).

[View the complete list of parameters for this command.](https://docs.akeyless.io/docs/cli-ref-targets#splunk)

## Create a Splunk Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Infra (Splunk)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
   For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

4. Define the remaining parameters as follows:

   * **Splunk URL:** The **Splunk** server URL.

   * **Auth Mode**: In this section, you can select the preferred type of authentication with the Splunk server either `Username` or `Token`:
     * Select the **Username** option to authenticate with **Username** and **Password**
     * Select the **Token** option to authenticate with a **token**.

   * **TLS**: Enable this option to use a **secure (TLS) connection**.

   * **Certificate**: Upload a certificate to secure the connection if one doesn’t already exist.
