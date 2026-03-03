---
title: Windows Code Signing with Akeyless
deprecated: false
hidden: false
metadata:
  robots: index
---
This guide provides step-by-step instructions to set up code signing using Akeyless for PKI certificate issuance and the Akeyless Key Storage Provider (KSP) on Windows. It covers creating secrets, generating certificates, configuring the KSP, and troubleshooting.

## Prerequisites

* A Windows environment with `signtool` and `certutil` installed and available in `PATH`.
* A DLL artifact file to sign.
* Akeyless CLI installed and authenticated, with permission to create keys in your target folder.
* An API Key auth method for the SignTool plugin, with read permissions on your target folder.
* Administrator privileges on the Windows machine.
* Replace placeholder paths (for example, `/YourCompany/`) with your organization-specific paths.

### Expected Flow

* Use Akeyless CLI to generate a Certificate Signing Request (CSR) from a newly generated DFC (RSA) key.
* Issue the certificate from your CA with code-signing constraints.
* Use the issued certificate that is generated and stored by Akeyless under your issuer destination path, then sync it to the Windows Certificate Store through the Akeyless KSP helper.

### Suggested Environment Variables

```powershell
$env:msi = "C:\Path\To\AkeylessKspInstaller.msi"
$env:prov = "Akeyless KSP"
$env:helper = "C:\Program Files\Akeyless\Akeyless KSP\akeyless-ksp-cert-helper.exe"
$env:AKEYLESS_SQLCRYPT_CONFIG_PATH = "C:\Akeyless\conf\sqlcrypt.conf"
$env:configFile = $env:AKEYLESS_SQLCRYPT_CONFIG_PATH
$env:logInstall = "C:\Akeyless\logs\AkeylessKspInstall.log"
$env:logUninst = "C:\Akeyless\logs\AkeylessKspUninstall.log"
$env:file = "C:\Temp\test_app.dll"
$env:DLL_Signer_key = "/YourCompany/code-signing/root-key"
$env:Cert_Signer_Key = "/YourCompany/code-signing/signing-key"
$env:PKI_DLL_Issuer = "/YourCompany/code-signing/pki-issuer"
$env:Cert_destination_path = "/YourCompany/code-signing"
$env:Root_Key_Cert_Path = ".\\root-ca.pem"
$env:Common_Name = "code.sign.example.com"
$env:CSR_File = ".\\signing.csr"
$env:CERT_File = ".\\signing.pem"
```

## Part 1: Create Secrets and Issue Code-Signing Certificate

### Create Root Key for PKI Issuer

This key will sign the certificates issued by your internal CA.

```shell
akeyless create-dfc-key \
  --profile default \
  --name /YourCompany/code-signing/root-key \
  --alg RSA2048 \
  --split-level 3 \
  --certificate-common-name code.sign.example.com \
  --certificate-ttl 30 \
  --conf-file-path csr.conf \
  --generate-self-signed-certificate true
```

[Read more about the create-dfc-key command.](https://docs.akeyless.io/reference/createdfckey)

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

[Read more about Creating a Certificate Signing Request](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates?isFramePreview=true#creating-a-certificate-signing-request)

### Create PKI Certificate Issuer

This defines the policy for your internal CA.

```shell
akeyless create-pki-cert-issuer \
  --profile default \
  --name /YourCompany/code-signing/pki-issuer \
  --allowed-domains code.sign.example.com \
  --signer-key-name /YourCompany/code-signing/root-key \
  --code-signing-flag \
  --key-usage DigitalSignature \
  --critical-key-usage true \
  --ttl 600d \
  --destination-path /YourCompany/code-signing
```

[Read more about Creating a Certificate Issuer.](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates?isFramePreview=true#creating-a-certificate-issuer)

### Issue the 4096-bit Certificate

Sign the CSR generated in step 2.

```shell
akeyless get-pki-certificate \
  --profile default \
  --cert-issuer-name /YourCompany/code-signing/pki-issuer \
  --extended-key-usage codesigning \
  --csr-file-path signing.csr \
  > signing.pem
```

[Read more about Issuing a Certificate.](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates?isFramePreview=true#issuing-a-certificate)

## Part 2: Akeyless KSP Installation and Configuration

### Prepare Configuration File

Create a file named `sqlcrypt.conf` in a persistent location (`C:\Akeyless\conf\sqlcrypt.conf`).

```shell sqlcrypt.conf
akeyless_url = "https://gw-aws.lm.cs.akeyless.fans/api/v2"
base_item_path = "/YourCompany/"
log_level = "debug"
use_classic_keys = false

[ksp]
signing_key_item = "/YourCompany/code-signing/signing-key"
signing_cert_item = "/YourCompany/code-signing/code.sign.example.com"

[auth]
access_type = "access_key"
access_id = "YOUR_ACCESS_ID"
access_key = "YOUR_ACCESS_KEY"
```

Set `signing_cert_item` to the generated certificate item path.
By default, Akeyless stores issued certificates as:
`<destination-path>/<common-name>` (or `<destination-path>/<serial-number>` if Common Name is empty).

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

Reboot the machine now to register the provider. **Important:** After reboot, session-level PowerShell environment variables may no longer be set. Re-define them before continuing.

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
& $helper --config-path $env:AKEYLESS_SQLCRYPT_CONFIG_PATH sync-cert --dry-run

# If dry-run looks correct, sync to LocalMachine\My
& $helper --config-path $env:AKEYLESS_SQLCRYPT_CONFIG_PATH sync-cert --store-scope machine --store-name My
```

### Verify Binding

Ensure the certificate is present and linked to "Akeyless KSP".

```shell
$thumb = (
  Get-ChildItem Cert:\LocalMachine\My |
  Where-Object { $_.Subject -like "*code.sign.example.com*" -and $_.HasPrivateKey } |
  Sort-Object NotAfter |
  Select-Object -Last 1 -ExpandProperty Thumbprint
)
certutil -store -v My $thumb | findstr /i "Provider Container"
# Expected Output: Provider = Akeyless KSP
```

### Sign a Test File

```shell
$file = "C:\Temp\test_app.dll"
signtool sign /debug /v /sm /s My /sha1 $thumb /fd SHA256 /tr "http://timestamp.digicert.com" /td SHA256 $file
```

### Establish Trust (Import Root CA)

If `signtool verify` fails because the chain is untrusted, you must import the Root CA used in Part 1.

Step A: Retrieve the Root CA certificate.

```shell
$rootCertRaw = (akeyless describe-item --name /YourCompany/code-signing/root-key --json | ConvertFrom-Json).certificates
try {
  [System.IO.File]::WriteAllBytes(".\root-ca.pem", [System.Convert]::FromBase64String($rootCertRaw))
} catch {
  $rootCertRaw | Out-File -Encoding ascii .\root-ca.pem
}
```

Optional validation:

```shell
certutil -dump .\root-ca.pem
```

Step B: Import into Trusted Root Store.

```shell
certutil -addstore -f "Root" .\root-ca.pem
```

Step C: Verify Chain

```shell
Get-AuthenticodeSignature $file
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
$uninstRoots = @(
  "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
  "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
)

$app = Get-ChildItem $uninstRoots | 
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
