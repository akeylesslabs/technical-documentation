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

## Target Types

### Database

* [Cassandra](https://docs.akeyless.io/docs/database-targets#cassandra)
* [Microsoft SQL Server (MSSQL)](https://docs.akeyless.io/docs/database-targets#microsoft-sql-server-mssql)
* [MongoDB](https://docs.akeyless.io/docs/database-targets#mongodb)
* [MySQL](https://docs.akeyless.io/docs/database-targets#mysql-and-mariadb)
* [Oracle](https://docs.akeyless.io/docs/database-targets#oracle)
* [PostgreSQL](https://docs.akeyless.io/docs/database-targets#postgresql)
* [Redis](https://docs.akeyless.io/docs/database-targets#redis)
* [Redshift](https://docs.akeyless.io/docs/database-targets#amazon-redshift)
* [SAP HANA database](https://docs.akeyless.io/docs/database-targets#sap-hana-database)
* [Snowflake](https://docs.akeyless.io/docs/database-targets#snowflake)

### Cloud

* [AWS](https://docs.akeyless.io/docs/aws-targets)
* [Azure AD](https://docs.akeyless.io/docs/azure-targets)
* [Cloudflare](https://docs.akeyless.io/docs/cloudflare-target)
* [GCP](https://docs.akeyless.io/docs/gcp-targets)
* [Salesforce](https://docs.akeyless.io/docs/salesforce-target)

### AI

* [Gemini](https://docs.akeyless.io/docs/gemini-target)
* [OpenAI](https://docs.akeyless.io/docs/openai-target)

### Kubernetes

* [EKS](https://docs.akeyless.io/docs/kubernetes-targets)
* [GKE](https://docs.akeyless.io/docs/kubernetes-targets)
* [Generic](https://docs.akeyless.io/docs/kubernetes-targets)

### Operating System

* [SSH](https://docs.akeyless.io/docs/ssh-target)
* [Windows](https://docs.akeyless.io/docs/windows-target)

### Certificate Automation

* [DigiCert](https://docs.akeyless.io/docs/digicert-target)
* [GlobalSign](https://docs.akeyless.io/docs/globalsign-target)
* [GlobalSign Atlas](https://docs.akeyless.io/docs/globalsign-atlas)
* [GoDaddy](https://docs.akeyless.io/docs/godaddy-target)
* [Google CA](https://docs.akeyless.io/docs/google-ca-target)
* [Let's Encrypt](https://docs.akeyless.io/docs/lets-encrypt)
* [Sectigo](https://docs.akeyless.io/docs/sectigo-target)
* [Venafi](https://docs.akeyless.io/docs/venafi-target)
* [ZeroSSL](https://docs.akeyless.io/docs/zerossl-target)

### Infrastructure

* [Artifactory](https://docs.akeyless.io/docs/artifactory-targets)
* [Chef Infra](https://docs.akeyless.io/docs/chef-infra-targets)
* [Docker Hub](https://docs.akeyless.io/docs/docker-hub-target)
* [GitHub](https://docs.akeyless.io/docs/github-target)
* [GitLab](https://docs.akeyless.io/docs/gitlab-target)
* [Splunk](https://docs.akeyless.io/docs/splunk-target)

### Other

* [Custom](https://docs.akeyless.io/docs/web-targets)
* [HashiCorp Vault](https://docs.akeyless.io/docs/hashicorp-vault-target)
* [LDAP](https://docs.akeyless.io/docs/ldap-target)
* [Linked](https://docs.akeyless.io/docs/linked-target)
* [Ping](https://docs.akeyless.io/docs/ping-target)
* [RabbitMQ](https://docs.akeyless.io/docs/rabbitmq-targets)

## Delete protection for targets

Targets support delete protection to reduce accidental deletion risk.

Use the delete protection setting on target create and update operations to help prevent accidental deletion.

For related item protection controls, see [Secret and Target Locking](https://docs.akeyless.io/docs/secret-and-target-locking).

## Tutorial

Check out our tutorial video on [Creating and Configuring Targets](https://tutorials.akeyless.io/docs/creating-targets).
