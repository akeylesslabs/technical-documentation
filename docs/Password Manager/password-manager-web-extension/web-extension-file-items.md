---
title: Creating New File Item
---
File items store a file inside the Akeyless vault — certificates, keystores, private keys,
service-account `.json` files, configuration bundles. Anything you would otherwise email to a colleague
or leave in a shared drive.

## Creating one

1. Select the blue **+** in the header.
2. Choose **New File Item**.
3. Give the item a **Name**.
4. Select the file to upload.
5. Choose the **Location** folder — Personal or Corporate, using the folder browser.
6. Optionally set a **Description**, `Protection Key`, **Tags** and `Delete protection`.
7. Select **Save**.

## Storage quota

File items consume your account's file storage quota, shared across the account rather than
allocated per user.

Check it in **Settings → File storage**, which shows:

| Reading | Meaning |
|---|---|
| *N used* | How much of the quota is consumed |
| *N remaining* | What is left |
| Progress bar | The same figure visually |
| *N / N account quota* | Used against total |

<Callout icon="⚠️" theme="warn">
  If an upload fails, check the quota before retrying. A full account quota is the most common
  cause, and retrying the same upload will not clear it.
</Callout>

## Downloading

Open the item and use the download control in the item preview. The file is fetched from the
vault at that moment rather than being cached in the browser.

## Protection and encryption

File items support the same protections as other item types:

| Control | Effect |
|---|---|
| `Protection Key` | The DFC key that encrypts the file |
| **Zero Knowledge Encryption** | Shown on items wrapped with a customer fragment |
| `Delete protection` | Prevents deletion until cleared |

## Sharing a file

Files are shared the same way as other items, by time-limited link — see
[Sharing Password / Secret](https://docs.akeyless.io/docs/sharing-password-1).

## When the option is missing

<Callout icon="ℹ️" theme="info">
  **New File Item** appears only when password management is enabled on your account. If it is
  absent from the create menu, see
  [Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies).
</Callout>

## Related

- [Item Types Reference](https://docs.akeyless.io/docs/web-extension-item-types)
- [Extension Settings](https://docs.akeyless.io/docs/web-extension-settings)
- [Viewing an Item](https://docs.akeyless.io/docs/web-extension-viewing-items)
