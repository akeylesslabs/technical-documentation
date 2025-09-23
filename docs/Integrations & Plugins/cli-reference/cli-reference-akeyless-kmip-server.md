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

### <p style={{ color: "blue" }}>*client-delete-rule*</p>

Delete an RBAC rule from a client

##### Usage

```shell
akeyless kmip-client-delete-rule \
--path &lt;Access path&gt; \
--name &lt;KMIP client name&gt; \
--client-id &lt;KMIP client ID&gt; \
--gateway-url &lt;API Gateway URL:8000&gt;
```

##### Flags

 `-p, --path`: **Required**, Access path, e.g /\* or /some-key 

 `-n, --name`: KMIP client name (either name or id are required) 

 `-i, --client-id`: KMIP client ID (either name or id are required)   

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port) 

### <p style={{ color: "blue" }}>*client-set-rule*</p>

Add a new RBAC rule to a client

Supported capabilities are:\
`DENY`\
`CREATE`\
`REGISTER`\
`REKEY`\
`LOCATE`\
`GET`\
`GET_ATTRIBUTES`\
`ACTIVATE`\
`REVOKE`\
`DESTROY`

##### Usage

```shell
akeyless kmip-client-set-rule \
--path &lt;Access path&gt; \
--capability &lt;Access capability&gt; \
--name &lt;KMIP client name&gt; \
--client-id &lt;KMIP client ID&gt; \
--gateway-url &lt;API Gateway URL:8000&gt;
```

##### Flags

 `-p, --path`: **Required**, Access path, e.g /\* or /some-key                                   

 `-c, --capability`: **Required**, Access capability (see command description for supported values)    

 `-n, --name`: KMIP client name (either name or id are required)                                   

 `-i, --client-id`: KMIP client ID (either name or id are required)                                     

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### <p style={{ color: "blue" }}>*create-client*</p>

Create a new KMIP client

##### Ussage

```shell
akeyless kmip-create-client \
--name &lt;Client name&gt; \
--certificate-ttl &lt;Server certificate TTL in days (Deafult = 90)&gt; \
--gateway-url &lt;API Gateway URL:8000&gt;
```

##### Flags

 `-n, --name`: **Required**, Client name                                                                                                      

 `-t, --certificate-ttl[=90]`: Client certificate TTL in days                                                                                                   

 `-p, --output-file-folder`: Folder path to save client certificate files (for example, '.'). Two files are created: &lt;client-name&gt;.key and &lt;client-name&gt;.cert 

 `-a, --activate-keys-on-creation"h-0": "`: If set to 'true', newly created keys on the client will be set to an 'active' state                                              

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### <p style={{ color: "blue" }}>*delete-client*</p>

Delete a KMIP client

##### Flags

 `-n, --name`: KMIP client name (either name or id are required)                                   

 `-i, --client-id`: KMIP client ID (either name or id are required)                                     

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port) 

### <p style={{ color: "blue" }}>*describe-client*</p>

Show KMIP client details

##### Flags

 `-n, --name`: KMIP client name (either name or id are required)                                   

 `-i, --client-id`: KMIP client ID (either name or id are required)                                     

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### <p style={{ color: "blue" }}>*describe-server*</p>

Show KMIP environment details

##### Flags

 `-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port).

### <p style={{ color: "blue" }}>*list-clients*</p>

Show existing KMIP clients

##### Flags

 `-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port).

### <p style={{ color: "blue" }}> *renew-client-certificate*</p>

Renew KMIP client certificate

##### Flags

 `-n, --name`: KMIP client name (either name or id are required)                                                                                

 `-i, --client-id`: KMIP client ID (either name or id are required)                                                                                  

 `-p, --output-file-folder`: Folder path to save client certificate files (for example, '.'). Two files are created: &lt;client-name&gt;.key and &lt;client-name&gt;.cert 

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### <p style={{ color: "blue" }}>*renew-server-certificate*</p>

Renew KMIP server certificate

##### Flags

 `-u, --gateway-url[=http://localhost:8000]`:  API Gateway URL (Configuration Management port)  

### <p style={{ color: "blue" }}>*server-delete*</p>

Delete the kmip server (allowed only if it has no clients nor associated items)

##### Flags

 `-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port).

### <p style={{ color: "blue" }}> *server-setup*</p>

 Create a new KMIP environment

##### Usage

```shell
akeyless kmip-server-setup \
--hostname &lt;KMPI server hostname&gt; \
--certificate-ttl &lt;Server certificate TTL in days (Deafult = 90)&gt; \
--root &lt;Root path of KMIP Objects&gt; \
--gateway-url &lt;API Gateway URL:8000&gt;
```

##### Flags

 `-n, --hostname`: **Required**, Hostname of this KMIP server                                                                    

 `-t, --certificate-ttl[=90]`: Server certificate TTL in days                                                                                  

 `-r, --root`: **Required**, Root path of KMIP Objects                                                                       

 `-p, --output-file-folder`: Folder path to save CA certificate file (for example, '.'). A new file will be created in that folder: ca.cert. 

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### <p style={{ color: "blue" }}>*server-move*</p>

Move the root location of the kmip server and all associated items to a new root location

##### Usage

```shell
akeyless kmip-server-move \
--new-root &lt;New root for the kmip server&gt; \
--gateway-url &lt;API Gateway URL:8000&gt;
```

##### Flags

 `-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port).                                        

 `-n, --new-root`: **Required**, New root for the kmip server 

### <p style={{ color: "blue" }}>*set-server-state*</p>

Set the server state to enabled/disabled

##### Usage

```shell
akeyless kmip-set-server-state \ 
--state &lt;Enabled / Disabled&gt; \
--gateway-url &lt;API Gateway URL:8000&gt;
```

##### Flags

 `-s, --state`: **Required**, Make the server enabled or disabled \[use 'enabled' or 'disabled']   

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)                                     

> 📘 Info
>
> **Writing commands - generating secrets**
>
> The default Akeyless Vault behavior is that the write commands (generate secrets) are performed to the main region of Akeyless Vault, while the read commands (fetch secrets) are performed on the nearest region to you, in order to minimize latency.\
> If you wish to change that, in order to work only with the master region, please add\
> optimize_dns_disable=true in the settings file.