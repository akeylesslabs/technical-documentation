---
title: Automatic Migration
slug: automatic-migration
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
## Introduction

Automatic migration allows importing Static Secrets into Akeyless from other identity security platforms. This feature is available as part of the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) functionality. Additionally, it is possible to configure migration by way of the Console, where each Gateway has its dedicated directory for managing the migration process.

## Supported Platforms

Currently, you can import Static Secrets from the following platforms:

* [1Password](https://docs.akeyless.io/docs/automatic-migration#1password) - Deprecated from Gateway version `4.35.1`
* [AWS Secrets Manager](https://docs.akeyless.io/docs/automatic-migration#aws-secrets-manager)
* [Azure Key Vault](https://docs.akeyless.io/docs/automatic-migration#azure-key-vault)
* [Conjur Secrets Manager](https://docs.akeyless.io/docs/automatic-migration#conjur-secrets-manager)
* [CSV import](https://docs.akeyless.io/docs/automatic-migration#csv-import), Relevant for Firefox, Chrome and LastPass
* [GCP Secrets Manager](https://docs.akeyless.io/docs/automatic-migration#gcp-secrets-manager)
* [HashiCorp Vault](https://docs.akeyless.io/docs/automatic-migration#hashicorp-vault)
* [Kubernetes](https://docs.akeyless.io/docs/automatic-migration#kubernetes)

## General Configuration

The following options are available when importing secrets from other identity security platforms:

* **Name:** This is an arbitrary name for the migration object.

* **Target location:** This is where secrets are created in Akeyless.

For example, when importing secrets from Kubernetes, it may be a good idea to put them all under the `/kubernetes` path. This is also recommended if there are multiple Kubernetes clusters, under `/kubernetes/staging` or similar.

After the migration, new secrets will be available under the specified path. If the location is not provided, the secrets will be created in the root `/` folder of your account.

* **Protect secrets with the following key:** This required field allows selecting the encryption key for the protection of imported secrets. This property will enable you to use [Zero-Knowledge Encryption](https://docs.akeyless.io/docs/zero-knowledge).

> ℹ️ **Note:**
>
> If there are existing secrets under the **Target location**, their values are replaced if a conflict occurs. This can happen if you leave the "Target location" field blank and a new secret has the same name as an existing one.
>
> ✅ **Tip:**
>
> Before getting started, ensure that the platform where the secrets are stored is accessible over the network from the Akeyless Gateway server. Depending on the deployment, it might require adding an Akeyless Gateway IP address to a security group or a firewall.

## 1Password

> ℹ️ **Note (Deprecation):**
>
> Due to internal security restrictions this migration is deprecated starting from Gateway version `4.35.1`.

To import secrets as `LOGIN`, `PASSWORD`, and `SECURE_NOTE` from 1Password into Akeyless Provide the relevant `sign-in address` which is your 1Password account URL for example “company_name.1Password.com” with a privileged email and password with your 1Password Secret Key`.

You can choose the relevant `Vaults` you would like to migrate items from. Enter them as a comma-separated list. If left empty, all non-private Vaults are migrated.

To import the private vaults of your users into Akeyless Personal folder space, each user will have to run its own process using the Akeyless CLI command `gateway-migrate-personal-items`.

## AWS Secrets Manager

To import secrets from AWS Secrets Manager, you need to provide access credentials of a user with sufficient permissions to get all secrets. The required configuration includes AWS Access Key ID, AWS Secret Access Key, and an AWS region.

## Azure Key Vault

To import secrets from Azure Key Vault, you need to create an [Azure AD app with a service principal](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal). Access credentials and the unique Key Vault name must be provided in the configuration dialog.

## Conjur Secrets Manager

To import secrets from Conjur Secrets Manager, you need to provide access credentials of a user with sufficient permissions to get all secrets. The required configuration includes the Conjur URL, Conjur Account, Username, and API Key.

You can create a Conjur migration using the Console, the CLI, or the API.

```shell
akeyless gateway-create-migration \
--type conjur \
--name <migration-name> \
--target-location <destination-path-in-akeyless> \
--conjur-url 'https://<Your-Conjur-URL>' \
--conjur-account <conjur-account> \
--conjur-username <conjur-username> \
--conjur-api-key <conjur-api-key> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

Where:

* `name`: A unique name for the migration object.

* `target-location`: The destination folder path in Akeyless where the migrated secrets will be created.

* `conjur-url`: The URL of your Conjur instance.

* `conjur-account`: The Conjur account name.

* `conjur-username`: The Conjur username with permissions to read secrets.

* `conjur-api-key`: The API key for the Conjur user.

* `gateway-url`: Akeyless Gateway URL (port `8000`).

To update an existing Conjur migration, use `akeyless gateway-migration-update --type conjur` with the same flags.

## CSV Import

To upload a CSV file containing passwords into your Akeyless, you will need to run the following command in the Akeyless CLI:

```shell
akeyless import-passwords --import-path <path to file> --format <source format>
```

The main parameters for this command are:

* `import-path`: Path to the CSV file that contains the passwords downloaded from the relevant service. This is a mandatory parameter.

* `format`: Password source format. The default is `LastPass`, the other options are `Chrome` or `Firefox`.

* `accessibility`: The folder you wish the passwords to be imported into. The default is to the personal folder.

* `target-folder`: Target folder for the imported passwords in your Akeyless directory. The default is in the main folder.

* `skip`: Ignores any existing passwords with the same name as those in the import file. This is useful to add new passwords and avoid accidentally duplicating or overwriting existing ones.

* `update`: Replacing any existing passwords with the same name as those in the import file. This ensures that existing passwords are updated with the latest information from the import file, it can potentially overwrite any changes made on the system since the last import.

## GCP Secrets Manager

To import secrets from GCP Secrets Manager, you need to provide a GCP Service Account Key in the JSON format with sufficient permissions to get all secrets or a Gateway that runs on GCP using the Gateway Cloud ID option.

> ✅ **Tip:**
>
> A GCP Service Account is a type of Google identity intended to interact with workloads. Authentication with this identity is required to fetch information over Google APIs.
>
> The minimum required permissions to access the secret payload can be acquired from the Secret Manager Secret Accessor role (`roles/secretmanager.secretAccessor`).

## HashiCorp Vault

To import secrets from HashiCorp Vault into Akeyless, you need to create a new access token or use the existing one with sufficient permissions. You also need to provide a full URL of the HashiCorp Vault API server.

For migration from HashiCorp Vault Enterprise, the configuration of namespaces is available. A comma-separated list of namespaces must be imported into Akeyless. For every provided Namespace, all its child namespaces are imported as well.

Akeyless supports migration from the `kv` storage engine of versions 1 and 2. For v2 migrations, up to `5`  versions of the secret will be migrated.

For HashiCorp Vault KV v2 migrations, you can control how much metadata is migrated by selecting a metadata preservation mode:

* `full`: Migrates the complete KV v2 metadata block (trimmed to the secret versions being migrated).
* `minimal`: Migrates only the [custom metadata](https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2#custom-metadata).
* `none`: Migrates only secret values without KV v2 metadata.

For more details, see [HashiCorp Vault Metadata Preservation Mode](https://docs.akeyless.io/docs/gateway-automatic-migration#hashicorp-vault-metadata-preservation-mode).

For all supported engines the following prefix structure will be used: `<vault-namespace>/<vault secret engine name>`

## Kubernetes

Akeyless supports secrets migration from Kubernetes Secrets using Kubernetes API.

Three types of authentication are available:

* Bearer token
* Certificate
* Password

For any Kubernetes authentication method, the following options are available:

* **Cluster URL endpoint:** This is the URL of the Kubernetes API server (including schema and port, for example, `https://<k8s-api.mycompany.com>:6443)`.

* **Cluster CA Certificate:** Optional Certificate Authority data if the server is accessed over HTTPS. This value can be found in your `~/.kube/config` file, under the **certificate-authority-data** property of the cluster with the existing secrets. There is no need to Base64-decode this value. It should be used as-is. If no value is provided, an insecure connection is used, which is discouraged.

* **Namespace:** Use this field to import secrets from a particular Namespace only. By default, the secrets are imported from all namespaces.

* **Skip Control Plane Secrets:** This flag allows us to avoid importing secrets from system namespaces (the ones that begin with `kube-`). If you need to import secrets from all namespaces, uncheck this flag.

> ✅ **Tip:**
>
> When choosing an authentication method to access your Kubernetes cluster, ensure that the credentials you provide have sufficient privileges to list and get secrets in the Namespace(s) you selected.

**Bearer token authentication:** For servers that support Bearer Token authentication, use Token authentication method. Make sure that this token is not expired when used.

**Certificate authentication:** For servers that use client certificates for authentication, use Certificate authentication method when creating a new migration.

**Password authentication:** For servers that allow username/password authentication, use Password authentication method

[Read more about command parameters.](https://docs.akeyless.io/docs/cli-reference-automatic-migration)

## Tutorials

Check out our tutorial videos on [AWS and HashiCorp Vault Secrets Migration Into Akeyless](https://tutorials.akeyless.io/docs/aws-and-hashicorp-vault-secrets-migration-into-akeyless) and [Kubernetes Secrets Migration into Akeyless](https://tutorials.akeyless.io/docs/kubernetes-secrets-migration-to-akeyless).
