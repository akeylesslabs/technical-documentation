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
## Overview

The Akeyless Model Context Protocol (MCP) Server lets MCP-enabled tools connect to your Akeyless identity security platform through the Akeyless CLI. This section explains the MCP server, its command syntax, and the supported client integrations documented by Akeyless.

Model Context Protocol (MCP) is an open protocol that standardizes how an AI client discovers tools and sends tool calls to an external server. In this model, your MCP client (for example, Claude Desktop, Cursor, or GitHub Copilot) launches the Akeyless MCP server locally over `stdio`, then uses it to run authorized operations against Akeyless resources.

## What This Section Covers

Use the pages in this section for the following goals:

* Understand what the Akeyless MCP Server does and when to use it.
* Configure a supported MCP client integration.
* Review the `akeyless mcp` command syntax and authentication options.
* Follow the JetBrains IDE plugin flow when you need an IDE-native integration.

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

## Command: akeyless mcp

The `akeyless mcp` command starts an MCP server so AI assistants can securely interact with Akeyless services through a standardized interface.

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

The `mcp` command accepts the same authentication parameters as standard Akeyless CLI auth commands. For details, see [Access and Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods).

### Common Parameters

* `--access-id`: Your Akeyless Access ID.
* `--access-key`: Your Akeyless Access Key (for `access_key` auth).
* `--access-type`: Authentication method.
* `--gateway-url`: Gateway URL (required for `akeyless mcp`; must be supplied in-line).
* `--profile`: Use an existing CLI profile.

### Examples

```shell
# Production
akeyless mcp --profile prod --gateway-url https://<your-gateway-url>:8000/api/v2

# Development / Testing
akeyless mcp --profile dev --gateway-url https://<your-gateway-url>:8000/api/v2
```

## Command: akeyless mcp-runtime-authority

The `akeyless mcp-runtime-authority` command starts the MCP server for Agentic Runtime Authority runtime-query tools.

### Runtime Authority Parameters

* `--gateway-url`: Gateway URL (required).
* `--profile`: Use an existing CLI profile.
* `--secret-name`: Optional default secret path for `query-db`. If omitted, the client must provide `secret-name` in tool calls.
* Authentication flags: Same auth model as `akeyless mcp`.

### Runtime Authority Example

```shell
akeyless mcp-runtime-authority \
  --gateway-url https://<your-gateway-url>:8000 \
  --secret-name /demo/apps/analytics/postgres-ro \
  --profile <profile-name>
```

For Runtime Authority behavior, prerequisites, and tool semantics, see [Agentic Runtime Authority](https://docs.akeyless.io/docs/agentic-runtime-authority).

## Supported Integrations

| Integration | Primary use case | Configuration surface |
| --- | --- | --- |
| Claude Desktop | Desktop AI assistant workflow with local MCP client configuration | `~/Library/"Application Support"/Claude/claude_desktop_config.json` |
| Cursor | Editor-based MCP workflow in Cursor | `~/.cursor/mcp.json` or Cursor settings JSON |
| GitHub Copilot | MCP workflow with GitHub Copilot CLI | `~/.copilot/mcp-config.json` |
| JetBrains IDEs | IDE-native plugin workflow for JetBrains products | JetBrains plugin settings |

The dedicated integration pages in this section provide client-specific setup details for Claude Desktop, Cursor, GitHub Copilot, and JetBrains IDEs.

Use these pages for client-specific configuration:

* [Claude Desktop Integration](https://docs.akeyless.io/docs/mcp-claude-desktop)
* [Cursor Integration](https://docs.akeyless.io/docs/mcp-cursor)
* [GitHub Copilot Integration](https://docs.akeyless.io/docs/mcp-github-copilot)
* [JetBrains IDEs Integration](https://docs.akeyless.io/docs/mcp-jetbrains-ides)

## How To Use This Section

1. Start with this page when you need to understand the MCP content set.
2. Open the integration-specific page for the MCP client you plan to use.
3. Use [Akeyless CLI](https://docs.akeyless.io/docs/cli) and [Access and Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) when you need installation or authentication background.
