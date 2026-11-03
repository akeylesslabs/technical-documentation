---
title: Signing In on Mobile
---
Sign in with the same Akeyless identity you use in the web console and the browser
extension. Which methods you see depends on what your organization allows.

## Authentication methods

Tap the method shown on the sign-in screen to open the list, then choose one.

| Method | What you enter | What happens |
|---|---|---|
| **Login with Email** | Email, password, and a code if your account uses two-factor authentication | Signs in directly |
| **Login with Alias** | Your alias, such as `team/you` | Signs in directly |
| **Login with SAML** | Your `Access ID` | Your identity provider opens inside the app |
| **Login with OIDC** | Your `Access ID` | Your OIDC provider opens inside the app |
| **Login with Access ID** | `Access ID` and `Access Key` | Signs in directly |

<Callout icon="ℹ️" theme="info">
  **Gmail and GitHub sign-in are not offered in the mobile app.** If you normally use them in
  the browser extension, sign in on mobile with another method your account supports, or ask
  your administrator.
</Callout>

## Email sign-in

1. Choose **Login with Email**.
2. Check the **environment** — the region your account is hosted in. Most accounts use the
   default. Change it only if your account lives in a specific region, such as US or EU.
3. Enter your email address and tap **Continue**.
4. If your email belongs to more than one Akeyless account, choose the account and tap
   **Continue**.
5. Enter your password and tap **Sign In**.
6. If your account requires two-factor authentication, enter the code that is emailed to you.

## SAML and OIDC (single sign-on)

1. Choose **Login with SAML** or **Login with OIDC**.
2. Enter your organization's `Access ID` and continue.
3. Your identity provider's page — for example Okta or Microsoft Entra ID — opens in a
   browser window inside the app. Sign in there as you normally would.
4. When the provider finishes, the window closes on its own and your vault opens.

You do not need to switch to Safari or Chrome. If you close the provider window before
finishing, you return to the sign-in screen and can start again.

<Callout icon="ℹ️" theme="info">
  **Where do I find my Access ID?** Ask your Akeyless administrator. It is the same Access ID
  you use for SAML or OIDC sign-in in the web extension and the web console.
</Callout>

The region for Alias, SAML, OIDC and Access ID sign-in comes from the Access ID itself, so
there is nothing to choose.

## The app remembers your last sign-in

After a successful sign-in, the app remembers the method and the Access ID or alias you used,
so next time the sign-in screen opens ready to go. A failed attempt changes nothing. Signing
out does not clear this, so you can sign back in without retyping.

## When sign-in fails

For your security, every rejected sign-in shows the same message:

> Sign-in failed. Check your details and try again.

The app does not say whether it was the email, the account or the password that was wrong.
Two other messages mean something different:

| Message | Meaning |
|---|---|
| **Too many sign-in attempts. Wait a few minutes and try again.** | Too many attempts in a short time. Wait, then retry |
| **Akeyless could not complete sign-in right now. Try again shortly.** | A temporary service problem, not your credentials |

If your organization has blocked mobile access, the app shows your administrator's message
instead.

## Staying signed in

Your session lasts as long as your authentication method allows. When it expires, the app
returns you to the sign-in screen — including when you reopen the app after it has been in
the background. To change how long sessions last, contact your administrator.

To sign out yourself, tap **More** → **Settings** → **Sign out**. Signing out also removes
every saved login from the phone's AutoFill — see
[AutoFill on iPhone and Android](https://docs.akeyless.io/docs/pwm-mobile-autofill).

## Related

- [Installing the Mobile App](https://docs.akeyless.io/docs/pwm-mobile-installation)
- [Troubleshooting](https://docs.akeyless.io/docs/pwm-mobile-troubleshooting)
- [Signing In to the Web Extension](https://docs.akeyless.io/docs/web-extension-sign-in)
