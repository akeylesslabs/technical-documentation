---
title: Setting Password Policy On Account Level
---
Password policy is configured once at the account level, in the Akeyless console, and the extension applies it everywhere a password is entered or generated.

## What the policy controls

- Minimum length
- Required character classes — uppercase, lowercase, digits, symbols
- Any additional constraints your account defines

## Where the extension applies it

| Surface | Behavior |
|---|---|
| **Create / edit password overlay** | The strength meter reports against the policy; a password that fails cannot be saved |
| **Password generator** | Generates only passwords that satisfy the policy |
| **Passphrase mode** | Generates passphrases that satisfy the policy, rather than re-rolling until one passes |
| **In-page suggestion popup** | Generated passwords on signup and password-change forms follow the policy |

## Related account settings

Two other account settings shape the create and edit overlays:

| Setting | Effect |
|---|---|
| **Default maximum versions** | Pre-fills **Maximum Versions**, and sets the allowed range |
| **Default protection key** | Preselects the protection key; when configured as exclusive, the picker is locked |
| **Protect items by default** | New items are created with delete protection on |

See [Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies) for the full list.

## Related

- [Password Generator & Strength](https://docs.akeyless.io/docs/web-extension-password-generator)
- [Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies)
