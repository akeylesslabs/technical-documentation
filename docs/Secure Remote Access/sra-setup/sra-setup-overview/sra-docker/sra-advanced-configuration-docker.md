---
title: Docker Compose Advanced Configuration
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
For centralized policy guidance on entitlements, username claim mapping, redirect hardening, and session controls, see [Access Configuration and Policies](https://docs.akeyless.io/docs/sra-access-configuration-and-policies).

## SSH Legacy Algorithm

As both classic SSH and RDP access are based on SSH certificates, to support legacy algorithms for SSH signing, please set the `legacySigningAlg` with `true` to sign the SSH certificates using the legacy `ssh-rsa-cert-v01@openssh.com` signing algorithm.

```shell
akeyless gateway update remote-access --legacy-ssh-algorithm true --gateway-url https://<Your-Akeyless-GW-URL>:8000
```

## Key Exchange Algorithm

A Key Exchange Algorithm is a method used to securely exchange cryptographic keys between parties over an insecure channel such as a public network. The primary goal of these algorithms is to enable two or more parties to securely establish a shared secret key, which can then be used for encrypting and decrypting messages during communication.

```shell
akeyless gateway update remote-access --kexalgs <algorithm-name> --gateway-url https://<Your-Akeyless-GW-URL>:8000
```

The options for this are:

- `curve25519-sha256`
- `diffie-hellman-group-exchange-sha1`
- `diffie-hellman-group-exchange-sha256`
- `diffie-hellman-group14-sha1`
- `diffie-hellman-group14-sha256`
- `diffie-hellman-group16-sha512`
- `diffie-hellman-group18-sha512`
- `ecdh-sha2-nistp256`
- `ecdh-sha2-nistp384`
- `ecdh-sha2-nistp521`

## RDP Configuration

### RDP & SSH User Access

For RDP connections with an [externally provided username](https://docs.akeyless.io/docs/sra-remote-desktop#set-up-remote-access-to-a-windows-machine-from-the-akeyless-console), you can set your RDP or SSH resources to use the relevant attribute from the IdP JWT (For example, email) to establish a connection to the target server using the authenticated username. This applies to all SSH-based sessions, including RDP and Linux systems.

```yaml RDP
akeyless gateway update remote-access --rdp-target-configuration <your-sub-claim> --ssh-target-configuration <your-sub-claim> --gateway-url https://<Your-Akeyless-GW-URL>:8000
```
```yaml SSH
akeyless gateway update remote-access --ssh-target-configuration <your-sub-claim> --gateway-url https://<Your-Akeyless-GW-URL>:8000
```

### Support for Other Keyboard Layouts

To enable a keyboard layout in your remote sessions for Windows, use the following command (the default is `en-us-qwerty`):

```shell
akeyless gateway update remote-access --keyboard-layout <layout-option> --gateway-url https://<Your-Akeyless-GW-URL>:8000
```

```yaml Layout Options
value: da-dk-qwerty # Danish (Qwerty)
value: de-ch-qwertz # Swiss German (Qwertz)
value: de-de-qwertz # German (Qwertz)
value: en-gb-qwerty # UK English (Qwerty)
value: en-us-qwerty # US English (Qwerty) default
value: es-es-qwerty # Spanish (Qwerty)
value: es-latam-qwerty # Latin American (Qwerty)
value: fr-be-azerty # Belgian French (Azerty)
value: fr-ch-qwertz # Swiss French (Qwertz)
value: fr-fr-azerty # French (Azerty)
value: hu-hu-qwertz # Hungarian (Qwertz)
value: it-it-qwerty # Italian (Qwerty)
value: ja-jp-qwerty # Japanese (Qwerty)
value: no-no-qwerty # Norwegian (Qwerty)
value: pl-pl-qwerty # Polish (Qwerty)
value: pt-br-qwerty # Portuguese Brazilian (Qwerty)
value: sv-se-qwerty # Swedish (Qwerty)
value: tr-tr-qwerty # Turkish-Q (Qwerty)
```

## Session Log Forwarding

The Akeyless SRA supports Session Log Forwarding, which forwards SSH session recordings to any logging system. These settings can be added by way of the Gateway management console or by way of CLI:

```shell
akeyless gateway update remote-access-session-forwarding -h
```

For provider-specific commands and flags, see [CLI Reference - Gateway Secure Remote Access](https://docs.akeyless.io/docs/cli-reference-sra).

### What a Session Log Contains

* **Input:** The command as the terminal showed it when Enter was pressed, reflecting Tab completion, command history, and line edits — not the raw keystrokes used to produce it.

* **Hidden input:** Never recorded. Typing at a prompt that hides input, such as a password prompt, produces an `[input not displayed]` marker instead.

* **Output:** Each line the target printed, unless commands-only mode is enabled (see `SRA_RECORDING_CAPTURE_OUTPUT` below).

* **Full-screen applications** (for example, `vi`, `less`, `top`): Recorded using start and end markers instead of keystroke-by-keystroke output.

* Commands entered in shells running inside **tmux** continue to be recorded.

* **Masking:** Enabled by default. Known secret formats are replaced with `[masked]` in every record — including values following secret-named flags and fields (`--password`, `DB_PASSWORD=`, `"api_key":`), bearer tokens, passwords embedded in URLs, AWS, GitHub, Slack, Google, and Stripe keys, JWTs, and private key blocks. Masking is best effort on visible text, and is separate from the hidden-input rule above (hidden input is never recorded in the first place, so there's nothing for masking to replace there).

<Callout icon="📘" theme="info">
  SIEM rules that rely on raw keystrokes may need to be updated: SSH recordings now capture commands as displayed when Enter is pressed, instead of raw keystrokes.
</Callout>

### Session Recording Settings

These are environment variables on the SSH bastion, set as part of your deployment in the `sra.env` config file:

* `SRA_RECORDING_CAPTURE_OUTPUT` (default `true`): Set to `false` to record commands only, without their output.

* `SRA_RECORDING_CAPTURE_KEYSTROKES` (default `false`): Set to `true` to also record every key as typed.

* `SRA_RECORDING_MASKING` (default `true`): Set to `false` to stop masking known secret formats.

* `SRA_RECORDING_MASK_PATTERNS` (default empty): Extra masking rules, as one RE2 regular expression per line. Leave empty to rely only on the built-in masking patterns.

```yaml
SRA_RECORDING_CAPTURE_OUTPUT=true
SRA_RECORDING_CAPTURE_KEYSTROKES=false
SRA_RECORDING_MASKING=true
SRA_RECORDING_MASK_PATTERNS=
```

<Callout icon="⚠️" theme="warn">
  ### Keystroke capture

  Keystroke capture records every key exactly as typed, including passwords typed at hidden prompts, and sends them to your log destination in clear text. Enable it only if your compliance requirements call for keystroke-level evidence, and restrict access to the destination.
</Callout>

## RDP Recordings

**RDP** sessions provide video recordings that can be saved to AWS S3 buckets or Azure Blob Storage. To work with session recording for RDP, provide the following settings to upload your recording to an S3 bucket or Azure Blob Storage.

```shell
akeyless gateway update remote-access-rdp-recording -h
```

For CLI flags and usage, see [CLI Reference - Gateway Secure Remote Access](https://docs.akeyless.io/docs/cli-reference-sra).

To store local recordings inside your Gateway, set the `rdp-session-storage` to `local`. Session recordings will be stored inside the Gateway under `/home/akeyless/recordings`. Make sure to add a persistent volume to your SRA deployment.

## SSH Fingerprint

Use this parameter inside your deployment to store fingerprint information in a specific location within your Akeyless account. This approach prevents the need to manually re-accept the SSH host key fingerprint after upgrades or other changes, make sure the Gateway Authentication method has the following permissions on that folder `create`, `read`, `list`. In the example below, the fingerprints will be stored in the `/MY_SSH_REMOTE_ACCESS_HOST_KEYS` folder.

```yaml
SSH_HOST_KEYS_PATH=/MY_SSH_REMOTE_ACCESS_HOST_KEYS
```

## SSH Session Liveness Settings&#x20;

To control how the bastion checks that both sides of a session are still responsive: the connection from the client into the gateway, and the connection from the gateway onward to the target server, set the `SSH_CLIENT_ALIVE_INTERVAL`, `SSH_CLIENT_ALIVE_COUNT_MAX`, `SSH_SERVER_ALIVE_INTERVAL`, and `SSH_SERVER_ALIVE_COUNT_MAX` variables as part of your deployment in the `sra.env` config file:

```yaml
SSH_CLIENT_ALIVE_INTERVAL=120
SSH_CLIENT_ALIVE_COUNT_MAX=2
SSH_SERVER_ALIVE_INTERVAL=120
SSH_SERVER_ALIVE_COUNT_MAX=2
```

## SSH Agent Forwarding

Starting with SRA `v3.5.0`, multi-hop SSH sessions support SSH agent forwarding. To enable it, set the `SSH_ALLOW_AGENT_FORWARDING` variable as part of your deployment in the `sra.env` config file:

```yaml
SSH_ALLOW_AGENT_FORWARDING=true
```

#
Users then pass `-A` through to the SSH client when connecting:

```shell
akeyless connect \
--ssh-extra-args=-A \
-t <[user@]target/hostname/ip[:port]>
```

The SSH key remains on the bastion and is not forwarded to the remote host. The destination server must also permit agent forwarding - set `AllowAgentForwarding yes` in its `sshd_config`.

<Callout icon="⚠️" theme="warn">
  ### **Security considerations:**

  Agent forwarding exposes the bastion's agent socket to every host in the session chain. A user with root on any of those hosts can use that socket to authenticate as the bastion identity to further systems, for as long as the session is open.

  This variable applies to the whole deployment, not to individual sessions. Enabling it affects every session on that bastion, not only the multi-hop ones that need it.
</Callout>