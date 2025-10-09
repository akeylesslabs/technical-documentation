---
title: CLI Reference - Certificates
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
This section outlines the CLI commands relevant to SSH and PKI certificates.

<CLIGeneralFlags />

## SSH certificates

### `create-ssh-cert-issuer`

Creates a new SSH certificate issuer

##### Usage

```shell
akeyless create-ssh-cert-issuer \
--name <SSH certificate issuer name> \
--signer-key-name <A key to sign the certificate with> \
--allowed-users <Users allowed to fetch the certificate> \
--ttl <Time To Live for the certificate>
```

##### Flags

`-n, --name`: **Required**, SSH certificate issuer name

`-s, --signer-key-name`: **Required**, A key to sign the certificate with

`-a, --allowed-users`: **Required**, List of allowed users that will be able to use the certificate, e.g ubuntu

`-t, --ttl`: **Required**, The requested Time To Live for the certificate, in seconds

`-p, --principals`: Signed certificates with principal, e.g example_role1,example_role2

`-x, --extensions `: Signed certificates with extensions, e.g permit-port-forwarding="true"

`--host-provider[=explicit]`: Host provider type [explicit/target]

`-m, --metadata`: A metadata about the issuer

`--secure-access-enable`: Enable/Disable secure remote access, [true/false]

`--secure-access-bastion-api`: Bastion's SSH control API endpoint. e.g. `https://my.bastion:9900`

`--secure-access-bastion-ssh`: Bastion's SSH server. e.g. `my.bastion:22`

`--secure-access-ssh-creds-user`: SSH username to connect to target server, must be in 'Allowed Users' list

`--secure-access-host`: Target servers for connections., For multiple values repeat this flag.

`--secure-access-use-internal-bastion`: Use internal SSH Bastion - Relevant only for Secure Remote Access Deployment, mostly when using Dockers. Set the relevant IP address of the SSH Bastion for internal communication between ZT and SSH bastions.

`--delete-protection`: Protection from accidental deletion of this item, [true/false]

### `get-ssh-certificate`

Generate SSH certificate using Akeyless certificate issuer

##### Usage

```shell
akeyless get-ssh-certificate \
--cert-username <Username to sign> \
--cert-issuer-name <The name of the SSH certificate issuer> \
--public-key-file-path <path/to/SSH public key> \
--public-key-data <key file contents>
```

##### Flags

`-s, --cert-username `: **Required**, The username to sign in the SSH certificate (use a comma-separated list for more than one username)

`-c, --cert-issuer-name`: **Required**, The name of the SSH certificate issuer

`-p, --public-key-file-path`: SSH public key

`-o, --outfile`: Output file path with the certificate. If not provided, and public-key-file-path used, the file with the certificate will be created in the same location of the provided public key with the -cert extension

`--public-key-data`: SSH public key file contents. If this option is used, the certificate will be printed to stdout

`-t, --ttl`: Updated certificate lifetime in seconds (must be less than the Certificate Issuer default TTL)

`--legacy-signing-alg-name[=false]`: Set this option to use the legacy signing algorithm `ssh-rsa-cert-v01@openssh.com`.

### `update-ssh-cert-issuer`

Updates an existing SSH certificate issuer

##### Usage

```shell
akeyless update-ssh-cert-issuer \
--name <SSH cert issuer name> \
--signer-key-name <A key to sign the certificate with> \
--allowed-users <Users allowed to fetch the certificate> \
--ttl <Time To Live for the certificate>
```

#### Flags

`-n, --name`: **Required**, SSH certificate issuer name

`--new-name`: New item name

`-s, --signer-key-name`: **Required**, A key to sign the certificate with

`-a, --allowed-users`: **Required**, List of allowed users that will be able to use the certificate, e.g ubuntu

`-t, --ttl`: **Required**, The requested Time To Live for the certificate, in seconds.

`-p, --principals`: Signed certificates with principal, e.g example_role1,example_role2

`-x, --extensions`: Signed certificates with extensions, e.g permit-port-forwarding="true"

`--host-provider[=explicit]`: Host provider type [explicit/target]

`-m, --metadata`: A metadata about the issuer

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use argument multiple times: --add-tag Tag1 --add-tag Tag2

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use argument multiple times: --rm-tag Tag1 --rm-tag Tag2

`--secure-access-enable`: Enable/Disable secure remote access, [true/false]

`--secure-access-bastion-api`: Bastion's SSH control API endpoint. e.g. `https://my.bastion:9900`

`--secure-access-bastion-ssh`: Bastion's SSH server. e.g. `my.bastion:22`

`--secure-access-ssh-creds-user`: SSH username to connect to target server, must be in 'Allowed Users' list

`--secure-access-host`: Target servers for connections., For multiple values repeat this flag

`--secure-access-use-internal-bastion`: Use internal SSH Bastion

## PKI certificates

### `create-pki-cert-issuer`

Creates a new PKI certificate issuer

##### Usage

```shell
akeyless create-pki-cert-issuer \
--name <PKI issuer name> \
--ttl <The maximum requested Time To Live for issued certificates, in seconds> \
--signer-key-name <A singer key to sign and issue certificate> 
```

##### Flags

`-n, --name`: **Required**, PKI certificate issuer name

`--ca-target`: The name of an existing CA target (e.g. GlobalSign,GoDaddy,ZeroSSL) to attach this PKI Certificate Issuer, Relevant only when using Public CA.

`-s, --signer-key-name`: A key to sign the issued certificates.

`--gw-cluster-url`: The GW cluster URL, Relevant for Public CA and CRL.

`-t, --ttl`: **Required**, The maximum requested Time To Live for the issued certificate by `default` in seconds, supported formats are `s`,`m`,`h`,`d`.

`--allowed-domains`: A list of domains (comma seperated) this Issuer is allowed to issue certificates for.

`--allowed-uri-sans`: A list of the allowed URIs Subject Alternative Names (comma seperated) this Issuer is allowed to issue certificate for.

`--allow-subdomains [=false]`: If set, clients can request certificates for subdomains and wildcard subdomains of the allowed domains

`--not-enforce-hostnames [=false]`: If set, any names are allowed for CN and SANs in the certificate and not only a valid host name

`--allow-any-name [=false]`: If set, clients can request certificates for any CN

`--allowed-ip-sans`: A list of the allowed CIDRs for ips that clients can request to be included in the certificate as part of the IP Subject Alternative Names (in a comma-delimited list)

`--not-require-cn [=false]`: If set, clients can request certificates without a CN.

`--server-flag [=false] `: Extended Key Usage field If set, certificates will be flagged for server auth.

`--client-flag [=false] `: Extended Key Usage field If set, certificates will be flagged for client auth use.

`--code-signing-flag [=false] `: Extended Key Usage field If set, certificates will be flagged for code signing use.

`--key-usage[=DigitalSignature,KeyAgreement,KeyEncipherment]`: A list of Key Usage flags

`--critical-key-usage[=true]`: Mark key usage as critical [`true`/`false`]

`--organization-units `: A comma-separated list of organizational units (OU) that will be set in the issued certificate.

`--organizations `: A comma-separated list of organizations (O) that will be set in the issued certificate.

`--country `: A comma-separated list of the country that will be set in the issued certificate.

`--locality`: A comma-separated list of the locality that will be set in the issued certificate.

`--province`: A comma-separated list of the province that will be set in the issued certificate.

`--street-address`: A comma-separated list of the street address that will be set in the issued certificate.

`--postal-code`: A comma-separated list of the postal code that will be set in the issued certificate.

`--destination-path`: A path in Akeyless to store the generated certificates for future provisioning, renwals and expirtaion events.

`--protect-certificates`: Whether to protect generated certificates from deletion

`--is-ca [=false]`: If set, the basic constraints extension will be added to the issued certificate

`--max-path-len[=-1]`:  The maximum path length for the generated certificate. `-1`, means unlimited

`--enable-acme`: If set, the cert issuer will support the ACME protocol

`-e, --expiration-event-in`: How many days before the expiration of the certificate would you like to be notified, To specify multiple events, use the argument multiple times: --expiration-event-in 1 --expiration-event-in 5

`--allowed-extra-extensions`: A `JSON `string that defines the allowed extra extensions for the PKI cert issuer, e.g. `'{"<OID>":["<Vlaue>"]}'`

`--allowed-extra-extensions-file-path`: A path to a file containing a JSON string that defines the allowed extra extensions for the PKI cert issuer

`--allow-copy-ext-from-csr`: If set, will allow copying the extra extensions from the CSR file (if given)

`--create-public-crl`: Set this to allow the cert issuer will expose a public CRL endpoint

`--create-private-crl`: Set this to allow the issuer will expose a CRL endpoint in the Gateway

`--auto-renew`: Automatically renew certificates before expiration

`--scheduled-renew`: Number of days before expiration to renew certificates

`--disable-wildcards[=false]`: If set, generation of wildcard certificates will be disabled

`--description`: Description of the object

`--delete-protection`: Protection from accidental deletion of this item, [true/false]

`--tag`: List of the tags attached to this key. To specify multiple tags use argument multiple times: --tag Tag1 --tag Tag2

### `generate-csr`

Generates a new Certificate Signing Request (CSR)

##### Usage

```shell
akeyless generate-csr \
--name <Key Name> \
--common-name <Common Name> 
```

##### Flags

`-n, --name`: **Required**, Full path to the Key that will sign the CSR

`-g, --generate-key`: Use this flag to generate a new classic key to sign the CSR - **A name must be specified for the new key**

`-k, --key-type[=classic-key]`: The type of the key to generate (classic-key/dfc)

`--export-private-key[=false]`: If set the private key will be provided with the CSR.

`-a, --alg`: Algorithm to use for generating the new key (`RSA1024`, `RSA2048`, `RSA3072`, `RSA4096`, `EC256`, `EC384`)

`--hash-algorithm[=SHA256]`:  Specifies the hash algorithm used for the encryption key's operations, available options: [`SHA256`, `SHA384`, `SHA512`] (only for **RSA** and **EC** keys)

`-c, --common-name`: **Required**, common name to be included in the CSR certificate

`--certificate-type`: certificate type to be included in the CSR certificate (ssl-client/ssl-server/certificate-signing)

`--critical`: add critical to the key usage extension (will be false if not added)

`--org`: organization to be included in the CSR

`--dep`: department to be included in the CSR

`--city`: city to be included in the CSR

`--state`: state to be included in the CSR

`--country`: country to be included in the CSR

`--alt-names`: a comma-separated list of dns alternative names

`--email-addresses`: a comma-separated list of email addresses alternative names

`--ip-addresses`: a comma-separated list of ip addresses alternative names

`--uri-sans`: a comma-separated list of URI alternative names

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL `http://Your-Akeyless-Gateway-URL:8000`

`--description`: Description of the object

### `get-kube-exec-creds`

Gets credentials for authentication with Kubernetes cluster based on a PKI Cert Issuer

##### Usage

```shell
akeyless get-kube-exec-creds \
--cert-issuer-name <PKI cert issuer name> \
--key-file-path <The client public or private key file path> \
--alt-names <The Subject Alternative Names to be included in the PKI certificate> \ 
--ttl <Updated certificate lifetime in seconds>
```

##### Flags

`-c, --cert-issuer-name `: **Required**, The name of the PKI certificate issuer.

`-k, --key-file-path`: The client public or private key file path (in case of a private key, it will be use to extract the public key)

`--key-data-base64`: PKI key file contents encoded using Base64. If this option is used, the certificate will be printed to stdout

`--csr-file-path`: Path to Certificate Signing Request file to generate the certificate with

`--csr-data-base64`: Certificate Signing Request contents encoded in Base64 to generate the certificate with (if `--csr-file-path` is provided this flag is ignored)

`--common-name`: The common name to be included in the PKI certificate.

`--alt-names`: The Subject Alternative Names to be included in the PKI certificate (in a comma-delimited list).

`--uri-sans`: The URI Subject Alternative Names to be included in the PKI certificate (in a comma-delimited list).

`-t, --ttl`: Updated certificate lifetime in seconds (must be less than the Certificate Issuer default TTL)

`-e, --extended-key-usage`: A comma-separated list of extended key usage requests which will be used for certificate issuance. Supported values: `clientauth`, `serverauth`.

`-o, --outfile`: Output file path with the certificate. If not provided, the file with the certificate will be created in the same location of the provided public key with the -cert extension

`-a, --api-version[=v1]`: The version of the client authentication API

### `get-pki-certificate`

Generates PKI certificate from a PKI Issuer

##### Usage

```shell
akeyless get-pki-certificate \
--cert-issuer-name <PKI issuer name> \
--key-file-path <client Key> \
--ttl <certificate lifetime> 
```

##### Flags

`-c, --cert-issuer-name`: **Required**, The name of the PKI certificate issuer.

`-k, --key-file-path`: The client public or private key file path (in case of a private key, it will be use to extract the public key). When using **CSR** with a **private** key, the provided key will be stored with the issued certificate.

`--key-data-base64`: PKI key file contents encoded using Base64. If this option is used, the certificate will be printed to stdout

`--csr-file-path`: Path to Certificate Signing Request file to generate the certificate with

`--csr-data-base64`: Certificate Signing Request contents encoded in Base64 to generate the certificate with (if `--csr-file-path` is provided this flag is ignored)

`--common-name`: The common name to be included in the PKI certificate

`--alt-names`: The Subject Alternative Names to be included in the PKI certificate (in a comma-delimited list)

`--uri-sans`: The URI Subject Alternative Names to be included in the PKI certificate (in a comma-delimited list)

`-t, --ttl`: Updated certificate lifetime (must be less than the Certificate Issuer default TTL). `Default` in seconds, supported formats are `s`,`m`,`h`,`d`

`-e, --extended-key-usage`: A comma-separated list of extended key usage requests that will be used for certificate issuance. Supported values: `clientauth`, `serverauth`, If critical is present the extension will be marked as critical

`--extra-extensions`: A JSON string that defines the requested extra extensions for the certificate

`--extra-extensions-file-path`: A path to a file containing a JSON string that defines the requested extra extensions for the certificate

`-o, --outfile`: Output file path with the certificate. If not provided, the file with the certificate will be created in the same location as the provided public key with the -cert extension

### `get-cert-challenge`

Get a challenge for certificate authentication

##### Usage

```shell
akeyless get-cert-challenge \
--access-id <AccessID> \
--cert-data <'Certificate data encoded in Base64'>
```

### `renew-certificate`

Renew a PKI certificate

##### Usage

```shell
akeyless renew-certificate \
--name <Certificate name> \
--item-id <Certificate Item-ID>
```

##### Flags

`-n, --name`: Certificate name

`-i, --item-id`: Certificate item ID

`--generate-key`: Generate a new key as part of the certificate renewal

`-c, --cert-issuer-name`: Optional,the name of the PKI certificate issuer, relevant only for **imported** Certificates.

### `update-pki-cert-issuer`

Updates a new PKI certificate issuer

##### Usage

```shell
akeyless update-pki-cert-issuer \
--name <PKI issuer name> \
--ttl <The maximum requested Time To Live for issued certificates, in seconds> \ 
--new-name <New item name> \
--signer-key-name <A key to sign the certificate with> 
```

#### Flags

`-n, --name`: **Required**, PKI certificate issuer name

`--new-name`: New item name

`-s, --signer-key-name`: A key to sign the certificate with

`-t, --ttl`: **Required**, The maximum requested Time To Live for issued certificate by `default` in seconds, supported formats are `s`,`m`,`h`,`d`.  In case of Public CA, this is based on the CA target's supported maximum TTLs

`--gw-cluster-url`: The GW cluster URL to issue the certificate from, required in Public CA mode

`--allowed-uri-sans`: A list of the allowed URIs that clients can request to be included in the certificate as part of the URI Subject Alternative Names (in a comma-delimited list)

`--allow-subdomains`: If set, clients can request certificates for subdomains and wildcard subdomains of the allowed domains

`--not-enforce-hostnames`: If set, any names are allowed for CN and SANs in the certificate and not only a valid host name

`--allow-any-name`: If set, clients can request certificates for any CN

`--not-require-cn`: If set, clients can request certificates without a CN

`--server-flag`: If set, certificates will be flagged for server auth use

`--client-flag`: If set, certificates will be flagged for client auth use

`--code-signing-flag`: If set, certificates will be flagged for code signing use

`--key-usage[=DigitalSignature, KeyAgreement, KeyEncipherment]`: A comma-separated string or list of key usages

`--critical-key-usage[=true]`: Mark key usage as critical [`true`/`false`]

`--organization-units`: A comma-separated list of organizational units (OU) that will be set in the issued certificate

`--organizations`: A comma-separated list of organizations (O) that will be set in the issued certificate

`--country`: A comma-separated list of the country that will be set in the issued certificate

`--locality`: A comma-separated list of the locality that will be set in the issued certificate

`--province`: A comma-separated list of the province that will be set in the issued certificate

`--street-address`: A comma-separated list of the street address that will be set in the issued certificate

`--postal-code`: A comma-separated list of the postal code that will be set in the issued certificate

`--destination-path`: A path in Akeyless which to save generated certificates

`--protect-certificates`: Whether to protect generated certificates from deletion

`--is-ca`: If set, the basic constraints extension will be added to the certificate

`--max-path-len[=-1]`:  The maximum path length for the generated certificate. `-1`, means unlimited

`--enable-acme`: If set, the cert issuer will support the ACME protocol

`--expiration-event-in`: How many days before the expiration of the certificate would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`

`--allowed-extra-extensions`: A JSON string that defines the allowed extra extensions for the PKI cert issuer

`--allowed-extra-extensions-file-path`: A path to a file containing a JSON string that defines the allowed extra extensions for the PKI cert issuer.

`--allow-copy-ext-from-csr`: If set, will allow copying the extra extensions from the CSR file (if given)

`--create-public-crl`: Set this to allow the cert issuer will expose a public CRL endpoint

`--create-private-crl`: Set this to allow the issuer will expose a CRL endpoint in the Gateway

`--auto-renew`: Automatically renew certificates before expiration

`--scheduled-renew`: Number of days before expiration to renew certificates

`--disable-wildcards[=false]`: If set, generation of wildcard certificates will be disabled

`--description`: Description of the object

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: --rm-tag Tag1 --rm-tag Tag2

## Certificate Storage

### `create-certificate`

Creates a new certificate

##### Usage

```shell
akeyless create-certificate \
--name <certificate-name> \
--certificate <path-to-certificate-PEM/CER/CRT/PFX/P12>
```

##### Flags

`-n, --name`: **Required**, Unique Certificate name (mandatory)

`-c, --certificate`: **Required**, Path to a file that contain the certificate. Supported formats are: pem,cer,crt,pfx,p12.

`--certificate-data`: Content of the certificate PEM/CER/CRT/PFX/P12 in a Base64 format. It is mandatory to add this  **OR** the `--certificate`

`--format[=pem]`: Certificate Format of the certificate and private key, possible values: `cer,crt,pem,pfx,p12`

`--passphrase`: Passphrase to decrypt pkcs12/pks certificate data

`-p, --private-key`: Path to the file with the certificate's private key. Certificate Format should be the same as provided for the certificate

`--key-data`: Content of the certificate's private key PEM in a Base64 format.  If this  is defined `--private-key` is disabled.

`-e, --expiration-event-in`: How many days before the expiration of the certificate would you like to be notified. To specify multiple events, use argument multiple times: --expiration-event-in 1 --expiration-event-in 5

`-k, --key`: The name of a key to use to encrypt the certificate's key' (if empty, the account default protectionKey key will be used)

`-m, --metadata`: Metadata about the certificate

`-t, --tag`: List of the tags attached to this certificate. To specify multiple tags use argument multiple times: --tag Tag1 -t Tag2

`--delete-protection`: Protection from accidental deletion of this item, [true/false]

### `get-certificate-value`

Gets the certificate's PEM, and the private key's PEM if it exists, in a JSON file

##### Usage

```shell
akeyless get-certificate-value --name <certificate-name>
```

##### Flags

`-n, --name`: **Required**, Certificate name

`-d, --display-id`: Certificate display ID

`--version`: Certificate version

`-c, --cert-issuer-name`: The parent PKI Certificate Issuer's name of the certificate, required when used with display-id and token

`--certificate-file-output`: File to write the certificates to

`--private-key-file-output`: File to write the private key to

### `provision-certificate`

Provision a certificate content to a target

##### Usage

```shell
akeyless provision-certificate \
--name <Certificate name> \
--item-id <Certificate Item-ID>
```

##### Flags

`-n, --name`: Certificate name

`-I, --item-id`: Certificate item ID

`-d, --display-id`: Certificate display ID

### `revoke-certificate`

Revokes a certificate and adds it to the issuer CRL

##### Usage

```shell
akeyless revoke-certificate \
--name <Certificate name> \
--item-id <item-id> 
```

##### Flags

`-n, --name`: Certificate name

`-i, --item-id`: The item ID of the certificate to revoke

`-s, --serial-number`: The serial number of the certificate to revoke, in `base10` or `hex` format

`--version`: Certificate version to revoke. Required if item-id or name are used

### `update-certificate-value`

Updates the data in an existing certificate

##### Usage

```shell
akeyless update-certificate-value \
--name <certificate-name> \
--certificate <path-to-certificate-PEM/CER/CRT/PFX/P12>
```

##### Flags

`-n, --name`: **Required**, Certificate name

`-c, --certificate`: Path to a file that contain the certificate. Supported formats are: `pem,cer,crt,pfx,p12`

`--certificate-data`: Content of the certificate PEM in a Base64 format. It is mandatory to add this  **OR** the `--certificate`

`--format[=pem]`: Certificate Format of the certificate and private key, possible values: `cer,crt,pem,pfx,p12`

`--passphrase`: Passphrase to decrypt pkcs12/pks certificate data

`-p, --private-key`: Path to the file with the certificate's private key. Certificate Format should be the same as provided for the certificate

`--key-data`: Content of the certificate's private key PEM in a Base64 format.  If this  is defined `--private-key` is disabled.

`-e, --expiration-event-in`: How many days before the expiration of the certificate would you like to be notified. To specify multiple events, use argument multiple times: --expiration-event-in 1 --expiration-event-in 5

`-k, --key`: The name of a key to use to encrypt the certificate's key' (if empty, the account default protectionKey key will be used)

`-m, --metadata`: Metadata about the certificate

`-t, --tag`: List of the tags attached to this certificate. To specify multiple tags use argument multiple times: --tag Tag1 -t Tag2

`--delete-protection`: Protection from accidental deletion of this item, [true/false]

## ACME

### `generate-acme-eab`

Generates an external account binding for a cert issuer

##### Usage

```shell
akeyless generate-acme-eab \
--cert-issuer-name <PKI issuer name> 
```

### `list-acme-accounts`

Lists ACME external accounts for a cert issuer

##### Usage

```shell
akeyless list-acme-accounts \
--cert-issuer-name <PKI issuer name>
```

### `deactivate-acme-account`

Deactivate an ACME external account

##### Usage

```shell
akeyless deactivate-acme-account \
--cert-issuer-name <PKI issuer name> \
--acme-account-id <Account ID>
```

## Chain of Trust

### `generate-ca`

Creates a new PKI CA and Intermediate issuers

##### Usage

```shell
akeyless generate-ca \ 
--pki-chain-name <PKI Issuer name> \
--allowed-domains <Allowed domain list> \
--ttl <Issued Certificates TTL> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

##### Flags

`-n, --pki-chain-name`: **Required**, PKI certificate issuer name.

`--allowed-domains`: **Required**, A list of the allowed domains clients can request to be included in the certificate (in a comma-delimited list).

`-t, --ttl`: **Required**, The maximum requested Time To Live for issued certificate by default in seconds, supported formats are `s`,`m`,`h`,`d`.

`--extended-key-usage[=serverauth,clientauth]`: A separate list of extended key usage for the intermediate (`serverauth` / `clientauth` / `codesigning`).

`--key-type[=dfc]`: The type of the key to generate (`dfc`/`classic-key`).

`-a, --alg[=RSA4096]`: The algorithm (`RSA`/`Elliptic-curve`) to use for generating the new key.

`--max-path-len[=1]`: The maximum number of intermediate certificates that can appear in a certification path.

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port).

`-k, --protection-key-name`: The name of a key used to encrypt the secret values (if empty, the account default protection key will be used).

`-s, --split-level[=3]`: The number of fragments that the item will be split into.

`--delete-protection`: Protection from accidental deletion of this object, [`true`/`false`].
