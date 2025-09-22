---
title: ZeroSSL Target
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
**ZeroSSL** Target enables you to use ZeroSSL as a Public CA with Akeyless [PKI Issuer](doc:ssh-and-pkitls-certificates). 

With Public CA, Akeyless cannot access the private key that signs the certificates. Hence, Akeyless will programmatically contact ZeroSSL through the [Gateway](doc:api-gw) using IMAP user credentials to validate the certificate request. Akeyless will store and manage the issued certificates and notify you of upcoming expiration events. 

# Create a ZeroSSL Target in the CLI

To create a ZeroSSL target from the CLI, run the following command:

```shell
akeyless target create zerossl \
--name <Target Name> \
--api-key <API Key of the ZeroSSLTarget account> \
--imap-username <Username to access the IMAP service> \
--imap-password <Password to access the IMAP service> \
--imap-fqdn <FQDN of the IMAP service> \
--imap-validation-email <Email address to send the validation email>
```

Where:

- `name`: A unique name for the target. The name can include a path to the virtual folder where you want to create a new target using the slash `/`separators. If the folder does not exist, it will be created with the target.

- `api-key`:** ZeroSSL API Key**, can be found under **your** ZeroSSL account in the **Developer** section

- `imap-username`: An email address of the user registered to the IMAP service. This is either the same as `imap-validation-email` or a forward email address of  `imap-validation-email` if the domain does not have native email forwarding feature.

- `imap-password`: **IMAP APP-Password** - for example, on **Gmail**  Under **Settings-> Security** , click on** 2-Step Verification**, and generate **APP-Password** (2-Step verification must be enabled)

- `imap-fqdn`: IMAP FQDN, for example: `imap.gmail.com`

- `imap-validation-email`:  The domain owner's email address that certificate validation mail will be sent, currently available email address - `admin@domain.com`

Once the ZeroSSL Target is created, it can be used to generate a [public certificate](https://docs.akeyless.io/docs/public-ca).

You can find the complete list of parameters for this command in the [CLI reference](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorbluezerosslp) section.

# Create a ZeroSSL Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Certificate Automation (ZeroSSL)**.

2. Define a **Name** of the target, and specify the Location as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.  
   For more information, [read here](doc:implement-zero-knowledge).

4. Define the remaining parameters as follows:

- **API Key:** ZeroSSL API Key, can be found under **your** ZeroSSL account in the **Developer** section

- **IMAP Username:** An email address of the user registered to the IMAP service

- **IMAP Password:** **IMAP APP-Password**, for example, on **Gmail**  Under **Settings -> Security**, click on** 2-Step Verification** and generate **APP-Password** (2-Step verification must be enabled)

- **IMAP FQDN:** A FQDN of an IMAP service, For example, `imap.gmail.com`

- **IMAP Port:** IMAP service port, default is `993`

- **IMAP Validation Email:** Email to use when asking ZeoSSL to send a validation email, if left empty it will use username. There is no need to manually approve based on Verify Domains as Akeyless takes care of this with configured IMAP user name and password.

- **Timeout (seconds):** Timeout in seconds waiting for certificate validation (min: 300, max: 3600, default is 300).  For ZeroSSL, it might take longer than 5 min to get a validation email. Set it to max as needed.

5. Click **Finish**.