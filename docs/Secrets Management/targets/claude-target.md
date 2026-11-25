---
title: Claude Target
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define a [Claude](https://www.anthropic.com/api) target to be used for [AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight) in your account, and for the [Claude Scanner](doc:claude-scanner) in [Identity & Secrets Intelligence](doc:identity-and-secrets-intelligence).

For the Claude Scanner, set the **API Key** to an organization-scoped API key of a service account. The **Admin** role reads members, keys, workspaces, usage, the compliance settings, and Managed Agents. The **Developer** role is the least-privileged option, but cannot read the compliance settings or the workspace member roles. An Admin API key, or an `org:admin` OAuth access token, is also accepted, but cannot read Managed Agents, which the scan then reports as a permission gap.

A Claude target can authenticate to Anthropic in one of two ways:

- **API Key** (default): A static Claude API key.
- **Workload Identity Federation (WIF)**: The Gateway exchanges an OIDC JWT for a short-lived Claude access token bound to a Claude service account, so no static API key is stored, rotated, or at risk of leaking.

## Create a Claude Target with the CLI

To create a Claude target with an API key, run the following command:

```shell
akeyless target create claude \
  --name <target name> \
  --api-key <Claude API key> \
  --claude-url <Claude API base URL> \
  --key <protection key>
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
- `api-key`: The Claude API key.
- `claude-url`: The Claude API base URL. Default: `https://api.anthropic.com`
- `key`: The protection key used to encrypt the target secret value. If not specified, the account default protection key is used.

To create a Claude target with Workload Identity Federation instead, run the following command:

```shell
akeyless target create claude \
  --name <target name> \
  --use-gw-cloud-identity \
  --wif-organization-id <Anthropic organization ID> \
  --wif-service-account-id <Claude service account ID (svac_...)> \
  --wif-federation-rule-id <Federation rule ID (fdrl_...)> \
  --wif-workspace-id <Workspace ID (wrkspc_...)> \
  --key <protection key>
```

Where:

- `use-gw-cloud-identity`: A boolean flag to use Workload Identity Federation instead of a static API key. Cannot be used together with `api-key`.
- `wif-organization-id`: The Anthropic organization ID.
- `wif-service-account-id`: The Claude service account ID (`svac_...`).
- `wif-federation-rule-id`: The federation rule ID (`fdrl_...`).
- `wif-workspace-id`: Optional, the workspace ID (`wrkspc_...`), needed only when the federation rule covers more than one workspace.

On save, Akeyless validates the target by exchanging the Gateway's identity token for a Claude access token and calling the Anthropic API with it; the target creation fails with a clear error if validation does not succeed.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets]() section.

## Create a Claude Target in the Console

1. Log in to the Akeyless Console, and go to **Targets** > **New** > **AI (Claude)**.&#x20;
2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
   For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).
4. Select an **Auth type**:
   - **API Key**:
     - **API Key**: The Claude API key.
     - **Claude URL**: The Claude API base URL. Default: `https://api.anthropic.com`
   - **Workload Identity Federation**:
     - **Organization ID**: The Anthropic organization ID.
     - **Service Account ID**: The Claude service account ID (`svac_...`).
     - **Federation Rule ID**: The federation rule ID (`fdrl_...`).
     - **Workspace ID**: Optional, needed only when the federation rule covers more than one workspace.

Existing API key targets continue to work unchanged.

<br />
