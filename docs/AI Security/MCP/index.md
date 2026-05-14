---
title: MCP Server
excerpt: Overview of Akeyless MCP content, requirements, and supported integrations.
deprecated: false
hidden: false
link:
  new_tab: false
metadata:
  title: Akeyless MCP Server
  description: Overview of Akeyless MCP content, requirements, and supported integrations.
  robots: index
---
The Akeyless Model Context Protocol (MCP) Server lets MCP-enabled tools connect to your Akeyless identity security platform through the Akeyless CLI or Gateway. This section explains the MCP server, its command syntax, and the supported client integrations documented by Akeyless.

Model Context Protocol (MCP) is an open protocol that standardizes how an AI client discovers tools and sends tool calls to an external server. In this model, your MCP client (for example, Claude Desktop, Cursor, or GitHub Copilot) launches the Akeyless MCP server locally over `stdio`, then uses it to run authorized operations against Akeyless resources.

## Common Requirements

All documented MCP integrations share these requirements:

* Akeyless CLI version `1.130.0` or later.
* An Akeyless account and a configured CLI profile, or explicit authentication flags.
* A Gateway URL passed directly in the client configuration or command arguments.
* A client that can launch the Akeyless MCP server over `stdio`.

Read more about the [Model Context Protocol](https://modelcontextprotocol.io/).

## General MCP Usage Flow

Use this high-level flow for any supported MCP integration:

1. Install and configure the Akeyless CLI and authentication profile.
2. Configure your MCP client to run the Akeyless MCP server command.
3. Start or reload the MCP client so it discovers the Akeyless tools.
4. Invoke Akeyless tools from the client prompt and review the response.
5. Use RBAC and scoped secret permissions to control what the client can access.

## MCP-Related CLI Commands

The Akeyless CLI currently exposes two MCP-related commands:

| Command | Purpose |
| --- | --- |
| `akeyless mcp` | Starts the general Akeyless MCP server for standard Akeyless tools. |
| `akeyless mcp-runtime-authority` | Starts the Agentic Runtime Authority MCP server for runtime query workflows (`list-secrets`, `query-db`, `service-execute`). |

For full command flags and usage details, see [CLI Reference](https://docs.akeyless.io/docs/cli-reference#mcp).

### Command: akeyless mcp

The `akeyless mcp` command starts an MCP server so AI assistants can securely interact with Akeyless services through a standardized interface. It accepts the same authentication flags as other Akeyless CLI commands. For details, see [Access and Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods).

> Important: `akeyless mcp` does not use the `gateway_url` value configured in a CLI profile. You must pass `--gateway-url` directly in every `akeyless mcp` command (or MCP client args).

For full command syntax and flags, see [CLI Reference - mcp](https://docs.akeyless.io/docs/cli-reference#mcp).

### Command: akeyless mcp-runtime-authority

The `akeyless mcp-runtime-authority` command starts the MCP server for Agentic Runtime Authority runtime-query tools (`list-secrets`, `query-db`, `service-execute`). It uses the same authentication model as `akeyless mcp`, and accepts an optional `--secret-name` flag to set a default secret path for `query-db`.

For full command syntax and flags, see [CLI Reference - mcp-runtime-authority](https://docs.akeyless.io/docs/cli-reference#mcp-runtime-authority).

For Runtime Authority behavior, prerequisites, and tool semantics, see [Agentic Runtime Authority](https://docs.akeyless.io/docs/agentic-runtime-authority).

## Supported Integrations

| Integration | Primary use case | Configuration surface |
| --- | --- | --- |
| [Claude Desktop](https://docs.akeyless.io/docs/mcp-claude-desktop) | Desktop AI assistant workflow with local MCP client configuration | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| [Cursor](https://docs.akeyless.io/docs/mcp-cursor) | Editor-based MCP workflow in Cursor | `~/.cursor/mcp.json` or Cursor settings JSON |
| [GitHub Copilot](https://docs.akeyless.io/docs/mcp-github-copilot) | MCP workflow with GitHub Copilot CLI | `~/.copilot/mcp-config.json` |
| [JetBrains IDEs](https://docs.akeyless.io/docs/mcp-jetbrains-ides) | IDE-native plugin workflow for JetBrains products | JetBrains plugin settings |
