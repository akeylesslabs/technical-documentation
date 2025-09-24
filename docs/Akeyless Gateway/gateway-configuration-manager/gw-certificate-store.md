---
title: Gateway Certificate Store
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
You can upload private CA certificates into the gateway to enable secure connections with trusted API endpoints, ensuring reliable communication by verifying authenticity. This requires [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) version `4.29.0` or later.

> 🚧 Note
>
> After uploading a private CA to certificate store, some services may require a restart or reconnection to fully recognize and utilize the new certificate authority.

# Manage Certificates Using the CLI

To upload certificates to your gateway using the CLI, run the following command:

```shell
akeyless gateway update certificate-store \
--name <Certificate Display name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--certificate <path/to/certificate/file> \
--certificate-data <certificate data in base64 format>
```

To delete certificates from your gateway using the CLI, run the following command:

```shell
akeyless gateway delete certificate-store \
--name <Certificate Display name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

Where:

* `name`: The Certificate Display name.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `certificate`: Path to a file that contains the certificate. Supported formats are: `pem`,`cer`,`crt`,`pfx`,`p12`.

* `certificate-data`: Content of the certificate in a Base64 format.

# Manage Certificates Using the UI

To upload certificates to your gateway using the UI, follow these steps:

1. From the console, go to **Gateways**, choose the relevant Gateway, and press **Manage Gateway**.

2. Go to **Certificate Store** and press **Add**.

3. Type the **Display Name** and add the certificate content under **Certificate**.

4. Click **Save**.

To remove certificates from your gateway using the UI, follow these steps:

1. From the console, go to **Gateways**, choose the relevant Gateway, and press **Manage Gateway**.

2. Go to **Certificate Store**.

3. Choose the certificate you wish to remove and press the **Action Menu** > **Delete**.
