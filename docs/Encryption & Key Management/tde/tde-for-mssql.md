---
title: TDE for MSSQL
excerpt: EKM Provider
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Transparent data encryption ([TDE](https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/transparent-data-encryption?view=sql-server-ver16)) encrypts SQL Server data files. This encryption is known as encrypting data at rest. The encryption uses a database encryption key (**DEK**). The database boot record stores the key for availability during recovery. The **DEK** is a symmetric key, and is secured by a certificate that the server's master database stores or by an asymmetric key that an [EKM](https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/enable-tde-on-sql-server-using-ekm?view=sql-server-ver16)  module protects.

**TDE** protects data at rest, which is the data and log files. It lets you follow many laws, regulations, and guidelines established in various industries. This ability lets software developers encrypt data by using **AES** and **3DES** encryption algorithms without changing existing applications.

<Callout icon="📒" theme="default">
  ### **Platform prerequisites**

  *The TDE for MSSQL workflow documented above has been tested**only** with full SQL Server installations on Windows (on-prem or in an Azure “SQL Virtual Machine”).*  

  **Not supported**\
  • MSSQL in Docker containers (Microsoft does not support TDE in containers)\
  • Azure SQL Managed DB / Managed Instance (they only expose Azure Key Vault for external keys)  

  **Supported**\
  • Traditional Windows Server + SQL Server\
  • Azure “SQL VM” (a standard VM running SQL Server)
</Callout>

# Install the Akeyless EKM provider

1. Download and run the official Akeyless EKM provider:

```curl
curl https://akeylessservices.s3.us-east-2.amazonaws.com/services/akeyless-crypto-provider/release/latest/AkeylessEkmProviderInstaller.msi --output AkeylessEkmProviderInstaller.msi
```

Follow the wizard installation steps - enter your Akeyless [Gateway](doc:api-gw) URL using the `/api/v2` endpoint (previously port  `8081`), and choose a path in the Akeyless platform to store the keys.

Choose the OS installation path and save it for later. This will copy the `dll`  files, and also creates a configuration file that can be edited later. 

> 📘 The file should be formatted as follows:
>
> log\_level="debug"\
> akeyless\_url="https\://Your-GW-URL/api/v2"\
> base\_item\_path=" /path/to/keys"\
> use\_classic\_keys=true

**Notice:** It is optional to configure TDE to create & leverage Akeyless [Classic Keys](doc:classic-keys), the default is otherwise using a DFC key.

* To work with Classic Keys, make sure you work against your own Gateway (on the API v2 endpoint)

# Configure the Akeyless EKM provider

Open Microsoft SQL Server Management Studio, and run the SQL commands below to complete the installation.

1. Enable the **EKM** provider on the MSSQL server:

```sql
USE master;
GO
sp_configure 'show advanced', 1
GO
RECONFIGURE
GO
sp_configure 'EKM provider enabled', 1
GO
RECONFIGURE
GO
```

2. Create the **EKM** provider named Akeyless using the `dll` file from the installation folder: 

```sql
CREATE CRYPTOGRAPHIC PROVIDER Akeyless
FROM FILE = 'C:\Program Files\Akeyless\Akeyless Ekm Provider\AkeylessEkm.dll'
```

3. Create a SQL `CREDENTIAL` that will be used by the system administrators to access Akeyless from the SQL server, for example using an [API Key](doc:api-key) which is stored inside a SQL `CREDENTIAL` named `akeyless_tde`

```sql
CREATE CREDENTIAL akeyless_tde
WITH IDENTITY = '<ACCESS_ID>', SECRET = '<ACCESS_KEY>'
FOR CRYPTOGRAPHIC PROVIDER Akeyless ;
GO
```

* For instance, if you wish to utilize`'azure ad authentication'`you will need to modify the configuration file located in the installation directory at`'C:\Program Files\Akeyless\Akeyless Ekm Provider\sqlcrypt.conf'` Specifically, add the following lines:\
  `[auth]
  access_type="azure_ad"
  object_id="..." # optional`

<Callout icon="📒" theme="default">
  ### Access-Role Reminder

  The API Key (or other Auth Method) used in **`akeyless_tde`** **must** be linked to an Akeyless **Access Role** that grants **Create**, **Read**, and **List** permissions on the TDE key path you chose earlier.

  When working **Classic Keys**, make sure you also  grant the Auth Method the appropriate Gateway “[Access Permissions](doc:gateway-access-permissions)” to manage “**Classic Keys**”
</Callout>

4. Add the credential to a privileged user, in the following example replace the [`DOMAIN\login`] with your privileged username format and add the SQL `CREDENTIAL`:

```sql
ALTER LOGIN [DOMAIN\login]
ADD CREDENTIAL akeyless_tde;
GO
```

5. Create an asymmetric key for the **EKM** provider.  This will create a key in Akeyless named `SQL_Server_Key`. To work with an existing key add the`CREATION_DISPOSITION = OPEN_EXISTING`. The following algorithms are supported: `RSA_2048`, `RSA_3072`, or `RSA_4096`:

```sql
CREATE ASYMMETRIC KEY akls_ekm_login_key
FROM PROVIDER Akeyless
WITH ALGORITHM = RSA_2048,
PROVIDER_KEY_NAME = 'SQL_Server_Key'
GO
```

> 📘 Working on Cluster
>
> When working with cluster, the above command should be executed only on the Primary server, on all other servers run the following statement: 
>
> `CREATE ASYMMETRIC KEY akls_ekm_login_key
> FROM PROVIDER Akeyless WITH PROVIDER_KEY_NAME = 'SQL_Server_Key' , CREATION_DISPOSITION=OPEN_EXISTING;`

6. Create **another** SQL credential that the database engine (**TDE**) will use:

```sql
CREATE CREDENTIAL akls_ekm_tde_cred
WITH IDENTITY = '<ACCESS_ID>', SECRET = '<ACCESS_KEY>'
FOR CRYPTOGRAPHIC PROVIDER Akeyless ;  
GO
```

7. Create a login that will be used by the database engine (**TDE**) using the key that we created, and add the new credential to the login.

```sql
CREATE LOGIN akls_EKM_Login
FROM ASYMMETRIC KEY akls_ekm_login_key ;
GO  

ALTER LOGIN akls_EKM_Login
ADD CREDENTIAL akls_ekm_tde_cred ;
GO  
```

8. Create the database encryption key that will be used for **TDE**.  In the following example `AdventureWorks` is a placeholder for the database name. Supported algorithms are `AES_128` or `AES_256`. 

```sql
USE [AdventureWorks] ;
GO  
CREATE DATABASE ENCRYPTION KEY
WITH ALGORITHM  = AES_128  
ENCRYPTION BY SERVER ASYMMETRIC KEY akls_ekm_login_key ;
GO  
```

Note: This doesn’t create a new key in the Akeyless platform, the key is created inside the database and encrypted by using the key from Akeyless.

9. Alter the database to enable transparent data encryption.

```sql
ALTER DATABASE [AdventureWorks]
SET ENCRYPTION ON ;
GO
```

# Troubleshooting

If you're running into issues getting TDE with Akeyless set up on MSSQL, here are some useful tips and common pitfalls to check:

* If you're looking for logs about the setup, you can find them in the **Windows Event Viewer** — most EKM-related errors are recorded there and are very helpful for debugging.
* After you first run the installer, any future changes to the configuration file (which by default will be located under: `C:\\Program Files\\Akeyless\\Akeyless Ekm Provider\\sqlcrypt.conf`) will only take effect after restarting the `SQL Server (MSSQLSERVER)` Windows service.
* If no config file is found, the setup will default to using [https://api.akeyless.io](https://api.akeyless.io) as the Akeyless Gateway URL and the root path / for key creation.
* Make sure the key was created at the specified path in Akeyless. If not:
  * Confirm that the TDE auth method you created has an Access Role permitting access to that path.
  * If you are using Classic Keys (instead of DFC), ensure the auth method also has Gateway Access Permissions to manage Classic Keys.
