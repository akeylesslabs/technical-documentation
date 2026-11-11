---
title: Self-Distribution with Microsoft Intune
---
<Callout icon="ℹ️" theme="info">
  **Audience: IT and endpoint administrators** who manage Chrome or Edge with Microsoft Intune.
</Callout>

From version **1.26.20**, the store version of the extension can be repackaged with your organization's sign-in settings inside it. You then push that package to managed devices with Intune. Users get the extension installed automatically, and it opens on a login screen that is already set up: the right sign-in method, the right Access ID, and no choices to make.

This page walks through the whole process: preparing the package, signing it, hosting it, and deploying it with Intune on Windows and macOS. If you don't use Intune, or users install the extension themselves, see [Option C](#option-c--public-store-with-a-preconfigured-link): users install from the regular public store through a preconfigured link that Akeyless creates for you.

## Before you start

| You need | Why |
|---|---|
| The extension installed from the official store on an admin machine | You copy it from there. Use only the official [Chrome](https://chromewebstore.google.com/detail/akeyless-password-manager/afmojeipcbpcfkdohnnjfkilfekoobmc) or [Edge](https://microsoftedge.microsoft.com/addons/detail/akeyless-password-manager/fppjjcloabbllcakfjefmkdpbaaikeog) listing, or a package supplied by Akeyless. Never repackage a copy from any other source. |
| Your **Access ID** and **authentication method** | These go into the configuration file. See [Preconfigured Installs: Overview](https://docs.akeyless.io/docs/web-extension-preconfigured-install) for every supported field. |
| Intune administrator rights | To create device configuration profiles. |
| **Managed devices** | Chrome and Edge only force-install an extension from outside their stores on devices that are joined to Microsoft Entra ID or Active Directory, or enrolled in MDM. Personal devices that are only *registered* will reject it. |
| An HTTPS location your devices can reach | For **Option B** only. Any web server or blob storage works, including an internal one. |

<Callout icon="⚠️" theme="warn">
  **Settings apply on first install only.** The configuration file is read once, when the extension is installed on a browser profile, and never overwrites existing settings. Plan your settings before the first rollout. To change them for a fleet that already has the extension, use a [Bridge Link](https://docs.akeyless.io/docs/web-extension-bridge-link).
</Callout>

## How it works

Every store build of the extension contains a file named `preconfigured_install.json`, switched off:

```json
{ "enabled": false }
```

When you switch it on and fill in your settings, the extension reads the file the first time it is installed and saves the settings to its login screen. Because you changed the package, it is no longer the store's copy. It becomes **your own private build**, with its own extension ID, which you distribute yourself.

| | Store extension | Your repackaged extension |
|---|---|---|
| Extension ID | Akeyless's store ID | A new ID, set by your signing key |
| Updates | Automatic from the store | You repackage each new release |
| Settings | User picks at sign-in | Preconfigured from your file |
| Distribution | Store | Intune, through Edge Add-ons or your own hosting |

## Choose a distribution option

| | **Option A — Intune + Edge Add-ons (hidden listing)** | **Option B — Intune + self-hosted package** *(recommended for managed fleets)* | **Option C — Public store + preconfigured link** |
|---|---|---|---|
| Browsers | Edge only | Chrome and Edge | Chrome, Edge and Firefox |
| How users get it | Installed automatically by Intune | Installed automatically by Intune | Users click a link and install from the regular store |
| Who builds it | You repackage it | You repackage and sign it | Nothing to build. Akeyless creates the link |
| Updates | You resubmit each release | You repackage each release | Automatic from the store |
| Needs MDM | Yes | Yes | No. Works on any device, including personal ones |
| Best for | Edge-only organizations without a web server | Most Intune deployments | Organizations without MDM, BYOD, pilots and contractors |

Options A and B share **Part 1**. Then follow **Part 2A** or **Part 2B**, and finish with **Part 3** and **Part 4**. For **Option C**, go straight to [Option C — Public store with a preconfigured link](#option-c--public-store-with-a-preconfigured-link).

---

## Part 1 — Prepare the package

### Step 1: Install the extension from the store

On an admin machine, install the extension in the browser you will deploy to, from the official listing. For Edge deployments, copy from Edge; for Chrome deployments, copy from Chrome.

### Step 2: Find the extension folder

1. Open `chrome://version` (or `edge://version`).
2. Copy the **Profile Path**.
3. In your file explorer, open that path, then open the `Extensions` folder inside it.

The usual locations are:

| Browser | Windows | macOS |
|---|---|---|
| Chrome | `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions` | `~/Library/Application Support/Google/Chrome/Default/Extensions` |
| Edge | `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Extensions` | `~/Library/Application Support/Microsoft Edge/Default/Extensions` |

4. Open the folder named after the extension ID:
   - Chrome: `afmojeipcbpcfkdohnnjfkilfekoobmc`
   - Edge: `fppjjcloabbllcakfjefmkdpbaaikeog`
5. Inside it is one folder per installed version, for example `1.30.158_0`.

### Step 3: Copy the version folder

Copy the version folder to a working location, for example `C:\akeyless\akeyless-extension`. Work only on the copy, never on the installed folder.

### Step 4: Delete the `_metadata` folder

The copy contains a folder named `_metadata`, which holds the store's signature hashes. **Delete it.** Browsers refuse to load or package a folder that contains it.

### Step 5: Remove the store update address

Open `manifest.json` in a text editor and delete the `update_url` line. It points to the store, which does not know about your private build.

```json
"update_url": "https://clients2.google.com/service/update2/crx",
```

Make sure the file is still valid JSON afterwards, with no trailing comma left on the line above. In Option B you will add your own `update_url` back in [Step 9](#step-9-point-the-package-at-your-update-file).

### Step 6: Edit `preconfigured_install.json`

Open `preconfigured_install.json` at the root of the folder and replace its contents with your settings. The simplest configuration, a single sign-in method with no picker, looks like this:

```json
{
  "enabled": true,
  "prefillAccessId": "p-xxxxxxxxxxxx",
  "preferredAuthMethod": "oidc",
  "allowedAuthMethods": ["oidc"],
  "installationSource": "bundled_prefill"
}
```

A fuller example, with branding and your own wording on the login screen:

```json
{
  "enabled": true,
  "prefillAccessId": "p-xxxxxxxxxxxx",
  "preferredAuthMethod": "saml",
  "allowedAuthMethods": ["saml"],
  "environment": "global",
  "config_id": "your-branding-id",
  "contact_support_url": "https://support.example.com",
  "open_web_console_url": "https://console-pwm.akeyless.io",
  "passkey_enabled": true,
  "passkey_verification": "required",
  "preconfigured_sign_in_title": "Sign in to Example Corp",
  "preconfigured_sign_in_message": "Use your corporate account.\n\nContact the IT help desk if you need help.",
  "installationSource": "bundled_prefill"
}
```

| Field | Required | Values |
|---|---|---|
| `enabled` | Yes | Must be `true`, or the file is ignored |
| `preferredAuthMethod` | Yes | `alias`, `saml`, `oidc`, `google`, `github`, `access-id`, `email` |
| `prefillAccessId` | Yes, unless the method is `email` | Your Access ID, for example `p-xxxxxxxxxxxx` |
| `allowedAuthMethods` | No | Limits the methods users can choose. Defaults to the preferred method only |
| `environment` | No | Region for email sign-in: `global`, `us`, `eu` and others |
| `config_id` | No | ID of your branding bundle. See [Branding & Customization](https://docs.akeyless.io/docs/web-extension-branding) |
| `preconfigured_sign_in_title` | No | Heading on the login screen, up to 120 characters |
| `preconfigured_sign_in_message` | No | Text on the login screen, up to 2,000 characters. `\n\n` starts a new paragraph |
| `passkey_verification` | No | `off`, `on` or `required` |

Both `snake_case` and `camelCase` names are accepted. The full list is on [Preconfigured Installs: Overview](https://docs.akeyless.io/docs/web-extension-preconfigured-install).

<Callout icon="⚠️" theme="warn">
  If `preferredAuthMethod` is missing or misspelled, or `prefillAccessId` is missing for a method that needs it, the extension **silently ignores the whole file** and users get the standard login screen. Check the JSON carefully, for example with any JSON validator.
</Callout>

### Step 7: Test the folder before you distribute it

1. Create a new, empty browser profile, so nothing from earlier installs gets in the way.
2. Open `chrome://extensions` (or `edge://extensions`) and turn on **Developer mode**.
3. Click **Load unpacked** and select your working folder.
4. Open the extension. The login screen should show your title, message and sign-in method.

If it shows the standard login screen instead, recheck Steps 4–6. When the test passes, remove the test profile.

---

## Part 2A — Publish to Edge Add-ons (hidden listing)

Skip this part if you are using Option B.

1. Zip the **contents** of your working folder. `manifest.json` must be at the top level of the ZIP, not inside a subfolder.
2. Sign in to [Microsoft Partner Center](https://partner.microsoft.com/dashboard/microsoftedge/overview) with your organization's developer account.
3. Create a new extension and upload the ZIP.
4. Under **Availability**, set visibility to **Hidden**, so that only people with the link (and your Intune policy) can find it.
5. Submit it for certification and wait for approval.
6. When it is published, note its **extension ID** from the listing URL. You need it in Part 3.

For Intune, the update address of an Edge Add-ons extension is always:

```
https://edge.microsoft.com/extensionwebstorebase/v1/crx
```

<Callout icon="ℹ️" theme="info">
  Each new Akeyless release needs a new submission and review. Talk to your Akeyless contact before you publish a listing.
</Callout>

---

## Part 2B — Sign and host the package yourself

Skip this part if you are using Option A.

### Step 8: Create the signing key and the package

The signing key decides the extension ID. **Create it once and keep it forever.** If you lose it, the next version gets a new ID, and every device installs it as a brand-new extension.

**Using the browser:**

1. Open `chrome://extensions` and turn on **Developer mode**.
2. Click **Pack extension**.
3. For **Extension root directory**, select your working folder. Leave **Private key file** empty the first time.
4. Click **Pack extension**.

**Or from the command line** (Windows):

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --pack-extension="C:\akeyless\akeyless-extension"
```

Chrome creates two files next to your working folder:

- `akeyless-extension.crx` — the package you will host
- `akeyless-extension.pem` — **the signing key. Store it somewhere safe**, such as your Akeyless vault.

For every later release, pack with the same key:

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --pack-extension="C:\akeyless\akeyless-extension" --pack-extension-key="C:\akeyless\akeyless-extension.pem"
```

### Step 9: Point the package at your update file

Decide where you will host the files, for example `https://downloads.example.com/akeyless/`. Then:

1. Add this line to `manifest.json` in your working folder:

   ```json
   "update_url": "https://downloads.example.com/akeyless/updates.xml",
   ```

2. Pack again with the same key, as in Step 8.

This tells installed copies where to look for new versions.

### Step 10: Get the extension ID

The ID is calculated from your key. On macOS, Linux, or Git Bash on Windows, run:

```bash
openssl rsa -in akeyless-extension.pem -pubout -outform DER 2>/dev/null | shasum -a 256 | head -c32 | tr 0-9a-f a-p
```

The result is a 32-letter ID made of the letters `a` to `p`. Write it down. You need it in Steps 11 and 12.

### Step 11: Create the update file

Create a file named `updates.xml`. Replace the ID, the address and the version. The version must match the `"version"` value in `manifest.json` **exactly**.

```xml
<?xml version='1.0' encoding='UTF-8'?>
<gupdate xmlns='http://www.google.com/update2/response' protocol='2.0'>
  <app appid='YOUR_EXTENSION_ID'>
    <updatecheck codebase='https://downloads.example.com/akeyless/akeyless-extension-1.30.158.crx' version='1.30.158' />
  </app>
</gupdate>
```

### Step 12: Upload both files

1. Rename the package to include its version, for example `akeyless-extension-1.30.158.crx`.
2. Upload it and `updates.xml` to your HTTPS location.
3. Make sure the server sends the `.crx` file with the content type `application/x-chrome-extension`. In Azure Blob Storage, set it in the blob's properties.
4. From a managed device, open the `updates.xml` address in a browser to confirm it loads.

---

## Part 3 — Deploy with Intune

In the steps below, **the forcelist value** is:

| Option | Forcelist value |
|---|---|
| A — Edge Add-ons | `YOUR_EXTENSION_ID;https://edge.microsoft.com/extensionwebstorebase/v1/crx` |
| B — Self-hosted | `YOUR_EXTENSION_ID;https://downloads.example.com/akeyless/updates.xml` |

### Windows

1. Sign in to the [Intune admin center](https://intune.microsoft.com).
2. Go to **Devices → Configuration → Create → New policy**.
3. Set **Platform** to **Windows 10 and later** and **Profile type** to **Settings catalog**. Click **Create**.
4. Name the profile, for example *Akeyless Password Manager – force install*, and click **Next**.
5. Click **Add settings** and add the settings for the browsers you manage:

   | Browser | Category | Setting | Value |
   |---|---|---|---|
   | Edge | Microsoft Edge → Extensions | **Control which extensions are installed silently** | The forcelist value |
   | Chrome *(Option B only)* | Google → Google Chrome → Extensions | **Configure the list of force-installed apps and extensions** | The forcelist value |

6. **Recommended for Option B:** so that devices always use your update file, add **Configure extension management settings** (Edge) or **Extension management settings** (Chrome) with:

   ```json
   {
     "YOUR_EXTENSION_ID": {
       "installation_mode": "force_installed",
       "update_url": "https://downloads.example.com/akeyless/updates.xml",
       "override_update_url": true
     }
   }
   ```

7. **Recommended:** block the public store version so users don't end up with two copies. Add **Control which extensions cannot be installed** (Edge) or **Configure extension installation blocklist** (Chrome) with:
   - Edge: `fppjjcloabbllcakfjefmkdpbaaikeog`
   - Chrome: `afmojeipcbpcfkdohnnjfkilfekoobmc`
8. Click **Next**. Skip scope tags unless you use them.
9. Under **Assignments**, add the device or user groups that should get the extension. Start with a small pilot group.
10. Click **Next**, then **Create**.

<Callout icon="ℹ️" theme="info">
  If **Google Chrome** does not appear in the settings catalog, import the Chrome ADMX templates first under **Devices → Configuration → Import ADMX**.
</Callout>

### macOS

**Edge:**

1. Go to **Devices → Configuration → Create → New policy**.
2. Set **Platform** to **macOS** and **Profile type** to **Settings catalog**.
3. Add the same Microsoft Edge extension settings as on Windows (steps 5–7 above).
4. Assign the policy and create it.

**Chrome:**

1. Save the following as `com.google.Chrome.plist`, with your forcelist value:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
     <key>ExtensionInstallForcelist</key>
     <array>
       <string>YOUR_EXTENSION_ID;https://downloads.example.com/akeyless/updates.xml</string>
     </array>
     <key>ExtensionInstallBlocklist</key>
     <array>
       <string>afmojeipcbpcfkdohnnjfkilfekoobmc</string>
     </array>
   </dict>
   </plist>
   ```

2. Go to **Devices → Configuration → Create → New policy**.
3. Set **Platform** to **macOS**, **Profile type** to **Templates**, and choose **Preference file**.
4. Set **Preference domain name** to `com.google.Chrome` and upload the plist.
5. Assign the policy and create it.

---

## Part 4 — Verify the rollout

On a pilot device:

1. Sync the device with Intune. On Windows: **Settings → Accounts → Access work or school → your account → Info → Sync**. On macOS: **Company Portal → Check settings**.
2. Open `edge://policy` or `chrome://policy` and click **Reload policies**. Your extension policy should be listed with status **OK**.
3. Open `edge://extensions` or `chrome://extensions`. The extension should appear with **Installed by your organization**, and users can't remove it.
4. Open the extension. The login screen should show your title, message and sign-in method.

In the Intune admin center, the profile's **Device status** shows which devices have applied it.

## Updating to a new version

Your private build doesn't update from the store. When Akeyless releases a new version:

1. Update the extension from the store on your admin machine.
2. Repeat **Steps 2–7** with the new version folder.
3. **Option A:** submit the new ZIP to your Partner Center listing.
   **Option B:** add your `update_url` back (Step 9), pack with **the same key** (Step 8), upload the new `.crx`, and change the address and `version` in `updates.xml`.

Devices pick up the new version on their own, usually within a few hours. Users stay signed in, and the settings saved on their devices stay as they are.

## Option C — Public store with a preconfigured link

You don't need Intune or your own package to give users a preconfigured extension. Akeyless creates a link for your organization. Users open it, install the extension from the regular store, and it opens already set up.

### How it works

1. Akeyless creates a **preconfigured link** for your tenant. It points to the official store listing and carries your settings: Access ID, sign-in method, region, branding, and your login-screen title and message.
2. The user opens the link. It shows the normal store page for Akeyless Password Manager 2.0.
3. The user clicks **Add to Chrome** (**Get** in Edge, **Add to Firefox** in Firefox).
4. When it installs, the extension reads the settings from the link and saves them.
5. The user opens the extension and sees your preconfigured login screen, for example a single **Sign in** button for your identity provider.

Because users install the official store extension, they get every update automatically, and there is nothing for you to repackage, sign or host.

### Setting it up

1. **Send your details to Akeyless** (your account team or support):
   - Your **Access ID** and **authentication method** (SAML, OIDC, alias, Google, GitHub, Access ID or email).
   - For email sign-in, your **region**.
   - Optional: your branding, the login-screen **title** and **message**, and your support URL.
   - The browsers your users use.
2. **Receive your links.** Akeyless sends one preconfigured link per browser.
3. **Test a link** on a browser profile that doesn't have the extension: open it, install, and check the login screen.
4. **Share the links** with your users by email, on your intranet or IT portal, or in your onboarding instructions.

### What a link looks like

A store link carries your settings as parameters after the normal store address. For example, a Chrome link for OIDC sign-in:

```
https://chromewebstore.google.com/detail/akeyless-password-manager/afmojeipcbpcfkdohnnjfkilfekoobmc?access_id=oidc:p-xxxxxxxxxxxx
```

And the Edge equivalent:

```
https://microsoftedge.microsoft.com/addons/detail/akeyless-password-manager/fppjjcloabbllcakfjefmkdpbaaikeog?access_id=oidc:p-xxxxxxxxxxxx
```

The part before the colon is the sign-in method, and the part after it is the Access ID. Links from Akeyless can also carry your branding and login-screen text. Ask Akeyless to generate them rather than writing them by hand, because values that fail validation are silently dropped. The full parameter list is on [Bridge Link Install](https://docs.akeyless.io/docs/web-extension-bridge-link).

### Instructions to give your users

Copy this into your email or intranet page:

> 1. Open this link in Chrome (or Edge): *[your link]*
> 2. Click **Add to Chrome** (in Edge: **Get**), then **Add extension**. Keep the store page open until it finishes.
> 3. Click the puzzle-piece icon in the toolbar and pin **Akeyless Password Manager**.
> 4. Click the Akeyless icon and sign in with your company account.
>
> If you already have the Akeyless extension installed, remove it first, then follow these steps.

### Things to know

| Rule | What it means |
|---|---|
| Install from the page the link opened | The extension reads the settings from that open store tab while it installs. If the user closes the tab first, or searches the store instead of using the link, they get the standard login screen. |
| Fresh installs only | The link sets up a new install. If the extension is already installed, remove it and install again through the link, or ask Akeyless for a **bridge link**, which updates an existing install. |
| Bridge links expire after 10 minutes | If Akeyless gives you a bridge link rather than a store link, users must install within 10 minutes of opening it. If it expires, open the link again rather than trying to fix the install. |
| Users can still remove it | Unlike an Intune install, users can remove the extension. Use Option A or B when the extension must be mandatory. |

<Callout icon="ℹ️" theme="info">
  **Combining with Intune.** You can also force-install the **public store** extension with Intune, using the store ID with the store's update address, for example `afmojeipcbpcfkdohnnjfkilfekoobmc;https://clients2.google.com/service/update2/crx` for Chrome. The extension then installs without a store page, so it can't read a link. Users get the standard login screen, and you deliver the settings afterwards with a bridge link from Akeyless.
</Callout>

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Policy page shows an error for the forcelist | The device isn't Entra ID-joined, domain-joined or MDM-enrolled | Deploy only to managed devices |
| Extension not installed, no policy error | The device hasn't synced, or `updates.xml` can't be reached | Sync the device. Open the `updates.xml` address on the device |
| Extension not installed (Option B) | Wrong content type for the `.crx`, or the ID doesn't match the key | Serve `application/x-chrome-extension`. Recalculate the ID (Step 10) |
| *"Cannot load extension with file or directory name _metadata"* | The `_metadata` folder was left in | Delete it (Step 4) and pack again |
| Extension installs but the login screen isn't preconfigured | `enabled` isn't `true`, a required field is missing, or the browser profile had the extension before | Check the JSON (Step 6). Test in a new profile |
| Changed settings don't reach devices | Settings apply on first install only | Use a [Bridge Link](https://docs.akeyless.io/docs/web-extension-bridge-link) for devices that already have the extension |
| Users see two Akeyless extensions | The store version is still installed | Block the store ID (Part 3, step 7) |
| New version doesn't arrive (Option B) | `version` in `updates.xml` doesn't match the package, or the package was signed with a different key | Fix `updates.xml`. Always pack with the original `.pem` |

<Callout icon="⚠️" theme="warn">
  **Removing the extension from the forcelist uninstalls it** from devices and clears the settings saved in the browser. Vault data is not affected, because it lives in Akeyless, but users have to sign in again after reinstalling.
</Callout>

## Security notes

- Repackage only the official store build or a package supplied by Akeyless. This is a password manager, so a modified copy from an unknown source is a serious risk.
- Protect the `.pem` signing key like any other credential. Anyone who has it can publish an update that your devices will trust.
- Host `updates.xml` and the `.crx` where only your administrators can change them.

## Related

- [Preconfigured Installs: Overview](https://docs.akeyless.io/docs/web-extension-preconfigured-install)
- [Preconfigured Package](https://docs.akeyless.io/docs/web-extension-preconfigured-package)
- [Bridge Link Install](https://docs.akeyless.io/docs/web-extension-bridge-link)
- [Branding & Customization](https://docs.akeyless.io/docs/web-extension-branding)
- [Troubleshooting](https://docs.akeyless.io/docs/web-extension-troubleshooting)
