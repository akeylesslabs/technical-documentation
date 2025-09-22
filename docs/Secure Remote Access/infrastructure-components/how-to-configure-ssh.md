---
title: SSH Certificates
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: ssh-remote-access
      title: SSH Access
---
# Introduction

Via a Single Sign-on (SSO), the Akeyless Platform connects an SSH client to the server, using your chosen [Authentication Methods](doc:access-and-authentication-methods), while using existing Access Groups and Policies in your environment.

<Image align="center" src="https://files.readme.io/d650059-SSH_Certificates.png" />

Instead of issuing public and private SSH key pair, Akeyless provides ephemeral SSH certificates to allow access over standard SSH protocol while eliminating the need for public SSH keys on the server side.

You can define several SSH Certificate Authorities (CAs). Each CA can sign your SSH public keys, with additional parameters like expiration date, principals, extensions, etc.

You can sign the certificate with your own private key or generate a new one in the Akeyless Platform.

# Prerequisites

## Creating a Key

In order to configure a CA, you will first need an RSA key to match. You can either use an existing key or create a new one. Once you are logged in to your Akeyless account on the desired server, proceed to one of the following:

In case you want to use an existing key, upload your CA (RSA private key) for signing the client SSH certificate, using the following command:

```shell your-RSA-key-name
akeyless upload-rsa --name your-RSA-key-name --alg RSA2048 --rsa-key-file-path Path-to-RSA.pem
```

Alternatively, you can create a new RSA key in the Akeyless Platform:

```shell your-RSA-key-name
akeyless create-dfc-key --name your-RSA-key-name --alg RSA2048
```

After you have the desired key on the server, display your key using the following command:

```shell your-RSA-key-name
akeyless get-rsa-public --name your-RSA-key-name
```

The output should look like this:

```shell your-RSA-key-name
- RAW: MIIBIjANBgkqhkiG9w0BAQEFAAOCOA89zd/GgaPmzisJ3PMqYy3cPvRJc7VWRu72wR9muOdHX3vP7bscR+fGgKuOn1XPXBPjsOmo
- SSH: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQMpAMLn3TyairCPzfIqG4wUJFTWCemKV5Z0blvxzUuZnkWUHRdSnowxXyANqQcZ
- PEM: -----BEGIN RSA PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8w0BAQEFAAOCAQAQdfIsN7oV4BZdlj9PT8
xi+XdAcQeElmSEgetlQ3INYfdUzOEwroj4RlscYhKPeF730gtlQ3INYfdUzOEwro
WgAaZ+XdAcQeElmSEgetlQ3INYfdUzOEwroj4RlscYhKPeF730gkVv502+LCLeC3
53jXHt2ZYUnUzJUt1Bhnm33Sa/YYUl5ZSxru1f10D2FCYi2njsQoMgxxoN9GYDdp
53jYUnUvYUnUnm33Sa/uY31iXrMKQcP6QJ2IauY31iXrMKQcP6QJ2IauY31iXrMK
l4BfQzeHV23YLvCLDRVB5YxXHogQ00IDGjYFPbp3KuYVqIZiDcTdmQ0HsHE28bQe
-----END RSA PUBLIC KEY-----
```

## Configuring the Server

To enable certificate authentication, you will need to configure the target server to trust any certificates signed by your CA's public key as follows:

1. Fetch the CA's public key from your Akeyless account via the following command:

```shell your-RSA-key-name
akeyless get-rsa-public --name "/path/to/your-RSA-key-name"
```

The output should contain three sections, one in a raw format, the second in an SSH format, and the third in a `PEM` key format, similar to the example in the previous section.

2. Copy the Public Key with the **SSH** format from step 1 (starting from `ssh-rsa…` and ending before `- PEM`) to a file in the desired folder on the SSH server (for example `/etc/ssh/ca.pub`), then to a new file **on the target server that will be accepting SSH connections**.

Example of retrieving the SSH value and putting it into the `/etc/ssh/ca.pub` file

```shell ssh > ca.pub file
akeyless get-rsa-public --name "/path/to/your-RSA-key-name" --json --jq-expression='.ssh' > /etc/ssh/ca.pub
```

```shell your-RSA-key-name
ssh-rsa AAAAB3NzaC1yc2EAAAA...
```

3. Add the following lines to `/etc/ssh/sshd_config` on the target server. Once done, the `sshd` service may need to be restarted.

```shell /etc/ssh/sshd_config
TrustedUserCAKeys /etc/ssh/ca.pub
```

4. If your server's SSH version is over 8.2, you will also have to add the following line to the same file. It can be either before or after the line from step 3, but in the same section at the end of the file.

```shell /etc/ssh/sshd_config
PubkeyAcceptedKeyTypes=+ssh-rsa,ssh-rsa-cert-v01@openssh.com
```

# Principals

An advanced feature available for server configuration in OpenSSH 6.2 and later is the use of the `AuthorizedPrincipalsFile`. This configuration option specifies a file that enumerates the valid principals (identities) permitted for certificate-based authentication.

In SSH terminology, a "principal" is a designated named entity, serving as an auxiliary form of identification, especially during certificate-based authentication processes. An SSH key certificate can be associated with one or multiple principals, akin to roles or usernames. The `AuthorizedPrincipalsFile` aims to determine which of these principals are granted login privileges.

The procedure is as follows:

1. During the authentication phase, an SSH client submits a certificate to the server.
2. The server assesses the certificate's legitimacy, examining factors such as its trusted authority signature and expiration status.
3. If deemed valid, the server juxtaposes the certificate's principals with the allowed principals delineated in the `AuthorizedPrincipalsFile`.
4. Authentication is successful if there's a match between one of the certificate's principals and an entry in the `AuthorizedPrincipalsFile`. Otherwise, the authentication is denied.

The structure of the `AuthorizedPrincipalsFile` is simple. Each line within the file stands for a valid principal, with the provision for comments (lines that commence with #).

For instance:

```bash /etc/ssh/principals
principal1
principal2
admin
```

```shell /etc/ssh/sshd_config
AuthorizedPrincipalsFile /etc/ssh/principals
```

# Generating a Certificate - CLI

## Creating the Certificate Authority

The following command will create a new SSH Cert Issuer in the Akeyless Platform with ancillary data.

* **`name`**: The name that will be assigned to the new Cert Issuer 
* **`signer-key-name`**: The private key to be used for certificate signing 
* **`allowed-users`**: Users allowed to use the certificate (supports wildcard)
* **`ttl`**: The time (in seconds) to the expiration of the certificate
* **`principals`**: A specific set of SSH Certificate principals (optional)
* **`extensions`**: A specific set of SSH Certificate extensions (this parameter is also optional, if not stated the default extensions are: permit-X11-forwarding, permit-agent-forwarding, permit-port-forwarding, permit-pty, permit-user-rc)

```shell CLI
akeyless create-ssh-cert-issuer --name /prod/ssh-cert-issuer --signer-key-name /your-RSA-key-name --allowed-users 'ubuntu,root' --ttl 300
```

> 👍 Akeyless Secure Remote Access
>
> While working with Secure Remote Access Bastion, make sure to set `allowed_users` with `session_*` to ensure JIT users will be authorized for access.
>
> You will also need to enable Secure Remote Access on the SSH Cert Issuer either in the UI or by adding the `--secure-access-enable true` flag to your CLI command.
>
> It is also possible to enforce host restrictions for SSH connections to only those listed in the SSH Cert Issuer when using [Akeyless Connect](doc:akeyless-connect) by adding the `--secure-access-enforce-hosts-restriction true` flag when creating the Cert Issuer.

## Issuing a Certificate

After setting up a key and a certificate issuer, the following command will generate a certificate signed by the CA.

* **`cert-username`**: The username with which you intend to connect to the server, note to match it to the **`allowed-users`** from the previous section.
* **`cert-issuer-name`**: The certificate issuer you configured using the previous section.
* **`public-key-file-path`**: The path to the file containing your SSH public key.

```shell CLI
akeyless get-ssh-certificate --cert-username ubuntu --cert-issuer-name /prod/ssh-cert-issuer --public-key-file-path ~/.ssh/id_rsa.pub
```

> 📘 Tip
>
> The command `get-ssh-certificate` returns a certificate that is signed by the private CA key and uses the client’s public key that will be used to connect to the target server. The client's public key is not the same as the CA’s public key. It is a local public key that should be located in the command’s path together with the client’s private key. After you run the command, the signed certificate will be placed in the same path, so you will be able to connect to the target server using the client’s private/public keys which are located on the same path.

The outcome of this command will be creating a new file beside the public key by adding a suffix to its name with `-cert.pub`, e.g. `~/.ssh/id_rsa-cert.pub`. This is a well-known convention that OpenSSH uses during authentication.

After generating a certificate, you should be able to connect to the server without a key, using a standard command:

```shell ssh
ssh user@server
```

# Generating a Certificate - Console

## Creating the Certificate Authority

This guide includes the steps needed for the necessary prerequisites. If you want to create the Certificate Issuer for an existing key, you may skip steps 1-3.

1. Log in to the Akeyless Console, and go to **Items > New > Encryption Key>DFC**.

2. Define a **Name** of the key, and specify the **Location** as a path to the virtual folder where you want to create the new key, using slash `/` separators. If the folder does not exist, it will be created together with the key.

3. Define the remaining parameters as follows:

* **Description:** general description of the key (optional).

* **Tags:** assign tags to the key (optional).

* **Delete Protection:** When enabled, protects the secret from accidental deletion.

* **Type:** The encryption algorithm used for the key.

* **Customer Fragment:** If you have an existing [customer fragment](https://docs.akeyless.io/docs/dfc), you may attach it to the key. If you wish to generate one, please refer to [these instructions](https://docs.akeyless.io/docs/cli-reference-encryption-keys#p-stylecolorbluegen-customer-fragmentp).

4. Go to the folder in Akeyless where you saved the desired key, select it, and tap **get public RSA key**.

5. Copy the SSH format string (the top box starting with `ssh-rsa…`, not the raw key) to a file on the desired folder on the SSH server, for example, `/etc/ssh/ca.pub`

6. Go to **Items > New > SSH Cert Issuer**

7. Define a **Name** of the cert issuer, and specify the **Location** as a path to the virtual folder where you want to create it, using slash `/` separators. If the folder does not exist, it will be created together with the cert issuer.

8. Define the remaining parameters as follows:

* **Description:** General description of the key (optional).

* **Tags:** Assign tags to the key (optional).

* **Delete Protection:** When enabled, protects the secret from accidental deletion.

* **Signer Key:** The name of the linked key you defined in advance and used in steps 4-5.

* **Certificate Lifetime in Seconds:** The time (in seconds) to the expiration of the certificate.

* **Allowed Users:** Specify the allowed users for the certificates issued.

* **Principals:** A specific set of SSH Certificate principals (optional)

You should now have a working certificate issuer.

## Issuing a Certificate

In order to issue an SSH certificate using an existing CI through the console, go through the following steps:

1. Go to the folder in which your certificate issuer is located and select it.

2. Under the key details you will see a button reading **Generate SSH Certificate**, tap it.

3. Fill in the following details:

* **Certificate Username:** The username that will be linked to the certificate. Make sure this username matches the allowed usernames you defined in the previous section.

* **Public Key:**  Your SSH public key, can be copied in or uploaded from file.

4. Tap generate, and if all parameters are valid, you will get a string representing your certificate. Download the certificate, or copy it to a file, in the client's `ssh` relevant folder.

5. After generating a certificate, you should be able to connect to the server without a key, just a standard `ssh user@server` command.

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/using-ssh-certificates-to-access-remote-machines" target="_blank" style="color: #00e">Using SSH Certificates to Access Remote Machines</a>.
