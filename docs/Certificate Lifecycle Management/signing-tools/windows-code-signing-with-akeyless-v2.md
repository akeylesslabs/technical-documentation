---
title: Windows Code Signing with Akeyless
deprecated: false
hidden: false
metadata:
  robots: index
---
This guide provides step-by-step instructions to set up code signing using Akeyless for PKI certificate issuance and the Akeyless Key Storage Provider (KSP) on Windows. It covers creating secrets, generating certificates, configuring the KSP, and troubleshooting.

## Prerequisites

* Akeyless CLI installed and authenticated.
* Administrator privileges on the Windows machine.
* Replace placeholder paths (`/YourCompany/)` with your organization-specific paths.

## Part 1: Create Secrets and Issue Code-Signing Certificate

### Create Root Key for PKI Issuer

This key will sign the certificates issued by your internal CA.

```shell
akeyless create-dfc-key \
  --profile default \
  --name /YourCompany/code-signing/root-key \
  --alg RSA2048 \
  --split-level 2 \
  --certificate-ttl 30 \
  --generate-self-signed-certificate true
```

* [https://docs.akeyless.io/reference/createdfckey](https://docs.akeyless.io/reference/createdfckey)

### Create 4096-bit Key and Generate CSR

This is the key used for actual code signing.

```shell
akeyless generate-csr \
  --profile default \
  --split-level 2 \
  --name /YourCompany/code-signing/signing-key \
  --generate-key \
  --key-type dfc \
  --alg RSA4096 \
  --common-name code.sign.example.com | Out-File -Encoding ascii signing.csr
```

* [https://docs.akeyless.io/docs/ssh-and-pkitls-certificates?isFramePreview=true#creating-a-certificate-signing-request](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates?isFramePreview=true#creating-a-certificate-signing-request)

### Create PKI Certificate Issuer

This defines the policy for your internal CA.

```shell
akeyless create-pki-cert-issuer \
  --profile default \
  --name /YourCompany/code-signing/pki-issuer \
  --allowed-domains code.sign.example.com \
  --signer-key-name /YourCompany/code-signing/root-key \
  --code-signing-flag \
  --ttl 600d \
  --destination-path /YourCompany/code-signing
```

* [https://docs.akeyless.io/docs/ssh-and-pkitls-certificates?isFramePreview=true#creating-a-certificate-issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates?isFramePreview=true#creating-a-certificate-issuer)

### Issue the 4096-bit Certificate

Sign the CSR generated in step 2.

```shell
akeyless get-pki-certificate \
  --profile default \
  --cert-issuer-name /YourCompany/code-signing/pki-issuer \
  --csr-file-path signing.csr \
  -e codesigning \
  > signing.pem
```

* [https://docs.akeyless.io/docs/ssh-and-pkitls-certificates?isFramePreview=true#issuing-a-certificate](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates?isFramePreview=true#issuing-a-certificate)

## Part 2: Akeyless KSP Installation and Configuration

### Prepare Configuration File

Create a file named `sqlcrypt.conf` in a persistent location (`C:\Akeyless\conf\sqlcrypt.conf`).

```shell
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

### Set Environment Variable (Mandatory)

The Akeyless KSP requires the AKEYLESS_SQLCRYPT_CONFIG_PATH environment variable to locate your configuration file.

Run this in an Elevated PowerShell:

```shell
[System.Environment]::SetEnvironmentVariable('AKEYLESS_SQLCRYPT_CONFIG_PATH', 'C:\Akeyless\conf\sqlcrypt.conf', [System.EnvironmentVariableTarget]::Machine)

# Verify the variable is set
$env:AKEYLESS_SQLCRYPT_CONFIG_PATH
```

Note: You may need to restart your shell or machine for this to take effect globally.

### Download KSP

[https://akeyless.jfrog.io/ui/native/akeyless-ksp/](https://akeyless.jfrog.io/ui/native/akeyless-ksp/)

### Install the KSP

Use a dedicated folder for logs to ensure they persist across reboots.

```shell
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

### Verify Installation

After rebooting, confirm the KSP is registered.

```shell
certutil -csplist | findstr /i "Akeyless"
# Output should be: Provider Name: Akeyless KSP
```

## Part 3: Sync Certificate and Test Signing

### Sync Certificate to Windows Store

The helper tool downloads the certificate from Akeyless and binds it to the KSP in the Windows Certificate Store.

```shell
$helper = "C:\Program Files\Akeyless\Akeyless KSP\akeyless-ksp-cert-helper.exe"
& $helper --config-path $env:AKEYLESS_SQLCRYPT_CONFIG_PATH sync-cert --store-scope machine --store-name My
```

### Verify Binding

Ensure the certificate is present and linked to "Akeyless KSP".

```shell
$thumb = (Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.Subject -like "*code.sign.example.com*" }).Thumbprint
certutil -store -v My $thumb | findstr /i "Provider Container"
# Expected Output: Provider = Akeyless KSP
```

### Sign a Test File

```shell
$file = "C:\Temp\test_app.dll"
signtool sign /debug /v /sm /s My /sha1 $thumb /fd SHA256 /tr "http://timestamp.digicert.com" /td SHA256 $file
```

### Establish Trust (Import Root CA)

```shell
$file = "C:\Temp\test_app.dll"
signtool sign /debug /v /sm /s My /sha1 $thumb /fd SHA256 /tr "http://timestamp.digicert.com" /td SHA256 $file
```

If `signtool verify` fails because the chain is untrusted, you must import the Root CA used in Part 1.

Step A: Retrieve the Root CA Get the public certificate of the root key you created earlier.

```shell
akeyless get-certificate \
  --name /YourCompany/code-signing/root-key \
  --out-file root-ca.pem
```

* [https://docs.akeyless.io/docs/certificate-based-authentication?isFramePreview=true#getting-a-certificate](https://docs.akeyless.io/docs/certificate-based-authentication?isFramePreview=true#getting-a-certificate)

Step B: Import into Trusted Root Store Run this in Elevated PowerShell on the signing machine (or any machine verifying the signature).

```shell
Import-Certificate -FilePath .\root-ca.pem -CertStoreLocation Cert:\LocalMachine\Root
```

* [https://learn.microsoft.com/en-us/powershell/module/pki/import-certificate?view=windowsserver2025-ps](https://learn.microsoft.com/en-us/powershell/module/pki/import-certificate?view=windowsserver2025-ps)

Step C: Verify Chain

```shell
signtool verify /pa /v $file
```

## Troubleshooting (Clean Uninstall)

If you need to troubleshoot or reinstall a clean version, follow this uninstall procedure.

Full Uninstall

```shell
# Define stable log path
$logDir = "C:\Akeyless\logs" 
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logUninst = Join-Path $logDir "AkeylessKspUninstall.log"

# Find Product Code
$app = Get-ChildItem "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" | 
       ForEach-Object { Get-ItemProperty $_.PSPath } | 
       Where-Object { $_.DisplayName -like "Akeyless KSP*" } | Select-Object -First 1

# Uninstall
if ($app) {
    msiexec /x $app.PSChildName /l*v "$logUninst"
} else {
    Write-Host "Akeyless KSP not found."
}
```

Reboot the machine to clear locked files and registry handles.

Verify Cleanup

After reboot, ensure no traces remain:

```shell
certutil -csplist | findstr /i "Akeyless"  # Should return nothing
Test-Path "C:\Windows\System32\AkeylessKsp.dll" # Should be False
```
