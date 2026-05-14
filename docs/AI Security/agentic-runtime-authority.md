---
title: Agentic Runtime Authority
excerpt: Configure Agentic Runtime Authority for controlled AI agent access and runtime query governance.
deprecated: false
hidden: false
metadata:
  title: Agentic Runtime Authority
  description: Configure Agentic Runtime Authority to apply runtime controls, role-based access, and MCP workflows for AI agent access.
  robots: index
---

> ⚠️ **Warning:**
>
> Agentic Runtime Authority is currently in early access. Features, behavior, and availability can change between releases.

Agentic Runtime Authority allows AI agents to securely communicate with protected resources through the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview). It provides controlled, authorized access so agents can interact with supported secrets without exposing long-lived credentials. In this context, **runtime control** means the authorization checks and input or output rules that Akeyless enforces when an agent sends a live request to a protected resource.

**Agentic Runtime Authority** currently supports these target categories for runtime execution:

* **Database targets**: MySQL, PostgreSQL, MSSQL, Oracle, Snowflake, HanaDB, Redshift, MongoDB, Redis, and Cassandra.
* **Service targets**: AWS, GCP, Azure, and GitHub.

The `runtime-authority` command and the MCP execution tools operate on supported dynamic, rotated, and static secrets. Static secrets are typically used for OAuth 2.1-based MCP workflows and connection-string-based integrations.

Agentic Runtime Authority extends Akeyless AI security beyond secretless credential retrieval by adding runtime controls and reporting for agent access.

Agentic Runtime Authority policy controls are central to secure agent execution. Input and output rules define what the agent can send and what data it can receive, and each runtime session is traceable for monitoring and audit workflows.

The current implementation exposes Agentic Runtime Authority in these places:

* The **Agentic Runtime Authority** step or details tab on supported Dynamic Secrets in the Akeyless Console
* The [runtime-authority CLI command](https://docs.akeyless.io/docs/cli-reference#runtime-authority) for direct runtime queries through the Gateway
* The [mcp-runtime-authority CLI command](https://docs.akeyless.io/docs/cli-reference#mcp-runtime-authority) for MCP-based agent integrations
* The MCP tools exposed by `mcp-runtime-authority`: `list-secrets`, `query-db`, and `service-execute`
* The `ara-reports-access` role rule for dashboard visibility
* The **Agentic Runtime Authority** role-rule type with the **Allow Access** capability in the Console role editor
* Repeated `--input-rule` and `--output-rule` flags on Dynamic Secret create and update commands

## Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) version `4.51.0` or later.
* [AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight) enabled on the Gateway.
* A Dynamic Secret configured with Agentic Runtime Authority enabled.
* A role with access to the relevant Dynamic Secret and, when required, reporting access to Agentic Runtime Authority.
* An authentication method associated with that role.
* A supported desktop client, such as Claude Desktop or Cursor, if you plan to use MCP.
* CLI version `1.144.0` or later, only when you plan to use CLI-based setup or execution flows.

## Control Access With RBAC

Agentic Runtime Authority uses separate RBAC controls for dashboard visibility and runtime execution.

### Control Dashboard Visibility

Use the `ara-reports-access` administrative rule on a role to control access to the Agentic Runtime Authority dashboard.

Supported values are:

* `none`
* `scoped`
* `all`

Use the Console when you want to configure dashboard visibility on a role without using the CLI:

1. Open the relevant access role in the Akeyless Console.
2. Open the administrative rules section.
3. Locate **Agentic Runtime Authority**.
4. Set the reporting scope to `None`, `Scoped`, or `All`.
5. Save the role.

For command syntax, see [CLI Reference - Access Roles](https://docs.akeyless.io/docs/cli-reference-access-roles). Use the create role command when creating a new role:

```shell
akeyless create-role \
  --name <role-name> \
  --ara-reports-access <none|scoped|all>
```

Use the update role command when modifying an existing role:

```shell
akeyless update-role \
  --name <role-name> \
  --ara-reports-access <none|scoped|all>
```

This rule controls dashboard visibility. Runtime execution also depends on the relevant Agentic Runtime Authority role rule and underlying secret permissions.

### Grant Runtime Execution Access

Use the role-rule workflow when you want a role to execute Agentic Runtime Authority operations on a path.

1. Open the access role that should run Agentic Runtime Authority queries.
2. Add a role rule with the type **Agentic Runtime Authority**.
3. Set the path to the relevant Agentic Runtime Authority (ARA)-enabled secret path.
4. Select the **Allow Access** capability.
5. Save the role.

Use the administrative rule separately when you also want reporting visibility.

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

Dynamic Secret [create](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#create) and [update](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#update) commands accept repeated `--input-rule` and `--output-rule` flags in `name=...,rule=...` format.

Example input and output rule values:

```text
name=read-only-sql,rule=Only allow read-only SQL statements: SELECT, SHOW, DESCRIBE, DESC, EXPLAIN, WITH. Reject any DML or DDL statements such as INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, GRANT, REVOKE.
name=mask-email,rule=Mask email addresses in the returned results.
```

The current CLI parser requires both `name` and `rule` for each repeated flag.

## Set Up The AI Agent

To integrate Akeyless with your AI agent, add the **Akeyless MCP server** configuration to the agent’s config file. For general MCP concepts, command syntax, and client setup patterns, see [Akeyless MCP Model Context Protocol Command](https://docs.akeyless.io/docs/akeyless-mcp-model-context-protocol-command). The configuration below is specific to the [mcp-runtime-authority subcommand](https://docs.akeyless.io/docs/cli-reference#mcp-runtime-authority).

### For Claude

Create the following file: `~/Library/Application Support/Claude/claude_desktop_config.json`.

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
        "--profile",
        "profile_name"
      ]
    }
  }
}
```

Where:

* `gateway-url`: The Gateway URL where the Dynamic Secret exists.

* `secret-name`: Optional. Use this only when you want to set a default path for the `query-db` MCP tool. This does not replace RBAC scoping for the server. Use role rules and secret permissions to restrict which secrets the profile can access.

* `profile`: The CLI profile with the required RBAC permissions for working with Agentic Runtime Authority.

When the MCP server is running, it exposes these workflows:

* `list-secrets`: Lists ARA-supported secrets that the current profile can access.
* `query-db`: Runs database queries. `payload` and `agent-id` are required. `secret-name` is required per request only when no default `--secret-name` was provided at server startup.
* `service-execute`: Runs service actions against supported service targets. `secret-name`, `payload`, and `agent-id` are required.

For OAuth-backed service flows, `service-execute` can also require `auth-code` and `state` on the follow-up call after the server returns an authorization URL.

## Query Protected Resources With The CLI

Use the [runtime-authority command](https://docs.akeyless.io/docs/cli-reference#runtime-authority) for direct runtime queries through the Gateway:

```shell
akeyless runtime-authority \
  --name /demo/apps/analytics/postgres-ro \
  --payload 'SELECT current_user, current_database();' \
  --agent-id ai-assistant-01 \
  -u https://<gateway-url>:8000 \
  --profile <profile-name>
```

Use the [mcp-runtime-authority command](https://docs.akeyless.io/docs/cli-reference#mcp-runtime-authority) when the agent connects through MCP:

```shell
akeyless mcp-runtime-authority \
  --gateway-url https://<gateway-url>:8000 \
  --secret-name /demo/apps/analytics/postgres-ro \
  --profile <profile-name>
```

## Monitoring Access

Each session and resource query is logged by the runtime services. Use the `ara-reports-access` role rule to grant access to Agentic Runtime Authority reporting data. See [Control Access With RBAC](#control-access-with-rbac) for role setup details.

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

Example input rules:

```text PostgreSQL
name=read-only-sql,rule=Only allow read-only SQL statements: SELECT, SHOW, DESCRIBE, DESC, EXPLAIN, WITH. Reject any DML or DDL statements such as INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, GRANT, REVOKE.
```
```text Redis
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

* Identity and Secrets Intelligence
* [Akeyless AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight)
* [Prompt Injection Protection for AI Agents](https://docs.akeyless.io/docs/prompt-injection-protection-for-ai-agents)
