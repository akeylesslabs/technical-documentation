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
| **Hook** | `airflow.providers.akeyless.hooks.akeyless.AkeylessHook` | Interact with Akeyless directly from Directed Acyclic Graph (DAG) code — fetch static, dynamic, and rotated secrets; create, update, or delete items; list paths. |
| **Connection type** | `akeyless` | Airflow connection type identifier. Create a connection with this type in the Airflow UI or environment to supply credentials to the hook. |
| **Secrets Backend** | `airflow.providers.akeyless.secrets.akeyless.AkeylessBackend` | Transparently resolve Airflow Connections, Variables, and Config from Akeyless — no DAG code changes required. Supports `api_key`, `uid`, `aws_iam`, `gcp`, and `azure_ad` authentication. |

## Requirements

| Requirement | Minimum version |
| --- | --- |
| Python | 3.10 |
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
| `aws_iam` | `access_id` + `cloud_id` extras package | Hook, Secrets Backend |
| `gcp` | `access_id` + `cloud_id` extras package; optional: `gcp_audience` | Hook, Secrets Backend |
| `azure_ad` | `access_id` + `cloud_id` extras package; optional: `azure_object_id` | Hook, Secrets Backend |
| `uid` | `uid_token` | Hook, Secrets Backend |
| `jwt` | `access_id`, `jwt` | Hook only |
| `k8s` | `access_id`, `k8s_auth_config_name` | Hook only |
| `certificate` | `access_id`, `certificate_data`, `private_key_data` | Hook only |

> ⚠️ **Unsupported authentication methods:** The following Akeyless authentication methods are **not** supported by this provider: OCI IAM, Kerberos, LDAP, SAML, OIDC, and Email.

## Usage

### Airflow Connection (Hook)

Create an Airflow Connection with **Connection Type** = `akeyless`.

#### Via the Airflow UI

In the Airflow UI connection form, the following fields are available:

| UI field | Value |
| --- | --- |
| API URL | `https://api.akeyless.io` (or your Gateway URL) |
| Access ID | Your Akeyless Access ID |
| Access Key | Your Akeyless Access Key (for `api_key` authentication; leave blank for other types) |
| Access type | One of the `access_type` values from [Authentication Methods](#authentication-methods) (default: `api_key`) |

The form also shows dedicated fields for each authentication-method-specific parameter: **UID Token**, **JWT**, **K8s Auth Config Name**, **Certificate Data (PEM)**, **Private Key Data (PEM)**, **GCP Audience**, and **Azure Object ID**. The raw **Extra**, **Schema**, and **Port** fields are hidden.

#### Via environment variable or CLI

When defining connections outside the UI (for example, with `AIRFLOW_CONN_*` environment variables), provide the `extra` field as a JSON object:

| `access_type` | `extra` JSON |
| --- | --- |
| `api_key` (default) | `{"access_type": "api_key"}` |
| `uid` | `{"access_type": "uid", "uid_token": "<UID token>"}` — `login` and `password` are unused |
| `jwt` | `{"access_type": "jwt", "jwt": "<JWT>"}` |
| `k8s` | `{"access_type": "k8s", "k8s_auth_config_name": "<config name>"}` |
| `aws_iam` | `{"access_type": "aws_iam"}` — cloud identity resolved automatically |
| `gcp` | `{"access_type": "gcp"}` or `{"access_type": "gcp", "gcp_audience": "<audience>"}` |
| `azure_ad` | `{"access_type": "azure_ad"}` or `{"access_type": "azure_ad", "azure_object_id": "<object ID>"}` |
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

# Update a static secret's value
hook.update_secret_value("/new/secret", "updated-value")

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

For `uid` authentication, omit `access_key` and include `uid_token` in `backend_kwargs` instead:

```text
[secrets]
backend = airflow.providers.akeyless.secrets.akeyless.AkeylessBackend
backend_kwargs = {
    "connections_path": "/airflow/connections",
    "variables_path": "/airflow/variables",
    "config_path": "/airflow/config",
    "api_url": "https://api.akeyless.io",
    "access_id": "<Access ID>",
    "access_type": "uid",
    "uid_token": "<UID token>"
    }
```

Or with environment variables:

```shell
export AIRFLOW__SECRETS__BACKEND="airflow.providers.akeyless.secrets.akeyless.AkeylessBackend"
export AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_path": "/airflow/connections", "variables_path": "/airflow/variables", "config_path": "/airflow/config", "api_url": "https://api.akeyless.io", "access_id": "<Access ID>", "access_key": "<Access Key>", "access_type": "api_key"}'
```

#### Cloud-based authentication in the Secrets Backend

The Secrets Backend supports `aws_iam`, `gcp`, and `azure_ad` authentication, allowing managed Airflow services to authenticate using their workload identity — no static API keys required.

**AWS IAM** (for [Amazon MWAA](https://aws.amazon.com/managed-workflows-for-apache-airflow/) and EC2/ECS/EKS workloads):

```text
[secrets]
backend = airflow.providers.akeyless.secrets.akeyless.AkeylessBackend
backend_kwargs = {
    "connections_path": "/airflow/connections",
    "variables_path": "/airflow/variables",
    "config_path": "/airflow/config",
    "api_url": "https://api.akeyless.io",
    "access_id": "<Access ID>",
    "access_type": "aws_iam"
    }
```

**GCP** (for [Managed Service for Apache Airflow](https://cloud.google.com/composer/docs) and GCE/GKE workloads):

```text
[secrets]
backend = airflow.providers.akeyless.secrets.akeyless.AkeylessBackend
backend_kwargs = {
    "connections_path": "/airflow/connections",
    "variables_path": "/airflow/variables",
    "config_path": "/airflow/config",
    "api_url": "https://api.akeyless.io",
    "access_id": "<Access ID>",
    "access_type": "gcp",
    "gcp_audience": "akeyless.io"
    }
```

**Azure AD** (for Azure-hosted workloads):

```text
[secrets]
backend = airflow.providers.akeyless.secrets.akeyless.AkeylessBackend
backend_kwargs = {
    "connections_path": "/airflow/connections",
    "variables_path": "/airflow/variables",
    "config_path": "/airflow/config",
    "api_url": "https://api.akeyless.io",
    "access_id": "<Access ID>",
    "access_type": "azure_ad",
    "azure_object_id": "<Azure Object ID>"
    }
```

> ℹ️ Cloud-based authentication requires the `cloud_id` extras package. See [Installation](#installation).

##### Using with Amazon MWAA

1. Upload a `requirements.txt` to your MWAA S3 bucket containing:

   ```text
   apache-airflow-providers-akeyless[cloud_id]
   ```

2. In the MWAA console under **Airflow configuration options**, add:

   | Key | Value |
   | --- | --- |
   | `secrets.backend` | `airflow.providers.akeyless.secrets.akeyless.AkeylessBackend` |
   | `secrets.backend_kwargs` | `{"api_url": "https://api.akeyless.io", "access_id": "<Access ID>", "access_type": "aws_iam"}` |

3. Ensure the MWAA VPC has outbound HTTPS access to your Akeyless API endpoint (`api.akeyless.io` or your Akeyless Gateway).

4. Create an Akeyless `aws_iam` Authentication Method associated with the MWAA execution role ARN.

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

For AWS IAM, GCP, or Azure AD, omit `access_key` and set the appropriate `access_type`. The provider uses the workload's cloud identity automatically. Both the **Hook** and the **Secrets Backend** support cloud-based authentication.

Example using AWS IAM with the hook:

```python
from airflow.providers.akeyless.hooks.akeyless import AkeylessHook

hook = AkeylessHook(akeyless_conn_id="akeyless_aws_iam")
value = hook.get_secret_value("/my/secret")
```

Set the connection `access_type` extra field to `aws_iam` and install the `cloud_id` extras. The hook authenticates using the workload's AWS IAM identity (EC2 instance profile, ECS task role, and so on) — no static credentials required.

For Secrets Backend cloud authentication configuration examples, see [Cloud-based authentication in the Secrets Backend](#cloud-based-authentication-in-the-secrets-backend).

## Troubleshooting

### `ImportError: akeyless_cloud_id is required`

You are using `aws_iam`, `gcp`, or `azure_ad` authentication without the cloud ID extras package. Install it:

```shell
pip install apache-airflow-providers-akeyless[cloud_id]
```

### `ValueError: Unsupported access_type for AkeylessBackend`

`AkeylessBackend` supports `api_key`, `uid`, `aws_iam`, `gcp`, and `azure_ad`. Other authentication types (`jwt`, `k8s`, `certificate`) are only available through `AkeylessHook`.

### Secret not found when using Secrets Backend

Verify that the secret path in Akeyless matches the expected naming convention: `<base_path>/<key>`. For example, a Connection with `conn_id = postgres_default` is looked up at `<connections_path>/postgres_default`. Confirm the path and value are present in Akeyless, then restart Airflow for the configuration to take effect.

### Authentication fails with `401 Unauthorized`

* For `api_key`: confirm the **Access ID** and **Access Key** fields in the connection are correct.
* For `uid`: confirm the `uid_token` value is valid and not expired.
* For cloud-based authentication methods: confirm the workload has the expected IAM role or service account attached.
