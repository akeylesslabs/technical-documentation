---
title: Webhook Event Forwarder
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
Event forwarders are tools you can configure through the Event Center in order to get notified on other platforms when a certain event type happens. For example, one might want to be notified every time a certain [Certificate](https://docs.akeyless.io/docs/certificate-storage) is about to expire or when a user requests to access an item you have in your Akeyless Platform.

**Webhook Event Forwarder** enables you to forward event notifications to **Endpoint URLs** based on your configuration. These include notifications about **Items, Auth Methods, Targets, and Gateways**, which can be configured to be sent immediately or every 1 to 24 hours.

# Create a Webhook Event Forwarder using the CLI

To set up a **Webhook** Event Forwarder, use the following command:

```shell User-Pass
akeyless event-forwarder create webhook \
--name MyForwarder \
--gateway-url <'https://<Your-Akeyless-GW-URL:8000>'> \
--url <Webhook URL>
--items-event-source-locations </MySecrets/*> \
--targets-event-source-locations </MyTargets/*>
--auth-type user-pass
--username <Username> \
--password <Password> \
--event-types <event type> \
--runner-type[=immediate] <immediate, periodic> \
--every <1-24 hours> \
```
```shell Token
akeyless event-forwarder create webhook \
--name MyForwarder \
--gateway-url <'https://<Your-Akeyless-GW-URL:8000>'> \
--url <Webhook URL>
--items-event-source-locations </MySecrets/*> \
--targets-event-source-locations </MyTargets/*>
--auth-type bearer-token \
--auth-token <Base64 encoded Token string> \
--event-types <event type> \
--runner-type[=immediate] <immediate, periodic> \
--every <1-24 hours> \
```
```shell Certificate
akeyless event-forwarder create webhook \
--name MyForwarder \
--gateway-url <'https://<Your-Akeyless-GW-URL:8000>'> \
--url <Webhook URL>
--items-event-source-locations </MySecrets/*> \
--targets-event-source-locations </MyTargets/*>
--auth-type certificate \
--client-cert-file-name <file containing PEM certificate> \
--client-cert-data <Base64 encoded PEM certificate> \
--private-key-file-name <file containing a PEM RSA Private Key> \
--private-key-data <Base64 encoded PEM RSA Private Key> \
--event-types <event type> \
--runner-type[=immediate] <immediate, periodic> \
--every <1-24 hours> \
```

The main parameters for the command are as follows: 

- `name`: **Event Forwarder** name

- `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

- `url`: The server that will receive the events.

- `items-event-source-locations`: Items event sources to forward events about, for example: `/abc/*`

- `event-types`: A comma-separated list of types of events to notify about, [view the full list of the available events](https://docs.akeyless.io/docs/event-center#event-types)

- `auth-type`: The Webhook Authentication Type [`user-pass`, `bearer-token`, `certificate`]

  - For `user-pass`:

    - `username`: Username for Authentication

    - `password`: Password for Authentication

  - For `bearer-token`:

    - `auth-token`: Base64 encoded Token string

  - For `certificate`:

    - `client-cert-file-name`: Name of a file containing a `PEM` certificate

    - `client-cert-data`: `Base64` encoded `PEM` certificate

    - `private-key-file-name`: Name of a file containing a `PEM` **RSA Private Key**

    - `private-key-data`: `Base64` encoded `PEM` **RSA Private Key**

- `runner-type[=immediate]`: Event Forwarder runner type [`immediate`, `periodic`]

- `every`: Rate of periodic runner repetition in hours

You can find the complete list of parameters for this command in the [CLI Reference - Webhook Event forwarder](https://docs.akeyless.io/docs/cli-reference-event-forwarders#p-stylecolorblueevent-forwarder-create-webhookp)

# Create a Webhook event forwarder using the Console

1. Log in to the Akeyless Console and open the [Event Center](https://docs.akeyless.io/docs/event-center), select **Manage Forwarders**. If this is your first Forwarder, it appears as Add Forwarder, click it and choose: **Webhook**

2. Fill in the following fields:

- **Name**: The **Webhook** event forwarder name
- **Webhook URL**: The **URL** which will receive the notifications from Akeyless
- **Server Certificate**: **PEM certificate** of the **Webhook**

Choose Authentication Type (**Password / Token / Certificate**) 

- For **Password**:

  - Provide: **Username ** and a **Password** 

- For **Token**:

  - Provide: **Base64 **encoded Token string

- For **Certificate**:

  - Provide: ** PEM Certificate** and a ** PEM Private Key** 

- **Gateway**: Choose a gateway from the list

- **Protection-Key**: Protection key other than the default, if you wish to change it

- Choose either to:

  - **Forward Events Immediately**: Forward events as soon as the event occurs

  - **Forward Events Every**: choose when to forward events, in **hours**

- **Event Sources**: Select the **Items / Auth Methods / Targets / Gateways** you would like to get events on based on their locations

- **Event Type**: Choose the relevant event to be notified about [from the following list](https://docs.akeyless.io/docs/event-center#event-types)