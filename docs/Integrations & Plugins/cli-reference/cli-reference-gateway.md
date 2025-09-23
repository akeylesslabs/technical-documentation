---
title: CLI Reference - Gateway
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
This section outlines the CLI commands relevant to the Gateway.

General Flags:

`--profile, --token`:  Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal\_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

## Access Permissions

Commands for managing the access of users to your Gateway.

### <p style="color:blue">*add-gw-access-id*</p>

Grants Gateway access to users

##### Usage

```shell
akeyless add-gw-access-id \
--cluster-name <Cluster Name> \
--access-id <AccessID> \
--sub-claims <group=admins>
```

##### Flags

 `-c, --cluster-name`: **Required**,  The name of the updated cluster                                     

 `-a, --access-id`: **Required**,  The `Access ID` to be able to access the gateway                      

 `-s, --sub-claims`: `key/val` of sub-claims, e.g `group=admins,developers`

### <p style="color:blue">*create-allowed-access*</p>

Add users that will have permission to manage the Gateway 

##### Usage

```shell
akeyless gateway-create-allowed-access \
--name <Allowed Access Name> \
--access-id <Access-ID> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--description <Allowed Access description> \
--sub-claims <key/val of sub claims> \
--permissions <permissions for this allowed access> 
```

##### Flags

 `-n, --name`: **Required**,  Allowed access name                                                                                                                                                                                                                                           

 `--access-id`: **Required**,  The `Access ID` to be attached to this allowed access                                                                                                                                                                                                           

 `--description`: Allowed access description                                                                                                                                                                                                                                                    

 `-s, --sub-claims`: `key/val` of sub-claims, e.g `group=admins,developers`                                                                                                                                                                                                                            

 `-p, --permissions`: Comma-separated list of permissions for this allowed access. Available permissions: \[\`defaults\`,\`targets\`,\`classic\_keys\`,\`automatic\_migration\`,\`ldap\_auth\`,\`dynamic\_secret\`,\`k8s\_auth\`,\`log\_forwarding\`,\`zero\_knowledge\_encryption\`,\`rotated\_secret\`,\`caching,event\_forwarding\`,\`admin\`,\`kmip\`,\`general\`, \`rotate\_secret\_value\`] 

 `-c, --case-sensitive[=true]`: Treat sub-claims as case-sensitive                                                                                                                                                                                                                                            

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### <p style="color:blue">*update-allowed-access*</p>

Set users that will have permission to manage the Gateway

##### Usage

```shell
akeyless gateway-update-allowed-access \
--name <Allowed Access Name> \
--access-id <Access-ID> \
--new-name <New allowed access name> \
--gateway-url <API Gateway URL:8000> \
--description <Allowed Access description> \
--sub-claims <key/val of sub claims> \
--permissions <permissions for this allowed access> 
```

##### Flags

 `-n, --name`: **Required**,  Allowed access name                                                                                                                                                                                                                                           

 `--access-id`: **Required**,  The `Access ID` to be attached to this allowed access                                                                                                                                                                                                           

 `--new-name`: New allowed access name                                                                                                                                                                                                                                                       

 `--description`: Allowed access description                                                                                                                                                                                                                                                    

 `-s, --sub-claims`: `key/val` of sub claims, e.g `group=admins,developers`                                                                                                                                                                                                                            

 `-p, --permissions`: Comma-seperated list of permissions for this allowed access. Available permissions: \[\`defaults\`,\`targets\`,\`classic\_keys\`,\`automatic\_migration\`,\`ldap\_auth\`,\`dynamic\_secret\`,\`k8s\_auth\`,\`log\_forwarding\`,\`zero\_knowledge\_encryption\`,\`rotated\_secret\`,\`caching\`,\`event\_forwarding\`,\`admin\`,\`kmip\`,\`general\`] 

 `-c, --case-sensitive[=true]`: Treat sub claims as case-sensitive                                                                                                                                                                                                                                            

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### <p style="color:blue">*delete-gw-access-id*</p>

Denials Gateway access to users

##### Usage

```shell
akeyless delete-gw-access-id \
--cluster-name <Cluster Name> \
--access-id <Access ID>
```

##### Flags

`-c, --cluster-name`: **Required**, The name of the updated cluster                                     

 `-a, --access-id`: **Required**, The `Access ID` to be able to access the gateway

## Gateway Configuration

### <p style="color:blue">*delete-gateway-cluster*</p>

Deletes a gateway in the account

##### Usage

```shell
akeyless delete-gateway-cluster \
--cluster-name <Cluster Name> \
--force < true / flase>
```

##### Flags

 `-c, --cluster-name`: **Required**,  Gateway Cluster, e.g. `acc-abcd12345678/p-123456789012/defaultCluster`

 `--force`: Deletes cluster even if there is an active gateway or associated secrets. All Gateway secrets will be deleted

### <p style="color:blue">*get-config*</p>

Gets gateway configuration details

##### Usage

```shell
akeyless gateway-get-config \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

### <p style="color:blue">*update-tls-cert*</p>

Updates TLS certificate in the Gateway

```shell
akeyless gateway-update-tls-cert \
--cert-data <TLS Certificate> \
--cert-file-name <Path/To/Certificate> \
--key-data <TLS Private Key> \
--key-file-name <Path/To/Key> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

##### Flags

 `--cert-data`: TLS Certificate (base64 encoded), this flag is ignored if `--cert-file-name` is supplied          

 `--cert-file-name`: Path to the file containing the TLS Certificate, this flag is ignored if `--cert-data` is supplied 

 `--key-data`: TLS Private Key (base64 encoded), this flag is ignored if `--key-file-name` is supplied            

 ` --key-file-name`: Path to the file containing the TLS Private Key, this flag is ignored if `--key-data` is supplied  

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

## <p style="color:blue">*get*</p>

`akeyless gateway get`

Command to get specified gateway configuration

**Flags**

`cache`

`defaults`

### <p style="color:blue">*cache*</p>

Get cache settings

##### Usage

```shell
akeyless gateway get cache \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

### <p style="color:blue">*defaults*</p>

Get defaults settings

##### Usage

```shell
akeyless gateway get defaults \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

## <p style="color:blue">*list*</p>

`akeyless gateway list customer-fragments`

Command to list the Customer Fragments on the Gateway

##### Usage

```shell
akeyless gateway list customer-fragments \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

## <p style="color:blue">*update*</p>

`akeyless gateway update`

Command to update specified gateway configuration

**Flags**

`cache`

`defaults`

### <p style="color:blue">*cache*</p>

Updates cache settings

##### Usage

```shell
akeyless gateway update cache \
--enable-cache [true/false] \
--stale-timeout[=60] <Stale timeout in minutes> \
--enable-proactive [true/false] \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

##### Flags

`--enable-cache`: Enable cache \[\`true\`/\`false\`]

`--stale-timeout[=60]`: Stale timeout in minutes, cache entries which are not accessed within timeout will be removed from cache

`--enable-proactive`: Enable proactive caching \[\`true\`/\`false\`]

`--minimum-fetch-interval[=5]`: When using Cache or/and Proactive Cache, additional secrets will be fetched upon requesting a secret, based on the requestor's access policy. Define minimum fetching interval to avoid over fetching in a given time frame

`--backup-interval[=1]`: Secure backup interval in minutes. To ensure service continuity in case of power cycle and network outage secrets will be backed up periodically per backup interval

`-u, --gateway-url`: Gateway URL (Configuration Management port)

### <p style="color:blue">*defaults*</p>

Updates defaults settings

##### Usage

```shell
akeyless gateway update defaults \
--saml-access-id[=use-existing] <saml-AccessID> \
--oidc-access-id[=use-existing] <oidc-AccessID> \
--cert-access-id[=use-existing] <cert-AccessID> \
--key[=Default] <gw encryption key> \
--event-on-status-change [true/false]
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

##### Flags

`--saml-access-id[=use-existing]`: Default SAML access-id for UI login

`--oidc-access-id[=use-existing]`: Default OIDC access-id for UI login

`--cert-access-id[=use-existing]`: Default Certificate access-id for UI login

`--key[=Default]`: The name of the gateway default encryption key

`--hvp-route-version`: Hvp route version to use \[\`1\`/\`2\`]

`--event-on-status-change`: Trigger an event when Gateway status is changed \[\`true\`/\`false\`]

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)
