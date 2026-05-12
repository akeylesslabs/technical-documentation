---
title: Cursor
slug: mcp-cursor
excerpt: Connect Cursor to the Akeyless MCP Server.
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
Connect Cursor to the Akeyless MCP Server when you want MCP access inside the Cursor editor.

For general MCP background and command syntax, see [MCP Server](https://docs.akeyless.io/docs/mcp-server).

## Requirements

* Akeyless CLI version `1.130.0` or later.
* A configured Akeyless profile, or the authentication values required by your chosen access type.
* A Gateway URL passed directly in the client configuration.

## Configure Cursor

1. Install and configure the Akeyless CLI.
2. Open Cursor settings JSON.
3. Add the Akeyless MCP server configuration.
4. Restart Cursor.

The following examples show common authentication configurations:

```json Default
{
  "mcp.servers": {
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
  "mcp.servers": {
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
  "mcp.servers": {
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

After Cursor restarts, verify that Cursor can run MCP-backed requests such as:

* "Show me my Akeyless secrets"
* "Create a new secret called `api-key`"
* "List all my targets"

## Notes

* The Akeyless CLI serves MCP over `stdio`, so Cursor must invoke the `akeyless mcp` command directly.
* When `--profile` is used, the saved CLI profile supplies the authentication settings.
* Pass `--gateway-url` directly in the Cursor configuration even when the profile already has a saved Gateway value.
