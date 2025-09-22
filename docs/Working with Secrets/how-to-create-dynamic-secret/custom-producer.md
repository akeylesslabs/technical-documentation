---
title: Custom Dynamic Secrets
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Akeyless supports dynamic secrets for a growing number of services. If you need to integrate with a service that is not yet natively implemented in Akeyless, you can create a custom dynamic secret implementation that calls the service on demand to generate or revoke temporary secrets. 

Akeyless communicates with custom dynamic secret implementations over HTTP, and delegates `create`  
and `revoke` operations to the external services using a particular set of HTTP endpoints that follow a specific input/output format.

Once you have set up a custom dynamic secret implementation, you can create a custom dynamic secret that calls the implementation to generate dynamic credentials.

# Inputs

Custom dynamic secret implementations are completely stateless. Akeyless provides encrypted storage for any user credentials, API keys, or other secret data required by a particular implementation, and provides them to the dynamic secret implementation with every request.

In addition, some custom dynamic secret implementations require user input every time a new secret value is requested. Akeyless accepts user input for every `get-dynamic-secret-value` operation for custom dynamic secret implementations.

# Set Up a Custom Dynamic Secret Implementation

Implement the following endpoints to integrate with Akeyless:

- **POST /sync/create**: This endpoint is called each time a user requests a dynamic secret value.
- **POST /sync/revoke**: This endpoint is called each time temporary credentials need to be revoked.
- **POST /sync/rotate**: (Optional) This endpoint is called to rotate the custom dynamic secret payload.

## POST /sync/create Input

This endpoint is called each time a user requests a dynamic secret value.

```curl
POST /sync/create
{
    "payload": "secret data stored by Akeyless",
    "input": { "user": "input" },
    "client_info": {
        "access_id": "p-1234",
        "sub_claims": {
            "claim1": ["value1"]
        }
    }
}
```

Where:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Description",
    "h-2": "Example",
    "0-0": "payload",
    "0-1": "(Optional) Secret credentials stored by Akeyless. You define these credentials when you set up the custom dynamic secret in the Akeyless Gateway.",
    "0-2": "`mongodb://user:password@host`  \n  \n`{\"user\":\"foo\",\"pass\":\"bar\"}`",
    "1-0": "input",
    "1-1": "(Optional) User input provided with the current  \n `get-dynamic-secret-value` operation. This is a JSON object, and its format depends on the information provided by the user.",
    "1-2": "`{\n  \"domain\":\"foo.example.com\",\n  \"use_staging\":true\n}`  \n  \n`{\"project_id\":42}`",
    "2-0": "client_info",
    "2-1": "Information about the user requesting the credentials. It includes the user's Akeyless access ID, as well as any sub-claims.",
    "2-2": "`{\n  \"access_id\": \"p-1234\",\n  \"sub_claims\": {\n    \"claim1\": [\"value1\"]\n  }\n}`"
  },
  "cols": 3,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


## POST /sync/create Output

```http
HTTP 200 OK
{
    "id": "<unique id>",
    "response": { <response as json object> }
}
```

Where:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Description",
    "h-2": "Example",
    "0-0": "id",
    "0-1": "A unique identifier for the temporary credentials, which is required during a \\`POST /sync/revoke' operation.",
    "0-2": "`tmp.user1234`  \n  \n`f2fa1940-8d7e-41d4-a688-8d915795e88b`",
    "1-0": "response",
    "1-1": "A JSON object that includes any fields required by the particular use case.",
    "1-2": "`{\n  \"cert\":\"<redacted>\",\n  \"private_key\":\"<redacted>\"\n}`  \n  \n`{\"password\":\"strongpassword!\"}`"
  },
  "cols": 3,
  "rows": 2,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


## POST /sync/revoke Input

This endpoint is called every time credentials need to be revoked. This can happen either when the **TTL** defined for the custom dynamic secret expires, or if an administrator explicitly requests that particular credentials are revoked.

Not every service supports revocation. If not, the operation should just return the specified IDs.

```http
POST /sync/revoke
{
    "payload": "secret data stored by Akeyless",
    "ids": ["abc", "def"]
}
```

Where:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Description",
    "h-2": "Example",
    "0-0": "payload",
    "0-1": "(Optional) Secret credentials stored by Akeyless. You define these credentials when you set up the custom dynamic secret in the Akeyless Gateway.",
    "0-2": "`mongodb://user:password@host`  \n  \n`{\"user\":\"foo\",\"pass\":\"bar\"}`",
    "1-0": "ids",
    "1-1": "A list of IDs to revoke. These IDs were previously received in response to `POST /sync/create` operations.",
    "1-2": "`[\"foo\", \"bar\"]`"
  },
  "cols": 3,
  "rows": 2,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


## POST /sync/revoke Output

```http
HTTP 200 OK
{
    "revoked": ["abc", "def"],
    "message": "id foo was not removed: user does not exist"
}
```

Where:

| Field   | Description                                                                                                                        | Example                                         |
| :------ | :--------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------- |
| revoked | A list of revoked IDs.                                                                                                             | `["foo", "bar"]`                                |
| message | An optional message in case any of the specified IDs were not properly revoked. This field should only be used for error handling. | `"id foo was not removed: user does not exist"` |

## POST /sync/rotate Input

This endpoint is called to rotate the custom producer secret payload.

```curl
POST /sync/rotate
{
    "payload": "secret data stored by Akeyless"
}
```

Where:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Description",
    "h-2": "Example",
    "0-0": "payload",
    "0-1": "Secret credentials stored by Akeyless. You define these credentials when you set up the custom dynamic secret in the Akeyless Gateway.",
    "0-2": "`mongodb://user:password@host`  \n  \n`{\"user\":\"foo\",\"pass\":\"bar\"}`"
  },
  "cols": 3,
  "rows": 1,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


## POST /sync/rotate Output

```curl
HTTP 200 OK
{
    "payload": "new payload to replace the existing one"
}
```

Where:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Description",
    "h-2": "Example",
    "0-0": "payload",
    "0-1": "New secret credentials to replace the existing credentials stored by Akeyless.",
    "0-2": "`mongodb://user:password@host`  \n  \n`{\"user\":\"mun\",\"pass\":\"goh\"}`"
  },
  "cols": 3,
  "rows": 1,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


> 👍 Note
> 
> Payload rotation is performed on a best-effort basis. The rotation process could fail, and even after a successful `/sync/rotate` request the dynamic secret could still use the old payload. For these cases, the custom dynamic secret implementation should support both the old payload and the new payload until there is at least one `/sync/create` or `/sync/revoke` request that uses the old payload.

## Authentication

Custom dynamic secret implementations should only handle requests made by a known Akeyless Gateway instance. Every request made by Akeyless to a custom dynamic implementation includes an `AkeylessCreds` header with a temporary JWT token issued and signed by Akeyless.

Use the following endpoint to verify all requests:

```http
POST auth.akeyless.io/validate-producer-credentials
{
  "creds": "<redacted jwt token>",
  "expected_access_id": "p-1234",
  "expected_item_name": "/custom-producer-foo",
}
```

Where:

| Field              | Description                                                                                                                                                                                                                    | Example                  |
| :----------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------- |
| creds              | A temporary JWT token issued and signed by Akeyless that is included in the `AkeylessCreds` header of every `POST /sync/create` and `POST /sync/revoke` request.                                                               |                          |
| expected_access_id | The initial access ID used for the Akeyless Gateway (not the user credentials).                                                                                                                                                | `"p-1234"`               |
| expected_item_name | (Optional) The item name of the custom dynamic secret. This can be helpful if a single Akeyless Gateway runs multiple custom dynamic secrets, and the custom dynamic secret implementation should only respond to one of them. | `"/custom-producer-foo"` |

## Dry-Run Mode

When you define a custom dynamic secret in the Akeyless Gateway, the gateway makes several requests to the endpoints used in the configuration to ensure that the configuration is correct. These dry-run requests include the configured secret payload and empty user input, and all use the **p-custom** user access ID. Dry-run requests are authenticated using an Akeyless Gateway access ID.

Ensure that your custom dynamic secret implementation can handle these requests without failing, even though there is no user or user input, and return a `Success` response that includes a predefined ID.

This ID is sent to the `POST /sync/revoke` endpoint, which should also be configured to handle dry-run mode correctly.

# Create a Custom Dynamic Secret from the CLI

Once you have a custom dynamic implementation that follows these specifications, create a new custom dynamic secret from the Akeyless CLI. 

To create a custom dynamic secret from the CLI, run the following command: 

```shell Akeyless CLI
akeyless dynamic-secret create \
--name <Dynamic Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--create-sync-url 'https://example.com/sync/create:Port' \
--revoke-sync-url 'https://example.com/sync/revoke:Port' \
--revoke-sync-url 'https://example.com/sync/rotate:Port'
```

Where:

- **name:** A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

- **gateway-url:** Akeyless Gateway Configuration Manager URL (port `8000`).

- **create-sync-url:** The URL of an endpoint that implements the /sync/create method. 

- **revoke-sync-url:** The URL of an endpoint that implements the /sync/revoke method.

- **rotate-sync-url:** The URL of an endpoint that implements the /sync/rotate method.

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#p-stylecolorbluecustomp) section.

> 👍 Note
> 
> To start working with dynamic secrets from the Akeyless Console, you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

# Usage Examples

You can find examples of custom dynamic secret implementations in this <a href="https://github.com/akeylesslabs/custom-producer" target="_blank">GitHub Repository</a>. 

The repository includes sample authentication code, deployment examples (using a docker image, or [AWS Lambda function](https://github.com/akeylesslabs/custom-producer/tree/master/go/echoserver#setting-up-aws-lambda), or similar) and actual dynamic secret implementations, such as [Let’s Encrypt](https://github.com/akeylesslabs/custom-producer/tree/master/go/letsencrypt).