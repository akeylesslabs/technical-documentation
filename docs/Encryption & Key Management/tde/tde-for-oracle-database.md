---
title: TDE for Oracle Database
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
**Introduction**

Transparent Data Encryption (TDE) is a security feature provided by Oracle Database that enables the encryption of sensitive data stored within tables and tablespaces. While Oracle Database employs authentication, authorization, and auditing mechanisms to secure data during access and usage within the database, it does not inherently protect the data stored in the operating system files. These files, which contain the actual data, can be vulnerable to unauthorized access. To mitigate this risk, Akeyless offers integration with TDE, enabling the encryption of data at the storage level. This ensures that even if an unauthorized user gains access to the data files, the data remains unreadable, thereby enhancing overall data security.

**Oracle Database Integration Configuration**

To ensure compatibility, Oracle Database must be on an supported version. The supported Oracle Database versions for PKCS#11 integration with Transparent Data Encryption (TDE) are as follows:

* 11g Release 2 (11.2)
* 12c: Including both 12c Release 1 (12.1) and 12c Release 2 (12.2)
* 18c
* 19c
* 21c
* 23c

## Key Concepts of TDE

**TDE Table Key:** A TDE Table Key is a unique encryption key associated with a specific table that has columns marked for encryption. Each table that requires encryption will have its own TDE Table Key. This key is responsible for encrypting the data in the specified columns of the table. However, to further secure the TDE Table Key itself, it is encrypted by the TDE master encryption key. This two-tier encryption mechanism adds an additional layer of security by ensuring that the table-specific encryption key cannot be easily compromised.

**Tablespace Encryption Key:** In addition to table-level encryption, TDE also supports the encryption of entire tablespaces, which are logical storage units within the Oracle Database. A Tablespace Encryption Key is used to encrypt all the data stored within a tablespace. Similar to the TDE Table Key, the Tablespace Encryption Key is protected by the TDE master encryption key. This key hierarchy means that the data in the tablespace is encrypted by the Tablespace Encryption Key, which is, in turn, encrypted by the TDE master encryption key.

## How TDE Works

**Data Encryption Process:** When data is written to a table or tablespace that is protected by TDE, the Oracle Database automatically encrypts the data using either the TDE Table Key or the Tablespace Encryption Key, depending on the level of encryption applied (table or tablespace). The encryption process is transparent to the end-user, meaning that no changes are required in the application code or queries. The data is stored in an encrypted format in the data files.

**Data Decryption Process:** When an authorized user or application retrieves data from an encrypted table or tablespace, TDE automatically decrypts the data. The appropriate encryption key (TDE Table Key or Tablespace Encryption Key) is retrieved from the keystore, and the data is decrypted before being presented to the user or application. Again, this process is seamless and does not require any special handling by the user.

**Keystore Management:** The keystore, which houses the master encryption key and other related keys, must be securely managed. Administrators are responsible for ensuring that the keystore is accessible to the Oracle Database but protected from unauthorized access. Proper management of the keystore is critical because if the keystore is compromised or lost, the encrypted data may become inaccessible.

## Security Benefits of TDE

**Data Protection at Rest:**\
TDE ensures that sensitive data remains secure even when stored in the database's physical files on the operating system. This protection is crucial for compliance with data protection regulations and safeguarding against data breaches.

**Seamless Implementation:**\
Since TDE operates transparently at the database level, no modifications to existing applications or database schemas are required. The encryption and decryption processes are handled automatically by the database, simplifying the implementation of data security.

**Centralized Key Management:**\
By using an external keystore for encryption key management, TDE provides centralized control over key usage and rotation. This centralization ensures that encryption keys are properly managed and protected, further enhancing data security.

## Setting Up Oracle Database for Integration

To implement Transparent Data Encryption (TDE) with Oracle Database, Akeyless offers a PKCS#11 shared library file. This standard provides a platform-independent API designed to interface with cryptographic tokens, including hardware security modules (HSMs) and smart cards. By leveraging the Akeyless PKCS#11 shared library, organizations can seamlessly integrate their Oracle Database with the Akeyless Platform, ensuring secure key management and encryption functionalities.

Download the Akeyless PKCS#11 file to your Oracle server: 

```shell
curl -o libakeyless.so https://akeylessservices.s3.us-east-2.amazonaws.com/services/pkcs11/release/linux/amd64/latest/libakeyless.so
```

And set the following permissions and folders:

```shell
mkdir -p /opt/oracle/extapi/64/hsm/akeyless/0.0.1/ && \
cp libakeyless.so /opt/oracle/extapi/64/hsm/akeyless/0.0.1/. && \
chown -R oracle:dba /opt/oracle && \
mkdir /logs && \
chown -R oracle:dba /logs
```

With a privilege user permission on your Database server, create the following file:

```shell
touch /var/akeyless/conf/pkcs11.conf
```

Edit the created `pkcs11.conf` file and set the following:

```shell
log_level="info"
log_path="/logs/pkcs11.log"
akeyless_url="https://<your-Akeyless-Gateway-URL>:8081"
default_aes_mechanism="CBC"
base_item_path="/pkcs11"
[auth]
access_type="access_key"
access_id="<Access Id>"
access_key="<Access Key>"
```

 Where:

* `akeyless_url` is your [Akeyless Gateway](doc:api-gw) URL on API port `8081`.

* `base_item_path` - The destination path, to save all your TDE encryption keys inside the Akeyless Platform. Ensure your [Authentication Method](doc:access-and-authentication-methods) has permission to create and manage items under the desired path. 

* The `[auth]` section should be set with the relevant [Authentication Method](doc:access-and-authentication-methods) type and settings. Using the same structure as the Akeyless [CLI](doc:cli) profile setting file.

* `default_aes_mechanism` - Set the type of **AES** encryption keys. Oracle supports only `CBC`.

Optional:

* `customer_fragment_id` - Relevant Customer Fragment ID for  [Zero-Knowledge Encryption](doc:zero-knowledge).

* `split_level` - Defines the requested split level. By default, split level set with `2`.

* `[syslog]` Section can be added, to set the destination Syslog server settings:
  * `network` - Either **TCP** or **UDP**
  * `url` - Syslog server URL. 

Set the relevant permission on the `pkcs11.conf` file for your `oracle` user & group : 

```shell
chown -R oracle:dba /var/akeyless/conf/pkcs11.conf
```

Edit the `sqlnet.ora` file under `$ORACLE_HOME/network/admin/sqlnet.ora` where `$ORACLE_HOME` is your `oracle` user home directory. 

For docker setup, the file location is `/u01/app/oracle/product/12.2.0/dbhome_1/admin/ORCLCDB/sqlnet.ora`

Add the following line to set your `Oracle` wallet:

```shell
ENCRYPTION_WALLET_LOCATION=(SOURCE=(METHOD=HSM))
```

> 👍 Note
>
> Starting from Oracle version 18C/19C, before running the commands below, you need to first complete the steps below to set the keystore

1. Create a directory, called `wallet`, in the `$ORACLE_BASE/admin/db_unique_name` directory.
2. Log in to the database as a user with the `SYSDBA` administrative privilege.
3. Set the `WALLET_ROOT` parameter.

```shell
alter system set wallet_root='<path to the oracle wallet directory>' scope=spfile;
```

4. Shut down and start up the database. 

```shell
shutdown immediate;
startup;
```

5. Set the `TDE_CONFIGURATION` parameter as follows:

```shell
alter system set TDE_CONFIGURATION="KEYSTORE_CONFIGURATION=HSM" SCOPE=both ;
```

## Encrypting Tablespaces

Login to your `Oracle` DB, and run the following commands to create a wallet and a master encryption key:

```sql Oracle
administer key management set keystore open identified by "akeyless";
administer key management set key identified by "akeyless";
```

Run the following commands to create an encrypted tablespace:

```sql Oracle
CREATE TABLESPACE encrypt_ts
  DATAFILE '$ORACLE_HOME/dbs/encrypt_df.dbf' SIZE 1M
  ENCRYPTION USING 'AES128'
  DEFAULT STORAGE (ENCRYPT);
```

Run the following commands to create an encrypted table:

```sql Oracle
CREATE TABLE my_table (
    person_id NUMBER GENERATED BY DEFAULT AS IDENTITY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    PRIMARY KEY(person_id)
)  TABLESPACE encrypt_ts;
```

<br />

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

## Testing Data Encrypt

Once TDE is configured on the Oracle Database, you can start encrypting your data. There are two main options for encryption:

1. Encrypting Individual Columns: You can choose to encrypt specific columns within a table to secure sensitive information selectively.
2. Encrypting Entire Tablespaces: This involves encrypting the entire tablespace, which Oracle suggests as the preferred method due to its enhanced performance.

## Testing Encrypting Individual Column

**Connect to SQL\_Plus as a Non-Sysadmin User**

To begin, connect to the Oracle database using SQL\_Plus as a non-sysadmin user. This user should have the necessary privileges to create tables and manage encryption.

```sql bash
sqlplus your_username@your_database
```

Replace your\_username with your actual username and your\_database with the database service name.

**Enable Encryption on a Table**

Once connected, you can enable encryption on a table by creating a table with an encrypted column. The encryption is specified using the ENCRYPT clause in the CREATE TABLE statement.

```sql sql
CREATE TABLE employee (
    first_name VARCHAR2(128),
    last_name VARCHAR2(128),
    empID NUMBER,
    salary NUMBER(6) ENCRYPT
);

```

In this example:

The first\_name, last\_name, and empID columns are created as normal.\
The salary column is encrypted using Oracle's Transparent Data Encryption (TDE) by adding the ENCRYPT clause.

**Insert Data into the Encrypted Table**

After creating the table with the encrypted column, you can insert data into it. The data in the encrypted column will be automatically encrypted by Oracle TDE.

```sql sql
INSERT INTO employee VALUES ('JOHN', 'SMITH', 001, 10000);
```

This command inserts a record into the employee table, where the salary value of 10000 will be stored in an encrypted format.

**List Encrypted Columns in the Database**

To verify which columns in your database are encrypted, you can query the DBA\_ENCRYPTED\_COLUMNS view. This view provides details about the encrypted columns, including the encryption algorithm used, whether salt is applied, and the integrity algorithm

```sql sql
SELECT * FROM dba_encrypted_columns;
```

The output will show details like this:

```sql diff
OWNER  TABLE_NAME COLUMN_NAME ENCRYPTION_ALG SALT INTEGRITY_ALG
------ ---------- ----------- -------------- ---- -------------
OE     EMPLOYEE   SALARY      AES 192 bits   YES  SHA-1
```

In this example:

The SALARY column in the EMPLOYEE table is encrypted using the AES 192 bits algorithm.\
SALT is applied, and the integrity algorithm used is SHA-1.For more details about encryption options, such as how to specify different encryption algorithms or disable the use of salt, you can refer to the [Oracle documentation on Transparent Data Encryption (TDE)](https://docs.oracle.com/database/121/TDPSG/GUID-61259237-5514-4531-AFB4-CF716F93F1E5.htm#TDPSG44324). This documentation provides comprehensive guidelines on using TDE to secure sensitive data at rest within your Oracle database.

## Testing Tablespace Encryption

**Connect to SQL\_Plus as a Regular User**

Start by connecting to your Oracle database using SQL\_Plus as a non-sysadmin user. This user should have the necessary privileges to create tablespaces.

```sql bash
sqlplus your_username@your_database
```

Replace your\_username with your actual username and your\_database with the appropriate database service name.

**Verify and Set the COMPATIBLE Initialization Parameter**

Before creating an encrypted tablespace, ensure that the COMPATIBLE parameter is set to 11.2.0.0 or higher. This is particularly important for older versions of the 11g database.

**Check the Current COMPATIBLE Setting:**

```sql sql
SHOW PARAMETER COMPATIBLE;
```

You should see output similar to:

```sql sql
NAME                        TYPE        VALUE
--------------------------- ----------- -----------
compatible                  string      11.2.0.0
noncdbcompatible            BOOLEAN     FALSE
```

If the COMPATIBLE value is below 11.2.0.0, proceed with the following steps.

**Update the COMPATIBLE Parameter (if needed):**

```sql sql
ALTER SYSTEM SET COMPATIBLE='11.2.0.0' SCOPE=SPFILE;
SHUTDOWN IMMEDIATE;
STARTUP;
```

**Create an Encrypted Tablespace**

With the COMPATIBLE parameter correctly set, you can now create a new encrypted tablespace. Use the CREATE TABLESPACE statement along with the ENCRYPT clause to specify the encryption algorithm.

```sql sql
CREATE TABLESPACE encrypted_ts
DATAFILE '<PATH_TO_DATAFILE>/encrypted_ts01.dbf' SIZE 128K
AUTOEXTEND ON NEXT 64K
ENCRYPTION USING 'AES256'
DEFAULT STORAGE(ENCRYPT);
```

Replace \<PATH\_TO\_DATAFILE> with the actual path where you want to store the data file.

The tablespace is encrypted using the AES256 encryption algorithm.

Grant Unlimited Quota on the Encrypted Tablespace:

```sql sql
ALTER USER test QUOTA UNLIMITED ON encrypted_ts;
```

**Create a Table in the Encrypted Tablespace**

Now that the encrypted tablespace is set up, create a table within it to verify the encryption.

```sql sql
CREATE TABLE ets_test (
    id NUMBER(10),
    data VARCHAR2(50)
)
TABLESPACE encrypted_ts;
```

This creates a table named ets\_test in the encrypted\_ts tablespace.

**Insert Data into the Encrypted Table**

After creating the table, insert data to see how it is stored in the encrypted tablespace.

```sql sql
INSERT INTO ets_test (id, data) VALUES (1, 'This is a secret!');
COMMIT;
```

**Verify Tablespace Encryption**

To confirm that the tablespace is indeed encrypted, query the DBA\_TABLESPACES or USER\_TABLESPACES views.

```sql sql
SELECT tablespace_name, encrypted FROM dba_tablespaces;
```

The output will indicate whether each tablespace is encrypted:

```sql sql
TABLESPACE_NAME             ENC
--------------------------- ---
SYSTEM                      NO
SYSAUX                      NO
ENCRYPTED_TS                YES
```

The ENCRYPTED\_TS tablespace should display YES under the ENC column, confirming that encryption is enabled.

For more information, please refer to the [Oracle Tablespace Encryption documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/asoag/introduction-to-transparent-data-encryption.html)

## Configuring Auto-Login for Oracle TDE

In "Section 4.0," the method described involves saving the Oracle Wallet password in a configuration file, which is then used to manually open the wallet. However, if you want to enhance security and avoid exposing the wallet password in a file, you can configure Oracle Transparent Data Encryption (TDE) to use an auto-login keystore. This configuration offers several advantages:

### Step-by-Step Configuration

**Create a Software-Based Keystore**

First, you need to create a software-based keystore that will securely store the Oracle Wallet credentials. This keystore will facilitate the auto-login feature.

**Create the Keystore Directory:**\
Choose a secure location on your database server to store the keystore files. For example:

```sql bash
mkdir -p /u01/app/oracle/admin/ORCL/wallet
```

**Create the Keystore:**

Use the following command to create the keystore. Replace /u01/app/oracle/admin/ORCL/wallet with your chosen directory path.

```sql bash
ADMINISTER KEY MANAGEMENT CREATE KEYSTORE '/u01/app/oracle/admin/ORCL/wallet' IDENTIFIED BY "YourWalletPassword";
r -p /u01/app/oracle/admin/ORCL/wallet
```

**Open the Keystore:**

Before proceeding, you need to open the newly created keystore:

```sql bash
ADMINISTER KEY MANAGEMENT SET KEYSTORE OPEN IDENTIFIED BY "YourWalletPassword";
```

**Convert the Keystore to Auto-Login**

To enable the auto-login feature, the keystore must be converted to an auto-login keystore. This process creates an auto-login file that Oracle will use to open the wallet automatically.

**Convert to Auto-Login:**\
Execute the following command to create the auto-login keystore:

```sql sql
ADMINISTER KEY MANAGEMENT CREATE AUTO_LOGIN KEYSTORE FROM KEYSTORE '/u01/app/oracle/admin/ORCL/wallet' IDENTIFIED BY "YourWalletPassword";
```

**Verify the Auto-Login Keystore:**

After conversion, you should verify that the auto-login keystore was created successfully. Check that the cwallet.sso file exists in the keystore directory:

```sql sql
ls -l /u01/app/oracle/admin/ORCL/wallet/
```

You should see both the ewallet.p12 (the original keystore) and cwallet.sso (the auto-login keystore) files in this directory.

**Configure Oracle TDE to Use the Auto-Login Keystore**

With the auto-login keystore in place, you now need to configure Oracle TDE to use it. This ensures that the wallet is automatically opened during database startup.

**Set the Keystore Location:**

Modify the sqlnet.ora file to specify the location of the keystore. Add or update the following entry:

```sql plaintext
ENCRYPTION_WALLET_LOCATION=
  (SOURCE=
    (METHOD=FILE)
    (METHOD_DATA=
      (DIRECTORY=/u01/app/oracle/admin/ORCL/wallet/)
    )
  )
```

**Close and Reopen the Keystore:**

Test the auto-login functionality by closing and reopening the keystore. The wallet should open automatically without requiring a password.

```sql sql
ADMINISTER KEY MANAGEMENT SET KEYSTORE CLOSE;
ADMINISTER KEY MANAGEMENT SET KEYSTORE OPEN IDENTIFIED BY "YourWalletPassword";
```

**Restart the Database to Confirm:**

Restart the Oracle database to confirm that the auto-login feature is working as expected. Upon restart, the wallet should open automatically, and all encrypted columns and tablespaces should remain accessible.

```sql bash
shutdown immediate;
startup;
```

**Testing and Verification**

After setting up the auto-login keystore, it is crucial to test and verify the configuration to ensure that everything works as expected.

**Verify Wallet Status:**\
Use the following query to check the wallet status:

```sql sql
SELECT * FROM V$ENCRYPTION_WALLET;
```

The output should indicate that the wallet is open and that auto-login is enabled.

To displays information on the status of the wallet and the wallet location for Transparent Data Encryption (TDE) please refer to [7.204 V$ENCRYPTION\_WALLET documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-ENCRYPTION_WALLET.html).  

**Test Encrypted Data Access:**

Ensure that you can access encrypted tablespaces and columns without manually opening the wallet.

```sql sql
SELECT * FROM encrypted_table;
```

For additional details on Oracle TDE and auto-login keystore, please refer to the[ Oracle TDE Auto-Login documentation](https://docs.oracle.com/database/121/ASOAG/managing-keystore-and-tde-master-encryption-key.htm#GUID-D7ACB0B7-CA85-4F72-B29E-2E283409546F) and [Database Advanced Security Administrator's Guide](https://docs.oracle.com/cd/E11882_01/network.112/e40393/asotrans.htm)

## TDE Key Rotation

[Oracle - Setting or Rotating the TDE Master Encryption Key in the Keystore](https://docs.oracle.com/en/database/oracle/oracle-database/12.2/asoag/managing-keystore-and-tde-master-encryption-key.html#GUID-FDA3856D-5B88-42FD-A666-BC965C92689C)  and [Frequently Asked Questions About Transparent Data Encryption](https://docs.oracle.com/en/database/oracle/oracle-database/23/asoag/faq-tde.html) provides instructions on how to perform key rotations, including the necessary SQL commands and best practices to ensure a smooth transition to a new key.

## Restoring RMAN Backup with New TDE Key

Guidance on managing the restoration process of an RMAN backup with a new TDE key is available in the Oracle documentation, [Performing General Restore and Recovery Operations.](https://docs.oracle.com/en/cloud/paas/db-backup-cloud/csdbb/performing-general-restore-and-recovery-operations.html)

## Troubleshooting TDE

For common issues such as wallet access problems, key mismatches, or encryption errors, please refer to relevant sections of the [Oracle Transparent Data Encryption Troubleshooting and Debugging](https://support.oracle.com/knowledge/Oracle%20Database%20Products/1228046_1.html#aref_section310) (To view full details, sign in with Oracle support account). This page provides insights into common pitfalls and how to resolve them, ensuring that TDE implementation remains secure and functional.
