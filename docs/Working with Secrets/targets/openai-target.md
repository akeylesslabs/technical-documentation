---
title: OpenAI Target
deprecated: false
hidden: true
metadata:
  robots: index
---
You can define a RabbitMQ target to be used with OpenAI Dynamic Secret.

# Create an OpenAI Target in the CLI

To create an OpenAI target from the CLI, run the following command:

```shell
akeyless target create openai \
--name <target name> \
--api-key-id <Admin api_key_id> \
--api-key <Admin api_key> \
--org-id <Organization ID> \
--open-ai-url[=https://api.openai.com/v1] <The endpoint for the OpenAI API>     
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
* `api-key-id`: The **ID** of the Admin API Key.
* `api-key`: The Admin API Key that will be used in order to create the API Key. 
