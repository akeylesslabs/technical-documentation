---
title: CLI Reference - Static Secrets
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
This section outlines the CLI commands relevant to Static Secrets.

<CLIGeneralFlags />

## `create-secret`

Creates a new static secret item

### Usage

```shell
akeyless create-secret \
--name <Secret name> \
--value <Secret value> \
--type <generic/password> 
```

### Flags

`--name`: **Required**, Secret name

`--type[=generic]`: The secret sub type [`generic`/`password`]

`--value`: **Required**, The secret value (relevant only for type `generic`)

`-f, --format[=text]`: Secret format [`text`/`json` / `key-value`] (relevant only for type '`generic`')

`--url, --inject-url`: Comma-separated list of URLs associated with the item (only relevant for type `password`)

`-p, --password`: The password value (only relevant for type `password`)

`-u, --username`: The username value (only relevant for type `password`)

`-c, --custom-field`: Additional custom fields to associate with the item. To specify multiple fields, repeat the argument: `--custom-field fieldName1=value1 -c fieldName2=value2` (only relevant for type `password`)

`--accessibility[=regular]`: For an item in a user's personal folder [regular/personal]

`-t, --tag`: List of the tags attached to this secret. To specify multiple tags use argument multiple times: --tag Tag1 -t Tag2

`-k, --key`: The name of a key that used to encrypt the secret value (if empty, the account default protection key will be used)

`--multiline`: The provided value is a multiline value (separated by '\n')

`--max-versions`: Set the maximum number of versions, limited by the account settings defaults

`--secure-access-enable`: Enable/Disable Secure Remote Access, 'true'/'false'

`--secure-access-ssh-creds`: Static-Secret values contains SSH Credentials, either Private Key or Password [password/private-key]

`--secure-access-url`: Destination URL to inject secrets

`--secure-access-web-browsing[=false]`: Secure browser by way of Akeyless Web Access Bastion

`--secure-access-web-proxy[=false]`: Web-Proxy by way of Akeyless Web Access Bastion

`--secure-access-bastion-issuer`: Path to the SSH Certificate Issuer for your Akeyless Bastion

`--secure-access-host`: Target servers for connections. For multiple values repeat this flag.

`--secure-access-ssh-user`: Override the SSH username as indicated in SSH Certificate Issuer

`--secure-access-rdp-user`: Remote Desktop Username

`--description`: Secret description

`--delete-protection`: Protection from accidental deletion of this item, [true/false]

`--change-event`: Trigger an event when a secret value changed, [True/False]

## `describe-item`

Get the item details

### Usage

```shell
akeyless describe-item \
--name <item-name> \
--display-id <display id of the item> \
--item-id <Item-ID> 
```

### Flags

`-n, --name`: Item name

`-d, --display-id`: The display ID of the item

`-I, --item-id`: Item ID of the item

`--show-versions[=false]`: Include all item versions in reply

`--gateway-details[=false]`: Output will include additional gateway details (For example, cluster URL)

`--bastion-details[=false]`: Output will include additional bastion details

`--services-details[=false]`: Include all associated services details

`--accessibility[=regular]`: For an item in a user's personal folder [regular/personal]

See [Commands for all items and objects](https://docs.akeyless.io/docs/cli-reference#commands-for-all-items-and-objects) and also [Updating and versioning Static Secrets](https://docs.akeyless.io/docs/staticversions) for details.

## `get-secret-value`

Get static secret value

### Usage

<!-- secret-stdout-scan:ok -->
```shell
akeyless get-secret-value --name <Secret Name>
```

### Flags

`--name`: **Required**, Secret name

`--version`: Secret version, if negative value N is provided (--version=-N) the last N versions will return (maximum 20)

`--ignore-cache[=false]`: Retrieve the Secret value without checking the Gateway's cache [true/false]. This flag is only relevant when using the REST API

`--accessibility[=regular]`: For an item in a user's personal folder [regular/personal]

## `import-passwords`

Import passwords from CSV file

> ℹ️ **Note (CSV Example):**
>
> The box below has an example CSV that is valid for importing in the format of Chrome

### Usage

```shell
akeyless import-passwords \
--import-path <Path/to/CSV/Filee> \
--format <source format>
```
```text ExampleChromeFormatCSV.csv
name,url,username,password,description
/path/to/Example Email,https://mail.example.com,alice@example.com,P@ssword123,Primary email account for personal use
/full/path/to/Example Bank,https://bank.example.com,alice_bank,P@ssw0rd!,Banking account login details
/path/to/Example Social,https://social.example.com,alice_social,Social123,Social media account credentials

```

### Flags

`-p, --import-path`: **Required**, Path to the CSV file that contains passwords to import

`--format[=LastPass]`: Password format type [`LastPass`/`Chrome`/`Firefox`,`1password`,`keeper`,`bitwarden`,`dashlane`]

`--accessibility[=personal]`: Whether passwords should be imported to the user's personal folder [regular/personal]

`--target-folder[=/]`: Target folder for imported passwords

`-k, --key`: The name of a key that is used to encrypt the secret value (if empty, the account default protection key key will be used)

`--update-mode[=skip]`: Specify how to handle passwords that already exist (skip/update)

## `list-shared-items`

List shared items in the current account

## `rollback-secret`

Rollback secret to older version

### Usage

```shell
akeyless rollback-secret \
--name <Secret Name> \
--old-version <Secret version>
```

### Flags

`--name`: **Required**, Secret name

`--old-version`: **Required**, Old secret version to rollback to

## `share-item`

Sharing item operation [start sharing/stop sharing/sharing describe]

### Usage

```shell
akeyless share-item \
--item-name <Secret Name> \
--action <start/stop/describe> \
--email <Email list> 
```

### Flags

`-n, --item-name`: **Required**, The secret name (supported types: static secret)

`-a, --action`: **Required**, The action to perform [`start`/`stop`/`describe`]

`--share-type[=email]`: Share type [`email`/`token`]

`-e, --email`: List of emails to start/stop sharing the secret with, To specify multiple emails use argument multiple times: -e email1 -e email2

`-s, --shared-token-id`: Shared token ids to stop sharing a secret, To specify multiple token ids use the argument multiple times: `--shared-token-id token1` `--shared-token-id token2`

`-t, --ttl`: Availability of the shared secret in seconds

`-v, --view-once[=false]`: Shared secrets can only be viewed once [true/false]

`--accessibility[=regular]`: For an item in a user's personal folder [regular/personal]

## `unwrap-token`

Unwrapping the token containing a secret

### Usage

```shell
akeyless unwrap-token \
--shared-token <token>
```

### Flags

`-s, --shared-token`: **Required**, The value of the shared token that wraps the secret

## `update-secret-val`

Update static secret value

### Usage

```shell
akeyless update-secret-val \
--name <Secret Name> \
--value <secret value> 
```

### Flags

`--name`: **Required**, Secret name

`--value`: **Required**, The updated secret value

`--url, --inject-url`: List of URLs associated with the item (only relevant for type `password`)

`-p, --password`: The password value (only relevant for type `password`)

`-u, --username`: The username value (relevant for "password manager" only)

`-c, --custom-field`: Additional custom fields to associate with the item, to specify multiple fields repeat the argument: `--custom-field fieldName1=value1 -c fieldName2=value2` (only relevant for type 'password')

`-k, --key`: The name of a key that used to encrypt the secret value (if empty, the account default protectionKey key will be used)

`--multiline`: The provided value is a multiline value (separated by '\n')

`--last-version`: The last version number before the update

`--new-version`: [Deprecated: Use keep-prev-version instead] Whether to create a new version

`--keep-prev-version`: Whether to keep previous version, options:[true, false]. If not set, use default according to account settings

`--accessibility[=regular]`: For an item in a user's personal folder [regular/personal]

For other data, such as description or tags, use `update-item` as described in [Commands for all items and objects](https://docs.akeyless.io/docs/cli-reference#commands-for-all-items-and-objects).

## `static-secret-sync`

Sync a Static Secret using Universal Secret Connector

### Usage

```shell
akeyless static-secret-sync \
--name <Secret Name> \
--usc-name <Universal Secret Connector Name> \
--remote-secret-name <Name of the secret in the remote endpoint>
```

### Flags

`-n, --name`: **Required**, Secret name

`--usc-name`: Universal Secret Connector name, If not provided all attached USC's will be synced

`--remote-secret-name`: Remote Secret Name that will be synced on the remote endpoint

> ℹ️ **Note (AWS Targets):**
>
> For AWS Universal Secret Connector targets, Akeyless-initiated sync updates secret values while preserving existing AWS-side custom tags and description unless those fields are explicitly updated.

`--namespace`: Vault Namespace, relevant only for HashiCorp Vault Target

`--filter-secret-value`: jq expression to filter or transform the secret value

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

## `delete sync`

delete static secret sync

### Usage

```shell
akeyless static-secret-delete-sync \
--name <Rotated Secret Name> \
--usc-name <USC Name> \
--remote-secret-name <Remote secret Name> \
--delete-from-usc[=false] [true / false] \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

### Flags

`--name`: The Static Secret name.

`--usc-name`: The name of the Universal Secret Connector.

`--remote-secret-name`: Remote Secret name that will be created on the remote endpoint.

`--delete-from-usc[=false]`: Delete the secret from the remote target usc as well.

`--gateway-url`: Akeyless Gateway URL (port `8000`).
