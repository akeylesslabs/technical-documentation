---
title: MCPs
excerpt: Links to Akeyless MCP documentation
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
## Model Context Protocol (MCP)

Model Context Protocol (MCP) is an open protocol that lets AI clients connect to external tool servers through a standard interface. With Akeyless MCP, your client starts an Akeyless MCP server process and uses it to run authorized operations against your Akeyless identity security platform.

General usage flow:

1. Configure the Akeyless CLI and authentication profile.
2. Configure your MCP client to launch the Akeyless MCP server command.
3. Reload the MCP client and invoke Akeyless tools from your prompt.

Use MCP documentation in this order:

1. Start with [Akeyless MCP Server](https://docs.akeyless.io/docs/mcp-server) for the general model, requirements, and usage flow.
2. Open your integration-specific page for client setup details.

Integration guides:

* [Claude Desktop Integration](https://docs.akeyless.io/docs/mcp-claude-desktop)
* [Cursor Integration](https://docs.akeyless.io/docs/mcp-cursor)
* [GitHub Copilot Integration](https://docs.akeyless.io/docs/mcp-github-copilot)
* [JetBrains IDEs Integration](https://docs.akeyless.io/docs/mcp-jetbrains-ides)

If you use Cursor, see [Akeyless Secrets Manager for Cursor](https://docs.akeyless.io/docs/cursor-akeyless-secrets-manager) for the separate secret-scanning extension.
