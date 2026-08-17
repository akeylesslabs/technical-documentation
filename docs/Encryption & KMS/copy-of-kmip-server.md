---
title: KMIP Server - Multi CA
excerpt: Key Management Interoperability Protocol (KMIP) Server
deprecated: false
hidden: true
metadata:
  robots: index
next:
  pages:
    - slug: kmip-for-vsphere
      title: KMIP for Vsphere
      type: basic
---
The [Akeyless Gateway ](https://docs.akeyless.io/docs/gateway-overview)built-in Key Management Interoperability Protocol (KMIP) server handles the lifecycle of KMIP-managed objects.

By default, cryptographic objects managed by the KMIP server are stored under `/kmip/default/`. The Akeyless Gateway authentication method used for KMIP operations must include `create`, `list`, `delete`, and `read` permissions for `/kmip/default/*`.

This default path can be changed during KMIP server setup.

The KMIP Server supports multi-CA dual-trust authentication, allowing operators to rotate Certificate Authorities (CAs) and re-issue client certificates with zero downtime.

# KMIP Certificate Expiry Events

KMIP server, client, and CA certificates are time-bound objects. To reduce renewal failures and service interruptions, monitor certificate expiration events in the [Event Center.](https://docs.akeyless.io/docs/event-center)

For KMIP certificate observability, use the following event types:

- `kmip-ca-pending-expiration`: Triggered when a CA certificate enters its expiration notification window.

- `kmip-ca-expired`: Triggered when a trusted CA certificate has passed its validity window.

- `kmip-client-on-expiring-ca`: Triggered for each client certificate issued by a CA that is approaching expiration.

- `kmip-cert-pending-expiration`: Triggered before server or client certificate expiration based on configured notification windows.

- `kmip-cert-expired`: Triggered when a server or client certificate has expired.

To route these events to operational channels, configure an [Event Forwarder.](https://docs.akeyless.io/docs/event-center)

<Callout icon="📘" theme="info">
  ### Note:

  Only users from your Gateway admins list can configure the KMIP server.
</Callout>

# CA Lifecycle States

Each CA registered in the KMIP trust store exists in one of three states:

- `active`: The default CA used to sign new server listener certificates and newly issued client certificates. Only one CA can be active at a time.
- `trusted`: Accepted for mTLS client authentication, but not used for issuing new certificates. Multiple CAs can be trusted simultaneously.
- `sunset`: Removed from the trust store. Connections presenting client certificates signed only by a sunset CA will fail authentication.

# Recommended Workflow

Use this sequence for day-to-day KMIP operations and CA rotation:

1. Provision server: `kmip-server-setup`
2. Provision client: `kmip-create-client`
3. Rotate CA: `kmip-rotate-ca`
4. Get CA Bundle: `kmip-get-ca-bundle`
5. Renew client: `kmip-renew-client`
6. List CAs: `kmip-list-cas`
7. Sunset old CA: `kmip-sunset-ca`

***

# CLI Quickstart

## Step 1: Create a KMIP server

To start the Akeyless KMIP server using Akeyless CLI, run the following command:

```shell
akeyless kmip-server-setup \
  --hostname <akeyless.gateway.hostname> \
  --gateway-url 'https://<Your_Akeyless_GW_URL>:8000' \
  --root /kmip/default
```

Flags:

- `hostname:` Hostname of this KMIP server.
- `root`: Required path to store KMIP objects.
- `certificate-ttl`: Optional. Server certificate TTL in days. Values must be 90 days or longer.
- `expiration-event-in`: Optional. Number of days before expiration to notify. Repeat the flag to set multiple events.
- `gateway-url[=http://localhost:8000]`: Akeyless Gateway URL.

You can find the complete list of settings for this command in the [CLI Reference - Akeyless KMIP Server ](https://docs.akeyless.io/docs/cli-reference-akeyless-kmip-server#kmip-server-setup)section.

<br />
