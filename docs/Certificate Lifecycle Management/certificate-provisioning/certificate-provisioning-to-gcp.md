---
title: Certificate Provisioning to GCP Certificate Manager
deprecated: false
hidden: false
metadata:
  robots: index
---
Certificate Provisioning to GCP Certificate Manager lets you push a certificate stored in Akeyless directly into GCP Certificate Manager, using an existing [GCP Target](https://docs.akeyless.io/docs/gcp-targets). This is one of the [certificate provisioning](https://docs.akeyless.io/docs/certificate-provisioning) destinations supported by Akeyless.

Unlike provisioning to a Linux or Windows endpoint, the GCP Target holds only the credentials used to call the Certificate Manager API. The certificate is stored in GCP as a single object that bundles the certificate, private key, and chain. After a successful provisioning, future renewals of the certificate are provisioned automatically.

Every certificate provisioned by Akeyless is labeled `provisioned-by: akeyless` in GCP, so you can identify and audit Akeyless-managed certificates.

## Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview).
- A certificate item stored in Akeyless that includes its private key. For more information, see [Certificate Storage](https://docs.akeyless.io/docs/certificate-storage).
- A GCP Target whose service account has the **Certificate Manager Editor** (`roles/certificatemanager.editor`) role on the project, or at least the `certificatemanager.certs.create`, `certificatemanager.certs.get`, and `certificatemanager.certs.update` permissions.

## Provider-Specific Fields

| Field                | Description                                                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Certificate Name** | The certificate name in GCP Certificate Manager.                                                                            |
| **Location Scope**   | Mandatory. Whether the certificate is deployed to the `global` namespace or to a specific region, for example `us-central1`. |

<Callout icon="👍" theme="okay">
  ### Note

  The certificate is created in the project of the service account defined on the [GCP Target](https://docs.akeyless.io/docs/gcp-targets).
</Callout>

## Provisioning a Certificate Using the Akeyless CLI

Run the following CLI command to provision a certificate to GCP Certificate Manager:

```shell
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <GCP Target name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-name <Certificate name in GCP> \
--location-scope <global|region>
```

Where:

- `name`: The Certificate item name.
- `target-name`: The GCP Target item name to provision the certificate with.
- `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).
- `certificate-name`: The name of the certificate in GCP Certificate Manager.
- `location-scope`: `global`, or a specific region such as `us-central1`.

You can find the complete list of additional parameters for this command in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference) section.

## Provisioning a Certificate Using the Akeyless Console

1. Log in to the Akeyless Console, go to **Items**, and find the certificate you wish to provision.
2. Click on the Certificate item, click on the **Provisioning** tab, and then **Attach**.
3. Select a GCP **Target**.
4. Enter the fields:
   - **Certificate Name:** The certificate name in GCP.
   - **Location Scope:** `global`, or a specific region (for example, `us-central1`).
5. Select the **Gateway** through which the certificate will be provisioned.
6. Click **Save**.

## How the Certificate Is Stored in GCP Certificate Manager

The leaf and intermediate chain are uploaded as the certificate, together with the matching private key, as one Certificate Manager certificate.

If a certificate with the same ID already exists, Akeyless updates it only if it has the `provisioned-by=akeyless` label. Otherwise, provisioning fails. Choose another name, or add the label to the existing certificate.

## Post-Provisioning Actions

GCP Certificate Manager doesn't run commands on hosts, so **Post Provision Command** isn't supported. To reload services or update bindings after a certificate is provisioned or renewed, create a Cloud Logging sink for Certificate Manager certificate operations that routes to Pub/Sub or Eventarc, and trigger a Cloud Function or Cloud Run service.
