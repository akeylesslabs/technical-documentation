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

General Flags:

`--profile, --token`:  Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

## <p style="color:blue">_create_</p>

Create a new Target

##### Flags

`artifactory`

`aws`

`azure`

`db`

`dockerhub`

`eks`

`gcp`

`github`

`gitlab`

`gke`

`globalsign`

`globalsign-atlas`

`godaddy`

`hashi-vault`

`k8s`

`ldap`

`linked`

`ping`

`rabbitmq`

`salesforce`

`ssh`

`web`

`windows`

`zerossl`

### <p style="color:blue">_artifactory_</p>

Creates a new Artifactory target in the current account

##### Usage

```shell
akeyless target create artifactory \
--name <Target name> \
--base-url <Artifactory REST URL, must end with artifactory postfix> \
--artifactory-admin-name <Admin name> \
--artifactory-admin-pwd <Admin API Key/Password> \
--key <Key name>
```

##### Flags

 `-n, --name`: **Required**, Target name

 `-b, --base-url`: **Required**, Artifactory REST URL, must end with artifactory postfix

 `-a, --artifactory-admin-name`: **Required**, Admin name

 `-p, --artifactory-admin-pwd`: **Required**, Admin API Key/Password                                                                                   

 `-k, --key `: The name of a key used to encrypt the target secret value (if empty, the account default protectionKey key will be used) 

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_aws_</p>

Creates a new AWS target in the current account

##### Usage

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

### <p style="color:blue">_azure_</p>

Creates a new azure target in the current account

##### Usage

```shell
akeyless target create azure \
--name <Target name> \ 
--client-id <Azure client/application id> \
--client-secret <Azure client secret> \
--tenant-id <Azure tenant id> 
```

##### Flags

 `-n , --name`: **Required**, Target name

 `--client-id`: **Required**, Azure client/application id

 `--tenant-id`: Azure tenant id

 `--client-secret`: **Required**, Azure client secret

 `-i, --use-gw-cloud-identity`: Use the GW's Cloud IAM

 `--subscription-id`: Azure Subscription Id

 `--resource-group-name`: The Resource Group name in your Azure Subscription

 `--resource-name`: The name of the relevant Resource

 `-k, --key`: Key name. The key is used to encrypt the target secret value. If the key name is not specified, the account default protection key is used 

 `--description`: Target description  
 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_db_</p>

Creates a new DB target in the current account

##### Usage

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

 `--snowflake-api-private-key`: RSA Private key (base64 encoded)

 `--snowflake-api-private-key-file-name`: The path to the file containing the private key

 `--snowflake-api-private-key-passphrases`: The Private key passphrase                        

 `--db-server-certificates`: Set of root certificate authorities in base64 encoding used by clients to verify server certificates

 `--db-server-name`: Server name is used to verify the hostname on the returned certificates unless InsecureSkipVerify is provided. It is also included in the client's handshake to support virtual hosting unless it is an IP address 

 `--azure-client-id`: Azure client id (relevant for "cloud-service-provider" only)

 `--azure-tenant-id`: Azure tenant id (relevant for "cloud-service-provider" only)

 `--azure-client-secret`: Azure client secret (relevant for "cloud-service-provider" only)

 `--cloud-service-provider`: Cloud service provider (currently only supports Azure)

 `--connection-type[=credentials]`: Type of connection to mssql database [credentials/cloud-identity]  

 `--ssl[=false]`: Enable/Disable SSL [true/false]                                                                                

 `--ssl-certificate`: SSL CA certificate in base64 encoding generated from a trusted Certificate Authority (CA) 

 `--snowflake-account`: Snowflake account name   

 `--oracle-service-name`: oracle db service name

 `--oracle-wallet-login-type`: Oracle Wallet login type (`password`/`mtls`)

 `--oracle-wallet-path`: Path to Oracle wallet (where `cwallet.sso` and `ewallet.p12` reside)

 `--oracle-wallet-sso-file-data`: Oracle wallet `sso` file data in base64

  `--oracle-wallet-p12-file-data`: Oracle wallet `p12` file data in base64

 `--mongodb-atlas`: Flag, set database type to "mongodb" and the flag to "true" to create Mongo Atlas target 

 `--mongodb-default-auth-db`: MongoDB server default authentication database

 `--mongodb-uri-options`: MongoDB server URI options (e.g. replicaSet=mySet&authSource=authDB)

 `--mongodb-atlas-project-id`: MongoDB Atlas project ID

 `--mongodb-atlas-api-public-key`: MongoDB Atlas public key

 `--mongodb-atlas-api-private-key`: MongoDB Atlas private key

 `--cluster-mode`: Flag, if set, define this target as cluster mode. relevant for MsSQL targets

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_dockerhub_</p>

Creates a new Docker Hub target in the current account

##### Usage

```shell
akeyless target create dockerhub \
--name <Target name> \
--dockerhub-usernam <Username for docker repository> \
--dockerhub-password <Password for docker repository> \
--key <Key name>
```

##### Flags

 `-n, --name`: **Required**, Target name

 `--dockerhub-username`: **Required**, Username for docker repository

 `--dockerhub-password`: **Required**, Password for docker repository

 `-k, --key `: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_eks_</p>

Creates a new EKS target in the current account

##### Usage

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

 `-n , --name`: **Required**, Target name

 `-e, --eks-cluster-name`: **Required**, EKS cluster name

 `-c, --eks-cluster-endpoint`: **Required**, EKS cluster endpoint (i.e., https\://<IP> of the cluster)                                                                    

 `-t, --eks-cluster-ca-cert`: **Required**, EKS cluster base-64 encoded certificate

 `-i, --eks-access-key-id`: EKS access key ID

 `-s, --eks-secret-access-key`: EKS secret access key

 `-g, --use-gw-cloud-identity`: Use the GW's Cloud IAM

 `--eks-region[=us-east-2]` EKS region

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used. 

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_gcp_</p>

Creates a new GCP target in the current account

##### Usage

```shell
akeyless target create gcp \
--name <Target name> \
--gcp-key-file-path <Path to file with the base64-encoded service account private key> \
--gcp-key <Base64-encoded service account private key text> \ 
--use-gw-cloud-identity <Use the GWs Cloud IAM> \
--key <Key name> 
```

##### Flags

 `-n , --name`: **Required**, Target name

 `--gcp-key-file-path`: Path to file with the base64-encoded service account private key                                                                            

 `--gcp-key`: Base64-encoded service account private key text

 `-i, --use-gw-cloud-identity`: Use the GW's Cloud IAM 

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_github_</p>

Creates a new GitHub target in the current account

##### Usage

```shell
akeyless target create github \
--name <Target name> \
--github-app-id <Github application id> \
--github-app-private-key <Github application private key (base64 encoded key)> \
--github-base-url <Github base url (Deafult = https://api.github.com/> \
--key <Key name>
```

##### Flags

 `-n, --name`: **Required**, Target name 

 `--github-app-id`: Github application id

 `--github-app-private-key`: Github application private key (base64 encoded key)

 `--github-base-url[=https://api.github.com/]`: Github base url

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

 `-k, --key `: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used. 

### <p style="color:blue">_gke_</p>

Creates a new GKE target in the current account

##### Usage

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

 `-n , --name`: **Required**, Target name

 `-a, --gke-account-email`: GKE service account email

 `-e, --gke-cluster-endpoint`: GKE cluster endpoint, i.e., cluster URI https\://\<DNS/IP>                                                                                  

 `-c, --gke-cluster-ca-cert`: GKE Base-64 encoded cluster certificate

 `--gke-account-key-file-path`: File path to GKE service account key

 `--gke-cluster-name`: GKE cluster name

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `-i, --use-gw-cloud-identity`: Use the GW's Cloud IAM

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_globalsign_</p>

Creates a new GlobalSign Target in the current account

##### Usage

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

 `-p, --password`: **Required**, Passwordof the GlobalSign GCC account            

 `-i, --profile-id`: **Required**, Profile ID of the GlobalSign GCC account         

 `-f, --contact-first-name`: **Required**, First name of the GlobalSign GCC account contact 

 `-l, --contact-last-name`: **Required**, Last name of the GlobalSign GCC account contact  

 `--contact-phone`: **Required**, Telephone of the GlobalSign GCC account contact  

 `-e, --contact-email`: **Required**, Email of the GlobalSign GCC account contact      

 `--timeout[=5]`: Timeout for certificate validation.                              

 `-k, --key`: Key name. The key will be used to encrypt the target item.       

 `--description`: Description of the object                                        

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_globalsign-atlas_</p>

Creates a new GlobalSign Atlas target in the current account

##### Usage

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

 `--mtls-cert-data-base64`: Mutual TLS Certificate contents of the GlobalSign Atlas account encoded in base64, either `mtls-cert-file-path` or `mtls-cert-data-base64` must be supplied 

 `--mtls-key-file-path`: Path to the Mutual TLS Key of the GlobalSign Atlas account, either `mtls-key-file-path` or `mtls-key-data-base64` must be supplied                          

 `--mtls-key-data-base64`: Mutual TLS Key contents of the GlobalSign Atlas account encoded in base64, either `mtls-key-file-path` or `mtls-key-data-base64` must be supplied           

 `--timeout[=5m]`: Timeout waiting for certificate validation

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_godaddy_</p>

Creates a new Godaddy target

##### Usage

```shell
akeyless target create godaddy \
--name <Target name> \
--api-key <API Key> \
--secret <API credentials secret> \
--imap-username <Username>
--imap-password <Password>
--imap-fqdn <FQDN>
```

##### Flags:

`-n, --name`: **Required**, Target name

`-a, --api-key`: **Required**, Key of the api credentials to the Godaddy account

`-s, --secret`: **Required**, Secret of the api credentials to the Godaddy account

`--timeout[=5m]`: Timeout waiting for certificate validation

`-u, --imap-username`: **Required**, Username to access the IMAP service

`-u, --imap-password`:  **Required**, Password to access the IMAP service

`--imap-fqdn`: **Required**, FQDN of the IMAP service

`--imap-port[=993]`: **Required**, Port of the IMAP service

`--customer-id`: Customer ID (ShopperId) required for renewal of imported certificates

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--description`: Description of the object

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_hashi-vault_</p>

Creates a new hashi-vault target

##### Usage

```shell
akeyless target create hashi-vault \
--name <Target name> \
--hashi-url 'https://<your-vault-api-url:8200>' \
--vault-token <Access Token> \
--namespace <Namespace Name>
```

##### Flags:

`-n, --name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash / separators. If the folder does not exist, it will be created together with the target.

`--hashi-url`: HashiCorp Vault URL, e.g. https\://vault-mgr01:8200.

`--vault-token`: Vault access token with sufficient permissions.

`--namespace:` List of vault namespaces. To specify multiple namespaces use the argument multiple times: --namespace ns1 --namespace ns2

`--description`: Description of the object

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

### <p style="color:blue">_k8s_</p>

Creates a new K8S target in the current account

##### Usage

```shell
akeyless target create k8s \
--name <Target name> \
--k8s-cluster-endpoint <K8S Cluster endpoint> \
--k8s-cluster-ca-cert <K8S Cluster certificate> \
--k8s-cluster-token <K8S Cluster authentication token> \
--k8s-cluster-name <K8S cluster name> \
--key <Key name>
```

##### Flags

 `-n , --name`: **Required**, Target name

 `-e, --k8s-cluster-endpoint`: **Required**, K8S Cluster endpoint. https\:// , \<DNS / IP> of the cluster                                                                 

 `-c, --k8s-cluster-ca-cert`: **Required**, K8S Cluster certificate. Base 64 encoded certificate                                                                         

 `-t, --k8s-cluster-token`: **Required**, K8S Cluster authentication token

 `-i, --use-gw-service-account`: Use GW's service account. **Boolean** when provided only `name` is required                                                                  

 `--k8s-auth-type[=token]`: K8S auth type, [token/certificate]  
 `--k8s-client-certificate`: Content of the k8 client certificate (PEM format) in a Base64 format                                                                         

 `--k8s-client-certificate-file`: Path to a file that contain the k8s client private key in PEM format                                                                         

 `--k8s-client-key`: Content of the k8 client private key (PEM format) in a Base64 format                                                                         

 `--k8s-client-key-file`: Path to a file that contain the k8s client private key in PEM format                                                                         

`--k8s-cluster-name`: K8S cluster name

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used. 

 `--description`: Description of the object

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_ldap_</p>

Creates a new LDAP target in the current account

##### Usage

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

 `-s, --server-type[=OpenLDAP]`: Set Ldap server type, Options:[OpenLDAP, ActiveDirectory]. Default is OpenLDAP

 `-t, --ldap-ca-cert`: LDAP base-64 encoded CA Certificate

 `--token-expiration`: --token-expiration

 `-k, --key `: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_linked_</p>

Creates a new Linked Target which can inherit credentials from existing Targets

##### Usage

```shell
akeyless target create linked \
-n <linked target name> \
-p <parent target> \
-s <hosts>
```

##### Flags

 `-n, --name`: **Required**, Name for the linked target

 `-s, --hosts`: **Required**, A comma-separated list of server hosts and server descriptions joined by a semicolon ';' (i.e. 'server-dev.com;My Dev server,server-prod.com;My Prod server description') 

 `-p, --parent-target-name`: **Required**, The parent Target name from which to inherit credentials

 `--description`: Description of the object

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_ping_</p>

Creates a new Ping target in the current account

##### Usage

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

 `-k, --key `: The name of a key used to encrypt the target secret value (if empty, the account default protectionKey key will be used) 

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_rabbitmq_</p>

Creates a new RabbitMQ target in the current account

##### Usage

```shell
akeyless target create rabbitmq \
--name <Target name> \
--user <RabbitMQ server user> \
--uri <RabbitMQ server URI> \
--pwd <RabbitMQ server password> \
--key <Key name>
```

##### Flags

 `-n , --name`: **Required**, Target name

 `--user`: **Required**, RabbitMQ server user

 `--pwd`: RabbitMQ server password

 `--uri`: **Required**, RabbitMQ server URI

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_salesforce_</p>

Creates a new Salesforce target in the current account

##### Usage

```shell
akeyless target create salesforce \
--name <Target name> \
--tenant-url <Url of the Salesforce tenant> \
--client-id <Client ID of the oauth2 app to use for connecting to Salesforce> \
--email <The email of the user attached to the oauth2 app used for connecting to Salesforce> \
--auth-flow <type of the auth flow ('jwt' / 'user-password') \
--client-secret <Client secret of the oauth2 app to use for connecting to Salesforce> 
```

##### Flags

 `-n, --name`: **Required**, Target name

 `-u, --tenant-url`: **Required**, Url of the Salesforce tenant

 `-i, --client-id`: **Required**, Client ID of the oauth2 app to use for connecting to Salesforce                                                             

 `-e, --email`: **Required**, The email of the user attached to the oauth2 app used for connecting to Salesforce                                          

 `-a, --auth-flow`: **Required**, type of the auth flow ('jwt' / 'user-password')                                                                             

 `-s, --client-secret`: Client secret of the oauth2 app to use for connecting to Salesforce (required for password flow)                                            

 `-f, --app-private-key-file-name`: Name of the of file containing a PEM private key of the connected app (relevant for JWT auth only)                                          

 `--app-private-key-data`: Base64 encoded PEM of the connected app private key (relevant for JWT auth only)                                                            

 `-p, --password`: The password of the user attached to the oauth2 app used for connecting to Salesforce  (required for user-password flow)                    

 `-o, --security-token`: The security token of the user attached to the oauth2 app used for connecting to Salesforce  (required for user-password flow)              

 `--ca-cert-file-name`: Name of a file containing a PEM certificate to use when uploading new key to Salesforce                                                     

 `--ca-cert-data`: Base64 encoded PEM cert to use when uploading a new key to Salesforce. Used if file name was not provided.                                  

 `--ca-cert-name`: name of the certificate in Salesforce tenant to use when uploading new key                                                                  

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_sectigo_</p>

Creates a new Sectigo target in the current account

##### Usage

```shell
akeyless target create sectigo \
--name <Target name> \
--username <Sectigo Username> \
--password <Sectigo Password> \
--customer-uri <Sectigo Customer Uri > \
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

 `-c, --customer-uri`: **Required**, Customer Uri of the Sectigo account                                          

 `-o, --organization-id`: **Required**, Organization ID of the Sectigo account                                                                             

 `-i, --certificate-profile-id`: **Required**, Certificate Profile ID in Sectigo account                                            

 `-e, --external-requester`: **Required**, External Requester - a comma separated list of emails

 `--timeout[=5m]`: Timeout waiting for certificate validation

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_ssh_</p>

Creates a new SSH target in the current account

##### Usage

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

 `-n , --name`: **Required**, Target name

 `--description`: Target description

 `--host`: SSH host name

 `--port[=22]`: SSH port

 `--ssh-username`: SSH username

 `--ssh-password`: SSH password to rotate

 `--private-key-path`: SSH private key file path

 `--private-key`: SSH private key

 `--private-key-password`: SSH private key password

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--description`: Target desctiption

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_web_</p>

Creates a new web target in the current account

##### Usage

```shell
akeyless target create web \
--name <Target name> \
--url <Web target URL> \
--key <Key name>
```

##### Flags

 `-n , --name`: **Required**, Target name

 `-u, --url`: **Required**, Web target URL

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_windows_</p>

Creates a new Windows Target in the current account

##### Usage

```shell
akeyless target create windows \
-n <Windows target name> \
-s <hostname> \
-u <username> \
-p <password>
```

##### Flags

 `-n, --name`: **Required**, Name for the Windows target

 `-s, --hostname`: **Required**,  Server hostname or IP Address

 `-u, --username`: **Required**, Privileged username

 `-p, --password`: **Required**, Privileged user password 

 `-d, --domain`: User domain name  

 `-r, --port[=5986]`: Windows Server WinRM port, by default, set to `5986` for `Https`                                                                           

 `--use-tls[=true]`: Enable/Disable TLS for WinRM over HTTPS [true/false]                                                                                       

 `--certificate`: SSL CA certificate in base64 encoding generated from a trusted Certificate Authority (CA)                                                  

 `-k, --key`: Key name. The key is used to encrypt the target secret value. If the key name is not specified, the account default protection key is used 

 `--description`: Description of the object 

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

### <p style="color:blue">_zerossl_</p>

Creates a new ZeroSSL Target in the current account

##### Usage

```shell
akeyless target create zerossl \
--name <Target name> \
--api-key <API Key of the ZeroSSLTarget account> \
--imap-username <Username to access the IMAP service> \
--imap-password <Password to access the IMAP service> \
--imap-fqdn <FQDN of the IMAP service> \
--imap-validation-imap <Email address to send the validation email>
```

##### Flags

 `-n, --name`: **Required**, Name for the ZeroSSL target

 `--api-key`: **Required**, ZeroSSL API Key, can be found under your ZeroSSL account in the Developer section

 `--imap-username`: **Required**, An email address of the user registered to the IMAP service

 `--imap-password`: **Required**, IMAP APP-Password

 `imap-fqdn`: **(Mandatory) **IMAP FQDN, for example: `imap.gmail.com`

 `--imap-validation-email`: The domain owner email address that certificate validation mail will be sent to, needs to be one of the following: `admin@domain.com`,  `administrator@domain.com`, `hostmaster@domain.com`, `postmaster@domain.com`, `webmaster@domain.com` 

 `-timeout[=5m]-`: Timeout for certificate validation.

 `--imap-port[=993]`: Port of the IMAP service

 `-k, --key`: Key name. The key will be used to encrypt the target item.

 `--description`: Description of the object

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

## <p style="color:blue">_ assoc-target-item_</p>

Create an association between target and item

##### Usage

```shell
akeyless assoc-target-item \
--target-name <The target to associate> \
--name <The item to associate> \ 
--vault-name <Name of the vault used> \ 
--key-operations <List of allowed operations for the key>
```

##### Flags

 `-t, --target-name`: **Required**, The target to associate

 `-n, --name`: **Required**, The item to associate  

 `--vault-name`: Name of the vault used. (Relevant only for Classic Key and target association. Required for azure targets)

 `--key-operations`: A list of allowed operations for the key. (Relevant only for Classic Key and target association. Required for azure targets)                                                                            

 `--disable-previous-key-version[=false]`: Automatically disable previous key versions. (Required for classic key association with azure targets) 

`--project-id`: Project id of the GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)

`--location-id`: Location id of the GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)  

 `--keyring-name`: Keyring name of the GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)  

 `--purpose`: Purpose if the key in GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)  

 `--kms-algorithm`: Algorithm of the key in GCP KMS. (Relevant only for Classic Key and target association, Required for gcp targets)  

 `--tenant-secret-type`: The tenant secret type [Data/SearchIndex/Analytics]. (Relevant only for Classic Key and target association. Required for salesforce targets)                                                            

 `--multi-region[=false]`: Set to 'true' to create a multi-region managed key. (Relevant only for Classic Key AWS targets) 

 `--regions`: The list of regions in which to create a copy of the key. (Relevant only for Classic Key AWS targets). To specify multiple regions use argument multiple times: --regions us-east-1 --regions us-west-1 

 `--private-key-path`: A path on the target to store the private key (relevant only for certificate provisioning)

 `--certificate-path`: A path on the target to store the certificate pem file (relevant only for certificate provisioning)

 `--chain-path`: A path on the target to store the full chain pem file (relevant only for certificate provisioning)

 `--post-provision-command`: A custom command to run on the remote target after successful provisioning (relevant only for certificate provisioning)

 `--gateway-url[=http://localhost:8000]`: Gateway URL for the certificate provisioning (relevant only for certificate provisioning)

 `--sra-association[=false]`: Specify if the target to associate is for sra, relevant only for sra linked target association to `ldap` rotated secret

 `--external-key-name`: The external key name to associate with the classic key (Relevant only for Classic Key AWS/Azure/GCP targets)

## <p style="color:blue">_delete-assoc-target-item_</p>

Delete an association between target and item

##### Usage

```shell
akeyless delete-assoc-target-item \
--name <Item name> \
--assoc-id <Association id to be deleted. Not required if target name specified> \
--target-name <The target name with which association will be deleted>
```

##### Flags

 `-n , --name`: **Required**, Item name                                               

 `--id, --assoc-id`: The association id to be deleted. Not required if target name specified 

 `-t, --target-name`: The target name with which association will be deleted                  

## <p style="color:blue">_delete_</p>

Delete a target in the current account 

##### Usage

```shell
akeyless target delete \
--name <Target name> \
--target-version <Target Version>
```

##### Flags

 `-n , --name`: **Required**, Target name                                                         

 `-v, --target-version`: Target version                                                                      

 `--force-deletion[=false]`: Delete target even if it has associated items                                       

## <p style="color:blue">_delete-targets_</p>

Delete multiple targets from a given path

##### Usage

```shell
akeyless delete-targets \
--path <Path to delete the targets from>
```

##### Flags

 `-p, --path`: **Required**, Path to delete the targets from 

 `--force-deletion[=false]`: Delete target even if it has associated items   

## <p style="color:blue">_get_</p>

Get target in the current account

##### Usage

```shell
akeyless taregt get --name <Target name>
```

##### Flags

 `-n , --name`: **Required**, Target name          

 `--show-versions[=false]`: Include all target versions in reply 

## <p style="color:blue">_get-details_</p>

Get details of the specified target

##### Usage

```shell
akeyless target get-details --name <Target Name>
```

##### Flags

 `-n , --name`: **Required**, Target name          

 `-v, --target-version`: Target version                       

 `--show-versions[=false]`: Include all target versions in reply 

## <p style="color:blue">_list_</p>

List of all targets in the account

##### Flags

 `--filter`: Filter by target name or part of it

 `-t, --type`: The target types list of the requested targets. In case it is empty, all types of targets will be returned. Options: [hanadb cassandra aws ssh gke eks mysql mongodb snowflake mssql redshift artifactory azure rabbitmq k8s venafi gcp oracle dockerhub ldap github chef web salesforce postgres] 

 `--pagination-token`: Next page reference                                                   

 `--profile, --token`: Use a specific profile (located at $HOME/.akeyless/profiles) or a temp access token

 `--uid-token`: The universal identity token, Required only for universal_identity authentication

## <p style="text-decoration:underline">update</p>

#### <p style="color:blue">artifactory</p>

updates an existing artifactory target in the current account

##### Usage

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

 `-b, --base-url`: **Required**, Artifactory REST URL, must end with artifactory postfix                                                                     

 `-a, --artifactory-admin-name`: **Required**, Admin name

 `-p, --artifactory-admin-pwd`: **Required**, Admin API Key/Password

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

 `--description`: Target description

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version                                                                 

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings                              

#### <p style="color:blue">_aws_</p>

Updates an existing aws target in the current account

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

 `-n , --name`: **Required**, Target name

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

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version                                                                 

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings                              

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

#### <p style="color:blue">_azure_</p>

Updates an existing azure target in the current account

##### Usage

```shell
akeyless taregt update azure \
--name <Target name> \
--new-name <New target name> \
--client-id <Azure client/application id> \
--tenant-id <Azure tenant id> \
--client-secret <Azure client secret> \
--use-gw-cloud-identity <Use the GWs Cloud IAM> \
--subscription-id <Azure Subscription Id> \
--key <Key name>
```

##### Flags

 `-n , --name`: **Required**, Target name

 `--new-name`: New target name

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

 `--client-id`: Azure client/application id

 `--tenant-id`: Azure tenant id

 `--client-secret`: Azure client secret

 `-i, --use-gw-cloud-identity`: Use the GW's Cloud IAM

 `--subscription-id`: Azure Subscription Id

 `--resource-group-name`: The Resource Group name in your Azure Subscription

 `--resource-name`: The name of the relevant Resource

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version                                                                 

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings                              

#### <p style="color:blue">_db_</p>

Update an existing db target in the current account

##### Usage

```shell
akeyless update-db-target \
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

 `-t, --db-type`: **Required**, Database type: mysql/mssql/postgres/mongodb/snowflake/cassandra/oracle/redshift/redis

 `--new-name`: New target name

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

 `--user-name`: Database user name

 `--host`: Database host

 `--pwd`: Database password

 `--port`: Database port

 `--db-name`: Database name

 `--db-server-certificates`: Set of root certificate authorities in base64 encoding used by clients to verify server certificates

 `--db-server-name`: Server name is used to verify the hostname on the returned certificates unless InsecureSkipVerify is provided. It is also included in the client's handshake to support virtual hosting unless it is an IP address 

 `--snowflake-account`: Snowflake account name

 `--mongodb-atlas`: Flag, set database type to "mongodb" and the flag to "true" to create Mongo Atlas target

 `--mongodb-default-auth-db`: MongoDB server default authentication database

 `--mongodb-uri-options`: MongoDB server URI options (e.g. replicaSet=mySet&authSource=authDB)

 `--mongodb-atlas-project-id`: MongoDB Atlas project ID

 `--mongodb-atlas-api-public-key`: MongoDB Atlas public key

 `--mongodb-atlas-api-private-key`: MongoDB Atlas private key

`--cluster-mode`: Flag, if set, define this target as cluster mode. relevant for MsSQL targets

 `--ssl[=false]`: Enable/Disable SSL [true/false]

 `--ssl-certificate`: SSL CA certificate in base64 encoding generated from a trusted Certificate Authority (CA)

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used                                                                        

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings

#### <p style="color:blue">_dockerhub_</p>

updates an existing dockerhub target in the current account

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

 `--dockerhub-username`: **Required**, Username for docker repository

 `--dockerhub-password`: **Required**, Password for docker repository

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings

#### <p style="color:blue">_eks_</p>

Updates an existing eks target in the current account

#### Usage

```shell
akeyless target update eks \
--name <Target Name> \
--eks-cluster-name <EKS cluster Name> \
--eks-cluster-endpoint <EKS Cluster Endpoint> \
--eks-cluster-ca-cert <EKS Cluster Certificate \
--eks-access-key-id <EKS Access ID> \
--eks-secret-access-key <EKS Secret Access Key> \
--new-name <New target name> \
```

##### Flags

 `-n , --name`: **Required**, Target name

 `-c, --eks-cluster-name`: **Required**, EKS cluster name

 `-e, --eks-cluster-endpoint`: **Required**, EKS cluster endpoint (i.e., https\://<IP> of the cluster)                                                                   

 `-r, --eks-cluster-ca-cert`: **Required**, EKS cluster base-64 encoded certificate

 `-i, --eks-access-key-id`: **Required**, EKS access key ID

 `-s, --eks-secret-access-key`: **Required**, EKS secret access key

 `-g, --use-gw-cloud-identity`: Use the GW's Cloud IAM

 `--new-name`: New target name

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

 `--eks-region[=us-east-2]`: EKS region

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version                                                                 

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings                              

#### <p style="color:blue">_gcp_</p>

Update an existing gcp target in the current account

#### Usage

```shell
akeyless taregt update gcp \
--name <Target Name> \
--new-name <New target name> \
--gcp-key-file-path <Path to file with the base64-encoded service account private key> \
--gcp-key <Base64-encoded service account private key text> \
--use-gw-cloud-identity <Use the GWs Cloud IAM> \
--key <Key name>
```

##### Flags

 `-n , --name`: **Required**, Target name

 `--new-name`: New target name

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

 `--gcp-key-file-path`: Path to file with the base64-encoded service account private key

 `--gcp-key`: Base64-encoded service account private key text

 `-i, --use-gw-cloud-identity`: Use the GW's Cloud IAM

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version                                                                 

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings                              

#### <p style="color:blue">_github_</p>

updates a new github target in the current account

##### Usage

```shell
akeyless target update github \
--name <Target Name> \
--new-name <New target name> \
--github-app-id <Github application id> \
--github-app-private-key <Github application private key> \
--github-base-url <Github base url (Deafult = https://api.github.com>
```

#### Flags

 `-n, --name`: **Required**, Target name

 `--new-name`: New target name

 `--github-app-id`: Github application id

 `--github-app-private-key`: Github application private key (base64 encoded key)

 `--github-base-url[=https://api.github.com/]`: Github base url

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings

#### <p style="color:blue">_gke_</p>

Updates an existing gke target in the current account

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

 `-e, --gke-cluster-endpoint`: GKE cluster endpoint, i.e., cluster URI

 `-c, --gke-cluster-ca-cert`: GKE Base-64 encoded cluster certificate

 `--gke-account-key-file-path`: File path to GKE service account key

 `--gke-account-key`: GKE service account key

 `--gke-cluster-name`: GKE cluster name

 `--new-name`: New target name

 `-i, --use-gw-cloud-identity`: Use the GW's Cloud IAM

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version                                                                 

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings                              

#### <p style="color:blue">_globalsign_</p>

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

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings

 `--description`: Description of the object

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

#### <p style="color:blue">_globalsign-atlas_</p>

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

 `--mlts-cert-file-path`: Path to the Mutual TLS Certificate of the GlobalSign Atlas account, either mtls-cert-file-path or tls-cert-data-base64 must be supplied

 `--mlts-cert-data-base64`: Mutual TLS Certificate contents of the GlobalSign Atlas account encoded in base64, either mtls-cert-file-path or mtls-cert-data-base64 must be supplied 

 `--mlts-key-file-path`: Path to the Mutual TLS Key of the GlobalSign Atlas account, either mtls-key-file-path or mtls-key-data-base64 must be supplied                          

 `--mlts-key-data-base64`: Mutual TLS Key contents of the GlobalSign Atlas account encoded in base64, either mtls-key-file-path or mtls-key-data-base64 must be supplied           

 `--timeout[=5]`: Timeout waiting for certificate validation

 `--new-name`: New Target Name

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

#### <p style="color:blue">_godaddy_</p>

Creates a new Godaddy target

##### Usage

```shell
akeyless target update-godaddy-target \
--name <Target name> \
--new-name <New target name> \
--api-key <API Key> \
--secret <API credentials secret> \
--imap-username <Username> \
--imap-password <Password> \
--imap-fqdn <FQDN>
```

##### Flags:

`-n, --name`: **Required**, Target name

`--new-name`: New target name

`-a, --api-key`: **Required**, Key of the api credentials to the Godaddy account

`-s, --secret`: **Required**, Secret of the api credentials to the Godaddy account

`--timeout[=5m]`: Timeout waiting for certificate validation

`-u, --imap-username`: **Required**, Username to access the IMAP service

`-u, --imap-password`:  **Required**, Password to access the IMAP service

`--imap-fqdn`: **Required**, FQDN of the IMAP service

`--imap-port[=993]`: **Required**, Port of the IMAP service

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

`--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings

`--description`: Description of the object

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

#### <p style="color:blue">_hashi-vault_</p>

Updates a new hashi-vault target

##### Usage

```shell
akeyless target update hashi-vault \
--name <Target name> \
--new-name <New Target Name>
--hashi-url 'https://<your-vault-api-url:8200>' \
--vault-token <Access Token> \
--namespace <Namespace Name>
```

##### Flags:

`-n, --name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash / separators. If the folder does not exist, it will be created together with the target.

`--new-name`: New target name

`--hashi-url`: HashiCorp Vault URL, e.g. https\://vault-mgr01:8200.

`--vault-token`: Vault access token with sufficient permissions.

`--namespace:` List of vault namespaces. To specify multiple namespaces use the argument multiple times: --namespace ns1 --namespace ns2

`--description`: Description of the object

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

#### <p style="color:blue">_k8s_</p>

Updates an existing k8s target in the current account

##### Usage

```shell
akeyless target update k8s \
--name <Target Name> \
--k8s-cluster-endpoint <K8S Cluster endpoint> \
--k8s-cluster-ca-cert <K8S Cluster certificate> \
--k8s-cluster-token <K8S Cluster authentication token> \
--k8s-cluster-name <K8S cluster name> \
--new-name <New target name> 
```

##### Flags

 `-n, --name`: **Required**, Target name

 `-e, --k8s-cluster-endpoint`: **Required**, K8S Cluster endpoint. https\:// , \<DNS / IP> of the cluster                                                                

 `-c, --k8s-cluster-ca-cert`: **Required**, K8S Cluster certificate. Base 64 encoded certificate

 `-t, --k8s-cluster-token`: **Required**, K8S Cluster authentication token

 `-i, --use-gw-service-account`: Use the GW's service account

 `--k8s-auth-type[=token]`: K8S auth type, [token/certificate]

 `--k8s-client-certificate`: Content of the k8 client certificate (PEM format) in a Base64 format                                                                        

 `--k8s-client-certificate-file`: Path to a file that contain the k8s client certificate in PEM format                                                                        

 `--k8s-client-key`: Content of the k8 client private key (PEM format) in a Base64 format                                                                        

 `--k8s-client-key-file\`: Path to a file that contain the k8s client private key in PEM format                                                                        

`--k8s-cluster-name`: k8s-cluster-name

 `--new-name`: New target name

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version                                                                 

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings                              

#### <p style="color:blue">_ldap_</p>

updates a new ldap target in the current account

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

 `-s, --server-type`: Set Ldap server type, Options:[OpenLDAP, ActiveDirectory]

 `--new-name`: New target name

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

 `-t, --ldap-ca-cert`: LDAP base-64 encoded CA Certificate

 `--token-expiration`: LDAP token expiration in seconds

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version                                                                 

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings                              

#### <p style="color:blue">_linked_</p>

Update an existing Liked Target in the current account

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

 `-s, --hosts`: A comma-separated list of server hosts and server descriptions joined by a semicolon ';' (i.e. `server-dev.com`;`My Dev server`,`server-prod.com`;`My Prod server description`)

 `-p, --parent-target-name`: The parent Target name from which to inherit credentials

 `--description`: Description of the object

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

#### <p style="color:blue">_rabbitmq_</p>

Update an existing new rabbitmq target in the current account

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

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings

#### <p style="color:blue">_salesforce_</p>

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

 `--new-name`: New target name

 `-u, --tenant-url`: **Required**, Url of the Salesforce tenant

 `-i, --client-id`: **Required**, Client ID of the oauth2 app to use for connecting to Salesforce

 `-e, --email`: **Required**, The email of the user attached to the oauth2 app used for connecting to Salesforce

 `-a, --auth-flow`: **Required**, type of the auth flow ('jwt' / 'user-password')

 `-s, --client-secret`: Client secret of the oauth2 app to use for connecting to Salesforce (required for password flow)

 `-f, --app-private-key-file-name`: Name of the of file containing a PEM private key of the connected app (relevant for JWT auth only)

 `--app-private-key-data`: Base64 encoded PEM of the connected app private key (relevant for JWT auth only)

 `-p, --password`: The password of the user attached to the oauth2 app used for connecting to Salesforce  (required for user-password flow)

 `-o, --security-token`: The security token of the user attached to the oauth2 app used for connecting to Salesforce  (required for user-password flow)

 `--ca-cert-file-name`: Name of a file containing a PEM certificate to use when uploading new key to Salesforce

 `--ca-cert-data`: Base64 encoded PEM cert to use when uploading a new key to Salesforce. Used if file name was not provided.

 `--ca-cert-name`: name of the certificate in Salesforce tenant to use when uploading new key

 `--description`: Target description

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings 

#### <p style="color:blue">_sectigo_</p>

Updates the sectigo target in the current account

##### Usage

```shell
akeyless target create sectigo \
--name <Target name> \
--username <Sectigo Username> \
--password <Sectigo Password> \
--customer-uri <Sectigo Customer Uri > \
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

 `-c, --customer-uri`: **Required**, Customer Uri of the Sectigo account                                          

 `-o, --organization-id`: **Required**, Organization ID of the Sectigo account                                                                             

 `-i, --certificate-profile-id`: **Required**, Certificate Profile ID in Sectigo account                                            

 `-e, --external-requester`: **Required**, External Requester - a comma separated list of emails

 `--timeout[=5m]`: Timeout waiting for certificate validation

`--new-name`: New target name

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used 

 `--description`: Target description 

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults

#### <p style="color:blue">_ssh_</p>

Update an existing ssh target in the current account

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

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version                                                                 

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings                              

#### <p style="color:blue">_web_</p>

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

 `--update-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version

 `--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings                              

#### <p style="color:blue">_windows_</p>

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

 `--use-tls[=true]`: Enable/Disable TLS for WinRM over HTTPS [true/false]

 `--certificate`: SSL CA certificate in base64 encoding generated from a trusted Certificate Authority (CA)

 `-k, --key`: Key name. The key will be used to encrypt the target secret value. If key name is not specified, the account default protection key is used

 ` --keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings

 `--description`: Description of the object

#### <p style="color:blue">_zerossl_</p>

Update an existing ZeroSSL Target in the current account

##### Usage

```shell
akeyless target update-zerossl-target \
--name <Target Name> \
--api-key <API Key of the ZeroSSLTarget account> \
--imap-username <Username to access the IMAP service> \
--imap-password <Password to access the IMAP service> \
--imap-fqdn <FQDN of the IMAP service> \
--imap-validation-imap <Email address to send the validation email> \
--new-name <New Name>
```

##### Flags

 `-n, --name`: **Required**, Name for the ZeroSSL target

 `--api-key`: **Required**, ZeroSSL API Key, can be found under your ZeroSSL account in the Developer section

 `--imap-username`: **Required**, An email address of the user registered to the IMAP service

 `imap-password`: **Required**, IMAP APP-Password - for example, on Gmail Under Settings-> Security, click on 2-Step Verification and generate APP-Password (2-Step verification must be enabled)

 `--imap-fqdn`: **(Mandatory) **IMAP FQDN, for example imap.gmail.com

 `--imap-validation-email`: The domain owner email address that certificate validation mail will be sent to, needs to be one of the following: `admin@domain.com`, `administrator@domain.com`, `hostmaster@domain.com`, `postmaster@domain.com`, `webmaster@domain.com`

 `--imap-port[=993]`: Port of the IMAP service

 `--new-name`: New target name

 `-k, --key`: Key name. The key will be used to encrypt the target secret value

 `--keep-prev-version`: Whether to keep the previous version, options:[true, false], If not set, use default according to account settings

 `--description`: Description of the object

 `--max-versions`: Set the maximum number of versions, limited by the account settings defaults