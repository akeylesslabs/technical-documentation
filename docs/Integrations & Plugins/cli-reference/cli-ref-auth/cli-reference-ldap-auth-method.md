---
title: CLI Reference - LDAP Auth Method
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
This section outlines the CLI commands relevant to LDAP authentication.

General Flags:

`--profile, --token`:  Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

### <p style="color:blue">_create_</p>

Creates a new Authentication Method object that will allow the user to authenticate using LDAP

##### Usage

```shell
akeyless auth-method create ldap \
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

`--delete-protection`: Protection from accidental deletion of this object, \[true/false 

`--force-sub-claims`: enforce role-association must include sub-claims                                     

 `--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)     

 `-p, --public-key-file-path`: A path to a public key generated for LDAP authentication method on Akeyless [RSA2048]               

 `--public-key-data`: A public key generated for LDAP authentication method on Akeyless [RSA2048] in Base64 or PEM format            

 `--unique-identifier[=users]`: A unique identifier (ID) value should be configured for LDAP, OAuth2 and SAML authentication method types and is usually a value such as the email, username, or UPN for example. Whenever a user logs in with a token, these authentication types issue a "sub-claim" that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization 

 `--gen-key[=true]`: Automatically generate key-pair for LDAP configuration. If set to false, a public key needs to be provided                                                    

### <p style="color:blue">_update_</p>

Update a new Auth Method that will be able to authenticate using LDAP

##### Usage

```shell
akeyless update-auth-method-ldap \
--name <Auth method name> \
--new-name <Auth method new name> \
--public-key-file-path <Public/Key/Path> 
```

##### Flags

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

#### <p style="color:blue">_gateway-update-ldap-auth-config_</p>

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

##### Flags

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

### <p style="color:blue">_get_</p>

Gets Ldap Auth config from Gateway

##### Usage

```shell
akeyless gateway-get-ldap-auth-config \
--gateway-url <API Gateway URL (Configuration Management port)>
```

##### Flags

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)                                     

 `--profile, --token`: Use a specific profile (located at $HOME/.akeyless/profiles) or a temp access token 

 `--uid-token`: The universal identity token, Required only for universal_identity authentication