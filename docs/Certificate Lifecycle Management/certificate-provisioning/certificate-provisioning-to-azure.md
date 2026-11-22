---
title: Certificate Provisioning to Azure Key Vault
deprecated: false
hidden: false
metadata:
  robots: index
---
Certificate Provisioning to Azure Key Vault lets you push a certificate stored in Akeyless directly into Azure Key Vault, using an existing [Azure Target](https://docs.akeyless.io/docs/azure-targets). This is one of the [certificate provisioning](https://docs.akeyless.io/docs/certificate-provisioning) destinations supported by Akeyless.

Unlike provisioning to a Linux or Windows endpoint, the Azure Target holds only the credentials used to call the Key Vault API. The certificate is stored in Key Vault as a single object that bundles the certificate, private key, and chain. After a successful provisioning, future renewals of the certificate are provisioned automatically.

Every certificate provisioned by Akeyless is tagged with `provisioned-by: akeyless` in Azure, so you can identify and audit Akeyless-managed certificates.

## Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview).
- A certificate item stored in Akeyless that includes its private key. For more information, see [Certificate Storage](https://docs.akeyless.io/docs/certificate-storage).
- An Azure Target whose service principal has the **Key Vault Certificates Officer** role on the Key Vault, or, when using access policies, the **Get**, **List**, and **Import** certificate permissions.

## Provider-Specific Fields

| Field                | Description                                                                 |
| -------------------- | ---------------------------------------------------------------------------- |
| **Certificate Name** | The certificate name in Azure Key Vault.                                     |
| **Key Vault Name**   | Mandatory. The Azure Key Vault where the certificate object will be stored.  |

## Provisioning a Certificate Using the Akeyless CLI

Run the following CLI command to provision a certificate to Azure Key Vault:

```shell
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <Azure Target name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-name <Certificate name in Key Vault> \
--key-vault-name <Key Vault name>
```

Where:

- `name`: The Certificate item name.
- `target-name`: The Azure Target item name to provision the certificate with.
- `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).
- `certificate-name`: The name of the certificate in Azure Key Vault.
- `key-vault-name`: The name of the Azure Key Vault where the certificate will be stored.

You can find the complete list of additional parameters for this command in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference) section.

## Provisioning a Certificate Using the Akeyless Console

1. Log in to the Akeyless Console, go to **Items**, and find the certificate you wish to provision.
2. Click on the Certificate item, click on the **Provisioning** tab, and then **Attach**.
3. Select an Azure **Target**.
4. Enter the fields:
   - **Certificate Name:** The certificate name in Azure Key Vault.
   - **Key Vault Name:** The Azure Key Vault where the certificate object will be stored.
5. Select the **Gateway** through which the certificate will be provisioned.
6. Click **Save**.

## How the Certificate Is Stored in Azure Key Vault

The certificate, private key, and full chain are imported as a single native Key Vault **Certificate** object. Azure stores the private key securely and exposes the public certificate attributes.

## Post-Provisioning Actions

Azure Key Vault doesn't run commands on hosts, so **Post Provision Command** isn't supported. To reload services or update bindings after a certificate is provisioned or renewed, create an Azure Event Grid subscription on the Key Vault for the `Microsoft.KeyVault.CertificateNewVersionCreated` event, and trigger an Azure Function or Automation Runbook.
