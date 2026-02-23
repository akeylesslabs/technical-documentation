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

## Inputs

Custom Rotated Secret implementations are completely stateless. Akeyless provides encrypted storage for any user credentials, API keys, or other secret data required by a particular implementation and provides them to the custom Rotated Secret implementation with every request.

## Set Up a Custom Rotated Secret Implementation

First, you must create a [Web Target](https://docs.akeyless.io/docs/web-targets) in Akeyless. This target holds the target endpoint of your application (for example, `https://my.web.server/rotate`).

To create a [Web Target](https://docs.akeyless.io/docs/web-targets) using the Akeyless CLI, run the following command:

```shell
akeyless create-web-target -n <your web target name> \
-u https://my.web.server/rotate
```

### Authentication

> 👍 Note  
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

| Field | Description | Example |
| --- | --- | --- |
| creds | A temporary JWT token issued and signed by Akeyless that is included in the `AkeylessCreds` header of every request. |  |
| expected_access_id | The initial access ID used for the Akeyless Gateway (not the user credentials). | `"p-1234"` |
| expected_item_name | (Optional) The item name of the custom Rotated Secret. This can be helpful if a single Akeyless Gateway runs multiple custom Rotated Secrets, and the custom Rotated Secret implementation should only respond to one of them. | `"/custom-rotated-foo"` |

### Create a Custom Rotated Secret with the CLI

To create a custom Rotated Secret with the CLI, run the following command:

```shell
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

* `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `target-name`: The name of the [Web Target](https://docs.akeyless.io/docs/web-targets) with which the custom Rotated Secret should be associated.

* `authentication-credentials`: Determines how to connect to the target.
    * `use-user-creds`: Use the credentials defined on the Rotated Secret item.

* `rotator-type`: The type of credentials to be rotated. For [Web Target](https://docs.akeyless.io/docs/web-targets), should be `custom`.

* `custom-payload`: A secret payload to be sent with a rotation request.

* `custom-password-policy[=false]`: A boolean flag to set the policy for the rotated password, the endpoint must provide a new password according to the following settings:
    * `password-length`: Password length.
    * `PasswordLowercaseChar`: A boolean flag specifies whether the generated temporary password must contain at least one lowercase character from the ISO basic Latin alphabet (a to z).
    * `PasswordUppercaseChar`: A boolean flag specifies whether the generated temporary password must contain at least one uppercase character from the ISO basic Latin alphabet (A to Z).
    * `PasswordRequireNumbers`: A boolean flag specifies whether the generated temporary password must contain at least one numeric character (0 to 9)
    * `PasswordRequireSymbols`: A boolean flag specifies whether the generated temporary password must contain at least one of non-alphanumeric characters. For example, "! @ # $".

* `auto-rotate`: Enable auto-rotation if you need to update the password regularly. If this value is set to **true**, specify the `rotation-interval` in days.

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#p-stylecolorbluecustomp) section.

## Working Example: Rotate an On‑Premises Application Password by way of Web Target (Customer R/S)

This section provides an end-to-end, working example of creating a customer **Rotated Secret (R/S)** using a **Web Target** and a customer-managed **rotator endpoint**.

> **Scenario:** You have an on‑premises application that uses a local service account `svc-reporting`. You want Akeyless to rotate that password on a schedule. Because the application is not natively integrated, you expose an internal HTTPS endpoint that can update the password in the application.

### Architecture & Flow (High Level)

1. Akeyless Gateway triggers rotation (scheduled or manual).
2. Gateway calls the **Web Target** endpoint (your rotator service).
3. Rotator service:
   * Validates `AkeylessCreds` JWT (recommended).
   * Authenticates to the on‑premises app/admin API using the current credential.
   * Sets a new password.
4. Rotator service returns the new password to Akeyless.
5. Akeyless stores a new secret version; applications retrieve the latest value.

### Prerequisite

A rotator service must be created that the Akeyless Gateway can cell by HTTPS endpoint. The creation and maintenance of the rotator service is dependent on the application and your responsibility.

### Step 1: Create the Web Target (Example)

```shell
akeyless create-web-target -n my-rotator-target -u https://rotator.internal.example.com/rotate
```

### Step 2: Implement the Rotator Endpoint (Guidance)

Your rotator endpoint must:

* Accept HTTPS requests from the gateway
* Validate the `AkeylessCreds` JWT (recommended)
* Perform the actual rotation in the target system
* Return a success response with the new rotated value

#### Request Validation (Recommended)

Every request includes:

* Header: `AkeylessCreds: <jwt>`

Validate the JWT using:

```http
POST auth.akeyless.io/validate-producer-credentials
{
  "creds": "<redacted jwt token>",
  "expected_access_id": "<gateway-access-id>",
  "expected_item_name": "/<path-to-rotated-secret>"
}
```

### Step 3: Create the Custom Rotated Secret (Example)

This example creates a rotated secret named `reporting-app-svc` and enables auto-rotation every 30 days.

```shell
akeyless rotated-secret create custom \
--name reporting-app-svc \
--gateway-url 'https://gw.internal.example.com:8000' \
--target-name my-rotator-target \
--authentication-credentials use-user-creds \
--password-length 16 \
--rotator-type custom \
--custom-payload '{
  "target_system": "reporting-app",
  "account_id": "svc-reporting"
}' \
--auto-rotate true \
--rotation-interval 30
```

### Step 4: Test and Verify

1. Confirm the rotated secret item exists in Akeyless.
2. Trigger a rotation according to your operational procedure.
3. Verify:
   * A new version is created in Akeyless.
   * The on‑premises application accepts the new password.
4. Ensure the rotator endpoint logs show:
   * JWT validation succeeded
   * Password change succeeded
   * Response returned to gateway (do **not** log plaintext secrets)
