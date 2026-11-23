---
title: Terraform Ephemeral Resources
deprecated: false
hidden: false
metadata:
  robots: index
---
Terraform [ephemeral resources](https://developer.hashicorp.com/terraform/language/resources/ephemeral) let you fetch secret values for use during a plan or apply without writing them to the Terraform state file. Starting with [Terraform Provider](https://docs.akeyless.io/docs/terraform-provider) v2.2.0, the Akeyless provider exposes its secret-fetching data as ephemeral resources, so credentials never land in state in plain text.

Ephemeral resources require **Terraform 1.10 or later**. Combining them with a resource's write-only (`*_wo`) arguments, so a fetched value can be written somewhere without ever touching state, requires **Terraform 1.11 or later**.

## How It Works

Declare an `ephemeral` block instead of a `data` block:

```hcl
ephemeral "akeyless_static_secret" "db_password" {
  path = "/my-secret"
}
```

The resulting value is only available for the duration of the Terraform operation. Terraform only allows it to be referenced by another ephemeral resource, a provider configuration, or a resource's write-only argument — it cannot be assigned to an output or to a regular argument that Terraform persists in state.

## Available Ephemeral Resources

| Resource                     | Fetches                              | Key arguments                                                                                              | Returns                                       |
| ----------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- |
| `akeyless_static_secret`      | A static secret value                 | `path` (required), `version`, `ignore_cache`                                                                 | `value`                                        |
| `akeyless_dynamic_secret`     | A newly generated dynamic secret      | `path` (required), `target`, `args`, `host`, `dbname`, `timeout`                                             | `value`                                        |
| `akeyless_rotated_secret`     | A rotated secret value                | `name` (required), `host`, `version`, `ignore_cache`                                                         | `value`                                        |
| `akeyless_certificate`        | A certificate and its private key     | `name` (required), `version`, `ignore_cache`                                                                 | `certificate_pem`, `private_key_pem`           |
| `akeyless_pki_certificate`    | A newly issued PKI certificate        | `cert_issuer_name` (required), `common_name`, `alt_names`, `uri_sans`, `extended_key_usage`, `csr_data_base64`, `key_data_base64`, `ttl` | `data`, `cert_display_id`, `cert_item_id`, `parent_cert`, `path`, `reading_token` |
| `akeyless_ssh_certificate`    | A newly issued SSH certificate        | `cert_issuer_name` (required), `cert_username` (required), `public_key_data` (required), `ttl`, `legacy_signing_alg_name` | `data`, `path`                                 |
| `akeyless_target_details`     | A target's details, including credentials | `name` (required), `target_version`, `show_versions`                                                     | `value` (map)                                  |

All returned attributes are sensitive strings (`value` on `akeyless_target_details` is a sensitive map).

## Examples

### Fetch a Static Secret and Write It Out Without Storing It in State

Use the ephemeral value together with a write-only argument, so the value passes through without being saved in state:

```hcl
ephemeral "akeyless_static_secret" "db_password" {
  path = "/my-secret"
}

resource "akeyless_static_secret" "copy" {
  path              = "/my-secret-copy"
  value_wo          = ephemeral.akeyless_static_secret.db_password.value
  value_wo_version  = 1
}
```

### Configure a Provider with a Dynamic Secret

Dynamic secret values are often JSON-encoded. Fetch the credentials as an ephemeral resource and decode them directly into another provider's configuration:

```hcl
ephemeral "akeyless_dynamic_secret" "db_creds" {
  path = "/target/dynamic-secret-postgres"
}

provider "postgresql" {
  host     = "db.example.com"
  username = jsondecode(ephemeral.akeyless_dynamic_secret.db_creds.value)["user"]
  password = jsondecode(ephemeral.akeyless_dynamic_secret.db_creds.value)["password"]
}
```

### Issue a Short-Lived PKI Certificate

```hcl
ephemeral "akeyless_pki_certificate" "server_cert" {
  cert_issuer_name = "/pki/my-issuer"
  common_name      = "server.example.com"
  ttl              = 3600
}
```

## Good to Know

- **`akeyless_dynamic_secret`, `akeyless_pki_certificate` and `akeyless_ssh_certificate` issue new credentials on every Open.** Terraform opens ephemeral resources on both plan and apply, so each run generates two sets of credentials; the plan-time one is never used by apply. Terraform does not revoke either set, so rely on the secret's TTL to expire them.
- **Ephemeral resources don't replace data sources.** Use a `data` block when you need the value to persist in state, for example to detect drift between runs; use an `ephemeral` block when the value should never be written to state.

For the full reference, see the [Ephemeral Resources guide](https://registry.terraform.io/providers/akeyless-community/akeyless/latest/docs) in the Terraform Registry.
