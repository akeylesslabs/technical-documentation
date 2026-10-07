---
title: test
deprecated: false
hidden: false
metadata:
  robots: index
---
# Claude

Connect Claude to Akeyless.

Connect Claude to Akeyless so Claude can work with your Akeyless items, or run database queries and cloud actions without ever seeing your credentials. You can connect in two ways: with the Akeyless MCP Server, which runs through the Akeyless CLI, or with the Akeyless plugin for Claude, which doesn't need the CLI.

## Akeyless MCP Servers

Akeyless offers two MCP servers. Each one gives Claude a different set of tools, and most people need only one of them:

|                          | Vault management                                     | Agentic Runtime Authority                                                                                                            |
| ------------------------ | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **What Claude can do**   | Browse, read, create, and update your Akeyless items | Run database queries and cloud actions. The Gateway uses the credentials and returns only the result, so Claude never sees a secret. |
| **Example request**      | "List my secrets under `/prod`"                      | "Count the rows in the `customers` table in prod Postgres"                                                                           |
| **Akeyless CLI command** | `akeyless mcp`                                       | `akeyless mcp-runtime-authority`                                                                                                     |

For more about each server, see [MCP Server](https://docs.akeyless.io/docs/mcp).

## Choose How To Connect

The following table compares the two ways to connect Claude to Akeyless:

|                               | [Akeyless MCP Server](#connect-with-the-akeyless-mcp-server) | [Akeyless plugin](#connect-with-the-akeyless-plugin)                           |
| ----------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| **MCP servers**               | Vault management and Agentic Runtime Authority               | Agentic Runtime Authority                                                      |
| **Requires the Akeyless CLI** | Yes                                                          | No                                                                             |
| **Works in**                  | Claude Desktop and Claude Code                               | Claude Desktop, Cowork, and Claude Code                                        |
| **How Claude signs in**       | With your Akeyless CLI profile                               | With your Authentication Method, from a settings form or environment variables |

Use the following guidelines to pick one:

* To let Claude manage your Akeyless items, use the Akeyless MCP Server. It's the only way to connect vault management.
* To use Agentic Runtime Authority without installing the Akeyless CLI, use the Akeyless plugin.

## Connect With The Akeyless MCP Server

The Akeyless MCP Server provides both MCP servers. Claude starts them on your computer with the Akeyless CLI, and signs in with your CLI profile.

### Prerequisites

* The [Akeyless CLI](https://docs.akeyless.io/docs/cli) version `1.144.0` or later, with a profile configured on the computer that runs Claude.
* Your Gateway URL.
* An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) associated with an [Access Role](https://docs.akeyless.io/docs/rbac) that grants access to the items Claude should use.
* For Agentic Runtime Authority:&#x20;
  - your own Gateway with Agentic Runtime Authority and Akeyless AI Insights enabled
  - Secrets configured for Agentic Runtime Authority&#x20;
  - An Access Role with the Agentic Runtime Authority **Allow Access** rule on their paths.&#x20;
  See [Agentic Runtime Authority Prerequisites](https://docs.akeyless.io/docs/agentic-runtime-authority#prerequisites).

### Connect Claude Desktop

Claude Desktop starts the MCP servers with the Akeyless CLI. Servers that you add to its configuration file work in Claude Desktop chats and in the **Code** tab. To add them:

1. In Claude Desktop, go to **Settings** > **Developer** > **Edit Config**.
2. Add the configuration for the servers that you want, as shown in the following example.
3. Save the file, and then fully quit and restart Claude Desktop.

The file is at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS, and at `%APPDATA%\Claude\claude_desktop_config.json` on Windows.

The following configuration adds both MCP servers. Keep only the servers that you need:

```json
{
  "mcpServers": {
    "akeyless": {
      "command": "akeyless",
      "args": [
        "mcp",
        "--profile", "<profile-name>",
        "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
      ]
    },
    "akeyless-ara": {
      "command": "akeyless",
      "args": [
        "mcp-runtime-authority",
        "--profile", "<profile-name>",
        "--gateway-url", "https://<your-gateway-url>:8000"
      ]
    }
  }
}
```

Where:

* `--profile`: The Akeyless CLI profile that Claude uses to sign in. If the profile uses SAML or OIDC, the CLI opens your browser so that you can sign in.
* `--gateway-url`: Your Gateway URL. `akeyless mcp` takes it with `/api/v2`, and `akeyless mcp-runtime-authority` takes it without `/api/v2`. Set it here even when your CLI profile already has a Gateway URL, because the MCP servers don't read the Gateway URL from the profile.

### Connect Claude Code

Claude Code adds MCP servers with the `claude mcp add` command. To add both servers, run the following commands:

```shell
claude mcp add --scope user akeyless -- akeyless mcp --profile <profile-name> --gateway-url https://<your-gateway-url>:8000/api/v2
claude mcp add --scope user akeyless-ara -- akeyless mcp-runtime-authority --profile <profile-name> --gateway-url https://<your-gateway-url>:8000
```

Where:

* `--scope user`: Makes the servers available in all your projects. Use `--scope project` to share them with your team through the project's `.mcp.json` file.
* Everything after `--`: The Akeyless CLI command that Claude Code runs, as described in [Connect Claude Desktop](#connect-claude-desktop).

## Connect With The Akeyless Plugin

The Akeyless plugin for Claude provides the Agentic Runtime Authority MCP server without the Akeyless CLI. It signs in to Akeyless on its own, with the Authentication Method that you configure. You can install it as a Desktop extension for Claude Desktop chats, or as a Claude plugin for Cowork and Claude Code.

### Prerequisites

* Your own Gateway with Agentic Runtime Authority enabled. Agentic Runtime Authority isn't available on the public Gateway. Akeyless AI Insights must also be enabled at the account level and on the Gateway. See [Agentic Runtime Authority Prerequisites](https://docs.akeyless.io/docs/agentic-runtime-authority#prerequisites).
* A Dynamic Secret, Rotated Secret, or Static Secret configured for Agentic Runtime Authority.
* An Access Role with the Agentic Runtime Authority **Allow Access** rule on those secret paths, associated with an API Key, SAML, OIDC, Universal Identity, JWT, AWS IAM, Azure AD, or GCP Authentication Method.
* For the Claude plugin and the npm package, Node.js `18` or later. The Desktop extension doesn't need it.

### Install The Desktop Extension

The Desktop extension is the easiest way to connect Claude Desktop. You install it from one file, and fill in a settings form. To install the extension:

1. Download `claude-akeyless-connector.mcpb` from the [latest release](https://github.com/akeyless-community/claude-akeyless-connector/releases/latest).
2. In Claude Desktop, go to **Settings** > **Extensions**, and drag the file onto the page.
3. Select **Install**, and then confirm.
4. Fill in the settings form, as described in the following table, and make sure that the extension is turned on.
5. Start a new chat.

The form shows the fields for every Authentication Method. Fill in **Gateway URL**, **Authentication Method**, and **Agent ID**, plus the fields that your Authentication Method uses:

| Field                     | What to enter                                                                                          |
| ------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Gateway URL**           | Your Gateway URL, for example `https://<your-gateway-url>:8000/api/v2`.                                |
| **Authentication Method** | One of `access_key`, `saml`, `oidc`, `universal_identity`, `jwt`, `aws_iam`, `azure_ad`, or `gcp`.     |
| **Access ID**             | The Access ID of your Authentication Method. Every method except `universal_identity` needs it.        |
| **Access Key**            | For `access_key` only.                                                                                 |
| **UID Token File**        | For `universal_identity` only. Defaults to `~/.akeyless/uid_rotator/uid-token`.                        |
| **JWT**                   | For `jwt` only.                                                                                        |
| **Agent ID**              | A name that identifies you in Agentic Runtime Authority session records. Defaults to `claude-desktop`. |

With `saml` or `oidc`, the first request opens your browser so that you can sign in. Claude Desktop keeps the **Access Key** and **JWT** values in your operating system's keychain.

Use the Desktop extension in Claude Desktop chats. For Cowork, install the Claude plugin instead.

### Install The Claude Plugin

The `akeyless-ara` Claude plugin runs on your computer, so it works in Claude Code and in Cowork sessions that run on your computer, but not in chats. It reads its settings from environment variables.

To install the plugin from Claude Desktop or claude.ai:

1. Go to **Customize** > **Plugins**.
2. Select **Add** > **Add marketplace**, and enter `akeyless-community/claude-akeyless-connector`.
3. Find **akeyless-ara** in the list of plugins, and add it.

The plugin is saved to your claude.ai account, so it also appears in Claude Code the next time that you start a session.

To install the plugin in Claude Code instead, run the following commands in a Claude Code session:

```text
/plugin marketplace add akeyless-community/claude-akeyless-connector
/plugin install akeyless-ara@akeyless-claude
```

After you install the plugin, set the environment variables for your Authentication Method, as described in [Plugin Environment Variables](#plugin-environment-variables), and then restart Claude Code or Claude Desktop. The following example uses an API Key Authentication Method:

```shell
export AKEYLESS_GATEWAY_URL="https://<your-gateway-url>:8000/api/v2"
export AKEYLESS_ACCESS_TYPE="access_key"
export AKEYLESS_ACCESS_ID="<access-id>"
export AKEYLESS_ACCESS_KEY="<access-key>"
export AKEYLESS_AGENT_ID="claude-code"
```

Always set `AKEYLESS_ACCESS_TYPE` and `AKEYLESS_AGENT_ID`. Claude Code warns about plugin variables that you don't set, and you can ignore the warnings for variables that your Authentication Method doesn't use.

### Configure The Plugin Manually

If your organization turns off Desktop extensions, you can add the plugin to the Claude Desktop configuration file yourself, and run it from npm. Go to **Settings** > **Developer** > **Edit Config**, add the following configuration, and then fully quit and restart Claude Desktop:

```json
{
  "mcpServers": {
    "akeyless-ara": {
      "command": "npx",
      "args": ["-y", "@akeyless-community/claude-connector"],
      "env": {
        "AKEYLESS_GATEWAY_URL": "https://<your-gateway-url>:8000/api/v2",
        "AKEYLESS_ACCESS_TYPE": "access_key",
        "AKEYLESS_ACCESS_ID": "<access-id>",
        "AKEYLESS_ACCESS_KEY": "<access-key>",
        "AKEYLESS_AGENT_ID": "claude-desktop"
      }
    }
  }
}
```

This configuration keeps the Access Key in plain text in the file. To keep it out of the file, use the Desktop extension, or an Authentication Method that doesn't need a stored secret, such as SAML, OIDC, or Universal Identity.

### Plugin Environment Variables

The Claude plugin and the npm configuration read the same environment variables. Set `AKEYLESS_GATEWAY_URL`, `AKEYLESS_ACCESS_TYPE`, and `AKEYLESS_AGENT_ID`, plus the variables for your Authentication Method:

| Authentication Method | `AKEYLESS_ACCESS_TYPE` | Variables                                   |
| --------------------- | ---------------------- | ------------------------------------------- |
| API Key               | `access_key`           | `AKEYLESS_ACCESS_ID`, `AKEYLESS_ACCESS_KEY` |
| SAML                  | `saml`                 | `AKEYLESS_ACCESS_ID`                        |
| OIDC                  | `oidc`                 | `AKEYLESS_ACCESS_ID`                        |
| Universal Identity    | `universal_identity`   | `AKEYLESS_UID_TOKEN_FILE`                   |
| JWT                   | `jwt`                  | `AKEYLESS_ACCESS_ID`, `AKEYLESS_JWT`        |
| AWS IAM               | `aws_iam`              | `AKEYLESS_ACCESS_ID`                        |
| Azure AD              | `azure_ad`             | `AKEYLESS_ACCESS_ID`                        |
| GCP                   | `gcp`                  | `AKEYLESS_ACCESS_ID`                        |

`AKEYLESS_AGENT_ID` identifies you in Agentic Runtime Authority session records. With SAML or OIDC, the first request opens your browser so that you can sign in.

## Verify The Connection

Start a new chat, and check that the Akeyless tools are available. In a chat, click **+** > **Connectors**. In Claude Code, run `/mcp`. Then try a request that matches the server that you connected:

* Vault management: "Show me my Akeyless secrets", or "List all my targets".
* Agentic Runtime Authority: "List my Akeyless ARA secrets", or "Run `SELECT count(*) FROM customers` against `/prod/db/postgres-readonly`".

Claude might ask you to approve each tool call before it runs. Agentic Runtime Authority records every execution as a session in Akeyless, including the agent and MCP identifiers. See [Monitoring Access](https://docs.akeyless.io/docs/agentic-runtime-authority#monitoring-access).

## Troubleshooting

If something doesn't work, check the following:

* If the Akeyless tools don't appear, make sure that the server, extension, or plugin is turned on, fully quit and restart Claude, and start a new chat. You can also ask Claude to use a specific tool, for example "Use the Akeyless `list-secrets` tool".
* If Claude Desktop can't start the `akeyless` command, enter the command's full path, for example `/opt/homebrew/bin/akeyless`.
* Connect Agentic Runtime Authority in one way in each Claude app. Connecting it through both the Akeyless MCP Server and the Akeyless plugin adds duplicate Akeyless tools.
* Give each user or computer its own Agent ID, so that you can tell sessions apart in the Agentic Runtime Authority reports.

### What's Next

* [MCP Server](https://docs.akeyless.io/docs/mcp)
* [Agentic Runtime Authority](https://docs.akeyless.io/docs/agentic-runtime-authority)
* [CLI Reference - mcp-runtime-authority](https://docs.akeyless.io/docs/cli-reference#mcp-runtime-authority)
* [Akeyless Connector for Claude on GitHub](https://github.com/akeyless-community/claude-akeyless-connector)
