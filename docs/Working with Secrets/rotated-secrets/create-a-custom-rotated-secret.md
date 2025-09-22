---
title: Custom Rotated Secret
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
Akeyless supports Rotated Secrets for a growing number of services. Suppose you need to integrate with a service that is not yet natively implemented in Akeyless. In that case, you can create a custom Rotated Secret implementation that calls the service on demand to rotate secrets. 

Akeyless communicates with custom Rotated Secret implementations over `HTTP` and delegates the `rotate` operation to the external services using a particular `HTTP` endpoint that follows a specific input/output format.

Once you have set up a custom Rotated Secret implementation, you can create a custom Rotated Secret that calls the implementation to rotate credentials.

# Inputs

Custom Rotated Secret implementations are completely stateless. Akeyless provides encrypted storage for any user credentials, API keys, or other secret data required by a particular implementation and provides them to the custom Rotated Secret implementation with every request.

# Set Up a Custom Rotated Secret Implementation

First, you must create a [Web Target](doc:web-targets) in Akeyless. This target holds the target endpoint of your application (e.g., `https://my.web.server/rotate` endpoint).

To create a [Web Target](doc:web-targets) using the Akeyless CLI, run the following command:

```shell Akeyless CLI
akeyless create-web-target -n <your web target name> \
-u https://my.web.server/rotate
```

## Authentication

> 👍 Note
> 
> Custom Rotated Secret implementations should only handle requests from a known Akeyless Gateway instance. Every request made by Akeyless to a custom Rotated Secret implementation includes an `AkeylessCreds` header with a temporary JWT token issued and signed by Akeyless.

Use the following endpoint to verify all requests:

```http
POST auth.akeyless.io/validate-producer-credentials
{
  "creds": "<redacted jwt token>",
  "expected_access_id": "p-1234",
  "expected_item_name": "/custom-rotated-foo",
}
```

Where:

| Field              | Description                                                                                                                                                                                                                    | Example                 |
| :----------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------- |
| creds              | A temporary JWT token issued and signed by Akeyless that is included in the `AkeylessCreds` header of every request.                                                                                                           |                         |
| expected_access_id | The initial access ID used for the Akeyless Gateway (not the user credentials).                                                                                                                                                | `"p-1234"`              |
| expected_item_name | (Optional) The item name of the custom Rotated Secret. This can be helpful if a single Akeyless Gateway runs multiple custom Rotated Secrets, and the custom Rotated Secret implementation should only respond to one of them. | `"/custom-rotated-foo"` |

## Create a Custom Rotated Secret from the CLI

To create a custom Rotated Secret from the CLI, run the following command: 

```shell Akeyless CLI
akeyless rotated-secret create custom \
--name <Rotated Secret name>
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--target-name <Web Target item name> \
--authentication-credentials <use-user-creds> \
--password-length 16
--rotator-type custom \
--custom-payload <Secret payload to be sent with rotation request> \
--auto-rotate <true|false> \
--rotation-interval <1-365>
```

Where:

- `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

- `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

- `target-name`: The name of the [Web Target](doc:web-targets) with which the custom Rotated Secret should be associated.

- `authentication-credentials`: Determines how to connect to the target.
  - `use-user-creds`: Use the credentials defined on the Rotated Secret item.

- `rotator-type`: The type of credentials to be rotated. For [Web Target](doc:web-targets), should be `custom`.

- `custom-payload`: A secret payload to be sent with a rotation request.

- `custom-password-policy[=false]`: A boolean flag to set the policy for the rotated password, the endpoint must provide a new password according to the following settings:
  - `password-length`:  Password length.
  - `PasswordLowercaseChar`: A boolean flag specifies whether the generated temporary password must contain at least one lowercase character from the ISO basic Latin alphabet (a to z).
  - `PasswordUppercaseChar`: A boolean flag specifies whether the generated temporary password must contain at least one uppercase character from the ISO basic Latin alphabet (A to Z).
  - `PasswordRequireNumbers`: A boolean flag specifies whether the generated temporary password must contain at least one numeric character (0 to 9)
  - `PasswordRequireSymbols`: A boolean flag specifies whether the generated temporary password must contain at least one of non-alphanumeric characters. i.e. "! @ # $".

- `auto-rotate`: Enable auto-rotation if you need to update the password regularly. If this value is set to **true**, specify the `rotation-interval` in days.

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#p-stylecolorbluecustomp) section.