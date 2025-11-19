---
title: Akeyless AI Insights
deprecated: false
hidden: false
metadata:
  robots: index
---
## Overview

Akeyless AI Insights enables natural-language interaction with the Akeyless platform using Large Language Models (LLMs). To use AI Insights, it must be configured at:

1. **Account level** — Enable the feature
2. **Gateway level** — Specify the LLM target and model

### Supported LLM Providers

* OpenAI (GPT models)

## Prerequisites

Before you begin, ensure you have the following:

* Akeyless CLI installed and authenticated with admin access
* LLM Provider account and API Key
  * OpenAI — [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
* Akeyless Gateway running
* Ability to create and manage Targets in Akeyless
* Protection key available for encrypting API credentials

## High-Level Setup Steps

| Step | Description                                    | Tool       |
| ---- | ---------------------------------------------- | ---------- |
| 1    | Enable AI Insights at the account level        | CLI        |
| 2    | Create an OpenAI Target                        | CLI        |
| 3    | Configure the Akeyless Gateway for AI Insights | REST API   |
| 4    | Validate the configuration and test            | CLI or GUI |

### Step 1: Enable AI Insights at the Account Level

To enable AI Insights, run the following command:

```shell
akeyless update-account-settings --enable-ai-insights true
```

To verify that AI Insights is enabled, run the following command:

```shell
akeyless get-account-settings
```

The output should contain:

```shell
"ai_insights": { "enable": true }
```

<Callout icon="📘" theme="info">
  To disable AI Insights, run the following command:

  `akeyless update-account-settings --enable-ai-insights false`
</Callout>

Text.

<Image border={false} src="https://files.readme.io/df738f5faf06a3befb13f4f8a90ec9445814754171e5f2b2228df221a140103b-AccountLevel.png" />

### Step 2: Create an OpenAI Target

This section describes how to create an OpenAI target for use with AI Insights.

### Command Syntax

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

#### Example

The following example creates an OpenAI target named `my-openai-target` with the GPT-4 model:

```shell
akeyless target create openai \
  --name my-openai-target \
  --api-key sk-xxxx \
  --model gpt-4
```

### Find the Target ID

To retrieve the target ID, run the following command:

```shell
akeyless get-target --name <target-name>
```

### Model Requirements

OpenAI models must use the `gpt-` prefix. The following are valid examples:

* gpt-4
* gpt-3.5-turbo

Option A - OpenAI Target

<br />

Command

```shell
akeyless target create openai \
  --name <target-name> \
  --api-key <openai-api-key> \
  [--openai-url <base-url>] \
  [--model <default-model>] \
  [--organization-id <org-id>] \
  [--key <protection-key>]
```

Example

```shell
akeyless target create openai \
  --name my-openai-target \
  --api-key sk-xxxx \
  --model gpt-4
```

Find Target ID

```shell
akeyless get-target --name <target-name>
```

Model Rules

| Provider | Valid Prefix |
| -------- | ------------ |
| OpenAI   | `gpt-`       |

Examples:

* gpt-4, gpt-3.5-turbo
* gpt4

Step 3 - Configure Gateway

<Image border={false} src="https://files.readme.io/3a98a777c3c391c38e6dc1818b5f6f242468d45db8ced474176d64f2e6a60076-GatewayLevel.png" />

<br />

Configuration uses the Gateway API.

```shell
TOKEN=$(akeyless auth | grep token | awk '{print $2}')

curl -X PUT "http://localhost:8000/config/ai-insights" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "cluster_identity": {
      "account_id": "a-1234567890",
      "access_id": "p-1234567890",
      "cluster_name": "my-gateway"
    },
    "ai_insights": {
      "enable": true,
      "target_name": "my-openai-target",
      "model": "gpt-4"
    }
  }'

```

To disable:

```shell
"ai_insights": { "enable": false }
```

## Verification

Verify Account Setting

```shell
akeyless get-account-settings
```

Verify Target

```shell
akeyless get-target --name my-openai-target
```

Verify Gateway Config

```shell
curl -X GET http://localhost:8000/config/ai-insights
```

Test in UI

<Image border={false} src="https://files.readme.io/9214bc7c65691ab90764917b7da86d69a6be792b3c494b6289b338aabf90f851-chatInteraction.png" />

<br />

1. Open Akeyless Web UI
2. Navigate to AI Insights
3. Start a chat
4. Ask a natural language question

Troubleshooting

| Issue                  | Resolution                   |
| ---------------------- | ---------------------------- |
| `AI Insights disabled` | Enable at account level      |
| `Gateway disabled`     | Update gateway config        |
| Invalid model          | Must use `gpt-`              |
| Invalid target         | Must be OpenAI               |
| Target not found       | Validate target name/ID      |
| Authentication failure | Re-auth with `akeyless auth` |
| Gateway unreachable    | Check port 8000 + firewall   |
| API key errors         | Check validity + base URLs   |

Configuration Checklist

| Step                  | Status |
| --------------------- | ------ |
| Enable AI Insights    | ☐      |
| Create Target         | ☐      |
| Store Target ID       | ☐      |
| Configure Gateway     | ☐      |
| Verify Gateway Config | ☐      |
| Test in UI            | ☐      |
