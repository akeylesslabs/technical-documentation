---
title: Windows Code Signing with Akeyless v2
deprecated: false
hidden: true
metadata:
  robots: index
---
This guide provides step-by-step instructions to set up code signing using Akeyless for PKI certificate issuance and the Akeyless Key Storage Provider (KSP) on Windows. It covers creating secrets, generating certificates, configuring the KSP, and troubleshooting.

Prerequisites:

* Akeyless CLI installed and authenticated.
* Administrator privileges on the Windows machine.
* Replace placeholder paths (`/YourCompany/)` with your organization-specific paths.

### Part 1: Create Secrets and Issue Code-Signing Certificate

#### Create Root Key for PKI Issuer

This key will sign the certificates issued by your internal CA.

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

This is the key used for actual code signing.

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

This defines the policy for your internal CA.

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

Sign the CSR generated in step 2.

```shell Bash
akeyless get-pki-certificate \
  --profile default \
  --cert-issuer-name /YourCompany/code-signing/pki-issuer \
  --csr-file-path signing.csr \
  > signing.pem
```

### Part 2: Akeyless KSP Installation and Configuration

#### Prepare Configuration File


Create a file named `sqlcrypt.conf` in a persistent location (`C:\Akeyless\conf\sqlcrypt.conf`).

```shell Bash
akeyless_url = "https://gw-aws.lm.cs.akeyless.fans/api/v2"
base_item_path = "/YourCompany/"
log_path = ""
use_classic_keys = false

[ksp]
signing_key_item = "/YourCompany/code-signing/signing-key"
signing_cert_item = "/YourCompany/code-signing/signing-cert"

[auth]
access_type = "access_key"
access_id = "YOUR_ACCESS_ID"
access_key = "YOUR_ACCESS_KEY"
```

#### Set Environment Variable (Mandatory)


The Akeyless KSP requires the AKEYLESS_SQLCRYPT_CONFIG_PATH environment variable to locate your configuration file.

Run this in an Elevated PowerShell:

```shell Bash
[System.Environment]::SetEnvironmentVariable('AKEYLESS_SQLCRYPT_CONFIG_PATH', 'C:\Akeyless\conf\sqlcrypt.conf', [System.EnvironmentVariableTarget]::Machine)

# Verify the variable is set
$env:AKEYLESS_SQLCRYPT_CONFIG_PATH
```

Note: You may need to restart your shell or machine for this to take effect globally.

#### Install the KSP


Use a dedicated folder for logs to ensure they persist across reboots.

```shell Bash
# Define paths
$msi = "C:\Path\To\AkeylessKspInstaller.msi"
$logDir = Split-Path -Parent $msi
$logInstall = Join-Path $logDir "AkeylessKspInstall.log"

# Install
Start-Process -FilePath "msiexec.exe" -Verb RunAs -Wait -ArgumentList @(
    "/i", $msi, "IMPORT_CERT=0", "/l*v", $logInstall
)

# Check Exit Code (0 or 3010 means success)
$LASTEXITCODE
```

Reboot the machine now to register the provider.

#### Verify Installation


After rebooting, confirm the KSP is registered.

```shell Bash
certutil -csplist | findstr /i "Akeyless"
# Output should be: Provider Name: Akeyless KSP
```

### Part 3: Sync Certificate and Test Signing
