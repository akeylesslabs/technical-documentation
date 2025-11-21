---
title: Akeyless MCP Server
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
The akeyless mcp command starts an MCP server that enables AI assistants such as Cursor and GitHub Copilot to securely interact with Akeyless services through a standardized interface.

### What is MCP?

Model Context Protocol (MCP) is an open standard that allows AI assistants to securely access external data sources and tools.

### With MCP, you can:

* Safely authenticate AI assistants with Akeyless
* Interact with Akeyless secrets, targets, and other resources
* Leverage existing profiles and authentication methods
* Connect to Akeyless Gateway instances

### Features

* Secure Authentication – Uses Akeyless authentication mechanisms
* Tool Integration – Access Akeyless secrets, targets, RBAC, and more
* Profile Support – Works with your existing Akeyless CLI profiles
* Gateway Integration – Supports both local and cloud Akeyless Gateways

### Usage

#### Basic Commands

```shell
# Start MCP server with access key authentication
akeyless mcp --access-id <your-access-id> --access-key <your-access-key> --access-type access_key --gateway-url https://api.akeyless.io

# Start MCP server with SAML authentication
akeyless mcp --access-id <your-access-id> --access-type saml --gateway-url https://api.akeyless.io

# Start MCP server with a profile
akeyless mcp --profile <profile-name> --gateway-url https://api.akeyless.io
```

#### Supported Authentication Methods

```shell
--access-type [=access_key]  
(access_key / password / saml / ldap / k8s / azure_ad / oidc / aws_iam / universal_identity / jwt / gcp / cert / oci / kerberos)
```

The MCP command accepts the same authentication parameters as standard Akeyless CLI auth commands.\
For more details, see [Akeyless Authentication Documentation](https://docs.akeyless.io/docs/access-and-authentication-methods)

### Common Parameters

\--access-id: Your Akeyless Access ID

\--access-key: Your Akeyless Access Key (for access\_key auth)

\--access-type: Authentication method (see list above)

\--gateway-url: Gateway URL (default: http\://localhost:8080/v2)

\--profile: Use an existing CLI profile

### Setting up MCP with Cursor

1. Install Akeyless CLI\
   Ensure the Akeyless CLI is installed and configured.
2. Update Cursor Settings\
   Open settings (Cmd/Ctrl + Shift + P → Preferences: Open Settings (JSON)) and add:

```yaml
{
  "mcp.servers": {
    "akeyless": {
      "command": "akeyless",
      "args": ["mcp", "--profile", "your-profile-name", "--gateway-url", "https://api.akeyless.io"]
    },
    "akeyless-saml": {
      "command": "akeyless",
      "args": ["mcp", "--access-id", "your-access-id", "--access-type", "saml", "--gateway-url", "https://api.akeyless.io"]
    },
    "akeyless-oidc": {
      "command": "akeyless",
      "args": ["mcp", "--access-id", "your-access-id", "--access-type", "oidc", "--gateway-url", "https://api.akeyless.io"]
    }
  }
}
```

<br />

3. Restart Cursor\
   Restart for the changes to take effect.
4. Verify\
   You can now run queries such as:

* “Show me my Akeyless secrets”
* “Create a new secret called api-key”
* “List all my targets”

### Setting up MCP with GitHub Copilot

1. Install Copilot CLI

```shell
npm install -g @githubnext/github-copilot-cli
```

2. Configure Copilot

Edit \~/.copilot/config.yml to include:

```yaml
mcpServers:
  akeyless:
    command: akeyless
    args: ["mcp", "--profile", "your-profile-name", "--gateway-url", "https://api.akeyless.io"]
  akeyless-saml:
    command: akeyless
    args: ["mcp", "--access-id", "your-access-id", "--access-type", "saml", "--gateway-url", "https://api.akeyless.io"]
  akeyless-oidc:
    command: akeyless
    args: ["mcp", "--access-id", "your-access-id", "--access-type", "oidc", "--gateway-url", "https://api.akeyless.io"]
```

3. Start Copilot with MCP

```shell
copilot mcp
```

4. Use Copilot\
   You can now manage secrets, configure targets, and perform infrastructure tasks via Copilot.

### Examples

#### Secret Operations

```shell
# Start MCP server
akeyless mcp --profile production --gateway-url https://api.akeyless.io

# In Cursor/Copilot
# "Create a secret called 'database-password' with value 'secure123'"
# "Show me all secrets in the /prod/ path"
```

#### Target Management

```shell
# "List all my AWS targets"
# "Update the SSH target with new credentials"
```

#### Production Setup

```shell
# Production
akeyless mcp --profile prod --gateway-url https://api.akeyless.io

# Development / Testing
akeyless mcp --profile dev --gateway-url http://localhost:8080/v2
```