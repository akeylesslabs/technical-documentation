---
title: Signing In Through the Browser Extension
---
When the Akeyless browser extension is installed and your organization uses a preconfigured
install, the console can sign you in without you entering an authentication method or an
Access ID. The console asks the extension what your organization is configured for, and uses
that.

<Callout icon="ℹ️" theme="info">
  **This is one-click sign-in, not silent sign-in.** The console never signs you in on its own
  — you still select **Sign In**. What it removes is having to know and type your
  organization's authentication method, Access ID and region.
</Callout>

---

## What you see

On the sign-in screen, the console looks for the extension in the background.

| Situation | The sign-in screen shows |
|---|---|
| Extension installed **and** org preconfigured | Your organization's message and a single **Sign In** button — no method picker, no Access ID field |
| Extension installed, no org preconfiguration | The normal sign-in screen with every method |
| Extension not installed or not reachable | The normal sign-in screen |

The collapsed, sign-in-only screen matches what the extension itself shows for a preconfigured
install, so the two feel like one product.

---

## What the extension supplies

Two distinct things, which is why this works even when you have never signed in to the console
before:

| Supplied | What it is | Used for |
|---|---|---|
| **Preconfigured sign-in details** | Your organization's authentication method, Access ID and region — **not credentials** | Pre-filling the sign-in so you do not have to know them |
| **A live session** | The session from the extension, when you are already signed in there | Carrying you straight into the console with no identity-provider round trip |

When the extension already holds a session, selecting **Sign In** can drop you straight into
the console. Otherwise the console starts the normal flow for your organization's method —
SAML or OIDC opens your identity provider, Google or GitHub opens OAuth — with the identifiers
already filled in.

---

## Requirements

All of these must hold:

| Requirement | Notes |
|---|---|
| The extension is **installed and enabled** | See [Downloads](https://docs.akeyless.io/docs/pwm-console-downloads) |
| Your install is **preconfigured** by your organization | Via a preconfigured link or a managed package — [Preconfigured Installs](https://docs.akeyless.io/docs/web-extension-preconfigured-install) |
| The console is on an **approved origin** | The extension answers only the official `console-pwm.*` consoles and local development hosts |

<Callout icon="⚠️" theme="warn">
  The extension will not hand a session to an arbitrary website. The set of origins it responds
  to is fixed in the extension itself and cannot be extended from a web page — which is what
  stops a lookalike site asking for your session.
</Callout>

---

## How the probe behaves

The console asks the extension about its state when the sign-in screen loads, and waits up to
**6 seconds**. While it waits, the sign-in screen holds off rather than flashing the wrong UI.

If your extension is an older build without the availability API, the console falls back to
asking for the preconfigured details and the session directly, so older installs still work.

If the probe finds nothing, you get the normal sign-in screen — nothing is blocked.

---

## Signing out

**Sign out** ends the console session and returns you to the sign-in screen. It does not sign
you out of the extension.

To sign in again, select **Sign In**. To sign in as somebody else, sign out of the extension
first — otherwise the console continues to offer the configuration the extension holds.

---

## Launch uses the same bridge

The same connection powers **Launch**. Selecting the launch button on an item in the console
hands the credential to the extension, which opens the site and fills the login form.

[Settings](https://docs.akeyless.io/docs/pwm-console-settings) shows whether the console can see the extension, and which
version is installed.

---

## Troubleshooting

| Symptom | Cause |
|---|---|
| Full sign-in screen when you expected one button | The extension is not installed, not enabled, or your install is not preconfigured |
| *Could not read preconfigured sign-in from the extension* | The extension is installed but did not answer. Reload the extension, then reload the console |
| *Extension sign-in failed* | The flow started but did not complete — usually the identity-provider popup was blocked. Allow popups for the console and retry |
| Sign-in-only screen but you need a different account | Sign out of the extension; the console follows whatever it holds |
| Works in one browser, not another | The extension is per-browser. Install it in the browser you are using |

## Related

- [Settings](https://docs.akeyless.io/docs/pwm-console-settings)
- [Downloads: Extension and Desktop App](https://docs.akeyless.io/docs/pwm-console-downloads)
- [Password Manager Web Extension](https://docs.akeyless.io/docs/password-manager-web-extension)
