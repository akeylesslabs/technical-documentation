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
slug: mcp
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

## Available MCP Servers

The Akeyless CLI provides two separate MCP servers. They're built for different jobs, so most integrations only need one of them.

|                     | `akeyless mcp`                                                                                                                                      | `akeyless mcp-runtime-authority`                                                                           |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **What it's for**   | Managing Akeyless itself - browsing, reading, and (optionally) writing vault objects                                                                | Using secrets Akeyless already manages, without exposing them to the model                                 |
| **Typical prompts** | "List my secrets under `/prod`", "Show me the `api-key` secret", "Create a static secret named `db-password`"                                       | "Query the `orders` table in prod Postgres", "List pods in the `staging` namespace", "Open a PR on GitHub" |
| **Tools**           | `list_items`, `describe_item`, `get_secret`, `get_password`, `list_targets`, `list_roles`, `create_secret`, `update_item`, `delete_item`, and more. | `list-secrets`, `list-sub-tools`, `query-db`, `service-execute`                                            |

For full command flags and usage details, see [CLI Reference](https://docs.akeyless.io/docs/cli-reference#mcp).

### When to use `akeyless mcp`

Use this server when the client needs to work with Akeyless itself - browsing the secrets tree, reading a secret's value, checking who has access to what, or `creating/updating/deleting` an item. It talks over `stdio` from the CLI, or over HTTP from the Akeyless Gateway if you'd rather not run the CLI locally. Access is scoped by the calling profile's or token's RBAC permissions, same as any other Akeyless client.

Reach for this one for assistants built for admins and developers: "what's in my vault," "rotate this secret's metadata," "who can access this role."

### When to use `akeyless mcp-runtime-authority`

Use this server when an agent needs to _use_ a secret to do something - run a database query, call a cloud API, hit Kubernetes, or act against GitHub - **without the model ever seeing the underlying credential**. The Gateway fetches just-in-time credentials behind the scenes and returns only the query/action result to the model.

The typical flow is:

1. `list-secrets` - see which ARA-enabled secrets (and target types) the calling role can use
2. `list-sub-tools` _-&#x20;_&#x6F;ptional, for a **service** secret, discover what actions/parameters are available before calling it
3. `query-db` or `service-execute` - actually run the query or action

Reach for this one for agents that need to act on production systems (databases, AWS/GCP/Azure, Kubernetes, GitHub) or on a third-party service reachable through a custom MCP target - anywhere you want the agent to get results, not raw secrets.

<Callout icon="📘" theme="success">
  ### Note

  A secret configured with an `mcp_url` (a "custom MCP" target, e.g. HubSpot, Linear, Postman) is proxied through `service-execute` / `list-sub-tools` the same way - it isn't a third server, just another target type ARA can reach.
</Callout>

For full command syntax and flags, see [CLI Reference - mcp-runtime-authority](https://docs.akeyless.io/docs/cli-reference#mcp-runtime-authority).

For Runtime Authority behavior, prerequisites, and tool semantics, see [Agentic Runtime Authority](https://docs.akeyless.io/docs/agentic-runtime-authority).

## Supported Integrations

| Integration                                                        | Primary use case                                                  | Configuration surface                                             |
| ------------------------------------------------------------------ | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| [Claude Desktop](https://docs.akeyless.io/docs/mcp-claude-desktop) | Desktop AI assistant workflow with local MCP client configuration | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| [Cursor](https://docs.akeyless.io/docs/mcp-cursor)                 | Editor-based MCP workflow in Cursor                               | `~/.cursor/mcp.json` or Cursor settings JSON                      |
| [GitHub Copilot](https://docs.akeyless.io/docs/mcp-github-copilot) | MCP workflow with GitHub Copilot CLI                              | `~/.copilot/mcp-config.json`                                      |
| [JetBrains IDEs](https://docs.akeyless.io/docs/mcp-jetbrains-ides) | IDE-native plugin workflow for JetBrains products                 | JetBrains plugin settings                                         |
