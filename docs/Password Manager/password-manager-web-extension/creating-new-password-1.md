---
title: Creating New Password
---
Select the blue **+** in the header and choose what to create.

![The create menu](https://files.readme.io/71524d6baca1ca29089f21534f798294c773d64b6f1d3b81bd151f2268989dc6-create-menu-corporate.png)
*The create menu. Corporate offers three types; Personal adds **New File Item***

---

## New Password Item

![The New Password overlay](https://files.readme.io/657113041fe938f989c79f20af69484e95deda9fd211b06c287e03d0bf54f039-new-password-overlay.png)
*General, Location and the Personal / Corporate switch*


**General** — item name, username, and one or more **Website URLs** (`https://www.example.com`).
Select **Add URL** for additional addresses. These URLs drive autofill matching and the
[Launch](https://docs.akeyless.io/docs/web-extension-launch) button.

**Location** — switch between **Personal** and **Corporate**, then pick the destination folder
with **Select**. Optionally set a **Description** and `Maximum Versions` (default **100**).

**Password** — type one or generate it. See [Password Generator & Strength](https://docs.akeyless.io/docs/web-extension-password-generator).

`Metadata` — `Protection Key` (fixed if your account enforces an exclusive default key),
**Tags**, and `Delete protection`.

**Custom Fields** — select **Add Field** for each Key/Value pair.

**Authenticator (OTP)** — paste a Base32 secret, or use **Scan otpauth QR from the current
website tab** to read a QR code from the page you have open. Give it a label such as *GitHub*.

---

## New Secret Item

![The New Secret overlay](https://files.readme.io/cfbbfbe5bfcb6053707eba0ee75ae77e41909e70a22e0d64036a43a4c6f4b123-new-secret-overlay.png)
*Text, Key/value and JSON formats, with a secret Type and Maximum Versions*


A static secret with a free-form value, plus the same Location, Metadata, description and
Maximum Versions controls. Values may be plain text or structured key/value.

## New File Item

Uploads a file into the vault. Files count against your account's **File storage** quota,
shown in [Extension Settings](https://docs.akeyless.io/docs/web-extension-settings).

## New Folder

![The New Folder overlay](https://files.readme.io/14a60ae4d1032eaf4029b9d9287303c52fe334be0d3483268682c8a2a02a9088-new-folder-overlay.png)
*Location, description, delete protection and tags*


Creates a folder at the location you choose, in Personal or Corporate.

## Related

- [Password Generator & Strength](https://docs.akeyless.io/docs/web-extension-password-generator)
- [Creating New Secret](https://docs.akeyless.io/docs/creating-new-secret)
- [Adding and Using One-Time Passwords](https://docs.akeyless.io/docs/adding-and-using-otp-1)
