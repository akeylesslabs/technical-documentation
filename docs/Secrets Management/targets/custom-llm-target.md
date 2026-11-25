---
title: Custom LLM Provider Target
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define a **Custom LLM Provider** target to connect any OpenAI-compatible LLM provider—such as LiteLLM, Mistral, vLLM, NVIDIA NIM, OpenRouter, Groq, or Together—for use with [AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight) and [Agentic Runtime Authority](https://docs.akeyless.io/docs/agentic-runtime-authority), when the provider isn't one of the dedicated targets ([OpenAI](https://docs.akeyless.io/docs/openai-target), [Claude](https://docs.akeyless.io/docs/claude-target), [Gemini](https://docs.akeyless.io/docs/gemini-target), [Grok](https://docs.akeyless.io/docs/grok-target), [Bedrock](https://docs.akeyless.io/docs/bedrock-target)).

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

## Using a Custom LLM Provider Target for AI Insights

When you add a model in **Gateway Management > AI settings**, the model field behaves differently depending on the target type:

- For the dedicated LLM targets, the model is chosen from a provider-specific dropdown.
- For a **Custom LLM Provider** target, the model field is free text, since the Gateway has no fixed model list for an arbitrary provider.

The model name is limited to 256 characters, using only letters, digits, and the characters `. _ : / @ + -`. A name that doesn't meet these rules is rejected with a `400` error before any request is sent to the provider.

On save, the Gateway sends a single test request to `{URL}/chat/completions` with the entered model and a short message, using only the `model` and `messages` fields so that providers which reject optional parameters still pass. The save only completes if the provider returns a successful response with a completion; otherwise the save is blocked and the provider's HTTP status and error message are shown. The same test runs again whenever you update the model or target on an existing entry.

Each test call writes an audit log line with the caller, target, host, and result.

To add or update a model from the CLI, run:

```shell
akeyless gateway create ai-model \
  --target-name <Custom LLM Provider target name> \
  --model-name <model name> \
  --role <default|quorum>
```

```shell
akeyless gateway update ai-model \
  --target-name <Custom LLM Provider target name> \
  --model-name <model name> \
  --role <default|quorum>
```

For general setup of AI Insights at the account and gateway level, see [Akeyless AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight).

<br />
