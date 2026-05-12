---
title: Claude Desktop
slug: mcp-claude-desktop
excerpt: Connect Claude Desktop to the Akeyless MCP Server.
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
Connect Claude Desktop to the Akeyless MCP Server when you want Claude Desktop to access Akeyless tools through MCP.

For general MCP background and command syntax, see [MCP Server](https://docs.akeyless.io/docs/mcp-server).

## Requirements

* Akeyless CLI version `1.130.0` or later.
* A configured Akeyless profile, or the authentication values required by your chosen access type.
* A Gateway URL passed directly in the client configuration.

## Configure Claude Desktop

1. Install and configure the Akeyless CLI.
2. Edit `~/Library/"Application Support"/Claude/claude_desktop_config.json`.
3. Add the Akeyless MCP server configuration.
4. Restart Claude Desktop.

Use one of the following examples:

```json Default
{
  "mcpServers": {
    "akeyless": {
      "command": "akeyless",
      "args": [
        "mcp",
        "--profile", "<profile-name>",
        "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
      ]
    }
  }
}
```
```json SAML
{
  "mcpServers": {
    "akeyless-saml": {
      "command": "akeyless",
      "args": [
        "mcp",
        "--access-id", "<access-id>",
        "--access-type", "saml",
        "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
      ]
    }
  }
}
```
```json OIDC
{
  "mcpServers": {
    "akeyless-oidc": {
      "command": "akeyless",
      "args": [
        "mcp",
        "--access-id", "<access-id>",
        "--access-type", "oidc",
        "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
      ]
    }
  }
}
```

## Verify The Integration

After Claude Desktop restarts, verify that Claude can run MCP-backed requests such as:

* "Show me my Akeyless secrets"
* "List all my targets"
* "Create a new secret called `api-key`"

## Notes

* The Akeyless CLI serves MCP over `stdio`, so Claude Desktop must invoke the `akeyless mcp` command directly.
* When `--profile` is used, the saved CLI profile supplies the authentication settings.
* Pass `--gateway-url` directly in the Claude Desktop configuration even when the profile already has a saved Gateway value.
