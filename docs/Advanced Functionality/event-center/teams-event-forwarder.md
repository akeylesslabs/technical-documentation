---
title: Teams Event Forwarder
deprecated: false
hidden: false
metadata:
  robots: index
---
**Teams Event Forwarder** enables you to forward event notifications to **Teams URLs** based on your configuration. These include notifications about Items, Auth Methods, Targets, and Gateways, which can be configured to be sent immediately or every 1 to 24 hours.

# Create a Teams Event Forwarder using the CLI

To set up a **Teams** Event Forwarder, use the following command:

```shell
akeyless event-forwarder create teams \
--name MyForwarder \
--gateway-url <'https://<Your-Akeyless-GW-URL:8000>'> \
--url <Teams Webhook URL> \
--items-event-source-locations </MySecrets/*> \
--targets-event-source-locations </MyTargets/*> \
--event-types <event type> \
--runner-type[=immediate] <immediate / periodic> \
--every <1-24 hours>
```

The main parameters for the command are as follows:

* `name`: **Event Forwarder** name

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `url`: The server that will receive the events

* `items-event-source-locations`: **Items** event sources to forward events about,  for example: `/MySecrets/*`

* `targets-event-source-locations` **Targets** event sources to forward events about, for example: `/MyTargets/*`

* `auth-methods-event-source-locations` **Auth Methods** event sources to forward events about, for example: `/API-Keys/*`

* `gateways-event-source-locations`: **Gateways** event sources to forward events about, for example, the relevant Gateways cluster URL: `https://<Your-Akeyless-GW-URL:8000`

* `event-types`: A comma-separated list of types of events to notify about, A list of all the event types can be found here

* `runner-type[=immediate]`: Event Forwarder runner type [`immediate`, `periodic`]

* `every`: Rate of periodic runner repetition in hours

You can find the complete list of parameters for this command in the [CLI Reference - Teams Event Forwarder](https://docs.akeyless.io/docs/cli-reference-event-forwarders#p-stylecolorblueevent-forwarder-create-slackp)

# Create a Teams Event Forwarder using the Console

1. Log in to the Akeyless Console and open the [Event Center](https://docs.akeyless.io/docs/event-center), select **Manage Forwarders**. If this is your first Forwarder, it appears as Add Forwarder, click it and choose: **Teams**

2. Fill in the following fields:

* **Name**: The **Teams** event forwarder name.

* **Teams URL**: The **URL** which will receive the notifications from Akeyless

* **Gateway**: Choose an existing Gateway from the drop-down list to select the relevant Gateway

* Choose either to receive notifications about the events immediately or on an hourly basis

* **Event Sources**: Select the **Items / Auth Methods / Targets / Gateways** you would like to get events on based on their locations

* **Event Type**: Choose the relevant event to be notified about [from the following list](https://docs.akeyless.io/docs/event-center#event-types)