---
title: Claude
excerpt: Connect Claude to Akeyless
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
slug: mcp-claude-desktop
---
Connect Claude Desktop to the Akeyless Model Context Protocol (MCP) Server when you want Claude Desktop to access Akeyless tools through MCP.

For general MCP background and command syntax, see [MCP Server](https://docs.akeyless.io/docs/mcp).

## Requirements

* Akeyless CLI version `1.130.0` or later.
* A configured Akeyless profile, or the authentication values required by your chosen access type.
* A Gateway URL passed directly in the client configuration.

## Configure Claude Desktop

1. Install and configure the Akeyless CLI.
2. Edit `~/Library/Application Support/Claude/claude_desktop_config.json`.
3. Add the Akeyless MCP server configuration.
4. Restart Claude Desktop.

The following examples show common authentication configurations:

```json Default
{
  "mcpServers": {
    "akeyless": {
      "command": "akeyless",
      "args": [
        "mcp",
        "--profile", "<profile-name>",
        "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
      ]
    }
  }
}
```
```json SAML
{
  "mcpServers": {
    "akeyless-saml": {
      "command": "akeyless",
      "args": [
        "mcp",
        "--access-id", "<access-id>",
        "--access-type", "saml",
        "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
      ]
    }
  }
}
```
```json OIDC
{
  "mcpServers": {
    "akeyless-oidc": {
      "command": "akeyless",
      "args": [
        "mcp",
        "--access-id", "<access-id>",
        "--access-type", "oidc",
        "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
      ]
    }
  }
}
```

Akeyless exposes two separate MCP entry points:

- `mcp` - Managing Akeyless itself - browsing, reading, and writing vault objects
- `mcp-runtime-authority` - execute actions on resources, without exposing secrets to the model

## Verify The Integration

After Claude Desktop restarts, verify that Claude can run MCP-backed requests such as:

* "Show me my Akeyless secrets"
* "List all my targets"
* "Create a new secret called `api-key`"

## Notes

* The Akeyless CLI serves MCP over `stdio`, so Claude Desktop must invoke the `akeyless mcp` command directly.
* When `--profile` is used, the saved CLI profile supplies the authentication settings.
* Pass `--gateway-url` directly in the Claude Desktop configuration even when the profile already has a saved Gateway value.

<br />

<br />

# Claude

Connect Claude to Akeyless.

Connect Claude to Akeyless so Claude can work with your Akeyless items, or run database queries and cloud actions without ever seeing your credentials. Claude connects to Akeyless through MCP servers, and you can set them up in several ways. This page starts with the quickest method and moves on to the methods that need more setup.

## Akeyless MCP Servers

Akeyless offers two MCP servers. Each one gives Claude a different set of tools, and most people need only one of them:

|                          | Vault management                                     | Agentic Runtime Authority                                                                                                            |
| ------------------------ | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **What Claude can do**   | Browse, read, create, and update your Akeyless items | Run database queries and cloud actions. The Gateway uses the credentials and returns only the result, so Claude never sees a secret. |
| **Example request**      | "List my secrets under `/prod`"                      | "Count the rows in the `customers` table in prod Postgres"                                                                           |
| **Akeyless CLI command** | `akeyless mcp`                                       | `akeyless mcp-runtime-authority`                                                                                                     |

For more about each server, see [MCP Server](https://docs.akeyless.io/docs/mcp).

## Prerequisites

Every connection method needs the following:

* An Akeyless Gateway, and its URL.
* An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) associated with an [Access Role](https://docs.akeyless.io/docs/rbac) that grants access to the items Claude should use.

To use Agentic Runtime Authority, you also need:

* Your own Gateway with Agentic Runtime Authority enabled. Agentic Runtime Authority isn't available on the public Gateway. Akeyless AI Insights must also be enabled at the account level and on the Gateway. See [Agentic Runtime Authority Prerequisites](https://docs.akeyless.io/docs/agentic-runtime-authority#prerequisites).
* A Dynamic Secret, Rotated Secret, or Static Secret configured for Agentic Runtime Authority.
* An Access Role with the Agentic Runtime Authority **Allow Access** rule on those secret paths.

## Choose A Connection Method

The following table lists the connection methods, from the quickest to set up to the most hands-on:

| Method                                                                                  | Works in                                                                                     | MCP servers               | Requires the Akeyless CLI | What you need                                                                                                         |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------- | ------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [Custom connector](#connect-claude-on-the-web)                                          | Claude on the web, Claude Desktop, Cowork, and Claude Code, including Claude Code on the web | Both                      | No                        | A Gateway that Claude can reach over the internet, an Akeyless token, and the **Request headers** option in claude.ai |
| [Desktop extension](#install-the-desktop-extension)                                     | Claude Desktop chats                                                                         | Agentic Runtime Authority | No                        | One file that you download                                                                                            |
| [Configuration file with the Akeyless CLI](#edit-the-claude-desktop-configuration-file) | Claude Desktop chats and the **Code** tab                                                    | Both                      | Yes, `1.144.0` or later   | A CLI profile                                                                                                         |
| [Configuration file with npm](#edit-the-claude-desktop-configuration-file)              | Claude Desktop chats and the **Code** tab                                                    | Agentic Runtime Authority | No                        | Node.js `18` or later                                                                                                 |
| [Claude plugin](#install-the-claude-plugin)                                             | Claude Code and Cowork                                                                       | Agentic Runtime Authority | No                        | Node.js `18` or later, and environment variables                                                                      |
| [Claude Code with the Akeyless CLI](#add-the-servers-to-claude-code-without-the-plugin) | Claude Code                                                                                  | Both                      | Yes, `1.144.0` or later   | A CLI profile                                                                                                         |

Use the following guidelines to pick a method:

* To try Akeyless in Claude quickly, or to use it in Claude on the web, add a custom connector. Its token expires, so you replace it from time to time.
* For everyday use in Claude Desktop, install the Desktop extension. It signs in for you, and you don't need the Akeyless CLI.
* To manage Akeyless items from Claude Desktop or Claude Code, install the [Akeyless CLI](https://docs.akeyless.io/docs/cli), and add it to the configuration file or with `claude mcp add`. Without the CLI, vault management is available only through the Gateway URL, as in a custom connector.
* For Claude Code and Cowork, install the Claude plugin.

## Connect Claude On The Web

A custom connector links Claude to an MCP server on your Gateway. You add it once in claude.ai, and Claude can then use it in Claude on the web, Claude Desktop, Cowork, and Claude Code. It's the quickest way to connect, and the only method that works in Claude on the web.

Before you start, make sure you have:

* A Gateway that Claude can reach over HTTPS. Claude connects from Anthropic's cloud, not from your computer. If your Gateway is on a private network, allow [Anthropic's IP addresses](https://platform.claude.com/docs/en/api/ip-addresses) through your firewall.
* The **Request headers** option in the claude.ai **Add custom connector** dialog. This option is in beta, and it isn't available to every organization yet.
* An Akeyless token. To copy your own token, log in to the Akeyless Console, click your user avatar, and select **Copy Token**. To create a token for a dedicated Authentication Method, run `akeyless auth --access-id <access-id> --access-key <access-key>`.

Akeyless tokens are short-lived, so plan for how you replace them:

<Callout icon="⚠️" theme="warning">
  ### Warning

  An Akeyless token expires after 60 minutes by default, and an administrator can extend the token lifetime of an Authentication Method up to 12 hours. Claude can't change the token of an existing connector, so when the token expires, remove the connector and add it again with a new token.
</Callout>

To add the connector on a Free, Pro, or Max plan:

1. In claude.ai or Claude Desktop, go to **Customize** > **Connectors**.
2. Click **Add**, and then select **Add custom connector**.
3. Enter a name, such as `Akeyless`, and the URL of the MCP server you want, as described in the following table. Then click **Continue**.
4. Under **Authentication**, select **No sign-in**.
5. Under **Request headers**, select the `authorization` header, and enter `Bearer` followed by a space and your token, for example `Bearer t-1a2b3c4d`.
6. Click **Add**.

Each MCP server has its own URL on your Gateway:

| MCP server                | URL                                       |
| ------------------------- | ----------------------------------------- |
| Vault management          | `https://<your-gateway-url>:8000/mcp`     |
| Agentic Runtime Authority | `https://<your-gateway-url>:8000/ara-mcp` |

To use both servers, add a connector for each URL.

On Team and Enterprise plans, an Owner adds the connector in **Organization settings** > **Connectors**, by selecting **Add** > **Custom** > **Web** and following the same steps. Members then go to **Customize** > **Connectors**, find the connector, and click **Connect**. Every member shares the token that the Owner entered, so create it from an Authentication Method whose Access Role grants only what Claude needs.

To use the connector in a chat, click **+** > **Connectors**, and turn on the Akeyless connector. The connector is also available in Claude Desktop and Cowork, and in Claude Code when you sign in with your claude.ai account.

### Use Akeyless In Claude Code On The Web

Claude Code on the web brings in the connectors from your claude.ai account, so a custom connector works in cloud sessions with no extra setup. Connector traffic goes through Anthropic's servers, so you don't need to change the network access of your cloud environment.

If you can't add a custom connector, add your Gateway to your repository instead. Claude Code on the web loads the MCP servers that the repository's `.mcp.json` file lists:

1. Add a `.mcp.json` file to the root of your repository, as shown in the following example, and commit it.
2. Edit the [cloud environment](https://code.claude.com/docs/en/cloud-environments#configure-your-environment) that your sessions use:
   * Set **Network access** to **Custom**, and add your Gateway's host name to **Allowed domains**.
   * Under **Environment variables**, add `AKEYLESS_TOKEN=<your-token>`.
3. Start a new session with the repository.

The following `.mcp.json` file connects both MCP servers. Keep only the servers that you need:

```json
{
  "mcpServers": {
    "akeyless": {
      "type": "http",
      "url": "https://<your-gateway-url>:8000/mcp",
      "headers": {
        "Authorization": "Bearer ${AKEYLESS_TOKEN}"
      }
    },
    "akeyless-ara": {
      "type": "http",
      "url": "https://<your-gateway-url>:8000/ara-mcp",
      "headers": {
        "Authorization": "Bearer ${AKEYLESS_TOKEN}"
      }
    }
  }
}
```

Anyone who uses the cloud environment can read its environment variables. When the token expires, update `AKEYLESS_TOKEN` in the environment, and start a new session.

## Connect Claude Desktop

Claude Desktop runs the Akeyless MCP servers on your computer, so Claude reaches your Gateway from your own network. Start with the Desktop extension. Use the configuration file when you need vault management, or when you prefer the Akeyless CLI.

### Install The Desktop Extension

The Desktop extension is the easiest way to connect Claude Desktop to Agentic Runtime Authority. You install it from one file, fill in a settings form, and you don't need the Akeyless CLI. To install the extension:

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

Use the Desktop extension in Claude Desktop chats. For Cowork, install the [Claude plugin](#install-the-claude-plugin) instead.

### Edit The Claude Desktop Configuration File

Use the configuration file to connect vault management, or to run either server with the Akeyless CLI. Servers that you add to this file work in Claude Desktop chats and in the **Code** tab. To edit the file:

1. In Claude Desktop, go to **Settings** > **Developer** > **Edit Config**.
2. Add the configuration for the servers that you want, as shown in the following examples.
3. Save the file, and then fully quit and restart Claude Desktop.

The file is at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS, and at `%APPDATA%\Claude\claude_desktop_config.json` on Windows.

To run the servers with the [Akeyless CLI](https://docs.akeyless.io/docs/cli), install CLI version `1.144.0` or later, and add the following configuration. Keep only the servers that you need:

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

* `--profile`: The Akeyless CLI profile that Claude uses to sign in. Instead of a profile, you can pass `--access-id` and `--access-type`. With `--access-type saml` or `--access-type oidc`, the CLI opens your browser so that you can sign in.
* `--gateway-url`: Your Gateway URL. `akeyless mcp` takes it with `/api/v2`, and `akeyless mcp-runtime-authority` takes it without `/api/v2`.

To run Agentic Runtime Authority without the Akeyless CLI, use the Akeyless connector from npm. It requires Node.js `18` or later:

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

This configuration keeps the Access Key in plain text in the file. To keep it out of the file, use the Desktop extension, or an Authentication Method that doesn't need a stored secret, such as SAML, OIDC, or Universal Identity. For the variables of the other Authentication Methods, see [Connector Environment Variables](#connector-environment-variables).

## Install The Claude Plugin

The `akeyless-ara` plugin adds Agentic Runtime Authority to Claude Code and Cowork. The plugin runs on your computer, so it works in Claude Code and in Cowork sessions that run on your computer, but not in chats. It needs Node.js `18` or later, and it reads its settings from environment variables.

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

After you install the plugin, set the environment variables for your Authentication Method, and then restart Claude Code or Claude Desktop. The following example uses an API Key Authentication Method:

```shell
export AKEYLESS_GATEWAY_URL="https://<your-gateway-url>:8000/api/v2"
export AKEYLESS_ACCESS_TYPE="access_key"
export AKEYLESS_ACCESS_ID="<access-id>"
export AKEYLESS_ACCESS_KEY="<access-key>"
export AKEYLESS_AGENT_ID="claude-code"
```

Always set `AKEYLESS_ACCESS_TYPE` and `AKEYLESS_AGENT_ID`. Claude Code warns about plugin variables that you don't set, and you can ignore the warnings for variables that your Authentication Method doesn't use.

### Connector Environment Variables

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

### Add The Servers To Claude Code Without The Plugin

If you prefer the Akeyless CLI, or you need vault management in Claude Code, add the servers with the `claude mcp add` command. This method requires the [Akeyless CLI](https://docs.akeyless.io/docs/cli) version `1.144.0` or later on the computer that runs Claude Code. To add both servers, run the following commands:

```shell
claude mcp add --scope user akeyless -- akeyless mcp --profile <profile-name> --gateway-url https://<your-gateway-url>:8000/api/v2
claude mcp add --scope user akeyless-ara -- akeyless mcp-runtime-authority --profile <profile-name> --gateway-url https://<your-gateway-url>:8000
```

Where:

* `--scope user`: Makes the servers available in all your projects. Use `--scope project` to share them with your team through the project's `.mcp.json` file.
* Everything after `--`: The Akeyless CLI command that Claude Code runs, as described in [Edit The Claude Desktop Configuration File](#edit-the-claude-desktop-configuration-file).

## Verify The Connection

Start a new chat, and check that the Akeyless tools are available. In a chat, click **+** > **Connectors**. In Claude Code, run `/mcp`. Then try a request that matches the server that you connected:

* Vault management: "Show me my Akeyless secrets", or "List all my targets".
* Agentic Runtime Authority: "List my Akeyless ARA secrets", or "Run `SELECT count(*) FROM customers` against `/prod/db/postgres-readonly`".

Claude might ask you to approve each tool call before it runs. Agentic Runtime Authority records every execution as a session in Akeyless, including the agent and MCP identifiers. See [Monitoring Access](https://docs.akeyless.io/docs/agentic-runtime-authority#monitoring-access).

## Troubleshooting

If something doesn't work, check the following:

* If the Akeyless tools don't appear, make sure that the connector, extension, or server is turned on, fully quit and restart Claude, and start a new chat. You can also ask Claude to use a specific tool, for example "Use the Akeyless `list-secrets` tool".
* If Claude Desktop can't start the `akeyless` command, enter the command's full path, for example `/opt/homebrew/bin/akeyless`.
* Connect Agentic Runtime Authority through one method in each Claude app. Using more than one method at a time adds duplicate Akeyless tools.
* Give each user or computer its own Agent ID, so that you can tell sessions apart in the Agentic Runtime Authority reports.

### What's Next

* [MCP Server](https://docs.akeyless.io/docs/mcp)
* [Agentic Runtime Authority](https://docs.akeyless.io/docs/agentic-runtime-authority)
* [CLI Reference - mcp-runtime-authority](https://docs.akeyless.io/docs/cli-reference#mcp-runtime-authority)
* [Akeyless Connector for Claude on GitHub](https://github.com/akeyless-community/claude-akeyless-connector)
