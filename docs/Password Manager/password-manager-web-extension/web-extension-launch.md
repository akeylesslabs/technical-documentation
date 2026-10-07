---
title: 'Launch: Open a Site Already Signed In'
---
***Launch*** is more than autofill. It opens the target site, fills the login form, and submits it — so you arrive already signed in.

## Using it

Any item with a **Website URL** shows a **Launch Website** control on its row and in the suggestion popup. Select it.

The extension then:

1. Fetches the credential from the vault.
2. Opens the target URL in a new tab.
3. Fills the login form.
4. Clicks the submit control.

An overlay shows progress, and the flow can be cancelled while it runs.

## Dynamic and rotated secrets

Launch resolves the producer payload before filling, so dynamic and rotated secrets work the same as stored passwords. The extension maps the producer output to the right fields for the target — database users, AWS console sign-in, Azure, Google Workspace and others each have their own mapping.

<Callout icon="ℹ️" theme="info">
  For AWS specifically, the **console** user and password are used for `signin.aws.amazon.com`, not the programmatic access key ID.
</Callout>

## Multi-step logins

Many sites ask for the username on one screen and the password on the next. Launch carries the remaining steps across page transitions, scores the candidate submit buttons on each screen, and traverses Shadow DOM to reach fields inside web components.

## Restrictions

Launch runs only on allowed domains, and specific sites have tailored handling. If Launch opens the site but does not sign in:

- confirm the item has **both** a username and a password
- confirm the URL points at the actual login page, not a landing page
- allow the page to finish loading between steps

## Related

- [Using Autofill / Password Injection](https://docs.akeyless.io/docs/using-autofillpassword-injection-functionality-1)
- [Item Types Reference](https://docs.akeyless.io/docs/web-extension-item-types)
- [Troubleshooting](https://docs.akeyless.io/docs/web-extension-troubleshooting)
