---
title: Security Health in the Extension
---
A scored view of your **personal** credentials. Corporate and team items are out of scope.

<Callout icon="ℹ️" theme="info">
  The web console has its own Security Health page covering a different scope.
  See *Password Manager Web Console → Security Health*.
</Callout>

---

## Protection score

The score runs 0–100 and is built from two equal 50-point pillars:

- **Uniqueness** — reduced by password reuse across items, and by matches against the
  offline breach list.
- **Freshness** — how many items were updated in the last 90 days.

Bands: **0–35 red**, **36–66 orange**, **67+ green**. An empty vault scores 100.

While a scan is running the gauge reads red and blends toward the real color as it completes.
A green progress bar and *"All personal items were scanned"* confirm completion.

![Protection score, gauge view](https://files.readme.io/88acc2b51fe69738737e124efb85096c90537766bb18349a53b887a344045daa-security-health-gauge.png)
*Gauge view*

Switch to **Graph** to see how each metric contributes.

![Protection score, graph view](https://files.readme.io/6b10585669cfeb506a0624d6a72c35c1c5186d26f1ecc1e95ab347755bc9e9c6-security-health-graph.png)
*Graph view*

Use the refresh icon to rescan, and the info icon for an explanation of the score.

---

## Metrics

| Tile | Meaning |
|---|---|
| **Same password** | Items sharing a password with at least one other item |
| **Stale 90d+** | Items not edited in 90 or more days, or with an unknown date |
| **Leaked passwords** | Passwords found in public data breaches |
| **Passkeys** | Count of passkeys — personal folder only |
| **OTP** | Items carrying an `otpauth` URI or an OTP custom field |

Select any tile to open the matching list of items.

**Passkeys and OTP are reported but do not change the score.**

<Callout icon="ℹ️" theme="info">
  **The breach check runs entirely offline.** Passwords are compared against a filter bundled
  with the extension. No password is ever sent anywhere.
</Callout>

---

## Nothing shown?

Security Health covers personal items only. Save passwords or passkeys to your personal folder
to populate the reuse, freshness, OTP and leak metrics.

## Related

- [Password Generator & Strength](https://docs.akeyless.io/docs/web-extension-password-generator)
- [Passkey](https://docs.akeyless.io/docs/passkey)
- [Adding and Using One-Time Passwords](https://docs.akeyless.io/docs/adding-and-using-otp-1)
