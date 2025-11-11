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

```shell
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

### Configure MID properties (Akeyless parameters)

Set the following MID properties on your instance (System Properties or MID Properties). Property names are case-sensitive.

* ext.cred.akeyless.gw_url (string): Akeyless Gateway. Default: [https://api.akeyless.io](https://api.akeyless.io)
* ext.cred.akeyless.access_type (string): One of access_key, aws_iam, azure_ad, gcp. Default: access_key
* ext.cred.akeyless.access_id (string): Your Akeyless Access ID (required)
* ext.cred.akeyless.access_key (string): Your Akeyless Access Key (required for access_key only)

Optional field mapping overrides for JSON secrets (see Mapping section below):

* ext.cred.akeyless.map.username (default: username)
* ext.cred.akeyless.map.password (default: password)
* ext.cred.akeyless.map.private_key (default: private_key)
* ext.cred.akeyless.map.passphrase (default: passphrase)

Environment/system property alternatives

* The resolver also supports the following system properties or environment variables:
  * AKEYLESS_GW_URL
  * AKEYLESS_ACCESS_TYPE
  * AKEYLESS_ACCESS_ID (required)
  * AKEYLESS_ACCESS_KEY (when using access_key)
* As a fallback for any ext.cred.* property, an environment variable with the uppercased name and dots replaced by underscores is also read (e.g., EXT_CRED_AKEYLESS_GW_URL).
* Precedence: MID properties override environment/system variables.

### Configure MID config.xml (secure local parameters)


Add sensitive Akeyless credentials in the MID’s config.xml.

Edit the file on each MID host:

* Linux: /opt/agent/config.xml
* Windows: C:\ServiceNow\agent\config.xml

Insert your parameters inside the `<parameters> `block:

```shell
<parameters>
    ...
    <!-- Akeyless secure credentials -->
    <parameter name="ext.cred.akeyless.gw_url" value="https://api.akeyless.io" />
    <parameter name="ext.cred.akeyless.access_type" value="access_key" />
    <parameter name="ext.cred.akeyless.access_id" value="AKEYLESS_ACCESS_ID" />
    <parameter name="ext.cred.akeyless.access_key" value="AKEYLESS_SECRET_KEY" secure="true" />

    <!-- Optional JSON mapping overrides -->
    <parameter name="ext.cred.akeyless.map.username" value="username" />
    <parameter name="ext.cred.akeyless.map.password" value="password" />
    <parameter name="ext.cred.akeyless.map.private_key" value="private_key" />
    <parameter name="ext.cred.akeyless.map.passphrase" value="passphrase" />
</parameters>
```

<br />
