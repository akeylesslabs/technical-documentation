---
title: CLI Reference - MCP Server
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
The `akeyless mcp` command starts an MCP server that enables AI assistants such as Cursor and GitHub Copilot to securely interact with Akeyless services through a standardized interface.

If you use JetBrains IDEs, see the <Anchor label="Akeyless MCP Plugin for JetBrains IDEs" href="doc:akeyless-mcp-plugin-jetbrains-ides" /> page for the IDE-specific setup flow.

## What Is MCP?

Model Context Protocol (MCP) is an open standard that allows AI assistants to securely access external data sources and tools.

## With MCP, You Can

* Safely authenticate AI assistants with Akeyless
* Interact with Akeyless secrets, targets, and other resources
* Leverage existing profiles and authentication methods
* Connect to Akeyless Gateway instances

## Features

* Secure Authentication – Uses Akeyless authentication mechanisms
* Tool Integration – Access Akeyless secrets, targets, RBAC, and more
* Profile Support – Uses your existing Akeyless CLI profiles for authentication context
* Gateway Integration – Supports both local and cloud Akeyless Gateways

## Usage

> Important: `akeyless mcp` does not use the `gateway_url` value configured in a CLI profile. You must pass `--gateway-url` directly in every `akeyless mcp` command (or MCP client args).

### Basic Commands

```shell
# Start MCP server with access key authentication
akeyless mcp --access-id <your-access-id> --access-key <your-access-key> --access-type access_key --gateway-url https://<your-gateway-url>:8000/api/v2

# Start MCP server with SAML authentication
akeyless mcp --access-id <your-access-id> --access-type saml --gateway-url https://<your-gateway-url>:8000/api/v2
```

### Supported Authentication Methods

```shell
--access-type [=access_key]  
(access_key / password / saml / ldap / k8s / azure_ad / oidc / aws_iam / universal_identity / jwt / gcp / cert / oci / kerberos)
```

The `mcp` command accepts the same authentication parameters as standard Akeyless CLI auth commands. For more details, see [Akeyless Authentication Documentation](https://docs.akeyless.io/docs/access-and-authentication-methods)

## Common Parameters

`--access-id`: Your Akeyless Access ID

`--access-key`: Your Akeyless Access Key (for `access_key` auth)

`--access-type`: Authentication method (see list above)

`--gateway-url`: Gateway URL (required for `akeyless mcp`; must be supplied in-line)

`--profile`: Use an existing CLI profile

## Setting Up MCP With Cursor

1. Install Akeyless CLI:
    Ensure the Akeyless CLI is installed and configured.

2. Update Cursor Settings:
    Open settings (Cmd/Ctrl + Shift + P → Preferences: Open Settings (JSON)) and add:

    ```json
    {
      "mcp.servers": {
        "akeyless": {
          "command": "akeyless",
          "args": ["mcp", "--profile", "your-profile-name", "--gateway-url", "https://<your-gateway-url>:8000/api/v2"]
        },
        "akeyless-saml": {
          "command": "akeyless",
          "args": ["mcp", "--access-id", "your-access-id", "--access-type", "saml", "--gateway-url", "https://<your-gateway-url>:8000/api/v2"]
        },
        "akeyless-oidc": {
          "command": "akeyless",
          "args": ["mcp", "--access-id", "your-access-id", "--access-type", "oidc", "--gateway-url", "https://<your-gateway-url>:8000/api/v2"]
        }
      }
    }
    ```

3. Restart Cursor for the changes to take effect.

4. Verify that you can now run queries such as:

    * “Show me my Akeyless secrets”
    * “Create a new secret called `api-key`”
    * “List all my targets”

## Setting Up MCP With GitHub Copilot

1. Install Copilot CLI

    ```shell
    npm install -g @githubnext/github-copilot-cli
    ```

2. Configure Copilot

    Edit `~/.copilot/config.yml` to include:

    ```yaml
    mcpServers:
      akeyless:
        command: akeyless
        args: ["mcp", "--profile", "your-profile-name", "--gateway-url", "https://<your-gateway-url>:8000/api/v2"]
      akeyless-saml:
        command: akeyless
        args: ["mcp", "--access-id", "your-access-id", "--access-type", "saml", "--gateway-url", "https://<your-gateway-url>:8000/api/v2"]
      akeyless-oidc:
        command: akeyless
        args: ["mcp", "--access-id", "your-access-id", "--access-type", "oidc", "--gateway-url", "https://<your-gateway-url>:8000/api/v2"]
    ```

3. Start Copilot with MCP

    ```shell
    copilot mcp
    ```

4. Use Copilot

  You can now manage secrets, configure targets, and perform infrastructure tasks through Copilot.

## Examples

### Secret Operations

```shell
# Start MCP server
akeyless mcp --profile production --gateway-url https://<your-gateway-url>:8000/api/v2

# In Cursor/Copilot
# "Create a secret called 'database-password' with value 'secure123'"
# "Show me all secrets in the /prod/ path"
```

### Target Management

```shell
# "List all my AWS targets"
# "Update the SSH target with new credentials"
```

### Production Setup

```shell
# Production
akeyless mcp --profile prod --gateway-url https://<your-gateway-url>:8000/api/v2

# Development / Testing
akeyless mcp --profile dev --gateway-url https://<your-gateway-url>:8000/api/v2
```
