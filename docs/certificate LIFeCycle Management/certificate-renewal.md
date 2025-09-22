---
title: Certificate Renewal
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
Akeyless provides a simple flow for certificates renewals, without the need to manually regenerate a **CSR**, while maintaining the certificate metadata including any [provisioning](doc:certificate-provisioning) settings. 

As part of the renewal, the user can choose either to renew the certificate using a **new key and CSR**, which is considered best practice, or **using the existing key** when the private key is stored in the certificate item. In both modes, all fields will be automatically populated from the expired certificate.

Upon successful renewal, in case [provisioning](doc:certificate-provisioning) settings exists, the certificate will be provisioned automatically.

# Renew a certificate using the Akeyless CLI

Run the following command to renew a certificate from the CLI: 

```shell
akeyless renew-certificate \
--name <Certificate name> \
--generate-key
```

Where:

- `name` :  The certificate full name, alternatively can be provided using `item-id` instead. 
- `generate-key` : Generate a new key as part of the certificate renewal, if not provided, the certificate private  key will be used when exists (i.e. stored on the certificate item).

Upon successful renewal a new version will be created on the certificate item itself, and automatic provisioning will be triggered based on the existing settings. 

You can find the complete list of additional parameters for this command in the [CLI Reference - Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#p-stylecolorbluerenew-certificatep) section.

# Renew a certificate using the Akeyless Console

Certificates can be renewed, either from the item or the event itself. the following flow will describe the renewal flow from the certificate item itself:

1. Log in to the Akeyless Console, and go to Items, find the certificate you wish to renew. 
2. Click on the **Certificate**, open the **Action Menu**, and click  **Certificate Renewal**.
3. You will be asked to either **Generate new CSR and Key** or **Use an existing Key** when applicable.
4. Click **Renew** to renew the certificate, once done, a pop-up with the **Certificate** and **Private Key** will appear.

To renew a certificate from the **Event Center**:

1. Open the **Event Center** and open the **Action Menu**  on the event of the certificate that is about to expire. 
2. Click **Certificate Renewal**.
3. You will be asked to either **Generate new CSR and Key** or **Use an existing Key** when applicable. 
4. Click **Renew** to renew the certificate, once done, a pop-up with the **Certificate** and **Private Key** will appear.

# Viewing the certificate versions

In Akeyless console, press on the **certificate **item and then, press on **Versions**. You will find a table listing all the versions of the certificate and keys.