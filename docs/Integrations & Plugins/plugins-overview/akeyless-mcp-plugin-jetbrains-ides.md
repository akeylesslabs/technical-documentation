---
title: Akeyless MCP Plugin for JetBrains IDEs
excerpt: Integrate Akeyless secrets management directly into JetBrains IDEs with MCP
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Integrate Akeyless secrets management directly into your JetBrains IDE through the Model Context Protocol (MCP). Browse, create, and manage secrets, keys, certificates, and other Akeyless resources without leaving your IDE.

See also: <Anchor label="MCP Server" href="doc:mcp-server" />.

Source repository: [https://github.com/akeyless-community/akeyless-mcp-plugin](https://github.com/akeyless-community/akeyless-mcp-plugin).

## Features

* Hierarchical Tree View: Browse Akeyless items in a folder tree structure
* Item Details: View full details and metadata for any selected item
* Create Secrets: Create new secrets directly from the IDE
* Query Interface: Use natural language queries (for example, "List all secrets")
* MCP Tools: Access 17+ Akeyless MCP tools directly from the IDE
* Real-time Refresh: Refresh the items list with one click
* Secure Authentication: Supports Akeyless CLI profiles, including SAML and other authentication methods

## Requirements

* JetBrains IDE (IntelliJ IDEA, PyCharm, WebStorm, and others) version `2023.2` or higher
* Akeyless CLI installed and configured
* Node.js installed (if using `npx` to run the MCP server)
* A valid Akeyless account

## Getting Started

### Step 1: Install the Akeyless CLI

Using package managers (recommended):

```shell macOS (Homebrew)
brew install akeylesslabs/tap/akeyless
```
```shell Linux (apt)
apt-get install -y akeyless
```
```shell Linux (yum/dnf)
yum install -y akeyless
# or
dnf install -y akeyless
```

Direct download options:

```shell macOS Intel
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-darwin-amd64
```
```shell macOS Apple Silicon
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/cli-darwin-arm64
```
```shell Linux AMD64
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-linux-amd64
```
```shell Linux ARM64
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-linux-arm64
```
```powershell Windows
curl -o akeyless.exe https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-windows-amd64.exe
```

After downloading:

```shell Linux and macOS
chmod +x akeyless
./akeyless
```
```powershell Windows
.\akeyless.exe
```

For complete installation details, see [Akeyless CLI documentation](https://docs.akeyless.io/docs/cli).

### Step 2: Configure Your Akeyless Profile

The Akeyless CLI supports multiple authentication methods, including:

`access_key`, `saml`, `oidc`, `aws_iam`, `azure_ad`, `gcp`, `ldap`, `k8s`, `cert`, and more.

Examples:

```shell API Key
akeyless configure --profile default --access-id p-xxxx --access-key xxxx --access-type access_key
```
```shell SAML
akeyless configure --profile saml --access-id p-xxxx --access-type saml
```

For profile details and advanced options, see [CLI Profiles](https://docs.akeyless.io/docs/cli-profiles).

### Step 3: Install the Plugin

1. Open your JetBrains IDE (`2023.2+`).
2. Go to **Settings → Plugins → Marketplace**.
3. Search for **Akeyless MCP**.
4. Select **Install**.
5. Restart the IDE when prompted.

### Step 4: Configure the Plugin

Navigate to **Settings → Tools → Akeyless MCP**.

Configuration fields:

* **Server Command**

  Enter the command that starts the Akeyless MCP server. For example:

  ```text
  npx -y @akeyless/cli-mcp
  ```

* **Working Directory**

  Optional. If empty, the plugin uses the current project directory.

* **Akeyless Profile**

  Optional. Enter the Akeyless CLI profile name to use for authentication. If this field is empty, the plugin uses the default profile.

* **Auto-connect on IDE startup**

  Automatically connects to the MCP server when the IDE starts.

### Step 5: Use the Plugin

Open **View → Tool Windows → Akeyless MCP**.

Tabs:

* **Secrets Tab**: Browse secrets, keys, and certificates in a hierarchical tree
* **Query MCP Tab**: Run natural language queries
* **MCP Tools Tab**: Access and execute Akeyless MCP tools

Toolbar options:

* Refresh items list
* Create new secret
* Open settings

## MCP Server Details

The plugin connects to the Akeyless MCP server using `stdio` transport.

Communication uses JSON-RPC over `stdio`.

Authentication is handled by the Akeyless CLI using configured profiles or environment variables.
