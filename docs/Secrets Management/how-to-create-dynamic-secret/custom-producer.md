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
Akeyless supports Dynamic Secrets for a growing number of services. If you need to integrate with a service that is not yet natively implemented in Akeyless, you can create a custom dynamic secret implementation that calls the service on demand to generate or revoke temporary secrets.

Akeyless communicates with custom dynamic secret implementations over HTTP. It delegates `create` and `revoke` operations to the external service by calling a defined set of HTTP endpoints that follow a specific input/output schema.

After you set up a custom dynamic secret implementation, you can create a custom dynamic secret that calls the implementation to generate dynamic credentials.

## Inputs

Custom dynamic secret implementations are stateless. Akeyless provides encrypted storage for any user credentials, API keys, or other secret data required by a particular implementation. Akeyless includes those values in every request to the dynamic secret implementation.

In addition, some custom dynamic secret implementations require user input every time a new secret value is requested. Akeyless accepts user input on every `get-dynamic-secret-value` operation for custom dynamic secret implementations.

## Set up a custom dynamic secret implementation

Implement the following endpoints to integrate with Akeyless:

- **POST `/sync/create`**: Called each time a user requests a dynamic secret value.
- **POST `/sync/revoke`**: Called each time temporary credentials must be revoked.
- **POST `/sync/rotate`** (optional): Called to rotate the custom dynamic secret payload.

## POST `/sync/create`

### Input

This endpoint is called each time a user requests a dynamic secret value.

```json
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

| Field | Description | Example |
| --- | --- | --- |
| `payload` | (Optional) Secret credentials stored by Akeyless. You define these credentials when you set up the custom dynamic secret in the Akeyless Gateway. | `mongodb://user:password@host`, `{"user":"foo","pass":"bar"}` |
| `input` | (Optional) User input provided with the current `get-dynamic-secret-value` operation. This is a JSON object and its schema depends on the inputs collected from the user. | `{"domain":"foo.example.com","use_staging":true}`, `{"project_id":42}` |
| `client_info` | Information about the user requesting the credentials. It includes the user's Akeyless access ID and any sub-claims. | `{"access_id":"p-1234","sub_claims":{"claim1":["value1"]}}` |

### Output

```json
HTTP 200 OK
{
  "id": "<unique id>",
  "response": { "any": "json object" }
}
```

Where:

| Field | Description | Example |
| --- | --- | --- |
| `id` | A unique identifier for the temporary credentials. This value is required during a `POST /sync/revoke` operation. | `tmp.user1234`, `f2fa1940-8d7e-41d4-a688-8d915795e88b` |
| `response` | A JSON object that includes any fields required by the specific use case. | `{"cert":"<redacted>","private_key":"<redacted>"}`, `{"password":"strongpassword!"}` |

## POST `/sync/revoke`

### Input

This endpoint is called every time credentials need to be revoked. This can happen when the **TTL** defined for the custom dynamic secret expires, or when an administrator explicitly requests that specific credentials are revoked.

Not every service supports revocation. If revocation is not supported, the operation should still return the specified IDs.

```json
POST /sync/revoke
{
  "payload": "secret data stored by Akeyless",
  "ids": ["abc", "def"]
}
```

Where:

| Field | Description | Example |
| --- | --- | --- |
| `payload` | (Optional) Secret credentials stored by Akeyless. You define these credentials when you set up the custom dynamic secret in the Akeyless Gateway. | `mongodb://user:password@host`, `{"user":"foo","pass":"bar"}` |
| `ids` | A list of IDs to revoke. These IDs were previously received in response to `POST /sync/create` operations. | `["foo","bar"]` |

### Output

```json
HTTP 200 OK
{
  "revoked": ["abc", "def"],
  "message": "id foo was not removed: user does not exist"
}
```

Where:

| Field | Description | Example |
| --- | --- | --- |
| `revoked` | A list of revoked IDs. | `["foo","bar"]` |
| `message` | Optional message if any of the specified IDs were not revoked. Use this field for error handling only. | `"id foo was not removed: user does not exist"` |

## POST `/sync/rotate` (optional)

### Input

This endpoint is called to rotate the custom dynamic secret payload.

```json
POST /sync/rotate
{
  "payload": "secret data stored by Akeyless"
}
```

Where:

| Field | Description | Example |
| --- | --- | --- |
| `payload` | Secret credentials stored by Akeyless. You define these credentials when you set up the custom dynamic secret in the Akeyless Gateway. | `mongodb://user:password@host`, `{"user":"foo","pass":"bar"}` |

### Output

```json
HTTP 200 OK
{
  "payload": "new payload to replace the existing one"
}
```

Where:

| Field | Description | Example |
| --- | --- | --- |
| `payload` | New secret credentials to replace the existing credentials stored by Akeyless. | `mongodb://user:password@host`, `{"user":"mun","pass":"goh"}` |

> **Note**
>
> Payload rotation is performed on a best-effort basis. The rotation process can fail, and even after a successful `/sync/rotate` request the dynamic secret can still use the old payload. To handle this scenario, the custom dynamic secret implementation should support both the old payload and the new payload until it receives at least one `/sync/create` or `/sync/revoke` request that uses the new payload.

## Authentication

Custom dynamic secret implementations should only handle requests made by a known Akeyless Gateway instance. Every request made by Akeyless to a custom dynamic implementation includes an `AkeylessCreds` header with a temporary JWT token issued and signed by Akeyless.

Use the following endpoint to verify all requests:

```json
POST auth.akeyless.io/validate-producer-credentials
{
  "creds": "<redacted jwt token>",
  "expected_access_id": "p-1234",
  "expected_item_name": "/custom-producer-foo"
}
```

Where:

| Field | Description | Example |
| --- | --- | --- |
| `creds` | Temporary JWT token included in the `AkeylessCreds` header of every `POST /sync/create` and `POST /sync/revoke` request. | (redacted) |
| `expected_access_id` | Initial access ID used for the Akeyless Gateway (not the end-user credentials). | `"p-1234"` |
| `expected_item_name` | (Optional) Item name of the custom dynamic secret. Use this when a single Akeyless Gateway runs multiple custom dynamic secrets and the implementation should only respond to one of them. | `"/custom-producer-foo"` |

## Dry-run mode

When you define a custom dynamic secret in the Akeyless Gateway, the gateway makes several requests to the endpoints configured for the integration. These dry-run requests include the configured secret payload and an empty user input object, and they use the **p-custom** user access ID.

Dry-run requests are authenticated using an Akeyless Gateway access ID. Ensure that your custom dynamic secret implementation can handle these requests without failing, even though there is no end user or user input. The implementation should return a success response that includes a predefined ID.

That predefined ID is sent to the `POST /sync/revoke` endpoint, which must also support dry-run behavior.

## Create a custom dynamic secret with the CLI

After you have a custom dynamic secret implementation that follows these specifications, create a custom dynamic secret from the Akeyless CLI.

```bash
akeyless dynamic-secret create   --name <Dynamic Secret Name>   --gateway-url 'https://<Your-Akeyless-GW-URL:8000>'   --create-sync-url 'https://example.com/sync/create:Port'   --revoke-sync-url 'https://example.com/sync/revoke:Port'   --rotate-sync-url 'https://example.com/sync/rotate:Port'
```

Where:

- `name`: Unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the dynamic secret, using `/` separators. If the folder does not exist, Akeyless creates it together with the dynamic secret.
- `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).
- `create-sync-url`: URL of an endpoint that implements the `POST /sync/create` operation.
- `revoke-sync-url`: URL of an endpoint that implements the `POST /sync/revoke` operation.
- `rotate-sync-url`: URL of an endpoint that implements the `POST /sync/rotate` operation.

You can find the complete list of parameters for this command in [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#p-stylecolorbluecustomp).

> **Note**
>
> To work with Dynamic Secrets from the Akeyless Console, you must configure the Gateway URL to enable communication between the Akeyless SaaS and the Akeyless Gateway.

## Usage examples

You can find examples of custom dynamic secret implementations in the [custom-producer GitHub repository](https://github.com/akeylesslabs/custom-producer).

The repository includes sample authentication code, deployment examples (for example, using a Docker image or an [AWS Lambda function](https://github.com/akeylesslabs/custom-producer/tree/master/go/echoserver#setting-up-aws-lambda)), and implementations such as [Let’s Encrypt](https://github.com/akeylesslabs/custom-producer/tree/master/go/letsencrypt).
