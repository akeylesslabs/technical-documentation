---
title: TDE Setup (using HSM) for Oracle Database
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
This document outlines the steps to set up Transparent Data Encryption (TDE) on Oracle Database 19c and above, using an HSM wallet for encryption. This guide includes the creation of directories, keystore configuration, and verification of the wallet status.

### Directory Creation

•	Create the folder and subfolder /tde.  
•	No changes required to sqlnet.ora for Oracle Database 19c and up.

### Configuration Steps

a. In this example, we use hsm_wallet as the base folder. This can be adjusted based on your specific environment or the naming conventions used in your organization.

b. The APP_PASSWORD is not directly used during the configuration process. It can be any value, as the actual configuration is pulled from a file.

c. /opt/oracle/admin corresponds to the $ORACLE_HOME directory in your environment.

### Key Management and Keystore Setup

Perform the following commands in SQL\*Plus or another Oracle SQL interface:

```text SQL
SQL> ADMINISTER KEY MANAGEMENT SET KEYSTORE CLOSE IDENTIFIED BY akeyless;
```

Result: Keysotre closed successfully 

```text SQL
SQL> ALTER SYSTEM SET TDE_CONFIGURATION="KEYSTORE_CONFIGURATION=FILE";
```

Result: System altered to use FILE-based keystore configuration.

```text SQL
SQL> ADMINISTER KEY MANAGEMENT CREATE KEYSTORE '/opt/oracle/admin/FREE/hsm_wallet/tde' IDENTIFIED BY "APP_PASSWORD";
```

Result: Keystore created at the specified location.

```text SQL
SQL> ADMINISTER KEY MANAGEMENT SET KEYSTORE OPEN IDENTIFIED BY "APP_PASSWORD";
```

Result: Keystore opened seccessfully

```text SQL
SQL> ADMINISTER KEY MANAGEMENT ADD SECRET 'APP_PASSWORD' FOR CLIENT 'HSM_PASSWORD' IDENTIFIED BY "APP_PASSWORD" WITH BACKUP;
```

Result: Secret added successfully for client HSM_PASSWORD.

```text SQL
SQL> ADMINISTER KEY MANAGEMENT SET KEYSTORE CLOSE IDENTIFIED BY "APP_PASSWORD";
```

Result: Keystore closed again

```text SQL
SQL> ADMINISTER KEY MANAGEMENT CREATE AUTO_LOGIN KEYSTORE FROM KEYSTORE '/opt/oracle/admin/FREE/hsm_wallet/tde' IDENTIFIED BY "APP_PASSWORD";
```

Result: Auto-login key store created. 

```text SQL
SQL> ALTER SYSTEM SET TDE_CONFIGURATION="KEYSTORE_CONFIGURATION=HSM|FILE";
```

Result: System altered to use a combination of HSM and file-based keystore configurations.

### Post-Restart Verification

After restarting the database, you can verify that the HSM wallet is open and correctly configured.

```text SQL
SQL> shutdown immediate;
Database closed.
Database dismounted.
ORACLE instance shut down.

SQL> startup;
ORACLE instance started.
```

Verification Output: Check the database’s global area and buffers. The database should be opened successfully.

```text SQL
SQL> SELECT * FROM V$ENCRYPTION_WALLET;
```

#### Expected Output

```text SQL
WRL_TYPE   WRL_PARAMETER                      STATUS            WALLET_TYPE  WALLET_OR  KEYSTORE FULLY_BAC  CON_ID
---------- --------------------------------- ----------------- ------------- ---------- ------------- --------
FILE       /opt/oracle/admin/FREE/hsm_wallet/tde/  OPEN_UNKNOWN_MASTER_KEY_STATUS  AUTOLOGIN    SINGLE  NONE    UNDEFINED   1
HSM        OPEN                               HSM                 SINGLE       NONE         UNDEFINED   1
FILE       OPEN_UNKNOWN_MASTER_KEY_STATUS    AUTOLOGIN           SINGLE       UNITED      UNDEFINED   2
HSM        OPEN                               HSM                 SINGLE       UNITED      UNDEFINED   2
FILE       OPEN_NO_MASTER_KEY                AUTOLOGIN           SINGLE       UNITED      UNDEFINED   3
HSM        OPEN_NO_MASTER_KEY               HSM                 SINGLE       UNITED      UNDEFINED   3
```

#### Error Handling

If you encounter the following error:

```text SQL
SQL> ALTER SYSTEM SET WALLET OPEN IDENTIFIED BY akeyless;
ERROR at line 1:
ORA-28354: Encryption wallet, auto login wallet, or HSM is already open.
```

This error indicates that the wallet is already open. Refer to Oracle documentation for troubleshooting: [ORA-28354: Wallet Already Open](https://docs.oracle.com/en/error-help/db/ora-28354/?r=23ai)