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
You can define an LDAP target to be used with [LDAP Dynamic Secrets](https://docs.akeyless.io/docs/ldap-dynamic-secret) or [LDAP Rotated Secrets](https://docs.akeyless.io/docs/create-an-ldap-rotated-secret).

<Callout icon="📘" theme="info">
  ### Custom Usernames

  The LDAP Target includes an optional **Username** field, separate from the required **Bind DN**. Use it when the account's username is domain-qualified, in the `DOMAIN\username` format (for example, `CORP\svc-akeyless`), commonly used with Active Directory.

  Setting the Username field is optional and has no effect on the rotation flow. When set, the Rotated Secret's response returns this username instead of the full Bind DN (for a target rotator) or the username without the domain (for a self-rotator).
</Callout>

## Create an LDAP Target with the CLI

To create an LDAP target with the CLI, run the following command:

```shell
akeyless target create ldap \
--name <target name> \
--ldap-url <LDAP server URL> \
--bind-dn <LDAP Bind DN with CN> \
--bind-dn-password < Password for LDAP user > \
--ldap-username <Optional domain-qualified username>
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `ldap-url`: The URL of your LDAP server (For example, `ldap[s]://<hostname>:<port>`)

* `bind-dn`: The Bind DN of your LDAP user, will be used for connection setup. Accepts a full DN (for example, `cn=admin,dc=example,dc=com`).

* `bind-dn-password`: The password of the LDAP user.

* `ldap-username`: **Optional**. A domain-qualified username for this account, in the `DOMAIN\username` format (for example, `CORP\svc-akeyless`). When set, the Rotated Secret's response returns this value instead of the Bind DN.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#ldap) section.

## Create an LDAP Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Infra (LDAP)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

4. Define the remaining parameters as follows:

    * **LDAP Server URL:** Specify the LDAP Server URL.

    * **CA Certificate File Content:** Provide the Base64-encoded CA Certificate to enable the secure connection.

    * **LDAP Bind DN:** Provide Bind DN for authentication of a privileged user. Accepts a full DN (for example, `cn=admin,dc=example,dc=com`).

    * **Username:** **Optional**. A domain-qualified username for this account, in the `DOMAIN\username` format (for example, `CORP\svc-akeyless`). When set, the Rotated Secret's response returns this value instead of the Bind DN.

    * **Password for LDAP Bind DN:** Provide the password of the privileged user for authentication.

5. Click **Finish**.