---
title: CLI Reference
slug: cli-reference
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
This section describes the available CLI commands that you can use when working with Akeyless.
If you need help in context, check out the help flag (`-h`)

<CLIGeneralFlags />

```shell
akeyless -h
akeyless <command> -h, --help
akeyless <command> --debug
```

## Commands

### `configure`

Configure client profile

For profile creation, default-profile behavior, and precedence rules, see [CLI Profiles](https://docs.akeyless.io/docs/cli-profiles).

#### Usage

```shell
akeyless configure
```

#### Flags

`--profile[=default]`: The profile name to be configure

`--access-id`: Access ID

`--access-key`: Access Key

`--access-type[=access_key]`: Access Type, options: `[access_key/password/azure_ad/saml/oidc/aws_iam/gcp/k8s]`

`--admin-password`: Password (relevant only for `access-type=password`)

`--admin-email`: Email (relevant only for `access-type=password`)

`--oidc-sp`: OIDC Service Provider (relevant only for `access-type=oidc`, inferred if empty), supported SPs: google, github

`--azure-ad-object-id`: Azure Active Directory ObjectId (relevant only for access-type=azure_ad)

`--azure-cloud[=AzureCloud]`: Azure cloud environment to use. Values: `AzureCloud` (default), `AzureUSGovernment`, `AzureChinaCloud` (relevant only for `access-type=azure_ad`)

`--gcp-audience`: GCP audience to use in signed JWT (relevant only for access-type=gcp)

`--gateway-url`: Gateway URL for the Kubernetes authenticated (relevant only for `access-type=k8s`)

`--k8s-auth-config-name`: The Kubernetes Auth config name (relevant only for `access-type=k8s`)

`--k8s-token-path[=/var/run/secrets/kubernetes.io/serviceaccount/token]`: An optional path to a projected service account token inside the pod, for use instead of the default service account token (relevant only for `access-type=k8s`)

`--cert-file-name`: Name of the certificate file to use (relevant only for `access-type=cert`)

`--cert-data`: Certificate data encoded in Base64. Used if file was not provided. (relevant only for `access-type=cert` in Curl Context)

`--key-file-name`: Name of the private key file to use (relevant only for `access-type=cert`)

`--key-data`: Private key data encoded in Base64. Used if file was not provided (relevant only for `access-type=cert` in Curl Context)

### `delete-item`

Delete an item or an item version

#### Usage

```shell
akeyless delete-item -n <Item name>
```

#### Flags

`-n, --name`: Required, Item name

`--version[=-1]`: The specific version you want to delete - 0=last version, -1=entire item with all versions (default)

`--delete-in-days`: The number of days to wait before deleting the item (relevant for keys only)

`--delete-immediately[=false]`: When delete-in-days=-1, must be set

`--accessibility[=regular]`: For an item in a user's personal folder [regular/personal]

### `delete-items`

Deletes multiple items from a given path

#### Usage

```shell
akeyless delete-items -p <Path\do\delete\items>
```

#### Flags

`-p, --path`: Required, Path to delete the items from

### `describe-item`

Gets the item details

#### Flags

`-n, --name`: Item name

`-d, --display-id`: The display ID of the item

`-I, --item-id`: Item ID of the item

`--show-versions[=false]`: Include all item versions in reply

`--gateway-details[=false]`: Output will include additional gateway details (For example, cluster URL)

`--bastion-details[=false]`: Output will include additional bastion details

`--services-details[=false]`: Include all associated services details

`--accessibility[=regular]`: For an item in a user's personal folder [regular/personal]

#### Output

With only `--name` specified, the command returns all details about the specified item except for its version.

When a version number is specified, the command returns all details about the specified item for the specified version.

When `--show-versions` is specified, the command returns all details about the specified item including a full list of versions, their creation dates, and their encryption keys for any version for which a key other than the default was used.

### `get-account-settings`

Get the settings of the account

### `get-cloud-identity`

Get a Cloud Identity token.

#### Usage

```shell
akeyless get-cloud-identity --cloud-provider <cloud provider>
```

#### Flags

`--cloud-provider`: Cloud provider (`azure_ad/aws_iam/gcp/oci`)

`--azure_ad_object_id`: Azure Active Directory ObjectId (relevant only for `cloud-provider=azure_ad`)

`--azure-cloud[=AzureCloud]`: Azure cloud environment to use. Values: `AzureCloud` (default), `AzureUSGovernment`, `AzureChinaCloud`

`--gcp-audience[=akeyless.io]`: GCP audience to use in signed JWT (relevant only for `cloud-provider=gcp`)

`--oci-auth-type[=apikey]`: The type of the OCI configuration to use `[instance/apikey/resource]` (relevant only for `cloud-provider=oci`)

`--oci-group-ocid`: A list of required groups OCIDs (relevant only for `cloud-provider=oci`)

`--describe-sub-claims`: Describe the cloud identity sub-claims

`--url_safe`: Escapes the token so it can be safely placed inside a URL query

`--debug[=false]`: Turn on debug logging

For broader authentication context, see [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#get-cloud-identity).

### `get-default-profile`

Display current default profile information.

For default-profile behavior and precedence, see [CLI Profiles](https://docs.akeyless.io/docs/cli-profiles).

#### Usage

```shell
akeyless get-default-profile
```

#### Flags

`--profile, --token`: Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temporary access token

`--uid-token`: The universal identity token (required only for `universal_identity` authentication)

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired credentials

### `get-tags`

Get all tags of selected item

#### Usage

```shell
akeyless get-tags --name <Item Name>
```

#### Flags

`-n, --name`: Required, The item name

### `list-items`

List of all accessible items

#### Flags

`-t, --type`: The item types list of the requested items. If it is empty, all item types are returned, options: [key, static-secret, dynamic-secret, rotated-secret, ssh-cert-issuer, pki-cert-issuer, classic-key]

`--sub-types`: Optional the items sub types

`--filter`: Filter by item name or part of it

`--tag`: Filter by item tag

`--sra-only[=false]`: Filter by items with SRA functionality enabled

`--path`: Path to folder

`--pagination-token`: Next page reference

`--auto-pagination[=enabled]`: Retrieve all items using pagination, when disabled retrieving only first 1000 items

`--minimal-view`: Show only basic information of the items

`--accessibility[=regular]`: For an item in a user's personal folder, options: [regular/personal]

### `list-sra-bastions`

Lists all Secure Remote Access (SRA) bastions in the account.

For command usage, flags, and behavior notes, see [CLI Reference - Gateway Secure Remote Access](https://docs.akeyless.io/docs/cli-reference-sra).

### `move-objects`

Moves or renames folders and their contents in bulk. Both `--source` and `--target` must be folder paths. This command does not move an individual object.

#### Usage

```shell
akeyless move-objects --source <Source path to move the objects from> \
--target <Target path to move the objects to> \
--objects-type <The objects type to move (item/auth_method/role)>
```

#### Flags

`-s, --source`: Required, Source path to move the objects from

`-t, --target`: Required, Target path to move the objects to

`-o, --objects-type[=item]`: The objects type to move (item/auth_method/role)

### `set-item-state`

Set an item's state (Enabled, Disabled)

#### Usage

```shell
akeyless set-item-state --name <Current item name> \
--desired-state <Desired item state [Enabled, Disabled]>
```

#### Flags

`-n, --name`: Required, Current item name

`-s, --desired-state`: Required, Desired item state

### `set-default-profile`

Set the default profile for CLI commands.

This command sets the default profile used when `--profile` is not specified and persists the value in `~/.akeyless/settings`.

For default-profile behavior and precedence, see [CLI Profiles](https://docs.akeyless.io/docs/cli-profiles).

#### Usage

```shell
akeyless set-default-profile --profile <Profile name>
```

#### Flags

`--profile`: The profile name to set as default

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired credentials

### `unconfigure`

Remove configuration of client profile

#### Usage

```shell
akeyless unconfigure --profile <Profile name>
```

### `update`

Update the Akeyless CLI version or change to a prior version

#### Usage

```shell
akeyless update
```

#### Flags

`-v, --version[=latest]`: Provide the CLI version to update to, by default, the latest version is used

`-s, --show-changelog`: Show the changelog between the current version and the latest version

`-r, --artifact-repository`: Alternative CLI repository URL, for example, `https://artifacts.site2.akeyless.io`

### `update-account-settings`

Updates account settings.

Note: The operation is allowed only for admin user

#### Flags

`--company-name`: Update Company Name of account

`--phone`: Update Phone number of account

`--address`: Update Address of account

`--city`: Update City of account

`--country`: Update Country of account

`--postal-code`: Update Postal Code of account

`--jwt-ttl-default`: default JWT TTL for Auth Method authentication (in minutes)

`--jwt-ttl-min`: minimum allowed JWT TTL for Auth Method authentication (in minutes)

`--jwt-ttl-max`: maximum allowed JWT TTL for Auth Method authentication (in minutes)

`--max-versions`: Maximum versions of a given item-type, valid range [`1`, `300`]. When item version exceeds this number, the oldest versions will be deleted

`--item-type`: Associated with max-versions

`--default-versioning`: If set to true, new item version will be created on each update

`--force-new-versions`: If set to true, new version will be created on update

`--dp-enable-classic-key-protection`: Set to update protection with classic keys state meter

`--default-sharing-link-ttl`: Set to update the default TTL in minutes for sharing item, number between 60 min to 30 days (`43200` minute)

`--password-policy-password-length`: "13-1": "Password length between 5 - to 50 characters

`--password-policy-contains-capital-letters`: Password must contain capital letters

`--password-policy-contains-lower-letters`: Password must contain lower case letters

`--password-policy-contains-numbers`: Password must contain numbers

`--password-policy-contains-special-characters`: Password must contain special characters

`--items-deletion-protection`: Set to update the default behavior of new items creations deletion protection attribute [true/false]

`--default-key-name`: Set the account default key based on the DFC key item name. Use "set-original-akeyless-default-key" to revert to using the original default key of the account. Empty string will change nothing

`--invalid-characters[=notReceivedInvalidCharacter]`: Characters that cannot be used for items/targets/roles/auths/event_forwarder names

`--lock-default-key`: Lock the account's default protection key, if set - users will not be able to use a different protection key, relevant only if default-key-name is configured [true/false]

`--usage-event-enable`: Enable event for objects that have not been used or changed [true/false]

`--usage-event-object-type`: Usage event is supported for Auth Method or secrets-and-keys [auth/item]

`--usage-event-interval`: Interval by days for unused objects. Default and minimum interval is 90 days

`--dynamic-secret-max-ttl-enable`: Set a maximum TTL for Dynamic Secrets [true/false]

`--dynamic-secret-max-ttl`: Set the maximum TTL for Dynamic Secrets

`--max-rotation-interval-enable`: Set a maximum rotation interval for Rotated Secrets auto rotation settings [true/false]

`--max-rotation-interval`: Set the maximum rotation interval for Rotated Secrets auto rotation settings

`--bound-ips`: A default list of comma-separated CIDR block that are allowed to authenticate

`--lock-bound-ips`: Lock bound-ips setting globally in the account

`--gw-bound-ips`: A default list of comma-separated CIDR block that acts as a trusted Gateway entity

`--lock-gw-bound-ips`: Lock bound-ips setting globally in the account

`--enable-password-expiration`: Enable password expiration policy [`true`/`false`]

`--password-expiration-days`: Specifies the number of days that a password is valid before it must be changed. A default value of 90 days is used

`--password-expiration-notification-days`: Specifies the number of days before a user receives notification that their password will expire. A default value of 14 days is used

`--hide-personal-folder`: Controls the visibility of the personal folder, this setting hides the personal folder for users.

`--hide-static-password`: Hide static secret's password type [`true`/`false`].

`--enable-default-certificate-expiration-event`: Enable how many days before the expiration of the certificate would you like to be notified. [`true`/`false`].

`--default-certificate-expiration-notification-days`: How many days before the expiration of the certificate would you like to be notified. To specify multiple events, use argument multiple times: `--default-certificate-expiration-notification-days 1`, `--default-certificate-expiration-notification-days 5`.

### `update-item`

Update item name and description

> **Critical:**
>
> **Secret versioning**
>
> No updates made with `update-item` can be saved as part of new versions, which means that these changes override existing data. If you wish to track these updates as part of secret versioning, first create a new version with `update-version-val`. You can create a new version value using the same value for the current version if you don't want to actually change the value. Thereafter, run `update-item`.

#### Usage

```shell
akeyless update-item --name <Item name> \
--new-name <New item name>
```

#### Flags

`-n, --name`: Required, Current item name

`--new-name`: New item name

`--description[=default_metadata]`: Description of the object

`--add-tag`: List of new tags to attach to this item. To specify multiple tags, repeat the flag: `--add-tag Tag1 --add-tag Tag2`

`--rm-tag`: List of existing tags to remove from this item. To specify multiple tags, repeat the flag: `--rm-tag Tag1 --rm-tag Tag2`

`--max-versions`: Set the maximum number of versions, limited by account settings defaults

`--secure-access-enable`: Enable or disable Secure Remote Access [`true`/`false`]

`--secure-access-certificate-issuer`: Path to the SSH Certificate Issuer for Akeyless Secure Access

`--secure-access-api`: Secure Access SSH control API endpoint, for example `https://my.sra-server:9900` (relevant only for SSH cert issuer)

`--secure-access-ssh`: Secure Access SSH server, for example `my.sra-server:22` (relevant only for SSH cert issuer)

`--secure-access-ssh-creds-user`: SSH username used to connect to target server, and must be in the allowed users list (relevant only for SSH cert issuer)

`--secure-access-use-internal-ssh-access`: Use internal SSH access

`--secure-access-ssh-creds`: Secret values that contain SSH credentials, either private key or password [`password`/`private-key`] (relevant only for Static Secret or Rotated Secret)

`--secure-access-host`: Target servers for connections. To specify multiple hosts, repeat this flag

`--secure-access-add-host`: List of new hosts to attach to SRA servers host. To specify multiple hosts, repeat the flag: `--secure-access-add-host host1 --secure-access-add-host host2`

`--secure-access-rm-host`: List of existing hosts to remove from SRA servers host. To specify multiple hosts, repeat the flag: `--secure-access-rm-host host1 --secure-access-rm-host host2`

`--secure-access-url`: Destination URL to inject secrets

`--secure-access-web-browsing[=false]`: Secure browser via Akeyless Secure Remote Access (SRA)

`--secure-access-web-proxy[=false]`: Web proxy via Akeyless Secure Remote Access (SRA)

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user (relevant only for RDP Dynamic Secret)

`--secure-access-rdp-user`: Override the RDP domain username

`--secure-access-rd-gateway-server`: RD Gateway server (relevant only for RDP)

`--secure-access-allow-external-user`: Allow providing an external user for domain users [`true`/`false`]

`--secure-access-db-schema`: DB schema (relevant only for DB Dynamic Secret)

`--secure-access-db-name`: DB name (relevant only for DB)

`--secure-access-aws-account-id`: AWS account ID (relevant only for AWS)

`--secure-access-aws-region`: AWS region (relevant only for AWS)

`--secure-access-aws-native-cli`: AWS native CLI (relevant only for AWS)

`--secure-access-cluster-endpoint`: Kubernetes cluster endpoint URL (relevant only for EKS/GKE/K8s Dynamic Secret)

`--secure-access-dashboard-url`: Kubernetes dashboard URL (relevant only for Kubernetes)

`--secure-access-allow-port-forwading`: Enable port forwarding when using CLI access (relevant only for EKS/GKE/K8s Dynamic Secret)

`--host-provider`: Host provider type [`explicit`/`target`] (relevant only for Secure Remote Access of SSH cert issuer, LDAP rotated secret, and LDAP dynamic secret)

`--secure-access-gateway`: Defines which Gateway (Gateway URL) is related to a secret item

`--rotate-after-disconnect[=false]`: Post-session rotation policy for SRA [use `false` to disable rotation, `true` or `0` for immediate rotation at disconnect, or a positive integer `N` to delay rotation by `N` minutes]

Examples: `--rotate-after-disconnect true`, `--rotate-after-disconnect 0`, `--rotate-after-disconnect 15`

`--change-event`: Trigger an event when a secret value changes [`true`/`false`] (relevant only for Static Secret)

`-e, --expiration-event-in`: Number of days before certificate expiration to notify. To specify multiple events, repeat the flag: `--expiration-event-in 1 --expiration-event-in 5`

`-c, --cert-file-path`: Path to a file containing the certificate in PEM format. Used for updating RSA keys certificates

`--cert-file-data`: PEM certificate in Base64 format. Used for updating RSA keys certificates

`--certificate-format`: Format of the returned certificate [`pem`/`der`]

`--item-custom-fields`: Additional custom fields to associate with the item. To specify multiple fields, repeat the flag: `--item-custom-fields field1=value1 --item-custom-fields field2=value2`

`--gcp-sm-regions`: GCP Secret Manager regions for regional secrets (comma-separated). USC with GCP targets only

`--accessibility[=regular]`: For an item in a user's personal folder [`regular`/`personal`]

`--delete-protection`: Protection from accidental deletion of this object [`true`/`false`]

### `folder`

Commands for managing folders in the account

#### `folder create`

Creates a new folder

##### Usage

```shell
akeyless folder create \
--name <Folder Name> \
--type[=items] <Folder Type> \
--accessibility[=regular] <[regular/personal]>
```

#### `folder update`

Updates a new folder

##### Usage

```shell
akeyless folder update \
--name <Folder Name> \
--type[=items] <Folder Type> \
--accessibility[=regular] <[regular/personal]>
```

#### `folder get`

Get information of a folder

##### Usage

```shell
akeyless folder get \
--name <Folder Name> \
--type[=items] <Folder Type> \
--accessibility[=regular] <[regular/personal]>
```

#### `folder delete`

Deletes a new folder

##### Usage

```shell
akeyless folder delete \
--name <Folder Name> \
--type[=items] <Folder Type> \
--accessibility[=regular] <[regular/personal]>
```

### CLI Agent

#### `agent start`

Start Akeyless Agent
Accepted alias: `agent-start`.

##### Usage

```shell
akeyless agent start
```

#### `agent status`

Get Akeyless Agent status
Accepted alias: `agent-status`.

##### Usage

```shell
akeyless agent status
```

#### `agent stop`

Stop Akeyless Agent
Accepted alias: `agent-stop`.

##### Usage

```shell
akeyless agent stop
```

### `account-custom-field`

Commands to interact with custom fields.

#### Subcommands

`create`

`delete`

`get`

`list`

`update`

#### `account-custom-field create`

Create a new custom field in the account.
Accepted alias: `account-custom-field-create`.

##### Usage

```shell
akeyless account-custom-field create \
--object-type <Object type> \
--name <Custom field name> \
--required[=false]
```

##### Flags

`-o, --object[=ITEM]`: The object to create the custom field for

`-t, --object-type`: **Required**, The object type to create the custom field for, for example `STATIC_SECRET`, `DYNAMIC_SECRET`, or `ROTATED_SECRET`

`-n, --name`: **Required**, Custom field name

`-r, --required[=false]`: Specify whether the custom field is mandatory

#### `account-custom-field delete`

Delete a custom field from the account.
Accepted alias: `account-custom-field-delete`.

##### Usage

```shell
akeyless account-custom-field delete \
--id <Custom field ID>
```

##### Flags

`-i, --id`: **Required**, Custom field ID

#### `account-custom-field get`

Retrieve a custom field.
Accepted alias: `account-custom-field-get`.

##### Usage

```shell
akeyless account-custom-field get \
--id <Custom field ID>
```

##### Flags

`-i, --id`: **Required**, Custom field ID

#### `account-custom-field list`

Retrieve a list of custom fields in the account.
Accepted alias: `account-custom-field-list`.

##### Usage

```shell
akeyless account-custom-field list \
--object <Object type> \
--object-type <Custom field object type>
```

##### Flags

`-o, --object`: Filter by object

`-t, --object-type`: Filter by object type

#### `account-custom-field update`

Update an existing custom field in the account.
Accepted alias: `account-custom-field-update`.

##### Usage

```shell
akeyless account-custom-field update \
--id <Custom field ID> \
--name <New custom field name> \
--required[=false]
```

##### Flags

`-i, --id`: **Required**, Custom field ID

`-n, --name`: New custom field name

`-r, --required[=false]`: Specify whether the custom field is mandatory

### Group Management

Commands for creating, viewing, listing, and updating groups.

#### `create-group`

Create a new group.

Group names must start with `/`, must not end with `/`, and cannot contain `*`. Group aliases cannot contain `*`, `/`, `+`, `?`, or `.`. The command also requires a non-empty user-assignment payload supplied with `--user-assignment` or `--user-assignment-file`.

##### Usage

```shell
akeyless create-group \
--name <Group name> \
--group-alias <Group alias> \
--user-assignment <User assignment JSON>
```

##### Flags

`-n, --name`: **Required**, Group name

`-g, --group-alias`: **Required**, Short group alias

`--description`: Description of the object

`-u, --user-assignment`: **Required**, JSON string defining the user assignment for this group. Must contain at least one element

`-f, --user-assignment-file`: Path to a file containing the user-assignment JSON. Provide this instead of `--user-assignment`

#### `delete-group`

Delete a group.

##### Usage

```shell
akeyless delete-group \
--name <Group name>
```

##### Flags

`-n, --name`: **Required**, Group name

#### `get-group`

Return information about a group.

##### Usage

```shell
akeyless get-group \
--name <Group name>
```

##### Flags

`-n, --name`: **Required**, Group name

#### `list-groups`

List groups.

##### Usage

```shell
akeyless list-groups
```

##### Flags

`--filter`: Filter by group name or part of it

`--pagination-token`: Next page reference

#### `update-group`

Update a group.

The existing `--name` value and any `--new-name` value must follow the same group-name rules as `create-group`. This command also requires a non-empty user-assignment payload supplied with `--user-assignment` or `--user-assignment-file`.

##### Usage

```shell
akeyless update-group \
--name <Group name> \
--group-alias <Group alias> \
--user-assignment <User assignment JSON>
```

##### Flags

`-n, --name`: **Required**, Group name

`--new-name`: New group name

`-g, --group-alias`: **Required**, Short group alias

`--description`: Description of the object

`-u, --user-assignment`: **Required**, JSON string defining the user assignment for this group. Must contain at least one element

`-f, --user-assignment-file`: Path to a file containing the user-assignment JSON. Provide this instead of `--user-assignment`

### OIDC Applications

Commands for creating and updating OIDC applications and rotating their client secrets.

#### `create-oidc-app`

Create a new OIDC application.

This command requires a non-empty permission-assignment payload supplied with `--permission-assignment` or `--permission-assignment-file`.

##### Usage

```shell
akeyless create-oidc-app \
--name <OIDC application name> \
--redirect-uris <Comma-separated redirect URIs> \
--permission-assignment <Permission assignment JSON>
```

##### Flags

`-n, --name`: **Required**, OIDC application name

`-r, --redirect-uris`: Comma-separated list of allowed redirect URIs

`-s, --scopes[=openid]`: Comma-separated list of allowed scopes

`-a, --audience`: Comma-separated list of allowed audiences

`--public`: Set this flag if the app is public and cannot keep secrets

`-p, --permission-assignment`: Required unless `--permission-assignment-file` is provided. JSON string defining the permission assignment for this app. Must contain at least one element

`-f, --permission-assignment-file`: Required unless `--permission-assignment` is provided. Path to a file containing the permission-assignment JSON

`--item-custom-fields`: Additional custom fields to associate with the item. Repeat the flag to add multiple fields

`-t, --tag`: Add tags attached to this object. Repeat the flag to add multiple tags

`-k, --key`: Key used to encrypt the OIDC application

`--description`: Description of the object

`--accessibility[=regular]`: Accessibility for an item in a user's personal folder [`regular`/`personal`]

`--delete-protection`: Protection from accidental deletion of this object [`true`/`false`]

#### `rotate-oidc-client-secret`

Rotate an OIDC client secret.

##### Usage

```shell
akeyless rotate-oidc-client-secret \
--name <OIDC application name>
```

##### Flags

`-n, --name`: **Required**, OIDC application name

#### `update-oidc-app`

Update an existing OIDC application.

This command requires a non-empty permission-assignment payload supplied with `--permission-assignment` or `--permission-assignment-file`.

##### Usage

```shell
akeyless update-oidc-app \
--name <OIDC application name> \
--redirect-uris <Comma-separated redirect URIs> \
--permission-assignment <Permission assignment JSON>
```

##### Flags

`-n, --name`: **Required**, OIDC application name

`-r, --redirect-uris`: Comma-separated list of allowed redirect URIs

`-s, --scopes[=openid]`: Comma-separated list of allowed scopes

`-a, --audience`: Comma-separated list of allowed audiences

`--public`: Set this flag if the app is public and cannot keep secrets

`-p, --permission-assignment`: Required unless `--permission-assignment-file` is provided. JSON string defining the permission assignment for this app. Must contain at least one element

`-f, --permission-assignment-file`: Required unless `--permission-assignment` is provided. Path to a file containing the permission-assignment JSON

`-k, --key`: Key used to encrypt the OIDC application

### `policy`

Commands to manage account policies.

#### Subcommands

`create`

`delete`

`get`

`list`

`update`

#### `policy create`

Command to create a policy in the account.

##### Subcommands

`keys`

##### `policy create keys`

Create a new keys policy.

Provide at least one configuration flag in addition to `--path`. `--allowed-key-types` and `--allowed-key-names` are mutually exclusive. If you set `--object-types targets`, do not also set `--max-rotation-interval-days` or `--allowed-algorithms`. When `--object-types` is omitted, the policy applies to both `items` and `targets`.

###### Usage

```shell
akeyless policy create keys \
--path <Policy path>
```

###### Flags

`-p, --path`: **Required**, The path the policy refers to

`--max-rotation-interval-days`: Maximum automatic key-rotation interval

`--allowed-algorithms`: Allowed key algorithms, for example `RSA2048,AES128GCM`

`--allowed-key-types`: Allowed key protection types, `dfc` or `classic-key`

`--allowed-key-names`: Allowed protection key names. Use `default-account-key` to enforce the account default protection key

`-t, --object-types`: Object types this policy applies to, `items` or `targets`

#### `policy delete`

Delete an account policy by ID.

##### Usage

```shell
akeyless policy delete \
--id <Policy ID>
```

##### Flags

`-i, --id`: **Required**, Policy ID

#### `policy get`

Retrieve an account policy by ID.

##### Usage

```shell
akeyless policy get \
--id <Policy ID>
```

##### Flags

`-i, --id`: **Required**, Policy ID

#### `policy list`

List account policies.

##### Usage

```shell
akeyless policy list
```

##### Flags

`--paths`: Filter by exact policy paths

`--types`: Filter by policy types

`--object-type`: Filter by object types, `items` or `targets`

`--aggregate`: Aggregate missing configurations from parent policies. Requires `--paths`

#### `policy update`

Update an existing account policy.

##### Subcommands

`keys`

##### `policy update keys`

Update an existing keys policy.

Provide at least one update flag. `--allowed-key-types` and `--allowed-key-names` are mutually exclusive. If you set `--object-types targets`, do not also set `--max-rotation-interval-days` or `--allowed-algorithms`.

###### Usage

```shell
akeyless policy update keys \
--id <Policy ID>
```

###### Flags

`-i, --id`: **Required**, Policy ID

`-p, --path`: New policy path

`--max-rotation-interval-days`: Maximum automatic key-rotation interval

`--allowed-algorithms`: Allowed key algorithms, for example `RSA2048,AES128GCM`

`--allowed-key-types`: Allowed key protection types, `dfc` or `classic-key`

`--allowed-key-names`: Allowed protection key names. Use `default-account-key` to enforce the account default protection key

`-t, --object-types`: Object types this policy applies to, `items` or `targets`

### `delete-personal-folder`

Delete a personal folder.

#### Usage

```shell
akeyless delete-personal-folder \
--unique-id <Account unique ID>
```

#### Flags

`--unique-id`: Unique identifier of the account whose personal folder is to be deleted

`--access-id`: Access ID of the user whose personal folder is targeted for deletion by an administrator

### `get-analytics-data`

Get analytics data.

#### Usage

```shell
akeyless get-analytics-data
```

This command does not define command-specific flags beyond the global CLI flags shown above.

### `kubeconfig-generate`

Generate a unified kubeconfig for Kubernetes Dynamic Secrets.

Provide exactly one selector mode: `--name` or `--tag`. If you use `--tag`, only one tag value is supported.

#### Usage

```shell
akeyless kubeconfig-generate \
--name <Dynamic secret name> \
--out <Output file path>
```

#### Flags

`-n, --name`: Dynamic secret name. Repeat the flag to include multiple dynamic secrets

`-t, --tag`: Tag attached to the Dynamic Secret. At present, only one tag is supported

`-o, --out[=kubeconfig.json]`: Kubeconfig output file path

### `lock-item`

Lock a static secret item.

#### Usage

```shell
akeyless lock-item \
--name <Item name>
```

#### Flags

`--name`: **Required**, Item name

`--lock-ttl[=60]`: Lock time to live in minutes

`--actions[=update,read]`: Comma-separated blocked actions

### `unlock-item`

Unlock a static secret item.

#### Usage

```shell
akeyless unlock-item \
--name <Item name>
```

#### Flags

`-n, --name`: **Required**, Item name
