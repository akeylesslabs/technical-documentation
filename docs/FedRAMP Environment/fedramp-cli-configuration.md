---
title: FedRAMP CLI Configuration
deprecated: false
hidden: true
metadata:
  robots: index
---

# FedRAMP CLI Configuration

Point the Akeyless CLI at the FedRAMP environment by changing the vault DNS in the CLI settings file.

The Akeyless CLI is the same binary in every environment. By default, it connects to the commercial vault endpoint (`vault.akeyless.io`). To work with the FedRAMP environment, set the CLI to use `vault.fedramp.akeyless.io`, and use credentials from your FedRAMP account.

## Two Different URLs

The CLI uses two separate settings. Do not mix them up.

| Setting | Where it is set | FedRAMP value | What it points to |
| ------- | --------------- | ------------- | ----------------- |
| **Vault DNS** (control plane) | `dns` in the `~/.akeyless/settings` file | `vault.fedramp.akeyless.io` | The Akeyless FedRAMP environment |
| **Gateway URL** | `gateway_url` in a profile, the `--gateway-url` flag, or the `AKEYLESS_GATEWAY_URL` variable | `https://<your-gateway-host>:8000/api/v1` | Your own Gateway, deployed in your environment |

> 📘 Note
>
> Use `vault.fedramp.akeyless.io` as the CLI endpoint. Do not point the CLI at the public API gateway (`api.fedramp.akeyless.io`). The Gateway URL is optional, and it must always be the URL of a Gateway that is connected to the FedRAMP environment.

## Configure the Vault DNS

The CLI reads its endpoint from the `settings` file in your Akeyless home folder.

| Operating system | Path |
| ---------------- | ---- |
| Linux and macOS | `~/.akeyless/settings` |
| Windows | `%USERPROFILE%\.akeyless\settings` |

For the commercial environment, the file contains:

settings

```toml
dns="vault.akeyless.io"
protocol="https"
```

For the FedRAMP environment, change `dns`:

settings

```toml
dns="vault.fedramp.akeyless.io"
protocol="https"
```

Keep `protocol` set to `https`.

> 📘 Note
>
> The `settings` file applies to the whole CLI installation, not to a single profile. When you switch between the commercial and FedRAMP environments, switch the `settings` file as well as the profile. See [Switching Between Environments](#switching-between-environments).

## Create a FedRAMP Profile

Create a dedicated profile for the FedRAMP account, so that your commercial profile is not changed. The Access ID and key must belong to the FedRAMP account.

```shell
akeyless configure \
  --profile fedramp \
  --access-id <FEDRAMP_ACCESS_ID> \
  --access-type api_key \
  --access-key <FEDRAMP_ACCESS_KEY>
```

Add `--gateway-url` only if you want gateway-backed operations to go through your FedRAMP Gateway:

```shell
akeyless configure \
  --profile fedramp \
  --access-id <FEDRAMP_ACCESS_ID> \
  --access-type api_key \
  --access-key <FEDRAMP_ACCESS_KEY> \
  --gateway-url https://<your-gateway-host>:8000/api/v1
```

Run any command with the profile:

```shell
akeyless list-items --profile fedramp
```

## Use Environment Variables for the Gateway URL

To route CLI calls through your FedRAMP Gateway without a profile (for example, in CI/CD), set the Gateway URL as a variable:

```shell
export AKEYLESS_GATEWAY_URL="https://<your-gateway-host>:8000/api/v1"
```

When this variable is set, it takes priority over the `gateway_url` value in the profile. The variable sets the Gateway URL only. It does not change the vault DNS. The vault DNS is always taken from the `settings` file.

## Authenticate and Verify

1. Confirm the `settings` file contains `dns="vault.fedramp.akeyless.io"`.
2. Authenticate with the FedRAMP profile:

   ```shell
   akeyless auth --profile fedramp
   ```

3. Run a simple command to confirm access to the FedRAMP account:

   ```shell
   akeyless list-items --profile fedramp
   ```

## Switching Between Environments

Because `settings` is shared by all profiles, keep one copy per environment and switch both the file and the profile.

```shell
# One-time setup
cp ~/.akeyless/settings ~/.akeyless/settings.commercial
printf 'dns="vault.fedramp.akeyless.io"\nprotocol="https"\n' > ~/.akeyless/settings.fedramp

# Switch to FedRAMP
cp ~/.akeyless/settings.fedramp ~/.akeyless/settings

# Switch back to commercial
cp ~/.akeyless/settings.commercial ~/.akeyless/settings
```

| Environment | `dns` in `settings` | Profile |
| ----------- | ------------------- | ------- |
| Commercial | `vault.akeyless.io` | `default` |
| FedRAMP | `vault.fedramp.akeyless.io` | `fedramp` |

Do not store access keys in scripts or shell history. Use your CI/CD secret store, or retrieve them from Akeyless.

## Troubleshooting

| Symptom | Likely cause | Action |
| ------- | ------------ | ------ |
| `Access ID not found` or `invalid credentials` | `dns` is still `vault.akeyless.io`, or the profile holds a commercial Access ID | Check the `settings` file and the `--profile` value |
| Timeout | Egress to `*.fedramp.akeyless.io` is blocked | See [FedRAMP Network Connectivity](https://docs.akeyless.io/docs/fedramp-network-connectivity) |
| Gateway-backed commands fail | `gateway_url` or `AKEYLESS_GATEWAY_URL` points to a commercial Gateway, or is missing `/api/v1` | Use the URL of a Gateway connected to the FedRAMP environment |
| Commands go to a different Gateway than expected | `AKEYLESS_GATEWAY_URL` overrides the profile's `gateway_url` | Unset the variable, or set it to the FedRAMP Gateway |
