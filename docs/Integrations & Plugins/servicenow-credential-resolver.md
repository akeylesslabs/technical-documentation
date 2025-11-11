---
title: ServiceNow Credential Resolver
excerpt: >-
  A ServiceNow MID external credential resolver that retrieves secrets from
  Akeyless and maps them to ServiceNow Discovery credential fields.
deprecated: false
hidden: true
link:
  new_tab: false
metadata:
  robots: index
---
# Overview

The ServiceNow Credential Resolver is a MID external credential resolver that securely retrieves secrets from Akeyless and maps them to ServiceNow Discovery credential fields. The resolver integrates seamlessly with ServiceNow's Discovery process using the `com.snc.discovery.CredentialResolver` class.

## Features

- **Secure credential retrieval** from Akeyless vault
- **Multiple authentication methods** supported (Access Key, AWS IAM, Azure AD, GCP)
- **Seamless ServiceNow integration** with Discovery and External Credentials
- **Cloud-native support** with automatic CloudID detection

## Prerequisites

Before implementing the ServiceNow Credential Resolver, ensure you have the following:

### ServiceNow Requirements

- ServiceNow instance (Quebec+ recommended)
- Discovery module enabled
- External Credentials feature enabled
- MID Server installed and connected to your instance

### Network Requirements

- Network access from the MID Server host to the Akeyless Gateway
- Default gateway: `https://api.akeyless.io` (or your private gateway URL)

### Akeyless Requirements

- Valid Akeyless Access ID
- One of the supported authentication methods (see below)

## Supported Authentication Methods

The resolver supports multiple Akeyless authentication methods:

<Accordion title="Access Key Authentication" icon="key">

**Method:** `access_key`

**Requirements:**
- Access ID
- Access Key

**Best for:** Local development and testing environments
</Accordion>

<Accordion title="AWS IAM Authentication" icon="aws">

**Method:** `aws_iam`

**Requirements:**
- CloudID from AWS
- EC2 instance with appropriate IAM role/instance profile

**Best for:** MID Servers running on AWS EC2 instances
</Accordion>

<Accordion title="Azure AD Authentication" icon="microsoft">

**Method:** `azure_ad`

**Requirements:**
- CloudID from Azure
- Azure VM with managed identity

**Best for:** MID Servers running on Azure Virtual Machines
</Accordion>

<Accordion title="GCP Authentication" icon="google">

**Method:** `gcp`

**Requirements:**
- CloudID from GCP
- GCP VM with default service account credentials

**Best for:** MID Servers running on Google Cloud Platform
</Accordion>

> **Note:** For cloud-based authentication methods, the resolver automatically detects CloudID using the cloud environment. Ensure your MID Server is running in an environment where CloudID can be obtained. For local development, use the `access_key` method.

## Building the Project

This is a Maven-based project. Follow these steps to build a versioned JAR with a stable filename for MID Server deployment:

```bash
# Clone the repository
git clone <repository-url>
cd servicenow-credential-resolver

# Build the project
mvn clean package

# The JAR will be generated in the target/ directory
```

The build process creates a versioned JAR file that maintains filename stability for consistent MID Server integration.

## Next Steps

1. **[Installation & Configuration](link-to-installation)** - Deploy the resolver to your MID Server
2. **[Authentication Setup](link-to-auth-setup)** - Configure your preferred authentication method  
3. **[Testing & Validation](link-to-testing)** - Verify the resolver is working correctly
4. **[Troubleshooting](link-to-troubleshooting)** - Common issues and solutions