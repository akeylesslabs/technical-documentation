---
title: CLI Reference - Gateway
slug: cli-reference-gateway
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
This section outlines the CLI commands relevant to the Gateway.

<CLIGeneralFlags />

## Additional flags on this page

The following flag is also used by commands documented in this page.

`--new-metadata[=default_metadata]`: Replaces the existing metadata value for an item.

## Access Permissions

Commands for managing the access of users to your Gateway.

### `add-gw-access-id`

Grants Gateway access to users

#### Usage

```shell
akeyless add-gw-access-id \
--cluster-name <Cluster Name> \
--access-id <AccessID> \
--sub-claims <group=admins>
```

#### Flags

`-c, --cluster-name`: **Required**, The name of the updated cluster

`-a, --access-id`: **Required**, The `Access ID` to be able to access the gateway

`-s, --sub-claims`: `key/val` of sub-claims, for example, `group=admins,developers`

### `delete-gw-access-id`

Denials Gateway access to users

#### Usage

```shell
akeyless delete-gw-access-id \
--cluster-name <Cluster Name> \
--access-id <Access ID>
```

#### Flags

`-c, --cluster-name`: **Required**, The name of the updated cluster

`-a, --access-id`: **Required**, The `Access ID` to be able to access the gateway

### `gateway-create-allowed-access`

Add users that will have permission to manage the Gateway

#### Usage

```shell
akeyless gateway-create-allowed-access \
--name <Allowed Access Name> \
--access-id <Access-ID> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--description <Allowed Access description> \
--sub-claims <key/val of sub claims> \
--permissions <permissions for this allowed access> 
```

#### Flags

`-n, --name`: **Required**, Allowed access name

`--access-id`: **Required**, The `Access ID` to be attached to this allowed access

`--description`: Allowed access description

`-s, --sub-claims`: `key/val` of sub-claims, for example, `group=admins,developers`

`-p, --permissions`: Comma-separated list of permissions for this allowed access. Available permissions: [`defaults`, `targets`, `classic_keys`, `automatic_migration`, `ldap_auth`, `dynamic_secret`, `k8s_auth`, `log_forwarding`, `zero_knowledge_encryption`, `rotated_secret`, `caching`, `event_forwarding`, `admin`, `kmip`, `general`, `rotate_secret_value`]

`-c, --case-sensitive[=true]`: Treat sub-claims as case-sensitive

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `gateway-update-allowed-access`

Set users that will have permission to manage the Gateway

#### Usage

```shell
akeyless gateway-update-allowed-access \
--name <Allowed Access Name> \
--access-id <Access-ID> \
--new-name <New allowed access name> \
--gateway-url <API Gateway URL>:8000 \
--description <Allowed Access description> \
--sub-claims <key/val of sub claims> \
--permissions <permissions for this allowed access> 
```

#### Flags

`-n, --name`: **Required**, Allowed access name

`--access-id`: **Required**, The `Access ID` to be attached to this allowed access

`--new-name`: New allowed access name

`--description`: Allowed access description

`-s, --sub-claims`: `key/val` of sub claims, for example, `group=admins,developers`

`-p, --permissions`: Comma-separated list of permissions for this allowed access. Available permissions: [`defaults`, `targets`, `classic_keys`, `automatic_migration`, `ldap_auth`, `dynamic_secret`, `k8s_auth`, `log_forwarding`, `zero_knowledge_encryption`, `rotated_secret`, `caching`, `event_forwarding`, `admin`, `kmip`, `general`]

`-c, --case-sensitive[=true]`: Treat sub claims as case-sensitive

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `gateway-delete-allowed-access`

Delete Allowed Access

#### Usage

```shell
akeyless gateway-delete-allowed-access \
--name <Allowed Access name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`-n, --name`: **Required**, Allowed Access name

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `gateway-get-allowed-access`

Get Allowed Access

#### Usage

```shell
akeyless gateway-get-allowed-access \
--name <Allowed Access name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`-n, --name`: **Required**, Allowed Access name

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

## Gateway Configuration

### `delete-gateway-cluster`

Deletes a gateway in the account

#### Usage

```shell
akeyless delete-gateway-cluster \
--cluster-name <Cluster Name> \
--force < true / false>
```

#### Flags

`-c, --cluster-name`: **Required**, Gateway Cluster, for example, `acc-abcd12345678/p-123456789012/defaultCluster`

`--force`: Deletes cluster even if there is an active gateway or associated secrets. All Gateway secrets will be deleted

### `gateway-get-config`

Gets gateway configuration details

#### Usage

```shell
akeyless gateway-get-config \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

### `gateway-update-tls-cert`

Updates TLS certificate in the Gateway

```shell
akeyless gateway-update-tls-cert \
--cert-data <TLS Certificate> \
--cert-file-name <Path/To/Certificate> \
--key-data <TLS Private Key> \
--key-file-name <Path/To/Key> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`--cert-data`: TLS Certificate (Base64-encoded), this flag is ignored if `--cert-file-name` is supplied

`--cert-file-name`: Path to the file containing the TLS Certificate, this flag is ignored if `--cert-data` is supplied

`--key-data`: TLS Private Key (Base64-encoded), this flag is ignored if `--key-file-name` is supplied

`--key-file-name`: Path to the file containing the TLS Private Key, this flag is ignored if `--key-data` is supplied

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `gateway-update-item`

Update a Gateway item.

#### Usage

```shell
akeyless gateway-update-item \
--name <Item name> \
--type <classic-key/rotated-secret> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`-n, --name`: **Required**, Item name

`-t, --type`: **Required**, Item type. Options: [`classic-key`, `rotated-secret`]

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`--new-name`: New item name

`--add-tag`: Tags to attach to this item. Repeat the flag to add multiple tags

`--rm-tag`: Tags to remove from this item. Repeat the flag to remove multiple tags

`--auto-rotate`: Enable or disable automatic rotation [`true`/`false`]

`--rotation-interval`: Number of days between automatic rotations

`--rotation-hour[=0]`: Rotation hour in UTC for rotated secrets

`--rotation-event-in`: Number of days before rotation to notify. Repeat the flag to add multiple events

`--rotator-creds-type[=use-self-creds]`: Credentials used for rotation

`-k, --key`: Key name used to encrypt the item value

`--description[=default_metadata]`: Description of the object

`--keep-prev-version`: Whether to keep the previous version [`true`/`false`]

`--delete-protection`: Protection from accidental deletion of this object [`true`/`false`]

### `list-gateways`

List all Gateways in the account.

#### Usage

```shell
akeyless list-gateways
```

## `gateway get`

Command to get specified gateway configuration

### `gateway get cache`

Get cache settings

#### Usage

```shell
akeyless gateway get cache \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

### `gateway get defaults`

Get defaults settings

#### Usage

```shell
akeyless gateway get defaults \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

## `gateway list`

### `gateway list customer-fragments`

Command to list the Customer Fragments on the Gateway

#### Usage

```shell
akeyless gateway list customer-fragments \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

## `gateway update`

Command to update specified gateway configuration

### `gateway update cache`

Updates cache settings

#### Usage

```shell
akeyless gateway update cache \
--enable-cache [true/false] \
--stale-timeout[=60] <Stale timeout in minutes> \
--enable-proactive [true/false] \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`--enable-cache`: Enable cache [`true`/`false`]

`--stale-timeout[=60]`: Stale timeout in minutes, cache entries which are not accessed within timeout will be removed from cache

`--enable-proactive`: Enable proactive caching [`true`/`false`]

`--minimum-fetch-interval[=5]`: When using Cache or/and Proactive Cache, additional secrets will be fetched upon requesting a secret, based on the requestor's access policy. Define minimum fetching interval to avoid over fetching in a given time frame

`--backup-interval[=1]`: Secure backup interval in minutes. To ensure service continuity during power cycles and network outages, secrets are backed up periodically according to the backup interval

`-u, --gateway-url`: Gateway URL (Configuration Management port)

### `gateway update defaults`

Updates defaults settings

#### Usage

```shell
akeyless gateway update defaults \
--saml-access-id[=use-existing] <saml-AccessID> \
--oidc-access-id[=use-existing] <oidc-AccessID> \
--cert-access-id[=use-existing] <cert-AccessID> \
--key[=Default] <gw encryption key> \
--event-on-status-change [true/false] \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`--saml-access-id[=use-existing]`: Default SAML `access-id` for UI login

`--oidc-access-id[=use-existing]`: Default OIDC `access-id` for UI login

`--cert-access-id[=use-existing]`: Default Certificate `access-id` for UI login

`--key[=Default]`: The name of the gateway default encryption key

`--hvp-route-version`: HashiCorp Vault Proxy route version to use [`1`/`2`]

`--event-on-status-change`: Trigger an event when Gateway status is changed [`true`/`false`]

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port)

### `gateway update certificate-store`

Update the Gateway certificate store.

Provide certificate content with either `--certificate-path` or `--certificate-data`.

#### Usage

```shell
akeyless gateway update certificate-store \
--name <Certificate display name> \
--certificate-path <Path/To/Certificate.pem> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`-n, --name`: **Required**, Certificate display name

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

`-p, --certificate-path`: Path to a file that contains the certificate in PEM format

`--certificate-data`: Certificate content in Base64 format

`-e, --expiration-event-in`: Number of days before certificate expiration to notify. Repeat the flag to add multiple events

## `gateway delete`

Command to delete specified gateway configuration.

### `gateway delete certificate-store`

Delete an entry from the Gateway certificate store.

#### Usage

```shell
akeyless gateway delete certificate-store \
--name <Certificate display name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

#### Flags

`-n, --name`: **Required**, Certificate display name

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)
