---
title: Password Generator & Strength
---
The generator is available wherever you enter a password — the create and edit overlays, and the in-page suggestion popup on signup and password-change forms.

## Strength meter

As you type or generate, the meter reports:

- **Effective entropy in bits**, not just a colour bar
- **Specific feedback** on what weakens the password — dictionary words, keyboard runs, repeated characters, dates

## Breach check

The password is checked against a list of passwords known from public data breaches. A match is flagged as:

<Callout icon="⚠️" theme="warn">
  Found in common breached password lists

  **This check runs entirely offline.** The comparison uses a filter bundled inside the extension. **Your password is never sent anywhere** — no network request is made, to Akeyless or to any third party.
</Callout>

The check is approximate in one direction only: a flagged password is definitely in the leaked set, while an unflagged password is probably not.

## Passphrase mode

Instead of a random character string, the generator can produce a memorable passphrase built from a 100,000-word English dictionary using a cryptographically secure random source.

Passphrases can be generated to satisfy your organization's password policy, so you do not have to re-roll until one passes.

## Account password policy

If your organization sets a password policy, the generator and the strength meter both respect it. See [Setting Password Policy On Account Level](https://docs.akeyless.io/docs/setting-password-policy-on-account-level-1).

## Related

- [Setting Password Policy On Account Level](https://docs.akeyless.io/docs/setting-password-policy-on-account-level-1)
- [Creating New Password](https://docs.akeyless.io/docs/creating-new-password-1)
- [Security Health in the Extension](https://docs.akeyless.io/docs/web-extension-security-health)
