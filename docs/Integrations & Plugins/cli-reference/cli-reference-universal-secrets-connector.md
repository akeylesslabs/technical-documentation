---
title: CLI Reference - Universal Secrets Connector
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
_The External Secrets Manager has been renamed Universal Secrets Connector. All`esm` commands will still work as expected._

## Universal Secrets Connector

This section outlines the CLI commands relevant to Universal Secrets Connector.

<CLIGeneralFlags />

### `create-usc`

Creates a new Universal Secrets Connector

##### Usage

```shell
akeyless create-usc \
--name <USC name> \
--target-to-associate <target to associate>
```

##### Flags

`-n, --name`: **Required**, Universal Secrets Connector name

`-a, --target-to-associate` :**Required**, Target Universal Secrets Connector to connect

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--description` :Description of the Universal Secrets Connector

`-t, --tag`: List of the tags attached to this Universal Secrets Connector. To specify multiple tags use the argument multiple times: -t Tag1 -t Tag2

`-v, --azure-kv-name`:   Azure Key Vault name (Relevant only for Azure targets)

`-s, --k8s-namespace`: K8s namespace (Relevant to Kubernetes targets)

`--usc-prefix`: A prefix for all secret that will be created on the USC endpoint (relevant only for AWS targets)

`--use-prefix-as-filter[=true]`: Filter the USC secret list by the usc-prefix [`true`/`false`]

`--delete-protection`: Protection from accidental deletion of this item, [true/false]

`--profile, --token`: Use a specific profile (located at $HOME/.akeyless/profiles) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

## USC Subcommands

After creating a USC, you will need to use these sub-commands, prefixed with `usc`, to further interact with it.

### `usc`

This command only has one parameter, `-h`, and it will display a list of the other `usc` commands.

### `create`

Create a new secret in an existing USC

##### Usage

```shell
usc create \
--usc-name <usc name> \
--secret-name <Secret name> \
--value <secret value>
```

##### Flags

`-n, --usc-name`:  **Required**, USC name

`-u, --gateway-url[=http://localhost:8000]`:API Gateway URL (Configuration Management port)

`-s, --secret-name`:**Required**,Name for the new external secret

`--object-type[=secret]`: Either secret or certificate (Relevant only for Azure KV targets)

`--pfx-password`: Optional, the passphrase that protects the private key within the pfx certificate (Relevant only for Azure KV certificates)

`--usc-encryption-key`: Optional, The name of the remote key that used to encrypt the secret value (if empty, the default key will be used). Relevant only for **AWS** and **GCP**

`-v, --value`:**Required**,Value of the external secret item, either text or base64 encoded binary

`-b, --binary-value`:Use this option if the external secret value is a base64 encoded binary

`--description`:Description of the external secret

`--tags`:Tags for the external secret. Should be provided as --tags tag1=value1 --tags tag2=value2

### `delete`

Delete a secret from an Universal Secrets Connector

##### Usage

```shell
usc delete \
--usc-name <usc name> \
--secret-id <Secret name or id>
```

##### Flags

`-n, --usc-name`: **Required**, USC name

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-s, --secret-id`: **Required**, The secret id (or name, for AWS, Azure or K8s targets) to get from the Universal Secrets Connector

`--object-type[=secret]`: Either secret or certificate (Relevant only for Azure KV targets)

### `get`

Gets the value and internal details of a secret from an Universal Secrets Connector

##### Usage

```shell
usc get \
--usc-name <usc name> \
--secret-id <Secret name or id>
```

##### Flags

`-n, --usc-name`: **Required**, USC name

`-s, --secret-id`: **Required**, The secret id (or name, for AWS, Azure or K8s targets) to get from the Universal Secrets Connector

`--object-type[=secret]`: Either secret or certificate (Relevant only for Azure KV targets)

`-u, --gateway-url[=http://localhost:8000]`:   API Gateway URL (Configuration Management port)

`--profile, --token`: Use a specific profile (located at $HOME/.akeyless/profiles) or a temp access token

`--uid-token`:The universal identity token, Required only for universal_identity authentication

`-h, --help`:Display help information

`--json[=false]`:Set output format to JSON

`--jq-expression`:JQ expression to filter result output

`--no-creds-cleanup[=false]`:Do not clean local temporary expired creds

### `list`

Lists the secrets within the Universal Secrets Connector

##### Usage

```shell
akeyless usc list --usc-name <USC name>
```

##### Flags

`-n, --usc-name`: **Required**, USC name

`--object-type[=secret]`: Either secret or certificate (Relevant only for Azure KV targets)

`-u, --gateway-url[=http://localhost:8000]`:  API Gateway URL (Configuration Management port)

`--profile, --token`: Use a specific profile (located at $HOME/.akeyless/profiles) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

### `update`

Update an existing secret within the Universal Secrets Connector

##### Usage

```shell
usc update \
--usc-name <usc name> \
--secret-id <Secret name or id> \
--value <secret value>
```

##### Flags

`-n, --usc-name`: **Required**, USC name

`-s, --secret-id`: **Required**, The secret id (or name, for AWS, Azure or K8s targets) to get from the Universal Secrets Connector

`--object-type[=secret]`: Either secret or certificate (Relevant only for Azure KV targets)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-v, --value`: **Required**,Value of the external secret item, either text or base64 encoded binary

`-b, --binary-value`: Use this option if the external secret value is a base64 encoded binary

`--description`: Description of the external secret

`--tags`: Tags for the external secret. Should be provided as --tags tag1=value1 --tags tag2=value2
