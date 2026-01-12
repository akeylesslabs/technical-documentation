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

<br />
