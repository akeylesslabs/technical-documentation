---
title: GlobalSign Atlas Target
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
[GlobalSign Atlas](https://www.globalsign.com/en/resources/datasheets) is a high-availability, high-throughput Certificate Authority (CA) that's powering automation and simplifying how companies and organizations use digital certificates.

**GlobalSign Atlas** target enables you to use GlobalSign Atlas as a Public CA with [Akeyless PKI Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates).

With Public CA, Akeyless cannot access the private key that signs the certificates. Hence, Akeyless will programmatically contact GlobalSign Atlas through the Gateway using the account details of the domain owner to validate the certificate request.

Akeyless will store and manage the issued certificates and notify you of upcoming expiration events.

# Create a GlobalSign Atlas Target in the CLI

To create a GlobalSign Atlas target from the CLI, run the following command:

```shell shell
akeyless target create globalsign-atlas \
--name <Target name> \
--api-key <API Key> \
--api-secret <API Secret> \
--mtls-cert-file-path <path/to/mTLS-certificate> \
--mtls-key-file-path <path/to/mTLS Key>   
```

Where:

* `name`: A unique name for the target. The name can include a path to the virtual folder where you want to create a new target using the slash /separators. The folder will be created with the target if it does not exist.

* `api-key`: API Key of the GlobalSign Atlas account.

* `api-secret`: API Secret of the GlobalSign Atlas account.

* `mtls-cert-file-path`: Path to the Mutual TLS Certificate of the GlobalSign Atlas account, either `mtls-cert-file-path.pem` or `tls-cert-data-base64` must be supplied.

You can find the complete list of parameters for this command in the [CLI reference](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorblueglobalsign-atlasp) section.

# Create a GlobalSign Atlas Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Certificate Automation (GlobalSign Atlas)**.

2. Define the Name of the target, and specify the Location as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.\
   For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

4. Define the remaining parameters as follows:

* **API Secret:** API Secret of the GlobalSign Atlas account

* **API Key:** API Key of the GlobalSign Atlas account

* **mTLS Cert:** mutual TLS (mTLS) Certificate of the GlobalSign Atlas account

* **mTLS Key:** mutual TLS (mTLS) Key of the GlobalSign Atlas account

* **Timeout (seconds):** Timeout in seconds waiting for certificate validation (min: 300, max: 3600, default is 300)

5. Click **Finish**.
