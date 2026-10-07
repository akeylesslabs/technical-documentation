---
title: SA Web Extension (Secrets Automation)
---
**Akeyless SA 2.0** is a separate extension built from the same codebase as Akeyless Password
Manager 2.0. It keeps every vault feature and adds Secure Remote Access: proxy-routed sessions,
Zero Trust Portal launch, and an audit trail of every connection.

<Callout icon="⚠️" theme="warn">
  This is a **different extension** from Akeyless Password Manager 2.0, with its own store
  listings. Install the one your organization uses — not both. Running both means two
  extensions competing to fill the same login forms.
</Callout>

## Download

| Browser | Install |
|---|---|
| **Google Chrome** | [Akeyless SA 2.0](https://chromewebstore.google.com/detail/akeyless-sa-20/cdghndnnjccefelakphihcjngdokccpm) |
| **Microsoft Edge** | [Akeyless SA 2.0](https://microsoftedge.microsoft.com/addons/detail/akeyless-sa-20/eplnolemlmkfhbmmafdnncdnapoijkgo) |
| **Mozilla Firefox** | [Akeyless SA 2.0](https://addons.mozilla.org/en-US/firefox/addon/akeyless-sa-2-0/) |
| **Safari** | Not published |

---

## What Secure Remote Access adds

### Zero Trust Portal (ZTP) launch

Opens a target application **through the Akeyless proxy** rather than directly. The browser
never holds a route to the target, and the credential is never typed by a human.

A ZTP launch runs in sequence:

1. The extension receives a launch request carrying the target URL and the vault item.
2. It authenticates to the gateway and exchanges the session for a short-lived token.
3. It resolves the credential from the vault, including dynamic and rotated secret producers.
4. It opens the target — in a private or incognito window when configured — with proxy routing
   applied to that window only.
5. It fills the credential on arrival and submits.

Because routing is scoped to the launched window, your normal browsing is unaffected.

### Credential mapping

The producer payload rarely matches the target's login form field for field, so the extension
maps it:

| Producer type | Mapped to |
|---|---|
| **Database dynamic secrets** | Generated username and password |
| **AWS** | The **console** user and password for `signin.aws.amazon.com` — not the programmatic access key ID |
| **Azure** | The nested user object |
| **Google Workspace** | The producer's own identity fields |
| **Rotated secrets** | The current rotation's value |

### SRA clipboard

Clipboard support for remote-access sessions, driven by a server-sent-event channel from the
SRA worker, so copy and paste work inside a proxied session without weakening its isolation.

### Flow audit log

Every launch is recorded as a structured trail — inject, authentication, secret resolution,
fill — with timings. Use it to answer *where did this connection stall* without reproducing
the problem.

The log can be copied for support, and diagnostics can be uploaded directly.

### Verbose logging

On by default in SA builds. Structured console output covering the whole launch pipeline.
Silence it by setting `enableZtpVerboseLogs` to `false` in the extension's feature flags.

### Launch guard

While a ZTP launch is in flight, the tab is marked for up to 45 seconds so background probes
cannot race the proxy's navigation and autofill. This is what stops a half-filled form from
being submitted mid-launch.

---

## Additional permissions

SA builds request more than the Password Manager build, because they route traffic rather than
just reading pages:

| Permission | Why |
|---|---|
| `proxy` | Routes the launched window through the Akeyless proxy |
| `webRequest`, `webRequestAuthProvider` | Answers authentication challenges on proxied requests |
| `webNavigation` | Tracks multi-step logins across redirects |
| `clipboardRead` | SRA clipboard support |
| `management` | Detects conflicting extensions |
| `<all_urls>`, `http://*/*` | Targets may be internal hosts on any scheme or port |

The Password Manager build requests none of these.

---

## Everything else is the same

Vault browsing, item creation, autofill, Launch, sharing, import, passkeys, Security Health
and settings behave identically. See
[Password Manager Web Extension](https://docs.akeyless.io/docs/password-manager-web-extension).

Sign-in is the same too, including the remembered method and Access ID — see
[Signing In to the Web Extension](https://docs.akeyless.io/docs/web-extension-sign-in).

## Related

- [Installation & Supported Browsers](https://docs.akeyless.io/docs/installation-of-akeyless-web-extension)
- [Launch: Open a Site Already Signed In](https://docs.akeyless.io/docs/web-extension-launch)
- [Troubleshooting](https://docs.akeyless.io/docs/web-extension-troubleshooting)
