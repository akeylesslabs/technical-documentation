---
title: Terraform Customized Retry
deprecated: false
hidden: false
metadata:
  robots: index
---
Large Terraform runs can send many requests to Akeyless at once and hit rate limits (HTTP `429 Too Many Requests`) or other temporary errors. Starting with [Terraform Provider](https://docs.akeyless.io/docs/terraform-provider) v2.1.0, you can tell the provider to retry these operations automatically, instead of failing the run.

By default, the provider retries only connection errors, such as a dropped or refused connection, up to 3 attempts. Every other error, including `429`, fails the operation. Customized retry lets you choose which errors to retry, how many times, and how long to wait.

## How It Works

Add a `retry` block to the provider, to a resource, or to both:

- **Provider&#x20;**`retry`**&#x20;block:** covers the retries for every resource in the configuration. If you want to cover all your resources in one place, define the `retry` block under the provider.
- **Resource&#x20;**`retry`**&#x20;block:** covers the retries for that resource only, and replaces the provider block for it.

When a resource's Create, Read, Update or Delete fails with an error that matches your settings, the provider waits and runs the whole operation again.

| Provider `retry` | Resource `retry` | What the provider uses              |
| ---------------- | ---------------- | ----------------------------------- |
| Not set          | Not set          | No extra retries (default behavior) |
| Set              | Not set          | The provider block                  |
| Not set          | Set              | The resource block                  |
| Set              | Set              | The resource block only             |

The `retry` block is available on every Akeyless resource. It isn't available on data sources.

## Retry Settings

A `retry` block requires at least one of `error_message_regex` or `retry_on_status_codes`; without one of them, the block has nothing to match and isn't applied.

| Setting                 | Default | Description                                                                               |
| ----------------------- | ------- | ----------------------------------------------------------------------------------------- |
| `retry_on_status_codes` | None    | HTTP status codes that trigger a retry, for example `[429, 503]`.                         |
| `error_message_regex`   | None    | Regular expressions matched against the error message, for example `"Too Many Requests"`. |
| `interval_seconds`      | `3`     | How long to wait before the first retry, in seconds. The wait doubles on each retry.      |
| `max_interval_seconds`  | `180`   | The longest wait between retries, in seconds.                                             |
| `max_retries`           | `3`     | How many times to retry after the first attempt.                                          |

### How Long the Provider Waits

The wait starts at `interval_seconds` and doubles on each retry, up to `max_interval_seconds`. If Akeyless tells the provider to wait longer (with a `Retry-After` header or a "will be released in N seconds" message), the provider waits that long instead, but never longer than `max_interval_seconds`.

## Examples

### Retry All Resources

```terraform
provider "akeyless" {
  api_gateway_address = "https://api.akeyless.io"

  api_key_login {
    access_id  = var.access_id
    access_key = var.access_key
  }

  retry {
    retry_on_status_codes = [429, 502, 503, 504]
    error_message_regex   = ["Too Many Requests", "will be released in"]
    interval_seconds      = 10
    max_retries           = 3
  }
}
```

### Retry One Resource

```terraform
resource "akeyless_dynamic_secret_mysql" "example" {
  name        = "mysql-ds"
  target_name = "my-mysql-target"

  retry {
    error_message_regex  = ["Too Many Requests", "will be released in"]
    interval_seconds     = 10
    max_interval_seconds = 180
    max_retries          = 3
  }
}
```

### Turn Off Retries for One Resource

To turn off the provider's retry for one resource, add a resource `retry` block with `max_retries = 0`. The block still needs `error_message_regex` or `retry_on_status_codes`.

```terraform
retry {
  retry_on_status_codes = [429]
  max_retries           = 0
}
```

## Good to Know

- **Changing only the&#x20;**`retry`**&#x20;block doesn't recreate or change the item.** `terraform plan` shows an in-place update, but the provider only saves the new retry settings.
- **Retry only temporary errors.** If a Create fails after the item was already created in Akeyless, a retry can fail with an "already exists" error. Use status codes and patterns that match only rate limits and temporary errors, such as `429`, `503` or `Too Many Requests`.

For the full reference, see the [Customized Retry guide](https://registry.terraform.io/providers/akeyless-community/akeyless/latest/docs/guides/customized_retry) in the Terraform Registry.