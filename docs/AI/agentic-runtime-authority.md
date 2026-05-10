---
title: Agentic Runtime Authority
deprecated: false
hidden: true
metadata:
  robots: index
---
Agentic Runtime Authority allows AI agents to securely communicate with your resources through the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview). It provides controlled, authorized access so agents can interact with protected environments without exposing long-lived credentials.

> 📘 Note
>
> In this guide, Claude AI is used to work with the Agentic Runtime Authority.

# Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) version `4.51.0`.
* CLI version `1.144.0`
* [AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight) enabled on the Gateway.
* Dynamic Secret with Agentic Runtime Authority enabled.
* An authentication method associated with a role that has Agentic Runtime Authority permissions
* Claude Desktop installed.

# Setting up the AI Agent

The following steps are required to integrate Akeyless with the AI agent. This guide uses Claude AI as an example.

Create the following file: `~/Library/"Application Support"/Claude/claude_desktop_config.json`:

```json claude_desktop_config.json
{
  "preferences": {
    "coworkWebSearchEnabled": true,
    "coworkScheduledTasksEnabled": false,
    "ccdScheduledTasksEnabled": false,
    "epitaxyPrefs": {
      "starred-local-code-sessions": [],
      "starred-cowork-spaces": [],
      "starred-session-groups": [],
      "dframe-local-slice": {
        "pinnedOrder": [],
        "customGroupAssignments": {},
        "customGroupOrder": {}
      }
    }
  },
  "mcpServers": {
    "akeyless-connector": {
      "command": "akeyless",
      "args": [
        "mcp-runtime-authority",
        "--gateway-url", "http://3.14.113.198:8000",
        "--profile", "staging"
      ]
    }
```

Where:

* `gateway-url`: TThe Gateway URL where the Dynamic Secret exists.
* `profile`: The CLI profile with the required RBAC permissions for working with Agentic Runtime Authority.

After the `claude_desktop_config.json` file is configured, quit and reopen Claude Desktop. Then go to **Settings** > **Developer**. You should see the **Akeyless-Connector** MCP Server in a **running** state.

# Querying the DB

You can now use Claude to query your databases in natural language. Each session is logged under the **Agentic Runtime Authority** tab in the **Akeyless Console**.

You can also control what users are allowed to ask. For example, you may want to block questions that expose sensitive data, such as **personal information**, **credentials**, or **internal records**.

To do this, add an Input Rule to the [Dynamic Secret ](https://docs.akeyless.io/docs/how-to-create-dynamic-secret)object. When a user sends a request that matches a blocked rule, the request is denied and the restricted information is not returned from the database.

This helps keep the AI agent useful while still making sure access stays controlled and secure.

<br />

<br />

<br />

<br />
