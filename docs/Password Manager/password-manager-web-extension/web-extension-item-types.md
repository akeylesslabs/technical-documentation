---
title: Item Types Reference
---
| Type | Icon | What it holds |
|---|---|---|
| **Folder** | Folder outline | A container for other items |
| **Password item** | Padlock | Username, password, Website URLs, OTP, Custom Fields |
| **Secret item (static)** | Key | A free-form secret value, plain text or Key/value |
| **File item** | Document | A file stored in the vault; counts against your file quota |
| **Rotated secret** | Rotating arrows | A secret rotated by Akeyless; the value is read-only |
| **Dynamic secret** | Dynamic icon | Credentials generated on demand, with producer status and TTL |
| [Passkey](https://docs.akeyless.io/docs/passkey) | Person with key | A WebAuthn credential for a website |

## Badges

| Badge | Meaning |
|---|---|
| **Personal** / **Corporate** | Which vault the item lives in |
| **Lock** | Delete protection is on — the item cannot be deleted |
| **Zero Knowledge Encryption** | The item is wrapped with a customer fragment |

## Which types you can create

The create menu offers **Folder**, **Secret Item**, **Password Item** and **File Item**.

Rotated and dynamic secrets are created in the Akeyless console or CLI and appear in the extension read-only. Passkeys are created by websites through the browser — see [Passkey](https://docs.akeyless.io/docs/passkey).

## Related

- [Creating New Password](https://docs.akeyless.io/docs/creating-new-password-1)
- [Creating New Secret](https://docs.akeyless.io/docs/creating-new-secret)
- [Creating New File Item](https://docs.akeyless.io/docs/web-extension-file-items)
