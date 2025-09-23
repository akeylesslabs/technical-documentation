---
title: Email Event Forwarder
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
**Email Event Forwarder** enables you to forward event notifications to email addresses based on your configuration. These include notifications about **Items, Auth Methods, Targets, and Gateways**, which can be configured to be sent immediately or every 1 to 24 hours.

# Create an Email Event Forwarder using the CLI

To set up a **Email** Event Forwarder, use the following command:

```shell
akeyless event-forwarder create email \
--name MyForwarder \
--email-to <comma seperated email addresses> \
--gateway-url <'https://<Your-Akeyless-GW-URL:8000>'> \
--overide-url <'https://<Your-Akeyless-GW-URL:8000/console/>'> #or use port 18888\
--include-error false \ 
--items-event-source-locations </MySecrets/*> \
--targets-event-source-locations </MyTargets/*> \
--event-types <event type>
--runner-type[=immediate] <immediate / periodic> \
--every <1-24 hours>
```

The main parameters for the command are as follows: 

- `name`: **Event Forwarder** name

- `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

- `overide-url`  Override Akeyless default URL inside the email with your Gateway Console endpoint `https://Your-Akeyless-GW-URL:8000/console`. (or use your gateway URL at port `18888`)

- `include-error` Boolean by default false, to include error details as part of the email. 

- `items-event-source-locations`: **Items **event sources to forward events about,  for example: `/MySecrets/*`

- `targets-event-source-locations` **Targets **event sources to forward events about, for example: `/MyTargets/*`

- `auth-methods-event-source-locations` **Auth Methods** event sources to forward events about, for example: `/API-Keys/*`

- `gateways-event-source-locations`: **Gateways** event sources to forward events about, for example, the relevant Gateways cluster URL: `https://<Your-Akeyless-GW-URL:8000`

- `event-types`: A comma-separated list of types of events to notify about, [view the full list of the available events](https://docs.akeyless.io/docs/event-center#event-types)

- `email-to`: A comma-separated list of email addresses to send events to

- `runner-type[=immediate]`: Event Forwarder runner type [`immediate`, `periodic`]

- `every`: Rate of periodic runner repetition in hours

You can find the complete list of parameters for this command in the [CLI Reference - Email Event forwarder](https://docs.akeyless.io/docs/cli-reference-event-forwarders#p-stylecolorblueevent-forwarder-create-emailp)

# Create an Email Event Forwarder using the Console

1. Log in to the Akeyless Console and open the [Event Center](https://docs.akeyless.io/docs/event-center), select **Manage Forwarders**. If this is your first Forwarder, it appears as Add Forwarder, click it and choose: **Email**

2. Fill in the following fields:

- **Name**: The **Email** event forwarder name.
- **Recipient Email Addresses**: A comma-separated list of email addresses to send events to
- **Gateway**: Choose an existing Gateway from the drop-down list to select the relevant Gateway
- **Override Event Link URL**: Check to override Akeyless default URL with your Gateway URL (Port `18888`)
- Choose either to:

  - **Forward Events Immediately**: Forward events as soon as the event occurs

  - **Forward Events Every**: choose when to forward events, in **hours**
- **Event Sources**: Select the **Items / Auth Methods / Targets / Gateways** you would like to get events on based on their locations
- **Event Type**: Choose the relevant event to be notified about [from the following list](https://docs.akeyless.io/docs/event-center#event-types)