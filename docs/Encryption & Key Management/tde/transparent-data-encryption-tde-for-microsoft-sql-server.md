---
title: Transparent Data Encryption (TDE) for Microsoft SQL Server
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Transparent Data Encryption ([TDE](https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/transparent-data-encryption?view=sql-server-ver16)) encrypts SQL Server data files to protect data at rest. The encryption uses a Database Encryption Key (DEK) that is secured by a certificate stored in the master database or by an asymmetric key protected by an External Key Management ([EKM](https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/enable-tde-on-sql-server-using-ekm?view=sql-server-ver16)) module like Akeyless.

### Prerequisites

Ensure the following conditions are met before proceeding with the configuration:

- MSSQL is deployed directly on a Windows Server environment.
  - TDE does not support:
    - MSSQL running in Docker (not supported by Microsoft).
    - Azure SQL Managed Databases or Managed Instances (only support Azure Key Vault, not external KMS options).
  - However, SQL Virtual Machine (VM) in Azure is supported, as it behaves similarly to running SQL Server on a VM.
- Ensure you have Administrator privileges on the Windows Server and MSSQL.
- Install the required .NET Framework to avoid issues with the sqlcrypt.conf file generation.

### Install the Akeyless EKM Provider

- Download and run the Akeyless EKM provider by executing the following  `curl` command:

```curl
curl https://akeylessservices.s3.us-east-2.amazonaws.com/services/akeyless-crypto-provider/release/latest/AkeylessEkmProviderInstaller.msi --output AkeylessEkmProviderInstaller.msi
```



- Run the MSI installer and follow the wizard installation steps:
  - Enter your Akeyless [Gateway](https://docs.akeyless.io/docs/api-gw) URL (port 8081) when prompted.
  - Choose the path in Akeyless to store the keys.
  - Choose the OS installation path and save it for later reference. This process will:
    - Copy the .dll files.
    - Create the configuration file (sqlcrypt.conf), which can be edited later.

The location of the sqlcrypt.conf file is depended on the installation path, Default location is:

"C:\\Program Files\\Akeyless\\Akeyless Ekm Provider\\sqlcrypt.conf"

The format of the file should look like this:

log_level="error"  
akeyless_url="<https://api.akeyless.io"> \<---- api v2 (8081 or 8000/api/v2)  
base_item_path="/sqlcrypt" \<--- base path for the keys to be created



> 📘 Note
> 
> Note: If the installer does not generate the `sqlcrypt.conf`  file, refer to the Troubleshooting section below.

### Configure the Akeyless EKM Provider

- Enable the EKM provider on the MSSQL server:

```curl SQL
USE master;
GO
sp_configure 'show advanced', 1;
GO
RECONFIGURE;
GO
sp_configure 'EKM provider enabled', 1;
GO
RECONFIGURE;
GO

```

- Create the Akeyless EKM provider using the .dll file from the installation folder:

```curl SQL
CREATE CRYPTOGRAPHIC PROVIDER Akeyless
FROM FILE = 'C:\Program Files\Akeyless\Akeyless Ekm Provider\AkeylessEkm.dll';
```

- Create a SQL CREDENTIAL that will be used by system administrators to access Akeyless from the SQL Server, for example, using an API Key:

```curl SQL
CREATE CREDENTIAL akeyless_tde
WITH IDENTITY = '<ACCESS_ID>', SECRET = '<ACCESS_KEY>'
FOR CRYPTOGRAPHIC PROVIDER Akeyless;
GO
```



> 📘 Note
> 
> Make sure to replace \<ACCESS_ID> and \<ACCESS_KEY> with your actual API Key credentials from Akeyless.

- Assign the SQL CREDENTIAL to a privileged user (replace [DOMAIN\login] with your privileged user format):

```curl SQL
ALTER LOGIN [DOMAIN\login]
ADD CREDENTIAL akeyless_tde;
GO
```

- Create an asymmetric key for the EKM provider. This creates a key in Akeyless called SQL_Server_Key. To work with an existing key, add `CREATION_DISPOSITION = OPEN_EXISTING`. Supported algorithms: `RSA_2048`, `RSA_3072`, ` RSA_4096`



```curl SQL
CREATE ASYMMETRIC KEY akls_ekm_login_key
FROM PROVIDER Akeyless
WITH ALGORITHM = RSA_2048,
PROVIDER_KEY_NAME = 'SQL_Server_Key';
GO
```



> 📘 Note
> 
> Note for Clusters: When working with a cluster, execute the above command only on the Primary server. On all other servers, use:



```curl SQL
CREATE ASYMMETRIC KEY akls_ekm_login_key
FROM PROVIDER Akeyless
WITH PROVIDER_KEY_NAME = 'SQL_Server_Key',
CREATION_DISPOSITION=OPEN_EXISTING;
```

- Create another SQL credential that the database engine (TDE) will use:

```curl SQL
CREATE CREDENTIAL akls_ekm_tde_cred
WITH IDENTITY = '<ACCESS_ID>', SECRET = '<ACCESS_KEY>'
FOR CRYPTOGRAPHIC PROVIDER Akeyless;
GO
```

- Create a login used by the database engine (TDE), and associate the new credential:

```curl SQL
CREATE LOGIN akls_EKM_Login
FROM ASYMMETRIC KEY akls_ekm_login_key;
GO

ALTER LOGIN akls_EKM_Login
ADD CREDENTIAL akls_ekm_tde_cred;
GO
```

- Create the database encryption key that will be used for TDE (replace `AdventureWorks` with your actual database name). Supported algorithms are `AES_128` or `AES_256`:

```curl SQL
USE [AdventureWorks];
GO
CREATE DATABASE ENCRYPTION KEY
WITH ALGORITHM = AES_128
ENCRYPTION BY SERVER ASYMMETRIC KEY akls_ekm_login_key;
GO
```

> 📘 Note
> 
> This does not create a new key in the Akeyless platform. The key is created inside the database and encrypted using the key from Akeyless.

- Enable Transparent Data Encryption (TDE):

```curl SQL
ALTER DATABASE [AdventureWorks]
SET ENCRYPTION ON;
GO
```



### Verification of TDE Configuration

To verify that TDE is properly configured and the database is encrypted, you can use the following SQL query:

```curl SQL
SELECT db.name AS DatabaseName, 
       dm.encryption_state,
       dm.encryption_state_desc,
       dm.encryptor_type
FROM sys.dm_database_encryption_keys dm
JOIN sys.databases db ON db.database_id = dm.database_id
WHERE db.name = 'TestDB'; -- Replace with your actual database name
```

- The `encryption_state` value should return 3, which means "Encrypted".

For example, the result should look similar to:

![](https://files.readme.io/5082a1e3f8881e26ac52f47aff100ade7464fc810f55e4800b557a386bc64514-Screenshot_2024-10-16_at_17.04.33.png)



### Troubleshooting

If you encounter issues during the installation or configuration, follow these steps:

- Missing sqlcrypt.conf File:
  - If the `sqlcrypt.conf` file was not created during installation, it could be due to a .NET Framework issue. The file is generated using a C# utility, so ensure that the correct version of .NET Framework is installed.
- Check Windows Event Viewer Logs:
  - All errors encountered during installation and configuration will be logged in the **Windows Event Viewer Logs.** This is useful for diagnosing the issue.
- Default Configuration Values:
  - If the sqlcrypt.conf file is missing, the system defaults to using the **Akeyless public gateway** (<https://api.akeyless.io>) and the default **root base path** (/).
- Configuration Changes:
  - Any changes made to the sqlcrypt.conf file after it is created **require a restart of the “SQL Server (MSSQLSERVER)**” service for the changes to take effect.