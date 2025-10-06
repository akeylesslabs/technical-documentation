---
title: CLI Reference - Event Forwarders
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
This section outlines the CLI commands relevant to Event Forwarder.

<CLIGeneralFlags />

# `event-forwarder` Commands

## `event-forwarder create`

Commands for managing the event forwarders.

### `event-forwarder create email`

Create a new Email Event Forwarder

#### Usage

```shell
akeyless event-forwarder create email \
--name <Event Forwarder name> \
--email-to <comma seperated email addresses> \
--gateway-url <'https://<Your-Akeyless-GW-URL:8000>'> \
--items-event-source-locations </Secrets/*> \
--targets-event-source-locations </Targets/*> \
--auth-methods-event-source-locations </Auth-Methods/*> \
--gateways-event-source-locations <https://<Your-Akeyless-GW-URL:8000>
--event-types <event type> \
--include-error <true / false>
--runner-type[=immediate] <immediate / periodic> \
--every <1-24 hours>
```

#### Flags

`-n, --name`: **Required**, Event Forwarder name

`--runner-type[=immediate]`: **Required**, Event Forwarder runner type [`immediate`, `periodic`]

`--items-event-source-locations`: Items event sources to forward events about, for example: /`Secrets`/*

`--targets-event-source-locations`: Targets event sources to forward events about, for example: /`Targets`/*

`--auth-methods-event-source-locations`: Auth Methods event sources to forward events about, for example: /`Auth-Methods`/*

`--gateways-event-source-locations`: Gateways event sources to forward events about, for example the relevant Gateways cluster URLs,: `https://<Your-Akeyless-GW-URL:8000`

`--event-types`: [Full list of available events](https://docs.akeyless.io/docs/event-center#event-types)

`--include-error`: Set this option to include event errors details [ `true` / `false` ]

`-k, --key`: Key name. The key will be used to encrypt the Event Forwarder secret value. If the key name is not specified, the account default protection key is used

`--email-to`: A comma-separated list of email addresses to send events to

`--override-url`: Override Akeyless default URL with your Gateway URL (port `18888`)

`--every`: Rate of periodic runner repetition in hours

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--description`: Description of the object

### `event-forwarder create servicenow`

Create a new Service Now Event Forwarder

#### Usage

```shell
akeyless event-forwarder create servicenow \
--name <Event Forwarder name> \
--gateway-url <'https://<Your-Akeyless-GW-URL:8000>'> \
--host <Workstation Host>
--items-event-source-locations </Secrets/*> \
--targets-event-source-locations </Targets/*> \
--auth-methods-event-source-locations </Auth-Methods/*> \
--gateways-event-source-locations <https://<Your-Akeyless-GW-URL:8000>
--event-types <event type>
```

#### Flags

`-n, --name`: **Required**, Event Forwarder name

`--runner-type[=immediate]`: **Required**, Event Forwarder runner type [`immediate`, `periodic`]

`--items-event-source-locations`: Items event sources to forward events about, for example: /`Secrets`/*

`--targets-event-source-locations`: Targets event sources to forward events about, for example: /`Targets`/*

`--auth-methods-event-source-locations`: Auth Methods event sources to forward events about, for example: /`Auth-Methods`

`--gateways-event-source-locations`: Gateways event sources to forward events about, for example the relevant Gateways cluster URLs,: `https://<Your-Akeyless-GW-URL:8000`

`--event-types`: [Full list of available events](https://docs.akeyless.io/docs/event-center#event-types)

`-k, --key`: Key name. The key will be used to encrypt the Event Forwarder secret value. If the key name is not specified, the account default protection key is used

`--host`: Workstation Host

`--auth-type[=user-pass]`: The authentication type to use [`user-pass`/`jwt`]

`--admin-name`: Workstation Admin Name

`--admin-pwd`: Workstation Admin Password

`--user-email`: The user email to identify with when connecting with `jwt` authentication

`--client-id`: The client ID to use when connecting with `jwt` authentication

`--client-secret`: The client's secret to use when connecting with `jwt` authentication

`--app-private-key-file-path`: Path to the RSA Private Key to use when connecting with `jwt` authentication

`--app-private-key-base64`: The RSA Private Key to use when connecting with `jwt` authentication

`--every`: Rate of periodic runner repetition in hours

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--description`: Description of the object

### `event-forwarder create slack`

Create a new Slack Event Forwarder

#### Usage

```shell
akeyless event-forwarder create slack \
--name <Event Forwarder name> \
--url <Slack Webhook URL>
--gateway-url <'https://<Your-Akeyless-GW-URL:8000>'> \
--items-event-source-locations </Secrets/*> \
--targets-event-source-locations </Targets/*> \
--auth-methods-event-source-locations </Auth-Methods/*> \
--gateways-event-source-locations <https://<Your-Akeyless-GW-URL:8000>
--event-types <event type>
--runner-type[=immediate] <immediate / periodic> \
--every <1-24 hours>
```

#### Flags

`-n, --name`: **Required**, Event Forwarder name

`--runner-type[=immediate]`: **Required**, Event Forwarder runner type [`immediate`, `periodic`]

`url`: **Required**, Slack Webhook URL

`--items-event-source-locations`: Items event sources to forward events about, for example: /`Secrets`/*

`--targets-event-source-locations`: Targets event sources to forward events about, for example: /`Targets`/*

`--auth-methods-event-source-locations`: Auth Methods event sources to forward events about, for example: /`Auth-Methods`

`--gateways-event-source-locations`: Gateways event sources to forward events about, for example the relevant Gateways cluster URLs,: `https://<Your-Akeyless-GW-URL:8000`

`--event-types`: [Full list of available events](https://docs.akeyless.io/docs/event-center#event-types)

`-k, --key`: Key name. The key will be used to encrypt the Event Forwarder secret value. If the key name is not specified, the account default protection key is used

`--every`: Rate of periodic runner repetition in hours

`-u, --gateway-url[=https://<Your-Akeyless-GW-URL:8000]`: API Gateway URL (Configuration Management port)

`--description`: Description of the object

### `event-forwarder create webhook`

Create a new Webhook Event Forwarder

#### Usage

```shell
akeyless event-forwarder create webhook \
--name <Event Forwarder name> \
--url <Webhook URL>
--gateway-url <'https://<Your-Akeyless-GW-URL:8000>'> \
--items-event-source-locations </Secrets/*> \
--targets-event-source-locations </Targets/*> \
--auth-methods-event-source-locations </Auth-Methods/*> \
--gateways-event-source-locations <https://<Your-Akeyless-GW-URL:8000>
--event-types <event type>
--runner-type[=immediate] <immediate / periodic> \
--every <1-24 hours>
```

#### Flags

`-n, --name`: **Required**, Event Forwarder name

`--runner-type[=immediate]`: **Required**, Event Forwarder runner type [`immediate`, `periodic`]

`--items-event-source-locations`: Items event sources to forward events about, for example: /`Secrets`/*

`--targets-event-source-locations`: Targets event sources to forward events about, for example: /`Targets`/*

`--auth-methods-event-source-locations`: Auth Methods event sources to forward events about, for example: /`Auth-Methods`

`--gateways-event-source-locations`: Gateways event sources to forward events about, for example the relevant Gateways cluster URLs,: `https://<Your-Akeyless-GW-URL:8000`

`--event-types`: [Full list of available events](https://docs.akeyless.io/docs/event-center#event-types)

`-k, --key`: Key name. The key will be used to encrypt the Event Forwarder secret value. If the key name is not specified, the account default protection key is used

`--every`: Rate of periodic runner repetition in hours

`--url`: Webhook URL

`--server-certificates-file-name`: Name of a file containing a `PEM` certificate of the Webhook

`--server-certificates`: `Base64 encoded PEM` certificate of the Webhook

`--auth-type[=user-pass]`: The Webhook authentication type [`user-pass`, `token`, `certificate`]

`--username`: Username for authentication relevant for `user-pass` auth-type

`--password`: Password for authentication relevant for `user-pass` auth-type

`--auth-token`: `Base64 encoded Token` string relevant for `token` auth-type

`--client-cert-file-name`: Name of a file containing a `PEM` certificate, relevant for `certificate` auth-type

`--client-cert-data`: `Base64 encoded PEM certificate`, relevant for `certificate` auth-type

`--private-key-file-name`: Name of a file containing a `PEM RSA Private Key`, relevant for `certificate`  auth-type

`--private-key-data`: `Base64 encoded PEM RSA Private Key`, relevant for `certificate` auth-type

`-u, --gateway-url[=https://<Your-Akeyless-GW-URL:8000]`: API Gateway URL (Configuration Management port)

`--description`: Description of the object

## `event-forwarder delete`

### Flags

`-n, --name`: **Required**, Event Forwarder name

## `event-forwarder get`

### Flags

`-n, --name`: **Required**, Event Forwarder name
