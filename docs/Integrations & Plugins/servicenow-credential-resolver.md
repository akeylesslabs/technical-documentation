---
title: ServiceNow Credential Resolver
deprecated: false
hidden: true
link:
  new_tab: false
metadata:
  robots: index
---
<br />

### Overview

This project provides a ServiceNow MID external credential resolver that retrieves secrets from Akeyless and maps them to ServiceNow Discovery credential fields. The resolver class is com.snc.discovery.CredentialResolver.

### Prerequisites

* ServiceNow instance (Quebec+ recommended) with Discovery and External Credentials enabled.
* MID Server installed and connected to your instance.
* Network access from the MID Server host to the Akeyless Gateway (default [https://api.akeyless.io](https://api.akeyless.io), or your private gateway URL).
* An Akeyless Access ID and one of the supported authentication methods listed below.

### Supported Akeyless authentication methods

* access_key: Access ID + Access Key
* aws_iam: CloudID from AWS
* azure_ad: CloudID from Azure
* gcp: CloudID from GCP

For cloud-based methods, the resolver detects CloudID using the cloud environment. Ensure the MID Server is running where a CloudID can be obtained (e.g., EC2 with an instance profile, Azure VM with a managed identity, GCP VM with default credentials). For local/dev use, prefer access_key.

### Build the JAR

This is a Maven project. Build a versioned JAR so the filename is stable in MID:

```shell Get-Dynamic-Secret
mvn -Drevision=1.0.0 clean package
```

**Artifacts:**

* With -Drevision=1.0.0: target/akeyless-servicenow-credential-resolver-1.0.0.jar
* Without a revision property, Maven will produce akeyless-servicenow-credential-resolver-null.jar.

### Install the resolver on the MID Server


1. Upload the JAR to the MID Server via the instance UI
   * Navigate: MID Server → JAR files → New
   * Set a descriptive Name (e.g., akeyless-servicenow-credential-resolver)
   * Manage Attachments → upload the built JAR from target/
   * Submit
2. Ensure the MID downloads the JAR

* The MID will sync and place the JAR in its agent lib cache.
* If not picked up, restart the MID service to force a sync.

<br />
