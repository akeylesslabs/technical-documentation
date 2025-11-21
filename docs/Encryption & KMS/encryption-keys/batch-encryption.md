---
title: Batch Encryption
excerpt: Batch Processing Support for Large Datasets in Encryption/Decryption Service
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
This documentation outlines the requirements and process for enhancing the Encryption/Decryption service to support batch processing for large datasets, specifically focusing on handling large volumes of credit card numbers in payment transactions.

The primary objective is to efficiently decrypt a substantial number of credit card numbers (approximately 400,000) within a constrained time frame (5-10 minutes) as part of payment processing transactions. The process involves decrypting batches of credit card numbers ranging from 1,000 to 10,000 and then sending the decrypted data to Visa (or a similar entity).

### Key Points

**Volume and Timing Requirements**

* Volume: Approximately 400,000 credit card numbers per batch.
* Time Frame: Decryption should be completed within 5-10 minutes.

**Encryption/Decryption Process**

* Batch Size: Credit card numbers will be processed in batches ranging from 1,000 to 10,000.
* Algorithm: AES256 with CBC mode.
* Data Length: 16-digit credit card numbers.
* Key Management:
  * Up to 5 active keys are maintained per year.
  * Keys are stored for a duration of 5 years, potentially involving up to 25 different keys per batch.

**Key Specifications**

* Encryption Algorithm: AES256 CBC.
* Keys: AES256 keys are used for encryption/decryption.
* Batch Processing:
  * Up to 25 different keys per batch, depending on the key version and key\_id.

**Workflow**

* The encryption/decryption service will be provided via an API supporting:
  * ingle value encryption/decryption.
  * Batch processing for encryption/decryption.
* The initial phase will focus on batch processing using a classic key (AES256) through a gateway, without involving asymmetric keys.

### Command References

**Batch Encryption Command**

The following command is used to encrypt a batch of plaintext using AES classic keys:

```shell
akeyless encrypt-batch -h
```

**Options:**

* \--batch-data: Batch data in JSON array format.
* \--batch-data-file-path: Path to the file containing batch data.
* \--profile, --token: Use a specific profile (located at $HOME/.akeyless/profiles) or a temporary access token.
* \--uid-token: The universal identity token (required only for universal\_identity authentication).
* \-h, --help: Display help information.
* \--json\[=false]\: Set output format to JSON.
* \--jq-expression: JQ expression to filter result output.
* \--no-creds-cleanup\[=false]\: Do not clean up local temporary expired credentials.

**Batch Decryption Command**

The following command is used to decrypt a batch of ciphertext using AES classic keys:

```shell
akeyless decrypt-batch -h
```

<br />

**Options:**

* \--batch-data: Batch data in JSON array format.
* \--batch-data-file-path: Path to the file containing batch data.
* \--profile, --token: Use a specific profile (located at $HOME/.akeyless/profiles) or a temporary access token.
* \--uid-token: The universal identity token (required only for universal\_identity authentication).
* \-h, --help: Display help information.
* \--json\[=false]\: Set output format to JSON.
* \--jq-expression: JQ expression to filter result output.
* \--no-creds-cleanup\[=false]\: Do not clean up local temporary expired credentials.
