---
title: RabbitMQ Access
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
You can enable secure remote access to RabbitMQ on the dynamic secret that generates ephemeral credentials for the RabbitMQ. Users can then access the RabbitMQ console from the Secure Remote Access Portal either over the web. 

## Prerequisite

To enable secure remote access to RabbitMQ you need:

* The [Secure Remote Access](https://docs.akeyless.io/docs/remote-access-setup-overview) deployed.

* A [RabbitMQ Dynamic Secrets](doc:rabbitmq-producer).

* Akeyless [Browser Extension](https://docs.akeyless.io/docs/browser-extensions).

## Set Up Remote Access to RabbitMQ from the Akeyless CLI

Create a [RabbitMQ Dynamic Secret](doc:rabbitmq-producer) in Akeyless API Gateway.

Let's set up remote access to RabbitMQ using the Akeyless CLI. If you’d prefer, see how to do this from the [Akeyless Console](https://docs.akeyless.io/docs/rabbitmq-secure-remote-access#set-up-remote-access-to-rabbitmq-from-the-akeyless-console) instead.

Run the relevant command to define the following fields to the secret that specifies the RabbitMQ details and access credentials:

```shell Akeyless CLI
akeyless dynamic-secret update rabbitmq \
--name <dynamic secret name> \
--secure-access-enable true \
--secure-access-url <RabbitMQ destination URL> \
--secure-access-web-browsing <true/false>
```

where:

* **secure-access-url:** The RabbitMQ URL to inject credentials. 
* **secure-access-web-browsing:** Optional, secure web browsing over isolated web browser **available only for clients with** [Web Access Bastion](https://docs.akeyless.io/docs/web-access-on-k8s).

# Set Up Remote Access to RabbitMQ from the Akeyless Console

Let's set up remote access to RabbitMQ from the Akeyless Console. If you'd prefer, see how to do this from [Akeyless CLI](https://docs.akeyless.io/docs/rabbitmq-secure-remote-access#set-up-remote-access-to-rabbitmq-from-the-akeyless-cli) instead.

1. Log in to the Akeyless Console and go to **Items**.

2. Select the dynamic secret that specifies the database details and access credentials.

3. Click on the **Secure Remote Access** tab, select the pencil icon and enable **Secure Remote Access**, then fill in the following fields:

* `Injection URL`: Required, a RabbitMQ URL to inject credentials. 
* `Secure Web Browsing`: Optional, secure web browsing over isolated web browser **available only for clients with** [Web Access Bastion](https://docs.akeyless.io/docs/web-access-on-k8s).

4. To the right of the **Enable Secure Remote Access** field, select the tick mark icon to save your changes.

On Akeyless Secure Remote Access Portal, click on the RabbitMQ application. A new tab will open to the page and inject credentials for a temporary user provided by the dynamic secret.
