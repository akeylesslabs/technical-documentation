---
title: Gemini Target
deprecated: false
hidden: true
metadata:
  robots: index
---
You can define an [Gemini](https://ai.google.dev/gemini-api/docs) target to be used for [AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight) in your account. 

## Create a Gemini Target with the CLI

To create a Gemini target with the CLI, run the following command:

```shell
akeyless target create gemini \
--name <target name> \
--api-key < Gemini API key> \
--gemini-url <Gemini API base URL>
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `api-key`: The Gemini API Key.

* `gemini-url`: The Gemini API base URL, for using the AI Insights, set: `https://generativelanguage.googleapis.com/v1beta/openai/`

## Create a Gemini Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > AI (Gemini)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
   For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

4. Define the remaining parameters as follows:

   * **API Key:** The Gemini API Key.

   * **OpenAI URL:** The endpoint for the OpenAI API - `https://generativelanguage.googleapis.com/v1beta/openai/`
