---
title: CLI Reference - Authentication
slug: cli-ref-auth
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

<CLIGeneralFlags />

## `auth`

This command authenticates to Akeyless and saves the temporary token so that it can be used again until the token expires without the need to re-authenticate every time.

### Usage

`akeyless auth --access-id <access ID> --access-type <accessType>`

with the relevant flags according to the `access-type` being used.

#### Flags

`--access-id`: Access ID

`--access-type[=access_key]`: Access Type (`access_key/password/saml/ldap/k8s/azure_ad/oidc/aws_iam/universal_identity/jwt/gcp/cert/oci`)

`--access-key`: Access key (relevant only for `access-type=access_key`)

`--cloud-id`: The cloud identity (relevant only for `access-type=azure_ad`, `aws_iam`, `gcp`)

`--uid_token`: The universal_identity token (relevant only for `access-type=universal_identity`)

`--jwt`: The JSON Web Token (relevant only for `access-type=jwt` and `access-type=oidc`)

`--admin-password`: Password (relevant only for `access-type=password`)

`--admin-email`: Email (relevant only for `access-type=password`)

`--account-id`: Akeyless Account id (relevant only for `access-type=password` where the email address is associated with more than one account)

`--oidc-sp`: OIDC Service Provider (relevant only for `access-type=oidc`, inferred if empty),supported SPs:`google`, `github`

`--ldap_proxy_url`: Address URL for LDAP proxy (relevant only for `access-type=ldap`)

`--username`: LDAP username (relevant only for `access-type=ldap`)

`--password`: LDAP password (relevant only for `access-type=ldap`)

`--gcp-audience[=akeyless.io]`: GCP audience to use in signed JWT (relevant only for `access-type=gcp`)

`--azure-cloud[=AzureCloud]`: Azure cloud environment to use. Values: `AzureCloud` (default), `AzureUSGovernment`, `AzureChinaCloud` (relevant only for `access-type=azure_ad`)

`--gateway-url`: Gateway URL for the Kubernetes authenticated (relevant only for `access-type=k8s`)

`--k8s-auth-config-name`: The Kubernetes Auth config name (relevant only for `access-type=k8s`)

`--k8s-service-account-token`: The Kubernetes service account token

`--cert-file-name`: Name of the cert file to use (relevant only for `access-type=cert`)

`--cert-data`: Certificate data encoded in Base64. Used if file was not provided. (relevant only for `access-type=cert`)

`--key-file-name`: Name of the private key file to use (relevant only for `access-type=cert`)

`--key-data`: Private key data encoded in Base64. Used if file was not provided.(relevant only for `access-type=cert`)

`--signed-cert-challenge`: Signed certificate challenge encoded in Base64. (relevant only for `access-type=cert`)

`--cert-challenge`: Certificate challenge encoded in Base64. (relevant only for `access-type=cert`)

`--oci-auth-type[=apikey]`: The type of the OCI configuration to use `[instance/apikey/resource]` (relevant only for `access-type=oci`)

`--oci-group-ocid`: A list of Oracle Cloud IDs groups (relevant only for `access-type=oci`)

`--use-remote-browser`: Returns a link to complete the authentication remotely (relevant only for `access-type=saml` and `access-type=oidc`)

`--disable-kerberos-fast[=true]`: Disable Kerberos Flexible Authentication via Secure Tunneling (FAST) negotiation

`--gateway-spn`: Optional, the service principal name (SPN) of the gateway as registered in LDAP (for example, `HTTP/gateway`)

`--kerberos-token`: Optional, Kerberos token for the gateway SPN, used by Simple and Protected Negotiation Mechanism (SPNEGO) for authentication

`--kerberos-username`: Optional, the username for the entry within the keytab to authenticate via Kerberos

`--debug`: Use this flag for a printout of the authorization JWT.

## Create

`akeyless auth-method create`

### Flags

`api-key` Creates a new API Key Auth Method

`aws-iam` Creates a new AWS IAM Auth Method

`azure-ad` Creates a new Azure AD Auth Method

`cert` Creates a new Certificate Auth Method

`email` Creates a new Email Auth Method

`gcp` Creates a new GCP Auth Method

`k8s` Creates a new Kubernetes Auth Method

`ldap` Creates a new LDAP Auth Method

`oauth2` Creates a new OAuth Auth Method

`oci` Creates a new Oracle Cloud Auth Method

`oidc` Creates a new OIDC Auth Method

`saml` Creates a new SAML Auth Method

`universal-identity` Creates a new Universal Identity Auth Method

### API Key

Create a new [API Key](https://docs.akeyless.io/docs/auth-with-api-key) Auth Method

#### Usage

```shell
akeyless auth-method create api-key --name <Auth method name>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descriptions`: Auth Method description

`--access-expires[=0]`:Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--allowed-client-type`: limit the Auth Method usage for specific client types [`cli`, `ui`, `gateway-admin`, `sdk`, `mobile`, `extension`]

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

### `aws-iam`

Create a new Auth Method that can authenticate using AWS IAM credentials

#### Usage

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

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--allowed-client-type`: limit the Auth Method usage for specific client types [`cli`, `ui`, `gateway-admin`, `sdk`, `mobile`, `extension`]

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--aws-account-id`: **Required**, A list of AWS account-IDs that the access is restricted to

`--sts-url[=https://sts.amazonaws.com]`: STS URL. For `aws-us-gov`, use a regional endpoint such as `https://sts.us-gov-west-1.amazonaws.com` or `https://sts.us-gov-east-1.amazonaws.com`. For `aws-cn`, use a regional endpoint such as `https://sts.cn-north-1.amazonaws.com.cn` or `https://sts.cn-northwest-1.amazonaws.com.cn`.

`--bound-arn`: A list of full arns that the access is restricted to. Use the ARN partition prefix that matches your environment (for example, `arn:aws:...`, `arn:aws-us-gov:...`, or `arn:aws-cn:...`).

For partition support and endpoint examples, see [AWS Partition and Deployment Support](https://docs.akeyless.io/docs/aws-partition-and-deployment-support#aws-partition-support).

`--bound-role-name`: A list of full role-name that the access is restricted to

`--bound-role-id`: A list of full role ids that the access is restricted to

`--bound-resource-id`: A list of full resource ids that the access is restricted to

`--bound-user-name`: A list of full user-name that the access is restricted to

`--bound-user-id`: A list of full user ids that the access is restricted to

`--unique-identifier`: A unique identifier (ID) value which is a `sub claim` name that contains details uniquely identifying that resource. This `sub claim` is used to distinguish between different identities.

### `azure-ad`

Create a new Auth Method that can authenticate using Azure Active Directory credentials

#### Usage

```shell
akeyless auth-method create azure-ad \
--name <Auth method name> \
--bound-tenant-id <Azure tenant id> 
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--allowed-client-type`: limit the Auth Method usage for specific client types [`cli`, `ui`, `gateway-admin`, `sdk`, `mobile`, `extension`]

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`-b, --bound-tenant-id`: **Required**, The Azure tenant ID that the access is restricted to

`--issuer`: Issuer URL (=`https://sts.windows.net/bound_tenant_id`)

`--jwks-uri`: The URL to the JSON Web Key Set (JWKS) that containing the public keys that should be used to verify any JSON Web Token (JWT) issued by the authorization server (=`[https://login.microsoftonline.com/common/discovery/keys](https://login.microsoftonline.com/common/discovery/keys))

`--audience[=https://management.azure.com/]`: The audience in the JWT

`--bound-spid`: A list of service principal IDs that the access is restricted to

`--bound-group-id`: A list of group ids that the access is restricted to

`--bound-sub-id`: A list of subscription ids that the access is restricted to

`--bound-rg-id`: A list of resource groups that the access is restricted to

`--bound-providers`: A list of resource providers that the access is restricted to (For example, Microsoft.Compute, Microsoft.ManagedIdentity, and so on)

`--bound-resource-types`: A list of resource types that the access is restricted to (For example, virtualMachines, userAssignedIdentities, and so on)

`--bound-resource-names`: A list of resource names that the access is restricted to (For example, a virtual machine name, scale set name, and so on)

`--bound-resource-id`: A list of full resource ids that the access is restricted to

`--unique-identifier`: A unique identifier (ID) value which is a `sub claim` name that contains details uniquely identifying that resource. This `sub claim` is used to distinguish between different identities.

### `cert`

Create a new Auth Method that can authenticate using a client certificate

#### Usage

```shell
akeyless auth-method create cert \
--name <Auth method name> \
--unique-identifier <Unique ID> \
--certificate-file-name </Path/To/File/signing_certificate.pem> 
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--allowed-client-type`: limit the Auth Method usage for specific client types [`cli`, `ui`, `gateway-admin`, `sdk`, `mobile`, `extension`]

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--certificate-data`: The certificate data in Base64, if no file was provided

`--certificate-file-name`: The path to the file containing the CA certificate

`--bound-common-names`: A list of names. At least one must exist in the Common Name. Supports globbing

`--bound-dns-sans`: A list of DNS names. At least one must exist in the SANs. Supports globbing

`--bound-email-sans`: A list of Email Addresses. At least one must exist in the SANs. Supports globbing

`--bound-uri-sans`: A list of URIs. At least one must exist in the SANs. Supports globbing

`--bound-organizational-units`: A list of Organizational Units names. At least one must exist in the OU field

`--bound-extensions`: A list of extensions formatted as `oid:value`. Expects the extension value to be some type of ASN1 encoded string. All values much match. Supports globbing on `value`

`--revoked-cert-ids`: A list of revoked cert ids

`--allowed-cors`: Comma-separated list of allowed Cross-Origin Resource Sharing (CORS) domains to be validated as part of the authentication flow

`--require-crl-dp`: Require certificate CRL distribution points (CDP) and enforce CRL validation during authentication

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OIDC, OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

### `email`

Create a new Auth Method that can authenticate using an email address

#### Usage

```shell
akeyless auth-method create email \
--name <Auth mehotd name> \
--email <Email address>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descriptions`: Auth Method description

`--access-expires[=0]`: A comma-separated CIDR block list to allow client access

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--allowed-client-type`: limit the Auth Method usage for specific client types [`cli`, `ui`, `gateway-admin`, `sdk`, `mobile`, `extension`]

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--email`: **Required**, An email address to be invited to have access

### `gcp`

Create a new Auth Method that can authenticate using GCP IAM ServiceAccount credentials or GCE instance credentials

#### Usage

```shell
akeyless auth-method create gcp \
--name <Auth method name> \
--type <iamgce> \
--audience <audience to verify in the JWT received by the client> \
--service-account-creds-file </path/to/service account creds.json>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--allowed-client-type`: limit the Auth Method usage for specific client types [`cli`, `ui`, `gateway-admin`, `sdk`, `mobile`, `extension`]

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`-t, --type`: **Required**, The type of the GCP Auth Method (IAM/GCE)

`-a, --audience[=akeyless.io]`: **Required**, The audience to verify in the JWT received by the client

`--service-account-creds-file`: Service Account credentials key file path

`--service-account-creds-data`: Service Account credentials data, Base64-encoded

`--bound-projects`: A list of GCP project IDs. Clients must belong to any of the provided projects to authenticate. For multiple values repeat this flag

`--bound-service-accounts`: A list of Service Accounts. Clients must belong to any of the provided service accounts to authenticate. For multiple values repeat this flag

`--bound-zones`: GCE only. A list of zones. GCE instances must belong to any of the provided zones to authenticate. For multiple values repeat this flag

`--bound-regions`: GCE only. A list of regions. GCE instances must belong to any of the provided regions to authenticate. For multiple values repeat this flag

`--bound-labels`: GCE only. A list of GCP labels formatted as "key:value" pairs that must be set on instances to authenticate. For multiple values repeat this flag. If this is added, the `--service-account-creds-file` or `--service-account-creds-data` becomes mandatory.

`--unique-identifier`: A unique identifier (ID) value which is a `sub claim` name that contains details uniquely identifying that resource. This `sub claim` is used to distinguish between different identities.

### `oauth2`

Create a new Auth Method that can authenticate using OAuth2

#### Usage

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

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`-j, --jwks-uri`: The URL to the JSON Web Key Set (JWKS) that containing the public keys that should be used to verify any JSON Web Token (JWT) issued by the authorization server

`--jwks-json-data`: The JSON Web Key Set (JWKS) that containing the public keys that should be used to verify any JSON Web Token (JWT) issued by the authorization server. Base64-encoded string

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or UPN for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

`--bound-clients-ids`: The clients ids that the access is restricted to

`--issuer`: Issuer URL

`--audience`: The audience in the JWT

`--gateway-url`: Gateway URL `http://<Your-Akeyless-Gateway-URL>:8000`

`--jwks-json-file`: The JSON Web Key Set (`JWKS`) JSON file path that will be used to verify any JSON Web Token (`JWT`) issued by the authorization server

`-d, --delimiters`: A list of additional sub-claims delimiters"

### `oci`

Create a new Oracle Auth Method that will be used in the account using OCI principle and groups

#### Usage

```shell
akeyless auth-method create oci \
--name <Auth Method name> \
--tenant-ocid <Oracle Cloud tenant ID> \
--group-ocid <required groups OCIDs>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`-t, --tenant-ocid`: **Required**, The Oracle Cloud tenant ID

`-g, --group-ocid`: **Required**, A list of required groups OCIDs

`--description`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--allowed-client-type`: limit the Auth Method usage for specific client types [`cli`, `ui`, `gateway-admin`, `sdk`, `mobile`, `extension`]

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

### `oidc`

Creates a new Authentication Method object that will allow the user to authenticate using OIDC

#### Usage

```shell
akeyless auth-method create oidc \
--name <Auth method name> \
--unique-identifier <Unique ID> \
--issuer <Issuer URL> \
--client-id <Client ID> \
--client-secret <Client Secret>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--allowed-client-type`: limit the Auth Method usage for specific client types [`cli`, `ui`, `gateway-admin`, `sdk`, `mobile`, `extension`]

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--issuer`: Issuer URL
`--client-id`: Client ID
`--client-secret`: Client Secret
`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OIDC, OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

`--allowed-redirect-uri`: Allowed redirect URIs after the authentication (default is `https://console.akeyless.io/login-oidc` to enable OIDC by way of Akeyless Console and `http://127.0.0.1:*` to enable OIDC by way of the Akeyless CLI)

`--require-scopes`: required scopes that the OIDC method will request from the OIDC Provider and the user must approve

`--required-scopes-prefix`: a prefix to add to all required-scopes when requesting them from the OIDC server (for example, Azure's Application ID URI)

`--audience`: Audience claim to be used as part of the authentication flow. If set, it must match the one configured on the Identity Provider's Application

`-d, --delimiters`: A list of additional sub-claims delimiters

### `saml`

Create a new Auth Method that can authenticate using SAML

#### Usage

```shell
akeyless auth-method create saml \
--name <Auth method name> \
--unique-identifier <Unique ID> \
--allowed-redirect-uri <Allowed redirect URIs after the authentication> \
--idp-metadata-url <IDP metadata url>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--allowed-client-type`: limit the Auth Method usage for specific client types [`cli`, `ui`, `gateway-admin`, `sdk`, `mobile`, `extension`]

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or UPN for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

`--idp-metadata-url`: IdP metadata URL

`--allowed-redirect-uri`: Allowed redirect URIs after the authentication (default is `https://console.akeyless.io/login-saml` to enable SAML by way of Akeyless Console and `http://127.0.0.1:*` to enable SAML by way of the Akeyless CLI)

`--idp-metadata-xml-file-path`: IdP metadata XML file path

`--idp-metadata-xml-data`: IdP metadata as XML encoded in Base64

`-d, --delimiters`: A list of additional sub-claims delimiters

## `get-cloud-identity`

Get Cloud Identity Token (relevant only for access-type=`azure_ad`, `aws_iam`, `gcp`, `oci`)

### Usage

```shell
akeyless get-cloud-identity \
--cloud-provider <azure_ad> \
--azure_ad_object_id <Azure AD ObjectID>
```

#### Flags

`--cloud-provider`: Cloud provider (`azure_ad`/`aws_iam`/`gcp`)

`--azure_ad_object_id`: Azure Active Directory ObjectId (relevant only for `access-type=azure_ad`)

`--azure-cloud[=AzureCloud]`: Azure cloud environment to use. Values: `AzureCloud` (default), `AzureUSGovernment`, `AzureChinaCloud` (relevant only for `access-type=azure_ad`)

`--gcp-audience[=akeyless.io]`: GCP audience to use in signed JWT (relevant only for `access-type=gcp`)

`--oci-auth-type[=apikey]`: The type of the OCI configuration to use `[instance/apikey/resource]` (relevant only for `access-type=oci`)

`--describe-sub-claims`: Describe the cloud identity sub-claims

`--oci-group-ocid`: A list of required groups OCIDs (relevant only for `access-type=oci`)

`--url_safe`: Escapes the token so it can be safely placed inside a URL query

`--debug[=false]`: Turn on debug logging

## Update

Update Auth Method

### `api-key`

Update a new API Key Auth Method in the account

#### Usage

```shell
akeyless auth-method update api-key --name <Auth method>
```

##### Flags

`--new-name`: Auth Method new name

`-n, --name`: **Required**, Auth Method name

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

#### `aws-iam`

Update a new Auth Method that can authenticate using AWS IAM credentials

##### Usage

```shell
akeyless auth-method update aws-iam \
--name <Auth method name> \
--bound-aws-account-id <Accessible AWS account IDs> \
--new-name <Auth method new name> 
```

#### Flags

`--new-name`: Auth Method new name

`-n, --name`: **Required**, Auth Method name

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`-b, --bound-aws-account-id`: **Required**, A list of AWS account-IDs that the access is restricted to

`--sts-url[=https://sts.amazonaws.com]`: STS URL. For `aws-us-gov`, use a regional endpoint such as `https://sts.us-gov-west-1.amazonaws.com` or `https://sts.us-gov-east-1.amazonaws.com`. For `aws-cn`, use a regional endpoint such as `https://sts.cn-north-1.amazonaws.com.cn` or `https://sts.cn-northwest-1.amazonaws.com.cn`.

`--bound-arn`: A list of full arns that the access is restricted to. Use the ARN partition prefix that matches your environment (for example, `arn:aws:...`, `arn:aws-us-gov:...`, or `arn:aws-cn:...`).

For partition support and endpoint examples, see [AWS Partition and Deployment Support](https://docs.akeyless.io/docs/aws-partition-and-deployment-support#aws-partition-support).

`--bound-role-name`: A list of full role-name that the access is restricted to

`--bound-role-id`: A list of full role ids that the access is restricted to

`--bound-resource-id`: A list of full resource ids that the access is restricted to

`--bound-user-name`: A list of full user-name that the access is restricted to

`--bound-user-id`: A list of full user ids that the access is restricted to

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

#### `azure-ad`

Update a new Auth Method that can authenticate using Azure Active Directory credentials

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

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`-b, --bound-tenant-id`: **Required**, The Azure tenant ID that the access is restricted to

`--issuer[=https://sts.windows.net/bound_tenant_id]`: Issuer URL

`--jwks-uri[=https://login.microsoftonline.com/common/discovery/keys]`: The URL to the JSON Web Key Set (JWKS) that containing the public keys that should be used to verify any JSON Web Token (JWT) issued by the authorization server.

`--audience[=https://management.azure.com/]`: The audience in the JWT

`--bound-spid`: A list of service principal IDs that the access is restricted to

`--bound-group-id`: A list of group ids that the access is restricted to

`--bound-sub-id`: A list of subscription ids that the access is restricted to

`--bound-rg-id`: A list of resource groups that the access is restricted to

`--bound-providers`: A list of resource providers that the access is restricted to (For example, Microsoft.Compute, Microsoft.ManagedIdentity, and so on)

`--bound-resource-types`: A list of resource types that the access is restricted to (For example, virtualMachines, userAssignedIdentities, and so on)

`--bound-resource-names`: A list of resource names that the access is restricted to (For example, a virtual machine name, scale set name, and so on).

`--bound-resource-id`: A list of full resource ids that the access is restricted to

#### `cert`

Update a new Auth Method that can authenticate using a client certificate.

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

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--certificate-data`: The certificate data in Base64, if no file was provided.

`--certificate-file-name`: the path to the file containing the CA certificate

`--bound-common-names`: A list of names. At least one must exist in the Common Name. Supports globbing.

`--bound-dns-sans`: A list of DNS names. At least one must exist in the SANs. Supports globbing.

`--bound-email-sans`: A list of Email Addresses. At least one must exist in the SANs. Supports globbing.

`--bound-uri-sans`: A list of URIs. At least one must exist in the SANs. Supports globbing.

`--bound-organizational-units`: A list of Organizational Units names. At least one must exist in the OU field.

`--bound-extensions`: A list of extensions formatted as `oid:value`. Expects the extension value to be some type of ASN1 encoded string. All values much match. Supports globbing on `value`.

`--revoked-cert-ids`: A list of revoked cert ids

`--allowed-cors`: Comma-separated list of allowed Cross-Origin Resource Sharing (CORS) domains to be validated as part of the authentication flow

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OIDC, OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization.

#### `email`

Update an existing Email Auth Method in the account

##### Usage

```shell
akeyless auth-method update email \
--name <Auth method name> \
--new-name <Auth method new name>
```

#### Flags

`--new-name`: Auth Method new name

`-n, --name`: **Required**, Auth Method name

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--enable-mfa`: Enable MFA for this authentication method [true/false]

`--mfa-type[=email]`: Enable two-factor authentication via [email/app]

#### `gcp`

Update a new Auth Method that can authenticate using GCP IAM Service Account credentials or GCE instance credentials

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

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`-t, --type`: **Required**, The type of the GCP Auth Method (`iam`/`gce`)

`-a, --audience[=akeyless.io]`: **Required**, The audience to verify in the JWT received by the client

`--service-account-creds-file`: Service Account credentials key file path

`--service-account-creds-data`: Service Account credentials data, Base64-encoded

`--bound-projects`: A list of GCP project IDs. Clients must belong to any of the provided projects to authenticate. For multiple values repeat this flag.

`--bound-service-accounts`: A list of Service Accounts. Clients must belong to any of the provided service accounts to authenticate. For multiple values repeat this flag.

`--bound-zones`: GCE only. A list of zones. GCE instances must belong to any of the provided zones to authenticate. For multiple values repeat this flag.

`--bound-regions`: GCE only. A list of regions. GCE instances must belong to any of the provided regions to authenticate. For multiple values repeat this flag.

`--bound-labels`: GCE only. A list of GCP labels formatted as "key:value" pairs that must be set on instances to authenticate. For multiple values repeat this flag. If this is added, the `--service-account-creds-file` or `--service-account-creds-data` becomes mandatory.

#### `oauth2`

Update a new Auth Method that can authenticate using OAuth2

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

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`-j, --jwks-uri`: The URL to the JSON Web Key Set (JWKS) that containing the public keys that should be used to verify any JSON Web Token (JWT) issued by the authorization server.

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization.

`--bound-clients-ids`: The clients ids that the access is restricted to

`--issuer`: Issuer URL

`--audience`: The audience in the JWT

`--gateway-url`: Gateway URL `http://<Your-Akeyless-Gateway-URL>:8000`

`--jwks-json-file`: The JSON Web Key Set (`JWKS`) JSON file path that will be used to verify any JSON Web Token (`JWT`) issued by the authorization server

`-d, --delimiters`: A list of additional sub-claims delimiters

#### `oci`

Update an Oracle Auth Method that will be used in the account using OCI principle and groups

##### Usage

```shell
akeyless auth-method update oci \
--name <Auth Method name> \
--new-name <Auth Method new name> \
--tenant-ocid <Oracle Cloud tenant ID> \
--group-ocid <required groups OCIDs>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`-t, --tenant-ocid`: **Required**, The Oracle Cloud tenant ID

`-g, --group-ocid`: **Required**, A list of required groups OCIDs

`--new-name`: Auth Method new name

`--description`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

#### `oidc`

Update a new Auth Method that can authenticate using OIDC

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

`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity
`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--issuer`: Issuer URL

`--client-id`: Client ID

`--client-secret`: Client Secret

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

`--allowed-redirect-uri`: Allowed redirect URIs after the authentication (default is `https://console.akeyless.io/login-oidc` to enable OIDC by way of Akeyless Console and `http://127.0.0.1:*` to enable OIDC by way of the Akeyless CLI)

`--required-scopes`: required scopes that the OIDC method will request from the OIDC Provider and the user must approve
`--required-scopes-prefix`: a prefix to add to all required-scopes when requesting them from the OIDC server (for example, Azure's Application ID URI)

`--audience`: Audience claim to be used as part of the authentication flow. If set, it must match the one configured on the Identity Provider's Application

`-d, --delimiters`          A list of additional sub-claims delimiters

#### `saml`

Update a new Auth Method that can authenticate using SAML

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
`--descriptions`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)
`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: Credentials expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the Auth Method [`sm`, `sra`, `pm`, `dp`, `ca`]

`--audit-logs-claims`: Additional sub-claims to include in Audit Logs. For example, `--audit-logs-claims email --audit-logs-claims username`

`--expiration-event-in`: How many days before the Auth Method expires would you like to be notified. To specify multiple events, use the argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`, Relevant only when `access-expires` option is set.

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization.

`--idp-metadata-url`: IdP metadata URL

`--allowed-redirect-uri`: Allowed redirect URIs after the authentication (default is `https://console.akeyless.io/login-saml` to enable SAML by way of Akeyless Console and `http://127.0.0.1:*` to enable SAML by way of the Akeyless CLI)

`--idp-metadata-xml-file-path`: IdP metadata XML file path

`--idp-metadata-xml-data`: IdP metadata as XML encoded in Base64

`-d, --delimiters`: A list of additional sub-claims delimiters

## `validate-token`

Validates the provided token and, if valid, prints its expiration time (Time-To-Live).

### Usage

```shell
akeyless validate-token \
--token <Token to validate>
```

## `revoke-creds`

This command will permanently revoke the credentials associated with the provided token or profile

```shell
akeyless revoke-creds --profile/token <Profile/Token>
```

## Get

### Usage

```shell
akeyless auth-method get -n <Auth method name>
```

## List

### Usage

```shell
akeyless auth-method list \
--type <Auth method type> \
--filter <Filter by auth method name or part of it>
```

#### Flags

`-t, --type`: The Auth Method types list of the requested method. If it is empty, all Auth Method types are returned. options: [`api_key`, `azure_ad`, `oauth2/jwt`, `saml2`, `ldap`, `aws_iam`, `oidc`, `universal_identity`, `gcp`, `k8s`, `cert`]

`--filter`: Filter by Auth Method name or part of it

`--pagination-token`: Next page reference

## Delete

Delete an Auth Method

### Usage

```shell
akeyless auth-method delete -n <Auth method name>
```

#### Flags

`-n, --name`: **Required**, Auth Method name

#### Delete-auth-methods

Delete multiple auth methods from a given path

##### Usage

```shell
akeyless delete-auth-methods -p <Path/to/auth-methods>
```

##### Flags

`-p, --path`: **Required**, path to delete the auth methods from

## Reset-access-key

Reset an existing access key

```shell
akeyless reset-access-key --name <Auth Method Name>
```

### Flags

`-n, --name`: **Required**, API Key Auth Method name to reset the access key.
