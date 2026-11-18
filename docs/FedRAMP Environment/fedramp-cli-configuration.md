---
title: FedRAMP CLI Configuration
deprecated: false
hidden: true
metadata:
  robots: index
---
# FedRAMP CLI Configuration

Point the Akeyless CLI at the FedRAMP environment by changing the API URL in a profile or an environment variable.

The Akeyless CLI is the same binary in every environment. By default, it connects to the commercial endpoint (`https://vault.akeyless.io`). To work with the FedRAMP environment, set the URL to the FedRAMP Vault endpoint, or to your Gateway.

## Which URL to Use

| URL                    | Value                               | When to use                                                                      |
| ---------------------- | ----------------------------------- | -------------------------------------------------------------------------------- |
| FedRAMP Vault endpoint | `https://vault.fedramp.akeyless.io` | Direct calls to the hosted control plane                                         |
| Your Gateway URL       | `https://<your-gateway-URL>:8000`   | Gateway-backed operations, such as dynamic secrets, rotated secrets, and targets |

<Callout icon="📘" theme="info">
  ### Note

  The Access ID, access key, and any credentials you use must belong to the FedRAMP account. Credentials from a commercial account are not valid in the FedRAMP environment.
</Callout>

## Option 1: Use a Dedicated Profile

Create a separate profile for the FedRAMP environment, so that you can switch between environments without editing configuration.

```shell
akeyless configure \
  --profile fedramp \
  --access-id <FEDRAMP_ACCESS_ID> \
  --access-type api_key \
  --access-key <FEDRAMP_ACCESS_KEY> \
  --gateway-url https://<your-gateway-URL>:8000
```

Run any command with the profile:

```shell
akeyless list-items --profile fedramp
```

Keep your existing commercial profile as is, and use `--profile` to choose the environment on every command.

## Option 2: Use Environment Variables

Environment variables are useful in CI/CD pipelines and containers.

```shell
export AKEYLESS_GATEWAY_URL="https://api.fedramp.akeyless.io"
export AKEYLESS_ACCESS_ID="<FEDRAMP_ACCESS_ID>"
export AKEYLESS_ACCESS_TYPE="api_key"
export AKEYLESS_ACCESS_KEY="<FEDRAMP_ACCESS_KEY>"
```

| Variable               | Description                                                                  |
| ---------------------- | ---------------------------------------------------------------------------- |
| `AKEYLESS_GATEWAY_URL` | The Public API Gateway or your Gateway URL. Set this to the FedRAMP endpoint |
| `AKEYLESS_ACCESS_ID`   | Access ID of an Auth Method in the FedRAMP account                           |
| `AKEYLESS_ACCESS_TYPE` | Authentication type, for example `api_key` or `aws_iam`                      |
| `AKEYLESS_ACCESS_KEY`  | Access key for the `api_key` type                                            |

## Authenticate and Verify

```shell
akeyless auth \
  --access-id <FEDRAMP_ACCESS_ID> \
  --access-type api_key \
  --access-key <FEDRAMP_ACCESS_KEY> \
```

A successful response returns a token. Then run a simple command, such as `akeyless list-items --profile fedramp`, to verify that the profile works.

## Switching Between Environments

| Environment | Profile   | URL                                 |
| ----------- | --------- | ----------------------------------- |
| Commercial  | `default` | `https://vault.akeyless.io`         |
| FedRAMP     | `fedramp` | `https://vault.fedramp.akeyless.io` |

Do not store the access key in shell history or in scripts. Use your CI/CD secret store, or retrieve it from Akeyless.

## Troubleshooting

| Symptom                                        | Likely cause                                                             | Action                                                                                         |
| ---------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| `Access ID not found` or `invalid credentials` | The command is still using the commercial URL, or a commercial Access ID | Check `--profile` and `AKEYLESS_GATEWAY_URL`                                                   |
| Timeout                                        | Egress to `*.fedramp.akeyless.io` is blocked                             | See [FedRAMP Network Connectivity](https://docs.akeyless.io/docs/fedramp-network-connectivity) |
| Environment variables are ignored              | A command-line flag or profile overrides the variables                   | Remove `--profile` and `--gateway-url` from the command, or unset the conflicting values       |