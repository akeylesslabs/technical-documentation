---
title: 'Connecting Your First Resource '
deprecated: false
hidden: false
metadata:
  robots: index
---
This guide assumes Akeyless Gateway + SRA are already deployed and running (see
[SRA Beginner Quick Start](sra-quick-start-beginner.md) if not) and walks you through
connecting your **first protected SSH resource**, reusing an **existing SSH Certificate
Issuer** — entirely through the Akeyless Console. No CLI commands are needed for
configuration or connection.

By the end, you'll have a real SSH session open **in your browser**, proxied through
SRA to a real target host. A working in-browser terminal session is the only real
confirmation that everything below was done correctly — "settings saved" is not enough.

***

## Prerequisites checklist

- [ ] Gateway + SRA already deployed and showing **Active** in the Akeyless Console
- [ ] An **existing SSH Certificate Issuer** already created (this guide reuses it —
  it does not create a new one)
- [ ] The signer key backing that issuer already exists and is attached to it
- [ ] A real, reachable target host you can already reach over SSH some other way
  (e.g. via an existing key or bastion) — this is what you're about to connect
  through SRA
- [ ] Console access with permission to edit SSH Certificate Issuers and targets

***

## 1. Network prerequisite — allow the SRA SSH gateway pod to reach the host

Do this **first**. Every step after this one will look correctly configured even if
this is wrong, and the connection will still fail — this is the single most common
thing people forget.

The target host's firewall / security group must allow **inbound SSH (port 22)** from
the SRA SSH gateway pod. In your cluster, this pod is named something like
`ssh-gw-akeyless-gateway-...`. Allow-list the pod's outbound IP/CIDR — or the node
group / subnet range it runs in — on port 22 on the target host.

Verify this before moving on. If you skip it, steps 2 and 3 will save cleanly, the
issuer will show as configured, and you'll still get a connection timeout at the very
last step.

***

## 2. Reuse the existing SSH Certificate Issuer — enable SRA and set the target (Console)

Do **not** create a new issuer, and do not use the CLI for this. You're editing the
existing issuer's settings directly in the Akeyless Console.

**Navigation:** Console → **Secrets & Keys** (PKI / SSH Certificate Issuers section) →
locate your existing SSH Certificate Issuer → **Edit**

> **TODO (verify before publishing):** confirm the exact console breadcrumb and section
> name in the current Console UI — this may differ slightly (e.g. a dedicated
> "Certificate Issuers" or "SSH" tab) depending on your Console version.

On the issuer's edit screen, set/confirm the following fields, then **Save**:

| Field                        | Value               | What it does                                                           |
| ---------------------------- | ------------------- | ---------------------------------------------------------------------- |
| Allowed Users                | `ubuntu`            | Which OS user(s) on the target the issued SSH certificate is valid for |
| TTL                          | `300` (seconds)     | Lifetime of certificates issued by this issuer                         |
| Secure Access                | **ON**              | Enables SRA (Secure Remote Access) for this issuer                     |
| Secure Access SSH Creds User | `ubuntu`            | The OS user SRA uses to broker the session on the target               |
| Secure Access Host           | `<host-ip-address>` | The target host SRA will connect to                                    |

Ordered actions:

1. Open the existing SSH Certificate Issuer for editing.
2. Turn the **Secure Access** toggle **ON**.
3. Fill in **Secure Access SSH Creds User** and **Secure Access Host**.
4. Confirm **Allowed Users** and **TTL** match the table above (adjust `ubuntu` /
   `300` to your actual OS username and desired certificate lifetime).
5. **Save**.

> **TODO (verify before publishing):** confirm these field labels match the live
> Console exactly — they're presented here as the source of truth for _behavior_,
> but exact label wording should be checked against the current UI.

***

## 3. Unset "Override default SSH Certificate Issuer"

On the same issuer/target configuration area (or wherever it lives in your Console
version — flag this as a TODO if uncertain), there is a separate toggle called
**"Override default SSH Certificate Issuer."**

This must be turned **OFF** for the issuer settings you just saved in step 2 to
actually take effect. It's easy to miss because it's a separate control from the
fields you just edited — if it's left on, the target will keep using whatever issuer
it was overridden to, ignoring your changes.

> **TODO (verify before publishing):** confirm the exact screen/location of this
> toggle in the current Console.

***

## 4. Connect — via the Console (SRA web portal)

You can now open a session entirely from your browser:

1. Log into the Akeyless Console / SRA web portal using **any configured auth
   method** (API key, SSO/SAML, OAuth, etc.). Authentication into Akeyless is
   independent of the SSH certificate flow you just configured — any method works here.
2. Navigate to the SRA portal / targets list.
3. Select the target you just connected (the host from step 2).
4. Launch an SSH session in-browser.

Landing in a real in-browser terminal on your target host means SRA is genuinely
working end-to-end. That's your confirmation — not just that the settings saved.

***

## Troubleshooting

| Symptom                                                        | Likely cause                                                                                                               | Fix                                                                                                      |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Connection times out                                           | Step 1 (network/firewall) was skipped or the pod's IP/CIDR isn't actually allow-listed on the target                       | Re-check the target's firewall/security group against the SRA SSH gateway pod's real egress IP or subnet |
| "Permission denied" when session opens                         | Username not included in **Allowed Users**, or **Secure Access SSH Creds User** doesn't match a real OS user on the target | Re-check both fields on the issuer against the actual OS username on the target host                     |
| Changes from step 2 don't seem to apply                        | **Override default SSH Certificate Issuer** is still ON                                                                    | Go back to step 3 and confirm it's OFF                                                                   |
| Session works, then a new connection fails a few minutes later | SSH certificate TTL expired                                                                                                | Expected behavior — raise **TTL** on the issuer for longer sessions                                      |

***

## Related Documentation

- [SRA Beginner Quick Start](sra-quick-start-beginner.md)
- SSH Certificate Issuer reference — _(TODO: add real docs.akeyless.io link before publishing)_

<br />
