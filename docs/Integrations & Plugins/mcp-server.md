---
title: MCP Server
deprecated: false
hidden: true
metadata:
  robots: index
---
#### Overview

The Akeyless MCP (Model Context Protocol) Server is a powerful integration that allows AI assistants and applications to securely interact with your Akeyless secrets management platform. It provides a standardized interface for AI models to access, manage, and manipulate secrets, keys, certificates, and other sensitive data stored in Akeyless.

#### What is MCP?

Model Context Protocol (MCP) is a standardized protocol that enables AI assistants to securely connect to external data sources and services. It provides a secure, authenticated way for AI models to:

* Access external APIs and services
* Retrieve and manage sensitive data
* Perform operations on behalf of users
* Maintain security boundaries and access controls

#### Akeyless MCP Server Features

The Akeyless MCP server provides comprehensive access to Akeyless functionality including:

**Core Capabilities**

* Secrets Management: Create, read, update, and delete static secrets
* Key Management: Generate, rotate, and manage encryption keys
* Certificate Management: Issue, renew, and manage PKI and SSH certificates
* Dynamic Secrets: Generate temporary credentials for databases and cloud services
* Access Control: Manage roles, permissions, and authentication methods
* Analytics: Retrieve usage analytics and audit data

**Supported Operations**

* List and describe items (secrets, keys, certificates)
* Create and update secrets
* Generate dynamic secrets
* Manage authentication methods and roles
* Retrieve analytics data
* Handle targets and associations

#### Installation Guide

**Prerequisites**

* macOS, Linux, or Windows operating system
* Internet connection for downloading and updates
* Akeyless account (free tier available)

**Step 1: Download Akeyless CLI**

```shell Linux-AMD
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-linux-amd64
chmod +x akeyless
./akeyless
```
```shell Linux-ARM
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-linux-arm64
chmod +x akeyless
./akeyless
```
```shell Mac Intel
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-darwin-amd64
chmod +x akeyless
./akeyless
```
```shell Mac Apple Silicon
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/cli-darwin-arm64
chmod +x akeyless
./akeyless
```
```powershell Windows
curl -o akeyless.exe https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-windows-amd64.exe
.\akeyless.exe
```

**Step 2: Verify Installation**

```shell CLI
# Check version
akeyless --version

# Verify MCP command is available
akeyless mcp --help
```

**Step 3: Update CLI (if needed)**

```shell CLI
# Update to latest version
akeyless update
```

**Configuration and Setup**

MCP Server Configuration
The Akeyless MCP server is configured through your MCP client configuration file (typically `~/.cursor/mcp.json` for Cursor IDE).

**Basic Configuration Structure**

```json JSON
{
  "mcpServers": {
    "akeyless": {
      "command": "/path/to/akeyless",
      "args": [
        "mcp",
        "--access-id", "your-access-id",
        "--access-key", "your-access-key",
        "--access-type", "access_key",
        "--gateway-url", "https://api.akeyless.io"
      ],
      "env": {}
    }
  }
}
```

**Configuration Parameters**

* command – Path to Akeyless CLI binary
  Required: Yes | Default: –
* --access-id – Your Akeyless access ID
  Required: Yes | Default: –
* --access-key – Your Akeyless access key
  Required: Yes* | Default: –
* --access-type – Authentication method
  Required: Yes | Default: access_key
* --gateway-url – Akeyless gateway URL
  Required: No | Default: [https://api.akeyless.io](https://api.akeyless.io)
* --profile – CLI profile name
  Required: No | Default: default
* --debug – Enable debug logging
  Required: No | Default: false

**Authentication Methods**
Akeyless MCP server supports multiple authentication methods:

1. Access Key Authentication (Default)

```json JSON
{
  "args": [
    "mcp",
    "--access-id", "p-xxxxxxxxxxxxx",
    "--access-key", "your-access-key",
    "--access-type", "access_key"
  ]
}
```

2. Password Authentication

```json JSON
{
  "args": [
    "mcp",
    "--admin-email", "user@example.com",
    "--admin-password", "your-password",
    "--access-type", "password"
  ]
}
```

3. SAML Authentication

```json JSON
{
  "args": [
    "mcp",
    "--access-type", "saml",
    "--gateway-url", "https://your-gateway.com"
  ]
}
```

4. OIDC/JWT Authentication

```json JSON
{
  "args": [
    "mcp",
    "--access-type", "oidc",
    "--jwt", "your-jwt-token",
    "--gateway-url", "https://your-gateway.com"
  ]
}
```

5. Kubernetes Authentication

```json JSON
{
  "args": [
    "mcp",
    "--access-type", "aws_iam",
    "--cloud-id", "your-aws-role-arn"
  ]
}
```

6. Cloud Provider Authentication
   1. AWS IAM:
   <br />
   ```json JSON
   {
     "args": [
       "mcp",
       "--access-type", "aws_iam",
       "--cloud-id", "your-aws-role-arn"
     ]
   }
   ```
   1. Azure AD:
   <br />
   ```json JSON
   {
     "args": [
       "mcp",
       "--access-type", "azure_ad",
       "--cloud-id", "your-azure-client-id"
     ]
   }
   ```
   1. Google Cloud:
   <br />
   ```json JSON
   {
     "args": [
       "mcp",
       "--access-type", "gcp",
       "--cloud-id", "your-gcp-service-account"
     ]
   }
   ```

<br />

7. Certificate Authentication

```json JSON
{
  "args": [
    "mcp",
    "--access-type", "cert",
    "--cert-file-name", "/path/to/cert.pem",
    "--key-file-name", "/path/to/key.pem"
  ]
}
```

8. LDAP Authentication

```json JSON
{
  "args": [
    "mcp",
    "--access-type", "ldap",
    "--ldap_proxy_url", "ldap://your-ldap-server",
    "--username", "your-username",
    "--password", "your-password"
  ]
}
```
