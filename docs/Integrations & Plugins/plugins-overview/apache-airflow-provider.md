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

| Capability | Class | Description |
| --- | --- | --- |
| **Hook** | `airflow.providers.akeyless.hooks.akeyless.AkeylessHook` | Interact with Akeyless directly from DAG code — fetch static, dynamic, and rotated secrets; create or delete items; list paths. |
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

The provider supports all Akeyless [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods):

| `access_type` | Required fields |
| --- | --- |
| `api_key` _default_ | `access_id`, `access_key` |
| `aws_iam` | `access_id` + `cloud_id` extras package |
| `gcp` | `access_id` + `cloud_id` extras package |
| `azure_ad` | `access_id` + `cloud_id` extras package |
| `uid` | `uid_token` |
| `jwt` | `access_id`, `jwt` |
| `k8s` | `access_id`, `k8s_auth_config_name` |
| `certificate` | `access_id`, `certificate_data`, `private_key_data` |

## Usage

### Airflow Connection (Hook)

Create an Airflow Connection with **Connection Type** = `akeyless`:

| Field | Value |
| --- | --- |
| Host | `https://api.akeyless.io` (or your Gateway URL) |
| Login | Your Akeyless Access ID |
| Password | Your Akeyless Access Key |
| Extra | `{"access_type": "api_key"}` |

Then use the hook in a DAG:

```python
from airflow.providers.akeyless.hooks.akeyless import AkeylessHook

hook = AkeylessHook(akeyless_conn_id="akeyless_default")

# Static secret
value = hook.get_secret_value("/my/secret")

# Multiple secrets at once
values = hook.get_secret_values(["/secret/a", "/secret/b"])

# Create a new secret
hook.create_secret("/new/secret", "my-value", description="Created by Airflow")

# Dynamic secret (e.g., database credentials producer)
creds = hook.get_dynamic_secret_value("/dynamic/db-producer")
print(creds["username"], creds["password"])

# Rotated secret
rotated = hook.get_rotated_secret_value("/rotated/db-creds")

# List and describe
items = hook.list_items("/path/prefix")
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

Or with environment variables:

```shell
export AIRFLOW__SECRETS__BACKEND="airflow.providers.akeyless.secrets.akeyless.AkeylessBackend"
export AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_path": "/airflow/connections", "variables_path": "/airflow/variables", "api_url": "https://api.akeyless.io", "access_id": "<Access ID>", "access_key": "<Access Key>"}'
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
