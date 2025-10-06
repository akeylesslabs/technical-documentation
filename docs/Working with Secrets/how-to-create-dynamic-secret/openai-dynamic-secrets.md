---
title: OpenAI Dynamic Secrets
deprecated: false
hidden: true
metadata:
  robots: index
---
You can use Akeyless Dynamic Secrets to generate short-lived credentials that let you securely connect to OpenAI — no need to store or manage long-term API keys or worry about them being exposed.

# Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw#/)
* an [Admin API Key](https://platform.openai.com/docs/api-reference/admin-api-keys) 

# Create a Snowflake Dynamic Secret from the CLI

<Callout icon="👍">
  Note

  We recommend using dynamic secrets with Targets. While it saves time for multiple secret-level configurations by not requiring you to provide an inline connection string each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.
</Callout>

To create a Dynamic Secret for OpenAI from the CLI using an existing OpenAI target, run the following command:

```shell
akeyless dynamic-secret create openai \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \ 
```

Or using an inline connection string:

```shell
akeyless dynamic-secret create openai \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \ 
```

Where:

# Create a Dynamic RabbitMQ Secret in the Akeyless Console

<Callout icon="👍">
  Note

  To start working with dynamic secrets from the Akeyless Console, you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.
</Callout>

1. Log in to the Akeyless Console, and go to Items > New > Dynamic Secret.
2. Select the AWS secret type and click Next.
3. Define a Name of the dynamic secret, and specify the Location as a path to the virtual folder where you want to create the new dynamic secret, using slash / separators. If the folder does not exist, it will be created together with the dynamic secret.
4. Define the remaining parameters as follows:

* Delete Protection: When enabled, protects the secret from accidental deletion.

<br />
