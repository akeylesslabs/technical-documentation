---
title: CLI Reference - Authentication
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
## Authentication

This section outlines the CLI commands relevant to authentication.

General Flags:

`--profile, --token`:  Use a specific profile (located at $HOME/.akeyless/profiles) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

### `auth`

This command authenticates to Akeyless and saves the temporary token so that it can be used again until the token expires without the need to re-authenticate every time.

##### Flags

`--access-id`: Access ID

`--access-type[=access_key]`: Access Type (`access_key/password/saml/ldap/k8s/azure_ad/oidc/aws_iam/universal_identity/jwt/gcp/cert/oci`)

`--access-key`: Access key (relevant only for access-type=`access_key`)

`--cloud-id`: The cloud identity (relevant only for access-type=`azure_ad`,`aws_iam`,`gcp`)

`--uid-token`: The universal_identity token (relevant only for access-type=`universal_identity`)

`--jwt`: The JSON Web Token (relevant only for access-type=`jwt`/`oidc`)

`--admin-password`: Password (relevant only for access-type=`password`)

`--admin-email`: Email (relevant only for access-type=`password`)

`--oidc-sp`: OIDC Service Provider (relevant only for access-type=`oidc`, inferred if empty),  \nsupported SPs:`google`, `github`

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

`--oci-auth-type[=apikey]`: The type of the OCI configuration to use [instance/apikey/resource] (relevant only for access-type=oci)

`--oci-group-ocid`: A list of Oracle Cloud IDs groups (relevant only for access-type=oci)

`--use-remote-browser`: Returns a link to complete the authentication remotely (relevant only for `access-type`=`saml/oidc`o

`--debug`: Use this flag for a printout of the authorization `JWT`."

### `create-auth-method`

Create a new [API Key](doc:api-key) Auth Method in the current account

##### Usage

```shell
akeyless create-auth-method --name <Auth method name>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`:Access expiration date in Unix timestamp  \n(select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`:creds expiration time in minutes. If not set, use default according to account settings  \n(see get-account-settings)

### `create-auth-method-email`

Create a new Auth Method that will be able to authenticate using an email address

##### Usage

```shell
akeyless create-auth-method-email \
--name <Auth mehotd name> \
--email <Email address>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: A comma-separated CIDR block list to allow client access

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--email`: **Required**, An email address to be invited to have access

### `create-auth-method-azure-ad`

Create a new Auth Method that will be able to authenticate using Azure Active Directory credentials

##### Usage

```shell
akeyless create-auth-method-azure-ad \
--name <Auth method name> \
--bound-tenant-id <Azure tenant id> 
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

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

### `create-auth-method-aws-iam`

Create a new Auth Method that will be able to authenticate using AWS IAM credentials

##### Usage

```shell
akeyless create-auth-method-aws-iam \
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

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--aws-account-id`: **Required**, A list of AWS account-IDs that the access is restricted to

`--sts-url[=https://sts.amazonaws.com]`: STS URL

`--bound-arn`: A list of full arns that the access is restricted to

`--bound-role-name`: A list of full role-name that the access is restricted to

`--bound-role-id`: A list of full role ids that the access is restricted to

`--bound-resource-id`: A list of full resource ids that the access is restricted to

`--bound-user-name`: A list of full user-name that the access is restricted to

`--bound-user-id`: A list of full user ids that the access is restricted to

### `create-auth-method-gcp`

Create a new Auth Method that will be able to authenticate using GCP IAM ServiceAccount credentials or GCE instance credentials

##### Usage

```shell
akeyless create-auth-method-gcp \
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

` --audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`-t, --type`: **Required**, The type of the GCP Auth Method (iam/gce)

`-a, --audience[=akeyless.io]`: **Required**, The audience to verify in the JWT received by the client

`--service-account-creds-file`: Service Account credentials key file path

`--service-account-creds-data`: Service Account credentials data, base64 encoded

`--bound-projects`: A list of GCP project IDs. Clients must belong to any of the provided projects in order to authenticate. For multiple values repeat this flag

`--bound-service-accounts`: A list of Service Accounts. Clients must belong to any of the provided service accounts in order to authenticate. For multiple values repeat this flag

`--bound-zones`: GCE only. A list of zones. GCE instances must belong to any of the provided zones in order to authenticate. For multiple values repeat this flag

`--bound-regions`: GCE only. A list of regions. GCE instances must belong to any of the provided regions in order to authenticate. For multiple values repeat this flag

`--bound-labels`: GCE only. A list of GCP labels formatted as "key:value" pairs that must be set on instances in order to authenticate. For multiple values repeat this flag. If this is added, the `--service-account-creds-file` or `--service-account-creds-data`  becomes mandatory.

### `create-auth-method-oci`

Create a new Oracle Auth Method that will be used in the account using OCI principle and groups

##### Usage

```shell
akeyless create-auth-method-oci \
--name <Auth Method name> \
--tenant-ocid <Oracle Cloud tenant ID> \
--group-ocid <required groups ocids>
```

##### Flags

`-n, --name`:  **Required**, Auth Method name

`-t, --tenant-ocid`: **Required**, The Oracle Cloud tenant ID

`-g, --group-ocid`: **Required**, A list of required groups ocids

`--description`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false

`--force-sub-claims`: enforce role-association must include sub claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [sm, sra, pm, dp, ca]

### `get-cloud-identity`

Get Cloud Identity Token (relevant only for access-type=azure_ad, aws_iam, gcp)

##### Usage

```shell
akeyless get-cloud-identity \
--cloud-provider <azure_ad/aws_iam/gcp> \
--azure_ad_object_id <Azure AD ObjectID>
```

##### Flags

`--cloud-provider`: Cloud provider (azure_ad/aws_iam/gcp)

`--azure_ad_object_id`: Azure Active Directory ObjectId  \n(relevant only for access-type=`azure_ad`)

`--gcp-audience[=akeyless.io]`: GCP audience to use in signed JWT  \n(relevant only for access-type=`gcp`)

`--url_safe`: Escapes the token so it can be safely placed inside a URL query"

### `create-auth-method-oauth2`

Create a new Auth Method that will be able to authenticate using OAuth2

##### Usage

```shell
akeyless create-auth-method-oauth2 \
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

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`-j, --jwks-uri`: The URL to the JSON Web Key Set (JWKS) that containing the public keys that should be used to verify any JSON Web Token (JWT) issued by the authorization server

`--jwks-json-data: The JSON Web Key Set (JWKS) that containing the public keys  \nthat should be used to verify any JSON Web Token (JWT) issued by the authorization server.  base64 encoded string

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or UPNfor example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

`--bound-clients-ids`: The clients ids that the access is restricted to

`--issuer`: Issuer URL

`--audience`: The audience in the JWT

`--gateway-url`: API Gateway URL [http://Your-Akeyless-Gateway-URL:8000](http://Your-Akeyless-Gateway-URL:8000)

`-d, --delimiters`: A list of additional sub-claims delimiters"

### `create-auth-method-saml`

Create a new Auth Method that will be able to authenticate using SAML

##### Usage

```shell
akeyless create-auth-method-saml \
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

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or UPN for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

`--idp-metadata-url`: IDP metadata url

`--allowed-redirect-uri`: Allowed redirect URIs after the authentication (default is [https://console.akeyless.io/login-saml](https://console.akeyless.io/login-saml) to enable SAML via Akeyless Console and  [http://127.0.0.1:\*](http://127.0.0.1:*) to enable SAML via akeyless CLI)

`--idp-metadata-xml-file-path`: IDP metadata xml file path

`--idp-metadata-xml-data`: IDP metadata as xml encoded in base64

`-d, --delimiters`: A list of additional sub-claims delimiters

### `create-auth-method-oidc`

Creates a new Authentication Method object that will allow the user to authenticate using OIDC

##### Usage

```shell
akeyless create-auth-method-oidc \
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

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--issuer`: Issuer URL

`--client-id`: Client ID

`--client-secret`: Client Secret

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OIDC, OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

`--allowed-redirect-uri`: Allowed redirect URIs after the authentication (default is [https://console.akeyless.io/login-oidc](https://console.akeyless.io/login-oidc) to enable OIDC via Akeyless Console and [http://127.0.0.1:\*](http://127.0.0.1:*) to enable OIDC via akeyless CLI)

`--require-scopes`: required scopes that the oidc method will request from the oidc provider and the user must approve

`--required-scopes-prefix`: a prefix to add to all required-scopes when requesting them from the oidc server (for example, azures` Application ID URI)

`--audience`: Audience claim to be used as part of the authentication flow. In case set, it must match the one configured on the Identity Provider`s Application

`-d, --delimiters`: A list of additional sub-claims delimiters

### `create-auth-method-k8s`

Creates a new Authentication Method object that will allow the user to authenticate using Kubernetes

##### Usage

```shell
akeyless create-auth-method-k8s \
--name <Auth method name> \
--public-key-file-path <Path\To\Public\Key> \
--bound-pod-names <list of pods name> \
--bound-namespaces <list of namespaces that the access is restricted to> \
--public-key <Base64-encoded or PEM formatted public key data> \
--audience <The audience in the Kubernetes JWT that the access is restricted to>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`-p, --public-key-file-path`: In case the gen-key  set to false, path to a public key for K8S authentication method is required [RSA2048]

`--public-key`: Base64-encoded or PEM formatted public key data

`--audience`: The audience in the Kubernetes JWT that the access is restricted to

`--bound-sa-names`: A list of service account names that the access is restricted to

`--bound-pod-names`: A list of pod names that the access is restricted to

`--bound-namespaces`: A list of namespaces that the access is restricted to

`--gen-key[=true]`: Automatically generate key-pair for K8S configuration. If set to false, a public key needs to be provided

### `gateway-create-k8s-auth-config`

Creates K8S Auth config

##### Usage

```shell Akeyless CLI
akeyless gateway-create-k8s-auth-config \
--name <k8s-conf name> \
--access-id <Access_ID> \
--gateway-url <API Gateway URL:8000> \
--signing-key <Private_Key> \
--k8s-host <https://Your-K8s-Cluster-IP:8443> \
--token-reviewer-jwt <SA_JWT_TOKEN> \
--k8s-ca-cert <CA_CERT> \
--k8s-issuer <K8S_ISSUER>
```
```shell Rancher
akeyless gateway-create-k8s-auth-config  --name k8s-conf-rancher \
--gateway-url <https://Your-GW-URL>:8000 \
--access-id $ACCESS_ID \
--signing-key $PRV_KEY \
--cluster-api-type rancher \
--k8s-host=<https://Rancher Host>:443 \
--k8s-ca-cert $CA_CERT \
--k8s-issuer $K8S_ISSUER \
--rancher-api-key <API_KEY> \
--rancher-cluster-id <CLUSTER_ID> \
```
```shell Gateway Service Account
akeyless gateway-create-k8s-auth-config  --name k8s-conf \
--gateway-url <API Gateway URL:8000> \
--access-id <Access_ID> \
--signing-key <Private_Key> \
--use-gw-service-account
```

##### Flags

`-n, --name`: **Required**, K8S Auth config name

`--access-id`: **Required**, The Access ID of the Kubernetes auth method

`--signing-key`: The private key (base64 encoded) associated with the public key defined in the Kubernetes auth

`--token-exp[=300]`: Time in seconds of expiration of the Akeyless Kubernetes Auth Method token

`-i, --use-gw-service-account`: Use the GW's service account

`--cluster-api-type[=native_k8s]`: Cluster access type. options: `native_k8s`, `rancher`

` --k8s-host`: The URL of the kubernetes API server

`--k8s-ca-cert`: The CA Certificate (base64 encoded) to use to call into the kubernetes API server

`--k8s-auth-type[=token]`: Native K8S auth type, [token/certificate]. (relevant for "native_k8s" only)

`--k8s-client-certificate`: Content of the k8 client certificate (PEM format) in a Base64 format (relevant for "native_k8s" only)

`--k8s-client-certificate-file`: Path to a file that contain the k8s client certificate in PEM format (relevant for "native_k8s" only)

`--k8s-client-key`: Content of the k8 client private key (PEM format) in a Base64 format (relevant for "native_k8s" only)

`--k8s-client-key-file`: Path to a file that contain the k8s client private key in PEM format (relevant for "native_k8s" only)

`--token-reviewer-jwt`: A Kubernetes service account JWT used to access the TokenReview API to validate other JWTs (relevant for "native_k8s" only)

`--rancher-api-key`: The API Key used to access the TokenReview API to validate other JWTs (relevant for "rancher" only)

`--rancher-cluster-id`: The cluster ID as defined in Rancher (relevant for "rancher" only)

`--k8s-issuer[=kubernetes/serviceaccount]`: The Kubernetes JWT issuer name. If not set, this \<kubernetes/serviceaccount> will be used by default

`--disable-issuer-validation[=true]`: Disable issuer validation `true`/`false`

`--config-encryption-key-name`: Encrypt K8S Auth config with following key

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `gateway-get-k8s-auth-config`

Gets K8S Auth config

##### Usage

```shell
akeyless gateway-get-k8s-auth-config \
--name <K8S Auth config name> \
--gateway-url <API Gateway URL:8000> 
```

##### Flags

`-n, --name`: **Required**, K8S Auth config name
`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `create-auth-method-ldap`

Creates a new Authentication Method object that will allow the user to authenticate using LDAP

##### Usage

```shell
akeyless create-auth-method-ldap \
--name <Auth method name> \
--public-key-file-path <Path\To\Public\Key>
```

##### Flags

`-n, --name`: **Required**, Auth method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`-p, --public-key-file-path`: A path to a public key generated for LDAP authentication method on Akeyless [RSA2048]

`--public-key-data`: A public key generated for LDAP authentication method on Akeyless [RSA2048] in Base64 or PEM format

`--unique-identifier[=users]`: A unique identifier (ID) value should be configured for LDAP, OAuth2 and SAML authentication method types and is usually a value such as the email, username, or UPN for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

`--gen-key[=true]`: Automatically generate key-pair for LDAP configuration. If set to false, a public key needs to be provided

### `gateway-get-ldap-auth-config`

Gets Ldap Auth config

##### Usage

```shell
akeyless gateway-get-ldap-auth-config \
-gateway-url https://<API Gateway URL:8000>
```

##### Flags

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `create-auth-method-universal-identity`

Create a new Auth Method that will be able to authenticate using Akeyless Universal Identity

##### Usage

```shell
akeyless create-auth-method-universal-identity \
--name <Auth method name> \
--ttl <Token TTL> 
```

##### Flags

`-n, --name`: **Required** Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--delete-protection`: Protection from accidental deletion of this object, [true/false

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--deny-rotate`: Deny from the token to rotate

`--deny-inheritance`: Deny from root to create children

`--ttl[=60]`: Token TTL (has the value that configured in Akeyless console > Authentication settings)

### `create-auth-method-cert`

Create a new Auth Method that will be able to authenticate using a client certificate

##### Usage

```shell Shell
akeyless create-auth-method-cert \
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

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

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

### `validate-token`

Checks the provided validating a token, and if valid prints its expiration time (Time-To-Live)validity and its TTL

##### Usage

```shell
akeyless validate-token \
--token <Token to validate>
```

### `revoke-creds`

This command will permanently revoke the credentials associated with the provided token or profile

```shell
akeyless revoke-creds --profile/token <Profile/Token>
```

### `get-auth-method`

Get Auth Method details

##### Usage

```shell
akeyless get-auth-method -n <Auth method name>
```

### `list-auth-methods`

List details of all the Auth Methods in the account

##### Usage

```shell
akeyless list-auth-methods \
--type <Auth method type> \
--filter <Filter by auth method name or part of it>
```

##### Flags

`-t, --type`: The auth method types list of the requested method. In case it is empty, all types of auth method will be returned. options: [api_key, azure_ad, oauth2/jwt, saml2, ldap, aws_iam, oidc, universal_identity, gcp, k8s, cert]

`--filter`: Filter by auth method name or part of it

`--pagination-token`: Next page reference

### `delete-auth-method`

Delete the Auth Method

##### Usage

```shell
akeyless delete-auth-method -n <Auth method name>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

### `delete-auth-methods`

Delete multiple auth methods from a given path

##### Usage

```shell
akeyless delete-auth-methods -p <Path/to/auth-methods>
```

##### Flags

`-p, --path`: **Required**, path to delete the auth methods from

### `gateway-delete-k8s-auth-config`

Deletes K8S Auth config

##### Usage

```shell
akeyless gateway-delete-k8s-auth-config \
--name <Auth config name> \
--gateway-url <API Gateway URL:8000> 
```

##### Flags

`-n, --name`: **Required**, K8S Auth config name

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `update-auth-method`

Update a new API Key Auth Method in the account

##### Usage

```shell
akeyless update-auth-method --name <Auth method>
```

##### Flags

`--new-name`: Auth Method new name

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--force-sub-claims`: enforce role-association must include sub-claims

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

### `gateway-update-k8s-auth-config`

Updates the K8s Auth config

#### Usage

```shell
akeyless gateway-update-k8s-auth-config \
--name <Auth name> \
--access-id <access-id> \
--new-name <config new-name> \
--k8s-host <kubernetes API server URL> 
```

##### Flags

`-n, --name`: **Required**, K8S Auth config name

`--descrpition`: Auth Method description

`--access-id`: **Required**, The access ID of the Kubernetes auth method

`--signing-key`: The private key (base64 encoded) associated with the public key defined in the Kubernetes auth

`--token-exp[=300]`: Time in seconds of expiration of the Akeyless Kubernetes Auth Method token

`-i, --use-gw-service-account`: Use the GW's service account

`--cluster-api-type[=native_k8s]`: Cluster access type. options: [native_k8s, rancher]

`--k8s-host`: The URL of the kubernetes API server

`--k8s-ca-cert`: The CA Certificate (base64 encoded) to use to call into the kubernetes API server

`--k8s-auth-type[=token]`: Native K8S auth type, [token/certificate]. (relevant for "native_k8s" only)

`--k8s-client-certificate`: Content of the k8 client certificate (PEM format) in a Base64 format (relevant for "native_k8s" only)

`--k8s-client-certificate-file`: Path to a file that contain the k8s client certificate in PEM format (relevant for "native_k8s" only)

`--k8s-client-key`: Content of the k8 client private key (PEM format) in a Base64 format (relevant for "native_k8s" only)

`--k8s-client-key-file`: Path to a file that contain the k8s client private key in PEM format (relevant for "native_k8s" only)

`--token-reviewer-jwt`: A Kubernetes service account JWT used to access the TokenReview API to validate other JWTs (relevant for "native_k8s" only)

`--rancher-api-key`: The api key used to access the TokenReview API to validate other JWTs (relevant for "rancher" only)

`--rancher-cluster-id`: The cluster id as define in rancher (relevant for "rancher" only)

`--k8s-issuer=[kubernetes/serviceaccount]`: The Kubernetes JWT issuer name. If not set, this \<kubernetes/serviceaccount> will be used by default.

`--disable-issuer-validation[=true]`: Disable issuer validation `true`/`false`

`--config-encryption-key-name`: Encrypt K8S Auth config with following key

` -u, --gateway-url=[http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--new-name`: **Required**, K8S Auth config new-name

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

### `gateway-update-ldap-auth-config`

Updates LDAP Auth config

##### Usage

```shell
akeyless gateway-update-ldap-auth-config \
--ldap-enable <Enabling ldap authentication> \
--access-id <access ID of the Ldap auth method> \
--signing-key-file-name <path/to/PRV/key> \
--ldap-url <LDAP Server URL> \
--ldap-ca-cert <LDAP CA Certificate (base64 encoded)> 
```

#### Flags

`--ldap-enable`: Enabling ldap authentication

`--access-id`: The access ID of the Ldap auth method

`--signing-key-data`: The private key (base64 encoded), associated with the public key defined in the Ldap auth

`--signing-key-file-name`: the path to the file containing the private key

`--ldap-url`: LDAP Server URL, e.g. ldap://planetexpress.com:389

`-t, --ldap-ca-cert`: LDAP CA Certificate (base64 encoded)

`--ldap-ca-cert-file-name`: the path to the file containing the CA certificate

`--anonymous-search`: Enable LDAP Anonymous Search

`--bind-dn`: LDAP Bind DN

`--bind-dn-password`: Password for LDAP Bind DN

`--user-dn`: User Base DN

`--user-attribute`: LDAP User Attribute

`--group-dn`: Base DN to perform group membership search

`--group-filter`: Go template used when constructing the group membership query. The template can access the following context variables: [UserDN, Username]

`--group-attr`: LDAP attribute to follow on objects returned by ldap_group_filter in order to enumerate user group membership

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

### `update-auth-method-aws-iam`

Update a new Auth Method that will be able to authenticate using AWS IAM credentials

##### Usage

```shell
akeyless update-auth-method-aws-iam \
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

`-b, --bound-aws-account-id`: **Required**, A list of AWS account-IDs that the access is restricted to

`--sts-url[=https://sts.amazonaws.com]`: STS URL
`--bound-arn`: A list of full arns that the access is restricted to

`--bound-role-name`: A list of full role-name that the access is restricted to

`--bound-role-id`: A list of full role ids that the access is restricted to

`--bound-resource-id`: A list of full resource ids that the access is restricted to

`--bound-user-name`: A list of full user-name that the access is restricted to

`--bound-user-id`: A list of full user ids that the access is restricted to

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

### `update-auth-method-azure-ad`

Update a new Auth Method that will be able to authenticate using Azure Active Directory credentials

##### Usage

```shell
akeyless update-auth-method-azure-ad \
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

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

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

### `update-auth-method-cert`

Update a new Auth Method that will be able to authenticate using a client certificate.

##### Usage

```shell
akeyless update-auth-method-cert \
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

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

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

### `update-auth-method-gcp`

Update a new Auth Method that will be able to authenticate using GCP IAM Service Account credentials or GCE instance credentials

##### Usage

```shell
akeyless update-auth-method-gcp \
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

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`-t, --type`: **Required**, The type of the GCP Auth Method (iam/gce)

`-a, --audience[=akeyless.io]`: **Required**, The audience to verify in the JWT received by the client

`--service-account-creds-file`: Service Account creds key file path

`--service-account-creds-data`: Service Account creds data, base64 encoded

`--bound-projects`: A list of GCP project IDs. Clients must belong to any of the provided projects in order to authenticate. For multiple values repeat this flag.

`--bound-service-accounts`: A list of Service Accounts. Clients must belong to any of the provided service accounts in order to authenticate. For multiple values repeat this flag.

`--bound-zones`: GCE only. A list of zones. GCE instances must belong to any of the provided zones in order to authenticate. For multiple values repeat this flag.

`--bound-regions`: GCE only. A list of regions. GCE instances must belong to any of the provided regions in order to authenticate. For multiple values repeat this flag.

`--bound-labels`: GCE only. A list of GCP labels formatted as "key:value" pairs that must be set on instances in order to authenticate. For multiple values repeat this flag. If this is added, the `--service-account-creds-file` or `--service-account-creds-data`  becomes mandatory.

### `update-auth-method-oci`

Update an Oracle Auth Method that will be used in the account using OCI principle and groups

##### Usage

```shell
akeyless update-auth-method-oci \ 
--name <Auth Method name> \
--new-name <Auth Method new name> \
--tenant-ocid <Oracle Cloud tenant ID> \
--group-ocid <required groups ocids>
```

##### Flags

`-n, --name`: **Required**, Auth Method name

`-t, --tenant-ocid`: **Required**, The Oracle Cloud tenant ID

`-g, --group-ocid`: **Required**, A list of required groups ocids

`--new-name`: Auth Method new name

`--description`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub claims

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method [sm, sra, pm, dp, ca]

### `update-auth-method-k8s`

Update a new Auth Method that will be able to authenticate using Kubernetes

##### Usage

```shell
akeyless update-auth-method-k8s \
--name <Auth method name> \
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

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`-p, --public-key-file-path`: In case the gen-key  set to false, path to a public key for K8S authentication method is required [RSA2048]

`--public-key`: Base64-encoded or PEM formatted public key data

`--audience`: The audience in the Kubernetes JWT that the access is restricted to

`--bound-sa-names`: A list of service account names that the access is restricted to

`--bound-pod-names`: A list of pod names that the access is restricted to

`--bound-namespaces`: A list of namespaces that the access is restricted to

`--gen-key`: Automatically generate key-pair for K8S configuration. If set to false, a public key needs to be provided

### `update-auth-method-ldap`

Update a new Auth Method that will be able to authenticate using LDAP

##### Usage

```shell
akeyless update-auth-method-ldap \
--name <Auth method name> \
--new-name <Auth method new name> \
--public-key-file-path <Public/Key/Path> 
```

#### Flags

`--new-name`: Auth Method new name

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`-p, --public-key-file-path`: A path to a public key generated for LDAP authentication method on Akeyless [RSA2048]

`--public-key-data`: A public key generated for LDAP authentication method on Akeyless [RSA2048] in Base64 or PEM format

`--unique-identifier[=users]`: A unique identifier (ID) value should be configured for LDAP, OAuth2 and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization.

`--gen-key`: Automatically generate key-pair for LDAP configuration. If set to false, a public key needs to be provided

### `update-auth-method-oauth2`

Update a new Auth Method that will be able to authenticate using OAuth2

##### Usage

```shell
akeyless update-auth-method-oauth2 \
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

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`-j, --jwks-uri`: The URL to the JSON Web Key Set (JWKS) that containing the public keys that should be used to verify any JSON Web Token (JWT) issued by the authorization server.

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization.

`--bound-clients-ids`: The clients ids that the access is restricted to

`--issuer`: Issuer URL

`--audience`: The audience in the JWT

`--gateway-url`: API Gateway URL [http://Your-Akeyless-Gateway-URL:8000](http://Your-Akeyless-Gateway-URL:8000)

`-d, --delimiters`: A list of additional sub-claims delimiters

### `update-auth-method-oidc`

Update a new Auth Method that will be able to authenticate using OIDC

##### Usage

```shell
akeyless update-auth-method-oidc \
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

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--issuer`: Issuer URL

`--client-id`: Client ID

`--client-secret`: Client Secret

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization

`--allowed-redirect-uri`: Allowed redirect URIs after the authentication (default is [https://console.akeyless.io/login-oidc](https://console.akeyless.io/login-oidc) to enable OIDC via Akeyless Console and [http://127.0.0.1:\*](http://127.0.0.1:*) to enable OIDC via akeyless CLI)

`--required-scopes`: required scopes that the oidc method will request from the oidc provider and the user must approve

`--required-scopes-prefix`: a prefix to add to all required-scopes when requesting them from the oidc server (for example, azures` Application ID URI)

`--audience`: Audience claim to be used as part of the authentication flow. In case set, it must match the one configured on the Identity Provider`s Application

`-d, --delimiters`          A list of additional sub-claims delimiters

### `update-auth-method-saml`

Update a new Auth Method that will be able to authenticate using SAML

##### Usage

```shell
akeyless update-auth-method-saml \
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

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`-u, --unique-identifier`: **Required**, A unique identifier (ID) value should be configured for OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization.

`--idp-metadata-url`: IDP metadata url

`--allowed-redirect-uri`: Allowed redirect URIs after the authentication (default is [https://console.akeyless.io/login-saml](https://console.akeyless.io/login-saml) to enable SAML via Akeyless Console and  [http://127.0.0.1:\*](http://127.0.0.1:*) to enable SAML via akeyless CLI)

`--idp-metadata-xml-file-path`: IDP metadata xml file path

`--idp-metadata-xml-data`: IDP metadata as xml encoded in base64

`-d, --delimiters`: A list of additional sub-claims delimiters

### `update-auth-method-universal-identity`

Update a new Auth Method that will be able to authenticate using Akeyless Universal Identity

##### Usage

```shell
akeyless update-auth-method-universal-identity \
--name <Auth method name> \
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

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--deny-rotate`: Deny from the token to rotate

`--deny-inheritance`: Deny from root to create children

`--ttl[=60]`: Token ttl (in minutes)

### `gateway-get-ldap-auth-config`

Gets Ldap Auth config

##### Usage

```shell
akeyless gateway-get-ldap-auth-config \
--gateway-url <API Gateway URL (Configuration Management port)>
```

#### Flags

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--profile, --token`: Use a specific profile (located at $HOME/.akeyless/profiles) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

## Akeyless Universal Identity

### `uid-list-children`

List the token children ids of Akeyless Universal Identity

##### Usage

```shell
akeyless uid-list-children --auth-method-name <UID Auth Method Name>
```

### `uid-revoke-token`

Revoke token using Akeyless Universal Identity

##### Usage

```shell
akeyless uid-revoke-token \
--revoke-type <revokeSelf/revokeAll> \
--revoke-token <UID Token ID> 
```

##### Flags

`--revoke-type`: **Required**, revokeSelf/revokeAll (delete only this token/this token and his children)

`--revoke-token`: **Required**, the universal identity token/token-id to revoke

`-n, --auth-method-name`: The universal identity auth method name

### `uid-generate-token`

Generate a new token using Akeyless Universal Identity

##### Usage

```shell
akeyless uid-generate-token --auth-method-name <Auth method name>
```

### `uid-rotate-token`

Rotate Akeyless Universal Identity token

##### Flags

`-t, --token, --uid-token`: The Universal identity token to rotate

`--fork`: Create a new child token with default Flags

`--send-manual-ack-token`: The new rotated token to send manual ack for (with uid-token=the-orig-token)

`--with-manual-ack`: Disable automatic ack

`-o, --output-file`: Path to the output file

`-i, --input-file`:          Path to the input file

### `uid-create-child-token`

Create a new child token using Akeyless Universal Identity

##### Usage

```shell
akeyless uid-create-child-token \
--child-deny-rotate \
--child-deny-inheritance
```

##### Flags

`--child-deny-rotate`: Deny from new child to rotate

`--child-deny-inheritance`: Deny from new child to create their own children

`--child-ttl`: New child token TTL

`-n, --auth-method-name`: The universal identity auth method name, required only when uid-token is not provided

`--tid, --uid-token-id`: The ID of the uid-token, required only when uid-token is not provided

`--profile` or `--token`: Use a specific Akeyless profile (located at $HOME/.akeyless/profiles) or a temporary access token

`--uid-token`: The universal identity token. It is required only for universal_identity authentication
