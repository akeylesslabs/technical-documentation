---
title: CLI Reference - Authentication
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
This section outlines the CLI commands relevant to authentication.

General Flags:

`--profile, --token`:  Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

## `auth`

This command authenticates to Akeyless and saves the temporary token so that it can be used again until the token expires without the need to re-authenticate every time.

##### Usage

`akeyless auth --access-id <access ID> --access-type <accessType>`

with the relevant flags according to the `access-type` being used.

##### Flags

`--access-id`: Access ID

`--access-type[=access_key]`: Access Type (`access_key/password/saml/ldap/k8s/azure_ad/oidc/aws_iam/universal_identity/jwt/gcp/cert/oci`)

`--access-key`: Access key (relevant only for access-type=`access_key`)

`--cloud-id`: The cloud identity (relevant only for access-type=`azure_ad`,`aws_iam`,`gcp`)

`--uid_token`: The universal_identity token (relevant only for access-type=`universal_identity`)

`--jwt`: The JSON Web Token (relevant only for access-type=`jwt`/`oidc`)

`--admin-password`: Password (relevant only for access-type=`password`)

`--admin-email`: Email (relevant only for access-type=`password`)

`--oidc-sp`: OIDC Service Provider (relevant only for access-type=`oidc`, inferred if empty),supported SPs:`google`, `github`

`--ldap_proxy_url`: Address URL for LDAP proxy (relevant only for access-type=`ldap`)

`--username `: LDAP username (relevant only for access-type=`ldap`)

`--password `: LDAP password (relevant only for access-type=`ldap`)

`--gcp-audience[=akeyless.io]`: GCP audience to use in signed JWT (relevant only for access-type=`gcp`)

`--gateway-url`: Gateway URL for the K8S authenticated (relevant only for access-type=`k8s`)

`--k8s-auth-config-name`: The K8s Auth config name (relevant only for access-type=`k8s`)

`--k8s-service-account-token`: The K8S service account token

`--cert-file-name`: Name of the cert file to use (relevant only for access-type=`cert`)

`--cert-data`: Certificate data encoded in base64. Used if file was not provided. (relevant only for access-type=`cert`)

`--key-file-name`: Name of the private key file to use (relevant only for access-type=`cert`)

`--key-data`: Private key data encoded in base64. Used if file was not provided.(relevant only for access-type=`cert`)

`--signed-cert-challenge`: Signed certificate challenge encoded in base64. (relevant only for access-type=`cert`)

`--cert-challenge`: Certificate challenge encoded in base64. (relevant only for access-type=`cert`)

`--oci-auth-type[=apikey]`: The type of the OCI configuration to use [instance/apikey/resource] (relevant only for access-type=oci)

`--oci-group-ocid`: A list of Oracle Cloud IDs groups (relevant only for access-type=oci)

`--use-remote-browser`: Returns a link to complete the authentication remotely (relevant only for `access-type`=`saml/oidc`)

`--debug`: Use this flag for a printout of the authorization `JWT`.

## create

`akeyless auth-method create`

#### Flags

`api-key`  Creates a new API Key Auth method

`aws-iam`  Creates a new AWS IAM Auth method

`azure-ad` Creates a new Azure AD Auth method

`cert` Creates a new Certificate Auth method

`email` Creates a new Email Auth method

`gcp` Creates a new GCP Auth method

`k8s` Creates a new K8s Auth method

`ldap` Creates a new LDAP Auth method

`oauth2` Creates a new Oauth Auth method

`oci` Creates a new Oracle Cloud Auth method

`oidc` Creates a new OIDC Auth method

`saml` Creates a new SAML Auth method

`universal-identity` Creates a new Universal Identity Auth method

### API Key

Create a new [API Key](doc:api-key) Auth Method

##### Usage

```shell
akeyless auth-method create api-key --name <Auth method name>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`:Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`:creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

### `aws-iam`

Create a new Auth Method that will be able to authenticate using AWS IAM credentials

##### Usage

```shell
akeyless auth-method create aws-iam \
--name <Auth method name> \
--bound-aws-account-id <AWS account Id> \
--bound-arn <A list of full arns that the access is restricted to> \
--bound-role-name <A list of full role-name that the access is restricted to> \
--bound-role-id <A list of full role ids that the access is restricted to>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--aws-account-id`: **Required**, A list of AWS account-IDs that the access is restricted to

`--sts-url[=https://sts.amazonaws.com]`: STS URL

`--bound-arn`: A list of full arns that the access is restricted to

`--bound-role-name`: A list of full role-name that the access is restricted to

`--bound-role-id`: A list of full role ids that the access is restricted to

`--bound-resource-id`: A list of full resource ids that the access is restricted to

`--bound-user-name`: A list of full user-name that the access is restricted to

`--bound-user-id`: A list of full user ids that the access is restricted to

`--unique-identifier`: A unique identifier (ID) value which is a `sub claim` name that contains details uniquely identifying that resource. This `sub claim` is used to distinguish between different identities.

### `azure-ad`

Create a new Auth Method that will be able to authenticate using Azure Active Directory credentials

##### Usage

```shell
akeyless auth-method create azure-ad \
--name <Auth method name> \
--bound-tenant-id <Azure tenant id> 
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`-b, --bound-tenant-id`: **Required**, The Azure tenant id that the access is restricted to

`--issuer`: Issuer URL (=`https://sts.windows.net/bound_tenant_id`)

`--jwks-uri`: The URL to the JSON Web Key Set (JWKS) that containing the public keys that should be used to verify any JSON Web Token (JWT) issued by the authorization server (=`[https://login.microsoftonline.com/common/discovery/keys](https://login.microsoftonline.com/common/discovery/keys))

`--audience[=https://management.azure.com/]`: The audience in the JWT

`--bound-spid`: A list of service principal IDs that the access is restricted to

`--bound-group-id`: A list of group ids that the access is restricted to

`--bound-sub-id`: A list of subscription ids that the access is restricted to

`--bound-rg-id`: A list of resource groups that the access is restricted to

`--bound-providers`: A list of resource providers that the access is restricted to (e.g, Microsoft.Compute, Microsoft.ManagedIdentity, etc)

`--bound-resource-types`: A list of resource types that the access is restricted to (e.g, virtualMachines, userAssignedIdentities, etc)

`--bound-resource-names`: A list of resource names that the access is restricted to (e.g, a virtual machine name, scale set name, etc)

`--bound-resource-id`: A list of full resource ids that the access is restricted to

`--unique-identifier`: A unique identifier (ID) value which is a `sub claim` name that contains details uniquely identifying that resource. This `sub claim` is used to distinguish between different identities.

### `cert`

Create a new Auth Method that will be able to authenticate using a client certificate

##### Usage

```shell Shell
akeyless auth-method create cert \
--name <Auth method name> \
--unique-identifier <Unique ID> \
--certificate-file-name </Path/To/File/signing_certificate.pem> 
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false

`--certificate-data`: The certificate data in base64, if no file was provided

`--certificate-file-name`: The path to the file containing the CA certificate

`--bound-common-names`: A list of names. At least one must exist in the Common Name. Supports globbing

`--bound-dns-sans`: A list of DNS names. At least one must exist in the SANs. Supports globbing

`--bound-email-sans`: A list of Email Addresses. At least one must exist in the SANs. Supports globbing

`--bound-uri-sans`: A list of URIs. At least one must exist in the SANs. Supports globbing

`--bound-organizational-units`: A list of Organizational Units names. At least one must exist in the OU field

`--bound-extensions`: A list of extensions formatted as `oid:value`. Expects the extension value to be some type of ASN1 encoded string. All values much match. Supports globbing on `value`

`--revoked-cert-ids`: A list of revoked cert ids

` -u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OIDC, OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

### `email`

Create a new Auth Method that will be able to authenticate using an email address

##### Usage

```shell
akeyless auth-method create email \
--name <Auth mehotd name> \
--email <Email address>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: A comma-separated CIDR block list to allow client access

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--email`: **Required**, An email address to be invited to have access

### `gcp`

Create a new Auth Method that will be able to authenticate using GCP IAM ServiceAccount credentials or GCE instance credentials

##### Usage

```shell
akeyless auth-method create gcp \
--name <Auth method name> \
--type <iamgce> \
--audience <audience to verify in the JWT received by the client> \
--service-account-creds-file </path/to/service account creds.json>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

` --audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`-t, --type`: **Required**, The type of the GCP Auth Method (iam/gce)

`-a, --audience[=akeyless.io]`: **Required**, The audience to verify in the JWT received by the client

`--service-account-creds-file`: Service Account credentials key file path

`--service-account-creds-data`: Service Account credentials data, base64 encoded

`--bound-projects`: A list of GCP project IDs. Clients must belong to any of the provided projects in order to authenticate. For multiple values repeat this flag

`--bound-service-accounts`: A list of Service Accounts. Clients must belong to any of the provided service accounts in order to authenticate. For multiple values repeat this flag

`--bound-zones`: GCE only. A list of zones. GCE instances must belong to any of the provided zones in order to authenticate. For multiple values repeat this flag

`--bound-regions`: GCE only. A list of regions. GCE instances must belong to any of the provided regions in order to authenticate. For multiple values repeat this flag

`--bound-labels`: GCE only. A list of GCP labels formatted as "key:value" pairs that must be set on instances in order to authenticate. For multiple values repeat this flag. If this is added, the `--service-account-creds-file` or `--service-account-creds-data`  becomes mandatory.

`--unique-identifier`: A unique identifier (ID) value which is a `sub claim` name that contains details uniquely identifying that resource. This `sub claim` is used to distinguish between different identities.

### `oauth2`

Create a new Auth Method that will be able to authenticate using OAuth2

##### Usage

```shell
akeyless auth-method create oauth2 \
--name <Auth method name> \
--unique-identifier <unique ID> \
--issuer <issuer URL> \
--audience <The audience in the JWT> \
--jwks-uri <URL to JWKS>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false

`-j, --jwks-uri`: The URL to the JSON Web Key Set (JWKS) that containing the public keys that should be used to verify any JSON Web Token (JWT) issued by the authorization server

`--jwks-json-data`: The JSON Web Key Set (JWKS) that containing the public keys that should be used to verify any JSON Web Token (JWT) issued by the authorization server.  base64 encoded string

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or UPNfor example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

`--bound-clients-ids`: The clients ids that the access is restricted to

`--issuer`: Issuer URL

`--audience`: The audience in the JWT

`--gateway-url`:  Gateway URL `http://<Your-Akeyless-Gateway-URL>:8000`

`-d, --delimiters`: A list of additional sub-claims delimiters"

### `oci`

Create a new Oracle Auth Method that will be used in the account using OCI principle and groups

##### Usage

```shell
akeyless auth-method create oci \
--name <Auth Method name> \
--tenant-ocid <Oracle Cloud tenant ID> \
--group-ocid <required groups ocids>
```

##### Flags

`-n, --name`:  **Required**, Auth Method name

`-t, --tenant-ocid`: **Required**, The Oracle Cloud tenant ID

`-g, --group-oicd`: **Required**, A list of required groups ocids

`--description`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

### `oidc`

Creates a new Authentication Method object that will allow the user to authenticate using OIDC

##### Usage

```shell
akeyless auth-method create oidc \
--name <Auth method name> \
--unique-identifier <Unique ID> \
--issuer <Issuer URL> \
--client-id <Client ID> \
--client-secret <Client Secret>
```

##### Flags

`-n, --name`: **Required**, Auth method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false

`--issuer`: Issuer URL
`--client-id`: Client ID
`--client-secret`: Client Secret
`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OIDC, OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

`--allowed-redirect-uri`: Allowed redirect URIs after the authentication (default is `https://console.akeyless.io/login-oidc` to enable OIDC via Akeyless Console and `http://127.0.0.1:*` to enable OIDC via the Akeyless CLI)

`--require-scopes`: required scopes that the oidc method will request from the oidc provider and the user must approve

`--required-scopes-prefix`: a prefix to add to all required-scopes when requesting them from the oidc server (for example, azures` Application ID URI)

`--audience`: Audience claim to be used as part of the authentication flow. In case set, it must match the one configured on the Identity Provider`s Application

`-d, --delimiters`: A list of additional sub-claims delimiters

### `saml`

Create a new Auth Method that will be able to authenticate using SAML

##### Usage

```shell
akeyless auth-method create saml \
--name <Auth method name> \
--unique-identifier <Unique ID> \
--allowed-redirect-uri <Allowed redirect URIs after the authentication> \
--idp-metadata-url <IDP metadata url>
```

##### Flags

`-n, --name`: **Required**, Auth method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or UPN for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

`--idp-metadata-url`: IDP metadata url

`--allowed-redirect-uri`: Allowed redirect URIs after the authentication (default is `https://console.akeyless.io/login-saml` to enable SAML via Akeyless Console and  `http://127.0.0.1:*` to enable SAML via akeyless CLI)

`--idp-metadata-xml-file-path`: IDP metadata xml file path

`--idp-metadata-xml-data`: IDP metadata as xml encoded in base64

`-d, --delimiters`: A list of additional sub-claims delimiters

## `get-cloud-identity`

Get Cloud Identity Token (relevant only for access-type=`azure_ad`, `aws_iam`, `gcp`, `oci`)

##### Usage

```shell
akeyless get-cloud-identity \
--cloud-provider <azure_ad> \
--azure_ad_object_id <Azure AD ObjectID>
```

##### Flags

`--cloud-provider`: Cloud provider (azure_ad/aws_iam/gcp)

`--azure_ad_object_id`: Azure Active Directory ObjectId (relevant only for access-type=`azure_ad`)

`--gcp-audience[=akeyless.io]`: GCP audience to use in signed JWT (relevant only for access-type=`gcp`)

`--oci-auth-type[=apikey]`: The type of the OCI configuration to use [instance/apikey/resource] (relevant only for access-type=`oci`)

`--describe-sub-claims`: Describe the cloud identity sub-claims

`--oci-group-ocid`: A list of required groups ocids (relevant only for access-type=`oci`)

`--url_safe`: Escapes the token so it can be safely placed inside a URL query"

`--debug[=false]`: Turn on debug logging

## update

Update Auth Method

#### `api-key`

Update a new API Key Auth Method in the account

##### Usage

```shell
akeyless auth-method update api-key --name <Auth method>
```

##### Flags

`--new-name`: Auth Method new name

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

#### `aws-iam`

Update a new Auth Method that will be able to authenticate using AWS IAM credentials

##### Usage

```shell
akeyless auth-method update aws-iam \
--name <Auth method name> \
--bound-aws-account-id <Accessble AWS account`s IDs> \
--new-name <Auth method new name> 
```

#### Flags

`--new-name`: Auth method new name

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`-b, --bound-aws-account-id`: **Required**, A list of AWS account-IDs that the access is restricted to

`--sts-url[=https://sts.amazonaws.com]`: STS URL
`--bound-arn`: A list of full arns that the access is restricted to

`--bound-role-name`: A list of full role-name that the access is restricted to

`--bound-role-id`: A list of full role ids that the access is restricted to

`--bound-resource-id`: A list of full resource ids that the access is restricted to

`--bound-user-name`: A list of full user-name that the access is restricted to

`--bound-user-id`: A list of full user ids that the access is restricted to

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

#### `azure-ad`

Update a new Auth Method that will be able to authenticate using Azure Active Directory credentials

##### Usage

```shell
akeyless auth-method update azure-ad \
--name <Auth method name> \
--bound-tenant-id <Azure tenant id that the access is restricted to> \
--new-name <Auth method new name> 
```

#### Flags

`--new-name`: Auth Method new name

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`-b, --bound-tenant-id`: **Required**, The Azure tenant id that the access is restricted to

`--issuer[=https://sts.windows.net/bound_tenant_id]`: Issuer URL

`--jwks-uri[=https://login.microsoftonline.com/common/discovery/keys]`: The URL to the JSON Web Key Set (JWKS) that containing the public keys that should be used to verify any JSON Web Token (JWT) issued by the authorization server.

`--audience[=https://management.azure.com/]`: The audience in the JWT

`--bound-spid`: A list of service principal IDs that the access is restricted to

`--bound-group-id`: A list of group ids that the access is restricted to

`--bound-sub-id`: A list of subscription ids that the access is restricted to

`--bound-rg-id`: A list of resource groups that the access is restricted to

`--bound-providers`: A list of resource providers that the access is restricted to (e.g, Microsoft.Compute, Microsoft.ManagedIdentity, etc)

`--bound-resource-types`: A list of resource types that the access is restricted to (e.g, virtualMachines, userAssignedIdentities, etc)

`--bound-resource-names`: A list of resource names that the access is restricted to (e.g, a virtual machine name, scale set name, etc).

`--bound-resource-id`: A list of full resource ids that the access is restricted to

#### `cert`

Update a new Auth Method that will be able to authenticate using a client certificate.

##### Usage

```shell
akeyless auth-method update cert \
--name <Auth method name> \
--unique-identifier <Unique ID> \
--new-name <Auth method new name> 
```

#### Flags

`--new-name`: Auth Method new name

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--certificate-data`: The certificate data in base64, if no file was provided.

`--certificate-file-name`: the path to the file containing the CA certificate

`--bound-common-names`: A list of names. At least one must exist in the Common Name. Supports globbing.

`--bound-dns-sans`: A list of DNS names. At least one must exist in the SANs. Supports globbing.

`--bound-email-sans`: A list of Email Addresses. At least one must exist in the SANs. Supports globbing.

`--bound-uri-sans`: A list of URIs. At least one must exist in the SANs. Supports globbing.

`--bound-organizational-units`: A list of Organizational Units names. At least one must exist in the OU field.

`--bound-extensions`: A list of extensions formatted as `oid:value`. Expects the extension value to be some type of ASN1 encoded string. All values much match. Supports globbing on `value`.

`--revoked-cert-ids`: A list of revoked cert ids

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OIDC, OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization.

#### `gcp`

Update a new Auth Method that will be able to authenticate using GCP IAM Service Account credentials or GCE instance credentials

##### Usage

```shell
akeyless auth-method update gcp \
--name <Auth method name> \
--type <GCP type method> \
--audience <The audience to verify in the JWT received by the client> \
--new-name <Auth method new name> 
```

#### Flags

`--new-name`: Auth Method new name

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`-t, --type`: **Required**, The type of the GCP Auth Method (iam/gce)

`-a, --audience[=akeyless.io]`: **Required**, The audience to verify in the JWT received by the client

`--service-account-creds-file`: Service Account creds key file path

`--service-account-creds-data`: Service Account creds data, base64 encoded

`--bound-projects`: A list of GCP project IDs. Clients must belong to any of the provided projects in order to authenticate. For multiple values repeat this flag.

`--bound-service-accounts`: A list of Service Accounts. Clients must belong to any of the provided service accounts in order to authenticate. For multiple values repeat this flag.

`--bound-zones`: GCE only. A list of zones. GCE instances must belong to any of the provided zones in order to authenticate. For multiple values repeat this flag.

`--bound-regions`: GCE only. A list of regions. GCE instances must belong to any of the provided regions in order to authenticate. For multiple values repeat this flag.

`--bound-labels`: GCE only. A list of GCP labels formatted as "key:value" pairs that must be set on instances in order to authenticate. For multiple values repeat this flag. If this is added, the `--service-account-creds-file` or `--service-account-creds-data`  becomes mandatory.

#### `oauth2`

Update a new Auth Method that will be able to authenticate using OAuth2

##### Usage

```shell
akeyless auth-method update oauth2 \
--name <Auth method name> \
--unique-identifier *<Unique ID> \
--jwks-uri <URL to the JSON Web Key Set> 
```

#### Flags

`--new-name`: Auth Method new name

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`-j, --jwks-uri`: The URL to the JSON Web Key Set (JWKS) that containing the public keys that should be used to verify any JSON Web Token (JWT) issued by the authorization server.

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization.

`--bound-clients-ids`: The clients ids that the access is restricted to

`--issuer`: Issuer URL

`--audience`: The audience in the JWT

`--gateway-url`: Gateway URL `http://<Your-Akeyless-Gateway-URL>:8000`

`-d, --delimiters`: A list of additional sub-claims delimiters

#### `oci`

Update an Oracle Auth Method that will be used in the account using OCI principle and groups

##### Usage

```shell
akeyless auth-method update oci \ 
--name <Auth Method name> \
--new-name <Auth Method new name> \
--tenant-ocid <Oracle Cloud tenant ID> \
--group-ocid <required groups ocids>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`-t, --tenant-ocid`: **Required**, The Oracle Cloud tenant ID

`-g, --group-oicd`: **Required**, A list of required groups ocids

`--new-name`: Auth Method new name

`--description`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

#### `oidc`

Update a new Auth Method that will be able to authenticate using OIDC

##### Usage

```shell
akeyless auth-method update oidc \
--name <Auth method name> \
--unique-identifier <Unique ID> \
--new-name <Auth method new name> \
--client-id <Client ID> \
--client-secret <Client Secret>
--issuer <Issuer URL>
```

#### Flags

`--new-name`: Auth Method new name

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity
`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--issuer`: Issuer URL

`--client-id`: Client ID

`--client-secret`: Client Secret

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

`--allowed-redirect-uri`: Allowed redirect URIs after the authentication (default is `https://console.akeyless.io/login-oidc` to enable OIDC via Akeyless Console and `http://127.0.0.1:*` to enable OIDC via akeyless CLI)

`--required-scopes`: required scopes that the oidc method will request from the oidc provider and the user must approve
`--required-scopes-prefix`: a prefix to add to all required-scopes when requesting them from the oidc server (for example, azures` Application ID URI)

`--audience`: Audience claim to be used as part of the authentication flow. In case set, it must match the one configured on the Identity Provider`s Application

`-d, --delimiters`          A list of additional sub-claims delimiters

#### `saml`

Update a new Auth Method that will be able to authenticate using SAML

##### Usage

```shell
akeyless auth-method update saml \
--name <Auth method name> \
--unique-identifier <Unique ID> \
--new-name <Auth method new name> \
--allowed-redirect-uri <Allowed redirect URIs>
```

#### Flags

`--new-name`: Auth Method new name
`-n, --name`: **Required**, Auth Method name
`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)
`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the auth method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization.

`--idp-metadata-url`: IDP metadata url

`--allowed-redirect-uri`: Allowed redirect URIs after the authentication (default is [https://console.akeyless.io/login-saml](https://console.akeyless.io/login-saml) to enable SAML via Akeyless Console and  [http://127.0.0.1:\*](http://127.0.0.1:*) to enable SAML via akeyless CLI)
`--idp-metadata-xml-file-path`: IDP metadata xml file path
`--idp-metadata-xml-data`: IDP metadata as xml encoded in base64

`-d, --delimiters`: A list of additional sub-claims delimiters

## `validate-token`

Checks the provided validating a token, and if valid prints its expiration time (Time-To-Live)validity and its TTL

##### Usage

```shell
akeyless validate-token \
--token <Token to validate>
```

## `revoke-creds`

This command will permanently revoke the credentials associated with the provided token or profile

```shell
akeyless revoke-creds --profile/token <Profile/Token>
```

## get

##### Usage

```shell
akeyless auth-method get -n <Auth method name>
```

## list

##### Usage

```shell
akeyless auth-method list \
--type <Auth method type> \
--filter <Filter by auth method name or part of it>
```

##### Flags

`-t, --type`: The auth method types list of the requested method. In case it is empty, all types of auth method will be returned. options: [api_key, azure_ad, oauth2/jwt, saml2, ldap, aws_iam, oidc, universal_identity, gcp, k8s, cert]

`--filter`: Filter by auth method name or part of it

`--pagination-token`: Next page reference

## delete

Delete an Auth Method

##### Usage

```shell
akeyless auth-method delete -n <Auth method name>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

#### delete-auth-methods

Delete multiple auth methods from a given path

##### Usage

```shell
akeyless delete-auth-methods -p <Path/to/auth-methods>
```

##### Flags

`-p, --path`: **Required**, path to delete the auth methods from

## reset-access-key

Reset an existing access key

```shell
akeyless reset-access-key --name <Auth Method Name>
```

##### Flags

`-n, --name`: **Required**, API Key Auth Method name to reset the access key.
