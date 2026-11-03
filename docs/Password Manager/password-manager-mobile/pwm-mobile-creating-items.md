---
title: Creating Items and Generating Passwords
---
## Creating an item

1. Open **Personal** or **Corporate**. To create inside a folder, open that folder first.
2. Tap **+** in the header.
3. Choose what to create:

![The create menu](https://files.readme.io/3e53e2d964f8aa7676665e6d872595f7f9627c3681c0d7205a1ff8ade18d3bc5-new-item-menu.png)
*The create menu*

| Option | Creates | Details |
|---|---|---|
| **New Folder** | A folder | Name, location, description, delete protection, tags |
| **New Secret Item** | A secret — free text, key/value pairs or JSON | [Creating New Secret](https://docs.akeyless.io/docs/creating-new-secret) |
| **New Password Item** | A login: username, password, websites and an optional one-time password | [Creating New Password](https://docs.akeyless.io/docs/creating-new-password-1) |
| **New File Item** | A file uploaded from your phone | [Creating New File Item](https://docs.akeyless.io/docs/web-extension-file-items) |

4. Fill in the form and tap **Save** at the top right. Tap **✕** to close without saving.

Saving into a corporate folder needs create permission there; if your access role does not
allow it, Akeyless rejects the save.

## Creating a password item

![The New Password form](https://files.readme.io/628ec82b465735ef883a7a86efe02dc9c5b4784b1e0b9139cc16885d19c604bd-new-password.png)
*The New Password form*

| Field | Notes |
|---|---|
| **Password Item** | The item's name, as it appears in the list. Required |
| **Username** | Required |
| **Website URLs** | The sites this login is for. Tap **Add URL** for more than one. **AutoFill uses these to decide which logins to offer**, so add the address of the sign-in page |
| **Location** | **Personal** or **Corporate**, then the folder. Tap **Select** to pick a folder |
| **Description** | Optional |
| **Password** | Type one, or generate one — see below |
| **Authenticator (OTP)** | Optional. Add a one-time password by scanning a QR code — see [One-Time Passwords: Scanning a QR Code](https://docs.akeyless.io/docs/pwm-mobile-otp) |

<Callout icon="💡" theme="default">
  **Logins for Android apps.** To fill a login inside an Android app rather than a website,
  add a website URL of the form `androidapp://` followed by the app's package name — for
  example `androidapp://com.example.app`. See
  [AutoFill on iPhone and Android](https://docs.akeyless.io/docs/pwm-mobile-autofill).
</Callout>

## Generating a password

In the **Password** section:

1. Choose **Random** for a string of characters, or **Passphrase** for a set of words.
2. Tap the **refresh** icon beside the password field to generate one. Tap it again for a new
   one.
3. Tap the **eye** icon to see what was generated.

The strength meter rates whatever is in the field, whether you generated it or typed it, and
the generation settings let you set the length, the character types and exactly which symbols
are allowed — useful for sites with strict password rules.

The check against known leaked passwords runs **on your phone**. Your password is never sent
anywhere to be checked.

See [Password Generator & Strength](https://docs.akeyless.io/docs/web-extension-password-generator)
for every setting and how strength is scored.

## Editing an item

Swipe the item left, tap **More**, then **Edit**. The edit form is the same as the create
form. See [Editing, Copying & Moving Items](https://docs.akeyless.io/docs/editing-password-details-1).

Your organization can set a password policy that new passwords must meet — see
[Setting Password Policy On Account Level](https://docs.akeyless.io/docs/setting-password-policy-on-account-level-1).

## Importing

Importing from another password manager is not available in the mobile app. Use the
[web extension](https://docs.akeyless.io/docs/csv-password-importer) or the
[web console](https://docs.akeyless.io/docs/pwm-console-import) — imported items appear on
your phone the next time the list refreshes.

## Related

- [Viewing, Copying and Managing Items](https://docs.akeyless.io/docs/pwm-mobile-items)
- [Item Types Reference](https://docs.akeyless.io/docs/web-extension-item-types)
