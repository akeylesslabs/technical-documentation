---
title: CLI Reference
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

### `Configure`

Configure client profile

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

`--azure_ad_object_id`: Azure Active Directory ObjectId (relevant only for access-type=azure_ad)

`--gcp-audience`: GCP audience to use in signed JWT (relevant only for access-type=gcp)

`--gateway-url`: Gateway URL for the Kubernetes authenticated (relevant only for `access-type=k8s`)

`--k8s-auth-config-name`: The Kubernetes Auth config name (relevant only for `access-type=k8s`)

`--k8s-token-path[=/var/run/secrets/kubernetes.io/serviceaccount/token]`: An optional path to a projected service account token inside the pod, for use instead of the default service account token (relevant only for `access-type=k8s`)

`--cert-file-name`: Name of the certificate file to use (relevant only for `access-type=cert`)

`--cert-data`: Certificate data encoded in Base64. Used if file was not provided. (relevant only for `access-type=cert` in Curl Context)

`--key-file-name`: Name of the private key file to use (relevant only for `access-type=cert`)

`--key-data`: Private key data encoded in Base64. Used if file was not provided (relevant only for `access-type=cert` in Curl Context)

### `Delete-item`

Delete an item or an item version

#### Usage

```shell
akeyless delete-item -n <Item name>
```

#### Flags

`-n, --name`: Required, Item name

`--version[=-1]`: The specific version you want to delete - 0=last version, -1=entire item with all versions (default)

`--delete-in-days "day`: The number of days to wait before deleting the item (relevant for keys only)

`--delete-immediately[=false]`: When delete-in-days=-1, must be set

`--accessibility[=regular]`: In case of an item in a user's personal folder [regular/personal]

### `Delete-items`

Deletes multiple items from a given path

#### Usage

```shell
akeyless delete-items -p <Path\do\delete\items>
```

#### Flags

`-p, --path`: Required, Path to delete the items from

### `Describe-item`

Gets the item details

#### Flags

`-n, --name`: Item name

`-d, --display-id`: The display ID of the item

`-I, --item-id`: Item ID of the item

`--show-versions[=false]`: Include all item versions in reply

`--gateway-details[=false]`: Output will include additional gateway details (For example, cluster URL)

`--bastion-details[=false]`: Output will include additional bastion details

`--services-details[=false]`: Include all associated services details

`--accessibility[=regular]`: In case of an item in a user's personal folder [regular/personal]

#### Output

With only `--name` specified, the command returns all details about the specified item except for its version.

When a version number is specified, the command returns all details about the specified item for the specified version.

When `--show-versions` is specified, the command returns all details about the specified item including a full list of versions, their creation dates, and their encryption keys for any version for which a key other than the default was used.

### `Get-account-settings`

Get the settings of the account

### `Get-tags`

Get all tags of selected item

#### Usage

```shell
akeyless get-tags --name <Item Name>
```

#### Flags

`-n, --name`: Required, The item name

### `List-items`

List of all accessible items

#### Flags

`-t, --type`: The item types list of the requested items. In case it is empty, all types of items will be returned, options: [key, static-secret, dynamic-secret, rotated-secret, ssh-cert-issuer, pki-cert-issuer, classic-key]

`--sub-types`: Optional the items sub types

`--filter`: Filter by item name or part of it

`--tag`: Filter by item tag

`--sra-only[=false]`: Filter by items with SRA functionality enabled

`--path`: Path to folder

`--pagination-token`: Next page reference

`--auto-pagination[=enabled]`: Retrieve all items using pagination, when disabled retrieving only first 1000 items

`--minimal-view`: Show only basic information of the items

`--accessibility[=regular]`: In case of an item in a user's personal folder, options: [regular/personal]

### `List-sra-bastions`

List of all Secure Remote Access (SRA) Bastions in the account

#### Flags

`--only-allowed-urls[=false]`: Filter the response to show only bastions allowed URLs

### `Move-objects`

Moves/Renames objects

#### Usage

```shell
akeyless move-objects --source <Source path to move the objects from> \
--target <Target path to move the objects to> \
--objects-type <The objects type to move (item/auth_method/role)>
```

#### Flags

`-s, --source`: Required, Source path to move the objects from

`--t, --target`: Required, Target path to move the objects to

`-o, --objects-type[=item]`: The objects type to move (item/auth_method/role)

### `Set-item-state`

Set Dynamic Secret item's state (Enabled, Disabled)

#### Usage

```shell
akeyless set-item-state --name <Current item name> \
--desired-state <Desired item state [Enabled, Disabled]>
```

#### Flags

`-n, --name`: Required, Current item name

`-s, --desired-state`: Required, Desired item state

### `Unconfigure`

Remove configuration of client profile

#### Usage

```shell
akeyless unconfigure --profile <Profile name>
```

### `Update`

Update the Akeyless CLI version or change to a prior version

#### Usage

```shell
akeyless update
```

#### Flags

`-v, --version[=latest]`: Provide the CLI version to update to, by default, the latest version is used

`-s, --show-changelog`: Show the changelog between the current version and the latest version

`-r, --artifact-repository`: Alternative CLI repository URL, for example, `https://artifacts.site2.akeyless.io`

### `Update-account-settings`

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

### `Update-item`

Update item name and description

> ❗️ Critical
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

block:Flags]

`-n, --name`: Required, Current item name

`--new-name`: New item name

`--description[=default_metadata]`: Description of the object

`--add-tag`: List of the new tags that will be attached to this item. To specify multiple tags use argument multiple times: `--add-tag Tag1 --add-tag Tag2`

`--rm-tag`: List of the existent tags that will be removed from this item. To specify multiple tags use argument multiple times: `--rm-tag Tag1 --rm-tag Tag2`

`--secure-access-enable`: Enable/Disable Secure Remote Access, "0-1": "__(M

`--secure-access-bastion-issuer`: Path to the SSH Certificate Issuer for your Akeyless Bastion

`--secure-access-bastion-api`: Bastion's SSH control API endpoint. For example, `my.bastion:9900` (relevant only for SSH cert issuer)

`--secure-access-bastion-ssh`: Bastion's SSH server. For example, `my.bastion:22` (relevant only for SSH cert issuer)

`--secure-access-ssh-creds-user`: SSH username to connect to target server, must be in 'Allowed Users' list (relevant only for SSH cert issuer)

`--secure-access-use-internal-bastion`: Use internal SSH Bastion

`--secure-access-ssh-creds`: Secret values contains SSH Credentials, either Private Key or Password em name\ "h-0": " (relevant only for Static-Secret or Rotated-secret)

`--secure-access-host`: Target servers for connections, For multiple values repeat this flag

`--secure-access-add-host`: List of the new hosts that will be attached to SRA servers host. To specify multiple tags use argument multiple times: `--secure-access-add-host` host1 `--secure-access-add-host` host2

`--secure-access-rm-host`: List of the existent hosts that will be removed from SRA servers host. To specify multiple tags use argument multiple times: `--secure-access-rm-host` host1 `--secure-access-rm-host` host2

`--secure-access-url`: Destination URL to inject secrets

`--secure-access-web-browsing`: Secure browser by way of Akeyless Web Access Bastion

`--secure-access-web-proxy`: Web-Proxy by way of Akeyless Web Access Bastion

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user (relevant only for RDP Dynamic-Secret)

`--secure-access-rdp-user`: Override the RDP Domain username

`--secure-access-rdp-domain`: Required when the Dynamic Secret is used for a domain user (relevant only for RDP Dynamic-Secret)

`--secure-access-rdp-user`: Override the RDP Domain username

`--secure-access-allow-external-user`: Allow providing external user for a domain users (Mandatory)__

`--secure-access-db-schema`: The DB schema (relevant only for DB Dynamic-Secret)

`--secure-access-db-name`: "The DB name (relevant only for DB Dynamic-Secret)

`--secure-access-aws-account-id`: The AWS account ID (relevant only for AWS Dynamic-Secret)

`--secure-access-aws-region`: The AWS region (relevant only for AWS Dynamic-Secret)

`--secure-access-aws-native-cli`: The AWS native CLI (relevant only for AWS Dynamic-Secret)

`--secure-access-cluster-endpoint`: The Kubernetes cluster endpoint URL (relevant only for EKS/GKE/K8s Dynamic-Secret)

`--secure-access-dashboard-url`: The Kubernetes dashboard URL (relevant only for Kubernetes Dynamic-Secret)

`--secure-access-allow-port-forwading`: Enable Port forwarding while using CLI access (relevant only for EKS/GKE/K8s Dynamic-Secret)

`--rotate-after-disconnect[=false]`: Rotate the value of the secret after SRA session ends (Mandatory) (relevant only for Rotated-secret on SRA)

`--behaviordelete-protection`: Protection from accidental deletion of this item

`--change-event`: Trigger an event when a secret value changed [true/false] (Relevant only for Static Secret)

`-c, --cert-file-path`: Path to a file that contain the certificate in a PEM format. Used for updating RSA keys' certificates

`--cert-file-data`: PEM Certificate in a Base64 format. Used for updating RSA keys' certificates.

`--certificate-format`: The format of the returned certificate [`pem`/`der`]

`--accessibility \"data\":` In case of an item in a user's personal folder

### `Folder Management`

Commands for managing folders in the account

#### `Folder Create`

Creates a new folder

##### Usage

```shell
akeyless folder create \
--name <Folder Name> \
--type[=items] <Folder Type> \
--accessibility[=regular] <[regular/personal]>
```

#### `Folder Update`

Updates a new folder

##### Usage

```shell
akeyless folder update \
--name <Folder Name> \
--type[=items] <Folder Type> \
--accessibility[=regular] <[regular/personal]>
```

#### `Folder Get`

Get information of a folder

##### Usage

```shell
akeyless folder get \
--name <Folder Name> \
--type[=items] <Folder Type> \
--accessibility[=regular] <[regular/personal]>
```

#### `Folder Delete`

Deletes a new folder

##### Usage

```shell
akeyless folder delete \
--name <Folder Name> \
--type[=items] <Folder Type> \
--accessibility[=regular] <[regular/personal]>
```

### CLI Agent

#### `Agent Start`

Start Akeyless Agent

##### Usage

```shell
akeyless agent start
```

#### `Agent Status`

Get Akeyless Agent status

##### Usage

```shell
akeyless agent status
```

#### `Agent Stop`

Stop Akeyless Agent

##### Usage

```shell
akeyless agent stop
```
