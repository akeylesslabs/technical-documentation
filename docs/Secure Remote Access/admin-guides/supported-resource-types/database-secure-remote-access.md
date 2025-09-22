---
title: Database Access
excerpt: >-
  Secure remote access to a MySQL, MSSQL, MongoDB, Redshift, Oracle, PostgreSQL
  or Snowflake Database
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
You can enable secure remote access to a database using a [Dynamic Secret](doc:how-to-create-dynamic-secret) item that generates ephemeral credentials for that database or using a [Rotated Secret](doc:rotated-secrets). Users can then access the database from the Secure Remote Access Portal either over the web (using Adminer) or using the native database CLI.

> 👍 Note
>
> Use the `akeyless connect` command from Akeyless CLI to access databases from any UNIX terminal to work with your database native CLI.

# Prerequisites

To enable secure remote access to a database you need:

* The [Secure Remote Access](https://docs.akeyless.io/docs/remote-access-setup-overview) deployed.

In addition, for users to access the database using native CLI, you need:

* An [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates) for certificate authentication.

# Create a Database Secret

If you don't already have a database secret, see the following docs to either create a [Dynamic Secret](doc:create-dynamic-secret-to-sql-db) or [Rotated Secret](https://docs.akeyless.io/docs/create-a-database-rotated-secret) that specifies the database details and access credentials.

If you already have a database secret, continue below.

# Set Up Remote Access to a Database from the Akeyless CLI

Let's set up remote access to a database using the Akeyless CLI. If you’d prefer, see how to do this from the [Akeyless Console](https://docs.akeyless.io/docs/database-secure-remote-access#set-up-remote-access-to-a-database-from-the-akeyless-console) instead.

Run the relevant command to define the following fields to the secret that specifies the database details and access credentials:

```shell Dynamic Secret
akeyless dynamic-secret update <mongodb/mssql/mysql/oracledb/postgresql/redshift/snowflake> \
--name <dynamic secret name> \
--secure-access-enable true \
--secure-access-db-name <database name> \
--secure-access-host <database host:port> \
--secure-access-db-schema <schema-name> \
--secure-access-certificate-issuer </Path/to/SSH/Cert/Issuer>
```
```shell Rotated Secret
akeyless rotated-secret update <mongodb/mssql/mysql/oracledb/postgresql/redshift/snowflake> \
--name <rotated secret name> \
--secure-access-enable true \
--secure-access-db-name <database name> \
--secure-access-host <database host:port> \
--secure-access-db-schema <schema-name> \
--secure-access-certificate-issuer </Path/to/SSH/Cert/Issuer>
--rotate-after-disconnect <true|false>
```

where:

* **secure-access-db-name:** The database name as defined in the dynamic secret.
* **secure-access-host:** The hostname (or IP address) and port for accessing the database as defined in the dynamic secret.
* **secure-access-db-schema:** Optional, only supported for MSSQL and PostgreSQL database dynamic secrets.
* **secure-access-certificate-issuer:** Optional, only required to enable CLI access to the database. The path to the SSH Certificate Issuer that should be used for certificate authentication for CLI access.
* **rotate-after-disconnect:** Optional for Rotated Secret. Rotate the secret value when the SRA session ends.
* **secure-access-delay:** The delay duration, in seconds, to wait after generating just-in-time credentials. Accepted range: 0-120 seconds

# Set Up Remote Access to a Database from the Akeyless Console

Let's set up remote access to a database from the Akeyless Console. If you'd prefer, see how to do this from [Akeyless CLI](https://docs.akeyless.io/docs/database-secure-remote-access#set-up-remote-access-to-a-database-from-the-akeyless-cli) instead.

1. Log in to the Akeyless Console and go to **Items**.

2. Select the Dynamic Secret or Rotated Secret that specifies the database details and access credentials.

3. Click on the **Secure Remote Access** tab, select the pencil icon and enable **Secure Remote Access**, then fill in the following fields:

* `Host(s)`:  The hostname (or IP address) and port for accessing the database as defined in the dynamic secret.
* `Rotate after disconnection`: Optional for Rotated Secret. Rotate the secret value when the SRA session ends.

For **Web Access**, define the following fields: 

* `DB Name`:  The name of the database as defined in the dynamic secret.
* `Schema`: Optional, only supported for MSSQL and PostgreSQL database dynamic secrets.

For **CLI Access**, define the following field: 

* `SSH Cert Issuer`: The path to the SSH Certificate Issuer that should be used for certificate authentication.

4. To the right of the **Enable Secure Remote Access** field, select the tick mark icon to save your changes.

> 📘 Custom Delay
>
> You can specify a custom delay, measured in seconds \[0 - 120], before a newly generated dynamic secret becomes usable. This additional wait time helps target systems complete their sync process with the updated credentials

# Access a Database over the Web from the Secure Remote Access Portal

1. [Log in](https://docs.akeyless.io/docs/access-resources-remotely#connect-from-the-secure-remote-access-portal) to the Secure Remote Access Portal and select the database type to which you want to connect.

2. Select the database hostname or IP address, then select **Web**.\
   Adminer opens in a new tab, from which you can interact with the database according to your permissions.

# Access a Database Using CLI from the Secure Remote Access Portal

1. [Log in](https://docs.akeyless.io/docs/access-resources-remotely#connect-from-the-secure-remote-access-portal) to the Secure Remote Access Portal and select the database type to which you want to connect.

2. Select the database hostname or IP address, then select **CLI**.\
   A new tab opens, showing that you are connected to the database.

# Access a Database using Akeyless connect command

[Akeyless Connect](https://docs.akeyless.io/docs/remote-access-akeyless-connect) command enables application native CLI access:

```shell Akeyless connect
akeyless connect -t <mysql-server>:3306 -g <your-gateway-ip[:port]> -n "Path/to/Secret"
```

> 👍 Note
>
> Make sure your **Access ID** is specified in the `Allowed Access IDs` field of your SRA settings, to get access. **Access IDs** that are not listed, will not be authorized to get access.
