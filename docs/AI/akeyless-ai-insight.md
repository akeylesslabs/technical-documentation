---
title: Akeyless AI Insights
deprecated: false
hidden: false
metadata:
  robots: index
---
### Overview

Akeyless AI Insights enables natural-language interaction with the Akeyless platform using Large Language Models (LLMs).
To operate, AI Insights must be configured at:

1. Account level - feature enablement
2. Gateway level - specify LLM target + model

Supported LLM Providers

* OpenAI (GPT models)

### Prerequisites

Before you begin, ensure you have:

* Akeyless CLI installed & authenticated (admin access)\
* LLM Provider account + API Key
  * OpenAI — [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
* Akeyless Gateway running
* Ability to create and manage Targets in Akeyless
* Protection key available (for encrypting API credentials)

### High-Level Steps

| Step | Description                         | Tool     |
| ---- | ----------------------------------- | -------- |
| 1    | Enable AI Insights at account level | CLI      |
| 2    | Create OpenAI Target                | CLI      |
| 3    | Configure Gateway for AI Insights   | REST API |
| 4    | Validate configuration & test       | CLI / UI |

<br />

Step 1 - Enable AI Insights (Account Level)

```shell
akeyless update-account-settings \
  --enable-ai-insights true
```

To verify:

```shell
akeyless get-account-settings
```

Expected result contains:

```shell
"ai_insights": { "enable": true }
```

To disable:

```shell
akeyless update-account-settings --enable-ai-insights false
```

Step 2 - Create LLM Target

Option A - OpenAI Target

<Image border={false} src="https://files.readme.io/df738f5faf06a3befb13f4f8a90ec9445814754171e5f2b2228df221a140103b-AccountLevel.png" />

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

### Verification

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
