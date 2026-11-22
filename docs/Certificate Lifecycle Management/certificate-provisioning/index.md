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
Certificate Provisioning delivers a [stored](https://docs.akeyless.io/docs/certificate-storage) certificate to a remote destination through the [Gateway](https://docs.akeyless.io/docs/gateway-overview), using [Targets](https://docs.akeyless.io/docs/targets). Whenever a certificate is issued or renewed, Akeyless can push it straight to the servers, load balancers, and cloud certificate managers that use it, so certificates stay current everywhere without manual redeployment.

Akeyless supports provisioning certificates to the following endpoints. Each has its own dedicated page with the required Target, CLI command, and Console fields:

- **SSH servers**: Linux, or Windows over SSH, using an [SSH Target](https://docs.akeyless.io/docs/ssh-target). See [Certificate Provisioning to SSH Servers](https://docs.akeyless.io/docs/certificate-provisioning-to-ssh).
- **Windows servers**: over WinRM, using a [Windows Target](https://docs.akeyless.io/docs/windows-target). See [Certificate Provisioning to Windows Servers](https://docs.akeyless.io/docs/certificate-provisioning-to-windows).
- **F5 BIG-IP**: using an [F5 Target](https://docs.akeyless.io/docs/f5-target). See [Certificate Provisioning to F5 BIG-IP](https://docs.akeyless.io/docs/certificate-provisioning-to-f5-big-ip).
- **AWS Certificate Manager**: using an [AWS Target](https://docs.akeyless.io/docs/aws-targets). See [Certificate Provisioning to AWS Certificate Manager](https://docs.akeyless.io/docs/certificate-provisioning-to-aws).
- **Azure Key Vault**: using an [Azure Target](https://docs.akeyless.io/docs/azure-targets). See [Certificate Provisioning to Azure Key Vault](https://docs.akeyless.io/docs/certificate-provisioning-to-azure).
- **GCP Certificate Manager**: using a [GCP Target](https://docs.akeyless.io/docs/gcp-targets). See [Certificate Provisioning to GCP Certificate Manager](https://docs.akeyless.io/docs/certificate-provisioning-to-gcp).

<Callout icon="📘" theme="info">
  ### Post-Provision Command for Web Servers

  When you provision a certificate to a server (an SSH or Windows Target), you can set a custom **post-provision command** that runs on the server after each successful provisioning. For example, use it to reload or restart a web server so it serves the new certificate.

  The post-provision command isn't supported for F5 BIG-IP or cloud certificate managers.
</Callout>

## How Provisioning Works

- **Multiple targets per certificate:** A certificate can be provisioned to several targets. Each target is a separate row in the certificate's **Provisioning** table, with its own settings. Adding a target adds a row and doesn't replace the existing ones. Each target can be added to a certificate only once.
- **Immediate provisioning:** When you add a target, the certificate is provisioned to it right away. If that first provisioning fails, the target isn't added.
- **Automatic provisioning after renewal:** After every renewal, the certificate is provisioned again to every target in the **Provisioning** table. Each target is provisioned through its own Gateway, and a failure on one target doesn't stop the others.
- **Events:** Every provisioning raises a `certificate-provisioning-success` or `certificate-provisioning-failure` event, which you can forward with the [Event Center](https://docs.akeyless.io/docs/event-center).

Setting up certificate provisioning requires **Target** permissions on the Gateway.

### Provisioning on Demand

To provision a certificate again without renewing it, run:

```shell
akeyless provision-certificate --name <Certificate name>
```

Without `--target-name`, the certificate is provisioned to every target in its **Provisioning** table. Add `--target-name <Target name>` to provision it to that target only.

You can find the complete list of parameters for `assoc-target-item` in the [CLI Reference - Encryption Keys](https://docs.akeyless.io/docs/cli-reference-encryption-keys#assoc-target-item) section.

## Provisioning a Certificate Using the Akeyless Console

1. Log in to the Akeyless Console, go to **Items**, and find the certificate you wish to provision.
2. Click on the **Certificate** item, and click on the **Provisioning** tab. The **Provisioning** tab lists all the targets the certificate is currently provisioned to.
3. Click **Attach** to add a new row to the table.
4. Choose a **Target Name** from the drop-down list, and a **Gateway** to provision the certificate through. The remaining fields depend on the Target type - see the dedicated page for each endpoint, linked above, for its specific fields.
5. Click **Save**. The target is added as a new row in the **Provisioning** table.
6. To provision the certificate to additional targets, repeat steps 3-5. Each target can be configured with its own settings.
