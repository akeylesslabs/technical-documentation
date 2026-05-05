---
title: Apache Airflow Provider
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

The `apache-airflow-providers-akeyless` package integrates the Akeyless identity security platform with [Apache Airflow](https://airflow.apache.org/). It lets you fetch secrets, manage credentials, and use Akeyless as a native Airflow Secrets Backend.

The provider is maintained in the [apache/airflow](https://github.com/apache/airflow/tree/main/providers/akeyless) repository.

## Before you begin

* You have an Akeyless account with at least one [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) configured.
* If using `api_key` authentication, you have your Access ID and Access Key ready.
* If using a cloud-based authentication method (AWS IAM, GCP, or Azure AD), install the `cloud_id` extras package (see [Installation](#installation)).
* Apache Airflow 2.11.0 or later is installed.

| Capability | Class | Description |
| --- | --- | --- |
| **Hook** | `airflow.providers.akeyless.hooks.akeyless.AkeylessHook` | Interact with Akeyless directly from Directed Acyclic Graph (DAG) code — fetch static, dynamic, and rotated secrets; create or delete items; list paths. |
| **Connection type** | `akeyless` | Airflow connection type identifier. Create a connection with this type in the Airflow UI or environment to supply credentials to the hook. |
| **Secrets Backend** | `airflow.providers.akeyless.secrets.akeyless.AkeylessBackend` | Transparently resolve Airflow Connections, Variables, and Config from Akeyless — no DAG code changes required. Supports `api_key` and `uid` authentication only. |

## Requirements

| Package | Minimum version |
| --- | --- |
| `apache-airflow` | 2.11.0 |
| `akeyless` | 5.0.0 |

## Installation

Install the base package:

```shell
pip install apache-airflow-providers-akeyless
```

For cloud-based authentication (AWS IAM, GCP, Azure AD) also install the cloud ID extras:

```shell
pip install apache-airflow-providers-akeyless[cloud_id]
```

## Authentication Methods

The provider supports the following Akeyless [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods):

| `access_type` | Required fields | Supported by |
| --- | --- | --- |
| `api_key` _default_ | `access_id`, `access_key` | Hook, Secrets Backend |
| `aws_iam` | `access_id` + `cloud_id` extras package | Hook only |
| `gcp` | `access_id` + `cloud_id` extras package | Hook only |
| `azure_ad` | `access_id` + `cloud_id` extras package | Hook only |
| `uid` | `uid_token` | Hook, Secrets Backend |
| `jwt` | `access_id`, `jwt` | Hook only |
| `k8s` | `access_id`, `k8s_auth_config_name` | Hook only |
| `certificate` | `access_id`, `certificate_data`, `private_key_data` | Hook only |

> ⚠️ **Unsupported authentication methods:** The following Akeyless authentication methods are **not** supported by this provider: OCI IAM, Kerberos, LDAP, SAML, OIDC, and Email.

## Usage

### Airflow Connection (Hook)

Create an Airflow Connection with **Connection Type** = `akeyless`:

| Field | Value |
| --- | --- |
| Host | `https://api.akeyless.io` (or your Gateway URL) |
| Login | Your Akeyless Access ID |
| Password | Your Akeyless Access Key (for `api_key` authentication; leave blank for other types) |
| Extra | JSON object with `access_type` and any authentication-method-specific fields (refer to the next section) |

The `Extra` field controls authentication. Examples by authentication method:

| `access_type` | `Extra` JSON |
| --- | --- |
| `api_key` (default) | `{"access_type": "api_key"}` |
| `uid` | `{"access_type": "uid", "uid_token": "<UID token>"}` — `Login` and `Password` are unused |
| `jwt` | `{"access_type": "jwt", "jwt": "<JWT>"}` |
| `k8s` | `{"access_type": "k8s", "k8s_auth_config_name": "<config name>"}` |
| `aws_iam` / `gcp` / `azure_ad` | `{"access_type": "aws_iam"}` — cloud identity is resolved automatically |
| `certificate` | `{"access_type": "certificate", "certificate_data": "<PEM>", "private_key_data": "<PEM>"}` |

Then use the hook in a DAG:

```python
from airflow.providers.akeyless.hooks.akeyless import AkeylessHook

hook = AkeylessHook(akeyless_conn_id="akeyless_default")
```

#### Fetching secrets

```python
# Static secret
value = hook.get_secret_value("/my/secret")

# Multiple static secrets at once
values = hook.get_secret_values(["/secret/a", "/secret/b"])

# Dynamic secret (for example, a database credentials producer)
creds = hook.get_dynamic_secret_value("/dynamic/db-producer")
username, password = creds["username"], creds["password"]

# Rotated secret
rotated = hook.get_rotated_secret_value("/rotated/db-creds")
```

#### Managing secrets

```python
# Create a static secret
hook.create_secret("/new/secret", "my-value", description="Created by Airflow")

# List items under a path
items = hook.list_items("/path/prefix")

# Describe an item (returns metadata)
meta = hook.describe_item("/my/secret")
```

### Secrets Backend

Configure Airflow to fetch Connections, Variables, and Config directly from Akeyless.

Add to `airflow.cfg`:

```text
[secrets]
backend = airflow.providers.akeyless.secrets.akeyless.AkeylessBackend
backend_kwargs = {
    "connections_path": "/airflow/connections",
    "variables_path": "/airflow/variables",
    "config_path": "/airflow/config",
    "api_url": "https://api.akeyless.io",
    "access_id": "<Access ID>",
    "access_key": "<Access Key>",
    "access_type": "api_key"
    }
```

> ℹ️ In `airflow.cfg`, multi-line `backend_kwargs` values must have each continuation line indented with at least one space. Alternatively, provide the value as a single-line JSON string.

Or with environment variables:

```shell
export AIRFLOW__SECRETS__BACKEND="airflow.providers.akeyless.secrets.akeyless.AkeylessBackend"
export AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_path": "/airflow/connections", "variables_path": "/airflow/variables", "config_path": "/airflow/config", "api_url": "https://api.akeyless.io", "access_id": "<Access ID>", "access_key": "<Access Key>", "access_type": "api_key"}'
```

#### Naming Convention

Secrets are looked up by joining `<base_path>/<key>`:

| Type | Example lookup path |
| --- | --- |
| Connection `postgres_default` | `/airflow/connections/postgres_default` |
| Variable `my_var` | `/airflow/variables/my_var` |
| Config `smtp_host` | `/airflow/config/smtp_host` |

#### Storing Connections in Akeyless

Store the connection secret value in one of these formats:

URI format:

```text
postgresql://user:password@host:5432/dbname
```

JSON format:

```json
{
  "conn_type": "postgres",
  "host": "db.example.com",
  "login": "admin",
  "password": "secret",
  "schema": "mydb",
  "port": 5432
}
```

JSON with `conn_uri`:

```json
{
  "conn_uri": "postgresql://user:password@host:5432/dbname"
}
```

### Cloud-Based Authentication

For AWS IAM, GCP, or Azure AD, omit `access_key` and set the appropriate `access_type`. The provider uses the workload's cloud identity automatically.

> ⚠️ **Secrets Backend limitation:** `AkeylessBackend` only supports `api_key` and `uid` authentication. For cloud-based authentication (AWS IAM, GCP, Azure AD) use `AkeylessHook` directly in your DAGs.

Example using AWS IAM with the hook:

```python
from airflow.providers.akeyless.hooks.akeyless import AkeylessHook

hook = AkeylessHook(akeyless_conn_id="akeyless_aws_iam")
value = hook.get_secret_value("/my/secret")
```

Set the connection `access_type` extra field to `aws_iam` and install the `cloud_id` extras. The hook authenticates using the workload's AWS IAM identity (EC2 instance profile, ECS task role, and so on) — no static credentials required.

## Troubleshooting

### `ImportError: akeyless_cloud_id is required`

You are using `aws_iam`, `gcp`, or `azure_ad` authentication without the cloud ID extras package. Install it:

```shell
pip install apache-airflow-providers-akeyless[cloud_id]
```

### `ValueError: Unsupported access_type for AkeylessBackend`

`AkeylessBackend` only supports `api_key` and `uid`. For cloud-based authentication in the Secrets Backend, use `AkeylessHook` directly in your DAGs instead.

### Secret not found when using Secrets Backend

Verify that the secret path in Akeyless matches the expected naming convention: `<base_path>/<key>`. For example, a Connection with `conn_id = postgres_default` is looked up at `<connections_path>/postgres_default`. Confirm the path and value are present in Akeyless, then restart Airflow for the configuration to take effect.

### Authentication fails with `401 Unauthorized`

* For `api_key`: confirm the Access ID in **Login** and the Access Key in **Password** are correct.
* For `uid`: confirm the `uid_token` in the `Extra` field is valid and not expired.
* For cloud-based authentication methods: confirm the workload has the expected IAM role or service account attached.
