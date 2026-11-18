---
title: FedRAMP Account Onboarding
deprecated: false
hidden: true
metadata:
  robots: index
---
# FedRAMP Account Onboarding

Register your account in the FedRAMP tenant and onboard users to the FedRAMP Console.

In the FedRAMP environment, Console access has an extra first step. Before a person can use the Akeyless Console, they must be onboarded into the **hosted-provider identity layer** (the Game Warden identity service). After that first sign-in, account administration, auth methods, roles, and secrets work as they do in the commercial environment.

## How Access Works

Access to the FedRAMP environment has two layers:

| Layer                                                   | Who it applies to                           | What it does                                                                                                                                                      |
| ------------------------------------------------------- | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Hosted-provider IdP** (Game Warden identity layer) | People who use the Console                  | Authenticates the user before they reach the Akeyless Console. Can be federated to your corporate IdP (SAML or OIDC), with MFA enforced at your IdP               |
| **2. Akeyless authentication**                          | Everyone and everything that calls Akeyless | Auth methods, roles, and access policies inside your Akeyless account. Workloads, Gateways, the CLI, and SDKs authenticate directly to Akeyless with an Access ID |

<Callout icon="📘" theme="info">
  ### Note

  Machine identities (applications, Gateways, CI/CD, scripts) do not sign in through the hosted-provider IdP. They authenticate directly with Akeyless, using an auth method such as API Key or AWS IAM. See [User and Identity Types](#user-and-identity-types).
</Callout>

## Prerequisites

Before onboarding, make sure that:

- A federal order and addendum are in place, and Akeyless has confirmed that your account(s) are provisioned in the FedRAMP tenant. Accounts are created in Staging first, and then in Production.
- You have the list of initial administrators (name and work email).
- If you federate Console access to your corporate IdP: you have the IdP protocol (SAML or OIDC), the IdP metadata or discovery URL, and a technical contact who can configure the IdP side.
- Your network allows outbound HTTPS (443) to the FedRAMP domain. See [FedRAMP Network Connectivity](https://docs.akeyless.io/docs/fedramp-network-connectivity).

## Onboarding Flow

1. **Provide onboarding details to Akeyless.** Share the initial administrator list and your IdP details (SAML or OIDC) with your Akeyless Customer Success team.

2. **Account creation.** Akeyless creates your account(s) in the FedRAMP tenant, assigns the initial administrators, and sends you the FedRAMP endpoints for the environment (Staging or Production).

3. **Identity onboarding in the hosted-provider IdP.** Each user is onboarded into the Game Warden identity layer. When federation is used, sign-in is brokered to your corporate IdP, and MFA is enforced there. The federation procedure is confirmed with the hosting provider during onboarding.

4. **Sign in to the FedRAMP Console.** Open the FedRAMP Console and sign in with your onboarded identity.

   ```text
   https://console.fedramp.akeyless.io
   ```

5. **Create your administrative access.** In the Console, create the Auth Methods and Roles for your administrators and assign least-privilege access. Remove or limit any broad bootstrap access that is no longer needed.

6. **Create machine identities.** Create Auth Methods for Gateways, applications, and automation, and note the Access ID of each. See [User and Identity Types](#user-and-identity-types).

7. **Deploy a Gateway and configure your tools.** Continue with [FedRAMP Gateway Deployment](https://docs.akeyless.io/docs/fedramp-gateway-deployment) and [FedRAMP CLI Configuration](https://docs.akeyless.io/docs/fedramp-cli-configuration).

From this point, the rest of the operations are the same as in the commercial environment.

## User and Identity Types

| Identity                                   | How it authenticates                                                        | Notes                                                                                          |
| ------------------------------------------ | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Console users (non-privileged)             | Hosted-provider IdP, then the Console                                       | Read and write secrets according to their roles                                                |
| Administrators and operators               | Hosted-provider IdP, then the Console                                       | Multi-factor authentication is required                                                        |
| Gateways, applications, CI/CD, and scripts | Directly to Akeyless, with an Auth Method (for example, API Key or AWS IAM) | Do not use the hosted-provider IdP. Authenticate against the FedRAMP endpoints only            |
| Certificate-based clients                  | Mutual TLS to the dedicated certificate authentication endpoint             | See [FedRAMP Network Connectivity](https://docs.akeyless.io/docs/fedramp-network-connectivity) |

<Callout icon="📘" theme="info">
  ### Note

  PIV or CAC cards are not required to access the FedRAMP environment. Multi-factor authentication is enforced at your IdP.
</Callout>

## Sessions and Tokens

Akeyless issues a signed token (JWT) after a successful authentication. The default token lifetime is 60 minutes, and the maximum lifetime is 24 hours. Revoked tokens are rejected on every request.

## Keep Commercial and FedRAMP Accounts Separate

Use a separate account in each environment. The two are not mixed.

- An **Access ID**, **API key**, and **Gateway** created in one environment are not valid in the other.
- A user who needs both environments is onboarded separately in each.
- Keep separate CLI profiles per environment. See [FedRAMP CLI Configuration](https://docs.akeyless.io/docs/fedramp-cli-configuration).

## Offboarding Users

1. Remove the user from your IdP (or from the hosted-provider IdP, if you manage users there), so that the user can no longer reach the Console.
2. In the Console, remove the user's Auth Method and Role associations.
3. Rotate any API keys or credentials the user had access to.

## Troubleshooting

| Symptom                                                 | Likely cause                                                                                       | Action                                                                                                 |
| ------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| The Console URL does not load                           | Outbound HTTPS to `*.fedramp.akeyless.io` is blocked, or you are using a commercial URL            | Check your allow list and use `console.fedramp.akeyless.io`                                            |
| You can sign in to the IdP but cannot see your account  | The user was not assigned to the account                                                           | Ask your account administrator or Akeyless Customer Success to assign the user                         |
| `Access ID` rejected by the CLI, SDK, or Gateway        | The credentials belong to the other environment, or the tool still targets the commercial endpoint | Verify the Access ID is from the FedRAMP account, and the API URL is `https://api.fedramp.akeyless.io` |
| Authentication succeeds but the token is rejected later | The token expired or was revoked                                                                   | Re-authenticate                                                                                        |
