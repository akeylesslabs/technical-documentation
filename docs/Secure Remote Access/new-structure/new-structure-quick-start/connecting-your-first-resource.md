---
title: 'Connecting Your First Resource '
deprecated: false
hidden: false
metadata:
  robots: index
---
This guide walks you through connecting your **first protected SSH resource via** the Akeyless Console. <br />the connection itself is made from the CLI with `akeyless connect`, authenticated with an **API key**.

By the end, you'll have a real SSH session open **from your terminal**, proxied through
SRA to a real target host.

***

## Prerequisites

- Gateway + SRA already deployed.
- An existing SSH Certificate Issuer&#x20;
- A reachable target host you can already reach over SSH&#x20;
- **Console access with permission to edit SSH Certificate Issuers and targets.**
- The `akeyless` CLI installed locally

***

## Allow the SRA SSH gateway pod to reach the host

The target host's firewall / security group must allow inbound SSH (port 22) from the SRA SSH gateway pod. In your cluster, this pod is named`ssh-gw-akeyless-gateway-...`. Allow-list the pod's outbound IP/CIDR or the node group subnet range it runs in, on port 22 on the target host.

Every step after this one will look correctly configured even if this is wrong, and the connection will still fail.

<br />

***

## Enable SRA on SSH Certificate Issuer and set the target

Editing the existing issuer's we created in the GW deployment settings directly in the Akeyless Console.

**Navigation:** Console → **Items** → locate your existing SSH Certificate Issuer → **Secure Remote Access**

Ordered actions:

1. Press edit button.
2. Turn the **Enable Secure Remote Access** toggle **ON**.
3. &#x20;Press on Add and enter your target host IP-address.(internal for same network as the GW and public for different network)
4. Fill in **Default SSH Username&#x20;**`ubuntu`**&#x2009;**.
5. **Save**.

***

## Create Authentication Method

This [Authentication Method](doc:access-and-authentication-methods) will be used to authenticate your Akeyless Gateway to your Akeyless account. <br />For this guide, API key authentication is used for simplicity.

<ApiKeyWarning />

## Connect via SRA web portal)

You can now open a session entirely from your browser:

1. Log into the Akeyless Console / SRA web portal using **any configured auth
   method** (API key, SSO/SAML, OAuth, etc.). Authentication into Akeyless is
   independent of the SSH certificate flow you just configured — any method works here.
2. Navigate to the SRA portal / targets list.
3. Select the target you just connected (the host from step 2).
4. Launch an SSH session in-browser.

Landing in a real in-browser terminal on your target host means SRA is genuinely
working end-to-end. That's your confirmation — not just that the settings saved.

<br />

## 4. Connect — from the CLI with `akeyless connect`, authenticated via API key

You can now open the session from your terminal. Authenticate the CLI with your API key
(Access ID + Access Key) — this is independent of the SSH certificate flow you just
configured in the Console:

```bash
akeyless auth --access-id <your-access-id> --access-key <your-access-key>
```

Then connect through the SSH Certificate Issuer you configured in step 2:

```bash
akeyless connect \
  -t "ubuntu@<host-ip-address>:22" \
  -n <cert-issuer-name>
```

| Flag | Value                         | What it does                                                                                                         |
| ---- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `-t` | `ubuntu@<host-ip-address>:22` | The OS user and target host/port to connect to — must match **Allowed Users** and **Secure Access Host** from step 2 |
| `-n` | `<cert-issuer-name>`          | The existing SSH Certificate Issuer you enabled Secure Access on in step 2                                           |

Landing in a real shell on your target host means SRA is genuinely working end-to-end.
That's your confirmation — not just that the settings saved.

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
