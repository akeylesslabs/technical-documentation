---
title: Prompt to Save Password
---
## Saving a new credential

With `Prompt to save password` enabled in Settings, signing in to a site with credentials that are not in your vault opens the extension and offers to save them.

Accept, and you choose the name, folder and any other details before saving — the same overlay used to create a password item, pre-filled from the form you just submitted.

Decline, and nothing is stored.

## Updating an existing credential

When you change your password on a site, the extension detects the password-change form and offers to **update the existing vault item** rather than create a second one.

This keeps one item per credential, which matters for Security Health — duplicate items for the same login inflate the reuse metric.

## What is observed

Form submissions are observed only to detect these two cases. Guards prevent prompting on forms that are not sign-in or password-change forms, such as search boxes and newsletter signups.

## Turning it off

**Settings → Prompt to save password**. On by default.

## Related

- [Using Autofill / Password Injection](https://docs.akeyless.io/docs/using-autofillpassword-injection-functionality-1)
- [Extension Settings](https://docs.akeyless.io/docs/web-extension-settings)
- [Creating New Password](https://docs.akeyless.io/docs/creating-new-password-1)
