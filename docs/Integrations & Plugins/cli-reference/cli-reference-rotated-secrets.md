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
This section outlines the CLI commands relevant to [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets).

Rotated Secrets enable you to protect the credentials for privileged-user accounts such as an _Administrator_ account on a Windows Server, a **root** account on a Linux server, or an **Admin** account on a network device, by resetting its password.

<CLIGeneralFlags />

## `create`

`akeyless rotated-secret create`

Commands to create a Rotated Secret

### Subcommands

`aws`: Creates a new AWS rotated secret item

`azure`: Creates a new Azure rotated secret item

`cassandra`: Creates a new Cassandra rotated secret item

`custom`: Creates a new custom rotated secret item

`dockerhub`: Creates a new Docker Hub rotated secret item

`gcp`: Creates a new GCP rotated secret item.

`hanadb`: Creates a new SAP HANA database rotated secret item

`ldap`: Creates a new LDAP rotated secret item

`mongodb`: Creates a new MongoDB rotated secret item

`mssql`: Creates a new MSSQL rotated secret item

`mysql`: Creates a new MySQL rotated secret item

`openai`: Creates a new OpenAI rotated secret item

`oracledb`: Creates a new OracleDB rotated secret item

`postgresql`: Creates a new PostgreSQL rotated secret item

`redis`: Creates a new Redis rotated secret item

`redshift`: Creates a new Amazon Redshift rotated secret item

`snowflake`: Creates a new Snowflake rotated secret item

`ssh`: Creates a new SSH rotated secret item

`windows`: Creates a new Windows rotated secret item

### Shared flags

These flags are used by multiple `rotated-secret create` and `rotated-secret update` subcommands.

Permission behavior:

- For credentials-based rotators (for example, `password` rotator flows using `use-user-creds` or `use-target-creds`), creating the rotated secret supports list-only permissions on the associated target.
- For `target` rotator flows, read and update permissions on the target are still required.

`--grace-rotation-timing[=after]`: Controls whether graceful rotation creates the replacement credential before or after the old credential is removed. Supported values are `before` and `after`.

`--lock-during-sra-session`: Lock this rotated secret for read and update while a Secure Remote Access (SRA) session is active.

`--public-key-remote-path`: Remote path where the SSH public key is stored on the target host.

`--secure-access-target-type`: Secure Remote Access target type for SSH rotated secrets.

### `aerospike`

Creates a new Aerospike rotated secret item

#### Usage

```shell
akeyless rotated-secret create aerospike \
--name <Rotated Secret Name> \
--target-name <Target Name> \
--description <Description> \
--rotator-type <target|password> \
--rotated-username <Username to Rotate> \
--rotated-password <Current Password of Rotated User> \
--skip-dry-run <true|false> \
--gateway-url <Gateway URL> \
--key <Encryption Key Name> \
--auto-rotate <true|false> \
--rotation-interval <Rotation Interval> \
--rotation-hour <Rotation Hour (UTC)> \
--rotation-event-in <Days Before Rotation Notification> \
--password-length <Generated Password Length> \
--max-versions <Maximum Number of Versions> \
--input-rule "name=<Rule Name>,rule=<Rule Definition>" \
--output-rule "name=<Rule Name>,rule=<Rule Definition>" \
--ara-enabled <true|false> \
--item-custom-fields <FieldName=Value> \
--password-policy-contains-capital-letters <true|false> \
--password-policy-contains-lower-letters <true|false> \
--password-policy-contains-numbers <true|false> \
--password-policy-contains-special-characters <true|false> \
--authentication-credentials <use-user-creds|use-target-creds> \
--tag <Tag Name> \
--delete-protection <true|false>
```

#### Flags

`-n, --name`: **Required**, Rotated secret name

`-r, --target-name`: **Required**, The target to associate with the rotated secret

`--description`: Description of the object

`--rotator-type`: **Required**, Rotator type. Options: `target`, `password`

`--rotated-username`: Username to rotate. If `use-self-creds` is selected for `--authentication-credentials`, this user rotates its own password. If `use-target-creds` is selected, the target credentials are used to rotate this user's password. Relevant only when `--rotator-type=password`

`--rotated-password`: Current password of the rotated user. Relevant only when `--rotator-type=password`

`--skip-dry-run`: Skip the dry-run validation before creating the rotated secret (`true`/`false`)

`-u, --gateway-url`: Gateway URL (Configuration Management port). Default: `http://localhost:8000`

`-k, --key`: The name of a key used to encrypt the secret value (if empty, the account default `protectionKey` key is used)

`--auto-rotate`: Enable or disable automatic rotation based on the configured rotation interval

`--rotation-interval`: Number of days between automatic rotations (`1-365`). For custom rotators, the interval is set in minutes

`--rotation-hour`: Hour of the automatic rotation in UTC

`--rotation-event-in`: Number of days before rotation when a notification should be sent. To specify multiple notifications, repeat the flag (for example: `--rotation-event-in 1 --rotation-event-in 5`)

`--password-length`: Length of the generated password

`--max-versions`: Maximum number of versions to retain, limited by account settings

`--input-rule`: Agentic input rule in `name=...,rule=...` format. To specify multiple rules, repeat the flag

`--output-rule`: Agentic output rule in `name=...,rule=...` format. To specify multiple rules, repeat the flag

`--ara-enabled`: Enable Agentic Runtime Authority (ARA) rule enforcement (`true`/`false`). When set to `false`, custom input and output rules are not enforced

`--item-custom-fields`: Additional custom fields to associate with the item. To specify multiple fields, repeat the flag (for example: `--item-custom-fields fieldName1=value1`)

`--password-policy-contains-capital-letters`: Require generated passwords to contain at least one uppercase letter (`A-Z`) (`true`/`false`)

`--password-policy-contains-lower-letters`: Require generated passwords to contain at least one lowercase letter (`a-z`) (`true`/`false`)

`--password-policy-contains-numbers`: Require generated passwords to contain at least one numeric character (`0-9`) (`true`/`false`)

`--password-policy-contains-special-characters`: Require generated passwords to contain at least one non-alphanumeric character (for example: `!`, `@`, `#`, `$`) (`true`/`false`)

`--authentication-credentials`: Credentials used to connect and perform the rotation. Options: `use-user-creds`, `use-target-creds`

`-t, --tag`: Add tags to the object. To specify multiple tags, repeat the flag (for example: `--tag Tag1 --tag Tag2`)

`--delete-protection`: Protect the object from accidental deletion (`true`/`false`)

### `aws`

Creates a new AWS rotated secret item

#### Usage

```shell
akeyless rotated-secret create aws \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/api-key>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`api-key`]

`--api-id`: **API ID** to rotate (relevant only for `rotator-type`=`api-key`)

`--api-key`: **API Key** to rotate (relevant only for `rotator-type`=`api-key`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults.

`--grace-rotation`: A boolean flag, when enabled, a graceful mode of rotation will be conducted, where only the older AWS Access Key will be rotated. When there is only one Access Key, a new version will be created - to maintain 2 values at the same time, following AWS [best practice](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_RotateAccessKey).

`--grace-rotation-interval`: The number of days to wait before deleting the old key (must be lower than `rotation-interval`)

`--grace-rotation-hour`: The number of hours of grace rotation allowed in UTC

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-aws-account-id`: The **AWS account ID**

`--aws-region[=us-east-2]`: **AWS** region

`--secure-access-aws-native-cli`: The **AWS** native CLI

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `azure`

Creates a new Azure rotated secret item

#### Usage

```shell
akeyless rotated-secret create azure \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target|api-key|azure-storage-account|password> 
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`api-key`/`azure-storage-account`/`password`]

`--app-id`: ID of the Azure app that holds the secret to be rotated (relevant only for `rotator-type=api-key` and `authentication-credentials=use-target-creds`)

`--api-id`: **API ID** to rotate (relevant only for `rotator-type`=`api-key`)

`--api-key`: **API Key** to rotate (relevant only for `rotator-type`=`api-key`)

`--storage-account-key-name`: The name of the Storage Account key to rotate \[`key1`/`key2`/`kerb1`/`kerb2`] (relevant to `azure-storage-account`)

`--username`: The user principal name to rotate his password (relevant only for `rotator-type`=`password`)

`--explicitly-set-sa[=false]`: If set, explicitly provide the Storage Account details \[`true`/`false`]

`--resource-group-name`: The resource group name (only relevant when `explicitly-set-sa`=`true`)

`--resource-name`: The name of the Storage Account (only relevant when `explicitly-set-sa`=`true`)

`--secure-access-disable-concurrent-connections[=false]`: Enable this flag to prevent simultaneous use of the same secret

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--max-verisons`: Set the maximum number of versions, limited by the account settings defaults

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `cassandra`

Creates a new Cassandra rotated secret item

#### Usage

```shell
 akeyless rotated-secret create cassandra \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password> 
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `custom`

Creates a new custom rotated secret item

#### Usage

```shell
akeyless rotated-secret create custom \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--custom-payload`: Secret payload to be sent with rotation request

`--password-policy-contains-capital-letters`: Password must contain capital letters \[`true`/`false`]

`--password-policy-contains-lower-letters`: Password must contain lower case letters \[`true`/`false`]

`--password-policy-contains-numbers`: Password must contain numbers \[`true`/`false`]

`--password-policy-contains-special-characters`: Password must contain special characters \[`true`/`false`]

`--enable-password-policy`: Enable password policy

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--timeout-sec[=40]`: Maximum allowed timeout in seconds for the custom rotator to return the results

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-web-browsing[=false]`: Secure browser by way of Akeyless Web Access Bastion

`--secure-access-web-proxy[=false]`: Web-Proxy by way of Akeyless Web Access Bastion

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-rdp-user`: Override the **RDP** Domain username

`--secure-access-allow-external-user[=false]`: Allow providing external user for a domain users

`--secure-access-url`: Destination **URL** to inject secrets

`--secure-access-ssh-user`: Override the **SSH username** as indicated in **SSH Certificate Issuer**

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `dockerhub`

Creates a new Docker Hub rotated secret item

#### Usage

```shell
akeyless rotated-secret create dockerhub \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`&#x20;

### `f5-big-ip`

Creates a new F5 BIG-IP rotated secret in the current account.

#### Usage

```shell
akeyless rotated-secret create f5-big-ip \
--name <Rotated Secret Name> \
--target-name <Target Name> \
--rotator-type <target|password> \
```

##### Flags

`-n, --name`: **Required**, Rotated secret name

`-r, --target-name`: **Required**, The F5 BIG-IP target to associate with the rotated secret

`--description`: Description of the object

`--rotator-type`: **Required**, Rotator type. Options: `target`, `password`

`--rotated-username`: Username to rotate. If `use-user-creds` is selected for `--authentication-credentials`, this user rotates its own password. If `use-target-creds` is selected, the target credentials are used to rotate this user's password. Relevant only when `--rotator-type=password`

`--rotated-password`: Current password of the rotated user. Relevant only when `--rotator-type=password`

`--skip-dry-run`: Skip the dry-run validation before creating the rotated secret (`true`/`false`)

`-u, --gateway-url`: Gateway URL (Configuration Management port). Default: `http://localhost:8000`

`-k, --key`: The name of a key used to encrypt the secret value. If empty, the account default `protectionKey` key is used

`--auto-rotate`: Enable or disable automatic rotation based on the configured rotation interval

`--rotation-interval`: Number of days between automatic rotations (`1-365`). For custom rotators, the interval is set in minutes

`--rotation-hour`: Hour of the automatic rotation in UTC

`--rotation-event-in`: Number of days before rotation when a notification should be sent. To specify multiple notifications, repeat the flag (for example: `--rotation-event-in 1 --rotation-event-in 5`)

`--password-length`: Length of the generated password

`--max-versions`: Maximum number of versions to retain, limited by account settings

`--input-rule`: Agentic input rule in `name=...,rule=...` format. To specify multiple rules, repeat the flag

`--output-rule`: Agentic output rule in `name=...,rule=...` format. To specify multiple rules, repeat the flag

`--ara-enabled`: Enable Agentic Runtime Authority (ARA) rule enforcement (`true`/`false`). When set to `false`, custom input and output rules are not enforced

`--item-custom-fields`: Additional custom fields to associate with the item. To specify multiple fields, repeat the flag (for example: `--item-custom-fields fieldName1=value1`)

`--password-policy-contains-capital-letters`: Require generated passwords to contain at least one uppercase letter (`A-Z`) (`true`/`false`)

`--password-policy-contains-lower-letters`: Require generated passwords to contain at least one lowercase letter (`a-z`) (`true`/`false`)

`--password-policy-contains-numbers`: Require generated passwords to contain at least one numeric character (`0-9`) (`true`/`false`)

`--password-policy-contains-special-characters`: Require generated passwords to contain at least one non-alphanumeric character (for example: `!`, `@`, `#`, `$`) (`true`/`false`)

`--authentication-credentials`: Credentials used to connect and perform the rotation. Options: `use-user-creds`, `use-target-creds`

`-t, --tag`: Add tags to the object. To specify multiple tags, repeat the flag (for example: `--tag Tag1 --tag Tag2`)

`--delete-protection`: Protect the object from accidental deletion (`true`/`false`)

### `gcp`

Creates a new GCP rotated secret item

#### Usage

```shell
akeyless rotated-secret create gcp \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/service-account-rotator>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`service-account-rotator`]

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--gcp-key-file-path`: Path to file with the service account private key

`--gcp-key`: `Base64-encoded` service account private key text

`--gcp-service-account-email`: The email of the **GCP** service account to rotate (relevant only when `rotator-type`=`servcie-account-rotator`)

`--gcp-service-account-key-id`: The key ID of the **GCP** service account to rotate (relevant only when `rotator-type`=`servcie-account-rotator`)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--grace-rotation`: A boolean flag, when enabled, a graceful mode of rotation will be conducted, where only the older service account key will be rotated. When there is only one key, a new version will be created to maintain 2 values at the same time.

`--grace-rotation-interval`: The number of days to wait before deleting the old key (must be lower than `rotation-interval`)

`--grace-rotation-hour`: The number of hours of grace rotation allowed in UTC

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `hanadb`

Creates a new SAP HANA database rotated secret item

#### Usage

```shell
akeyless rotated-secret create hanadb \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `ldap`

Creates a new LDAP rotated secret item

#### Usage

```shell
akeyless rotated-secret create ldap \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/ldap>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`ldap`]

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

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--grace-rotation`: Create a new `access key` without deleting the old key from **AWS** for backup (relevant only for AWS) \[`true`/`false`]

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-url`: Destination **URL** to inject secrets

`--host-provider[=explicit]`: Host provider type \[`explicit`/`target`], Relevant only for **Secure Remote Access** of **SSH cert issuer** and **LDAP rotated secret**

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--target`: A list of linked targets to be associated, Relevant only for **Secure Remote Access** for **SSH cert issuer** and **LDAP rotated secret**, To specify multiple targets use argument multiple times

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `mongodb`

Creates a new MongoDB rotated secret item

#### Usage

```shell
akeyless rotated-secret create mongodb \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `mssql`

Creates a new MSSQL rotated secret item

#### Usage

```shell
akeyless rotated-secret create mssql \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-db-schema`: The DB scheme

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `mysql`

Creates a new MySQL rotated secret item

#### Usage

```shell
akeyless rotated-secret create mysql \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `openai`

Creates a new OpenAI rotated secret item

#### Usage

```shell
akeyless rotated-secret create openai \
--name <Rotated Secret name> \
--target-name <Target Name> \
--api-key-id <admin-api-key-id> \
--api-key <admin-api-key> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/api-key>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--api-key-id`: Admin API key ID to rotate (relevant only for `rotator-type=api-key`)

`api-key`: Admin API key value to rotate (relevant only for `rotator-type=api-key`)

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`api-key`]

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

### `oracledb`

Creates a new OracleDB rotated secret item

#### Usage

```shell
akeyless rotated-secret create oracledb \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds`/`use-target-creds`

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `postgresql`

Creates a new PostgreSQL rotated secret item

#### Usage

```shell
akeyless rotated-secret create postgresql \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-db-schema`: The DB scheme

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `redis`

Creates a new Redis rotated secret item

#### Usage

```shell
akeyless rotated-secret create redis \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2\`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `redshift`

Creates a new Amazon Redshift rotated secret item

#### Usage

```shell
akeyless rotated-secret create redshift \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2\`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `snowflake`

Creates a new Snowflake rotated secret item

#### Usage

```shell
akeyless rotated-secret create snowflake \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`password` / `key`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password` or `rotator-type`=`key`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`--private-key`: RSA Private key (Base64-encoded) to rotate (relevant only for `rotator-type`=`key`)

`--private-key-file-name`: The path to the file containing the private key (relevant only for `rotator-type`=`key`)

`--rotation-statement`: Snowflake rotation statement

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2\`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `splunk`

Creates a new Splunk rotated secret item

#### Usage

```shell
akeyless rotated-secret create splunk \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password/token/hec-token> \
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`password`/`token`/`hec-token`]

`--rotated-username`: **username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate it's own password, if `use-target-creds` is selected, target credentials will be use to rotate the rotated-password (relevant only for `rotator-type`=`password`)

`--rotated-password`: rotated-username password (relevant only for `rotator-type`=`password`)

`--token-owner`: Splunk token owner username (relevant only for `rotator-type`=`token`)

`--audience`: Token audience for Splunk token creation (relevant only for `rotator-type`=`token`)

`--splunk-token`: Current Splunk authentication token to store (relevant only for `rotator-type`=`token`). If not provided, a new token will be created in Splunk

`--hec-token-name`: Splunk HEC input name to manage (required for `rotator-type`=`hec-token`)

`--hec-token`: Current Splunk HEC token value to store (relevant only for `rotator-type`=`hec-token`). If not provided, a new HEC input will be created in Splunk

`--expiration-date`: Token expiration date in `YYYY`-`MM`-`DD` format (required for `rotator-type`=`token` when manual rotation is selected and no existing token is provided). Time will be set to `00:00 UTC`

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used).

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation.

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

### `ssh`

Creates a new SSH rotated secret item

#### Usage

```shell
akeyless rotated-secret create ssh \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--same-password`: Rotate the same password for each host from the Linked Target (**relevant only for Linked Target**)

`--rotator-custom-cmd`: Custom rotation command

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-rdp-user`: Override the **RDP** Domain username

`--secure-access-allow-external-user[=false]`: Allow providing external user for a domain users

`--secure-access-ssh-user`: Override the **SSH username** as indicated in **SSH Certificate Issuer**

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2\`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `windows`

Creates a new Windows rotated secret item

#### Usage

```shell
akeyless rotated-secret create windows \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`password`]

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--same-password`: Rotate the same password for each host from the Linked Target (**relevant only for Linked Target**)

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-rdp-user`: Override the **RDP** Domain username

`--secure-access-allow-external-user[=false]`: Allow providing external user for a domain user

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

## `gateway-rotate-secret`

Trigger a rotate operation for a Rotated Secret.
Accepted alias: `rotate-secret`.

### Usage

```shell
akeyless gateway-rotate-secret \
--name <Rotated Secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

### Flags

`-n, --name`: **Required**, Secret name (Rotated Secret or Custom Dynamic Secret)

`-r, --rotate-all-services[=false]`: Rotate all associated services

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

## Synchronization

### `sync`

#### Usage

```shell
akeyless rotated-secret sync \
--name <Rotated Secret Name> \
--usc-name <USC Name> \
--remote-secret-name <Remote secret Name> \
--namespace <Namespace Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`--name`: The Rotated Secret name.

`--usc-name`: The name of the Universal Secret Connector.

`--remote-secret-name`: Remote Secret name that will be created on the remote endpoint.

`--namespace`: Namespace name, Relevant only for HashiCorp Vault target.

`--filter-secret-value`: jq expression to filter or transform the secret value

`--delete-remote`: Delete the remote secret from the USC target during synchronization cleanup

`--gateway-url`: Akeyless Gateway URL (port `8000`).

### `delete sync`

delete rotated secret sync

#### Usage

```shell
akeyless rotated-secret delete-sync \
--name <Rotated Secret Name> \
--usc-name <USC Name> \
--remote-secret-name <Remote secret Name> \
--delete-from-usc[=false] [true / false]
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`--name`: The Rotated Secret name.

`--usc-name`: The name of the Universal Secret Connector.

`--remote-secret-name`: Remote Secret name that will be created on the remote endpoint.

`--delete-from-usc[=false]`: Delete the secret from the remote target usc as well.

`--gateway-url`: Akeyless Gateway URL (port `8000`).

## `update`

`akeyless rotated-secret-update`

Commands to update a Rotated Secret

### Subcommands

`aws`: Updates an AWS rotated secret item

`azure`: Updates an Azure rotated secret item

`cassandra`: Updates a Cassandra rotated secret item

`custom`: Updates a custom rotated secret item

`dockerhub`: Updates a Docker Hub rotated secret item

`gcp`: Updates a GCP rotated secret item.

`hanadb`: Updates a SAP HANA database rotated secret item

`ldap`: Updates a LDAP rotated secret item

`mongodb`: Updates a MongoDB rotated secret item

`mssql`: Updates a MSSQL rotated secret item

`mysql`: Updates a MySQL rotated secret item

`oracledb`: Updates an OracleDB rotated secret item

`postgresql`: Updates a PostgreSQL rotated secret item

`redis`: Updates a Redis rotated secret item

`redshift`: Updates a Redshift rotated secret item

`snowflake`: Updates a Snowflake rotated secret item

`ssh`: Updates a SSH rotated secret item

`windows`: Updates a Windows rotated secret item

### `aerospike`

#### Usage

```shell
akeyless rotated-secret create aerospike \
--name <Rotated Secret Name> \
--new-name <New item name> \
--target-name <Target Name> \
--description <Description> \
--rotator-type <target|password> \
--rotated-username <Username to Rotate> \
--rotated-password <Current Password of Rotated User> \
--skip-dry-run <true|false> \
--gateway-url <Gateway URL> \
--key <Encryption Key Name> \
--auto-rotate <true|false> \
--rotation-interval <Rotation Interval> \
--rotation-hour <Rotation Hour (UTC)> \
--rotation-event-in <Days Before Rotation Notification> \
--password-length <Generated Password Length> \
--max-versions <Maximum Number of Versions> \
--input-rule "name=<Rule Name>,rule=<Rule Definition>" \
--output-rule "name=<Rule Name>,rule=<Rule Definition>" \
--ara-enabled <true|false> \
--item-custom-fields <FieldName=Value> \
--password-policy-contains-capital-letters <true|false> \
--password-policy-contains-lower-letters <true|false> \
--password-policy-contains-numbers <true|false> \
--password-policy-contains-special-characters <true|false> \
--authentication-credentials <use-user-creds|use-target-creds> \
--tag <Tag Name> \
--delete-protection <true|false>
```

#### Flags

`-n, --name`: **Required**, Rotated secret name

`--new-name`: New item name

`-r, --target-name`: **Required**, The target to associate with the rotated secret

`--description`: Description of the object

`--rotator-type`: **Required**, Rotator type. Options: `target`, `password`

`--rotated-username`: Username to rotate. If `use-self-creds` is selected for `--authentication-credentials`, this user rotates its own password. If `use-target-creds` is selected, the target credentials are used to rotate this user's password. Relevant only when `--rotator-type=password`

`--rotated-password`: Current password of the rotated user. Relevant only when `--rotator-type=password`

`--skip-dry-run`: Skip the dry-run validation before creating the rotated secret (`true`/`false`)

`-u, --gateway-url`: Gateway URL (Configuration Management port). Default: `http://localhost:8000`

`-k, --key`: The name of a key used to encrypt the secret value (if empty, the account default `protectionKey` key is used)

`--auto-rotate`: Enable or disable automatic rotation based on the configured rotation interval

`--rotation-interval`: Number of days between automatic rotations (`1-365`). For custom rotators, the interval is set in minutes

`--rotation-hour`: Hour of the automatic rotation in UTC

`--rotation-event-in`: Number of days before rotation when a notification should be sent. To specify multiple notifications, repeat the flag (for example: `--rotation-event-in 1 --rotation-event-in 5`)

`--password-length`: Length of the generated password

`--max-versions`: Maximum number of versions to retain, limited by account settings

`--input-rule`: Agentic input rule in `name=...,rule=...` format. To specify multiple rules, repeat the flag

`--output-rule`: Agentic output rule in `name=...,rule=...` format. To specify multiple rules, repeat the flag

`--ara-enabled`: Enable Agentic Runtime Authority (ARA) rule enforcement (`true`/`false`). When set to `false`, custom input and output rules are not enforced

`--item-custom-fields`: Additional custom fields to associate with the item. To specify multiple fields, repeat the flag (for example: `--item-custom-fields fieldName1=value1`)

`--password-policy-contains-capital-letters`: Require generated passwords to contain at least one uppercase letter (`A-Z`) (`true`/`false`)

`--password-policy-contains-lower-letters`: Require generated passwords to contain at least one lowercase letter (`a-z`) (`true`/`false`)

`--password-policy-contains-numbers`: Require generated passwords to contain at least one numeric character (`0-9`) (`true`/`false`)

`--password-policy-contains-special-characters`: Require generated passwords to contain at least one non-alphanumeric character (for example: `!`, `@`, `#`, `$`) (`true`/`false`)

`--authentication-credentials`: Credentials used to connect and perform the rotation. Options: `use-user-creds`, `use-target-creds`

`-t, --tag`: Add tags to the object. To specify multiple tags, repeat the flag (for example: `--tag Tag1 --tag Tag2`)

`--delete-protection`: Protect the object from accidental deletion (`true`/`false`)

### `aws`

#### Usage

```shell
akeyless rotated-secret update aws \
--name <Rotated Secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--new-name <New Item name>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New item name

`--api-id`: **API ID** to rotate (relevant only for `rotator-type`=`api-key`)

`--api-key`: **API Key** to rotate (relevant only for `rotator-type`=`api-key`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--grace-rotation`: A boolean flag, when enabled, a graceful mode of rotation will be conducted, where only the older AWS Access Key will be rotated. When there is only one Access Key, a new version will be created - to maintain 2 values at the same time, following AWS [best practice](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_RotateAccessKey).

`--grace-rotation-interval`: The number of days to wait before deleting the old key (must be lower than `rotation-interval`)

`--grace-rotation-hour`: The number of hours of grace rotation allowed in UTC

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-aws-account-id`: The **AWS account ID**

`--aws-region[=us-east-2]`: **AWS** region

`--secure-access-aws-native-cli`: The **AWS** native CLI

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `azure`

#### Usage

```shell
akeyless rotated-secret update azure \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--app-id`: ID of the Azure app that hold the secret to be rotated (relevant only for `rotator-type=api-key` and `authentication-credentials=use-target-creds`)

`--api-id`: **API ID** to rotate (relevant only for `rotator-type=api-key`)

`--api-key`: **API Key** to rotate (relevant only for `rotator-type=api-key`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--storage-account-key-name`: The name of the Storage Account key to rotate \[`key1`/`key2`/`kerb1`/`kerb2`] (relevant to `azure-storage-account`)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--grace-rotation`: A boolean flag, when enabled, a graceful mode of rotation will be conducted, where only the older secret will be rotated. When there is only one secret, a new version will be created - to maintain 2 values at the same time. Relevant only for **Client Secret**.

`--grace-rotation-interval`: The number of days to wait before deleting the old key (must be lower than `rotation-interval`)

`--grace-rotation-hour`: The number of hours of grace rotation allowed in UTC

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `cassandra`

#### Usage

```shell
 akeyless rotated-secret update cassandra \
--name <Rotated Secret name> \
--new-name <New-Item name>
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

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

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `custom`

#### Usage

```shell
akeyless rotated-secret update custom \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--custom-payload`: Secret payload to be sent with rotation request

`--password-policy-contains-capital-letters`: Password must contain capital letters \[`true`/`false`]

`--password-policy-contains-lower-letters`: Password must contain lower case letters \[`true`/`false`]

`--password-policy-contains-numbers`: Password must contain numbers \[`true`/`false`]

`--password-policy-contains-special-characters`: Password must contain special characters \[`true`/`false`]

`--enable-password-policy`: Enable password policy

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--timeout-sec[=40]`: Maximum allowed timeout in seconds for the custom rotator to return the results

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-web-browsing[=false]`: Secure browser by way of Akeyless Web Access Bastion

`--secure-access-web-proxy[=false]`: Web-Proxy by way of Akeyless Web Access Bastion

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-rdp-user`: Override the **RDP** Domain username

`--secure-access-allow-external-user[=false]`: Allow providing external user for a domain users

`--secure-access-url`: Destination **URL** to inject secrets

`--secure-access-ssh-user`: Override the **SSH username** as indicated in **SSH Certificate Issuer**

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `dockerhub`

#### Usage

```shell
akeyless rotated-secret update dockerhub \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

### `f5-big-ip`

Updates an existing F5 BIG-IP rotated secret in the current account.

#### Usage

```shell
akeyless rotated-secret update f5-big-ip \
--name <Rotated Secret Name> \
--new-name <New Item Name> \
--target-name <Target Name> \
--rotator-type <target|password> \
```

##### Flags

`-n, --name`: **Required**, Rotated secret name

`--new-name`: New Item name

`-r, --target-name`: **Required**, The F5 BIG-IP target to associate with the rotated secret

`--description`: Description of the object

`--rotator-type`: **Required**, Rotator type. Options: `target`, `password`

`--rotated-username`: Username to rotate. If `use-user-creds` is selected for `--authentication-credentials`, this user rotates its own password. If `use-target-creds` is selected, the target credentials are used to rotate this user's password. Relevant only when `--rotator-type=password`

`--rotated-password`: Current password of the rotated user. Relevant only when `--rotator-type=password`

`--skip-dry-run`: Skip the dry-run validation before creating the rotated secret (`true`/`false`)

`-u, --gateway-url`: Gateway URL (Configuration Management port). Default: `http://localhost:8000`

`-k, --key`: The name of a key used to encrypt the secret value. If empty, the account default `protectionKey` key is used

`--auto-rotate`: Enable or disable automatic rotation based on the configured rotation interval

`--rotation-interval`: Number of days between automatic rotations (`1-365`). For custom rotators, the interval is set in minutes

`--rotation-hour`: Hour of the automatic rotation in UTC

`--rotation-event-in`: Number of days before rotation when a notification should be sent. To specify multiple notifications, repeat the flag (for example: `--rotation-event-in 1 --rotation-event-in 5`)

`--password-length`: Length of the generated password

`--max-versions`: Maximum number of versions to retain, limited by account settings

`--input-rule`: Agentic input rule in `name=...,rule=...` format. To specify multiple rules, repeat the flag

`--output-rule`: Agentic output rule in `name=...,rule=...` format. To specify multiple rules, repeat the flag

`--ara-enabled`: Enable Agentic Runtime Authority (ARA) rule enforcement (`true`/`false`). When set to `false`, custom input and output rules are not enforced

`--item-custom-fields`: Additional custom fields to associate with the item. To specify multiple fields, repeat the flag (for example: `--item-custom-fields fieldName1=value1`)

`--password-policy-contains-capital-letters`: Require generated passwords to contain at least one uppercase letter (`A-Z`) (`true`/`false`)

`--password-policy-contains-lower-letters`: Require generated passwords to contain at least one lowercase letter (`a-z`) (`true`/`false`)

`--password-policy-contains-numbers`: Require generated passwords to contain at least one numeric character (`0-9`) (`true`/`false`)

`--password-policy-contains-special-characters`: Require generated passwords to contain at least one non-alphanumeric character (for example: `!`, `@`, `#`, `$`) (`true`/`false`)

`--authentication-credentials`: Credentials used to connect and perform the rotation. Options: `use-user-creds`, `use-target-creds`

`-t, --tag`: Add tags to the object. To specify multiple tags, repeat the flag (for example: `--tag Tag1 --tag Tag2`)

`--delete-protection`: Protect the object from accidental deletion (`true`/`false`)

### `gcp`

#### Usage

```shell
akeyless rotated-secret update gcp \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`service-account-rotator`]

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--gcp-key-file-path`: Path to file with the service account private key

`--gcp-key`: `Base64-encoded` service account private key text

`--gcp-service-account-email`: The email of the **GCP** service account to rotate (relevant only when `rotator-type`=`servcie-account-rotator`)

`--gcp-service-account-key-id`: The key ID of the **GCP** service account to rotate (relevant only when `rotator-type`=`servcie-account-rotator`)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--rotation-hour`: The Hour of the rotation in **UTC**

`--grace-rotation`: A boolean flag, when enabled, a graceful mode of rotation will be conducted, where only the older service account key will be rotated. When there is only one key, a new version will be created to maintain 2 values at the same time.

`--grace-rotation-interval`: The number of days to wait before deleting the old key (must be lower than `rotation-interval`)

`--grace-rotation-hour`: The number of hours of grace rotation allowed in UTC

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `hanadb`

#### Usage

```shell
akeyless rotated-secret update hanadb \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `ldap`

#### Usage

```shell
akeyless rotated-secret update ldap \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

#### Flags

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

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--grace-rotation`: Create a new `access key` without deleting the old key from **AWS** for backup (relevant only for AWS) \[`true`/`false`]

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-url`: Destination **URL** to inject secrets

`--host-provider[=explicit]`: Host provider type \[`explicit`/`target`], Relevant only for **Secure Remote Access** of **SSH cert issuer** and **LDAP rotated secret**

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--target`: A list of linked targets to be associated, Relevant only for **Secure Remote Access** for **SSH cert issuer** and **LDAP rotated secret**, To specify multiple targets use argument multiple times

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `mongodb`

#### Usage

```shell
akeyless rotated-secret update mongodb \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

#### Flags

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

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `mssql`

#### Usage

```shell
akeyless rotated-secret update mssql \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

#### Flags

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

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `mysql`

#### Usage

```shell
akeyless rotated-secret update mysql \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

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

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `openai`

Updates a new OpenAI rotated secret item

#### Usage

```shell
akeyless rotated-secret update openai \
--name <Rotated Secret name> \
--new-name <New Item name>
--api-key-id <admin-api-key-id> \
--api-key <admin-api-key> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New item name

`--api-key-id`: Admin API key ID to rotate (relevant only for `rotator-type=api-key`)

`api-key`: Admin API key value to rotate (relevant only for `rotator-type=api-key`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

### `oracledb`

#### Usage

```shell
akeyless rotated-secret update oracledb \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

#### Flags

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

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`-t, --tag`: Add tags attached to this object. To specify multiple tags use the argument multiple times: `--tag Tag1` `-t Tag2`

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `postgresql`

#### Usage

```shell
akeyless rotated-secret update postgresql \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

#### Flags

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

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--secure-access-web[=false]`: Enable Web Secure Remote Access

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-db-schema`: The DB scheme

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `redis`

#### Usage

```shell
akeyless rotated-secret update redis \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

#### Flags

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

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `redshift`

#### Usage

```shell
akeyless rotated-secret update redshift \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

#### Flags

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

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-db-name`: The DB name (relevant only for DB)

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `snowflake`

#### Usage

```shell
akeyless rotated-secret update snowflake \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password>
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--rotated-username`: **Username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate its password, if `use-target-creds` is selected, target credentials will be used to rotate the rotated password (relevant only for `rotator-type`=`password` or `rotator-type`=`key`)

`--rotated-password`: Rotated-username password (relevant only for `rotator-type`=`password`)

`--private-key`: RSA Private key (Base64-encoded) to rotate (relevant only for `rotator-type`=`key`)

`--private-key-file-name`: The path to the file containing the private key (relevant only for `rotator-type`=`key`)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used)

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `splunk`

Updates a new Splunk rotated secret item

#### Usage

```shell
akeyless rotated-secret update splunk \
--name <Rotated Secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target/password/token/hec-token> \
```

#### Flags

`-n, --name`: **Required**, Rotated Secret name

`--new-name`: New Item name

`--target-name`: **Required**, the target name to associate

`--rotator-type`: **Required**, The rotator type. options: \[`target`/`password`/`token`/`hec-token`]

`--rotated-username`: **username** to be rotated, if selected `use-self-creds` at `rotator-creds-type`, this **username** will try to rotate it's own password, if `use-target-creds` is selected, target credentials will be use to rotate the rotated-password (relevant only for `rotator-type`=`password`)

`--rotated-password`: rotated-username password (relevant only for `rotator-type`=`password`)

`--token-owner`: Splunk token owner username (relevant only for `rotator-type`=`token`)

`--audience`: Token audience for Splunk token creation (relevant only for `rotator-type`=`token`)

`--splunk-token`: Current Splunk authentication token to store (relevant only for `rotator-type`=`token`). If not provided, a new token will be created in Splunk

`--hec-token-name`: Splunk HEC input name to manage (required for `rotator-type`=`hec-token`)

`--hec-token`: Current Splunk HEC token value to store (relevant only for `rotator-type`=`hec-token`). If not provided, a new HEC input will be created in Splunk

`--expiration-date`: Token expiration date in `YYYY`-`MM`-`DD` format (required for `rotator-type`=`token` when manual rotation is selected and no existing token is provided). Time will be set to `00:00 UTC`

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default **protection key** will be used).

`--auto-rotate`: Whether to automatically rotate every `--rotation-interval` days, or disable existing automatic rotation.

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365), custom rotator interval will be set in minutes

`--rotation-hour`: The Hour of the rotation in **UTC**

`--rotation-event-in`: How many days before auto rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

### `ssh`

#### Usage

```shell
akeyless rotated-secret update ssh \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

#### Flags

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

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--same-password`: Rotate the same password for each host from the Linked Target (**relevant only for Linked Target**)

`--rotator-custom-cmd`: Custom rotation command

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-bastion-issuer`: Path to the **SSH Certificate Issuer** for your **Akeyless Bastion**

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-rdp-user`: Override the **RDP** Domain username

`--secure-access-allow-external-user[=false]`: Allow providing external user for a domain users

`--secure-access-ssh-user`: Override the **SSH username** as indicated in **SSH Certificate Issuer**

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

### `windows`

#### Usage

```shell
akeyless rotated-secret update windows \
--name <Rotated Secret name> \
--new-name <New Item name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

#### Flags

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

`--authentication-credentials[=use-user-creds]`: The credentials to connect with `use-user-creds` or `use-target-creds`

`--password-length`: The length of the password to be generated

`--same-password`: Rotate the same password for each host from the Linked Target (**relevant only for Linked Target**)

`--secure-access-enable`: `Enable`/`Disable` Secure Remote Access, \[`true`/`false`]

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA \[use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

`--secure-access-host`: Target servers for connections. For multiple values, repeat this flag. (If a Linked Target is associated, hosts will inherit Linked Target hosts - relevant only for **Dynamic Secrets**/**producers**)

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user

`--secure-access-rdp-user`: Override the **RDP** Domain username

`--secure-access-allow-external-user[=false]`: Allow providing external user for a domain user

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use the argument multiple times: `--add-tag Tag1` `--add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use the argument multiple times: `--rm-tag Tag1` `--rm-tag Tag2`

`--keep-prev-version`: Whether to keep the previous version, options:\[`true`, `false`]. If not set, use default according to account settings

`--delete-protection`: Protection from accidental deletion of this item, \[`true`/`false`]

## Retrieve Information

### `get-value`

#### Usage

```shell
akeyless rotated-secret get-value \
--name <Rotated Secret name> \
--version <Rotated Secret version>
```

#### Flags

`--host`: Get rotated secret value of specific Host (relevant only for Linked Target)

`--ignore-cache[=false]`: Retrieve the Secret value without checking the Gateway's cache \[true/false]. This flag is only relevant when using the REST API

### `list`

#### Usage

```shell
akeyless rotated-secret list \
--gateway-url <API Gateway URL>:8000 
```

## Synchronization

### `sync`

#### Usage

```shell
akeyless rotated-secret sync \
--name <Rotated Secret Name> \
--usc-name <USC Name> \
--remote-secret-name <Remote secret Name> \
--namespace <Namespace Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`--name`: The Rotated Secret name.

`--usc-name`: The name of the Universal Secret Connector.

`--remote-secret-name`: Remote Secret name that will be created on the remote endpoint.

<Callout icon="ℹ️" theme="info">
  ### **Note (AWS Targets):**

  For AWS Universal Secret Connector targets, Akeyless-initiated sync updates secret values while preserving existing AWS-side custom tags and description unless those fields are explicitly updated.
</Callout>

`--namespace`: Namespace name, Relevant only for HashiCorp Vault target.

`--filter-secret-value`: jq expression to filter or transform the secret value

`--gateway-url`: Akeyless Gateway URL (port `8000`).

### `delete sync`

delete rotated secret sync

#### Usage

```shell
akeyless rotated-secret delete-sync \
--name <Rotated Secret Name> \
--usc-name <USC Name> \
--remote-secret-name <Remote secret Name> \
--delete-from-usc[=false] [true / false]
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`--name`: The Rotated Secret name.

`--usc-name`: The name of the Universal Secret Connector.

`--remote-secret-name`: Remote Secret name that will be created on the remote endpoint.

`--delete-from-usc[=false]`: Delete the secret from the remote target usc as well.

`--gateway-url`: Akeyless Gateway URL (port `8000`).
