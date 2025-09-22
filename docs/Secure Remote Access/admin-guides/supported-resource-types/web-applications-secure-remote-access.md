---
title: Web Applications Access
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
Akeyless Secure Remote Access for Web Applications enables full secure remote connection to any web application while sharing access to any user without sharing access credentials. 

The following browsing modes are available:

* **Direct Connections** - Users access web targets directly in the browser by simply injecting the secret credentials into the correct fields through the Akeyless Browser Extension.
* **Secure Web Browsing** - Users access an embedded, isolated & secured remote browser (Firefox) where the credentials are injected into the correct fields without exposing them to the user, provides auditing, and allows restricting user access to only allowed websites while enforcing specific policies per your preferences (such as disabling developer-tools, etc.)
* **Secure Web Proxy** - Users access the web application where the Web Access Bastion acts as web proxy to access internal web resources from the external network (through the standard browser). This offers a VPN-like functionality for specific web apps.

> 🚧 Warning
>
> Your web application must run over HTTPS

## Prerequisite

* The [Web Access Bastion](https://docs.akeyless.io/docs/web-access-on-k8s) deployed.

* Akeyless [Browser Extension](https://docs.akeyless.io/docs/browser-extensions). 

This application is used to inject credentials for any secured websites. To start using web access injection, the value of the secret must provide the credentials for the web service. Pattern of credentials: <code>username..password</code>. i.e. a concatenation of your username and password, with double dots as a delimiter. 

# Set Up Remote Access to a web application from the Akeyless CLI

Let's set up remote access to your web application using the Akeyless CLI. If you’d prefer, see how to do this from the [Akeyless Console](https://docs.akeyless.io/docs/web-applications-secure-remote-access#set-up-remote-access-to-a-web-application-from-the-akeyless-console) instead.

Run the `update-item` command to define the following fields on the static secret that specifies the web application access credentials:

```shell Akeyless CLI
akeyless update-item --name <static secret name> /
--secure-access-enable true /
--secure-access-url <Web Application URL> / 
--secure-access-web-browsing <true/false>
```

where:

* **secure-access-url:** The web application login URL to inject secret.
* **secure-access-web-browsing:** Optional, secure web browsing over isolated web browser **available only with** [Web Access Bastion](https://docs.akeyless.io/docs/web-access-on-k8s).
* **secure-access-web-proxy:** Optional, secure web-proxy,**available only with** [Web Access Bastion](https://docs.akeyless.io/docs/web-access-on-k8s).

> 🚧 Warning
>
> In case you are using an Alias or multiple fields as part of your login credentials, please make sure your secret value follows this format: <code>username..alias..password</code>

On Akeyless Secure Remote Access Portal, click on the Web Access application, select the relevant item in the list. 

A new tab will open, redirect to the requested page, and inject credentials provided by the static secret.

# Set Up Remote Access to a web application from the Akeyless Console

Let's set up remote access to the web application from the Akeyless Console. If you'd prefer, see how to do this from the [Akeyless CLI](https://docs.akeyless.io/docs/web-applications-secure-remote-access#set-up-remote-access-to-a-web-application-from-the-akeyless-cli) instead.

1. Log in to the Akeyless Console and go to **Items**.

2. Select the static secret that specifies the web application access credentials.

3. Click on the **Secure Remote Access** tab, select the pencil icon and enable **Secure Remote Access**, then fill in the following fields:

* `Injection URL`: The web application login URL to inject secrets. 

* `Secure Web Browsing`: Optional, secure web browsing over an isolated web browser **available only with** [Web Access Bastion](https://docs.akeyless.io/docs/web-access-on-k8s).

* `Secure Web Proxy`: Optional, secure web proxy via the bastion, **available only with** [Web Access Bastion](https://docs.akeyless.io/docs/web-access-on-k8s).

**Secure Web Browsing (Isolated)**

Secure Web Browsing available for applications any web application, includes, self managed K8s dashboard URL, AWS and Azure Portal, those application can be accessed in isolated mode. This method adds an extra layer of security in the usage of credentials injection. This mode requires A [Web Access Bastion](https://docs.akeyless.io/docs/web-access-on-k8s).

All secrets which have **Secure Web Browsing** option enabled are marked with a badge in the Akeyless Secure Remote Access Portal.
