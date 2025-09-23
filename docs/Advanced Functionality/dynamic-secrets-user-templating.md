---
title: Custom Username for Dynamic Secrets
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
By default, a [Dynamic Secret](doc:how-to-create-dynamic-secret)  is generated using a randomly assigned username. This is well-suited for ephemeral access scenarios where short-lived, unique credentials are preferred.

However, in cases where you need to use a **custom**  or **predefined** username, for example, to align with existing identities or to integrate with external systems that require consistent naming, you can define a [template](https://pkg.go.dev/text/template) using the supported Go functions listed below. 

> 👍 Note
>
> This feature is available only from GW version `4.34.0` and higher. Ensure you have enough randomness in your template to support the uniqueness of multiple usernames in parllel when using custom templates

# Supported Functions

You can use the following built-in functions to construct custom usernames dynamically:

**String/Character manipulation**:

* `uppercase / lowercase` – Converts input to upper or lower case. 

* `replace` – Replaces a portion of a string with another value.

* `truncate` – Trims a string or binary value to a defined length.

* `truncate_sha256` – Produces a `SHA‑256` hash and then truncates the result.

* `restricted_chars` – Filters or handles characters that are not allowed.

**Value Generation**:

* `random` – Generates a random string from lowercase letters, uppercase letters, and numbers.

* `timestamp` – Outputs the current timestamp.

* `unix_time` – The current Unix timestamp (number of seconds since`1970‑01‑01 UTC`).

* `unix_time_millis` – The current Unix timestamp in milliseconds.

* `uuid` – Generates a universally unique identifier (`UUID`).

**Hashing & Encoding**:

* `base64` – Encodes or decodes input using `Base64`.

* `sha256` – Computes a SHA‑256 hash of the input.

# Available Fields

By default, the following field values are available in your template using the `{{.field}}` syntax:

* `{{.UniqueIdentifier}}`

* `{{.DynamicSecretName}}`

If the field is not recognized, the system will attempt to retrieve it from [Sub-Claims](doc:sub-claims) and fail if not found. You can use any other available sub-claims in your template

# Examples

1. **Unique Identifier**  with random suffix:

```shell
user-{{.UniqueIdentifier}}-{{ random 4 }}
```

**Output**:

```shell
user-john.doe-7f3a
```

The example above combines the Unique identifier with a short random suffix. This is useful for generating multiple credentials per user while avoiding name collisions.

2. **Lowercased** secret name with truncated **UUID** hash:

```shell
{{ lowercase .DynamicSecretName }}-{{ truncate_sha256 uuid 6 }}
```

**Output**:

```shell
db-access-dev-2c91e3
```

The example above converts the secret name to lowercase and appends a shortened hash of a generated UUID. This keeps the format clean, consistent, and unique.

3. **Base64** encoded Unique Identifier with millisecond **timestamp**:

```shell
{{ base64 .UniqueIdentifier }}-{{ unix_time_millis }}
```

**Output**:

```shell
am9obi5kb2VAZXhhbXBsZS5jb20=-1720258847654
```

The example above encodes the Unique Identifier in Base64 and appends a millisecond-precision timestamp to ensure a high degree of uniqueness.
