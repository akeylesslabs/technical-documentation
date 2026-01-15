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

<br />
