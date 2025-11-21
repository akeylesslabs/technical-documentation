---
title: Certificate Provisioning
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
Certificate Provisioning is a process in which a certificate is injected into a remote endpoint. Currently, Akeyless supports provisioning certificates to a [Linux](https://docs.akeyless.io/docs/ssh-target) or a  [Windows](https://docs.akeyless.io/docs/windows-target) endpoint utilizing [Targets](https://docs.akeyless.io/docs/targets). 

Any [stored](https://docs.akeyless.io/docs/certificate-storage) certificate can be provisioned through the [Gateway](https://docs.akeyless.io/docs/api-gw), whereupon successful provisioning, future renewals of the certificate will be provisioned automatically. 

Setting up certificate provisioning requires **Target** permissions on the Gateway.

> 👍 Provisioning Permissions on Target
>
> To prevent partial files, the Gateway first saves new items (certificates, keys, etc.) in a temporary folder on your server, then atomically renames them into the final paths you specify. Ensure the temporary folder is writable by the user defined in the Target.

# Provisioning a certificate using the Akeyless CLI

Run the following CLI command to provision a certificate:

```shell Akeyless CLI
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--certificate-path <Where to save the certificate>  \ 
--post-provision-command <"echo Akeyless">
```

Where: 

* `name` : The **Certificate**  item name.

* `target-name` The **Target** item name, to provision the certificate. 

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `certificate-path` :A path on the **Target** to save the certificate PEM file can be used as well with `chain-path` and `private-key-path` flags to save those on different locations. 

* `post-provision-command`: Optional, a custom command to run on the remote target after successful provisioning e.g. restarting a service. 

You can find the complete list of additional parameters for this command in the [CLI Reference - Encryption Keys](https://docs.akeyless.io/docs/cli-reference-encryption-keys#p-stylecolorblueassoc-target-itemp) section.

# Provisioning a certificate using the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**, find the certificate you wish to provision.
2. Click on the **Certificate** item, click on the **Provisioning** tab, and then **Attach**.
3. Enter the following parameters:

* **Target Name** - **Choose an existing Target** from the drop-down list to select the existing [SSH ](https://docs.akeyless.io/docs/ssh-target)/ [Windows](https://docs.akeyless.io/docs/windows-target) Target.

* **Gateway** - **Choose an existing Gateway** from the drop-down list to select the relevant Gateway.

* **Certificate Remote Path** - The path where the certificate will be provisioned to in the remote machine.  

* **Private Key Remote Path** - A path on the target to store the private key.

* **Certificate Chain Path** - A path on the target to store the full chain.

* **Post Provision Command** - A custom command of your choice that will be executed on the remote machine as part of the provisioning process.
