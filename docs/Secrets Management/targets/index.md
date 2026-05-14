---
title: Targets
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
A target is a reusable endpoint credential item for a database, cloud platform, or server. Targets help admins keep endpoint details organized so you can reuse them across secrets instead of entering the same information for each item.

![Illustration for: A Target is an endpoint for a secret such as a database, cloud platform, or server. Targets help admins keep their secrets and endpoints more organized. Instead of adding an endpoint to each secret separately.](https://files.readme.io/7481a59-Creates_Targets.png)

Using targets has three primary advantages:

* Streamline your creation flow: Creating a target that has the credentials for a specific endpoint will allow you to reference said endpoint in other items like [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret), [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets) and more, without having to input the details again every time. You can have multiple secrets point to the same Target, making it easy for different teams to connect and minimizing the number of Targets in your organization.

* Keep your information safe: Using the [Role-Based Access Control (RBAC)](https://docs.akeyless.io/docs/rbac) capabilities, users are not required to have access to, or knowledge of, your privileged account credentials. Simply grant users with `list` permissions on those Target items to provide them with the ability to create [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) or [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets). For example, two [Database Dynamic Secrets](https://docs.akeyless.io/docs/create-dynamic-secret-to-sql-db) can be created using the same existing Target, but each with its own set of permissions.

* Don't break the credential chain: Targets can also be used to sync encryption keys with an external KMS, or to define a Target to be used with our [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets) to manage and automate your privilege account credentials rotation. This allows every item referencing the target to be up to date on the necessary information and to stay usable even after rotations are done.

## Common Target Families

If you are looking for a specific target type, start with the family that matches your endpoint:

* [Database Targets](https://docs.akeyless.io/docs/database-targets) for database credentials that applications and teams reuse across secrets.
* Cloud provider targets: [AWS Targets](https://docs.akeyless.io/docs/aws-targets), [Azure Targets](https://docs.akeyless.io/docs/azure-targets), and [GCP Targets](https://docs.akeyless.io/docs/gcp-targets) for cloud platform credentials and cloud-specific integrations.
* Certificate automation targets: [Let's Encrypt Target](https://docs.akeyless.io/docs/lets-encrypt), [DigiCert Target](https://docs.akeyless.io/docs/digicert-target), [Google CA Target](https://docs.akeyless.io/docs/google-ca-target), and [Cloudflare Target](https://docs.akeyless.io/docs/cloudflare-target) for DNS-01 validation with public Certificate Authority (CA) targets.
* [SSH Targets](https://docs.akeyless.io/docs/ssh-target) and [Web Targets](https://docs.akeyless.io/docs/web-targets) for server access and web-facing endpoints.

## Delete protection for targets

Targets support delete protection to reduce accidental deletion risk.

Use the delete protection setting on target create and update operations to help prevent accidental deletion.

For related item protection controls, see [Secret and Target Locking](https://docs.akeyless.io/docs/secret-and-target-locking).

## Tutorial

Check out our tutorial video on [Creating and Configuring Targets](https://tutorials.akeyless.io/docs/creating-targets).
