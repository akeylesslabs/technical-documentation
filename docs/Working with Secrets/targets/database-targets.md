---
title: Database Targets
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
You can define a database target to be used with [Database Dynamic Secrets](doc:create-dynamic-secret-to-sql-db) and [Database Rotated Secrets](doc:create-a-database-rotated-secret).

Available database targets:

* [MySQL/MariaDB](https://docs.akeyless.io/docs/database-targets#mysql)

* [PostgreSQL](https://docs.akeyless.io/docs/database-targets#postgresql)

* [MSSQL](https://docs.akeyless.io/docs/database-targets#mssql)

* [Redshift](https://docs.akeyless.io/docs/database-targets#redshift)

* [Oracle](https://docs.akeyless.io/docs/database-targets#oracle)

* [MongoDB](https://docs.akeyless.io/docs/database-targets#mongodb)

* [MongoDB Atlas](https://docs.akeyless.io/docs/database-targets#mongodb-atlas)

* [Snowflake](https://docs.akeyless.io/docs/database-targets#snowflake)

* [Cassandra](https://docs.akeyless.io/docs/database-targets#cassandra)

* [SAP HanaDB](https://docs.akeyless.io/docs/database-targets#sap-hanadb)

* [Redis](https://docs.akeyless.io/docs/database-targets#redis)

# Create a Database Target in the CLI

> 👍 Note
>
> To create a database target from Akeyless CLI, choose the database type within the `create-db-target` command

> 📘 Info
>
> `create-db-target` command includes all available databases targets, please follow the relevant database section for the relevant fields.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Database Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorbluedbp) section.

In order to create database targets you can define the following fields on [Akeyless CLI](doc:cli):

```shell MySQL/MariaDB
akeyless target create db \
--name <Target name> \
--db-type mysql \
--pwd <Database password> \
--host <Database host> \
--port <Database port> \
--user-name <Database user name> \
--db-name <Database name>
```
```shell PostgresSQL
akeyless target create db \
--name <Target name> \
--db-type postgres \
--pwd <Database password> \
--host <Database host> \
--port <Database port> \
--user-name <Database user name> \
--db-name <Database name>
```
```shell MSSQL
akeyless target create db \
--name <Target name> \
--db-type mssql \
--user-name <Database user name> \ 
--pwd <Database password> \ 
--host <Database host> \ 
--port <Database port> \
--db-name <Database name> 
```
```shell Redshift
akeyless target create db \
--name <Target name> \
--db-type redshift \
--pwd <Database password> \
--host <Database host> \
--port <Database port> \
--user-name <Database user name> \
--db-name <Database name>
```
```shell Oracle
akeyless target create db \
--name <Target name> \
--db-type oracle \
--pwd <Database password> \
--host <Database host> \
--port <Database port> \
--user-name <Database user name> \
--oracle-service-name <oracle db service name>
```
```shell MongoDB
akeyless target create db \
--name <Target name> \
--db-type mongodb \
--db-name <Database name> \
--pwd <Database password> \
--host <Database host> \
--port <Database port> \
--user-name <Database user name> 
```
```Text MongoDB Atlas
akeyless target create db \
--name <Target name> \
--db-type mongodb \
--mongodb-atlas true \
--db-name <Database name> \
--mongodb-atlas-project-id <MongoDB Atlas project ID> \
--mongodb-atlas-api-public-key <MongoDB Atlas public key> \
--mongodb-atlas-api-private-key <MongoDB Atlas private key>
```
```shell Snowflake
akeyless target create db \
--name <Target name> \
--db-type snowflake \
--user-name <Database user name> \
--pwd <Database password> \ #relevent for User-Password Authentication
--snowflake-api-private-key <RSA Private key (base64 encoded)> \ #relevent for "RSA Private Key" Authentication
--snowflake-api-private-key-passphrase <The Private key passphrase> \ #relevent for "RSA Private Key" Authentication
--db-name <Database name> \
--snowflake-account <Snowflake account name>
```
```shell Cassandra
akeyless target create db \
--name <Target name> \
--db-type cassandra \
--pwd <Database password> \
--host <Database host> \
--port <Database port> \
--user-name <Database user name>
```
```shell SAP HanaDB
akeyless target create db \
--name <Target name> \
--db-type hanadb \
--pwd <Database password> \
--host <Database host> \
--port <Database port> \
--user-name <Database user name> \
--db-name <Database name>
```
```shell Redis
akeyless target create db \
--name <Target name> \
--db-type redis \
--pwd <Database password> \
--user-name <Database user name>
```

# Create a Database Target in the Console

## MySQL

Log in to the Akeyless Console, and go to **Targets > New > Database (MySQL)**.

**Name:** A unique name for the target. The name can include the path to the virtual folder in which you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
For more information, [read here](doc:implement-zero-knowledge).

**DB Username:** Privilege database user name with sufficient rights to create users.

**DB Password:** Password of the database privilege user name.

**DB Hostname:** Target database hostname or IP address.

**DB Port:** Target database port.

**DB Name:** Target database name.

**SSL:** Check to enable SSL, requires SSL certificate.

**Advanced:**

**DB Server Certificate:** Set of root certificate authorities in base64 encoding used by clients to verify server certificates.

**DB Server Name:** The server name is used to verify the hostname on the returned certificates unless InsecureSkipVerify is provided. It is also included in the client's handshake to support virtual hosting unless it is an IP address

Click **Finish**.

## PostgreSQL

Log in to the Akeyless Console, and go to **Targets > New > Database (PostgreSQL)**.

**Name:** A unique name for the target. The name can include the path to the virtual folder in which you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
For more information, [read here](doc:implement-zero-knowledge).

**DB Username:** Privilege database user name with sufficient rights to create users.

**DB Hostname:** Target database hostname or IP address.

**DB Password:** Password of the database privilege user name.

**DB Port:** Target database port.

**DB Name:** Target database name.

**SSL:** Check to enable SSL, requires SSL certificate.

Click **Finish**.

## MSSQL

Log in to the Akeyless Console, and go to **Targets > New > Database (MSSQL)**.

**Name:** A unique name for the target. The name can include the path to the virtual folder in which you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
For more information, [read here](doc:implement-zero-knowledge).

Choose the desired mode of authenticating either **Use Credentials**,  **Use Cloud Identity**, or **Target** to utilize a domain credentials from an existing [LDAP Target](doc:ldap-target)

**DB Username:** Privilege database username with sufficient rights to create users.
(Relevant only when using **Credentials** authenticating)

**DB Password:** Password of the database privilege username.
(Relevant only when using **Credentials** authenticating)

**DB Hostname:** Target database hostname or IP address.

**DB Port:** Target database port.

**DB Name:** Target database name.

**Cluster Mode** Set when working with Cluster.

**Client ID (Application ID):** Azure Client id. (Relevant only when using **Cloud Identity** authenticating)

**Tenant ID:** Azure Tenant ID. (Relevant only when using **Cloud Identity** authenticating)

**Client Secret:** Azure Client Secret. (Relevant only when using **Cloud Identity** authenticating)

Click **Finish**.

## Redshift

Log in to the Akeyless Console, and go to **Targets > New > Database (Redshift)**.

**Name:** A unique name for the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
For more information, [read here](doc:implement-zero-knowledge).

**DB Username:** Privilege database user name with sufficient rights to create users.

**DB Hostname:** Target database hostname or IP address.

**DB Password:** Password of the database privilege user name.

**DB Port:** Target database port.

**DB Name:** Target database name.

**SSL:** Check to enable SSL, requires SSL certificate.

Click **Finish**.

## Oracle

Log in to the Akeyless Console, and go to **Targets > New > Database (Oracle)**.

**Name:** A unique name for the target. The name can include the path to the virtual folder in which you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
For more information, [read here](doc:implement-zero-knowledge).

**Connect Using:** Select how to connect to Oracle DB either using **Explicit Credentials**, or using  **Wallet**

For **Explicit Credentials** provide the following:

**DB Username:** Privilege database user name with sufficient rights to create users

**DB Hostname:** Target database hostname or IP address.

**DB Password:** Password of the database privilege user name.

**DB Port:** Target database port.

**Service Name:** Target database name.

**TLS:** Select to connect over TLS

To connect using **Wallet** provide the following:

**P12 File :** Wallet P12 file contains the key in PCKS12 format

**SSO File:** Wallet SSO file

**Wallet Login Type:** Select how to use the Wallet, either using **Password** or with **mTLS**

**DB Username:** Privilege database user name with sufficient rights to create users, relevant only for **Wallet Login Type** of Password.

**DB Hostname:** Target database hostname or IP address..

**DB Port:** Target database port.

**Service Name:** Target database name.

**TLS:** Select to connect over TLS

Click **Finish**.

> 📘 Wallet with Password
>
> To use your Wallet with login type of Password ensure to add the relevant username to your wallet using the following format: `mkstore -wrl ~/mywallet2 -createCredential "(HOST=<host>)(PORT=1521)(SERVICE_NAME=<SN Name>)" <Username> <Password>`

## MongoDB

Log in to the Akeyless Console, and go to **Targets > New > Database (MongoDB)**.

**Name:** A unique name for the target. The name can include the path to the virtual folder in which you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
For more information, [read here](doc:implement-zero-knowledge).

Select **MongoDB** radio button.

**DB Name:** Target database name.

**Username:** Privilege database user name with sufficient rights to create users.

**Password:** Password of the database privilege user name.

**Host and Port:** Target database hostname or IP address with port.

**Advanced:**

**Default Authentication DB:** MongoDB default authentication database.

**Options:** URI options (e.g. replicaSet=mySet&authSource=authDB)

Click **Finish**.

## MongoDB Atlas

Log in to the Akeyless Console, and go to **Targets > New > Database (MongoDB)**.

**Name:** A unique name for the target. The name can include the path to the virtual folder in which you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
For more information, [read here](doc:implement-zero-knowledge).

Select **MongoDB Atlas** radio button.

**DB Name:** Users DB name, the default should be `admin`

**Project ID:** MongoDB Atlas project ID.

**API public key:** MongoDB Atlas public key.

**API private key:** MongoDB Atlas private key.

Click **Finish**.

## Snowflake

Log in to the Akeyless Console, and go to **Targets > New > Database (Snowflake)**.

**Name:** A unique name for the target. The name can include the path to the virtual folder in which you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
For more information, [read here](doc:implement-zero-knowledge).

**Account Username:** Username for a Snowflake user administrator (with the USERADMIN role or higher).

**Authentication Type:** Select your authentication type, either **User-Password** or **RSA Private Key**.

**Account Password:** Password for the Snowflake user administrator account.
(Relevant only when using **User-Password** authenticating)

**Private Key:** RSA Private key (base64 encoded), associated with the public key defined in Snowflake connection.
(Relevant only when using **RSA Private Key** authenticating).
For more information on how to get this key, check this [guide](https://docs.snowflake.com/en/user-guide/key-pair-auth).

**Private Key Passphrase:** The Private key passphrase.
(Relevant only when using **RSA Private Key** authenticating)

**DB Name:** Target database name within your Snowflake account.

**Account Name:** Snowflake account name in `xy12345.region.cloud_provider` format.
Note: You can find this string in your Snowflake URL.

Click **Finish**.

## Cassandra

Log in to the Akeyless Console, and go to **Targets > New > Database (Cassandra)**.

**Name:** A unique name for the target. The name can include the path to the virtual folder in which you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
For more information, [read here](doc:implement-zero-knowledge).

**DB Username:** Privilege database user name with sufficient rights to create users.

**DB Hostname:** Target database hostname or IP address.

**DB Password:** Password of the database privilege user name.

**DB Port:** Target database port.

**SSL:** Check to enable SSL, requires SSL certificate.

Click **Finish**.

## SAP HanaDB

Log in to the Akeyless Console, and go to **Targets > New > Database (SAP HanaDB)**.

**Name:** A unique name for the target. The name can include the path to the virtual folder in which you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
For more information, [read here](doc:implement-zero-knowledge).

**DB Username:** Privilege database user name with sufficient rights to create users.

**DB Hostname:** Target database hostname or IP address.

**DB Password:** Password of the database privilege user name.

**DB Port:** Target database port.

**DB Name:** Target database name.

**SSL:** To enable SSL, requires SSL certificate.

Click **Finish**.

## Redis

Log in to the Akeyless Console, and go to **Targets > New > Database (Redis)**.

**Name:** A unique name for the target. The name can include the path to the virtual folder in which you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
For more information, [read here](doc:implement-zero-knowledge).

**DB Username:** Privilege database user name with sufficient rights to create users.

**DB Password:** Password of the database privilege user name.

**DB Hostname:** Target database hostname or IP address.

**DB Port:** Target database port.

**SSL:** To enable SSL, requires an SSL certificate.

Click **Finish**.

# Tutorial

Check out our tutorial video on [Creating and Configuring MySQL Targets](https://tutorials.akeyless.io/docs/creating-targets).
