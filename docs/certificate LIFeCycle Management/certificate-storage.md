---
title: Certificate Storage
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: event-center
      title: Event Center
---
# Overview

Akeyless Certificate storage allows you to securely store, sort, and browse through your certificates in one secure location, as well as set expiration notifications so you are always prepared.

The certificates are treated as their own type of item inside the Akeyless Platform with their parsed information saved in the form of a JSON array to represent the certificate chain. The item will include both the certificate itself and the private key (if it exists), which will be stored completely encrypted.

# Managing a Certificate in the CLI

## Creating a New Certificate

To create a new certificate, use the following command:

```shell create certificate
akeyless create-certificate \
--name <certificate-name> \
--certificate <path-to-certificate>
```

The main parameters for the command are as follows:

* `name`: A unique name for the Certificate. The name can include the path to the virtual folder in which you want to create it, using slash `/` separators. If the folder does not exist, it will be created together with the Certificate.

* `certificate`: Path to a file that contains the certificate in one of the following formats: `pem,cer,crt,pfx,p12`.

* `certificate-data`: Content of the certificate in a Base64 format, if you add this you do not need the certificate path parameter and vice versa.

* `private-key`: Optional, path to the file with the certificate's private key.

* `key-data`: Content of the certificate's private key in a Base64 format, if you add this you do not need the key path parameter and vice versa.

* `expiration-event-in`: How many days before the expiration of the certificate would you like to be notified, this parameter can be added multiple times for multiple notifications.

You can find the complete list of parameters for this command in the [CLI Reference - Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#p-stylecolorbluecreate-certificatep) section.

## Getting a Certificate

To view a certificate's value, use the following command:

```shell get certificates
akeyless get-certificate-value \
--name <certificate-name>
```

This command will return the certificates with the chain if it exists, as well as the private key if it exists.

You can find the complete list of parameters for this command in the [CLI Reference - Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#p-stylecolorblueget-certificate-valuep) section.

## Updating a Certificate

This command is similar to the creation command and uses the same parameters, but instead of creating a new item it will update the data in the existing item and overwrite the expiration notifications.\
The command is as follows:

```shell update-certificate
akeyless update-certificate-value \
--name <certificate-name> \
--certificate <path-to-certificate>
```

All of the parameters from the creation command will also apply here.

# Managing a Certificate in the Console

1. Select **Items** > **New** > **Certificate**.

2. Basic Configuration (fill in the following parameters):

* **Name (mandatory):** A unique Certificate name.

* **Location:** Location within your Akeyless account.

* **Description:** General description of the Certificate (optional).

* **Tags:** Assign tags to the Certificate (optional).

* **Delete Protection:** When enabled, protects the Certificate from accidental deletion.

* **Protection key:** If you wish to protect a certificate with one of your keys other than the default you can select it here.

* Click on **Next**.

3. Certificate Configuration (fill in the following parameters):

* **Certificate (Mandatory):** Upload the certificate itself from a file.

* **Private Key:** If exists, you may also upload the certificate's private key from a file.

* **Expiration Notification:** If you wish to get notified when the certificate's expiration date comes near, click on **⊕ Add Notification** and adjust the day count from the default 30 to any number you desire.\
  This can be done multiple times in order to be notified more than once.

> 👍 Tip
>
> To view the entire certificate hierarchy simply click on the **View Certificate Details** to get a the decoded information of your certificate.
