---
title: CLI Profiles
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
CLI profiles store authentication and command defaults for the Akeyless CLI.

## When to use profiles

Profiles are useful when you need to:

* Switch between tenants or environments.
* Use different authentication methods for different workflows.
* Keep Gateway or default path settings scoped to specific command contexts.
* Run automation with a consistent default profile while still allowing command-level override.

## Create and use profiles

### Create a profile

To create a profile explicitly, run:

```shell
akeyless configure --profile <profile name> --access-id <Access ID> --access-type <access type>
```

The `--profile` flag names the profile file that the CLI stores under `.akeyless/profiles`.

`configure` supports multiple access types, including `access_key`, `password`, `azure_ad`, `saml`, `oidc`, `aws_iam`, `gcp`, `k8s`, `cert`, `oci`, and `kerberos`. Add the flags required for the selected access type.

For example:

```shell API Key
akeyless configure --profile <profile name> --access-id <Access ID> --access-key <Access key> --access-type access_key
```
```shell Email
akeyless configure --profile <profile name> --access-id <Access ID> --admin-email <Email> --admin-password <Password> --access-type password
```

You can also create a profile during first-time CLI setup when the CLI prompts for a profile name.

### Where profiles are stored

Profile definitions are stored as individual `toml` files under `.akeyless/profiles` in the user's home directory.

To inspect them locally, run:

```shell
cd .akeyless/profiles/
```

The CLI also stores default-profile settings in `.akeyless/settings`.

### Use a profile on a command

After creating an additional profile, add the `--profile` flag with the profile name to any `akeyless` command:

```shell
akeyless get-secret-value --name /path/to/secret --profile <profile name>
```

An explicit `--profile` flag takes precedence over environment and settings-based defaults.

## Manage the default profile

> ⚠️ **Warning:**
>
> Support for changing the default profile with `set-default-profile` and viewing it with `get-default-profile` was added in CLI version `1.142.0`.

### Default profile precedence

The CLI resolves the effective default profile in this order:

1. Explicit `--profile` flag on the command.
2. `AKEYLESS_DEFAULT_PROFILE` environment variable.
3. `default_profile` stored in `.akeyless/settings`.
4. Built-in fallback value `default`.

### Set the default profile

To set the default profile used when `--profile` is not specified, run:

```shell
akeyless set-default-profile --profile <profile name>
```

This command persists the selected profile name in `.akeyless/settings`.

### View the default profile

To display the effective default profile information, run:

```shell
akeyless get-default-profile
```

The command output includes:

* Profile name
* Authentication type
* Akeyless URL
* Access ID
* Redacted token
* Token expiry

If the CLI is not currently authenticated, the command reports **Access ID**, **Token**, and **Token expiry** as `Not authenticated`.

### Edit the default profile manually

Because the default profile is stored in `.akeyless/settings`, changing the active default profile is separate from editing the individual profile files under `.akeyless/profiles`.

If needed, you can edit the `default_profile` value manually in `.akeyless/settings`, but Akeyless recommends using `akeyless set-default-profile --profile <profile name>` so the setting is written in the supported format.

Editing a profile's `toml` file changes that profile's configuration, but does not change which profile is treated as the default.

If both `AKEYLESS_DEFAULT_PROFILE` and `default_profile` are set, the environment variable wins for that shell or process.

## Profile configuration defaults

Profiles can include command defaults in addition to authentication settings.

For example:

```toml default.toml
["default"]
  gateway_url = 'https://<Your-Akeyless-GW-URL>:8000'
  default_location_prefix = 'non-production'
  cert_issuer_name = '/cert/IssuerName'
  cert_username = 'ubuntu'
  public_key_file_path = 'ssh/id_rsa.pub'
  legacy_signing_alg = 'true|false'
```

Where:

* `gateway_url`: Akeyless Gateway URL, port `8000`, for Gateway-dependent workflows such as certain dynamic secret operations. For general CLI API calls through a non-public Gateway, use `AKEYLESS_GATEWAY_URL` instead.
* `default_location_prefix`: Global default prefix for the `name` flag.
* `cert_issuer_name`: Default [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates) name.
* `cert_username`: Default username for issued SSH certificates.
* `public_key_file_path`: Path to the SSH public key file.
* `legacy_signing_alg`: Use the SSH legacy signing algorithm.
