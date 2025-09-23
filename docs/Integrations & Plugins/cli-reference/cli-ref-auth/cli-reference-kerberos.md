---
title: CLI Reference - Kerberos
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
This section outlines the CLI commands relevant to K8s authentication.

General Flags:

`--profile, --token`: Use a specific profile (located at $HOME/.akeyless/profiles) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

### <p style={{ color: "blue" }}>*create*</p>

Creates a new Authentication Method object that will allow the user to authenticate using Kerberos

##### Usage

```shell
akeyless auth-method create kerberos \
--name <Auth method name> \
--krb5conf-file-path path/to/krb5.conf \
--keytab-file-path path/to/keytab \
--ldap-url ldap://ldap.domain.com:389
```

##### Flags

`-n, --name`: Auth Method name

`--description`: Auth Method description

`--access-expires[=0]` Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: Enforce `role-association` must include sub-claims

`--jwt-ttl[=0]`: Creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method \[sm, sra, pm, dp, ca]

`--audit-logs-claims`: Subclaims to include in audit logs. e.g `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, \[true/false]

`-d, --delimiters`: A list of additional sub-claims delimiters (relevant only for SAML, OIDC, OAuth2/JWT). To specify multiple delimiters use the argument multiple times: `-d # -d ^`

`--krb5conf-file-path`: The path to a valid `krb5.conf` file, specifying the settings and parameters required for Kerberos authentication.

`--krb5conf-file-data`: Base64-encoded content of a valid krb5.conf file, specifying the settings and parameters required for Kerberos authentication.

`--keytab-file-path`: The path to a valid keytab file, containing the service account's entry

`--keytab-file-data`: Base64-encoded content of a valid keytab file, containing the service account's entry.

`--ldap-url`: LDAP server URL, e.g., `ldap://ldap.domain.com:389`

`--ldap-ca-cert`: LDAP CA certificate (base64 encoded)

`--ldap-ca-cert-file-name`: Path to the file containing the CA certificate

`--anonymous-search[=false]`: Enable LDAP anonymous search

`--bind-dn`: Full DN of the LDAP user to bind with

`--bind-dn-password`: Password for the LDAP Bind DN

`--user-dn`: The base DN for user searches

`--user-attribute[=sAMAccountName]`: LDAP attribute that maps to the username used for signing in

`--group-dn`: Base DN for group membership searches

`--group-filter`: Go template for constructing the group membership query. The template can access the following context variables: [`UserDN`, `Username`]

`--group-attr`: LDAP attribute to follow on objects returned by `ldap_group_filter` to enumerate user group membership

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

`--unique-identifier`: A unique identifier (ID) value which is a "sub claim" name that contains details uniquely identifying that resource. This "sub claim" is used to distinguish between different identities.

### <p style={{ color: "blue" }}>*update*</p>

Updates an Authentication Method object that will allow the user to authenticate using Kerberos

##### Usage

```shell
akeyless auth-method update kerberos \
--name <Auth method name> \
--new-name <Auth Method new name> \
--krb5conf-file-path path/to/krb5.conf \
--keytab-file-path path/to/keytab \
--ldap-url ldap://ldap.domain.com:389
```

##### Flags

`-n, --name`: Auth Method name

`--new-name`: Auth Method new name

`--description`: Auth Method description

`--access-expires[=0]` Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: Enforce `role-association` must include sub-claims

`--jwt-ttl[=0]`: Creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--product-type`: Choose the relevant product type for the auth method \[sm, sra, pm, dp, ca]

`--audit-logs-claims`: Subclaims to include in audit logs. e.g `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, \[true/false]

`-d, --delimiters`: A list of additional sub-claims delimiters (relevant only for SAML, OIDC, OAuth2/JWT). To specify multiple delimiters use the argument multiple times: `-d # -d ^`

`--krb5conf-file-path`: The path to a valid `krb5.conf` file, specifying the settings and parameters required for Kerberos authentication.

`--krb5conf-file-data`: Base64-encoded content of a valid krb5.conf file, specifying the settings and parameters required for Kerberos authentication.

`--keytab-file-path`: The path to a valid keytab file, containing the service account's entry

`--keytab-file-data`: Base64-encoded content of a valid keytab file, containing the service account's entry.

`--ldap-url`: LDAP server URL, e.g., `ldap://ldap.domain.com:389`

`--ldap-ca-cert`: LDAP CA certificate (base64 encoded)

`--ldap-ca-cert-file-name`: Path to the file containing the CA certificate

`--anonymous-search[=false]`: Enable LDAP anonymous search

`--bind-dn`: Full DN of the LDAP user to bind with

`--bind-dn-password`: Password for the LDAP Bind DN

`--user-dn`: The base DN for user searches

`--user-attribute[=sAMAccountName]`: LDAP attribute that maps to the username used for signing in

`--group-dn`: Base DN for group membership searches

`--group-filter`: Go template for constructing the group membership query. The template can access the following context variables: [`UserDN`, `Username`]

`--group-attr`: LDAP attribute to follow on objects returned by `ldap_group_filter` to enumerate user group membership

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

`--unique-identifier`: A unique identifier (ID) value which is a "sub claim" name that contains details uniquely identifying that resource. This "sub claim" is used to distinguish between different identities.