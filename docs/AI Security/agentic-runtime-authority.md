---
title: Agentic Runtime Authority
deprecated: false
hidden: false
metadata:
  robots: index
---

> ⚠️ **Warning:**
>
> Agentic Runtime Authority is currently in early access. Features, behavior, and availability can change between releases.

Agentic Runtime Authority allows AI agents to securely communicate with protected resources through the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview). It provides controlled, authorized access so agents can interact with supported Dynamic Secrets without exposing long-lived credentials.

**Agentic Runtime Authority** currently supports the following dynamic secret types:

* **DB Dynamic Secrets** for database access.
* **Cloud Dynamic Secrets** for cloud environment access.
* **GitHub Dynamic Secrets** for GitHub repository access.

Agentic Runtime Authority extends Akeyless AI security beyond secretless credential retrieval by adding runtime controls and reporting for agent access.

The current implementation exposes Agentic Runtime Authority in these places:

* The **Agentic Runtime Authority** step or details tab on supported Dynamic Secrets in the Akeyless Console
* The `runtime-authority` CLI command for direct runtime queries through the Gateway
* The `mcp-runtime-authority` CLI command for MCP-based agent integrations
* The `ara-reports-access` role rule for dashboard visibility
* Repeated `--input-rule` and `--output-rule` flags on Dynamic Secret create and update commands

## Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) version `4.51.0`.
* CLI version `1.144.0`.
* [AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight) enabled on the Gateway when output rules are used.
* A Dynamic Secret configured with Agentic Runtime Authority enabled.
* A role with access to the relevant Dynamic Secret and, when required, reporting access to Agentic Runtime Authority.
* An authentication method associated with that role.
* A supported desktop client, such as Claude Desktop or Cursor, if you plan to use MCP.

## Control Access With RBAC

Use the `ara-reports-access` administrative rule on a role to control access to the Agentic Runtime Authority dashboard.

Supported values are:

* `none`
* `scoped`
* `all`

Use `create-role` when creating a new role:

```shell
akeyless create-role \
  --name <role-name> \
  --ara-reports-access <none|scoped|all>
```

Use `update-role` when modifying an existing role:

```shell
akeyless update-role \
  --name <role-name> \
  --ara-reports-access <none|scoped|all>
```

This rule controls dashboard visibility. Access to the underlying Dynamic Secret still depends on the relevant secret permissions.

In the current Console role editor, the administrative rules form also exposes **Agentic Runtime Authority** as a selectable administrative rule.

## Configure Agentic Runtime Authority In The Console

1. Open the Dynamic Secret that the AI agent will use.
2. Open the **Agentic Runtime Authority** step or details tab.
3. Turn on **Enable Agentic Runtime Authority**.
4. Review the **Input Rules** table.
5. Review the **Output Rules** table.
6. Add, edit, or delete rules as needed.
7. Save the Dynamic Secret.

For new Dynamic Secrets, the current Console implementation can prepopulate default input rules for these producer types:

* MySQL
* PostgreSQL
* Redshift
* MSSQL
* Oracle
* Snowflake
* HanaDB
* Cassandra
* Redis
* MongoDB

These defaults are producer-specific. For example, SQL producers receive read-only and no-multi-statement input rules by default.

## Configure Agentic Runtime Authority With The CLI

Dynamic Secret create and update commands accept repeated `--input-rule` and `--output-rule` flags in `name=...,rule=...` format.

Example input and output rule values:

```text
name=read-only-sql,rule=Only allow read-only SQL statements: SELECT, SHOW, DESCRIBE, DESC, EXPLAIN, WITH. Reject any DML or DDL statements such as INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, GRANT, REVOKE.
name=mask-email,rule=Mask email addresses in the returned results.
```

The current CLI parser requires both `name` and `rule` for each repeated flag.

## Set Up The AI Agent

To integrate Akeyless with your AI agent, add the **Akeyless MCP server** configuration to the agent’s config file.

### For Claude

Create the following file: `~/Library/"Application Support"/Claude/claude_desktop_config.json`.

### For Cursor

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

## Query Protected Resources With The CLI

Use `runtime-authority` for direct runtime queries through the Gateway:

```shell
akeyless runtime-authority \
  --name /demo/apps/analytics/postgres-ro \
  --payload 'SELECT current_user, current_database();' \
  --agent-id ai-assistant-01 \
  -u https://<gateway-url>:8000 \
  --profile <profile-name>
```

Use `mcp-runtime-authority` when the agent connects through MCP:

```shell
akeyless mcp-runtime-authority \
  --gateway-url https://<gateway-url>:8000 \
  --secret-name /demo/apps/analytics/postgres-ro \
  --profile <profile-name>
```

## Query Protected Resources

With Agentic Runtime Authority configured, you can now use Claude or Cursor to interact with your protected resources in natural language. The AI agent will authenticate requests and retrieve credentials dynamically without storing long-lived secrets.

## Monitoring Access

Each session and resource query is logged by the runtime services.

In the current Console implementation, the verified UI coverage for Agentic Runtime Authority is on Dynamic Secret configuration surfaces (the **Agentic Runtime Authority** tab and rules tables). A dedicated Agentic Runtime Authority reporting page is not exposed in the frontend-react Console routes.

## Control Agent Behavior With Rules

For additional security, Agentic Runtime Authority supports both input rules and output rules on the Dynamic Secret. Use these rules to limit unsafe requests and reduce accidental exposure of sensitive information.

To restrict certain queries or responses:

1. Open the [Dynamic Secret](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) object in the Akeyless Console.
2. Add an **Input Rule** to block disallowed prompts.
3. Add an **Output Rule** to block disallowed response content.
4. When a request or response matches a blocked rule, the action is denied and the protected data is not returned.

This approach keeps the AI agent useful for legitimate queries while ensuring access remains controlled and secure.

## Examples

Example CLI role setup for reporting access:

```shell
akeyless create-role \
  --name <role-name> \
  --ara-reports-access scoped
```

Example input rule for SQL producers:

```text
name=read-only-sql,rule=Only allow read-only SQL statements: SELECT, SHOW, DESCRIBE, DESC, EXPLAIN, WITH. Reject any DML or DDL statements such as INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, GRANT, REVOKE.
```

Example input rule for Redis producers:

```text
name=denied-commands,rule=Deny the following Redis commands: KEYS, FLUSHALL, FLUSHDB, DEBUG, SHUTDOWN, BGSAVE, BGREWRITEAOF, SLAVEOF, REPLICAOF, CLUSTER, MIGRATE, MONITOR, SUBSCRIBE, PSUBSCRIBE, EVAL, EVALSHA, EVALRO, EVALSHA_RO, SCRIPT. Also deny CONFIG subcommands SET, REWRITE, and RESETSTAT.
```

Example direct runtime query:

```shell
akeyless runtime-authority \
  --name /demo/apps/analytics/postgres-ro \
  --payload 'SELECT count(*) FROM customers;' \
  --agent-id ai-assistant-01 \
  -u https://<gateway-url>:8000 \
  --profile <profile-name>
```

## Related AI Guides

* [Identity and Secrets Intelligence](https://docs.akeyless.io/docs/identity-and-secrets-intelligence)
* [Akeyless AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight)
* [Prompt Injection Protection for AI Agents](https://docs.akeyless.io/docs/prompt-injection-protection-for-ai-agents)
