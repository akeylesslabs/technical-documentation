---
title: OpenAI Dynamic Secrets
deprecated: false
hidden: false
metadata:
  robots: index
---
You can use Akeyless Dynamic Secrets to generate short-lived credentials that let you securely connect to [OpenAI](https://openai.com/) — no need to store or manage long-term API keys or worry about them being exposed.

## Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview#/)
* an [Admin API Key](https://platform.openai.com/docs/api-reference/admin-api-keys)

## Create an OpenAI Dynamic Secret with the CLI

> ✅ **Tip:** We recommend using Dynamic Secrets with Targets. While it saves time for multiple secret-level configurations by not requiring you to provide an inline connection string each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.

To create a Dynamic Secret for OpenAI with the CLI using an existing OpenAI target, run the following command:

```shell
akeyless dynamic-secret create openai \
--name <New Secret Name> \
--target-name <Target Name> \
--project-id <Project ID>
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

Or using an inline connection string:

```shell
akeyless dynamic-secret create openai \
--name <New Secret Name> \
--api-key-id <Admin API key ID> \
--api-key <Admin API key> \
--org-id <organization ID> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

Where:

* `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

* `target-name`: A name of the target that enables connection to the OpenAI account. The name can include the path to the virtual folder where this target resides.

* `project-id`: The project in OpenAI where the API Ket will be created in.

* `gateway-url`: Akeyless Gateway URL (port `8000`).

### Inline Connection String

* `api-key-id`: The **ID** of the Admin API Key.

* `api-key`: The Admin API Key that will be used to create the API Key.

* `org-id`: The organization ID.

* `open-ai-url`: The endpoint for the OpenAI API

## Create a Dynamic OpenAI Secret in the Akeyless Console

> ✅ **Tip:** To start working with Dynamic Secrets from the Akeyless Console, you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items**, then **New**, then **Dynamic Secret**.

2. Select the **OpenAI** secret type and click **Next**.

3. Define a Name of the dynamic secret, and specify the Location as a path to the virtual folder where you want to create the new dynamic secret, using slash / separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

    * **Delete Protection:** When enabled, protects the secret from accidental deletion.

    * **Target mode:** In this section, you can either select an existing OpenAI Target or specify details of the target OpenAI account explicitly.

        * Use the **Choose an existing target** drop-down list to select the existing OpenAI Target.
        * Check the **Explicitly specify target properties** to provide details of the target OpenAI account in the next step.

    * **Project ID:** The Project ID where the new API Key will be created.

    * **User TTL**: Provide a time-to-live value for a dynamic secret. When TTL expires, the token becomes obsolete.

    * **Gateway**: Select the Gateway through which the dynamic secret will create users.

    * **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge#/).

5. If you checked **Explicitly specify target properties**, click **Next**.

6. Provide details of the target OpenAI account:

    * **API Key:** The Admin API Key that will be used to create the API Key.

    * **API Key ID:** The **ID** of the Admin API Key.

    * **Organization ID:** The Organization where that API Key will be created.

    * **OpenAI URL:** The endpoint for the OpenAI API
