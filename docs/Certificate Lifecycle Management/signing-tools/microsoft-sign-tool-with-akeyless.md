---
title: Windows Code Signing with Akeyless
deprecated: false
hidden: true
metadata:
  robots: index
---
This guide provides step-by-step instructions to set up code signing using Akeyless for PKI certificate issuance and the Akeyless Key Storage Provider (KSP) on Windows. It includes creating secrets in Akeyless, generating certificates, configuring the KSP, and performing a complete uninstall/reinstall of the Akeyless KSP for troubleshooting or clean setup.

<br />

All commands assume you have the Akeyless CLI installed and authenticated. Replace placeholder paths (`/YourCompany/`) with your own organization-specific paths in Akeyless.

### Part 1: Create Secrets and Issue Code-Signing Certificate in Akeyless

#### Create Root Key for PKI Issuer

```shell Bash
akeyless create-dfc-key \
  --profile default \
  --name /YourCompany/code-signing/root-key \
  --alg RSA2048 \
  --split-level 2 \
  --certificate-ttl 30 \
  --generate-self-signed-certificate true
```

#### Create 4096-bit Key and Generate CSR

```shell Bash
akeyless generate-csr \
  --profile default \
  --split-level 2 \
  --name /YourCompany/code-signing/signing-key \
  --generate-key \
  --key-type dfc \
  --alg RSA4096 \
  --common-name code.sign.example.com | Out-File -Encoding ascii signing.csr
```

#### Create PKI Certificate Issuer

```shell Bash
akeyless create-pki-cert-issuer \
  --profile default \
  --name /YourCompany/code-signing/pki-issuer \
  --allowed-domains code.sign.example.com \
  --signer-key-name /YourCompany/code-signing/root-key \
  --code-signing-flag \
  --ttl 600d \
  --destination-path /YourCompany/code-signing
```

#### Issue the 4096-bit Certificate

```shell Bash
akeyless get-pki-certificate \
  --profile default \
  --cert-issuer-name /YourCompany/code-signing/pki-issuer \
  --csr-file-path signing.csr \
  > signing.pem
```

#### Example Configuration File (sqlcrypt.conf)

Create a file named sqlcrypt.conf in a secure location (example `C:\Akeyless\conf\sqlcrypt.conf)`:

```text Txt
akeyless_url = "https://gw-aws.lm.cs.akeyless.fans/api/v2"
base_item_path = "/YourCompany/"
log_path = ""
use_classic_keys = false

[ksp]
signing_key_item = "/YourCompany/code-signing/signing-key"
signing_cert_item = "/YourCompany/code-signing/signing-cert"

[auth]
access_type = "access_key"
access_id = ""
access_key = "*****************************"
```

<br />

> ❗️ Notes  
> Update `base_item_path` to match your Akeyless path.
> Fill in your actual `access_id` and `access_key`.
> The certificate will be automatically stored in Akeyless at the path specified in `signing_cert_item`.
>
>

### Part 2: Akeyless KSP – Full Uninstall and Install

This procedure ensures a clean removal and reinstallation of the Akeyless KSP. It clears registry entries, files, and cached provider information.

Important:

* Run all PowerShell commands from an elevated PowerShell (Run as Administrator).
* A reboot is required after uninstall and after install for changes to take effect reliably.
* Have the Akeyless KSP MSI file ready (e.g., downloaded from your build artifacts).

<br />
