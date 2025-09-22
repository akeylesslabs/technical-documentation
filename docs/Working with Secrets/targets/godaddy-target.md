---
title: GoDaddy Target
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
**GoDaddy** Target enables you to use GoDaddy as a Public CA with Akeyless [PKI Issuer](doc:ssh-and-pkitls-certificates). 

With Public CA, Akeyless cannot access the private key that signs the certificates. Hence, Akeyless will programmatically contact GoDaddy through the [Gateway](doc:api-gw) using IMAP user credentials to validate the certificate request. Akeyless will store and manage the issued certificates and notify you of upcoming expiration events. 

# Create a GoDaddy Target in the CLI

To create a GoDaddy target from the CLI, run the following command:

```shell
akeyless target create godaddy \
--name <Target Name> \
--api-key <API Key of the GoDaddyTarget account> \
--secret <Secret of the api credentials to the Godaddy account>
--imap-username <Username to access the IMAP service> \
--imap-password <Password to access the IMAP service> \
--imap-fqdn <FQDN of the IMAP service> \
--imap-port[=993] <Port of the IMAP service> \
--customer-id <Customer ID>
```

Where:

* `name`: A unique name for the target. The name can include a path to the virtual folder where you want to create a new target using the slash `/`separators. If the folder does not exist, it will be created with the target.

* `api-key`: The **GoDaddy API Key** .

* `secret`: The **GoDaddy API Key Secret** .

* `imap-username`: An email address of the user registered to the IMAP service

* `imap-password`: **IMAP APP-Password** - for example, on **Gmail**  Under **Settings-> Security** , click on **2-Step Verification**, and generate **APP-Password** (2-Step verification must be enabled)

* `imap-fqdn`: IMAP FQDN, for example: `imap.gmail.com`

* `imap-port[=993]`: Port of the IMAP service

* `--customer-id`: Customer ID (ShopperId) required for renewal of imported certificates

Once the GoDaddy Target is created, it can be used to generate a [public certificate](https://docs.akeyless.io/docs/public-ca).

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorbluegodaddyp) section

# Create a GoDaddy Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Certificate Automation (GoDaddy)**.

2. Define a **Name** of the target, and specify the Location as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.\
   For more information, [read here](doc:implement-zero-knowledge).

4. Define the remaining parameters as follows:

* **API Key:** **GoDaddy API Key**.

* **API Secret:** **GoDaddy API Key Secret**.

* **Customer ID:**  **GoDaddy Customer ID**, required for certificate renewals. 

* **IMAP Username:** An email address of the user registered to the IMAP service

* **IMAP Password:** **IMAP APP-Password**, for example, on **Gmail**  Under **Settings -> Security**, click on **2-Step Verification** and generate **APP-Password** (2-Step verification must be enabled)

* **IMAP FQDN:** A FQDN of an IMAP service, For example, `imap.gmail.com`

* **IMAP Port:** IMAP service port, default is `993`

* **Timeout (seconds):** Timeout in seconds waiting for certificate validation (min: 300, max: 3600, default is 300)

5. Click **Finish**.
