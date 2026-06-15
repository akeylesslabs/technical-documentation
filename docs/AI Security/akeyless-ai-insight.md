---
title: Akeyless AI Insights
excerpt: Configure Akeyless AI Insights with supported LLM targets and gateway settings.
deprecated: false
hidden: false
metadata:
  title: Akeyless AI Insights
  description: Configure Akeyless AI Insights at account and gateway levels with supported LLM targets.
  robots: index
---
## Overview

Akeyless AI Insights enables natural-language interaction with the Akeyless Platform using Large Language Models (LLMs). To use AI Insights, it must be configured at:

1. **Account level** — Enable the feature
2. **Gateway level** — Specify the LLM target and model

### Supported LLM Providers

* OpenAI (GPT models)
* Gemini (Gemini models)

This guide uses **OpenAI** examples. You can also use **Gemini** by creating a Gemini target and setting a compatible model.

## Prerequisites

Before you begin, ensure you have the following:

* Akeyless CLI installed and authenticated with admin access
* LLM Provider account and API Key
    * OpenAI - [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
* Akeyless Gateway running
* Ability to create and manage Targets in Akeyless
* Protection key available for encrypting API credentials

## High-Level Setup Steps

| Step | Description | Tool |
| --- | --- | --- |
| 1 | Enable AI Insights at the account level | CLI |
| 2 | Create an OpenAI / Gemini Target | CLI |
| 3 | Configure the Akeyless Gateway for AI Insights | REST API |
| 4 | Validate the configuration and test | CLI or Console |

### Step 1: Enable AI Insights at the Account Level

To enable AI Insights, run the following command:

```shell
akeyless update-account-settings --enable-ai-insights true
```

AI Insights can also be enabled at the account level using the Akeyless Console.

![Illustration for: Step 1: Enable AI Insights at the Account Level To enable AI Insights, run the following command: AI Insights can also be enabled at the account level using the Web UI.](https://files.readme.io/df738f5faf06a3befb13f4f8a90ec9445814754171e5f2b2228df221a140103b-AccountLevel.png)

> ℹ️ **Note:** To disable AI Insights, run the following command:
>
> `akeyless update-account-settings --enable-ai-insights false`

### Step 2: Create an LLM Target

Create either an OpenAI target or a Gemini target for use with AI Insights.

For Gemini target setup details, see [Gemini Target](https://docs.akeyless.io/docs/gemini-target).

The following OpenAI examples are provided as a reference workflow.

#### Command Syntax

Use the following command to create an OpenAI target:

```shell
akeyless target create openai \
  --name <target-name> \
  --api-key <openai-api-key> \
  [--openai-url <base-url>] \
  [--model <default-model>] \
  [--organization-id <org-id>] \
  [--key <protection-key>]
```

##### Example

The following example creates an OpenAI target named `my-openai-target` with the GPT-4 model:

```shell
akeyless target create openai \
  --name my-openai-target \
  --api-key <openai-api-key> \
  --model gpt-4
```

#### Find the Target ID

To retrieve the target ID, run the following command:

```shell
akeyless get-target --name <target-name>
```

#### Model Requirements

OpenAI models must use the `gpt-` prefix. The following are valid examples:

* gpt-4
* gpt-3.5-turbo

### Step 3: Configure the Gateway

This section describes how to configure the gateway to use AI Insights.

The gateway configuration uses the Akeyless Gateway API. First, obtain an authentication token, then use the token to configure the gateway.

#### Obtain an Authentication Token

```shell
ACCESS_TOKEN=$(akeyless auth | grep token | awk '{print $2}')
```

#### Configure AI Insights on the Gateway

Use the following command to configure AI Insights on the gateway:

```shell
curl -X PUT "http://localhost:8000/config/ai-insights" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "cluster_identity": {
      "account_id": "<gateway-account-id>",
      "access_id": "<gateway-access-id>",
      "cluster_name": "<my-gateway>"
    },
    "ai_insights": {
      "enable": true,
      "target_name": "<my-openai-target>",
      "model": "<gpt-4>"
    }
  }'
```

#### Disable AI Insights on the Gateway

To disable AI Insights on the gateway, set the enable field to `false`:

```shell
"ai_insights": { "enable": false }
```

The Gateway can also be configured with the Akeyless Console.

![Illustration for: Disable AI Insights on the Gateway To disable AI Insights on the gateway, set the enable field to false: The Gateway can also be configured with the Web UI.](https://files.readme.io/3a98a777c3c391c38e6dc1818b5f6f242468d45db8ced474176d64f2e6a60076-GatewayLevel.png)

## Verification

This section describes how to verify that AI Insights is properly configured.

### Verify the Account Setting

To verify that AI Insights is enabled at the account level, run the following command:

```shell
akeyless get-account-settings
```

### Verify the Target

To verify that the OpenAI target is configured correctly, run the following command:

```shell
akeyless get-target --name my-openai-target
```

### Verify the Gateway Configuration

To verify that the gateway is configured for AI Insights, run the following command:

```shell
curl -X GET http://localhost:8000/config/ai-insights
```

#### Test in the Console

To test AI Insights in the Akeyless Console, follow these steps:

1. Open the Akeyless Console.
2. Navigate to AI Insights.
3. Start a chat session
4. Ask a natural language question.
5. Open the chat list in the left panel to review previous chats.
6. Use **Search chats** to find a specific chat in your history.

![Illustration for: 2. Navigate to AI Insights. 3. Start a chat session 4. Ask a natural language question.](https://files.readme.io/9214bc7c65691ab90764917b7da86d69a6be792b3c494b6289b338aabf90f851-chatInteraction.png)

AI Insights stores chat sessions per gateway selection so you can return to prior conversations and search them by title.

## Troubleshooting

| Issue | Resolution |
| --- | --- |
| AI Insights disabled | Enable AI Insights at the account level |
| Gateway disabled | Update gateway configuration |
| Invalid model | Ensure the model value uses the `gpt-` prefix |
| Invalid target | Ensure the target is a supported LLM target (OpenAI or Gemini) |
| Target not found | Validate the target name and ID |
| Authentication failure | Re-authenticate by running `akeyless auth` |
| Gateway unreachable | Check that port 8000 is open and firewall rules allow access |
| API Key errors | Verify the API Key is valid and check the base URL |

## Configuration Checklist

* [ ] Enable AI Insights
* [ ] Create OpenAI or Gemini target
* [ ] Store target ID
* [ ] Configure gateway
* [ ] Verify the Gateway configuration
* [ ] Test in the Console

## Related AI Guides

* [Identity and Secrets Intelligence](https://docs.akeyless.io/docs/identity-and-secrets-intelligence)
* [Agentic Runtime Authority](https://docs.akeyless.io/docs/agentic-runtime-authority)
* [MCP Server](https://docs.akeyless.io/docs/mcp)
* [Prompt Injection Protection for AI Agents](https://docs.akeyless.io/docs/prompt-injection-protection-for-ai-agents)
* [Beyond .env: Building a "Dynamic-Only" Secretless AI Agent with Google ADK](https://docs.akeyless.io/docs/beyond-env-building-a-dynamic-only-secretless-ai-agent-with-google-adk)
