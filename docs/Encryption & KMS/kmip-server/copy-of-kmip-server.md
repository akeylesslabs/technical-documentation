---
title: KMIP Server - Multi CA
excerpt: Key Management Interoperability Protocol (KMIP) Server
deprecated: false
hidden: false
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

<Callout icon="📘" theme="info">
  ### Note:&#x20;

  Make sure to replace the `hostname` field with your **Akeyless Gateway** hostname.
</Callout>

## Step 2: Create a KMIP client

To create a KMIP client and issue a client certificate signed by the active CA, run the following command:

```shell
akeyless kmip-create-client \
--name <client-name> \
--gateway-url 'https://<Your_Akeyless_GW_URL>:8000'
```

Flags:

- `name`: Name of the KMIP client.
- `certificate-ttl`: Optional. Client certificate TTL in days. Values must be 90 days or longer (default: 90).
- `output-file-folder`: Optional. Folder location to save the client cert and key files (default: .).
- `gateway-url[=http://localhost:8000]`: Akeyless Gateway URL.

## Step 3: Rotate KMIP CA

To generate a new **Root CA**, set it to active, and demote the current CA to trusted without dropping client connections, run:

```shell
akeyless kmip-rotate-ca \
--gateway-url 'https://<Your_Akeyless_GW_URL>:8000' \
--output-file-folder .
```

Flags:

- `certificate-ttl`: Optional. CA certificate TTL in days (default: 3650).
- `output-file-folder`: Optional. Folder location to save the new `ca.cert` and updated `ca-bundle.cert` (default: `.`).
- `gateway-url[=http://localhost:8000]`: Akeyless Gateway URL.

## Step 4: Get CA Bundle

To retrieve a PEM-concatenated bundle containing all active and trusted CAs for distribution to clients, run:

```shell
akeyless kmip-get-ca-bundle \
  --gateway-url 'https://<Your_Akeyless_GW_URL>:8000' \
  --output-file-folder .
```

Flags:

- `output-file-folder`: Optional. Folder location to save ca-bundle.cert (default: .).
- `gateway-url[=http://localhost:8000]`: Akeyless Gateway URL.

## Step 5: Renew a KMIP client

To re-issue a client certificate signed by the current active CA while preserving client rules and permissions, run:

```shell
akeyless kmip-renew-client \
--name <client-name> \
--gateway-url 'https://<Your_Akeyless_GW_URL>:8000'
```

Flags:

- `name`: Name of the KMIP client (either name or client-id is required).
- `client-id`: ID of the KMIP client.
- `certificate-ttl`: Optional. Defaults to original TTL.
- `output-file-folder`: Optional. Folder location to save the new cert and key files (default: .).
- `gateway-url[=http://localhost:8000]`: Akeyless Gateway URL.

## Step 6: List CAs

To list all CAs registered in the Gateway along with their state, validity window, and issued client count, run:

```shell
akeyless kmip-list-cas \
  --gateway-url 'https://<Your_Akeyless_GW_URL>:8000'
```

Flags:

- `gateway-url[=http://localhost:8000]`: Akeyless Gateway URL.

## Step 7: Sunset a KMIP CA

To remove an old trusted CA from the trust store after client migration is complete, run:

```shell
akeyless kmip-sunset-ca \
  --ca-id <ca-id> \
  --gateway-url 'https://<Your_Akeyless_GW_URL>:8000'
```

Flags:

- `ca-id`: ID of the CA to sunset.
- `force`: Optional. Bypass the 7-day active client safety check.
- `gateway-url[=http://localhost:8000]`: Akeyless Gateway URL.

# Zero-Downtime CA Rotation

Follow this step-by-step procedure to rotate the KMIP **Root CA&#x20;**&#x77;ithout causing downtime on client targets.

## Prerequisites

- All KMIP clients are operational and connected.
- Operator has admin access to Akeyless Gateway and target systems.

## Step 1: Rotate CA on Akeyless Gateway

<br />Run `kmip-rotate-ca` to introduce the new CA. This sets the new CA as active and keeps the old CA as trusted:

```shell
akeyless kmip-rotate-ca \
  --gateway-url 'https://<GW_HOST>:8000' \
  --output-file-folder /tmp/kmip-rotation
```

Verify that both CAs are present:

```shell
akeyless kmip-list-cas --gateway-url 'https://<GW_HOST>:8000'
```

## Step 2: Distribute the CA Bundle to KMIP Clients

Fetch and apply `ca-bundle.cert` using `kmip-get-ca-bundle` and distribute it to your target environments so clients trust both old and new CAs.

## Step 3: Re-issue Client Certificates

<br />Re-issue certificates for each client using `kmip-renew-client`

```shell
akeyless kmip-renew-client \
  --name <client-name> \
  --output-file-folder /tmp/kmip-rotation/<client-name> \
  --gateway-url 'https://<GW_HOST>:8000'
```

Apply the newly generated certificate (`.cert`) and private key `.key`) to each target client. The old certificate remains valid until its expiration, preventing forced disconnects.

## Step 4: Verify Client Migration

Confirm all clients have successfully migrated to the new CA:

```shell
akeyless kmip-list-cas --gateway-url 'https://<GW_HOST>:8000'
```

Ensure the count of Issued clients under the old CA reaches `0`.

## Step 5: Sunset the Old CA

Once all clients are verified on the new CA, remove the old CA from the trust store:

```shell
akeyless kmip-sunset-ca \
  --ca-id ca-v1 \
  --gateway-url 'https://<GW_HOST>:8000'
```
