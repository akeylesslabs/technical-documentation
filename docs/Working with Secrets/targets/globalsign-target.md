---
title: GlobalSign Target
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: public-ca
      title: Public CA
---
**GlobalSign** Target enables you to use **GlobalSign** as a Public CA with Akeyless [PKI Issuer](doc:ssh-and-pkitls-certificates) .

With Public CA, Akeyless cannot access the private key that signs the certificates. Hence, Akeyless will programmatically contact GlobalSign through the [Gateway](doc:api-gw)  using the account details of the domain owner to validate the certificate request.

Akeyless will store and manage the issued certificates and notify you of upcoming expiration events.

# Create a GlobalSign Target in the CLI

To create a GlobalSign target from the CLI, run the following command:

```shell
akeyless target create globalsign \
--name <Target Name> \
--username <Username> \
--password <Password> \
--profile-id <Profile ID> \
--contact-first-name <Account owner first name> \
--contact-last-name <Account owner last name> \
--contact-phone <Account owner telephone> \
--contact-email <Account owner email> 
```

Where:

- `name`: A unique name for the target. The name can include a path to the virtual folder where you want to create a new target using the slash /separators. The folder will be created with the target if it does not exist.

- `username`: The username used to log in to the GlobalSign DCC account.

- `password`: the password used to log in to the GlobalSign DCC account.

- `profile-id`: The profile ID of the GlobalSign GCC account.

- `contact-first-name`: First name of the GlobalSign GCC account contact.

- `contact-last-name`: Last name of the GlobalSign GCC account contact.

- `contact-phone`: Telephone of the GlobalSign GCC account contact.

- `contact-email`: Email of the GlobalSign GCC account contact.

Once the GlobalSign Target is created, it can be used to generate a [Public certificate](https://docs.akeyless.io/docs/public-ca).

You can find the complete list of parameters for this command in the [CLI reference](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorblueglobalsignp) section.

# Create a GlobalSign Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Certificate Automation (GlobalSign)**.

2. Define the Name of the target, and specify the Location as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.  
   For more information, [read here](doc:implement-zero-knowledge).

4. Define the remaining parameters as follows:

- **Profile ID:** Profile ID of the GlobalSign GCC account

- **Username:** Username of the GlobalSign GCC account

- **Password:** Password of the GlobalSign GCC account

- **First Name:** First name of the GlobalSign GCC account contact

- **Last Name:** Last name of the GlobalSign GCC account contact

- **Phone:** Telephone of the GlobalSign GCC account contact

- **Email:** Email of the GlobalSign GCC account contact

- **Timeout (seconds):** Timeout in seconds waiting for certificate validation (min: 300, max: 3600, default is 300)

5. Click **Finish**.