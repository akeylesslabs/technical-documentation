---
title: TDE
excerpt: Transparent Data Encryption (TDE)
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Transparent Data Encryption (TDE) is a security feature that provides encryption of sensitive data stored in database tables and tablespaces. This ensures that the data at rest, i.e., the data stored on disk, is protected from unauthorized access. The primary purpose of TDE is to prevent data breaches resulting from stolen or improperly accessed storage media.

### How TDE Works

TDE operates by encrypting sensitive data within data files. This encryption process converts the data into an unreadable format using encryption keys. These keys are crucial for both encrypting and decrypting the data, ensuring that only authorized users and applications can access the plaintext information.

To enhance security and manageability, TDE integrates with the Akeyless Platform for key management. Akeyless offers robust key management capabilities, allowing encryption keys to be securely created, stored, and managed within the platform. By leveraging Akeyless, organizations can ensure that their encryption keys are protected from unauthorized access and misuse.

### Key Management and Decryption

Once data is encrypted using TDE, it remains encrypted on disk. However, when authorized users or applications access this data, TDE transparently decrypts it in real-time. This seamless decryption process ensures that users do not experience any difference in data access while maintaining strong security for the data at rest.

The key management capabilities of the Akeyless Platform include:

- Key Creation: Generating encryption keys with secure algorithms and appropriate key lengths.
- Key Storage: Storing encryption keys in a secure, tamper-proof environment.
- Key Rotation: Regularly updating encryption keys to mitigate the risk of key compromise.
- Access Control: Defining and enforcing policies to ensure that only authorized personnel can access and manage encryption keys.

<br />

### Benefits of Using TDE

Implementing TDE offers several benefits for organizations looking to secure their sensitive data:

- Data Protection: Encrypts sensitive data to protect it from unauthorized access and breaches.
- Compliance: Helps organizations meet regulatory requirements for data security and privacy.
- Transparency: Provides seamless encryption and decryption, ensuring that authorized users experience no disruption in data access.
- Centralized Key Management: Utilizes the Akeyless Platform to securely manage encryption keys, reducing the risk of key management errors and security vulnerabilities.

<br />

### [TDE for Oracle Database](https://docs.akeyless.io/docs/transparent-data-encryption-tde-for-oracle)

To set up TDE for Oracle Database, Akeyless provides a PKCS#11 shared library file. PKCS#11 is a standard that defines a platform-independent API for accessing cryptographic tokens such as hardware security modules (HSMs) and smart cards. By using the Akeyless PKCS#11 shared library, organizations can integrate their Oracle Database with the Akeyless Platform for secure key management and encryption operations.

### [TDE for SQL Server](https://docs.akeyless.io/docs/tde-for-mssql)

TDE is also available for Microsoft SQL Server, providing a robust solution for encrypting data at rest. SQL Server TDE encrypts the entire database, including the log files, using a database encryption key (DEK). This DEK is stored in the database boot record for availability during recovery.