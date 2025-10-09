---
title: Azure Portal Access
excerpt: Secure remote access to the Microsoft Azure Portal
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
You can enable secure remote access to Azure Portal with a Dynamic Secret that generates ephemeral credentials for Azure AD or using a Rotated Secret. Users can then access the Azure Portal from the Secure Remote Access Portal.

# Prerequisites

To enable secure remote access to Azure Portal you need:

* The [Secure Remote Access Bastion](https://docs.akeyless.io/docs/secure-remote-access-bastion) deployed.

* The [Akeyless Browser Extension](https://docs.akeyless.io/docs/browser-extensions).

In addition, for users to access the Azure Portal in Isolated mode, you need:

* The [Web Access Bastion](https://docs.akeyless.io/docs/web-access-on-k8s).
* The Azure Portal site URL is specified as part of the `policies` section in the **values.yaml** file on the Web Access Bastion.

# Create an Azure Secret

If you don't already have an Azure AD secret, see the following docs to either create a [Dynamic Secret](https://docs.akeyless.io/docs/azure-ad-dynamic-secrets) or [Rotated Secret](https://docs.akeyless.io/docs/create-an-azure-rotated-secret) that specifies the Azure AD account details and access credentials.

If you already have a relevant secret, continue below.

# Set Up Remote Access to the Azure Portal from the Akeyless CLI

Let's set up remote access to the Azure Portal using the Akeyless CLI. If you’d prefer, see how to do this from the [Akeyless Console](https://docs.akeyless.io/docs/azure-portal-access#set-up-remote-access-to-the-azure-portal-from-the-akeyless-console) instead.

Run the relevant command to define the following fields to the secret that specifies the Azure details and access credentials:

```shell Dynamic Secret
akeyless dynamic-secret update azure \
--name <dynamic secret name> \
--secure-access-enable true \
--secure-access-web-browsing <true/false>
```
```shell Rotated Secret
akeyless rotated-secret update azure \
--name <rotated secret name> \
--secure-access-enable true \
--secure-access-web-browsing <true/false> \
--secure-access-url <URL to inject secrets> \
--rotate-after-disconnect <true|false>
```

where:

By default, access to the Azure portal will use direct network access mode. To work with Akeyless [Web Access Bastion](https://docs.akeyless.io/docs/web-access-on-k8s) for session isolation or as a secure proxy entry point, please set **one** of the following: 

* **secure-access-web-browsing:** Optional, secure browser via Akeyless Web Access Bastion.

Alternatively, in case you prefer to work with the Akeyless bastions as a proxy entry point, set this parameter as true: 

* **secure-access-web-proxy:** Optional, web-proxy via Akeyless Web Access Bastion.
* **secure-access-url:** Required for Rotated Secret. The target URL where credentials will be injected.
* **rotate-after-disconnect:** Optional for Rotated Secret. You can enable an automatic secret rotation after a session ends.
* **secure-access-delay:** The delay duration, in seconds, to wait after generating just-in-time credentials. Accepted range: 0-120 seconds

# Set Up Remote Access to the Azure Portal from the Akeyless Console

Let's set up remote access to the Azure Portal from the Akeyless Console. If you'd prefer, see how to do this from the [Akeyless CLI](https://docs.akeyless.io/docs/azure-portal-access#set-up-remote-access-to-the-azure-portal-from-the-akeyless-cli) instead.

1. Log in to the Akeyless Console and go to **Items**.

2. Select the Dynamic Secret or Rotated Secret that specifies the Azure AD details.

3. Click on the **Secure Remote Access** tab, select the pencil icon and enable **Secure Remote Access**, then fill in the following fields:

* `Rotate after disconnection`: Optional for Rotated Secret. You can enable an automatic secret rotation after a session ends.

* `Block Concurrent Use`: Optional for Rotated Secret. Block concurrent use of this secret.

* `Injection URL`: Required for Rotated Secret. The target URL where credentials will be injected.

* `Direct connection`: Default, using a direct connection to AWS portal via Akeyless Secure Remote Access Bastion.

* `Secure Web Browsing`: Optional, only required to enable access to the Azure Portal in Isolated mode, which restricts user access to other websites while they are logged in to the portal. **available only with** [Web Access Bastion](https://docs.akeyless.io/docs/web-access-on-k8s).

* `Secure Web Proxy`: Optional, secure web proxy mode **available only with** [Web Access Bastion](https://docs.akeyless.io/docs/web-access-on-k8s).

4. To the right of the **Enable Secure Remote Access** field, select the tick mark icon to save your changes.

> 📘 Custom Delay
>
> You can specify a custom delay, measured in seconds \[0 - 120], before a newly generated dynamic secret becomes usable. This additional wait time helps target systems complete their sync process with the updated credentials

# Access the Azure Portal from the Secure Remote Access Portal

1. Log in to the Secure Remote Access Portal and select Azure Portal.

2. Select the required target, then select **Web**.\
   A new tab opens to the Azure Portal sign-in page, and Akeyless injects the credentials generated by the dynamic secret for the temporary user.
