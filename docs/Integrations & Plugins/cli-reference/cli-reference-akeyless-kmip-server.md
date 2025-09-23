---
title: CLI Reference - KMIP
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
This section outlines the CLI commands relevant to KMIP.

General Flags:

`--profile, --token`:  Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

### <p style="color:blue">_client-delete-rule_</p>

Delete an RBAC rule from a client

##### Usage

```shell
akeyless kmip-client-delete-rule \
--path <Access path> \
--name <KMIP client name> \
--client-id <KMIP client ID> \
--gateway-url <API Gateway URL:8000>
```

##### Flags

 `-p, --path`: **Required**, Access path, e.g /\* or /some-key 

 `-n, --name`: KMIP client name (either name or id are required) 

 `-i, --client-id`: KMIP client ID (either name or id are required)   

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port) 

### <p style="color:blue">_client-set-rule_</p>

Add a new RBAC rule to a client

Supported capabilities are:  
`DENY`  
`CREATE`  
`REGISTER`  
`REKEY`  
`LOCATE`  
`GET`  
`GET_ATTRIBUTES`  
`ACTIVATE`  
`REVOKE`  
`DESTROY`

##### Usage

```shell
akeyless kmip-client-set-rule \
--path <Access path> \
--capability <Access capability> \
--name <KMIP client name> \
--client-id <KMIP client ID> \
--gateway-url <API Gateway URL:8000>
```

##### Flags

 `-p, --path`: **Required**, Access path, e.g /\* or /some-key                                   

 `-c, --capability`: **Required**, Access capability (see command description for supported values)    

 `-n, --name`: KMIP client name (either name or id are required)                                   

 `-i, --client-id`: KMIP client ID (either name or id are required)                                     

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### <p style="color:blue">_create-client_</p>

Create a new KMIP client

##### Ussage

```shell
akeyless kmip-create-client \
--name <Client name> \
--certificate-ttl <Server certificate TTL in days (Deafult = 90)> \
--gateway-url <API Gateway URL:8000>
```

##### Flags

 `-n, --name`: **Required**, Client name                                                                                                      

 `-t, --certificate-ttl[=90]`: Client certificate TTL in days                                                                                                   

 `-p, --output-file-folder`: Folder path to save client certificate files (for example, '.'). Two files are created: <client-name>.key and <client-name>.cert 

 `-a, --activate-keys-on-creation"h-0": "`: If set to 'true', newly created keys on the client will be set to an 'active' state                                              

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### <p style="color:blue">_delete-client_</p>

Delete a KMIP client

##### Flags

 `-n, --name`: KMIP client name (either name or id are required)                                   

 `-i, --client-id`: KMIP client ID (either name or id are required)                                     

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port) 

### <p style="color:blue">_describe-client_</p>

Show KMIP client details

##### Flags

 `-n, --name`: KMIP client name (either name or id are required)                                   

 `-i, --client-id`: KMIP client ID (either name or id are required)                                     

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### <p style="color:blue">_describe-server_</p>

Show KMIP environment details

##### Flags

 `-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port).

### <p style="color:blue">_list-clients_</p>

Show existing KMIP clients

##### Flags

 `-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port).

### <p style="color:blue">_renew-client-certificate _</p>

Renew KMIP client certificate

##### Flags

 `-n, --name`: KMIP client name (either name or id are required)                                                                                

 `-i, --client-id`: KMIP client ID (either name or id are required)                                                                                  

 `-p, --output-file-folder`: Folder path to save client certificate files (for example, '.'). Two files are created: <client-name>.key and <client-name>.cert 

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### <p style="color:blue">_renew-server-certificate_</p>

Renew KMIP server certificate

##### Flags

 `-u, --gateway-url[=http://localhost:8000]`:  API Gateway URL (Configuration Management port)  

### <p style="color:blue">_server-delete_</p>

Delete the kmip server (allowed only if it has no clients nor associated items)

##### Flags

 `-u, --gateway-url[=http://localhost:8000]\<c`: Gateway URL (Configuration Management port).

### <p style="color:blue">_server-setup _</p>

 Create a new KMIP environment

##### Usage

```shell
akeyless kmip-server-setup \
--hostname <KMPI server hostname> \
--certificate-ttl <Server certificate TTL in days (Deafult = 90)> \
--root <Root path of KMIP Objects> \
--gateway-url <API Gateway URL:8000>
```

##### Flags

 `-n, --hostname`: **Required**, Hostname of this KMIP server                                                                    

 `-t, --certificate-ttl[=90]`: Server certificate TTL in days                                                                                  

 `-r, --root`: **Required**, Root path of KMIP Objects                                                                       

 `-p, --output-file-folder`: Folder path to save CA certificate file (for example, '.'). A new file will be created in that folder: ca.cert. 

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### <p style="color:blue">_server-move_</p>

Move the root location of the kmip server and all associated items to a new root location

##### Usage

```shell
akeyless kmip-server-move \
--new-root <New root for the kmip server> \
--gateway-url <API Gateway URL:8000>
```

##### Flags

 `-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port).                                        

 `-n, --new-root`: **Required**, New root for the kmip server 

### <p style="color:blue">_set-server-state_</p>

Set the server state to enabled/disabled

##### Usage

```shell
akeyless kmip-set-server-state \ 
--state <Enabled / Disabled> \
--gateway-url <API Gateway URL:8000>
```

##### Flags

 `-s, --state`: **Required**, Make the server enabled or disabled [use 'enabled' or 'disabled']   

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)                                     

> 📘 Info
> 
> **Writing commands - generating secrets**
> 
> The default Akeyless Vault behavior is that the write commands (generate secrets) are performed to the main region of Akeyless Vault, while the read commands (fetch secrets) are performed on the nearest region to you, in order to minimize latency.  
> If you wish to change that, in order to work only with the master region, please add  
> optimize_dns_disable=true in the settings file.