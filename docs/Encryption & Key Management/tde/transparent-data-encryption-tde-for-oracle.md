---
title: TDE for Oracle
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
This guide explains how to configure Oracle Transparent Data Encryption (TDE) with Akeyless and an HSM library on a directly installed Oracle Database. Each step includes detailed explanations to help you understand the purpose and function of each command. Adjust the examples (such as directory paths, passwords, and API keys) as needed for your environment.

### Prerequisites

#### Steps & Explanations:

Oracle Database Installation:\
Step: Ensure that Oracle Database is installed and running on your system.\
Explanation: This guide assumes a direct installation of Oracle Database (**Oracle 19c RU or later, including all 23ai/23c builds**), without the use of containerization.

#### Oracle Database Version Check:

Step: Confirm your Oracle version (this guide is written for **Oracle 19c RU or later, including all 23ai/23c builds**) and its architecture (multitenant with CDB/PDB or single instance).\
Explanation: Configuration details such as keystore parameters can vary by version. For instance, Oracle 23ai deprecates certain parameters. Always verify with the official documentation.

#### Akeyless & HSM Library Requirements:

Step: Download the required shared library (libakeyless.so) from Akeyless.\
Explanation: This library provides the interface between Oracle TDE and the external key management (HSM) system. Ensure that you use the correct API credentials (access ID and key) so that the integration can securely communicate with Akeyless.

#### File and Directory Permissions:

Step: Ensure that the necessary directories (such as /opt/oracle/extapi, /logs, and configuration folders) have the proper ownership and permissions for the Oracle user.\
Explanation: Correct permissions are essential to avoid runtime errors and ensure that the Oracle Database and its wallet management processes have access to required files.

### Environment Setup and Library Installation

#### Install and Configure Akeyless HSM Library

##### Commands:

```shell
curl -o libakeyless.so https://akeylessservices.s3.us-east-2.amazonaws.com/services/pkcs11/release/linux/amd64/latest/libakeyless.so
```

##### Explanation:

This command downloads the HSM library, which is necessary for Oracle to interface with the Akeyless key management service.

### Create Required Directories and Install the Library

##### Commands:

```shell
mkdir -p /opt/oracle/extapi/64/hsm/akeyless/0.0.1/
cp libakeyless.so /opt/oracle/extapi/64/hsm/akeyless/0.0.1/
chown -R oracle:dba /opt/oracle
mkdir /logs
chown -R oracle:dba /logs
mkdir -p /var/akeyless/conf
```

##### Explanation:

#### Directory Structure:

Create the directory structure for the HSM library and the Akeyless configuration.

#### Copy and Set Permissions:

Copy the library into the proper location and ensure that the directories are owned by the Oracle user and the appropriate group, so the Oracle processes can access them.

### Configure the HSM Settings

##### Steps:

Create the pkcs11 configuration file:

```shell
vi /var/akeyless/conf/pkcs11.conf
```

Insert the following content, and customize the parameters to work with your Akeyless account:

```shell
log_level="info"
log_path="/logs/pkcs11.log"
akeyless_url="https://api.akeyless.io"
default_aes_mechanism="CBC"
base_item_path="/DB/Oracle/TDE-pkcs11"
[auth]
access_type="access_key"
access_id="p-9ss1....l83am"
access_key="oLw05FzH3Rgmca.............lcijrsReM="
```

##### Explanation:

* This file defines how the Oracle DB will interact with the Akeyless service. It includes logging settings, the Akeyless API Gateway URL (to use a local Gateway, reference the `/api/v2` endpoint), and the Authentication Method (supported auth methods also include `aws_iam`, `azure_ad`, `gcp`).
* Ensure your Auth Method is associated with an Access Roles granting it permissions to create and access items under the desired items folder (base\_item\_path)
* Notice: to configure TDE to create & leverage Akeyless [Classic Keys](https://docs.akeyless.io/docs/classic-keys) (the default is otherwise DFC) you can add the following setting (in the top section):\
  `use_classic_keys="true"`
  * To work with Classic Keys make sure you work against your own Gateway (on the API v2 endpoint), and grant the above Auth Method “Access Permissions” to said Gateway to manage “Classic Keys”

Set proper file permissions:

```shell
chown -R oracle:dba /var/akeyless/conf/pkcs11.conf
```

##### Explanation:

* Setting the correct ownership ensures that the Oracle user can access this file during runtime.

#### Database Wallet and TDE Configuration

###### Prepare the Database Directory

##### Commands:

```shell
cd $ORACLE_BASE/admin/your_db_name/
mkdir -p ./hsm_wallet/tde
```

##### Explanation:

* Navigate to the Admin Directory:
  * The directory $ORACLE\_BASE/admin/your\_db\_name/ is the default location for managing database-specific files. Replace “your\_db\_name” with your actual database name.
* Create Wallet Directory:
  * Creating the directory for the HSM wallet ensures that the TDE configuration has a designated location to store keystore files.

### Connect to the Database and Set Initial Parameters

##### Commands:

```shell
sqlplus / as sysdba
ALTER SYSTEM SET WALLET_ROOT='/opt/oracle/admin/your_db_name/hsm_wallet' SCOPE=SPFILE;
```

##### Explanation:

* Connecting via SQL\*Plus:
  * This gives you a SQL prompt as the system administrator (SYSDBA) to execute configuration commands.
* WALLET\_ROOT Parameter:
  * This command sets the root location for the wallet. The SCOPE=SPFILE option ensures that the change is saved in the server parameter file and used at the next startup.

### Restart the Database:

```shell
SHUTDOWN IMMEDIATE;
STARTUP;
```

##### Explanation:

A restart is necessary for the new parameter values (like WALLET\_ROOT) to take effect.

### Set TDE Configuration:

```shell
ALTER SYSTEM SET TDE_CONFIGURATION='KEYSTORE_CONFIGURATION=HSM' SCOPE=BOTH;
```

##### Explanation:

* TDE\_CONFIGURATION Parameter:
  * This command instructs Oracle TDE to use a keystore that is configured with HSM. The SCOPE=BOTH option applies the parameter change to both the in-memory environment and the spfile.

### Create and Open the HSM Wallet

##### Commands:

```shell
ADMINISTER KEY MANAGEMENT SET KEYSTORE OPEN IDENTIFIED BY "AKEYLESS" CONTAINER=ALL;
ADMINISTER KEY MANAGEMENT SET KEY IDENTIFIED BY "AKEYLESS" CONTAINER=ALL;
```

##### Explanation:

* Opening the Keystore:
  * The first command opens the keystore using the provided password ("AKEYLESS").
* Setting the Master Key:
  * The second command sets the TDE master encryption key. The CONTAINER=ALL option applies this change to the entire multitenant environment (both the container database and all pluggable databases).
* Verification:
  * You should verify in the Akeyless management console or by checking Oracle's views that the key has been created successfully.

### Enabling Auto Login

After the initial HSM configuration, the next steps transition the wallet to a state where it opens automatically at database startup.

### Transition from HSM to File-Based Wallet for Auto Login

##### Commands:

```shell
ADMINISTER KEY MANAGEMENT SET KEYSTORE CLOSE IDENTIFIED BY "AKEYLESS" CONTAINER=ALL;
ALTER SYSTEM SET TDE_CONFIGURATION="KEYSTORE_CONFIGURATION=FILE";
```

##### Explanation:

* Close the Keystore:
  * This command closes the HSM-based keystore in preparation for creating a file-based wallet for auto-login.
* Switch TDE Configuration:
  * Changing the parameter to "KEYSTORE\_CONFIGURATION=FILE" directs Oracle to use a file-based keystore for subsequent operations.

### Create a File-Based Keystore and Enable Auto Login

##### Commands:

##### Create the Keystore:

```shell
ADMINISTER KEY MANAGEMENT CREATE KEYSTORE '/opt/oracle/admin/your_db_name/hsm_wallet/tde' IDENTIFIED BY "AKEYLESS";
```

#### Explanation:

This command creates a new software keystore in the specified directory, secured by the provided password.

##### Open the Keystore:

```shell
ADMINISTER KEY MANAGEMENT SET KEYSTORE OPEN IDENTIFIED BY "AKEYLESS" CONTAINER=ALL;
```

##### Explanation:

Opens the newly created keystore so that further modifications can be made.

### Add the HSM Password as a Secret:

```shell
ADMINISTER KEY MANAGEMENT ADD SECRET 'AKEYLESS' FOR CLIENT 'HSM_PASSWORD' IDENTIFIED BY "AKEYLESS" WITH BACKUP;
```

##### Explanation:

This step adds the HSM’s password to the file-based keystore as a secret. The secret is necessary for operations that require HSM credentials without manual input.

### Close the Keystore:

```shell
ADMINISTER KEY MANAGEMENT SET KEYSTORE CLOSE IDENTIFIED BY "AKEYLESS" CONTAINER=ALL;
```

##### Explanation:

The keystore is closed to finalize the changes after the secret has been added.

### Create Auto-Login Keystore:

```shell
ADMINISTER KEY MANAGEMENT CREATE AUTO_LOGIN KEYSTORE FROM KEYSTORE '/opt/oracle/admin/your_db_name/hsm_wallet/tde' IDENTIFIED BY "AKEYLESS";
```

##### Explanation:

This command generates an auto-login version of the file-based wallet. The auto-login keystore allows Oracle to open the wallet automatically at startup, eliminating the need for manual intervention.

{/*

 

### Reverse Migrate the Encryption Key:

```shell
ADMINISTER KEY MANAGEMENT SET ENCRYPTION KEY IDENTIFIED BY "AKEYLESS" REVERSE MIGRATE USING "AKEYLESS" WITH BACKUP;
```

##### Explanation:

Reverse migration applies the encryption key from the HSM-based configuration to the new file-based wallet, ensuring that the master encryption key remains consistent between configurations.

*/}

Reference: [Configuring an Auto-Open Connection into an External Key Manager](https://docs.oracle.com/en/database/oracle/oracle-database/19/asoag/managing-keystore-and-tde-master-encryption-key.html#GUID-1E8CD504-A87D-4690-8076-B2F1BA8EC645)

### Update TDE Configuration for Both HSM and File Keystores:

```shell
ALTER SYSTEM SET TDE_CONFIGURATION="KEYSTORE_CONFIGURATION=HSM|FILE";
```

> 📘 Note
>
> When using Oracle RAC, perform all the above steps only on one target instance and have all the other RAC instance(s) shutdown. After following the above steps copy the `cwallet.sso` and `ewallet.p12` file from the configured node to all the other node(s) at the same `<software_wallet_location>` location. After copying `cwallet.sso` and `ewallet.p12` on the other node(s), restart all the other RAC instance(s).

##### Explanation:

This update configures Oracle to recognize both the HSM and file-based keystore settings, providing a fallback mechanism and facilitating a smoother transition.

### Post-Restart Verification

##### Commands:

```shell
SHUTDOWN IMMEDIATE;
STARTUP;
SELECT * FROM V$ENCRYPTION_WALLET;
```

##### Explanation:

* Restart the Database:
  * A restart is necessary for the new wallet configuration to fully take effect.
* Verify Wallet Status:
  * Running the query against V$ENCRYPTION\_WALLET confirms that the wallet is open and shows the expected configuration. The output should indicate that the wallet is properly configured for auto-login.

In a multitenant environment (CDB/PDB). Note that you may see multiple rows corresponding to each container (for example, CON\_ID=0 for the CDB root, CON\_ID=5 for a PDB):

![](https://files.readme.io/0000d0f056d736ed13b4dd2f0a76517a1954d665075d3df44bf745543f7af6ef-2082746d-b5e1-467e-bb62-8923dffaefe0_1.png)

Key Points About the Columns:

* WRL\_TYPE: The type of wallet location in use (e.g., FILE, HSM).
* WRL\_PARAMETER: The file system path or parameter details for the wallet (sometimes blank for HSM rows).
* STATUS: Should be OPEN if the wallet is active and accessible.
* WALLET\_TYPE: Indicates whether it is AUTOLOGIN, HSM, or another type.
* WALLET\_OR\_KEYSTORE: Shows whether it’s a PRIMARY or SECONDARY wallet. In configurations using both HSM and FILE, the file wallet often appears as PRIMARY and HSM as SECONDARY.
* FULLY\_BACK: Indicates if the wallet is fully backed up. Common values are NONE or UNDEFINED.
* CON\_ID: The container ID. 0 typically refers to the root container (CDB$ROOT), while non-zero values (5) refer to pluggable databases (PDBs).
* STATUS: Should display “OPEN” if the keystore is accessible.\
  Additional Note: If the keystore is open but the TDE master encryption key has not yet been created—or if the wallet is configured as an SSL wallet rather than a TDE wallet—the STATUS column may show OPEN\_NO\_MASTER\_KEY.

For more details on these columns, refer to the official Oracle documentation:

Reference: [ENCRYPTION\_WALLET](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-ENCRYPTION_WALLET.html) , 

### Additional Notes and Version-Specific Considerations

#### Oracle Version Differences

##### For Oracle 19c:

##### Explanation:

In a 19c environment (which may use a multitenant architecture with a CDB/PDB), you have the option to use united mode (one master key for all containers) or isolated mode (separate keys per PDB). 

{/*

 

Note that reverse migration from an HSM to a file-based wallet may not be supported in united mode.

.

*/}

Reference:\
[Oracle 19c Advanced Security Guide ​](https://docs.oracle.com/en/database/oracle/oracle-database/19/asoag/managing-keystores-encryption-keys-in-united-mode.html#GUID-02343C2C-160B-4950-A191-48317B20C507)

#### For Oracle 23ai:

##### Explanation:

Some parameters, such as ENCRYPTION\_WALLET\_LOCATION, are deprecated in 23ai. Always consult the latest Oracle documentation for current key management practices.

Reference:\
[Introduction to TDE for Oracle 23ai ​](https://docs.oracle.com/en/database/oracle/oracle-database/23/dbtde/introduction-to-transparent-data-encryption.html#GUID-B0870B12-E6AD-4254-B4B3-D6A15A637975)

### Explanation of ENCRYPTION\_WALLET Status

##### Explanation:

* If you see OPEN\_NO\_MASTER\_KEY in the output of V$ENCRYPTION\_WALLET, it means that while the keystore is open, the master encryption key has not been created yet. This can also occur if the wallet location is configured for an SSL wallet (created with orapki) rather than a TDE wallet.
* Reference:\
  [Why ENCRYPTION\_WALLET Shows OPEN\_NO\_MASTER\_KEY](https://support.oracle.com/rs?type=doc\&id=2641533.1) ​

### Summary and Final Checks

#### Final Checklist & Explanation:

##### Environment Preparation:

* Confirm Oracle Database is installed and running on your system.
* Verify you are using the correct Oracle version and architecture.
* Ensure all required libraries and configuration files are in place with proper permissions.\
  Explanation: This minimizes the risk of errors during the TDE configuration process.

##### Initial HSM Wallet Configuration:

* Configure and open the HSM-based keystore.
* Set the TDE master encryption key.\
  Explanation: These steps secure the database encryption process by integrating the HSM library and initializing the keystore.

##### Auto-Login Enablement:

* Transition from the HSM wallet to a file-based wallet.
* Create an auto-login keystore so that the wallet opens automatically at startup.\
  Explanation: Auto-login keystores remove the need for manual intervention during database startup, which is critical for production environments.

##### Verification:

* Restart the database.
* Verify the wallet status using `SELECT * FROM V$ENCRYPTION_WALLET;`.\
  Explanation: This confirms that the configuration changes are applied correctly and the keystore is accessible.

##### Version Considerations:

* Adjust settings as needed and consult the latest documentation, since configuration parameters may differ across Oracle versions.
* Explanation: Ensuring that your configuration complies with the current Oracle guidelines is essential for security and stability.

### Column and Tablespace Encryption

#### Column Encryption

Create a table with column encryption option.

```shell
CREATE TABLE EMPLOYEES (ID INT, NAME VARCHAR (200), SALARY INT ENCRYPT);
```

Enter some values.

```shell
INSERT INTO EMPLOYEES VALUES (1, 'Bob', 10000);
```

Access the data using the SELECT query.

```shell
SELECT * FROM EMPLOYEES;
```

Check the encrypted columns in the database.

```shell
SELECT * FROM EMPLOYEES;
```

#### Tablespace Encryption

Create an encrypted tablespace. Then create a table in that tablespace.

```shell
CREATE TABLESPACE ENCRYPTED_SPACE DATAFILE '$ORACLE_HOME/dbs/enc_space.dbf' SIZE 150M ENCRYPTION USING 'AES256' DEFAULT STORAGE (ENCRYPT);  
CREATE TABLE CUSTOMERS (ID INT, NAME VARCHAR (200), CREDIT_LIMIT INT) TABLESPACE ENCRYPTED_SPACE;
```

Insert some values into the CUSTOMERS table.

```shell
INSERT INTO CUSTOMERS VALUES (1, 'Bob', 10000);
```

Access the data using the select query.

```shell
SELECT * FROM CUSTOMERS;
```

Check the encrypted tablespaces in the database:

```shell
SELECT * FROM V$ENCRYPTED_TABLESPACES;
```

> 👍 Note
>
> To migrate a database with an existing file-based wallet, follow these steps:
>
> 1. Set the TDE configuration:
>
> ```sql
> ALTER SYSTEM SET TDE_CONFIGURATION="KEYSTORE_CONFIGURATION=HSM|FILE" SCOPE=both SID='*';
> ```
>
> 2. Migrate the encryption key:
>
> ```sql
> ADMINISTER KEY MANAGEMENT SET ENCRYPTION KEY IDENTIFIED BY "akeyless" MIGRATE USING "<old file based tde password>" WITH BACKUP;
> ```
>
> Ensure to replace <old file based tde password> with the appropriate password.
