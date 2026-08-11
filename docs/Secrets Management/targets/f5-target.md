---
title: F5 Target
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define an F5 Target to store the credentials of a privileged F5 BIG-IP administrator account.

An F5 Target can be used to [provision certificates](https://docs.akeyless.io/docs/certificate-provisioning) to remote servers, and to create an F5 [Rotated Secret](https://docs.akeyless.io/docs/rotated-secrets) to rotate the target's admin password.

## Create an F5 Target with the CLI

To create an F5 target with the CLI, run the following command:

Shell

```
akeyless target create f5-big-ip \
--name <Target name> \
--url <F5 Big IP target URL> \
--username <F5 username> \
--password <F5 username password>
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

- `url`: The F5 BIG-IP target URL.

- `username`: An F5 username with permission to manage certificates.

- `password`: The password of the F5 username.

- `key`: **Optional**, a key name to be used to encrypt the target secret value. If a key name is not specified, the account default protection key is used.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets) section.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  When associating a certificate item with an F5 Target for provisioning, use the `--f5-certificate-type` flag on the `assoc-target-item` command to specify whether the certificate should be provisioned as a `traffic` or `device` certificate on the F5 BIG-IP device. Defaults to `traffic`.
</Callout>

## Create an F5 Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Infra (F5 BIG-IP)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

4. Define the remaining parameters as follows:

   - **F5 BIG-IP URL:** The F5 BIG-IP target URL.

   - **Username:** An F5 username with permission to manage certificates.

   - **Password:** The password of the F5 username.

5. Click **Finish**.
