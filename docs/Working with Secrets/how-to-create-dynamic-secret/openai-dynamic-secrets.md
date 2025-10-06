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
