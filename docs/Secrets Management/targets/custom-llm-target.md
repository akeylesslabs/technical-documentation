---
title: Custom LLM Provider Target
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define a **Custom LLM Provider** target to connect any OpenAI-compatible LLM provider-such as LiteLLM, Mistral, vLLM, NVIDIA NIM, OpenRouter, Groq, or Together-for use with [AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight) and [Agentic Runtime Authority](https://docs.akeyless.io/docs/agentic-runtime-authority), when the provider isn't one of the dedicated targets ([OpenAI](https://docs.akeyless.io/docs/openai-target), [Claude](https://docs.akeyless.io/docs/claude-target), [Gemini](https://docs.akeyless.io/docs/gemini-target), [Grok](https://docs.akeyless.io/docs/grok-target), [Bedrock](https://docs.akeyless.io/docs/bedrock-target)).

Requests to the provider use the OpenAI-compatible chat completions format: `POST {URL}/chat/completions` with an `Authorization: Bearer {API Key}` header.

## URL Requirements

The provider URL must:

- Use `http` or `https`
- Be a base URL only, without a query string, fragment, or user info (the `/chat/completions` path is appended automatically)
- Not resolve to a loopback, link-local, multicast, unspecified, or cloud metadata-service address

Private and internal network addresses are allowed, since custom LLM providers are often reachable only from inside your network.

## Create a Custom LLM Provider Target with the CLI

To create a Custom LLM Provider target with the CLI, run the following command:

```shell
akeyless target create custom-llm \
  --name <target name> \
  --custom-llm-url <Custom LLM provider base URL> \
  --api-key <Custom LLM provider API key> \
  --key <protection key>
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
- `custom-llm-url`: The provider base URL, for example `https://llm.company.com/v1`.
- `api-key`: The provider API key, sent as `Authorization: Bearer`.
- `key`: The protection key used to encrypt the target secret value. If not specified, the account default protection key is used.

On save, Akeyless validates that the URL is well-formed and the API key isn't empty. No test call is made at this stage, since no model has been selected yet.

## Create a Custom LLM Provider Target in the Console

1. Log in to the Akeyless Console, and go to **Targets** > **New** > **AI (Custom LLM Provider)**.
2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
   For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).
4. Define the remaining parameters as follows:
   - **URL**: The provider base URL, for example `https://llm.company.com/v1`.
   - **API Key**: The provider API key.

##
