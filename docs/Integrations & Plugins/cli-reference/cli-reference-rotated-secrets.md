---
title: CLI Reference - Rotated Secrets
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
This section outlines the CLI commands relevant to[ Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets).

Rotated secrets enable you to protect the credentials for privileged-user accounts such as an _Administrator_ account on a Windows server, a **root** account on a Linux server, or an **Admin** account on a network device, by resetting its password.

General Flags:

`--profile, --token`:  Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

## <p style=color:blue>_create_</p>

`akeyless rotated-secret create`

Commands to create a Rotated Secret

**Flags**

`aws`: Creates new aws rotated secret item

`azure`: Creates new azure rotated secret item

`cassandra`: Creates new cassandra rotated secret item

`custom`: Creates new custom rotated secret item

`dockerhub`: Creates new dockerhub rotated secret item

`gcp`: Creates new gcp rotated secret item.

`hanadb`: Creates new hanadb rotated secret item

`ldap`: Creates new ldap rotated secret item

`mongodb`: Creates new mongodb rotated secret item

`mssql`: Creates new mssql rotated secret item

`mysql`: Creates new mysql rotated secret item

`oracledb`: Creates new oracledb rotated secret item

`postgresql`: Creates new postgresql rotated secret item

`redis`: Creates new redis rotated secret item

`redshift`: Creates new redshift rotated secret item

`snowflake`: Creates new snowflake rotated secret item

`ssh`: Creates new ssh rotated secret item

`windows`: Creates new windows rotated secret item

### <p style=color:blue>_aws_</p>

Creates new AWS rotated secret item

##### Usage

```shell AWS
akeyless rotated-secret create aws \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/api-key> 
```

##### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`api-key`]

`--api-id`: **API ID** to rotate (relevant only for `rotator-type`=`api-key`)

`--api-key`: **API key** to rotate (relevant only for `rotator-type`=`api-key`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults.

`--grace-rotation`: A boolean flag, when enabled, a graceful mode of rotation will be conducted, where only the older AWS Access Key will be rotated. When there is only one Access Key, a new version will be created - to maintain 2 values at the same time, following AWS [best practice](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_RotateAccessKey).

 `--grace-rotation-interval`: The number of days to wait before deleting the old key (must be bigger than rotation-interval)

 `--grace-rotation-hour`: The Hour of the grace rotation in UTC

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-bastion-issuer`:  Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-aws-account-id`: The **AWS account id**

`--aws-region[=us-east-2]`: **AWS** region 

`--secure-access-aws-native-cli`: The **AWS ** native cli

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_azure_</p>

Creates new azure rotated secret item

**Usage**

```shell Azure
akeyless rotated-secret create azure \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target|api-key|azure-storage-account|password> 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`api-key`/`azure-storage-account`/`password`]

`--app-id`: ID of the Azure app that holds the secret to be rotated (relevant only for `rotator-type`=`api-key` & `authentication-credentials`=`use-target-creds`)

`--api-id`: **API ID** to rotate (relevant only for `rotator-type`=`api-key`)

`--api-key`: **API key** to rotate (relevant only for `rotator-type`=`api-key`)

`--storage-account-key-name`: The name of the storage account key to rotate [`key1`/`key2`/`kerb1`/`kerb2`] \(relevat to `azure-storage-account`)

`--username`:  The user principal name to rotate his password (relevant only for `rotator-type`=`password`)

`--explicitly-set-sa[=false]`: If set, explicitly provide the storage account details [`true`/`false`]

`--resource-group-name`: The resource group name (only relevant when `explicitly-set-sa`=`true`)

`--resource-name`: The name of the storage account (only relevant when `explicitly-set-sa`=`true`)

`--secure-access-disable-concurrent-connections[=false]`: Enable this flag to prevent simultaneous use of the same secret

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

<br />

<br />

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--max-verisons`: Set the maximum number of versions, limited by the account settings defaults

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_cassandra_</p>

Creates new cassandra rotated secret item

**Usage**

```shell Cassandra
 akeyless rotated-secret create cassandra \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/password> 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_custom_</p>

Creates new custom rotated secret item

**Usage**

```shell Custom
akeyless rotated-secret create custom \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--custom-payload`: Secret payload to be sent with rotation request

`--password-policy-contains-capital-letters`: Password must contain capital letters [`true`/`false`]

`--password-policy-contains-lower-letters`: Password must contain lower case letters [`true`/`false`]

`--password-policy-contains-numbers`: Password must contain numbers [`true`/`false`]

`--password-policy-contains-special-characters`: Password must contain special characters [`true`/`false`]

`--enable-password-policy`: Enable password policy

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--timeout-sec[=40]`: Maximum allowed timeout in seconds for the custom rotator to return the results

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after SRA session ends [`true`/`false`]

`--secure-access-bastion-issuer`:  Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-web-browsing[=false]`: Secure browser via Akeyless Web Access Bastion

`--secure-access-web-proxy[=false]`: Web-Proxy via Akeyless Web Access Bastion

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-rdp-user`: Override the **RDP** Domain username

`--secure-access-allow-external-user[=false]`: Allow providing external user for a domain users

`--secure-access-url`: Destination **URL ** to inject secrets

`--secure-access-ssh-user`: Override the **SSH username** as indicated in **SSH Certificate Issuer**

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_dockerhub_</p>

Creates new dockerhub rotated secret item

**Usage**

```shell Dockerhub
akeyless rotated-secret create dockerhub \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
```

\*_Flags_

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

### <p style="color:blue">_gcp_</p>

Creates new gcp rotated secret item

**Usage**

```shell GCP
akeyless rotated-secret create gcp \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/service-account-rotator>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target naƒme to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`service-account-rotator`]

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--gcp-key-file-path`: Path to file with the service account private key

`--gcp-key`: `Base64-encoded` service account private key text

`--gcp-service-account-email`: The email of the **GCP ** service account to rotate (relevant only when `rotator-type`=`servcie-account-rotator`)

`--gcp-service-account-key-id`: The key id of the **GCP ** service account to rotate (relevant only when `rotator-type`=`servcie-account-rotator`)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--grace-rotation`: A boolean flag, when enabled, a graceful mode of rotation will be conducted, where only the older service account key will be rotated. When there is only one key, a new version will be created to maintain 2 values at the same time.

`--grace-rotation-interval`: The number of days to wait before deleting the old key (must be bigger than rotation-interval)

`--grace-rotation-hour`: The Hour of the grace rotation in UTC

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_hanadb_</p>

Creates new hanadb rotated secret item

**Usage**

```shell HanaDB
akeyless rotated-secret create hanadb \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/password>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_ldap_</p>

Creates new ldap rotated secret item

**Usage**

```shell Ldap
akeyless rotated-secret create ldap \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/ldap>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`ldap`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`ldap`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`ldap`)

`--user-dn`: **Base DN** to Perform User Search

`--user-attribute`: LDAP User Attribute, Default value `cn`

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--grace-rotation`: Create a new `access key` without deleting the old key from **AWS ** for backup (relevant only for AWS) [`true`/`false`]

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-url`: Destination **URL ** to inject secrets

`--host-provider[=explicit]`: Host provider type [`explicit`/`target`], Relevant only for **Secure Remote Access** of **ssh cert issuer** and **ldap rotated secret**

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--target`: A list of linked targets to be associated, Relevant only for **Secure Remote Access** for **ssh cert issuer** and **ldap rotated secret**, To specify multiple targets use argument multiple times

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_mongodb_</p>

Creates new mongodb rotated secret item

**Usage**

```shell MongoDB
akeyless rotated-secret create mongodb \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/password>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`:  Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_mssql_</p>

Creates new mssql rotated secret item

**Usage**

```shell Mssql
akeyless rotated-secret create mssql \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/password>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`:  Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-db-schema`: The DB scheme

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_mysql_</p>

Creates new mysql rotated secret item

**Usage**

```shell Mysql
akeyless rotated-secret create mysql \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/password>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`:  Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_oracledb_</p>

Creates new oracledb rotated secret item

**Usage**

```shell OracleDB
akeyless rotated-secret create oracledb \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/password>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_postgresql_</p>

Creates new postgresql rotated secret item

**Usage**

```shell Postgresql
akeyless rotated-secret create postgresql \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/password>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-db-schema`: The DB scheme

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_redis_</p>

Creates new redis rotated secret item

**Usage**

```shell Redis
akeyless rotated-secret create redis \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/password>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2\`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_redshift_</p>

Creates new redshift rotated secret item

**Usage**

```shell Redis
akeyless rotated-secret create redshift \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/password>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2\`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_snowflake_</p>

Creates new snowflake rotated secret item

**Usage**

```shell Redis
akeyless rotated-secret create snowflake \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/password>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`password` / `key`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password` or `rotator-type`=`key`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`--private-key`: RSA Private key (base64 encoded) to rotate (relevant only for `rotator-type`=`key`)

 `--private-key-file-name`: The path to the file containing the private key (relevant only for `rotator-type`=`key`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2\`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_ssh_</p>

Creates new ssh rotated secret item

**Usage**

```shell Redis
akeyless rotated-secret create ssh \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/password>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--same-password`: Rotate the same password for each host from the Linked Target (**relevant only for Linked Target**)

`--rotator-custom-cmd`: Custom rotation command

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after SRA session ends [`true`/`false`]

`--secure-access-bastion-issuer`:  Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-rdp-user`: Override the **RDP** Domain username

`--secure-access-allow-external-user[=false]`: Allow providing external user for a domain users

`--secure-access-ssh-user`: Override the **SSH username** as indicated in **SSH Certificate Issuer**

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2\`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

### <p style="color:blue">_windows_</p>

Creates new windows rotated secret item

**Usage**

```shell Redis
akeyless rotated-secret create windows \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/password>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: [`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--same-password`: Rotate the same password for each host from the Linked Target (**relevant only for Linked Target**)

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-rdp-user`: Override the **RDP** Domain username

`--secure-access-allow-external-user[=false]`: Allow providing external user for a domain user

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

## <p style=color:blue>_update_</p>

`akeyless rotated-secret-update`

Commands to update a Rotated Secret

**Flags**

`aws`: Updates new aws rotated secret item

`azure`: Updates new azure rotated secret item

`cassandra`: Updates new cassandra rotated secret item

`custom`: Updates new custom rotated secret item

`dockerhub`: Updates new dockerhub rotated secret item

`gcp`: Updates new gcp rotated secret item.

`hanadb`: Updates new hanadb rotated secret item

`ldap`: Updates new ldap rotated secret item

`mongodb`: Updates new mongodb rotated secret item

`mssql`: Updates new mssql rotated secret item

`mysql`: Updates new mysql rotated secret item

`oracledb`: Updates new oracledb rotated secret item

`postgresql`: Updates new postgresql rotated secret item

`redis`: Updates new redis rotated secret item

`redshift`: Updates new redshift rotated secret item

`snowflake`: Updates new snowflake rotated secret item

`ssh`: Updates new ssh rotated secret item

`windows`: Updates new windows rotated secret item

**Updates AWS rotated secret**

**Usage**

```shell AWS
akeyless rotated-secret update aws \
--name <Rotated Secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--new-name <New Item name>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New item name

`--api-id`: **API ID** to rotate (relevant only for `rotator-type`=`api-key`)

`--api-key`: **API key** to rotate (relevant only for `rotator-type`=`api-key`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--grace-rotation`: A boolean flag, when enabled, a graceful mode of rotation will be conducted, where only the older AWS Access Key will be rotated. When there is only one Access Key, a new version will be created - to maintain 2 values at the same time, following AWS [best practice](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_RotateAccessKey).

 `--grace-rotation-interval`: The number of days to wait before deleting the old key (must be bigger than rotation-interval)

 `--grace-rotation-hour`: The Hour of the grace rotation in UTC

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-bastion-issuer`:  Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-aws-account-id`: The **AWS account id**

`--aws-region[=us-east-2]`: **AWS** region 

`--secure-access-aws-native-cli`: The **AWS ** native cli

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates Azure rotated secret**

**Usage**

```shell Azure
akeyless rotated-secret update azure \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--app-id`: ID of the Azure app that hold the secret to be rotated (relevant only for `rotator-type`=`api-key` & `authentication-credentials`=`use-target-creds`)

`--api-id`: **API ID** to rotate (relevant only for `rotator-type`=`api-key`)

`--api-key`: **API key** to rotate (relevant only for `rotator-type`=`api-key`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--storage-account-key-name`: The name of the storage account key to rotate [`key1`/`key2`/`kerb1`/`kerb2`] \(relevat to `azure-storage-account`)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--grace-rotation`: A boolean flag, when enabled, a graceful mode of rotation will be conducted, where only the older secret will be rotated. When there is only one secret, a new version will be created - to maintain 2 values at the same time. Relevant only for **Client Secret**.

 `--grace-rotation-interval`: The number of days to wait before deleting the old key (must be bigger than rotation-interval)

 `--grace-rotation-hour`: The Hour of the grace rotation in UTC

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates cassandra rotated secret**

**Usage**

```shell Cassandra
 akeyless rotated-secret update cassandra \
--name <Rotated Secret name> \
--new-name <New-Item name>
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates custom rotated secret**

**Usage**

```shell Custom
akeyless rotated-secret update custom \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--custom-payload`: Secret payload to be sent with rotation request

`--password-policy-contains-capital-letters`: Password must contain capital letters [`true`/`false`]

`--password-policy-contains-lower-letters`: Password must contain lower case letters [`true`/`false`]

`--password-policy-contains-numbers`: Password must contain numbers [`true`/`false`]

`--password-policy-contains-special-characters`: Password must contain special characters [`true`/`false`]

`--enable-password-policy`: Enable password policy

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--timeout-sec[=40]`: Maximum allowed timeout in seconds for the custom rotator to return the results

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after SRA session ends [`true`/`false`]

`--secure-access-bastion-issuer`:  Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-web-browsing[=false]`: Secure browser via Akeyless Web Access Bastion

`--secure-access-web-proxy[=false]`: Web-Proxy via Akeyless Web Access Bastion

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-rdp-user`: Override the **RDP** Domain username

`--secure-access-allow-external-user[=false]`: Allow providing external user for a domain users

`--secure-access-url`: Destination **URL ** to inject secrets

`--secure-access-ssh-user`: Override the **SSH username** as indicated in **SSH Certificate Issuer**

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates custom rotated secret**

**Usage**

```shell Dockerhub
akeyless rotated-secret update dockerhub \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

**Updates custom rotated secret**

**Usage**

```shell GCP
akeyless rotated-secret update gcp \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotator-type`: **Required**, The rotator type. options: [`target`/`service-account-rotator`]

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--gcp-key-file-path`: Path to file with the service account private key

`--gcp-key`: `Base64-encoded` service account private key text

`--gcp-service-account-email`: The email of the **GCP ** service account to rotate (relevant only when `rotator-type`=`servcie-account-rotator`)

`--gcp-service-account-key-id`: The key id of the **GCP ** service account to rotate (relevant only when `rotator-type`=`servcie-account-rotator`)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--rotation-hour`: The Hour of the rotation in **UTC**

`--grace-rotation`: A boolean flag, when enabled, a graceful mode of rotation will be conducted, where only the older service account key will be rotated. When there is only one key, a new version will be created to maintain 2 values at the same time.

`--grace-rotation-interval`: The number of days to wait before deleting the old key (must be bigger than rotation-interval)

`--grace-rotation-hour`: The Hour of the grace rotation in UTC

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates hanadb rotated secret**

**Usage**

```shell HanaDB
akeyless rotated-secret update hanadb \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates ldap rotated secret**

**Usage**

```shell Ldap
akeyless rotated-secret update ldap \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`ldap`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`ldap`)

`--user-dn`: **Base DN** to Perform User Search

`--user-attribute`: LDAP User Attribute, Default value `cn`

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--grace-rotation`: Create a new `access key` without deleting the old key from **AWS ** for backup (relevant only for AWS) [`true`/`false`]

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-url`: Destination **URL ** to inject secrets

`--host-provider[=explicit]`: Host provider type [`explicit`/`target`], Relevant only for **Secure Remote Access** of **ssh cert issuer** and **ldap rotated secret**

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--target`: A list of linked targets to be associated, Relevant only for **Secure Remote Access** for **ssh cert issuer** and **ldap rotated secret**, To specify multiple targets use argument multiple times

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates mongodb rotated secret**

**Usage**

```shell MongoDB
akeyless rotated-secret update mongodb \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`:  Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates mssql rotated secret**

**Usage**

```shell Mssql
akeyless rotated-secret update  mssql \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`:  Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates mysql rotated secret**

**Usage**

```shell Mysql
akeyless rotated-secret update mysql \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`:  Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates oracledb rotated secret**

**Usage**

```shell OracleDB
akeyless rotated-secret update oracledb \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates postgresql rotated secret**

**Usage**

```shell Postgresql
akeyless rotated-secret update postgresql \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-db-schema`: The DB scheme

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates redis rotated secret**

**Usage**

```shell Redis
akeyless rotated-secret update redis \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates redshift rotated secret**

**Usage**

```shell Redis
akeyless rotated-secret update redshift \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates snowflake rotated secret**

**Usage**

```shell Redis
akeyless rotated-secret update snowflake \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rotator-type <target/password>
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password` or `rotator-type`=`key`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`--private-key`: RSA Private key (base64 encoded) to rotate (relevant only for `rotator-type`=`key`)

 `--private-key-file-name`: The path to the file containing the private key (relevant only for `rotator-type`=`key`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates ssh rotated secret**

**Usage**

```shell Redis
akeyless rotated-secret update ssh \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--same-password`: Rotate the same password for each host from the Linked Target (**relevant only for Linked Target**)

`--rotator-custom-cmd`: Custom rotation command

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after SRA session ends [`true`/`false`]

`--secure-access-bastion-issuer`:  Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-rdp-user`: Override the **RDP** Domain username

`--secure-access-allow-external-user[=false]`: Allow providing external user for a domain users

`--secure-access-ssh-user`: Override the **SSH username** as indicated in **SSH Certificate Issuer**

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

**Updates windows rotated secret**

**Usage**

```shell Redis
akeyless rotated-secret update windows \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' 
```

**Flags**

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with use-user-creds/use-target-creds

`--password-length`: The length of the password to be generated

`--same-password`: Rotate the same password for each host from the Linked Target (**relevant only for Linked Target**)

`--secure-access-enable`: `Enable`/`Disable` secure remote access, [`true`/`false`]

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after the SRA session ends [`true`/`false`]

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag. (In case of Linked Target association, host(s) will inherit Linked Target hosts - Relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-rdp-user`: Override the **RDP** Domain username

`--secure-access-allow-external-user[=false]`: Allow providing external user for a domain user

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, [`true`/`false`]

## Get

**Get rotated secret value**

**Usage**

```shell
akeyless rotated-secret get-value \
--name <Rotated Secret name> \
--version <Rotated Secret version> \
```

**Flags**

`--host`: Get rotated secret value of specific Host (relevant only for Linked Target)

`--ignore-cache[=false]`: Retrieve the Secret value without checking the Gateway's cache [true/false]. This flag is only relevant when using the RestAPI

## List

**Usage**

```shell
akeyless rotated-secret list \
--gateway-url <API Gateway URL:8000> 
```

## Sync

**Sync rotated secret**

**Usage**

```shell
akeyless rotated-secret sync \
--name <Rotated Secret Name> \
--usc-name <USC Name> \
--remote-secret-name <Remote secret Name> \
--namespace <Namespace Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

Where:

`--name`: The Rotated Secret name.

`--usc-name`: The name of the Universal Secret Connector.

`--remote-secret-name`: Remote Secret name that will be created on the remote endpoint.

`--namespace`: Namespace name, Relevant only for Hashicorp Vault target.

`--filter-secret-value`: JQ expression to filter or transform the secret value

`--gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).