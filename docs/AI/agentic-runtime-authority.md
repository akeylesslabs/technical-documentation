---
title: Agentic Runtime Authority
deprecated: false
hidden: true
metadata:
  robots: index
---
Agentic Runtime Authority allows AI agents to securely communicate with your resources through the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview). It provides controlled, authorized access so agents can interact with protected environments without exposing long-lived credentials.

**Agentic Runtime Authority** currently supports the following dynamic secret types:

* **DB Dynamic Secrets** for database access.
* **Cloud Dynamic Secrets** for cloud environment access.
* **GitHub Dynamic Secrets** for GitHub repository access.

# Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) version `4.51.0`.

* CLI version `1.144.0`.

* [AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight) enabled on the Gateway to power intelligent resource access.

* A Dynamic Secret configured with Agentic Runtime Authority enabled.

* An authentication method associated with a role that has Agentic Runtime Authority permissions.

* Claude/Cursor Desktop installed.

# Setting up the AI Agent

To integrate Akeyless with your AI agent, add the **Akeyless MCP server** configuration to the agent’s config file.

**For Claude**

Create the following file: `~/Library/"Application Support"/Claude/claude_desktop_config.json`.

**For Cursor**

Create the following file: `~/.cursor/mcp.json`.

Use the following configuration template for both **Claude** and **Cursor**. Replace the placeholder values with your environment details:

```json
{
  "mcpServers": {
    "akeyless-connector": {
      "command": "akeyless",
      "args": [
        "mcp-runtime-authority",
        "--gateway-url",
        "https://<Your-Akeyless-GW-URL>:8000",
        "--secret-name",
        "full/path/to/secret",
        "--profile",
        "profile_name"
      ]
    }
  }
}
```

Where:

* `gateway-url`: The Gateway URL where the Dynamic Secret exists.

* `secret-name`: The full path of a specific Dynamic Secret to expose to the AI agent. Use this parameter when you want the agent to access only one secret. To allow access to all supported Dynamic Secrets, remove this parameter. Multiple specific secrets are not supported.

* `profile`: The CLI profile with the required RBAC permissions for working with Agentic Runtime Authority.

# Querying Your Resources

With Agentic Runtime Authority configured, you can now use Claude or Cursor to interact with your protected resources in natural language. The AI agent will authenticate requests and retrieve credentials dynamically without storing long-lived secrets.

## Monitoring Access

Each session and resource query is automatically logged. You can view access activity under the **Agentic Runtime Authority** tab in the **Akeyless Console** to monitor which resources were accessed and when.

## Controlling Access with Input Rules

For additional security, you can control what users are allowed to ask the AI agent to do. This is useful for preventing accidental exposure of sensitive information.

**To restrict certain queries:**

1. Open the [Dynamic Secret](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) object in the Akeyless Console.
2. Add an **Input Rule** that matches patterns you want to block (for example: queries requesting **personal information**, **credentials**, or **internal records**).
3. When a user sends a request matching a blocked rule, the request is denied and restricted information is not returned from the database.

This approach keeps the AI agent useful for legitimate queries while ensuring access remains controlled and secure.
