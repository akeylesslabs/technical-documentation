---
title: ServiceNow Event Forwarder
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
**ServiceNow Event Forwarder** enables you to forward event notifications to **Endpoint URLs** based on your configuration. These include notifications about **Items, Auth Methods, Targets, and Gateways**, which can be configured to be sent immediately or every 1 to 24 hours.

> 📘 Note
> 
> The URL for the **ServiceNow** endpoint would be: `<serviceNowURL>/akeyless-events/`

# Create a ServiceNow Event Forwarder using the CLI

To set up a **ServiceNow** Event Forwarder, use the following command:

```shell JWT
akeyless event-forwarder create servicenow \
--name MyForwarder \
--gateway-url <'https://<Your-Akeyless-GW-URL:8000>'> \
--host <Endpoint URL> \
--items-event-source-locations </MySecrets/*> \
--targets-event-source-locations </MyTargets/*>
--event-types <event type> \
--auth-type <jwt> \
--user-email <user@email.com> \
--client-id <Client ID> \
--client-secret <Client Secret> \
--app-private-key-file-path <RSA Private Key>
--event-types <event types> \
--runner-type[=immediate] <immediate, periodic> \
--every <1-24 hours> \
```
```shell User-Pass
akeyless event-forwarder create servicenow \
--name MyForwarder \
--gateway-url <'https://<Your-Akeyless-GW-URL:8000>'> \
--host <Endpoint URL> \
--items-event-source-locations </MySecrets/*> \
--targets-event-source-locations </MyTargets/*>
--event-types <event type> \
--admin-name <Admin name> \
--admin-pwd <Admin password>
```

The main parameters for the command are as follows: 

- `name`: **Event Forwarder** name

- `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`)

- `host`: **ServiceNow ** endpoint URL

- `items-event-source-locations`: **Items **event sources to forward events about,  for example: `/MySecrets/*`

- `targets-event-source-locations` **Targets **event sources to forward events about, for example: `/MyTargets/*`

- `auth-methods-event-source-locations` **Auth Methods** event sources to forward events about, for example: `/API-Keys/*`

- `gateways-event-source-locations`: **Gateways** event sources to forward events about, for example, the relevant Gateways cluster URL: `https://localhost:8000`

- `event-types`: A comma-separated list of types of events to notify about, [view the full list of the available events](https://docs.akeyless.io/docs/event-center#event-types)

- `auth-type`: The Webhook Authentication Type [`user-pass`, `jwt`]

  - For `user-pass`:

    - `admin-name`: Workstation Admin Name

    - `admin-pwd`: Workstation Admin Password

  - For `jwt`:

    - `user-email`: The user email to identify with when connecting with `jwt` authentication
    - `client-id`: The **Client's ID** to use when connecting with `jwt` authentication
    - `client-secret`: The **Client's Secret** to use when connecting with `jwt` authentication
    - `app-private-key-file-path`: Path to the RSA Private Key to use when connecting with `jwt` authentication

- `--runner-type[=immediate]`: Event Forwarder runner type [`immediate`, `periodic`]

- `--every`: Rate of periodic runner repetition in hours

You can find the complete list of parameters for this command in the [CLI Reference - ServiceNow Event forwarder](https://docs.akeyless.io/docs/cli-reference-event-forwarders#p-stylecolorblueevent-forwarder-create-servicenowp)

# Create a ServiceNow event forwarder using the Console

1. Log in to the Akeyless Console and open the [Event Center](https://docs.akeyless.io/docs/event-center), select **Manage Forwarders**. If this is your first Forwarder, it appears as Add Forwarder, click it and choose: **ServiceNow**

2. Fill in the following fields:

- **Name**: The **ServiceNow** event forwarder name
- **ServiceNow URL**: The **URL** which will receive the notifications from Akeyless

Choose Authentication Type (**Password /  JWT**) 

- For **Password**:

  - Provide: **ServiceNow **Admin **Username **and **Password**

- For **JWT**:

  - Provide: **Username**, **ClientID**, **Client Secret**, and the **Private Key**

- **Gateway**: Choose a gateway from the list.

- **Protection-Key**: Protection key other than the default, if you wish to change it

- Choose either to:

  - **Forward Events Immediately**: Forward events as soon as the event occurs

  - **Forward Events Every**: choose when to forward events, in **hours**

- **Event Sources**: Select the **Items / Auth Methods / Targets / Gateways** you would like to get events on based on their locations

- **Event Type**: Choose the relevant event to be notified about [from the following list](https://docs.akeyless.io/docs/event-center#event-types)