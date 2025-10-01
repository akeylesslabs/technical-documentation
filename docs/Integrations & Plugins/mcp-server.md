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

<br />
