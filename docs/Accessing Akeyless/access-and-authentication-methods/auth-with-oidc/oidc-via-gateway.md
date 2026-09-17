---
title: OIDC via Gateway
deprecated: false
hidden: false
metadata:
  robots: index
---
## Authentication via Gateway

By default, OIDC authentication is handled by the Akeyless SaaS authentication service: the
browser and the Identity Provider (IdP) complete the authorization code flow against
`https://auth.akeyless.io`, and the Akeyless Gateway is not part of the login flow.

**Authentication via Gateway** moves that flow to your own
[Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview). When it is enabled on an OIDC
Authentication Method, the IdP and the client communicate with the Gateway instead of the SaaS
authentication service, and the Gateway completes the callback and issues the Akeyless token.

Use this option when the login flow must stay inside your network — for example when the IdP is
not reachable from the internet, when corporate policy forbids redirecting users to a SaaS
callback endpoint, or in air-gapped and offline-oriented deployments where the SaaS authentication
service is not reachable from the client.

<Callout icon="⚠️" theme="warn">
  ### **Warning:**

  When Authentication via Gateway is enabled, this authentication method **cannot** be used from
  the Akeyless SaaS Console (`https://console.akeyless.io`). Create, configure, and use the method from the Gateway
  Configuration Manager UI or the CLI instead.
</Callout>

### Prerequisites

- An Akeyless Gateway reachable from the client over **HTTPS** at its
  Configuration Manager address (default port `8000`), referred to below as `https://<Your-Akeyless-GW-URL>:8000`.
  See [TLS Settings](https://docs.akeyless.io/docs/gateway-tls-settings) for enabling HTTPS on the
  Gateway.
- **Admin** permission on the target Gateway. Enabling or changing the Gateway binding on an<br />Authentication Method modifies the Gateway configuration, so it requires the Admin capability in<br />the Gateway's access permissions. See<br />[Gateway Access Permissions Reference](https://docs.akeyless.io/docs/gateway-access-permissions-reference)<br />and [Authentication and Access](https://docs.akeyless.io/docs/gateway-authentication-and-access).
- The Gateway's own Authentication Method has **read** permission on the OIDC<br />Authentication Method being configured, so the Gateway can retrieve its configuration to<br />validate sign-ins on its behalf. See [Access Roles](https://docs.akeyless.io/docs/rbac) for<br />permission setup.
- Administrative access to the IdP application, so its redirect URI can be repointed to the
  Gateway.

### Enable Authentication via Gateway

1. Open the Gateway Configuration Manager UI at `https://<Your-Akeyless-GW-URL>:8000`.
2. Navigate to the OIDC Authentication Method (or create a new one).
3. Enable the **Enable Gateway Authentication** option.
4. Select the Gateway cluster that should own the authentication flow.
5. Save.

### Configure the IdP

Point the IdP application at the Gateway instead of the Akeyless SaaS callback. Replace
`https://<Your-Akeyless-GW-URL>:8000` with your Gateway Configuration Manager URL.

| IdP field                                      | Value                                                   |
| ---------------------------------------------- | ------------------------------------------------------- |
| Redirect URI / Callback URL / Sign-in redirect | `https://<Your-Akeyless-GW-URL>:8000/api/oidc-callback` |

<Callout icon="⚠️" theme="warn">
  ### **Warning:**

  Do not use `https://auth.akeyless.io/oidc/callback` with a Gateway-bound Authentication Method.
  The SaaS callback is not part of this flow.
</Callout>

### Configure Allowed Redirect URIs

**Allowed Redirect URIs** (`--allowed-redirect-uri` in the CLI) controls where the client is sent
_after_ a successful IdP login. This is separate from the IdP callback URL configured above, and
the Gateway addresses used by your clients must appear in this list.

### Sign in with the CLI

The CLI must be told explicitly to authenticate through the Gateway. Pass `--gateway-url` with the
Gateway Configuration Manager URL:

```shell
akeyless auth \
  --access-type oidc \
  --access-id <OIDC Access ID> \
  --gateway-url https://<Your-Akeyless-GW-URL>:8000
```

### Troubleshooting

| Symptom                                      | Cause and resolution                                                                                                                                                                      |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gateway-auth-required`                      | The flow reached the SaaS authentication service. Add `--gateway-url https://<Your-Akeyless-GW-URL>:8000` to the CLI command or to the profile, and do not sign in from the SaaS Console. |
| `redirect url after callback is not allowed` | The client's return URL is missing from **Allowed Redirect URIs**. Add it (for example `http://127.0.0.1:*` for the CLI).                                                                 |
| IdP error on redirect URI mismatch           | The IdP is still configured with `https://auth.akeyless.io/oidc/callback`. Repoint it to `https://<Your-Akeyless-GW-URL>:8000/api/oidc-callback`.                                         |
| Permission denied when saving the binding    | The user lacks **Admin** permission on the target Gateway. See [Gateway Access Permissions Reference](https://docs.akeyless.io/docs/gateway-access-permissions-reference).                |
| Browser TLS error during login               | The Gateway is not served over HTTPS at `https://<Your-Akeyless-GW-URL>:8000`. See [TLS Settings](https://docs.akeyless.io/docs/gateway-tls-settings).                                    |
