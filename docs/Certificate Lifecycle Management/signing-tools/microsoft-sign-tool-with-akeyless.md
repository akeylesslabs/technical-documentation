---
title: Windows Code Signing with Akeyless v0
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

#### Define Variables

```shell Shell
$msi = "C:\Path\To\AkeylessKspInstaller.msi"   # Update to your MSI location
$prov = "Akeyless KSP"
$logInstall = Join-Path $env:TEMP "AkeylessKspInstall.log"
$logUninst = Join-Path $env:TEMP "AkeylessKspUninstall.log"
```

Verify:

```shell Shell
$msi
$logInstall
Test-Path $msi   # Should return True
```

#### Full Uninstall

```shell Shell
$uninstRoots = @(
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
    "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
)

$app = Get-ChildItem $uninstRoots | ForEach-Object { Get-ItemProperty $_.PSPath } |
       Where-Object { $_.DisplayName -like "Akeyless KSP*" } | Select-Object -First 1

$app.DisplayName
$app.PSChildName   # This is the ProductCode GUID

msiexec /x $app.PSChildName /l*v "$logUninst"
$LASTEXITCODE
```

Expected exit code: 0 or 3010 (reboot required).

Reboot the machine now. Do not skip this step.

#### Verify Uninstall (after reboot)

Run these checks – all should show the provider is gone:

```shell Shell
certutil -csplist | findstr /i "Akeyless"   # No output

reg query "HKLM\SYSTEM\CurrentControlSet\Control\Cryptography\Providers\Akeyless KSP" /s   # Key not found
reg query "HKLM\SOFTWARE\Microsoft\Cryptography\Providers\Akeyless KSP" /s                  # Key not found

reg query "HKLM\SYSTEM\CurrentControlSet\Control\Cryptography\Configuration\Local\Default\00010001\KEY_STORAGE" /v Providers   # No Akeyless KSP

Test-Path "C:\Windows\System32\AkeylessKsp.dll"                     # False
Test-Path "C:\Program Files\Akeyless\Akeyless KSP\akeyless-ksp-cert-helper.exe"   # False
```

(Optional) Clean leftover certificate bindings:

```shell Shell
certutil -store -v My | Select-String -Pattern "Provider = Akeyless KSP" -Context 6,10
# If any found, run your cleanup script or manually re-bind certificates
```

#### Full Install

##### Install the MSI

```shell Shell
msiexec /i "$msi" IMPORT_CERT=0 /l*v "$logInstall"
$LASTEXITCODE
```

(Alternative robust version if issues occur:)

```shell Shell
Start-Process -FilePath "msiexec.exe" -Verb RunAs -Wait -ArgumentList @(
    "/i", $msi, "IMPORT_CERT=0", "/l*v", $logInstall
)
$LASTEXITCODE
```

Expected exit code: 0 or 3010.

Reboot the machine now.

#### Verify Installation (after reboot)

```shell Shell
Get-Item "C:\Windows\System32\AkeylessKsp.dll" | Select FullName,Length,LastWriteTime
Get-Item "C:\Program Files\Akeyless\Akeyless KSP\akeyless-ksp-cert-helper.exe" | Select FullName,Length,LastWriteTime

reg query "HKLM\SYSTEM\CurrentControlSet\Control\Cryptography\Providers\Akeyless KSP" /s
reg query "HKLM\SOFTWARE\Microsoft\Cryptography\Providers\Akeyless KSP" /s
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Cryptography\Configuration\Local\Default\00010001\KEY_STORAGE" /v Providers   # Contains Akeyless KSP

certutil -csplist | findstr /i "Akeyless"   # Shows "Provider Name: Akeyless KSP"
```

#### Sync Certificate and Test Signing

##### Run the Helper to Sync/Bind Certificate

```shell Shell
$helper = "C:\Program Files\Akeyless\Akeyless KSP\akeyless-ksp-cert-helper.exe"
& $helper --config-path "C:\Akeyless\conf\sqlcrypt.conf" sync-cert --store-scope machine --store-name My
"exit=$LASTEXITCODE"   # Should be 0
```

##### Find Your Certificate Thumbprint

```shell Shell
Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.HasPrivateKey } |
    Select-Object Subject, Thumbprint, NotAfter | Format-Table -Auto

# Example filter:
Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.Subject -like "*code.sign.example.com*" } |
    Select-Object Subject, Thumbprint, NotAfter | Format-Table -Auto
```

Set variable:

```shell Shell
$thumb = "YOUR_THUMBPRINT_HERE"
```

##### Confirm Binding

```shell Shell
(Get-Item "Cert:\LocalMachine\My\$thumb").HasPrivateKey
certutil -store -v My $thumb | findstr /i "Provider Container"
```

Expected: `Provider = Akeyless KSP`

##### Sign a Test File

```shell Shell
$file = "C:\Temp\hello.dll"   # Place a test DLL here
signtool sign /debug /v /sm /s My /sha1 $thumb /fd SHA256 `
    /tr "http://timestamp.digicert.com" /td SHA256 $file
"sign exit=$LASTEXITCODE"   # Should be 0
```

##### Validate Signature

```shell Shell
$sig = Get-AuthenticodeSignature $file
$sig.Status
$sig.SignerCertificate.Subject
$sig.SignerCertificate.Thumbprint
```

##### Verify Signature (with Trust)

```shell Shell
signtool verify /pa /v $file
```

If chain is not trusted, import your root CA into the machine's Trusted Root Certification Authorities store.
