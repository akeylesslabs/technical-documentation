---
title: Creating New Password
---
Select the blue **+** in the header and choose what to create.

![The create menu](https://files.readme.io/242d134a5a7a258504621882f82a5748e5deda13d3e74ee23eb7f408fd3e2dd9-create-item-menu.png)
*New Folder, New Secret Item, New Password Item, New File Item*

---

## New Password Item

**General** — item name, username, and one or more **Website URLs** (`https://www.example.com`).
Select **Add URL** for additional addresses. These URLs drive autofill matching and the
[Launch](https://docs.akeyless.io/docs/web-extension-launch) button.

**Location** — choose the destination folder using the searchable folder browser. Optionally
set a **Description** and **Maximum Versions**.

**Password** — type one or generate it. See [Password Generator & Strength](https://docs.akeyless.io/docs/web-extension-password-generator).

**MetaData** — **Protection Key** (fixed if your account enforces an exclusive default key),
**Tags**, and **Delete protection**.

**Custom Fields** — select **Add Field** for each Key/Value pair.

**Authenticator (OTP)** — paste a Base32 secret, or use **Scan otpauth QR from the current
website tab** to read a QR code from the page you have open. Give it a label such as *GitHub*.

---

## New Secret Item

A static secret with a free-form value, plus the same Location, MetaData, description and
Maximum Versions controls. Values may be plain text or structured key/value.

## New File Item

Uploads a file into the vault. Files count against your account's **File storage** quota,
shown in [Extension Settings](https://docs.akeyless.io/docs/web-extension-settings).

## New Folder

Creates a folder at the location you choose, in Personal or Corporate.

## Related

- [Password Generator & Strength](https://docs.akeyless.io/docs/web-extension-password-generator)
- [Creating New Secret](https://docs.akeyless.io/docs/creating-new-secret)
- [Adding and Using One-Time Passwords](https://docs.akeyless.io/docs/adding-and-using-otp-1)
