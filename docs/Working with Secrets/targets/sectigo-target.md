---
title: Sectigo Target
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
The **Sectigo Target** enables you to use **Sectigo** as a Public Certificate Authority (CA) with Akeyless [PKI Issuer](doc:ssh-and-pkitls-certificates).

With a public CA, Akeyless cannot access the private key that signs certificates. Akeyless will programmatically validate the certificate signing request by contacting Sectigo through the [Akeyless Gateway](doc:api-gw) using the domain owner's account details

Akeyless will store the issued certificates, manage them, and notify you of upcoming expiration events.

# Create a Sectigo Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Certificate Automation (Sectigo)**.

2. Define the Name of the target, and specify the Location as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
   For more information, [read here](doc:implement-zero-knowledge).

4. Define the remaining parameters as follows:

* **Customer URI:** The Customer URI of the Sectigo account.

* **Username:** Username used to log in to Sectigo.

* **Password:** Password of the Sectigo account

* **Organization ID:** Sectigo Orgnaiztion ID.

* **Certificate Profile ID:** Sectigo Certificate Profile ID.

* **External Requester:** Sectigo External Requester username.

* **Timeout (seconds):** Timeout in seconds waiting for certificate validation (min: 300, max: 3600, default is 300)

5. Click **Finish**.

# Create a Sectigo Target in the CLI

To create a Sectigo target from the CLI, run the following command:

```shell
akeyless target create globalsign \
--name <Target Name> \
--username <Username> \
--password <Password> \
--customer-uri <Sectigo Account CustomerUri> \
--organization-id <Sectigo Organization ID > \
--certificate-profile-id  <Sectigo Certificate Profile ID> 
--external-requester <username of the requester>
```

Where:

* `name`: A unique name for the target. The name can include a path to the virtual folder where you want to create a new target using the slash /separators. The folder will be created with the target if it does not exist.

* `username`: The username used to log in to Sectigo.

* `password`: the password used to log in to Sectigo.

* `customer-uri`: The Customer URI of the Sectigo account.

* `organization-id`: Sectigo Organization ID.

* `certificate-profile-id`: Sectigo Certificate Profile ID.

* `external-requester`: Sectigo external requester username.

Once the Sectigo Target is created, it can be used to generate a [public certificate](https://docs.akeyless.io/docs/public-ca).

For the complete list of parameters for this command, visit the [CLI Reference](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorblueglobalsignp).

<Callout icon="❗️">
  # Sectigo Approval Workflow

  Akeyless PKI Issuer does not support Sectigo approval workflows, make sure your Sectigo certificate profile does not require a second approval.
</Callout>
