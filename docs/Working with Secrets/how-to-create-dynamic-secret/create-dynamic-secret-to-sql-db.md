---
title: Database Dynamic Secrets
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
You can create dynamic secrets for a wide range of databases, including:

* Amazon Redshift

* Cassandra

* Microsoft SQL Server

* MongoDB

* MySQL/MariaDB

* OracleDB

* PostgreSQL

* Redis

* SAP HANA

* Vertica

With dynamic secrets, you can control and manage which databases, tables, schema, and what set of permissions to issue for each type of application access, as well as completely manage the lifecycle of those temporary credentials which are created just in time-based on short-lived TTL with flexible revocation statements.

When a client requests a dynamic secret value, the Akeyless Platform connects to the database through the [Gateway](https://docs.akeyless.io/docs/api-gw) within your internal network and generates a temporary set of restricted access credentials.

> 👍 Note
>
> We recommend using dynamic secrets with [Targets](https://docs.akeyless.io/docs/database-targets). While it saves time for multiple secret level configurations by not requiring you to provide an [inline connection string](https://docs.akeyless.io/docs/create-dynamic-secret-to-sql-db#inline-connection-strings) each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the DB used, using inline will force you to go and change the credentials in each individual item instead of just the target.

# Create a Dynamic Database Secret from the CLI

To create a dynamic database secret from the CLI using an existing [Target](doc:targets), run the following command:

```shell MySQL/MariaDB
akeyless dynamic-secret create mysql \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--mysql-statements "CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}' PASSWORD EXPIRE INTERVAL 30 DAY;GRANT SELECT ON *.* TO '{{name}}'@'%';" \
--mysql-revocation-statements  "REVOKE ALL PRIVILEGES, GRANT OPTION FROM '{{name}}'@'%'; DROP USER '{{name}}'@'%';" \
--password-length 16
```
```shell PostgreSQL
akeyless dynamic-secret create postgresql \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--postgresql-statements "CREATE USER \"{{name}}\" WITH PASSWORD '{{password}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\"; GRANT CONNECT ON DATABASE postgres TO \"{{name}}\"; GRANT USAGE ON SCHEMA public TO \"{{name}}\";" \
--postgresql-revoke-statement "REASSIGN OWNED BY \"{{name}}\" TO {{userHost}}; DROP OWNED BY \"{{name}}\"; SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = '{{name}}'; DROP USER \"{{name}}\";" \
--password-length 16
```
```shell Redshift
akeyless dynamic-secret create redshift \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--redshift-statements "CREATE USER '{{username}}' WITH PASSWORD '{{password}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO '{{username}}';" \
--ssl "<false|true>" \
--password-length 16
```
```shell MSSQL
akeyless dynamic-secret create mssql \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--mssql-creation-statements "CREATE LOGIN {{name}} WITH PASSWORD = '{{password}}';" \
--mssql-revocation-statements "DROP LOGIN '{{name}}';" \
--password-length 16
```
```shell MSSQL RDS
akeyless dynamic-secret create mssql \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--mssql-creation-statements "CREATE LOGIN [{{name}}] WITH PASSWORD = '{{password}}'; \
             CREATE USER [{{name}}] FOR LOGIN [{{name}}];" \
--mssql-revocation-statements " DROP USER [{{name}}]; DROP LOGIN [{{name}}];" \
--password-length 16
```
```shell Azure SQL
akeyless dynamic-secret create mssql \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--mssql-creation-statements "CREATE USER [{{name}}] WITH PASSWORD = '{{password}}';" \
--mssql-revocation-statements "DROP USER IF EXISTS [{{name}}]" \
--password-length 16
```
```shell MongoDB
akeyless dynamic-secret create mongodb \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--mongodb-roles <New User Role> \
--password-length 16
```
```shell Oracle
akeyless dynamic-secret create oracledb \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--oracle-statements 'CREATE USER {{username}} IDENTIFIED BY "{{password}}"; GRANT CONNECT TO {{username}}; GRANT CREATE SESSION TO {{username}};' \
--password-length 16
```
```shell Cassandra
akeyless dynamic-secret create cassandra  \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--cassandra-statements "CREATE ROLE '{{username}}' WITH PASSWORD = '{{password}}' AND LOGIN = true; GRANT SELECT ON ALL KEYSPACES TO '{{username}}';" \
--password-length 16
```
```shell SAP HanaDB
akeyless dynamic-secret create hanadb \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--hanadb-creation-statements "CREATE USER {{name}} PASSWORD '{{password}}';GRANT 'MONITOR ADMIN' TO {{name}};" \
--hanadb-revocation-statements "DROP USER {{name}};" \
--password-length 16
```
```shell Vertica
#Vertica uses similar structures to PostgreSQL and so uses the same command in Akeyless with select changes

akeyless dynamic-secret create postgresql \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--postgresql-statements 'CREATE USER "{{name}}" WITH PASSWORD "{{password}}"; GRANT SELECT ON ALL TABLES IN SCHEMA public TO "{{name}}"; GRANT USAGE ON SCHEMA public TO "{{name}}";' \
--postgresql-revoke-statement 'DROP USER "{{name}}";' \
--password-length 16
```
```shell Redis
akeyless dynamic-secret create redis \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--acl-rules '["~*", "+@read", "+info"]'
```

Or using an inline connection string:

```shell MySQL/MariaDB
akeyless dynamic-secret create mysql \
--name <New Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--mysql-statements "CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}' PASSWORD EXPIRE INTERVAL 30 DAY;GRANT SELECT ON *.* TO '{{name}}'@'%';" \
--mysql-dbname <MySQL DB Name > \
--mysql-host <MySQL host> \
--mysql-port <MySQL port> \
--mysql-username <MySQL admin username> \
--mysql-password <MySQL admin password>
```
```shell PostgreSQL
akeyless dynamic-secret create postgresql \
--name <New Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--postgresql-db-name <PostgreSQL DB name> \
--postgresql-username <PostgreSQL DB admin username> \
--postgresql-password <PostgreSQL DBadmin password> \
--postgresql-host <PostgreSQL DB host> \
--postgresql-port <PostgreSQL DB port> \
--postgresql-statements 'CREATE USER "{{name}}" WITH PASSWORD "{{password}}"; GRANT SELECT ON ALL TABLES IN SCHEMA public TO "{{name}}"; GRANT CONNECT ON DATABASE postgres TO "{{name}}"; GRANT USAGE ON SCHEMA public TO "{{name}}";' \
--postgresql-revoke-statement 'REASSIGN OWNED BY "{{name}}" TO {{userHost}}; DROP OWNED BY "{{name}}"; SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = "{{name}}"; DROP USER "{{name}}";'
```
```shell Redshift
akeyless dynamic-secret create redshift \
--name <New Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--redshift-db-name <Redshift DB name> \
--redshift-username <Redshift DB admin username> \
--redshift-password <Redshift DB admin password> \
--redshift-host <Redshift DB host> \
--redshift-port <Redshift DB port> \
--redshift-statements "CREATE USER '{{username}}' WITH PASSWORD '{{password}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO '{{username}}';"
```
```shell MSSQL
akeyless dynamic-secret create mssql \
--name <New Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--mssql-creation-statements "CREATE LOGIN {{name}} WITH PASSWORD = '{{password}}';" \
--mssql-revocation-statements "DROP LOGIN '{{name}}';" \
--mssql-dbname <MSSQL Server DB Name> \
--mssql-username <MSSQL Server admin user> \
--mssql-password <MSSQL Server admin password> \
--mssql-host <MSSQL Server host name> \
--mssql-port <MSSQL Server port>
```
```shell MSSQL RDS
akeyless dynamic-secret create mssql \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--mssql-creation-statements "CREATE LOGIN [{{name}}] WITH PASSWORD = '{{password}}'; \
             CREATE USER [{{name}}] FOR LOGIN [{{name}}];" \
--mssql-revocation-statements " DROP USER [{{name}}]; DROP LOGIN [{{name}}];" \
--password-length 16
```
```shell Azure SQL
akeyless dynamic-secret create mssql \
--name <New Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--mssql-creation-statements "CREATE USER [{{name}}] WITH PASSWORD = '{{password}}';" \
--mssql-revocation-statements "DROP USER IF EXISTS [{{name}}]" \
--mssql-dbname <MSSQL Server DB Name> \
--mssql-username <MSSQL Server admin user> \
--mssql-password <MSSQL Server admin password> \
--mssql-host <MSSQL Server host name> \
--mssql-port <MSSQL Server port>
```
```shell MongoDB
akeyless dynamic-secret create mongodb \
--name <New Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--mongodb-roles <New User Role> \
--mongodb-name <MongoDB name> \
--mongodb-username <MongoDB server admin username> \
--mongodb-password <MongoDB server admin password> \
--mongodb-host-port <host:port>
```
```shell Oracle
akeyless dynamic-secret create oracledb \
--name <New Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--oracle-service-name <Your Oracle DB Service name > \
--oracle-username <Oracle DB admin username> \
--oracle-password <Oracle DB admin password> \
--oracle-host <Your Oracle DB host> \
--oracle-port <Oracle DB port> \
--oracle-statements 'CREATE USER {{username}} IDENTIFIED BY "{{password}}"; GRANT CONNECT TO {{username}}; GRANT CREATE SESSION TO {{username}};'
```
```shell Cassandra
akeyless dynamic-secret create cassandra  \
--name <path to your secret> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--cassandra-hosts <Cassandra host> \
--cassandra-port <Cassandra port> \
--cassandra-username <Cassandra username> \
--cassandra-password <password> \
--cassandra-statements "CREATE ROLE '{{username}}' WITH PASSWORD = '{{password}}' AND LOGIN = true; GRANT SELECT ON ALL KEYSPACES TO '{{username}}';"
```
```shell SAP HanaDB
akeyless dynamic-secret create hanadb \
--name <New Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--hana-dbname <HanaDB name> \
--hanadb-username <HanaDB admin username> \
--hanadb-password <HanaDB admin password> \
--hanadbt-host <HanaDB host> \
--hanadb-port <HanaDB port> \
--hanadb-creation-statements "CREATE USER {{name}} PASSWORD '{{password}}';GRANT 'MONITOR ADMIN' TO {{name}};" \
--hanadb-revocation-statements "DROP USER {{name}};"
```
```shell Vertica
#Vertica uses similar structures to PostgreSQL and so uses the same command in Akeyless with select changes

akeyless dynamic-secret create postgresql \
--name <New Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--postgresql-db-name <Vertica DB name> \
--postgresql-username <Vertica DB admin username> \
--postgresql-password <Vertica DBadmin password> \
--postgresql-host <Vertica DB host> \
--postgresql-port <Vertica DB port> \
--postgresql-statements 'CREATE USER "{{name}}" WITH PASSWORD "{{password}}"; GRANT SELECT ON ALL TABLES IN SCHEMA public TO "{{name}}"; GRANT USAGE ON SCHEMA public TO "{{name}}";' \
--postgresql-revoke-statement 'DROP USER "{{name}}";'
```
```shell Redis
akeyless dynamic-secret create redis \
--name <New Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--host <Redis host> \
--port[=6379] <Redis port> \
--username <Redis Username> \
--password <Redis Password> \
--acl-rules '["~*", "+@read", "+info"]'
```

Where:

* `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

* `target-name`: Full path of the [Target](doc:targets) item that stores the connection settings to your database server.

* `gateway-url`: Akeyless Gateway URL.

* `password-length`: **Optional** The temporary user password length.

Depending on each database, set the relevant creation and revocation statements to control and manage the level of access and roles of your temporary credentials.

For example, the PostgreSQL database provides a `creation` statement that controls the capabilities (**create**, **read**, **update**, or **delete**) and access levels for the databases and tables.

## RDS and Cloud-Managed Databases

The following explains how to use **Creation** and **Revocation** statements in RDS and Cloud-Managed Databases:

**Creation Statement**

Please add the following to the creation statement `GRANT “{{name}}” TO postgres;`, where `postgres` refers to the `postgresql-username` variable.

**Revocation Statement**

Standard **PostgreSQL** provides full superuser privileges, allowing complete cleanup of user-owned objects and active sessions before dropping a user.

In **RDS PostgreSQL**, the administrative role has limited privileges, so certain cleanup operations, such as reassigning ownership or terminating sessions, may not be supported. Therefore, simpler revocation commands are required when removing users in RDS.

The following is an example revocation statement for Postgres:

`REVOKE CONNECT ON DATABASE postgres FROM "{{name}}"; REVOKE USAGE ON SCHEMA public FROM "{{name}}"; REVOKE SELECT ON ALL TABLES IN SCHEMA public FROM "{{name}}"; DROP USER "{{name}}";`

<br />

> 📘 Info
>
> **MySQL 8 Dynamic Secrets**
>
> For MySQL 8, modify the default `CREATE USER` statement to allow native MySQL password authentication.
>
> For example:
>
> `CREATE USER '{{name}}'@'%' IDENTIFIED WITH mysql_native_password BY '{{password}}' PASSWORD EXPIRE INTERVAL 30 DAY;GRANT SELECT ON *.* TO '{{name}}'@'%';`

### Inline connection string

If you don't have a [Database Target](doc:database-targets), you can use the command with your database target server connection string inline:

Depending on your database type, provide a **privileged username** that has enough permission to create and revoke users on your database with the relevant connection settings. And set the relevant creation and revocation statements to control and manage the level of access and roles of your temporary credentials.

You can find the complete list of parameters for these commands in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets) section.

# Fetch a Dynamic Database Secret value from the CLI

To fetch a dynamic database secret value from the CLI, run the following command:

```shell Akeyless CLI
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

# Create a Dynamic Database Secret in the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the required database type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

* **Delete Protection:** When enabled, protects the secret from accidental deletion.

* **Target mode:** In this section, you can either select an existing [Database Target](doc:database-targets) or specify details of the DB Server explicitly.

* **User TTL:** Provide a time-to-live value for a dynamic secret. When TTL expires, temporary users and roles will be removed.

* **Custom Username Template:** Set a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) for the generated user.

* **Temporary Password Length** Set the length of the temporary password.

* **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.

* **Gateway:** Select the Gateway through which the dynamic secret will create users.

* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](doc:implement-zero-knowledge).

If you selected the **Explicitly specify target properties** mode, click **Next**.

Depending on your database type, provide a privileged username that has enough permission to create users on your database with the relevant connection settings.

Set the relevant create & revoke statements to control and manage the level of access for your temporary credentials.

5. Click **Finish**.

# Fetch a Dynamic Database Secret Value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click **Get Dynamic Secret** button.

# Tutorial

Check out our tutorial video on [Creating and Using MySQL Dynamic Secrets](https://tutorials.akeyless.io/docs/creating-and-fetching-dynamic-secrets) .
