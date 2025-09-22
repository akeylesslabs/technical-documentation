---
title: LDAP Target
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
You can define an LDAP target to be used with [LDAP dynamic secrets](https://docs.akeyless.io/docs/ldap-dynamic-secret) or [LDAP rotated secrets](https://docs.akeyless.io/docs/create-an-ldap-rotated-secret).

# Create an LDAP Target in the CLI

To create an LDAP target from the CLI, run the following command:

```shell Akeyless CLI
akeyless target create ldap \
--name <target name> \
--ldap-url <LDAP server URL> \
--bind-dn <LDAP Bind DN with CN> \
--bind-dn-password < Password for LDAP user >
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

- `ldap-url`: The URL of your LDAP server (e.g., `ldap[s]://<hostname>:<port>`)

- `bind-dn`: The Bind DN of your LDAP user, will be used for connection setup. 

- `bind-dn-password`: The password of the LDAP user. 

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorblueldapp) section.

# Create an LDAP Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Infra (LDAP)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.  
   For more information, [read here](doc:implement-zero-knowledge).

4. Define the remaining parameters as follows:

- **LDAP Server URL:** Specify the LDAP Server URL.

- **CA Certificate File Content:** Provide the base64-encoded CA Certificate to enable the secure connection.

- **LDAP Bind DN:** Provide Bind DN for authentication of a privileged user.

- **Password for LDAP Bind DN:** Provide the password of the privileged user for authentication.

5. Click **Finish**.