---
title: OpenAI Target
deprecated: false
hidden: true
metadata:
  robots: index
---
You can define an [OpenAI](https://openai.com/) target to be used with [OpenAI Dynamic Secret](https://docs.akeyless.io/update/docs/openai-dynamic-secrets#/).

# Create an OpenAI Target in the CLI

To create an OpenAI target from the CLI, run the following command:

```shell
akeyless target create openai \
--name <target name> \
--api-key-id <Admin API key ID> \
--api-key <Admin API key> \
--org-id <organization ID> \
--open-ai-url[=https://api.openai.com/v1] <The endpoint for the OpenAI API>     
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `api-key-id`: The **ID** of the Admin API Key.

* `api-key`: The Admin API Key that will be used in order to create the API Key.

* `org-id`: The organization ID.

* `open-ai-url`: The endpoint for the OpenAI API

# Create an OpenAI Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > AI (OpenAI)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
   For more information, [read here](doc:implement-zero-knowledge).

4. Define the remaining parameters as follows:

* **API Key:** The Admin API Key that will be used in order to create the API Key.

* **API Key ID:** The **ID** of the Admin API Key.

* **Organization ID:** The Organization where that API Key will be created.

* **OpenAI URL:** The endpoint for the OpenAI API
