---
title: CLI Reference - Automatic Migration
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
This section outlines the CLI commands relevant to the Gateway Migrations.

General Flags:

`--profile, --token`:  Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal\_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

### `create`

Commands for creating and managing automatic migrations.

##### Usage

```shell
akeyless gateway-create-migration \
--name <Migration name> \
--type <Migration type> \
--target-location <Target location> \
--gateway-url <API Gateway URL:8000> 
```

##### Flags

 `-n, --name`: **Required**, Migration name for display                                                                                                                                                                                                                                                                                                                                                                       

 `-t, --type `: **Required**, Migration type (hashi/aws/gcp/k8s/azure\_kv/1password/active\_directory)                                                                                                                                                                                                                                                                                                                           

 `-l, --target-location`: **Required**, Target location in Akeyless for imported secrets                                                                                                                                                                                                                                                                                                                                                 

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)                                                                                                                                                                                                                                                                                                                                                                  

 `-k, --protection-key`: The name of the key that protects the classic key value (if empty, the account default key will be used)                                                                                                                                                                                                                                                                                                         

 `-g, --gcp-key-file-path`: Path to file with the base64-encoded GCP Service Account private key with sufficient permissions to Secrets Manager, Minimum required permission is Secret Manager Secret Accessor, e.g. 'roles/secretmanager.secretAccessor' (relevant only for GCP migration)                                                                                                                                                  

 `-G, --gcp-key-data`: Base64-encoded GCP Service Account private key text with sufficient permissions to Secrets Manager, Minimum required permission is Secret Manager Secret Accessor, e.g. 'roles/secretmanager.secretAccessor' (relevant only for GCP migration)                                                                                                                                                                   

 `-U, --hashi-url`: HashiCorp Vault API URL, e.g. [https://vault-server:8200](https://vault-server:8200) (relevant only for HasiCorp Vault migration)                                                                                                                                                                                                                                                                                                           

 `--hashi-ns`: HashiCorp Vault Namespaces is a comma-separated list of namespaces which need to be imported into Akeyless Vault. For every provided namespace, all its child namespaces are imported as well, e.g. nmsp/subnmsp1/subnmsp2,nmsp/anothernmsp. By default, import all namespaces (relevant only for HasiCorp Vault migration)                                                                                      

 `-T, --hashi-token`: HashiCorp Vault access token with sufficient permissions to preform list & read operations on secrets objects (relevant only for HasiCorp Vault migration)                                                                                                                                                                                                                                                       

 `--hashi-json=[true]`: Import secret key as json value or independent secrets (relevant only for HasiCorp Vault migration)                                                                                                                                                                                                                                                                                                              

 `-I, --aws-key-id`: AWS Access Key ID with sufficient permissions to get all secrets, e.g. 'arn:aws:secretsmanager:AWSregion:AWSAccountId:Secret:/path/to/secrets/\*' (relevant only for AWS migration)                                                                                                                                                                                                                              

 `-K, --aws-key`: AWS Secret Access Key (relevant only for AWS migration)                                                                                                                                                                                                                                                                                                                                                          

 `--aws-region[=us-east-2]`: AWS region of the required Secrets Manager (relevant only for AWS migration)                                                                                                                                                                                                                                                                                                                                     

 `-v, --azure-kv-name`: Azure Key Vault Name (relevant only for Azure Key Vault migration)                                                                                                                                                                                                                                                                                                                                               

 ` -a, --azure-tenant-id`: Azure Key Vault Access tenant ID (relevant only for Azure Key Vault migration)                                                                                                                                                                                                                                                                                                                                   

 `-c, --azure-client-id `: Azure Key Vault Access client ID, should be Azure AD App with a service principal (relevant only for Azure Key Vault migration)                                                                                                                                                                                                                                                                                  

 `-s, --azure-secret`: Azure Key Vault secret (relevant only for Azure Key Vault migration)                                                                                                                                                                                                                                                                                                                                             

 `--k8s-namespace`: K8s Namespace, Use this field to import secrets from a particular namespace only. By default, the secrets are imported from all namespaces (relevant only for K8s migration)                                                                                                                                                                                                                                     

 `--k8s-url`: K8s API Server URL, e.g. [https://k8s-api.mycompany.com:6443](https://k8s-api.mycompany.com:6443) (relevant only for K8s migration)                                                                                                                                                                                                                                                                                                                  

 `--k8s-skip-system`: K8s Skip Control Plane Secrets, This option allows to avoid importing secrets from system namespaces (relevant only for K8s migration)                                                                                                                                                                                                                                                                           

 `--k8s-ca-certificate`: K8s Cluster CA certificate (relevant only for K8s migration with Certificate Authentication method)                                                                                                                                                                                                                                                                                                              

 `--k8s-client-cert`: K8s Client certificate with sufficient permission to list and get secrets in the namespace(s) you selected (relevant only for K8s migration with Certificate Authentication method)                                                                                                                                                                                                                              

 `--k8s-client-key `: K8s Client key (relevant only for K8s migration with Certificate Authentication method)                                                                                                                                                                                                                                                                                                                          

 `--k8s-username`: K8s Client username with sufficient permission to list and get secrets in the namespace(s) you selected (relevant only for K8s migration with Password Authentication method)                                                                                                                                                                                                                                    

 ` --k8s-password`: K8s Client password (relevant only for K8s migration with Password Authentication method)                                                                                                                                                                                                                                                                                                                        

 `--k8s-token`: K8s Bearer Token with sufficient permission to list and get secrets in the namespace(s) you selected (relevant only for K8s migration with Token Authentication method)                                                                                                                                                                                                                                          

 `--ad-target-name`: Active Directory LDAP Target Name. Server type should be Active Directory (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                                         

 `--ad-domain-name`: Active Directory Domain Name (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                                                                                      

 `--ad-user-base-dn`: Distinguished Name of User objects to search in Active Directory, e.g.: CN=Users,DC=example,DC=com (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                

 `--ad-domain-users-path-template`: Path location template for migrating domain users as Rotated Secrets e.g.: .../DomainUsers/\{\{USERNAME}} (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                           

 `--ad-user-groups`: Comma-separated list of domain groups from which privileged domain users will be migrated (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                         

 `--ad-discover-local-users`: Enable/Disable discovery of local users from each domain server and migrate them as SSH Rotated Secrets. Default is false: only domain users will be migrated. Discovery of local users might require further installation of SSH on the servers, based on the supplied computer base DN. This will be implemented automatically as part of the migration process (Relevant only for Active Directory migration) 

 `--ad-targets-path-template`: Path location template for migrating domain servers as SSH Targets e.g.: .../Servers/\{\{COMPUTER\_NAME}} (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                            

 `--ad-local-users-path-template`: Path location template for migrating domain users as Rotated Secrets e.g.: .../LocalUsers/\{\{COMPUTER\_NAME}}/\{\{USERNAME}} (Relevant only for Active Directory migration)                                                                                                                                                                                                                                          

 `--ad-computer-base-dn`: Distinguished Name of Computer objects (servers) to search in Active Directory e.g.: CN=Computers,DC=example,DC=com (Relevant only for Active Directory migration)                                                                                                                                                                                                                                               

 `--ad-local-users-ignore`: Comma-separated list of Local Users which should not be migrated (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                                                  

 `--ad-os-filter`: Filter by Operating System to run the migration, can be used with wildcards, e.g. SRV20\* (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                         

 `--ad-targets-type[=windows]`: Set the target type of the domain servers \[ssh/windows]\(Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                                                           

 `--ad-ssh-port[=22]`: Set the SSH Port for further connection to the domain servers. Default is port 22 (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                                 

`--ad-winrm-port[=5986]`: Set the WinRM Port for further connection to the domain servers. Default is 5986 (Relevant only for Active Directory migration)

`--ad-winrm-over-http[=false]`: Use WinRM over HTTP, by default runs over HTTPS

`--ad-target-format[=linked]`: Relevant only for `ad-discovery-types`=`computers`. For linked, all computers will be migrated into a linked target(s). if set with regular, the migration will create a target for each computer.

`--ad-discover-services[=false]`: Enable/Disable discovery of Windows services from each domain server as part of the SSH/Windows Rotated Secrets. Default is false. (Relevant only for Active Directory migration)

`--ad-discovery-types`: Set migration discovery types (domain-users, computers, local-users). To specify multiple types use argument multiple times: --ad-discovery-types domain-users --ad-discovery-types local-users. (Relevant only for Active Directory migration)

 `--ad-sra-enable-rdp`: Enable/Disable RDP Secure Remote Access for the migrated local users rotated secrets. Default is false: rotated secrets will not be created with SRA (Relevant only for Active Directory migration)                                                                                                                                                                                                              

 `--ad-auto-rotate`: Enable/Disable automatic/recurrent rotation for migrated secrets. Default is false: only manual rotation is allowed for migrated secrets. If set to true, this command should be combined with --ad-rotation-interval and --ad-rotation-hour Flags (Relevant only for Active Directory migration)                                                                                                           

 `--ad-rotation-interval`: The number of days to wait between every automatic rotation \[1-365] \(Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                                              

 `--ad-rotation-hour`: The hour of the scheduled rotation in UTC (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                                                                         

 `--1password-url`: 1Password sign-in address for your account                                                                                                                                                                                                                                                                                                                                                                       

 `--1password-email`: 1Password user email                                                                                                                                                                                                                                                                                                                                                                                             

 `--1password-password`: 1Password password for the given user's email                                                                                                                                                                                                                                                                                                                                                                    

 `--1password-secret-key`: User's 1Password Secret Key                                                                                                                                                                                                                                                                                                                                                                                      

 `--1password-vaults`: Optional list of 1Password vaults to migrate items from; can be used multiple times (--1password-vaults vault1 --1password-vaults vault2), If not provided, all non-private vaults will be migrated                                                                                                                                                                                                              

 `--si-target-name`: SSH, Windows or Linked Target Name. (Relevant only for Server Inventory migration)                                                                                                                                                                                                                                                                                                                               

 `--si-users-path-template`: Path location template for migrating users as Rotated Secrets e.g.: .../Users/\{\{COMPUTER\_NAME}}/\{\{USERNAME}} (Relevant only for Server Inventory                                                                                                                                                                                                                                                                 

 `--si-users-ignore`: Comma-separated list of Local Users which should not be migrated (Relevant only for Server Inventory migration)                                                                                                                                                                                                                                                                                                  

 `--si-sra-enable-rdp[=false]`: Enable/Disable RDP Secure Remote Access for the migrated local users rotated secrets. Default is false: rotated secrets will not be created with SRA (Relevant only for Server Inventory migration)                                                                                                                                                                                                              

 `--si-auto-rotate`: Enable/Disable automatic/recurrent rotation for migrated secrets. Default is false: only manual rotation is allowed for migrated secrets. If set to true, this command should be combined with `--si-rotation-interval` and `--si-rotation-hour` Flags (Relevant only for Server Inventory migration)                                                                                                       

 `--si-rotation-interval`: The number of days to wait between every automatic rotation \[1-365] \(Relevant only for Server Inventory migration)                                                                                                                                                                                                                                                                                              

 `--si-rotation-hour`: The hour of the scheduled rotation in UTC (Relevant only for Server Inventory migration)                                                                                                                                                                                                                                                                                                                         

### `delete`

Delete migration

##### Usage

```shell
akeyless gateway-delete-migration \
--id <Migration ID> \
--gateway-url <API Gateway URL:8000> 
```

### `get`

Get migrations 

##### Usage

```shell
akeyless gateway-get-migration \
--name <Migration Name> \
--gateway-url <API Gateway URL:8000> 
```

### `list`

List migrations

##### Flags

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port) 

### `personal-items`

Migrates personal items from external vault

##### Usage

```shell
akeyless gateway-migrate-personal-items \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--type <1password> \
--protection-key <Key Name> \
--target-location <Path/To/Target> \
--1password-url <Account Address> \
--1password-email <User Email> \
--1password-password <Users Password> \
--1password-secret-key <Secret Key> \
```

##### Flags

 `-u, --gateway-url[=http://localhost:18888]`: API Gateway URL (Akeyless UI port)                                                                                                                                                                  

 `-t, --type[=1password]`: Migration provider type, Current supported options: \[1password]                                                                                                                                     

 `-k, --protection-key`: The name of a key that used to encrypt the secret value                                                                                                                                             

 `-l, --target-location`: Target location in your Akeyless personal folder for migrated secrets                                                                                                                               

 `--1password-url`: 1Password sign-in address for your account                                                                                                                                                          

 `--1password-email`: 1Password user email                                                                                                                                                                                

 `--1password-password`: 1Password password for the given user's email                                                                                                                                                       

 `--1password-secret-key`: User's 1Password Secret Key                                                                                                                                                                         

 `--1password-vaults`: Optional list of 1Password vaults to migrate items from; can be used multiple times (--1password-vaults vault1 --1password-vaults vault2), If not provided, all non-private vaults will be migrated

### `status`

Gets migration Status

##### Usage

```shell
akeyless gateway-migration-status \
--name <Migration Name> \
--id <Migration ID> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

##### Flags

 `-n, --name`: Migration name to display

 `-i, --id`: Optional, instead of migration name, set a Migration ID  \\n(Can be retrieve with gateway-list-migration command)

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `sync`

Sync migration

##### usage

```shell
Akeyless gateway-sync-migration \
--name <Migration Name> \
--gateway-url <API Gateway URL:8000> \
--sync <true/false>
```

##### Flags

 `-n, --name `: **Required**, Migration name                         

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)        

 `--sync`: true, for starting synchronization, false for stopping 

### `update`

Update migration

##### Usage

```shell
akeyless gateway-update-migration \
--target-location <Target location> \
--id <Migration ID> \
--name <Migration name> \
--new-name <New migration name> \
--gateway-url <API Gateway URL:8000>
```

##### Flags

 `-i, --id`: Migration ID (Can be retrieved with gateway-list-migration command)                                                                                                                                                                                                                                                                                                                                              

 `-n, --name`: Migration name                                                                                                                                                                                                                                                                                                                                                                                                   

 `--new-name`: New migration name                                                                                                                                                                                                                                                                                                                                                                                               

 `-l, --target-location`: **Required**, Target location in Akeyless for imported secrets                                                                                                                                                                                                                                                                                                                                                 

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)                                                                                                                                                                                                                                                                                                                                                                  

 `-k, --protection-key`: The name of the key that protects the classic key value (if empty, the account default key will be used)                                                                                                                                                                                                                                                                                                         

 `-g, --gcp-key-file-path`: Path to file with the base64-encoded GCP Service Account private key with sufficient permissions to Secrets Manager, Minimum required permission is Secret Manager Secret Accessor, e.g. 'roles/secretmanager.secretAccessor' (relevant only for GCP migration)                                                                                                                                                  

 `-G, --gcp-key-data `: Base64-encoded GCP Service Account private key text with sufficient permissions to Secrets Manager, Minimum required permission is Secret Manager Secret Accessor, e.g. 'roles/secretmanager.secretAccessor' (relevant only for GCP migration).                                                                                                                                                                  

 `-U, --hashi-url`: HashiCorp Vault API URL, e.g. [https://vault-mgr01:8200](https://vault-mgr01:8200) (relevant only for HasiCorp Vault migration)                                                                                                                                                                                                                                                                                                            

 `--hashi-ns`: HashiCorp Vault Namespaces is a comma-separated list of namespaces which need to be imported into Akeyless Vault. For every provided namespace, all its child namespaces are imported as well, e.g. nmsp/subnmsp1/subnmsp2,nmsp/anothernmsp. By default, import all namespaces (relevant only for HasiCorp Vault migration)                                                                                      

 `-T, --hashi-token`: HashiCorp Vault access token with sufficient permissions to preform list & read operations on secrets objects (relevant only for HasiCorp Vault migration)                                                                                                                                                                                                                                                       

 `--hashi-json='true'`: Import secret key as json value or independent secrets (relevant only for HasiCorp Vault migration)                                                                                                                                                                                                                                                                                                              

 `-I, --aws-key-id`: AWS Access Key ID with sufficient permissions to get all secrets, e.g. 'arn:aws:secretsmanager:[Region]\:[AccountId]\: secret:\[/path/to/secrets/\*]' (relevant only for AWS migration)                                                                                                                                                                                                                            

 ` -K, --aws-key`: AWS Secret Access Key (relevant only for AWS migration)                                                                                                                                                                                                                                                                                                                                                          

 `--aws-region[=us-east-2]`: AWS region of the required Secrets Manager (relevant only for AWS migration)                                                                                                                                                                                                                                                                                                                                     

 `-v, --azure-kv-name`: Azure Key Vault Name (relevant only for Azure Key Vault migration)                                                                                                                                                                                                                                                                                                                                               

 `-a, --azure-tenant-id`: Azure Key Vault Access tenant ID (relevant only for Azure Key Vault migration)                                                                                                                                                                                                                                                                                                                                   

 `-c, --azure-client-id`: Azure Key Vault Access client ID, should be Azure AD App with a service principal (relevant only for Azure Key Vault migration)                                                                                                                                                                                                                                                                                  

 `-s, --azure-secret`: Azure Key Vault secret (relevant only for Azure Key Vault migration)                                                                                                                                                                                                                                                                                                                                             

 `--k8s-namespace`: K8s Namespace, Use this field to import secrets from a particular namespace only. By default, the secrets are imported from all namespaces (relevant only for K8s migration)                                                                                                                                                                                                                                     

 `--k8s-url`: K8s API Server URL, e.g. [https://k8s-api.mycompany.com:6443](https://k8s-api.mycompany.com:6443) (relevant only for K8s migration)                                                                                                                                                                                                                                                                                                                  

 `--k8s-skip-system`: K8s Skip Control Plane Secrets, This option allows to avoid importing secrets from system namespaces (relevant only for K8s migration)                                                                                                                                                                                                                                                                           

 `--k8s-ca-certificate`: K8s Cluster CA certificate (relevant only for K8s migration with Certificate Authentication method)                                                                                                                                                                                                                                                                                                              

 `--k8s-client-cert`: K8s Client certificate with sufficient permission to list and get secrets in the namespace(s) you selected (relevant only for K8s migration with Certificate Authentication method)                                                                                                                                                                                                                              

 `--k8s-client-key`: K8s Client key (relevant only for K8s migration with Certificate Authentication method)                                                                                                                                                                                                                                                                                                                          

 `--k8s-username`: K8s Client username with sufficient permission to list and get secrets in the namespace(s) you selected (relevant only for K8s migration with Password Authentication method)                                                                                                                                                                                                                                    

 `--k8s-password`: K8s Client password (relevant only for K8s migration with Password Authentication method)                                                                                                                                                                                                                                                                                                                        

 `--k8s-token`: K8s Bearer Token with sufficient permission to list and get secrets in the namespace(s) you selected (relevant only for K8s migration with Token Authentication method)                                                                                                                                                                                                                                          

 `--ad-target-name`: Active Directory LDAP Target Name. Server type should be Active Directory (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                                         

 `--ad-domain-name`: Active Directory Domain Name (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                                                                                      

 `--ad-user-base-dn`: Distinguished Name of User objects to search in Active Directory, e.g.: CN=Users,DC=example,DC=com (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                

 `--ad-domain-users-path-template`: Path location template for migrating domain users as Rotated Secrets e.g.: .../DomainUsers/\{\{USERNAME}} (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                           

 `--ad-user-groups`: Comma-separated list of domain groups from which privileged domain users will be migrated (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                         

 `--ad-discover-local-users`: Enable/Disable discovery of local users from each domain server and migrate them as SSH Rotated Secrets. Default is false: only domain users will be migrated. Discovery of local users might require further installation of SSH on the servers, based on the supplied computer base DN. This will be implemented automatically as part of the migration process (Relevant only for Active Directory migration) 

 `--ad-targets-path-template`: Path location template for migrating domain servers as SSH Targets e.g.: .../Servers/\{\{COMPUTER\_NAME}} (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                            

 `--ad-local-users-path-template`: Path location template for migrating domain users as Rotated Secrets e.g.: .../LocalUsers/\{\{COMPUTER\_NAME}}/\{\{USERNAME}} (Relevant only for Active Directory migration)                                                                                                                                                                                                                                          

 `--ad-computer-base-dn`: Distinguished Name of Computer objects (servers) to search in Active Directory e.g.: CN=Computers,DC=example,DC=com (Relevant only for Active Directory migration)                                                                                                                                                                                                                                               

 `--ad-local-users-ignore`: Comma-separated list of Local Users which should not be migrated (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                                                  

 `--ad-os-filter`: Filter by Operating System to run the migration, can be used with wildcards, e.g. SRV20\* (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                         

 `--ad-targets-type[=ssh]`: Set the target type of the domain servers \[ssh/windows]\(Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                                                           

 `--ad-ssh-port[=22]`: Set the SSH Port for further connection to the domain servers. Default is port 22 (Relevant only for Active Directory migration)

`--ad-winrm-over-http[=false]`: Use WinRM over HTTP, by default runs over HTTPS

`--ad-target-format[=linked]`: Relevant only for `ad-discovery-types`=`computers`. For linked, all computers will be migrated into a linked target(s). if set with regular, the migration will create a target for each computer.

`--ad-discover-services[=false]`: Enable/Disable discovery of Windows services from each domain server as part of the SSH/Windows Rotated Secrets. Default is false. (Relevant only for Active Directory migration)

`--ad-discovery-types`: Set migration discovery types (domain-users, computers, local-users). To specify multiple types use argument multiple times: --ad-discovery-types domain-users --ad-discovery-types local-users. (Relevant only for Active Directory migration)

 `--ad-sra-enable-rdp`: Enable/Disable RDP Secure Remote Access for the migrated local users rotated secrets. Default is false: rotated secrets will not be created with SRA (Relevant only for Active Directory migration)                                                                                                                                                                                                              

 `--ad-auto-rotate`: Enable/Disable automatic/recurrent rotation for migrated secrets. Default is false: only manual rotation is allowed for migrated secrets. If set to true, this command should be combined with --ad-rotation-interval and --ad-rotation-hour Flags (Relevant only for Active Directory migration)                                                                                                           

 `--ad-rotation-interval`: The number of days to wait between every automatic rotation \[1-365] \(Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                                              

 `--ad-rotation-hour`: The hour of the scheduled rotation in UTC (Relevant only for Active Directory migration)                                                                                                                                                                                                                                                                                                                         

 `--1password-url`: 1Password sign-in address for your account                                                                                                                                                                                                                                                                                                                                                                       

 `--1password-email`: 1Password user email                                                                                                                                                                                                                                                                                                                                                                                             

 `--1password-password`: 1Password password for the given user's email                                                                                                                                                                                                                                                                                                                                                                    

 `--1password-secret-key`: User's 1Password Secret Key                                                                                                                                                                                                                                                                                                                                                                                      

 `--1password-vaults`: Optional list of 1Password vaults to migrate items from; can be used multiple times (--1password-vaults vault1 --1password-vaults vault2), If not provided, all non-private vaults will be migrated                                                                                                                                                                                                              

 `--si-target-name`: SSH, Windows or Linked Target Name. (Relevant only for Server Inventory migration)                                                                                                                                                                                                                                                                                                                               

 `--si-users-path-template`: Path location template for migrating users as Rotated Secrets e.g.: .../Users/\{\{COMPUTER\_NAME}}/\{\{USERNAME}} (Relevant only for Server Inventory migration)                                                                                                                                                                                                                                                      

 `--si-users-ignore`: Comma-separated list of Local Users which should not be migrated (Relevant only for Server Inventory migration)                                                                                                                                                                                                                                                                                                  

 `--si-sra-enable-rdp[=false]`: Enable/Disable RDP Secure Remote Access for the migrated local users rotated secrets. Default is false: rotated secrets will not be created with SRA (Relevant only for Server Inventory migration)                                                                                                                                                                                                              

 `--si-auto-rotate`: Enable/Disable automatic/recurrent rotation for migrated secrets. Default is false: only manual rotation is allowed for migrated secrets. If set to true, this command should be combined with `--si-rotation-interval` and `--si-rotation-hour` Flags (Relevant only for Server Inventory migration)                                                                                                       

 `--si-rotation-interval`: The number of days to wait between every automatic rotation \[1-365] \(Relevant only for Server Inventory migration)                                                                                                                                                                                                                                                                                              

 `--si-rotation-hour`: The hour of the scheduled rotation in UTC (Relevant only for Server Inventory migration)                                                                                                                                                                                                                                                                                                                         

 `--profile, --token`: Use a specific profile (located at $HOME/.akeyless/profiles) or a temp access token                                                                                                                                                                                                                                                                                                                              

 `--uid-token`: The universal identity token, Required only for universal\_identity authentication