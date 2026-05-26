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
_The External Secrets Manager has been renamed Universal Secrets Connector. All `esm` commands will still work as expected._

Legacy `esm` commands continue to accept `-n, --esm-name` for the Universal Secrets Connector name.

This section outlines the CLI commands relevant to Universal Secrets Connector.

<CLIGeneralFlags />

## `create-usc`

Creates a new Universal Secrets Connector

### Usage

```shell
akeyless create-usc \
--name <USC name> \
--target-to-associate <target to associate>
```

### Flags

`-n, --name`: **Required**, Universal Secrets Connector name

`-a, --target-to-associate`: **Required**, Target Universal Secrets Connector to connect

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--description`: Description of the Universal Secrets Connector

`-t, --tag`: List of the tags attached to this Universal Secrets Connector. To specify multiple tags use the argument multiple times: -t Tag1 -t Tag2

`-v, --azure-kv-name`: Azure Key Vault name (Relevant only for Azure targets)

`-s, --k8s-namespace`: Kubernetes Namespace (Relevant to Kubernetes targets)

`--usc-prefix`: A prefix for all secret that will be created on the USC endpoint (relevant only for AWS targets)

`--use-prefix-as-filter[=true]`: Filter the USC secret list by the usc-prefix [`true`/`false`]

`--gcp-project-id`: GCP Project ID (Relevant only for GCP targets)

`--gcp-sm-regions`: GCP Secret Manager regions for regional secrets (comma-separated, for example: `us-east1,us-west1`). USC with GCP targets only. Maximum 12 regions.

`--environment-names`: Comma-separated list of environment names to associate with the connector

`--github-scope[=repository]`: GitHub scope to use [`repository`/`organization`] (GitHub targets only)

`--organization-name`: GitHub organization name (organization-scoped GitHub targets only)

`--repository-access[=public]`: GitHub repository access level [`public`/`private`/`all`] (GitHub targets only)

`--repository-names`: Comma-separated list of GitHub repositories to include (GitHub targets only)

`--usc-tags`: Comma-separated list of tags to apply to remote secrets created or synced by this connector

`--use-tags-as-filter`: Filter the remote secret list using the specified `usc-tags` values [`true`/`false`]

`--delete-protection`: Protection from accidental deletion of this item, [true/false]

`--profile, --token`: Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: jq expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired credentials

## USC Subcommands

After creating a USC, you will need to use these sub-commands, prefixed with `usc`, to further interact with it.

### `usc`

This command only has one parameter, `-h`, and it will display a list of the other `usc` commands.

### `create`

Create a new secret in an existing USC
Accepted aliases: `usc-create`, `esm-create`.

#### Usage

```shell
akeyless usc create \
--usc-name <usc name> \
--secret-name <Secret name> \
--value <secret value>
```

#### Flags

`-n, --usc-name`: **Required**, USC name

`-u, --gateway-url[=http://localhost:8000]`:API Gateway URL (Configuration Management port)

`-s, --secret-name`:**Required**,Name for the new external secret

`--object-type[=secret]`: Either secret or certificate (Relevant only for Azure KV targets)

`--pfx-password`: Optional, the passphrase that protects the private key within the pfx certificate (Relevant only for Azure KV certificates)

`--usc-encryption-key`: Optional, The name of the remote key that used to encrypt the secret value (if empty, the default key will be used). Relevant only for **AWS** and **GCP**

`-v, --value`:**Required**,Value of the external secret item, either text or Base64-encoded binary

`-b, --binary-value`:Use this option if the external secret value is a Base64-encoded binary

`--description`:Description of the external secret

`--tags`:Tags for the external secret. Should be provided as --tags tag1=value1 --tags tag2=value2

`--remote-secret-activation-date`: Activation date for the remote secret

`--remote-secret-expires`: Expiration date for the remote secret

`--selected-repositories`: Explicit list of GitHub repositories selected for this operation

`--region`: Optional, create the secret in a specific region (GCP only). If omitted, the secret is created as a global secret.

### `delete`

Delete a secret from an Universal Secrets Connector
Accepted aliases: `usc-delete`, `esm-delete`.

#### Usage

```shell
akeyless usc delete \
--usc-name <usc name> \
--secret-id <Secret name or id>
```

#### Flags

`-n, --usc-name`: **Required**, USC name

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-s, --secret-id`: **Required**, The secret ID (or name, for AWS, Azure or Kubernetes targets) to delete from the Universal Secrets Connector

`--namespace`: The namespace (relevant for HashiCorp Vault target)

`--selected-repositories`: Explicit list of GitHub repositories selected for this operation

`--force-delete`: Force delete objects that are soft deleted by default (relevant only for Azure target)

### `get`

Gets the value and internal details of a secret from an Universal Secrets Connector
Accepted aliases: `usc-get`, `esm-get`.

#### Usage

```shell
akeyless usc get \
--usc-name <usc name> \
--secret-id <Secret name or id>
```

#### Flags

`-n, --usc-name`: **Required**, USC name

`-s, --secret-id`: **Required**, The secret ID (or name, for AWS, Azure or Kubernetes targets) to get from the Universal Secrets Connector

`--object-type[=secret]`: Object type filter: `secret` (default), `certificate` (Azure KV), or `regional-secrets` (GCP)

`--selected-repositories`: Explicit list of GitHub repositories selected for this operation

`--version-id`: Version ID of the remote secret

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--profile, --token`: Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`:The universal identity token, Required only for universal_identity authentication

`-h, --help`:Display help information

`--json[=false]`:Set output format to JSON

`--jq-expression`: jq expression to filter result output

`--no-creds-cleanup[=false]`:Do not clean local temporary expired credentials

### `list`

Lists the secrets within the Universal Secrets Connector
Accepted aliases: `usc-list`, `esm-list`.

#### Usage

```shell
akeyless usc list --usc-name <USC name>
```

#### Flags

`-n, --usc-name`: **Required**, USC name

`--object-type[=secret]`: Either secret or certificate (Relevant only for Azure KV targets)

`--page-size`: Optional number of items requested per response (Azure KV). When set, the response may include a next token.

`--page-token`: Optional continuation token returned by a previous `usc list --page-size` call.

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--profile, --token`: Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: jq expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired credentials

### `update`

Update an existing secret within the Universal Secrets Connector
Accepted aliases: `usc-update`, `esm-update`.

#### Usage

```shell
akeyless usc update \
--usc-name <usc name> \
--secret-id <Secret name or id> \
--value <secret value>
```

#### Flags

`-n, --usc-name`: **Required**, USC name

`-s, --secret-id`: **Required**, The secret ID (or name, for AWS, Azure or Kubernetes targets) to get from the Universal Secrets Connector

`--object-type[=secret]`: Either secret or certificate (Relevant only for Azure KV targets)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-v, --value`: **Required**,Value of the external secret item, either text or Base64-encoded binary

`-b, --binary-value`: Use this option if the external secret value is a Base64-encoded binary

`--description`: Description of the external secret

`--tags`: Tags for the external secret. Should be provided as --tags tag1=value1 --tags tag2=value2

`--remote-secret-activation-date`: Activation date for the remote secret

`--remote-secret-expires`: Expiration date for the remote secret

`--selected-repositories`: Explicit list of GitHub repositories selected for this operation
