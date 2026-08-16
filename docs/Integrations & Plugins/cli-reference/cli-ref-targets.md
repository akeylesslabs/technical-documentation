---
title: CLI Reference - Targets
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
This section outlines the CLI commands relevant to Targets.

<CLIGeneralFlags />

## `assoc-target-item`

Create an association between target and item

### Usage

```shell
akeyless assoc-target-item \
--target-name <The target to associate> \
--name <The item to associate> \
--vault-name <Name of the vault used> \
--key-operations <List of allowed operations for the key>
```

#### Flags

`-t, --target-name`: **Required**, The target to associate

`-n, --name`: **Required**, The item to associate

`--vault-name`: Name of the vault used. (Relevant only for Classic Key and target association. Required for Azure targets)

`--key-operations`: A list of allowed operations for the key. (Relevant only for Classic Key and target association. Required for Azure targets)

`--disable-previous-key-version[=false]`: Automatically disable previous key versions. (Required for classic key association with Azure targets)

`--project-id`: Project ID of the GCP KMS. (Relevant only for Classic Key and target association. Required for GCP targets)

`--location-id`: Location ID of the GCP KMS. (Relevant only for Classic Key and target association. Required for GCP targets)

`--keyring-name`: Keyring name of the GCP KMS. (Relevant only for Classic Key and target association. Required for GCP targets)

`--purpose`: Purpose if the key in GCP KMS. (Relevant only for Classic Key and target association. Required for GCP targets)

`--kms-algorithm`: Algorithm of the key in GCP KMS. (Relevant only for Classic Key and target association, Required for GCP targets)

`--tenant-secret-type`: The tenant secret type \[Data/SearchIndex/Analytics]. (Relevant only for Classic Key and target association. Required for Salesforce targets)

`--multi-region[=false]`: Set to 'true' to create a multi-region managed key. (Relevant only for Classic Key AWS targets)

`--regions`: The list of regions in which to create a copy of the key. (Relevant only for Classic Key AWS targets). To specify multiple regions use argument multiple times: --regions us-east-1 --regions us-west-1

`--private-key-path`: A path on the target to store the private key (relevant only for certificate provisioning)

`--certificate-path`: A path on the target to store the certificate pem file (relevant only for certificate provisioning)

`--chain-path`: A path on the target to store the full chain pem file (relevant only for certificate provisioning)

`--post-provision-command`: A custom command to run on the remote target after successful provisioning (relevant only for certificate provisioning)

`--gateway-url[=http://localhost:8000]`: Gateway URL for the certificate provisioning (relevant only for certificate provisioning)

`--sra-association[=false]`: Specify if the target to associate is for SRA, relevant only for SRA linked target association to `ldap` rotated secret

`--external-key-name`: The external key name to associate with the classic key (Relevant only for Classic Key AWS/Azure/GCP targets)

## `create`

Create a new Target

### Subcommands

`artifactory`

`aerospike`

`aws`

`azure`

`claude`

`cloudflare`

`custom-dns`

`db`

`digicert`

`dockerhub`

`eks`

`f5`&#x20;

`gcp`

`github`

`gitlab`

`google-trust`

`gke`

`globalsign`

`globalsign-atlas`

`godaddy`

`grok`

`hashi-vault`

`k8s`

`keycloak`

`ldap`

`lets-encrypt`

`linked`

`okta`

`openai`

`ping`

`rabbitmq`

`salesforce`

`sectigo`

`ssh`

`web`

`windows`

`zerossl`

### `artifactory`

Creates a new Artifactory target in the current account

#### Usage

```shell
akeyless target create artifactory \
--name <Target name> \
--base-url <Artifactory REST URL, must end with "artifactory" postfix> \
--artifactory-admin-name <Admin name> \
--artifactory-admin-pwd <Admin API Key/Password> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`-b, --base-url`: **Required**, Artifactory REST URL, must end with `artifactory` postfix

`-a, --artifactory-admin-name`: **Required**, Admin name

`-p, --artifactory-admin-pwd`: **Required**, Admin API Key/Password

`-k, --key`: The name of a key used to encrypt the target secret value (if empty, the account default protectionKey key will be used)

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `aerospike`

Creates a new aerospike target in the current account

#### Usage

```shell
akeyless target create artifactory \
--name <Target name> \
--aerospike-cloud <true|false> \
--hostname <Aerospike Hostname> \
--port <Database port> \
--namespace <Namespace Name> \
--admin-username <Admin Username> \
--password <Admin Usernames Password> \
--aerospike-cluster-id <Cloud cluster ID> \
--aerospike-client-id <Client ID> \
--aerospike-client-secret <Aerospike Client Secret> \
--ssl <Enable SSL Encryption> \
--ssl-certificate <Base64-encoded SSL CA certificate> \ f
--ssl-certificate-file-path <Path to a file containing the SSL CA certificate> \
--enable-mtls <Enable mutual TLS authentication> \
--client-certificate <Client certificate> \ 
--client-certificate-file-path <Path to a file containing the client certificate> 
--client-private-key <Client private key> \
--client-private-key-file-path <Path to a file containing the client private key> \
--db-server-name <TLS server name used to verify the certificate hostname> \
--skip-server-name-validation <Skip server name verification while still validating the certificate chain>
```

##### Flags

`-n, --name`: **Required**, Target name

`--aerospike-cloud`: Set to `true` for Aerospike Cloud deployments

`--hostname`: Aerospike host address and port (for example: `url.to.aerospike.db`)

`--port`: Database connection port

`--namespace`: Namespace name (relevant only for Aerospike databases)

`--admin-username`: **Required**, Username of an account with the `user-admin` role

`--password`: **Required**, Password for the admin user

`--aerospike-cluster-id`: Cloud cluster ID (relevant only for Aerospike Cloud)

`--aerospike-client-id`: Client ID for Aerospike Cloud authentication (relevant only for Aerospike Cloud)

`--aerospike-client-secret`: Client secret for Aerospike Cloud authentication (relevant only for Aerospike Cloud)

`--ssl`: Enable SSL encryption (`true`/`false`)

`--ssl-certificate`: Base64-encoded SSL CA certificate from a trusted Certificate Authority (CA)

`--ssl-certificate-file-path`: Path to a file containing the SSL CA certificate from a trusted Certificate Authority (CA)

`--enable-mtls`: Enable mutual TLS (mTLS) authentication. Requires `--ssl=true`

`--client-certificate`: Client certificate used for mTLS authentication

`--client-certificate-file-path`: Path to a file containing the client certificate used for mTLS authentication

`--client-private-key`: Client private key used for mTLS authentication

`--client-private-key-file-path`: Path to a file containing the client private key used for mTLS authentication

`--db-server-name`: TLS server name used to verify the certificate hostname. If not specified, the Aerospike hostname is used

`--skip-server-name-validation`: Skip server name verification while still validating the certificate chain (`true`/`false`). If empty, server name validation is performed normally.

### `aws`

Creates a new AWS target in the current account

#### Usage

```shell
akeyless target create aws \
--name <Target name> \
--access-key-id <AWS access key ID> \
--access-key <AWS secret access key> \
--region <AWS region>
```

##### Flags

`-n, --name`: **Required**, Target name

`--access-key-id`: **Required**, AWS access key ID

`--access-key`: **Required**, AWS secret access key

`--session-token`: Required only for temporary security credentials retrieved using STS

`--region [=us-east-2]`: AWS region

`-i, --use-gw-cloud-identity`: Use the GW's Cloud IAM

`--generate-external-id[=false]`: A unique auto-generated value used in your AWS account when configuring your AWS IAM role to securely delegate access to Akeyless. Relevant only when using **GW cloud ID**

`role-arn`: AWS IAM role identifier that Gateway will assume in your AWS account, relevant only when using **external ID**

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `azure`

Creates a new Azure target in the current account

#### Usage

```shell
akeyless target create azure \
--name <Target name> \
--client-id <Azure client/application id> \
--client-secret <Azure client secret> \
--tenant-id <Azure tenant id> \
--azure-cloud[=AzureCloud] <AzureCloud/AzureUSGovernment/AzureChinaCloud>
```

##### Flags

`-n, --name`: **Required**, Target name

`--client-id`: **Required**, Azure client/application ID

`--tenant-id`: Azure tenant ID

`--client-secret`: **Required**, Azure client secret

`--azure-cloud[=AzureCloud]`: Azure cloud environment to use. Values: `AzureCloud` (default), `AzureUSGovernment`, `AzureChinaCloud`

`-i, --use-gw-cloud-identity`: Use the GW's Cloud IAM

`--subscription-id`: Azure Subscription ID

`--resource-group-name`: The Resource Group name in your Azure Subscription

`--resource-name`: The name of the relevant Resource

`-k, --key`: Key name. The key is used to encrypt the target secret value. If the key name is not specified, the account default protection key is used

`--description`: Target description
`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `claude`&#x20;

Creates a new Azure target in the current account

#### Usage

```shell
akeyless target create claude \
--name <Target name> \
--api-key <Claude API Key> \
--claude-url[=https://api.anthropic.com] <Claude API base URL>
```

##### Flags

`-n, --name`: **Required**, Target name

`--api-key`: **Required**, Claude API Key

`--claude-url`: Claude API base URL

### `cloudflare`

Creates a new Claude target in the current account

#### Usage

```shell
akeyless target create cloudflare \
--name <Target name> \
--api-token <Cloudflare API token> \
--account-id <Cloudflare account ID>
```

##### Flags

`-n, --name`: **Required**, Target name

`--api-token`: **Required**, Cloudflare API token

`--account-id`: Optional. Cloudflare account ID

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `custom-dns`

Creates a new Custom-DNS target in the current account

#### Usage

```shell
akeyless target create custom-dns \
--name <Target name> \
--provider-type <DNS Provider> \
--dns-parameter <Key|Value>
```

##### Flags

`-n, --name`: **Required**, Target name

`provider-type`: The DNS provider type. All DNS providers available through the Lego project are supported.

`dns-parameter`: The parameters for the DNS provider.

### `db`

Creates a new DB target in the current account

#### Usage

```shell
akeyless target create db \
--name <Target name> \
--db-type <mysql/mssql/hanadb/postgres/mongodb/snowflake/oracle/cassandra/redshift/redis> \
--user-name <Database user name> \
--host <Database host> \
--pwd <Database password> \
--port <Database port> \
--db-name <Database name>
```

##### Flags

`-n, --name`: **Required**, Target name

`--db-type`: **Required**, Database type: `mysql/mssql/hanadb/postgres/mongodb/snowflake/oracle/cassandra/redshift/redis`

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If the key name is not specified, the account default protection key is used

`--user-name`: Database user name

`--host`: Database host

`--pwd`: Database password
`--port`: Database port

`--db-name`: Database name

`--snowflake-api-private-key`: RSA Private key (Base64-encoded)

`--snowflake-api-private-key-file-name`: The path to the file containing the private key

`--snowflake-api-private-key-passphrases`: The Private key passphrase

`--db-server-certificates`: Set of root certificate authorities in Base64 encoding used by clients to verify server certificates

`--db-server-name`: Server name is used to verify the hostname on the returned certificates unless InsecureSkipVerify is provided. It is also included in the client's handshake to support virtual hosting unless it is an IP address

`--azure-client-id`: Azure client ID (relevant for "cloud-service-provider" only)

`--azure-tenant-id`: Azure tenant ID (relevant for "cloud-service-provider" only)

`--azure-client-secret`: Azure client secret (relevant for "cloud-service-provider" only)

`--cloud-service-provider`: Cloud Service Provider (currently only supports Azure)

`--connection-type[=credentials]`: Type of connection to MSSQL database \[credentials/cloud-identity]

`--ssl[=false]`: Enable/Disable SSL \[true/false]

`--ssl-certificate`: SSL CA certificate in Base64 encoding generated from a trusted Certificate Authority (CA)

`--enable-mtls[=false]`: Enable/Disable mTLS \[true/false]. Relevant only when `--ssl=true`

`--client-certificate`: Client certificate in Base64 format. Relevant only when `--enable-mtls=true`

`--client-private-key`: Client private key in Base64 format. Relevant only when `--enable-mtls=true`

`--client-key-passphrase`: Optional private key passphrase. Relevant only when `--enable-mtls=true`

`--snowflake-account`: Snowflake account name

`--oracle-service-name`: Oracle DB service name

`--oracle-wallet-login-type`: Oracle Wallet login type (`password`/`mtls`)

`--oracle-wallet-path`: Path to Oracle wallet (where `cwallet.sso` and `ewallet.p12` reside)

`--oracle-wallet-sso-file-data`: Oracle wallet `sso` file data in Base64

`--oracle-wallet-p12-file-data`: Oracle wallet `p12` file data in Base64

`--mongodb-atlas`: Flag, set database type to `mongodb` and the flag to "true" to create Mongo Atlas target

`--mongodb-default-auth-db`: MongoDB server default authentication database

`--mongodb-uri-options`: MongoDB server URI options (For example, `replicaSet=mySet&authSource=authDB`)

`--mongodb-atlas-project-id`: MongoDB Atlas project ID

`--mongodb-atlas-api-public-key`: MongoDB Atlas public key

`--mongodb-atlas-api-private-key`: MongoDB Atlas private key

`--cluster-mode`: Flag, if set, define this target as cluster mode. relevant for MSSQL targets

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `digicert`

Creates a new DigiCert target in the current account

For initial Automated Certificate Management Environment (ACME) account bootstrap, provide `--eab-key-id` and `--eab-hmac-key` for External Account Binding (EAB). DNS-provider-specific flags such as `--hosted-zone`, `--dns-zone`, `--resource-group`, and `--gcp-project` are only relevant when `--acme-challenge=dns` and must match the provider used by `--dns-target-creds`.

#### Usage

```shell
akeyless target create digicert \
--name <Target name> \
--email <Email address for ACME account registration>
```

##### Flags

`-n, --name`: **Required**, Target name

`--digicert-url[=us-production]`: DigiCert ACME endpoint selector. Options: \[`us-production`/`eu-production`/`us-demo`/`eu-demo`]

`--acme-challenge[=dns]`: ACME challenge type. Options: \[`dns | http`]

`-e, --email`: **Required**, Email address for ACME account registration

`--eab-key-id`: DigiCert External Account Binding key identifier

`--eab-hmac-key`: DigiCert External Account Binding HMAC key

`--dns-target-creds`: Name of an existing cloud target that holds DNS provider credentials

`--hosted-zone`: AWS hosted-zone identifier for DNS validation

`--dns-zone`: Cloudflare DNS zone identifier for DNS validation

`--resource-group`: Azure resource group name for DNS validation

`--gcp-project`: GCP project ID for DNS validation

`--timeout[=5m]`: Timeout waiting for certificate validation

`-k, --key`: Key name used to encrypt the target secret value

`--description`: Description of the object

`--max-versions`: Maximum number of versions, limited by the account settings defaults

`--delete-protection`: Protection from accidental deletion of this object \[`true`/`false`]

### `dockerhub`

Creates a new Docker Hub target in the current account

#### Usage

```shell
akeyless target create dockerhub \
--name <Target name> \
--dockerhub-username <Username for docker repository> \
--dockerhub-password <Password for docker repository> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`--dockerhub-username`: **Required**, Username for Docker repository

`--dockerhub-password`: **Required**, Password for Docker repository

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `eks`

Creates a new Amazon EKS target in the current account

#### Usage

```shell
akeyless target create eks \
--name <Target name> \
--eks-cluster-name <EKS cluster name> \
--eks-cluster-endpoint <EKS cluster endpoint> \
--eks-cluster-ca-cert <EKS cluster base-64 encoded certificate> \
--eks-access-key-id <EKS access key ID> \
--eks-secret-access-key <EKS secret access key> \
--eks-region <EKS region> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`-e, --eks-cluster-name`: **Required**, EKS cluster name

`-c, --eks-cluster-endpoint`: **Required**, EKS cluster endpoint (that is, https\://`<IP>` of the cluster)

`-t, --eks-cluster-ca-cert`: **Required**, EKS cluster base-64 encoded certificate

`-i, --eks-access-key-id`: EKS access key ID

`-s, --eks-secret-access-key`: EKS secret access key

`-g, --use-gw-cloud-identity`: Use the GW's Cloud IAM

`--eks-region[=us-east-2]` EKS region

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used.

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `F5`&#x20;

Creates a new F5 target in the current account

#### Usage

```shell
akeyless target create f5-big-ip \
--name <Target name> \
--url <F5 BIG-IP URL> \
--username <F5 Username> \
--password <F5 Password> \
--key <Key name> \
--description <Description> \
--max-versions <Maximum Number of Versions> \
--delete-protection <true|false>
```

##### Flags

`-n, --name`: Required, Target name

`-u, --url`: Required, F5 BIG-IP target URL

`--username`: Required, F5 username with permission to manage certificates

`--password`: F5 BIG-IP password

`-k, --key`: The name of a key used to encrypt the target secret value. If not specified, the account default protectionKey is used

`--description`: Target description

`--max-versions`: Maximum number of versions to retain, limited by account settings

`--delete-protection`: Protect the object from accidental deletion (true/false)

### `gcp`

Creates a new GCP target in the current account

#### Usage

```shell
akeyless target create gcp \
--name <Target name> \
--gcp-key-file-path <Path to file with the base64-encoded service account private key> \
--gcp-key <Base64-encoded service account private key text> \
--use-gw-cloud-identity <Use the GWs Cloud IAM> \
--key <Key name> 
```

##### Flags

`-n, --name`: **Required**, Target name

`--gcp-key-file-path`: Path to file with the Base64-encoded service account private key

`--gcp-key`: Base64-encoded service account private key text

`-i, --use-gw-cloud-identity`: Use the GW's Cloud IAM

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `gemini`

Creates a new Gemini target in the current account

#### Usage

```shell
akeyless target create gemini \
--name <Target name> \
--gemini-url <Gemini API base URL> \
--api-key <Gemini API Key>
```

##### Flags

`-n, --name`: **Required**, Target name

`-u, --gemini-url[=https://generativelanguage.googleapis.com]`: Gemini API base URL

`-a, --api-key`: Gemini API key

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `github`

Creates a new GitHub target in the current account

#### Usage

```shell
akeyless target create github \
--name <Target name> \
--github-app-id <Github application id> \
--github-app-private-key <Github application private key (base64-encoded key)> \
--github-base-url <Github base url (Deafult = https://api.github.com/> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`--github-app-id`: GitHub application ID

`--github-app-private-key`: GitHub application private key (Base64-encoded key)

`--github-base-url[=https://api.github.com/]`: GitHub base URL

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used.

### `gitlab`

Creates a new GitLab target in the current account

#### Usage

```shell
akeyless target create gitlab \
--name <Target name> \
--gitlab-access-token <GitLab access token>
```

##### Flags

`-n, --name`: **Required**, Target name

`--gitlab-access-token`: GitLab access token

`--certificate`: GitLab TLS certificate in Base64 format

`--gitlab-url[=https://gitlab.com/]`: GitLab base URL

`--description`: Description of the object

`--max-versions`: Maximum number of versions, limited by the account settings defaults

`--delete-protection`: Protection from accidental deletion of this object \[`true`/`false`]

`-k, --key`: Key name used to encrypt the target secret value

### `google-trust`

Creates a new Google Trust target in the current account

For initial Automated Certificate Management Environment (ACME) account bootstrap, provide `--eab-key-id` and `--eab-hmac-key` for External Account Binding (EAB). DNS-provider-specific flags such as `--hosted-zone`, `--dns-zone`, `--resource-group`, and `--gcp-project` are only relevant when `--acme-challenge=dns` and must match the provider used by `--dns-target-creds`.

#### Usage

```shell
akeyless target create google-trust \
--name <Target name> \
--email <Email address for ACME account registration>
```

##### Flags

`-n, --name`: **Required**, Target name

`--google-trust-url[=production]`: Google Trust directory environment. Options: \[`production`/`staging`]

`--acme-challenge[=dns]`: ACME challenge type. Options: \[`dns | http`]

`-e, --email`: **Required**, Email address for ACME account registration

`--dns-target-creds`: Name of an existing cloud target that holds DNS provider credentials

`--hosted-zone`: AWS hosted-zone identifier for DNS validation

`--dns-zone`: Cloudflare DNS zone identifier for DNS validation

`--resource-group`: Azure resource group name for DNS validation

`--gcp-project`: GCP project ID for DNS validation

`--timeout[=5m]`: Timeout waiting for certificate validation

`-k, --key`: Key name used to encrypt the target secret value

`--description`: Description of the object

`--max-versions`: Maximum number of versions, limited by the account settings defaults

`--delete-protection`: Protection from accidental deletion of this object \[`true`/`false`]

### `gke`

Creates a new GKE target in the current account

#### Usage

```shell
akeyless target create gke \
--name <Target name> \
--gke-account-email <GKE service account email> \
--gke-cluster-endpoint <GKE cluster endpoint> \
--gke-cluster-ca-cert <GKE Base-64 encoded cluster certificate> \
--gke-account-key-file-path <File path to GKE service account key> \
--gke-cluster-name <GKE cluster name> \
--key <Key name> 
```

##### Flags

`-n, --name`: **Required**, Target name

`-a, --gke-account-email`: GKE service account email

`-e, --gke-cluster-endpoint`: GKE cluster endpoint, that is, cluster URI `https://<DNS/IP>`

`-c, --gke-cluster-ca-cert`: GKE Base64-encoded cluster certificate

`--gke-account-key-file-path`: File path to GKE service account key

`--gke-cluster-name`: GKE cluster name

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`-i, --use-gw-cloud-identity`: Use the GW's Cloud IAM

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `globalsign`

Creates a new GlobalSign Target in the current account

#### Usage

```shell
akeyless target create globalsign \
--name <Target name> \
--username <Username> \
--password <Password> \
--profile-id <Profile ID> \
--contact-first-name <Domain owner first name> \
--contact-last-name <Domain owner last name> \
--contact-phone <Domain owner Telephone> \
--contact-email <Domain owner Email> 
```

##### Flags

`-n, --name`: **Required**, Name for the GlobalSign target

`-u, --username`: **Required**, Username of the GlobalSign GCC account

`-p, --password`: **Required**, Password of the GlobalSign GCC account

`-i, --profile-id`: **Required**, Profile ID of the GlobalSign GCC account

`-f, --contact-first-name`: **Required**, First name of the GlobalSign GCC account contact

`-l, --contact-last-name`: **Required**, Last name of the GlobalSign GCC account contact

`--contact-phone`: **Required**, Telephone of the GlobalSign GCC account contact

`-e, --contact-email`: **Required**, Email of the GlobalSign GCC account contact

`--timeout[=5]`: Timeout for certificate validation.

`-k, --key`: Key name. The key will be used to encrypt the target item.

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `globalsign-atlas`

Creates a new GlobalSign Atlas target in the current account

#### Usage

```shell
akeyless target create globalsign-atlas \
--name <Target name> \
--api-key <GlobalSign Atlas API Key> \
--api-secret <GlobalSign Atlas API Secret> 
```

##### Flags

`-n, --name`: **Required**, Target Name

`-a, --api-key`: **Required**, API Key of the GlobalSign Atlas account

`-s, --api-secret`: **Required**, API Secret of the GlobalSign Atlas account

`--mtls-cert-file-path`: Path to the Mutual TLS Certificate of the GlobalSign Atlas account, either `mtls-cert-file-path` or `tls-cert-data-base64` must be supplied

`--mtls-cert-data-base64`: Mutual TLS Certificate contents of the GlobalSign Atlas account encoded in Base64, either `mtls-cert-file-path` or `mtls-cert-data-base64` must be supplied

`--mtls-key-file-path`: Path to the Mutual TLS Key of the GlobalSign Atlas account, either `mtls-key-file-path` or `mtls-key-data-base64` must be supplied

`--mtls-key-data-base64`: Mutual TLS Key contents of the GlobalSign Atlas account encoded in Base64, either `mtls-key-file-path` or `mtls-key-data-base64` must be supplied

`--timeout[=5m]`: Timeout waiting for certificate validation

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `godaddy`

Creates a new GoDaddy target

#### Usage

```shell
akeyless target create godaddy \
--name <Target name> \
--api-key <API Key> \
--secret <API credentials secret> \
--imap-username <Username>
--imap-password <Password>
--imap-fqdn <FQDN>
```

##### Flags

`-n, --name`: **Required**, Target name

`-a, --api-key`: **Required**, Key of the API credentials to the GoDaddy account

`-s, --secret`: **Required**, Secret of the API credentials to the GoDaddy account

`--timeout[=5m]`: Timeout waiting for certificate validation

`-u, --imap-username`: **Required**, Username to access the IMAP service

`-p, --imap-password`: **Required**, Password to access the IMAP service

`--imap-fqdn`: **Required**, FQDN of the IMAP service

`--imap-port[=993]`: **Required**, Port of the IMAP service

`--customer-id`: Customer ID (ShopperId) required for renewal of imported certificates

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `grok`

Creates a new Grok target

#### Usage

```shell
akeyless target create grok \
--name <Target name> \
--api-key <Grok API key> \
--grok-url[=https://api.x.ai] <Grok API base URL> \
--team-id <team ID> 
```

##### Flags

`-n, --name`: **Required**, Target name

`api-key`: The Grok API key

`grok-url`: The Grok API base URL. Default: [https://api.x.ai](https://api.x.ai)

`team-id`: The ID of the team this API key belongs to.

### `hashi-vault`

Creates a new HashiCorp Vault target

#### Usage

```shell
akeyless target create hashi-vault \
--name <Target name> \
--hashi-url 'https://<your-vault-api-url>:8200' \
--vault-token <Access Token> \
--namespace <Namespace Name>
```

##### Flags

`-n, --name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash / separators. If the folder does not exist, it will be created together with the target.

`--hashi-url`: HashiCorp Vault URL, for example, `https://<vault-mgr01>:8200`.

`--vault-token`: Vault access token with sufficient permissions.

`--namespace:` List of vault namespaces. To specify multiple namespaces use the argument multiple times: `--namespace ns1 --namespace ns2`

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

### `k8s`

Creates a new Kubernetes target in the current account

#### Usage

```shell
akeyless target create k8s \
--name <Target name> \
--k8s-cluster-endpoint <Kubernetes Cluster endpoint> \
--k8s-cluster-ca-cert <Kubernetes Cluster certificate> \
--k8s-cluster-token <Kubernetes Cluster authentication token> \
--k8s-cluster-name <Kubernetes cluster name> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`-e, --k8s-cluster-endpoint`: **Required**, Kubernetes Cluster endpoint. `https://<DNS / IP>` of the cluster

`-c, --k8s-cluster-ca-cert`: **Required**, Kubernetes Cluster certificate. Base 64 encoded certificate

`-t, --k8s-cluster-token`: **Required**, Kubernetes Cluster authentication token

`-i, --use-gw-service-account`: Use GW's service account. **Boolean** when provided only `name` is required

`--k8s-auth-type[=token]`: Kubernetes auth type, `[token/certificate]`

`--k8s-client-certificate`: Content of the Kubernetes client certificate (PEM format) in a Base64 format

`--k8s-client-certificate-file`: Path to a file that contain the Kubernetes client private key in PEM format

`--k8s-client-key`: Content of the k8 client private key (PEM format) in a Base64 format

`--k8s-client-key-file`: Path to a file that contain the Kubernetes client private key in PEM format

`--k8s-cluster-name`: Kubernetes cluster name

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used.

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `keycloak`

Creates a new Keycloak target in the current account

#### Usage

```shell
akeyless target create keycloak \
--name <Target name> \
--url <Keycloak URL> \
--realm <Keycloak realm> \
--client-id <Keycloak client ID> \
--client-secret <Keycloak client secret>
```

##### Flags

`-n, --name`: **Required**, Target name

`realm`: The Keycloak realm to connect to

`url`: The Keycloak API base URL

`client-id`: The ID of the Keycloak client configured for service account authentication

`client-secret`: The secret associated with the Keycloak client’s service account

`url`: The base URL of your Keycloak server

### `ldap`

Creates a new LDAP target in the current account

#### Usage

```shell
akeyless target create ldap \
--name <Target name> \
--ldap-url <LDAP Server URL> \
--bind-dn <LDAP Bind DN> \
--bind-dn-password <Password for LDAP Bind DN> \
--server-type <Set Ldap server type (Deafult = OpenLDAP)> \
--ldap-ca-cert <LDAP base-64 encoded CA Certificate> \
--token-expiration <token-expiration> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`-l, --ldap-url`: **Required**, LDAP Server URL

`-b, --bind-dn`: **Required**, LDAP Bind DN

`-p, --bind-dn-password`: **Required**, Password for LDAP Bind DN

`-s, --server-type[=OpenLDAP]`: Set LDAP server type, Options:\[OpenLDAP, ActiveDirectory]. Default is OpenLDAP

`-t, --ldap-ca-cert`: LDAP base-64 encoded CA Certificate

`--token-expiration`: --token-expiration

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `lets-encrypt`

Creates a new Let's Encrypt target in the current account

#### Usage

```shell
akeyless target create lets-encrypt \
--name <Target name> \
--lets-encrypt-url[=production] <production,staging> \
--acme-challenge[=http] <http/dns> \
--email <Email address for ACME account registration> \
--dns-target-creds <Target Name> \
--dns-zone <Cloudflare DNS zone> \
--hosted-zone <Amazon Route 53 hosted zone> \
--resource-group <Azure resource group name> \
--gcp-project <GCP project ID> \
--timeout[=5m] <Certificate validation timeout> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`--lets-encrypt-url[=production]`: Let's Encrypt directory environment. Options: \[`production`/`staging`]

`--acme-challenge[=http]`: ACME challenge type. Options: \[`http`/`dns`]

`-e, --email`: **Required**, Email address for ACME account registration

`--dns-target-creds`: Name of an existing cloud target that holds DNS provider credentials (supported: \[`AWS`/`Azure`/`GCP`/`Cloudflare`]). Relevant only when `--acme-challenge=dns`

`--dns-zone`: **Cloudflare DNS zone** name. Relevant only when `--acme-challenge`=`dns` and the DNS credentials target is Cloudflare

`--hosted-zone`: **Amazon Route 53** hosted zone identifier. Relevant only when `--acme-challenge`=`dns` and the DNS credentials target is AWS

`--resource-group`: **Azure resource group** name. Relevant only when `--acme-challenge`=`dns` and the DNS credentials target is Azure

`--gcp-project`: **GCP project ID**. Optional - can be derived from service account. Relevant only when `--acme-challenge`=`dns` and the DNS credentials target is GCP

`--timeout[=5m]`: Timeout waiting for certificate validation

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

### `linked`

Creates a new Linked Target which can inherit credentials from existing Targets

#### Usage

```shell
akeyless target create linked \
-n <linked target name> \
-p <parent target> \
-s <hosts>
```

##### Flags

`-n, --name`: **Required**, Name for the linked target

`-s, --hosts`: **Required**, A comma-separated list of server hosts and server descriptions joined by a semicolon ';' (that is 'server-dev.com;My Dev server,server-prod.com;My Prod server description')

`-p, --parent-target-name`: **Required**, The parent Target name from which to inherit credentials

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `okta`

Creates a new Okta target in the current account

#### Usage

```shell
akeyless target create okta \
--name <Target name> \
--api-token <Okta API token> \
--url <Okta URL> \
```

##### Flags

`-n, --name`: **Required**, Target name

`api-token`: The Okta API token

`url`: The URL of your Okta account

### `openai`

Creates a new OpenAI target in the current account

#### Usage

```shell
akeyless target create openai \
--name <Target name> \
--openai-url <OpenAI API base URL> \
--api-key <OpenAI API key> \
--api-key-id <OpenAI API key ID> \
--model <Default OpenAI model name> \
--organization-id <OpenAI Organization ID> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`-u, --openai-url[=https://api.openai.com/v1]`: OpenAI API base URL

`-a, --api-key`: OpenAI API key

`-i, --api-key-id`: OpenAI API key ID

`-m, --model`: Default OpenAI model name

`-o, --organization-id`: OpenAI Organization ID

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--delete-protection`: Protection from accidental deletion of this object, \[true/false]

### `ping`

Creates a new Ping target in the current account

#### Usage

```shell
akeyless target create ping \
--name <Target name> \
--ping-url <Ping url> \
--privileged-user <Username> \
--password <Pasword>
```

##### Flags

`-n, --name`: **Required**, Target name

`-u, --ping-url`: **Required**, Ping URL

`-s, --privileged-user`: **Required**, Privileged user name

`-p, --password`: **Required**, Privileged user Password

`-i, --administrative-port[=9999]`: Ping Federate administrative port

`-j, --authorization-port[=9031]`: Ping Federate authorization port

`-k, --key`: The name of a key used to encrypt the target secret value (if empty, the account default protectionKey key will be used)

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `rabbitmq`

Creates a new RabbitMQ target in the current account

#### Usage

```shell
akeyless target create rabbitmq \
--name <Target name> \
--user <RabbitMQ server user> \
--uri <RabbitMQ server URI> \
--pwd <RabbitMQ server password> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`--user`: **Required**, RabbitMQ server user

`--pwd`: RabbitMQ server password

`--uri`: **Required**, RabbitMQ server URI

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `salesforce`

Creates a new Salesforce target in the current account

#### Usage

```shell
akeyless target create salesforce \
--name <Target name> \
--tenant-url <URL of the Salesforce tenant> \
--client-id <Client ID of the OAuth2 app to use for connecting to Salesforce> \
--email <The email of the user attached to the oauth2 app used for connecting to Salesforce> \
--auth-flow <type of the auth flow ('jwt' / 'user-password') \
--client-secret <Client secret of the oauth2 app to use for connecting to Salesforce> 
```

##### Flags

`-n, --name`: **Required**, Target name

`-u, --tenant-url`: **Required**, URL of the Salesforce tenant

`-i, --client-id`: **Required**, Client ID of the oauth2 app to use for connecting to Salesforce

`-e, --email`: **Required**, The email of the user attached to the oauth2 app used for connecting to Salesforce

`-a, --auth-flow`: **Required**, type of the auth flow (`jwt`, `user-password`)

`-s, --client-secret`: Client secret of the oauth2 app to use for connecting to Salesforce (required for password flow)

`-f, --app-private-key-file-name`: Name of the of file containing a PEM private key of the connected app (relevant for JWT auth only)

`--app-private-key-data`: Base64-encoded PEM of the connected app private key (relevant for JWT auth only)

`-p, --password`: The password of the user attached to the OAuth2 app used for connecting to Salesforce (required for user-password flow)

`-o, --security-token`: The security token of the user attached to the oauth2 app used for connecting to Salesforce (required for user-password flow)

`--ca-cert-file-name`: Name of a file containing a PEM certificate to use when uploading new key to Salesforce

`--ca-cert-data`: Base64-encoded PEM cert to use when uploading a new key to Salesforce. Used if file name was not provided.

`--ca-cert-name`: name of the certificate in Salesforce tenant to use when uploading new key

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `sectigo`

Creates a new Sectigo target in the current account

#### Usage

```shell
akeyless target create sectigo \
--name <Target name> \
--username <Sectigo Username> \
--password <Sectigo Password> \
--customer-uri <Sectigo Customer URI > \
--organization-id <Sectigo Organization ID > \
--certificate-profile-id <Sectigo Certificate Profile ID> \
--external-requester <email1,emali2,email3> \
--timeout[=5m] <Certificate validation timeout> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`-u, --username`: **Required**, Username of the Sectigo account

`-p, --password`: **Required**, Password of the Sectigo account user

`-c, --customer-uri`: **Required**, Customer URI of the Sectigo account

`-o, --organization-id`: **Required**, Organization ID of the Sectigo account

`-i, --certificate-profile-id`: **Required**, Certificate Profile ID in Sectigo account

`-e, --external-requester`: **Required**, External Requester - a comma-separated list of emails

`--timeout[=5m]`: Timeout waiting for certificate validation

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `splunk`

Creates a new Splunk target in the current account

#### Usage

```shell
akeyless target create splunk \
--name <Target name> \
--url <Splunk server URLt> \
--use-tls[=true] <Enables TLS validation> \
--username <Splunk Username> \
--password <Splunk Password> \
--splunk-token <Splunk Token> \
--token-owner <Splunk token owner> \
--audience <Splunk token audience> 
--key <Key Name>
```

##### Flags

`-n, --name`: **Required**, Target name

`--url`: **Required**, Splunk server URL

`--use-tls[=true]`: Use TLS certificate verification when connecting to the Splunk management API

`--username`: Splunk Username

`--password`: Splunk Password

`--splunk-token`: Splunk Token

`--token-owner`: Splunk token owner (**relevant** when using **token** authentication for rotation)

`--audience`: Splunk token audience (**relevant** when using **token** authentication for rotation)

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

### `ssh`

Creates a new SSH target in the current account

#### Usage

```shell
akeyless target create ssh \
--name <Target name> \
--host <SSH host name> \
--port <SSH port (Default = 22)> \
--ssh-username <SSH username> \
--ssh-password <SSH password to rotate> \
--private-key-path <SSH private key file path> \
--private-key <SSH private key> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`--description`: Target description

`--host`: SSH host name

`--port[=22]`: SSH port

`--ssh-username`: SSH username

`--ssh-password`: SSH password to rotate

`--private-key-path`: SSH private key file path

`--private-key`: SSH private key

`--private-key-password`: SSH private key password

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `web`

Creates a new web target in the current account

#### Usage

```shell
akeyless target create web \
--name <Target name> \
--url <Web target URL> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`-u, --url`: **Required**, Web target URL

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `windows`

Creates a new Windows Target in the current account

#### Usage

```shell
akeyless target create windows \
-n <Windows target name> \
-s <hostname> \
-u <username> \
-p <password>
```

##### Flags

`-n, --name`: **Required**, Name for the Windows target

`-s, --hostname`: **Required**, Server hostname or IP Address

`-u, --username`: **Required**, Privileged username

`-p, --password`: **Required**, Privileged user password

`-d, --domain`: User domain name

`-r, --port[=5986]`: Windows Server WinRM port, by default, set to `5986` for `Https`

`--use-tls[=true]`: Enable/Disable TLS for WinRM over HTTPS \[true/false]

`--certificate`: SSL CA certificate in Base64 encoding generated from a trusted Certificate Authority (CA)

`-k, --key`: Key name. The key is used to encrypt the target secret value. If the key name is not specified, the account default protection key is used

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### `zerossl`

Creates a new ZeroSSL Target in the current account

#### Usage

```shell
akeyless target create zerossl \
--name <Target name> \
--api-key <API Key of the ZeroSSLTarget account> \
--imap-username <Username to access the IMAP service> \
--imap-password <Password to access the IMAP service> \
--imap-fqdn <FQDN of the IMAP service> \
--imap-validation-email <Email address to send the validation email>
```

##### Flags

`-n, --name`: **Required**, Name for the ZeroSSL target

`--api-key`: **Required**, ZeroSSL API Key, can be found under your ZeroSSL account in the Developer section

`--imap-username`: **Required**, An email address of the user registered to the IMAP service

`--imap-password`: **Required**, IMAP APP-Password

`--imap-fqdn`: **Required** IMAP FQDN, for example: `imap.gmail.com`

`--imap-validation-email`: The domain owner email address that certificate validation mail will be sent to, needs to be one of the following: `admin@domain.com`, `administrator@domain.com`, `hostmaster@domain.com`, `postmaster@domain.com`, `webmaster@domain.com`

`-timeout[=5m]-`: Timeout for certificate validation.

`--imap-port[=993]`: Port of the IMAP service

`-k, --key`: Key name. The key will be used to encrypt the target item.

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

## `delete`

Delete a target in the current account

### Usage

```shell
akeyless target delete \
--name <Target name> \
--target-version <Target Version>
```

#### Flags

`-n, --name`: **Required**, Target name

`-v, --target-version`: Target version

`--force-deletion[=false]`: Delete target even if it has associated items

## `delete-assoc-target-item`

Delete an association between target and item

### Usage

```shell
akeyless delete-assoc-target-item \
--name <Item name> \
--assoc-id <Association id to be deleted. Not required if target name specified> \
--target-name <The target name with which association will be deleted>
```

#### Flags

`-n, --name`: **Required**, Item name

`--id, --assoc-id`: The association ID to be deleted. Not required if target name specified

`-t, --target-name`: The target name with which association will be deleted

## `delete-targets`

Delete multiple targets from a given path

### Usage

```shell
akeyless delete-targets \
--path <Path to delete the targets from>
```

#### Flags

`-p, --path`: **Required**, Path to delete the targets from

`--force-deletion[=false]`: Delete target even if it has associated items

## `get`

Get target in the current account

### Usage

```shell
akeyless target get --name <Target name>
```

#### Flags

`-n, --name`: **Required**, Target name

`--show-versions[=false]`: Include all target versions in reply

## `get-details`

Get details of the specified target

### Usage

```shell
akeyless target get-details --name <Target Name>
```

#### Flags

`-n, --name`: **Required**, Target name

`-v, --target-version`: Target version

`--show-versions[=false]`: Include all target versions in reply

## `list`

List of all targets in the account

### Flags

`--filter`: Filter by target name or part of it

`-t, --type`: The target types list of the requested targets. If it is empty, all target types are returned. Options: `[hanadb cassandra aws ssh gke eks mysql mongodb snowflake mssql redshift artifactory azure rabbitmq k8s venafi gcp oracle dockerhub ldap github chef web salesforce postgres]`

`--pagination-token`: Next page reference

`--profile, --token`: Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

## `lock-target`

Lock a target.

### Usage

```shell
akeyless lock-target \
--name <Target name>
```

### Flags

`--name`: **Required**, Target name

`--lock-ttl[=60]`: Lock time to live in minutes

`--actions[=update,read]`: Comma-separated blocked actions

## `unlock-target`

Unlock a target.

### Usage

```shell
akeyless unlock-target \
--name <Target name>
```

### Flags

`--name`: **Required**, Target name

## `update`

### `artifactory`

Updates an existing Artifactory target in the current account

#### Usage

```shell
akeyless target update artifactory \
--name <Target name> \
--base-url <Artifactory REST URL> \
--artifactory-admin-name <Admin name> \
--artifactory-admin-pwd <Admin API Key/Password> \
--new-name <New target name> \
--key <Key name>
```

#### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`-b, --base-url`: **Required**, Artifactory REST URL, must end with `artifactory` postfix

`-a, --artifactory-admin-name`: **Required**, Admin name

`-p, --artifactory-admin-pwd`: **Required**, Admin API Key/Password

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--description`: Target description

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

### `aerospike`

Updates an existing aerospike target in the current account

#### Usage

```shell
akeyless target create artifactory \
--name <Target name> \
--new-name <New target name> \
--aerospike-cloud <true|false> \
--hostname <Aerospike Hostname> \
--port <Database port> \
--namespace <Namespace Name> \
--admin-username <Admin Username> \
--password <Admin Usernames Password> \
--aerospike-cluster-id <Cloud cluster ID> \
--aerospike-client-id <Client ID> \
--aerospike-client-secret <Aerospike Client Secret> \
--ssl <Enable SSL Encryption> \
--ssl-certificate <Base64-encoded SSL CA certificate> \ f
--ssl-certificate-file-path <Path to a file containing the SSL CA certificate> \
--enable-mtls <Enable mutual TLS authentication> \
--client-certificate <Client certificate> \ 
--client-certificate-file-path <Path to a file containing the client certificate> 
--client-private-key <Client private key> \
--client-private-key-file-path <Path to a file containing the client private key> \
--db-server-name <TLS server name used to verify the certificate hostname> \
--skip-server-name-validation <Skip server name verification while still validating the certificate chain>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name` : New Target Name

`--aerospike-cloud`: Set to `true` for Aerospike Cloud deployments

`--hostname`: Aerospike host address and port (for example: `url.to.aerospike.db`)

`--port`: Database connection port

`--namespace`: Namespace name (relevant only for Aerospike databases)

`--admin-username`: **Required**, Username of an account with the `user-admin` role

`--password`: **Required**, Password for the admin user

`--aerospike-cluster-id`: Cloud cluster ID (relevant only for Aerospike Cloud)

`--aerospike-client-id`: Client ID for Aerospike Cloud authentication (relevant only for Aerospike Cloud)

`--aerospike-client-secret`: Client secret for Aerospike Cloud authentication (relevant only for Aerospike Cloud)

`--ssl`: Enable SSL encryption (`true`/`false`)

`--ssl-certificate`: Base64-encoded SSL CA certificate from a trusted Certificate Authority (CA)

`--ssl-certificate-file-path`: Path to a file containing the SSL CA certificate from a trusted Certificate Authority (CA)

`--enable-mtls`: Enable mutual TLS (mTLS) authentication. Requires `--ssl=true`

`--client-certificate`: Client certificate used for mTLS authentication

`--client-certificate-file-path`: Path to a file containing the client certificate used for mTLS authentication

`--client-private-key`: Client private key used for mTLS authentication

`--client-private-key-file-path`: Path to a file containing the client private key used for mTLS authentication

`--db-server-name`: TLS server name used to verify the certificate hostname. If not specified, the Aerospike hostname is used

`--skip-server-name-validation`: Skip server name verification while still validating the certificate chain (`true`/`false`). If empty, server name validation is performed normally.

#### `aws`

Updates an existing AWS target in the current account

##### Usage

```shell
akeyless target update aws \
--name <Target name> \
--new-name <New target name> \
--access-key-id <AWS access key ID> \
--access-key <AWS secret access key> \
--region <AWS rigion (Default = us-east-2)> \
--use-gw-cloud-identity <Use the GWs Cloud IAM> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`--description`: Target description

`--access-key-id`: AWS access key ID

`--access-key`: AWS secret access key

`--session-token`: Required only for temporary security credentials retrieved using STS

`--region[=us-east-2]`: AWS region

`-i, --use-gw-cloud-identity`: Use the GW's Cloud IAM

`--generate-external-id[=false]`: A unique auto-generated value used in your AWS account when configuring your AWS IAM role to securely delegate access to Akeyless. Relevant only when using **GW cloud ID**

`role-arn`: AWS IAM role identifier that Gateway will assume in your AWS account, relevant only when using **external ID**

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

#### `azure`

Updates an existing Azure target in the current account

##### Usage

```shell
akeyless target update azure \
--name <Target name> \
--new-name <New target name> \
--client-id <Azure client/application id> \
--tenant-id <Azure tenant id> \
--client-secret <Azure client secret> \
--azure-cloud[=AzureCloud] <AzureCloud/AzureUSGovernment/AzureChinaCloud> \
--use-gw-cloud-identity <Use the GWs Cloud IAM> \
--subscription-id <Azure Subscription Id> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--client-id`: Azure client/application ID

`--tenant-id`: Azure tenant ID

`--client-secret`: Azure client secret

`--azure-cloud[=AzureCloud]`: Azure cloud environment to use. Values: `AzureCloud` (default), `AzureUSGovernment`, `AzureChinaCloud`

`-i, --use-gw-cloud-identity`: Use the GW's Cloud IAM

`--subscription-id`: Azure Subscription ID

`--resource-group-name`: The Resource Group name in your Azure Subscription

`--resource-name`: The name of the relevant Resource

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

#### `claude`

Updates an existing Claude target in the current account

##### Usage

```shell
akeyless target update claude \
--name <Target name> \
--new-name <New target name> \
--api-key <Claude API key> \
--claude-url <Claude API base URL> 
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`api-key`: The Claude API key.

`claude-url`: The Claude API base URL. Default: [https://api.anthropic.com](https://api.anthropic.com)

#### `cloudflare`

Updates an existing Cloudflare target in the current account

##### Usage

```shell
akeyless target update cloudflare \
--name <Target name> \
--new-name <New target name> \
--api-token <Cloudflare API token> \
--account-id <Cloudflare account ID> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`--api-token`: Cloudflare API token

`--account-id`: Optional. Cloudflare account ID

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

#### `custom-dns`

Updates an existing Custom-DNS target in the current account

##### Usage

```shell
akeyless target update custom-dns \
--name <Target name> \
--new-name <New target name> \
--provider-type <DNS Provider> \
--dns-parameter <Key|Value>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`provider-type`: The DNS provider type. All DNS providers available through the Lego project are supported.

`dns-parameter`: The parameters for the DNS provider.

#### `db`

Update an existing db target in the current account

##### Usage

```shell
akeyless target update db \
--name <Target name> \
--db-type *<mysql/mssql/postgres/mongodb/snowflake/cassandra/oracle/redshift/redis> \
--new-name <New target name> \
--user-name <Database user name> \
--host <Database host> \
--pwd <Database password> \
--port <Database port> \
--db-name <Database name>
```

##### Flags

`-n, --name`: **Required**, Target name

`-t, --db-type`: **Required**, Database type: `[mysql/mssql/postgres/mongodb/snowflake/cassandra/oracle/redshift/redis]`

`--new-name`: New target name

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--user-name`: Database user name

`--host`: Database host

`--pwd`: Database password

`--port`: Database port

`--db-name`: Database name

`--db-server-certificates`: Set of root certificate authorities in Base64 encoding used by clients to verify server certificates

`--db-server-name`: Server name is used to verify the hostname on the returned certificates unless InsecureSkipVerify is provided. It is also included in the client's handshake to support virtual hosting unless it is an IP address

`--snowflake-account`: Snowflake account name

`--mongodb-atlas`: Flag, set database type to `mongodb` and the flag to `true` to create Mongo Atlas target

`--mongodb-default-auth-db`: MongoDB server default authentication database

`--mongodb-uri-options`: MongoDB server URI options (For example, `replicaSet=mySet&authSource=authDB`)

`--mongodb-atlas-project-id`: MongoDB Atlas project ID

`--mongodb-atlas-api-public-key`: MongoDB Atlas public key

`--mongodb-atlas-api-private-key`: MongoDB Atlas private key

`--cluster-mode`: Flag, if set, define this target as cluster mode. relevant for MSSQL targets

`--ssl[=false]`: Enable/Disable SSL \[true/false]

`--ssl-certificate`: SSL CA certificate in Base64 encoding generated from a trusted Certificate Authority (CA)

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

#### `dockerhub`

updates an existing Docker Hub target in the current account

##### Usage

```shell
akeyless target update dockerhub \
--name <Target Name> \
--dockerhub-username <Username for docker repository> \
--dockerhub-password <Password for docker repository> \
--new-name <New target name>
```

#### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`--dockerhub-username`: **Required**, Username for Docker repository

`--dockerhub-password`: **Required**, Password for Docker repository

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

#### `eks`

Updates an existing Amazon EKS target in the current account

#### Usage

```shell
akeyless target update eks \
--name <Target Name> \
--eks-cluster-name <EKS cluster Name> \
--eks-cluster-endpoint <EKS Cluster Endpoint> \
--eks-cluster-ca-cert <EKS Cluster Certificate \
--eks-access-key-id <EKS Access ID> \
--eks-secret-access-key <EKS Secret Access Key> \
--new-name <New target name>
```

##### Flags

`-n, --name`: **Required**, Target name

`-c, --eks-cluster-name`: **Required**, EKS cluster name

`-e, --eks-cluster-endpoint`: **Required**, EKS cluster endpoint (that is, https\://`<IP>` of the cluster)

`-r, --eks-cluster-ca-cert`: **Required**, EKS cluster base-64 encoded certificate

`-i, --eks-access-key-id`: **Required**, EKS access key ID

`-s, --eks-secret-access-key`: **Required**, EKS secret access key

`-g, --use-gw-cloud-identity`: Use the Akeyless Gateway's Cloud IAM

`--new-name`: New target name

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--eks-region[=us-east-2]`: EKS cluster's region

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

#### `gcp`

Update an existing GCP target in the current account

#### Usage

```shell
akeyless target update gcp \
--name <Target Name> \
--new-name <New target name> \
--gcp-key-file-path <Path to file with the base64-encoded service account private key> \
--gcp-key <Base64-encoded service account private key text> \
--use-gw-cloud-identity <Use the GWs Cloud IAM> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--gcp-key-file-path`: Path to file with the Base64-encoded service account private key

`--gcp-key`: Base64-encoded service account private key text

`-i, --use-gw-cloud-identity`: Use the Akeyless Gateway's Cloud IAM

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

#### `digicert`

Updates an existing DigiCert target

DNS-provider-specific flags such as `--hosted-zone`, `--dns-zone`, `--resource-group`, and `--gcp-project` are only relevant when `--acme-challenge=dns` and must match the provider used by `--dns-target-creds`.

##### Usage

```shell
akeyless target update digicert \
--name <Target name> \
--email <Email address for ACME account registration>
```

##### Flags

`-n, --name`: **Required**, Target name

`--digicert-url[=us-production]`: DigiCert ACME endpoint selector. Options: \[`us-production`/`eu-production`/`us-demo`/`eu-demo`]

`--acme-challenge[=dns]`: ACME challenge type. Options: \[`dns`]

`-e, --email`: **Required**, Email address for ACME account registration

`--eab-key-id`: DigiCert External Account Binding key identifier

`--eab-hmac-key`: DigiCert External Account Binding HMAC key

`--dns-target-creds`: Name of an existing cloud target that holds DNS provider credentials

`--hosted-zone`: AWS hosted-zone identifier for DNS validation

`--dns-zone`: Cloudflare DNS zone identifier for DNS validation

`--resource-group`: Azure resource group name for DNS validation

`--gcp-project`: GCP project ID for DNS validation

`--timeout[=5m]`: Timeout waiting for certificate validation

`--new-name`: New target name

`-k, --key`: Key name used to encrypt the target secret value

`--keep-prev-version`: Whether to keep the previous version \[`true`/`false`]

`--description`: Description of the object

`--max-versions`: Maximum number of versions, limited by the account settings defaults

#### `gemini`

Updates a Gemini target in the current account

#### Usage

```shell
akeyless target update gemini \
--name <Target name> \
--new-name <New target name> \
--gemini-url <Gemini API base URL> \
--api-key <Gemini API Key>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`-u, --gemini-url[=https://generativelanguage.googleapis.com]`: Gemini API base URL

`-a, --api-key`: Gemini API key

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

#### `github`

updates a new GitHub target in the current account

##### Usage

```shell
akeyless target update github \
--name <Target Name> \
--new-name <New target name> \
--github-app-id <Github application ID> \
--github-app-private-key <Github application private key> \
--github-base-url <Github base url (Deafult = https://api.github.com>
```

#### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`--github-app-id`: GitHub application ID

`--github-app-private-key`: GitHub application private key (Base64-encoded key)

`--github-base-url[=https://api.github.com/]`: GitHub base URL

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

#### `gitlab`

Updates an existing GitLab target in the current account

##### Usage

```shell
akeyless target update gitlab \
--name <Target name> \
--gitlab-access-token <GitLab access token>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`--gitlab-access-token`: GitLab access token

`--certificate`: GitLab TLS certificate in Base64 format

`--gitlab-url[=https://gitlab.com/]`: GitLab base URL

`--description`: Description of the object

`--max-versions`: Maximum number of versions, limited by the account settings defaults

`--delete-protection`: Protection from accidental deletion of this object \[`true`/`false`]

`-k, --key`: Key name used to encrypt the target secret value

`--keep-prev-version`: Whether to keep the previous version \[`true`/`false`]

#### `google-trust`

Updates an existing Google Trust target

`--eab-key-id` and `--eab-hmac-key` are create-only bootstrap values. DNS-provider-specific flags such as `--hosted-zone`, `--dns-zone`, `--resource-group`, and `--gcp-project` are only relevant when `--acme-challenge=dns` and must match the provider used by `--dns-target-creds`.

##### Usage

```shell
akeyless target update google-trust \
--name <Target name> \
--email <Email address for ACME account registration>
```

##### Flags

`-n, --name`: **Required**, Target name

`--google-trust-url[=production]`: Google Trust directory environment. Options: \[`production`/`staging`]

`--acme-challenge[=dns]`: ACME challenge type. Options: \[`dns`]

`-e, --email`: **Required**, Email address for ACME account registration

`--dns-target-creds`: Name of an existing cloud target that holds DNS provider credentials

`--hosted-zone`: AWS hosted-zone identifier for DNS validation

`--dns-zone`: Cloudflare DNS zone identifier for DNS validation

`--resource-group`: Azure resource group name for DNS validation

`--gcp-project`: GCP project ID for DNS validation

`--timeout[=5m]`: Timeout waiting for certificate validation

`--new-name`: New target name

`-k, --key`: Key name used to encrypt the target secret value

`--keep-prev-version`: Whether to keep the previous version \[`true`/`false`]

`--description`: Description of the object

`--max-versions`: Maximum number of versions, limited by the account settings defaults

#### `gke`

Updates an existing GKE target in the current account

#### Usage

```shell
akeyless target update gke \
--name <Target Name> \
--new-name <New target name> \
--gke-account-email <GKE service account email> \
--gke-cluster-endpoint <GKE cluster endpoint> \
--gke-cluster-ca-cert <GKE Base-64 encoded cluster certificate> \
--gke-account-key-file-path <File path to GKE service account key> \
--gke-account-key <GKE service account key> \
--gke-cluster-name <GKE cluster name>
```

##### Flags

`-n, --name`: **Required**, Target name

`-a, --gke-account-email`: GKE service account email

`-e, --gke-cluster-endpoint`: GKE cluster endpoint, that is, cluster URI

`-c, --gke-cluster-ca-cert`: GKE Base-64 encoded cluster certificate

`--gke-account-key-file-path`: File path to GKE service account key

`--gke-account-key`: GKE service account key

`--gke-cluster-name`: GKE cluster name

`--new-name`: New target name

`-i, --use-gw-cloud-identity`: Use the GW's Cloud IAM

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

#### `globalsign`

Update an existing GlobalSign Target in the current account

##### Usage

```shell
akeyless target update globalsign \
--name <Target Name> \
--username <Username> \
--password <Password> \
--profile-id <Profile ID> \
--contact-first-name <Account owner first name> \
--contact-last-name <Account owner last name> \
--contact-phone <Account owner Telephone> \
--contact-email <Account owner email> \
--new-name <New Name>
```

##### Flags

`-n, --name`: **Required**, Target name

`-u, --username`: **Required**, Username of the GlobalSign GCC account

`-p, --password`: **Required**, Password of the GlobalSign GCC account

`-i, --profile-id`: **Required**, Profile ID of the GlobalSign GCC account

`-f, --contact-first-name`: **Required**, First name of the GlobalSign GCC account contact

`-l, --contact-last-name`: **Required**, First name of the GlobalSign GCC account contact

`--contact-phone`: **Required**, Telephone of the GlobalSign GCC account contact

`-e, --contact-email`: **Required**, Email of the GlobalSign GCC account contact

`--timeout[=5]`: Timeout waiting for certificate validation

`--new-name`: New target name

`-k, --key`: Key name. The key will be used to encrypt the target secret value

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

#### `globalsign-atlas`

Updates an existing GlobalSignAtlas target in the current account

##### Usage

```shell
akeyless target update globalsign-atlas \
--name <Target Name> \
--api-key <GlobalSign Atlas API Key> \
--api-secret <GlobalSign Atlas API Secret>
```

##### Flags

`-n, --name`: **Required**, Target Name

`-a, --api-key`: **Required**, API Key of the GlobalSign Atlas account

`-s, --api-secret`: **Required**, API Secret of the GlobalSign Atlas account

`--mlts-cert-file-path`: Path to the Mutual TLS Certificate of the GlobalSign Atlas account, either `mtls-cert-file-path` or `mtls-cert-data-base64` must be supplied

`--mlts-cert-data-base64`: Mutual TLS Certificate contents of the GlobalSign Atlas account encoded in base64, either `mtls-cert-file-path` or `mtls-cert-data-base64` must be supplied

`--mlts-key-file-path`: Path to the Mutual TLS Key of the GlobalSign Atlas account, either `mtls-key-file-path` or `mtls-key-data-base64` must be supplied

`--mlts-key-data-base64`: Mutual TLS Key contents of the GlobalSign Atlas account encoded in base64, either `mtls-key-file-path` or `mtls-key-data-base64` must be supplied

`--timeout[=5]`: Timeout waiting for certificate validation

`--new-name`: New Target Name

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

#### `godaddy`

Updates an existing GoDaddy target in the current account

##### Usage

```shell
akeyless target update godaddy \
--name <Target name> \
--new-name <New target name> \
--api-key <API Key> \
--secret <API credentials secret> \
--imap-username <Username> \
--imap-password <Password> \
--imap-fqdn <FQDN>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`-a, --api-key`: **Required**, Key of the API credentials to the GoDaddy account

`-s, --secret`: **Required**, Secret of the API credentials to the GoDaddy account

`--timeout[=5m]`: Timeout waiting for certificate validation

`-u, --imap-username`: **Required**, Username to access the IMAP service

`-p, --imap-password`: **Required**, Password to access the IMAP service

`--imap-fqdn`: **Required**, FQDN of the IMAP service

`--imap-port[=993]`: **Required**, Port of the IMAP service

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

#### `grok`

Updates an existing Grok target in the current account

##### Usage

```shell
akeyless target update grok \
--name <Target name> \
--new-name <New target name> \
--api-key <Grok API key> \
--grok-url[=https://api.x.ai] <Grok API base URL> \
--team-id <team ID> 
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`api-key`: The Grok API key&#x20;

`grok-url`: The Grok API base URL. Default: [https://api.x.ai](https://api.x.ai)

`team-id`: The ID of the team this API key belongs to

#### `hashi-vault`

Updates a new HashiCorp Vault target

##### Usage

```shell
akeyless target update hashi-vault \
--name <Target name> \
--new-name <New Target Name>
--hashi-url 'https://<your-vault-api-url>:8200' \
--vault-token <Access Token> \
--namespace <Namespace Name>
```

##### Flags

`-n, --name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash / separators. If the folder does not exist, it will be created together with the target.

`--new-name`: New target name

`--hashi-url`: HashiCorp Vault URL, for example, `https://<vault-mgr01>:8200`.

`--vault-token`: Vault access token with sufficient permissions.

`--namespace:` List of vault namespaces. To specify multiple namespaces use the argument multiple times: `--namespace ns1 --namespace ns2`

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

#### `k8s`

Updates an existing Kubernetes target in the current account

##### Usage

```shell
akeyless target update k8s \
--name <Target Name> \
--k8s-cluster-endpoint <Kubernetes Cluster endpoint> \
--k8s-cluster-ca-cert <Kubernetes Cluster certificate> \
--k8s-cluster-token <Kubernetes Cluster authentication token> \
--k8s-cluster-name <Kubernetes cluster name> \
--new-name <New target name> 
```

##### Flags

`-n, --name`: **Required**, Target name

`-e, --k8s-cluster-endpoint`: **Required**, Kubernetes Cluster endpoint. https\://, \<DNS / IP> of the cluster

`-c, --k8s-cluster-ca-cert`: **Required**, Kubernetes Cluster certificate. Base 64 encoded certificate

`-t, --k8s-cluster-token`: **Required**, Kubernetes Cluster authentication token

`-i, --use-gw-service-account`: Use the Gateway's ServiceAccount

`--k8s-auth-type[=token]`: Kubernetes auth type, `[token/certificate]`

`--k8s-client-certificate`: Content of the k8 client certificate (PEM format) in a Base64 format

`--k8s-client-certificate-file`: Path to a file that contain the Kubernetes client certificate in PEM format

`--k8s-client-key`: Content of the k8 client private key (PEM format) in a Base64 format

`--k8s-client-key-file\`: Path to a file that contain the Kubernetes client private key in PEM format

`--k8s-cluster-name`: Kubernetes cluster name

`--new-name`: New target name

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

#### `keycloak`

Updates an existing Keycloak target in the current account

##### Usage

```shell
akeyless target update keyclock \
--name <Target name> \
--new-name <New target name> \
--url <Keycloak URL> \
--realm <Keycloak realm> \
--client-id <Keycloak client ID> \
--client-secret <Keycloak client secret>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`--url`: The Keycloak API base URL

`--realm`: The Keycloak realm to connect to

`--client-id`: The ID of the Keycloak client configured for service account authentication

`--client-secret`: The secret associated with the Keycloak client’s service account.

`--url`: The base URL of your Keycloak server

#### `ldap`

updates a new LDAP target in the current account

##### Usage

```shell
akeyless target update ldap \
--name <Target Name> \
--ldap-url <LDAP Serve URL> \
--bind-dn <LDAP Bind DN> \
--bind-dn-password <Password for LDAP Bind DN> \
--new-name <New target name> \
--server-type <Set Ldap server type, Options:[OpenLDAP, ActiveDirectory]>
```

#### Flags

`-n, --name`: **Required**, Target name

`-l, --ldap-url`: **Required**, LDAP Server URL

`-b, --bind-dn`: **Required**, LDAP Bind DN

`-p, --bind-dn-password`: **Required**, Password for LDAP Bind DN

`-s, --server-type`: Set LDAP server type, Options:\[OpenLDAP, ActiveDirectory]

`--new-name`: New target name

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`-t, --ldap-ca-cert`: LDAP base-64 encoded CA Certificate

`--token-expiration`: LDAP token expiration in seconds

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

### `lets-encrypt`

Updates an existing Let's Encrypt target in the current account

#### Usage

```shell
akeyless target update lets-encrypt \
--name <Target name> \
--new-name <New Target name> \
--lets-encrypt-url[=production] <production,staging> \
--acme-challenge[=http] <http/dns> \
--email <Email address for ACME account registration> \
--dns-target-creds <Target Name> \
--dns-zone <Cloudflare DNS zone> \
--hosted-zone <Amazon Route 53 hosted zone> \
--resource-group <Azure resource group name> \
--gcp-project <GCP project ID> \
--timeout[=5m] <Certificate validation timeout> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New Target Name

`--lets-encrypt-url[=production]`: Let's Encrypt directory environment. Options: \[`production`/`staging`]

`--acme-challenge[=http]`: ACME challenge type. Options: \[`http`/`dns`]

`-e, --email`: **Required**, Email address for ACME account registration

`--dns-target-creds`: Name of an existing cloud target that holds DNS provider credentials (supported: \[`AWS`/`Azure`/`GCP`/`Cloudflare`]). Relevant only when `--acme-challenge=dns`

`--dns-zone`: **Cloudflare DNS zone** name. Relevant only when `--acme-challenge`=`dns` and the DNS credentials target is Cloudflare

`--hosted-zone`: **Amazon Route 53** hosted zone identifier. Relevant only when `--acme-challenge`=`dns` and the DNS credentials target is AWS

`--resource-group`: **Azure resource group** name. Relevant only when `--acme-challenge`=`dns` and the DNS credentials target is Azure

`--gcp-project`: **GCP project ID**. Optional - can be derived from service account. Relevant only when `--acme-challenge`=`dns` and the DNS credentials target is GCP

`--timeout[=5m]`: Timeout waiting for certificate validation

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

###

#### `linked`

Update an existing Linked Target in the current account

##### Usage

```shell
akeyless target update linked \
--name <linked target name> \
--new-name <new name> \
--parent <parent target> \
--hosts <hosts>
```

##### Flags

`-n, --name`: **Required**, The name of the existing Linked Target

`--new-name`: New name for the Linked Target

`-s, --hosts`: A comma-separated list of server hosts and server descriptions joined by a semicolon ';' (that is `server-dev.com`;`My Dev server`, `server-prod.com`;`My Prod server description`)

`--add-hosts`: A comma-separated list of new server hosts and server descriptions joined by a semicolon ';' that will be added to the Linked Target hosts (for example, `server-dev.com;My Dev server,server-prod.com;My Prod server description`).

`--rm-hosts`: Comma-separated list of existing hosts that will be removed from Linked Target hosts.

`-p, --parent-target-name`: The parent Target name from which to inherit credentials

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

#### `okta`

Updates an existing Okta target in the current account

##### Usage

```shell
akeyless target update okta \
--name <Target name> \
--new-name <New target name> \
--api-token <Okta API token> \
--url <Okta URL>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`api-token`: The Okta API token.

`url`: The URL of your Okta account.

#### `openai`

Updates an existing OpenAI target in the current account

##### Usage

```shell
akeyless target update openai \
--name <Target name> \
--new-name <New target name> \
--openai-url <OpenAI API base URL> \
--api-key <OpenAI API key> \
--api-key-id <OpenAI API key ID> \
--model <Default OpenAI model name> \
--organization-id <OpenAI Organization ID>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`-u, --openai-url[=https://api.openai.com/v1]`: OpenAI API base URL

`-a, --api-key`: OpenAI API key

`-i, --api-key-id`: OpenAI API key ID

`-m, --model`: Default OpenAI model name

`-o, --organization-id`: OpenAI Organization ID

`--description[=default_comment]`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults.

`--delete-protection`: Protection from accidental deletion of this object, \[true/false]

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

#### `ping`

Updates an existing Ping target in the current account

##### Usage

```shell
akeyless target update ping \
--name <Target name> \
--new-name <New target name> \
--ping-url <Ping URL> \
--privileged-user <Ping Federate privileged user> \
--password <Ping Federate privileged user password>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`-u, --ping-url`: **Required**, Ping URL

`-s, --privileged-user`: **Required**, Ping Federate privileged user

`-p, --password`: **Required**, Ping Federate privileged user password

`-i, --administrative-port[=9999]`: Ping Federate administrative port

`-j, --authorization-port[=9031]`: Ping Federate authorization port

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults.

`--delete-protection`: Protection from accidental deletion of this object, \[true/false]

#### `rabbitmq`

Update an existing new RabbitMQ target in the current account

##### Usage

```shell
akeyless target update rabbitmq \
--name <Target Name> \
--new-name <New target name> \
--user <RabbitMQ server user> \
--pwd <RabbitMQ server password> \
--uri <RabbitMQ server URI> \
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--user`: RabbitMQ server user

`--pwd`: RabbitMQ server password

`--uri`: RabbitMQ server URI

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

#### `salesforce`

Updates the Salesforce target in the current account

##### Usage

```shell
akeyless target update salesforce \
--name <Target name> \
--tenant-url <URL of the Salesforce tenant> \
--client-id <Client ID of the oauth2 app to use for connecting to Salesforce> \
--email <The email of the user attached to the oauth2 app used for connecting to Salesforce> \
--auth-flow <type of the auth flow ('jwt' / 'user-password')> \
--new-name <New target name> \
--client-secret <Client secret of the oauth2 app to use for connecting to Salesforce>
```

##### Flags

`-n, --name`: **Required**, Target name

`-u, --tenant-url`: **Required**, URL of the Salesforce tenant

`-i, --client-id`: **Required**, Client ID of the oauth2 app to use for connecting to Salesforce

`-e, --email`: **Required**, The email of the user attached to the oauth2 app used for connecting to Salesforce

`-a, --auth-flow`: **Required**, type of the auth flow ('jwt' / 'user-password')

`-s, --client-secret`: Client secret of the oauth2 app to use for connecting to Salesforce (required for password flow)

`-f, --app-private-key-file-name`: Name of the of file containing a PEM private key of the connected app (relevant for JWT auth only)

`--app-private-key-data`: Base64-encoded PEM of the connected app private key (relevant for JWT auth only)

`-p, --password`: The password of the user attached to the oauth2 app used for connecting to Salesforce (required for user-password flow)

`-o, --security-token`: The security token of the user attached to the oauth2 app used for connecting to Salesforce (required for user-password flow)

`--ca-cert-file-name`: Name of a file containing a PEM certificate to use when uploading new key to Salesforce

`--ca-cert-data`: Base64-encoded PEM cert to use when uploading a new key to Salesforce. Used if file name was not provided.

`--ca-cert-name`: name of the certificate in Salesforce tenant to use when uploading new key

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

#### `sectigo`

Updates the Sectigo target in the current account

##### Usage

```shell
akeyless target update sectigo \
--name <Target name> \
--username <Sectigo Username> \
--password <Sectigo Password> \
--customer-uri <Sectigo Customer URI > \
--organization-id <Sectigo Organization ID > \
--certificate-profile-id <Sectigo Certificate Profile ID> \
--external-requester <email1,emali2,email3> \
--timeout[=5m] <Certificate validation timeout> \
--new-name <New target name>
--key <Key name>
```

##### Flags

`-n, --name`: **Required**, Target name

`-u, --username`: **Required**, Username of the Sectigo account

`-p, --password`: **Required**, Password of the Sectigo account user

`-c, --customer-uri`: **Required**, Customer URI of the Sectigo account

`-o, --organization-id`: **Required**, Organization ID of the Sectigo account

`-i, --certificate-profile-id`: **Required**, Certificate Profile ID in Sectigo account

`-e, --external-requester`: **Required**, External Requester - a comma-separated list of emails

`--timeout[=5m]`: Timeout waiting for certificate validation

`--new-name`: New target name

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

#### `ssh`

Update an existing SSH target in the current account

##### Usage

```shell
akeyless target update ssh \
--name <Target Name> \
--new-name <New target name> \
--host <SSH host name> \
--port <SSH port (Deafult = 22)> \
--ssh-username <SSH username> \
--ssh-password <SSH password to rotate> \
--private-key-path <SSH private key file path> \
--private-key <SSH private key>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--host`: SSH host name

`--port[=22]`: SSH port

`--ssh-username`: SSH username

`--ssh-password`: SSH password to rotate

`--private-key-path`: SSH private key file path

`--private-key`: SSH private key

`--private-key-password`: SSH private key password

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

#### `web`

Update an existing web target in the current account

##### Usage

```shell
akeyless target update web \
--name <Target Name> \
--new-name <New target name> \
--url <Web target URL>
```

##### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`--description`: Target description

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`-u, --url`: Web target URL

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--update-version`: \[Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

#### `windows`

Update an existing Windows Target in the current account

##### Usage

```shell
akeyless target update windows \
--name <Windows target name> \
--hosts <hostname> \
--username <username> \
--password <password> \
--new-name <new name> 
```

##### Flags

`-n, --name`: **Required**, Name for the Windows target

`--new-name`: New name for the Windows Target

`-s, --hostname`: **Required**, Server hostname or IP Address

`-u, --username`: **Required**, Privileged username

`-p, --password`: **Required**, Privileged user password

`-d, --domain`: User domain name

`-r, --port[=5986]`: Server WinRM port

`--use-tls[=true]`: Enable/Disable TLS for WinRM over HTTPS \[true/false]

`--certificate`: SSL CA certificate in Base64 encoding generated from a trusted Certificate Authority (CA)

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--keep-prev-version`: Whether to keep previous version, options:\[true, false]. If not set, use default according to account settings

`--description`: Description of the object

#### `zerossl`

Update an existing ZeroSSL Target in the current account

##### Usage

```shell
akeyless target update zerossl \
--name <Target Name> \
--api-key <API Key of the ZeroSSLTarget account> \
--imap-username <Username to access the IMAP service> \
--imap-password <Password to access the IMAP service> \
--imap-fqdn <FQDN of the IMAP service> \
--imap-validation-email <Email address to send the validation email> \
--new-name <New Name>
```

##### Flags

`-n, --name`: **Required**, Name for the ZeroSSL target

`--api-key`: **Required**, ZeroSSL API Key, can be found under your ZeroSSL account in the Developer section

`--imap-username`: **Required**, An email address of the user registered to the IMAP service

`imap-password`: **Required**, IMAP APP-Password - for example, on Gmail Under Settings-> Security, click on 2-Step Verification and generate APP-Password (2-Step verification must be enabled)

`--imap-fqdn`: **(Mandatory)** IMAP FQDN, for example imap.gmail.com

`--imap-validation-email`: The domain owner email address that certificate validation mail will be sent to, needs to be one of the following: `admin@domain.com`, `administrator@domain.com`, `hostmaster@domain.com`, `postmaster@domain.com`, `webmaster@domain.com`

`--imap-port[=993]`: Port of the IMAP service

`--new-name`: New target name

`-k, --key`: Key name. The key will be used to encrypt the target secret value

`--keep-prev-version`: Whether to keep the previous version, options:\[true, false], If not set, use default according to account settings

`--description`: Description of the object

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

## `update-target`

Update a target.

### Usage

```shell
akeyless update-target \
--name <Target name> \
--new-name <New target name>
```

### Flags

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`--description[=default_comment]`: Description of the object

`--max-versions`: Maximum number of versions, limited by the account settings defaults

`--delete-protection`: Protection from accidental deletion of this object \[`true`/`false`]
