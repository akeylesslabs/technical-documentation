---
title: AutoFill on iPhone and Android
---
Once Akeyless is turned on as an AutoFill provider, your phone offers your saved Akeyless
logins whenever you tap a username or password field — in Safari, Chrome and other browsers,
and in other apps. One tap fills both the username and the password.

## What AutoFill fills

| Fills | Does not fill |
|---|---|
| Username and password from **password items** in Personal and Corporate | Secrets, files and certificates |
| | One-time codes — copy them from the app, see [One-Time Passwords](https://docs.akeyless.io/docs/pwm-mobile-otp) |
| | Passkeys |

AutoFill does not offer to save a new login you type into another app. Create the item in
Akeyless first, with the site's address under **Website URLs**.

---

## iPhone

### Turn it on

1. Sign in to the Akeyless app at least once, so your logins are available.
2. Open the iPhone **Settings** app.
3. Go to **General** → **AutoFill & Passwords** (iOS 18 and later).
   - On iOS 17: **Settings** → **Passwords** → **Password Options**.
   - On iOS 15 and 16: **Settings** → **Passwords** → **AutoFill Passwords**.
4. Turn on **Akeyless**.

### Fill a login

1. In Safari or another app, tap the username or password field.
2. Matching Akeyless logins appear above the keyboard, showing the username and the site.
   Tap one to fill.
3. Depending on your iPhone's settings, iOS may ask for Face ID, Touch ID or your passcode
   before it fills. Akeyless adds no extra prompt of its own.

### Choose from the full list

If the login you want is not suggested, tap the **key** icon or **Passwords** above the
keyboard and choose **Akeyless**. A list opens:

- It starts with the logins that match the site you are on.
- Use **Search** to find any login by name, username or website.
- Tap **Fill** on a row to fill it.

| Message | Meaning |
|---|---|
| **Sign in to Akeyless to fill logins for this site.** | Open the Akeyless app and sign in |
| **No logins for this site. Search to fill from any login.** | Nothing matches this site. Search instead |
| **Couldn't fill** | The password could not be retrieved. Open the app, check you are signed in, and try again |

### How iPhone matches sites

A login is suggested when the site you are on and one of the item's **Website URLs** share
the same host, or one is a subdomain of the other. `www.` is ignored. So an item saved with
`example.com` is offered on `login.example.com`, and the other way round.

---

## Android

AutoFill needs **Android 8.0 or later**.

### Turn it on

1. Sign in to the Akeyless app at least once, so your logins are available.
2. Open your phone's **Settings** and find the **Autofill service** setting. Its location
   varies by manufacturer and Android version — common paths are:
   - **Settings** → **Passwords & accounts** → **Autofill service**
   - **Settings** → **System** → **Languages & input** → **Autofill service**

   If you cannot find it, search Settings for *autofill*.
3. Choose **Akeyless**, and confirm that you trust the app.

### Chrome: one more step

Chrome uses its own password manager unless you tell it otherwise:

1. Open Chrome → **⋮** → **Settings** → **Autofill services**.
2. Select **Autofill using another service**.
3. Restart Chrome if asked.

Akeyless also fills in **Edge**, **Brave**, **Samsung Internet**, **Opera** and
**DuckDuckGo**.

### Fill a login

1. Tap the username or password field.
2. A dropdown lists the matching Akeyless logins, each with its name and username.
3. Tap one to fill the username and password.

If nothing matches, no Akeyless suggestion appears. Open the Akeyless app and copy the
password instead, or add the site's address to the item.

### How Android matches sites and apps

| You are in | An item matches when |
|---|---|
| **A website** | The page's host is the same as a saved website's host, or a subdomain of it. `www.` is ignored |
| **An app** | The item has a website URL of exactly `androidapp://<package name>` |

Matching on Android works in one direction: an item saved with `example.com` is offered on
`login.example.com`, but an item saved with `login.example.com` is **not** offered on
`example.com`. Save the shortest address the site uses.

<Callout icon="💡" theme="default">
  **Finding an app's package name.** It is in the app's Google Play address, after `id=`. For
  `play.google.com/store/apps/details?id=com.example.app`, add the website URL
  `androidapp://com.example.app` to the item.
</Callout>

---

## Keeping AutoFill up to date

AutoFill works from a copy of your logins kept encrypted on the phone. The app refreshes that
copy whenever it loads your vault, so:

- **After adding or changing a login elsewhere** — in the web extension or the console —
  open the Akeyless app once, or pull down to refresh, before you expect AutoFill to offer it.
- **After signing out**, every login is removed from the phone's AutoFill straight away. Sign
  in again to bring them back.

On iPhone, the full list can also look up a site's logins directly in Akeyless, so a login
added elsewhere may appear there before the app has refreshed.

<Callout icon="🔒" theme="default">
  **How your logins are protected.** On iPhone, the copy is kept in the iOS Keychain, readable
  only while the phone is unlocked, and never synced to other devices. On Android, it is
  encrypted with a key held in the Android Keystore, and the app is excluded from phone
  backups.
</Callout>

## Related

- [Creating Items and Generating Passwords](https://docs.akeyless.io/docs/pwm-mobile-creating-items)
- [Security and Privacy](https://docs.akeyless.io/docs/pwm-mobile-security)
- [Troubleshooting](https://docs.akeyless.io/docs/pwm-mobile-troubleshooting)
