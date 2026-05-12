---
title: Certificate Store
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
Use Certificate Store to add private CA certificates to Akeyless Gateway so services can trust required endpoints. This requires [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) version `4.29.0` or later.

> ℹ️ **Note:**
>
> After uploading a private CA to Certificate Store, some services may require a restart or reconnection before the new certificate authority is recognized. Starting with SRA v2.9.0, the SRA service dynamically loads custom CA certificates from the Gateway Certificate Store without requiring an SRA restart.

## Manage Certificates Using the CLI

To upload a certificate file to your Gateway using the CLI, run the following command:

```shell
akeyless gateway update certificate-store \
--name <Certificate Display name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-path <path/to/certificate/file>
```

To upload Base64-encoded certificate data to your Gateway using the CLI, run the following command:

```shell
akeyless gateway update certificate-store \
--name <Certificate Display name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-data <certificate data in base64 format>
```

To delete certificates from your gateway using the CLI, run the following command:

```shell
akeyless gateway delete certificate-store \
--name <Certificate Display name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

Where:

* `name`: The Certificate Display name.

* `gateway-url`: Akeyless Gateway URL (port `8000`).

* `certificate-path`: Path to a file that contains an X.509 certificate. PEM format is supported directly, and DER-encoded certificate data is normalized to PEM.

* `certificate-data`: Base64-encoded certificate content. PEM and DER certificate data are supported.

* `expiration-event-in`: Number of days before certificate expiration to trigger an event. Use the flag multiple times for multiple thresholds, for example `--expiration-event-in 1 --expiration-event-in 5`. Related events are documented in [Event Center](https://docs.akeyless.io/docs/event-center).

> ℹ️ **Note:**
>
> File extensions such as `.cer` and `.crt` can contain either PEM or DER certificate data. Gateway Certificate Store support is based on certificate encoding (PEM or DER), not on file extension.

## Manage Certificates Using the UI

To upload certificates to your gateway using the UI, follow these steps:

1. From the console, go to **Gateways**, choose the relevant Gateway, and select **Manage Gateway**.

2. Go to **Certificate Store** and select **Add**.

3. Type the **Display Name** and add the certificate content under **Certificate**.

4. Click **Save**.

To remove certificates from your gateway using the UI, follow these steps:

1. From the console, go to **Gateways**, choose the relevant Gateway, and select **Manage Gateway**.

2. Go to **Certificate Store**.

3. Choose the certificate you wish to remove and select the **Action Menu**, then **Delete**.
