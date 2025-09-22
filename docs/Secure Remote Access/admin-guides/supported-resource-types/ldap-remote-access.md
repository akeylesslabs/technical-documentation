---
title: LDAP Access
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
You can enable secure remote access to an LDAP server with a Dynamic Secret that generates ephemeral credentials for the server or a Rotated Secret. Users can access the LDAP server from the Secure Remote Access Portal over the web.

# Prerequisites

To enable secure remote access to an LDAP server you need:

* The [Secure Remote Access](https://docs.akeyless.io/docs/remote-access-setup-overview) deployed.

# Create an LDAP Secret

If you don't already have an LDAP secret, see the following docs to either create a [Dynamic Secret](https://docs.akeyless.io/docs/ldap-dynamic-secret) or [Rotated Secret](https://docs.akeyless.io/docs/create-an-ldap-rotated-secret) that specifies the server details and access credentials.

If you already have a relevant secret, continue below.

# Set Up Remote Access to an LDAP server from the Akeyless CLI

Let's set up remote access to an LDAP server using the Akeyless CLI. If you’d prefer, see how to do this from the [Akeyless Console](https://docs.akeyless.io/docs/ldap-remote-access#set-up-remote-access-to-an-ldap-server-from-the-akeyless-console) instead.

Run the relevant command to define the following fields to the secret that specifies the LDAP server details and access credentials:

```shell Dynamic Secret
akeyless dynamic-secret update ldap \
--name <dynamic secret name> \
--secure-access-enable true \
--secure-access-host <hostname or IP>
```
```shell Rotated Secret
akeyless rotated-secret update ldap \
--name <rotated secret name> \
--secure-access-enable true \
--secure-access-host <hostname or IP> \
--rotate-after-disconnect <true|false>
```

where:

* **secure-access-host:** The hostname (or IP address) for accessing the LDAP server as defined in the secret. For multiple values repeat this flag.

Optional: 

* **external-username:** Allow providing external user for a domain user \[true/false].
* **secure-access-rdp-domain:** Required only when `external-username` is set to true. Only required if the dynamic secret is configured to create credentials for a fixed user. This option defines the domain to which the LDAP user for whom credentials are created belongs.
* **rotate-after-disconnect:** Optional for Rotated Secret. Rotate the secret value when the SRA session ends.

# Set Up Remote Access to an LDAP server from the Akeyless Console

Let's set up remote access to a LDAP server from the Akeyless Console. If you'd prefer, see how to do this from the [Akeyless CLI](https://docs.akeyless.io/docs/ldap-remote-access#set-up-remote-access-to-an-ldap-server-from-the-akeyless-cli) instead.

1. Log in to the Akeyless Console and go to **Items**.

2. Select the Dynamic Secret or the Rotated Secret that specifies the LDAP server details and access credentials.

3. Click on the **Secure Remote Access** tab, select the pencil icon and enable **Secure Remote Access**, then fill in the following fields:

* `Host(s)`: The hostname (or IP address) for accessing the LDAP server as defined in the secret.
* `Externally Provided Username`: Optional for Dynamic Secret. Select to enable an external username to log into the target host.
* `Override User`: Optional for Dynamic Secret. Override the RDP Domain username.
* `Domain`: Optional for Dynamic Secret, required only when `Externally Provided Username` is ticked. Only required when the dynamic secret is configured to create credentials for a fixed user. This option defines the domain to which the LDAP user for whom credentials are created belongs.
* `Rotate after disconnection`: Optional for Rotated Secret. Rotate the secret value when the SRA session ends.

4. To the right of the **Enable Secure Remote Access** field, select the tick mark icon to save your changes.
