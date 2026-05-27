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

Agentic Runtime Authority allows AI agents to securely communicate with protected resources through the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview). It provides controlled, authorized access so agents can interact with supported secrets without exposing long-lived credentials. In this context, **runtime control** means the authorization checks and input or output rules that Akeyless enforces when an agent sends a live request to a protected resource. Policies on Dynamic Secrets define what agents can and cannot do—input rules restrict allowed operations, and output rules filter returned data—ensuring secure and compliant runtime execution.

## Supported Targets And Secret Types

**Agentic Runtime Authority** supports these target categories for runtime execution:

* **Database targets**: MySQL, PostgreSQL, MSSQL, Oracle, Snowflake, HanaDB, Redshift, MongoDB, Redis, and Cassandra.
* **Service targets**: AWS, GCP, Azure, Kubernetes (native K8s, EKS, and GKE), and GitHub.

The runtime authority execution path supports these secret types:

* **Dynamic secrets**: For temporary, rotated credentials.
* **Rotated secrets**: For regularly rotated credentials.
* **Static secrets**: For MCP-based service workflows, including OAuth authorization-code flows.

Agentic Runtime Authority extends Akeyless AI security beyond secretless credential retrieval by adding runtime controls and reporting for agent access.

## Runtime Entry Points

Runtime authority is exposed through these code-backed entry points:

* The [runtime-authority CLI command](https://docs.akeyless.io/docs/cli-reference#runtime-authority) for direct runtime execution through Gateway target query.
* The [mcp-runtime-authority CLI command](https://docs.akeyless.io/docs/cli-reference#mcp-runtime-authority) for MCP-based integrations.
* MCP tools: `list-secrets`, `query-db`, and `service-execute`.
* The `ara-reports-access` role administrative rule for dashboard visibility.
* The ARA role-rule **Allow Access** capability (`allow_access`) for runtime execution.
* Repeated `--input-rule` and `--output-rule` flags on Dynamic Secret create and update commands.

## Prerequisites

### Required

* [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) with runtime authority support enabled. See [Configure Agentic Runtime Authority In The Console](https://docs.akeyless.io/docs/agentic-runtime-authority#configure-agentic-runtime-authority-in-the-console).
* **[Akeyless AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight)** configured for the account and Gateway. Runtime query validation depends on AI validation. See [High-Level Setup Steps](https://docs.akeyless.io/docs/akeyless-ai-insight#high-level-setup-steps).
* A Dynamic Secret, Rotated Secret, or Static Secret configured for your runtime workflow.
* A role with ARA execution permissions to the relevant secret path and, when required, reporting visibility.
* An authentication method associated with that role.

### Optional

* A supported desktop client, such as Claude Desktop or Cursor, if you plan to use MCP.
* Akeyless CLI installed when you plan to use CLI-based setup or execution flows.

## Policy Control And Traceability Summary

Agentic Runtime Authority policy controls are central to secure agent execution. **Input and output rules define what the agent can send and what data it can receive**, and each runtime session is traceable for monitoring and audit workflows.

### Control: What the Agent Can and Cannot Do

* **Input rules**: Constrain what the agent is allowed to send (queries, prompts, commands) when accessing dynamic, rotated, or static secrets. Blocked requests are denied before reaching the target.
* **Output rules**: Constrain what data can be returned to the agent from protected resources. Blocked response content is filtered or redacted.

### Traceability: Full Audit Trail

* **Session recording**: Each runtime request is recorded as an ARA session with execution metadata (for example secret path, target type, agent or MCP identifiers, status, and payload).
* **Access scope**: Runtime behavior is scoped by role rules and secret permissions.
* **Monitoring and audit**: Use the `ara-reports-access` administrative rule to grant access to Agentic Runtime Authority reporting data for compliance and investigation workflows.

## Control Access With RBAC

Agentic Runtime Authority uses separate RBAC controls for dashboard visibility and runtime execution.

### Control Dashboard Visibility

Use the `ara-reports-access` administrative rule on a role to control access to the Agentic Runtime Authority dashboard.

Supported values are:

* `none` - No dashboard access.
* `scoped` - Shows sessions that match the role scope.
* `all` - Shows all sessions in the account.

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

## Secret Structure Requirements

Agentic Runtime Authority (ARA) runs against existing Akeyless secrets. The required structure depends on the target type, but these baseline requirements apply in all cases:

* The secret path is stable and scoped by RBAC so the calling role can access only the intended path.
* The secret type is supported for ARA runtime execution (dynamic, rotated, or static).
* ARA is enabled on the secret in the Console.
* Input and output rules are configured when you need runtime guardrails.

For OAuth 2.1-backed service workflows, use a static secret that includes the service's OAuth client configuration. At minimum, keep the following values available in the secret definition and service setup:

* Client identity values (for example, client ID and client secret).
* Authorization and token endpoints for the target service.
* Redirect URI values that match your OAuth app registration.
* Required scopes for the operations the agent must run.

## OAuth 2.1 Workflow For `service-execute`

When `service-execute` targets an OAuth-backed service, use this runtime sequence:

1. The agent calls `service-execute` with `secret-name`, `payload`, and `agent-id`.
2. The runtime returns an authorization URL when user consent is required.
3. The user signs in and approves access in the provider consent page.
4. The provider redirects back with an authorization code and state value.
5. The agent calls `service-execute` again with `auth-code` and `state` (plus the original request context) to complete the flow.
6. The action is executed and returned through the ARA runtime path.

Treat `state` as a required anti-forgery value and preserve it exactly between the initial and follow-up calls.

## Set Up The AI Agent

To integrate Akeyless with your AI agent, add the **Akeyless MCP server** configuration to the agent’s config file. For general MCP concepts, command syntax, and client setup patterns, see [Akeyless MCP Model Context Protocol Command](https://docs.akeyless.io/docs/mcp). The configuration below is specific to the [mcp-runtime-authority subcommand](https://docs.akeyless.io/docs/cli-reference#mcp-runtime-authority).

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

Each session and resource query is logged by the runtime services. Use the `ara-reports-access` administrative rule to grant access to Agentic Runtime Authority reporting data. See [Control Access With RBAC](#control-access-with-rbac) for role setup details.

## Control Agent Behavior With Rules

For additional security, Agentic Runtime Authority supports both input rules and output rules on the Dynamic Secret. Use these rules to limit unsafe requests and reduce accidental exposure of sensitive information.

To restrict certain queries or responses:

1. Open the [Dynamic Secret](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) object in the Akeyless Console.
2. Add an **Input Rule** to block disallowed prompts.
3. Add an **Output Rule** to block disallowed response content.
4. When a request or response matches a blocked rule, the action is denied and the protected data is not returned.

This approach keeps the AI agent useful for legitimate queries while ensuring access remains controlled and secure.

## Examples

### Security Administrator

Use this example to grant dashboard visibility for compliance and investigations.

1. Create a role with scoped ARA reporting visibility.
   ```shell
   akeyless create-role \
     --name <role-name> \
     --ara-reports-access scoped
   ```

   If the role already exists, update it instead:

   ```shell
   akeyless update-role \
     --name <role-name> \
     --ara-reports-access scoped
   ```
2. Assign this role to the users or auth methods that should view ARA reports.

   ```shell
   akeyless assoc-role-am \
     --role-name <role-name> \
     --am-name <auth-method-name>
   ```
3. After a runtime query is executed, open the Agentic Runtime Authority reporting view in the Console and verify that session records are visible.

### Platform Engineer

Use this example to set baseline runtime guardrails on a Dynamic Secret using input and output rules.

1. Define producer-appropriate input rules.
2. Apply the rules on Dynamic Secret create or update.
3. Save and test a safe query to confirm rule behavior.

```text PostgreSQL
name=read-only-sql,rule=Only allow read-only SQL statements: SELECT, SHOW, DESCRIBE, DESC, EXPLAIN, WITH. Reject any DML or DDL statements such as INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, GRANT, REVOKE.
```
```text Redis
name=denied-commands,rule=Deny the following Redis commands: KEYS, FLUSHALL, FLUSHDB, DEBUG, SHUTDOWN, BGSAVE, BGREWRITEAOF, SLAVEOF, REPLICAOF, CLUSTER, MIGRATE, MONITOR, SUBSCRIBE, PSUBSCRIBE, EVAL, EVALSHA, EVALRO, EVALSHA_RO, SCRIPT. Also deny CONFIG subcommands SET, REWRITE, and RESETSTAT.
```

Example update command:

```shell
akeyless update-dynamic-secret \
  --name /demo/apps/analytics/postgres-ro \
  --input-rule "name=read-only-sql,rule=Only allow read-only SQL statements: SELECT, SHOW, DESCRIBE, DESC, EXPLAIN, WITH. Reject any DML or DDL statements such as INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, GRANT, REVOKE." \
  --output-rule "name=mask-email,rule=Mask email addresses in the returned results."
```

### Security Analyst

Use this example to run an auditable read-only query through Gateway runtime authority.

1. Run a read-only query against an ARA-enabled secret.
2. Confirm the request succeeds and returns expected rows.
3. Verify the session in ARA reporting.

```shell
akeyless runtime-authority \
  --name /demo/apps/analytics/postgres-ro \
  --payload 'SELECT count(*) FROM customers;' \
  --agent-id ai-assistant-01 \
  -u https://<gateway-url>:8000 \
  --profile <profile-name>
```

Expected output (example; response fields vary by target type and query):

```json
{
  "target_type": "postgres",
  "results": [
    {
      "count": 42
    }
  ]
}
```

### Application Developer

Use this example to request a service action through MCP and then complete OAuth when consent is required.

1. Start the MCP runtime authority server.
2. Send the initial `service-execute` request without `auth-code` and `state`.
3. Open the returned authorization URL and approve consent.
4. Send a follow-up `service-execute` request with `auth-code` and `state`.

Start MCP runtime authority:

```shell
akeyless mcp-runtime-authority \
  --gateway-url https://<gateway-url>:8000 \
  --profile <profile-name>
```

```text
Use service-execute on /demo/services/github/oauth-app to list open pull requests in akeylesslabs/technical-documentation.
```

Initial MCP tool call (before consent):

```json
{
  "tool": "service-execute",
  "arguments": {
    "secret-name": "/demo/services/github/oauth-app",
    "payload": "{\"action\":\"list-repositories\"}",
    "agent-id": "ai-assistant-01"
  }
}
```

Follow-up MCP tool call (after consent redirect):

```json
{
  "tool": "service-execute",
  "arguments": {
    "secret-name": "/demo/services/github/oauth-app",
    "payload": "{\"action\":\"list-repositories\"}",
    "agent-id": "ai-assistant-01",
    "auth-code": "<oauth-authorization-code>",
    "state": "<oauth-state-from-initial-response>"
  }
}
```

## Related AI Guides

* Identity and Secrets Intelligence
* [Akeyless AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight)
* [Prompt Injection Protection for AI Agents](https://docs.akeyless.io/docs/prompt-injection-protection-for-ai-agents)
