---
title: Akeyless AI Insights
deprecated: false
hidden: true
metadata:
  robots: index
---
<br />

### Overview

Akeyless AI Insights enables natural-language interaction with the Akeyless platform using Large Language Models (LLMs).
To operate, AI Insights must be configured at:

1. Account level - feature enablement
2. Gateway level - specify LLM target + model

Supported LLM Providers

* OpenAI (GPT models)
* Google Gemini

<br />

### Prerequisites

Before you begin, ensure you have:

* Akeyless CLI installed & authenticated (admin access)\
* LLM Provider account + API Key
  * OpenAI — [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
  * Gemini — [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
* Akeyless Gateway running
* Ability to create and manage Targets in Akeyless
* Protection key available (for encrypting API credentials)

### High-Level Steps

| Step | Description                         | Tool     |
| ---- | ----------------------------------- | -------- |
| 1    | Enable AI Insights at account level | CLI      |
| 2    | Create OpenAI/Gemini Target         | CLI      |
| 3    | Configure Gateway for AI Insights   | REST API |
| 4    | Validate configuration & test       | CLI / UI |

<br />

<br />
