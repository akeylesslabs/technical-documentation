---
title: Ping Dynamic Secrets
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
You can create a PingFederate secret to allow users to dynamically receive short-lived authentication options to interact with a PingFederate service using an API key, a public key (private key JWT) and client certificates.

> 👍 Note
>
> We recommend using dynamic secrets with [Targets](https://docs.akeyless.io/docs/ping-targets). While it saves time for multiple secret-level configurations by not requiring you to provide an inline connection string each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.

# Working With Ping Dynamic Secrets from the CLI

## Create a Dynamic Ping Secret

To create a dynamic Ping secret from the CLI using an existing [Ping Target](https://docs.akeyless.io/docs/ping-target), run the following command:

```shell Akeyless CLI
akeyless dynamic-secret create ping \
--name <Producer Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--ping-client-authentication-type CLIENT_SECRET \
--ping-grant-types AUTHORIZATION_CODES \
--ping-redirect-uris 'https://<Your-Redirect-URL>'
```

Where:

* `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

* `target-name`: A name of the target that enables connection to the Ping server. The name can include the path to the virtual folder where this target resides.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `ping-client-authentication-type`: OAuth Client Authentication Type, this can be either `CLIENT_SECRET`, `PRIVATE_KEY_JWT` or `CLIENT_TLS_CERTIFICATE`, with `CLIENT_SECRET` being the default. Each of these selections has its own set of related parameters, which are elaborated upon in the [CLI reference](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#/ping).

* `ping-grant-types`: The grant type (or types) given to the OAuth client. This can be either `IMPLICIT`, `AUTHORIZATION_CODE`, `CLIENT_CREDENTIALS`, `TOKEN_EXCHANGE`, `REFRESH_TOKEN`, `ASSERTION_GRANTS`, `PASSWORD`, or `RESOURCE_OWNER_CREDENTIALS`, with `AUTHORIZATION_CODE` being the default. This flag can be added multiple times for multiple grant types. Some of these selections have their own set of related parameters, which are elaborated upon in the [CLI reference](https://docs.akeyless.io/docs/cli-reference-akeyless-producers#p-stylecolorbluegateway-create-producer-pingp).

* `ping-redirect-uris`: a URI to which the OAuth authorization server may redirect the resource owner's user-agent after authorization is obtained. At least one redirection **URI** is required for the `AUTHORIZATION_CODE` and `IMPLICIT` grant types. For multiple values repeat this flag.

To create a Ping Dynamic Secret without using an existing target, amend the command to show as follows:

```shell Akeyless CLI
akeyless dynamic-secret create ping \
--name <Producer Name> \
--gateway-url 'https://<Your_Akeyless_GW_URL:8000>' \
--ping-url 'https://my-pf-server.com' \
--ping-privileged-user <Username> \
--ping-password <Password>\
--ping-client-authentication-type CLIENT_SECRET \
--ping-grant-types AUTHORIZATION_CODES \
--ping-redirect-uris 'https://<Your_Redirect_URL>'
```

Where:

* `ping-url`: A URL address related to the Ping service.

* `ping-privileged-user`: A username of a user on your Ping service that may create OAuth Clients through Ping Federate Administrative API.

* `ping-password`: Password related to the privileged user.

All other parameters have the same meaning whether or not you choose to use a target. Additional parameters can be found in the [CLI reference](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#p-stylecolorbluepingp).

You may update the Dynamic Secret information using the following command with the same parameters:

```shell Akeyless CLI
akeyless dynamic-secret updateakeyless dynamic-secret get-value ping
```

## Fetch a Dynamic Ping Secret Value

> 🚧 Warning
>
> To authorize the producer in your gateway, add the following environment parameter as described in [Advanced Gateway Configuration](https://docs.akeyless.io/docs/advance-gw-docker-configuration):
>
> `-e PING_FEDERATE_CERTIFICATE= <Your Ping Federate server Certificate encoded in base64>`

To fetch a dynamic Ping secret value from the CLI, run the following command:

```shell Akeyless CLI
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

The output should look as follows:

```shell
{
  "client_id": "<Client ID>",
  "client_secret": "<Temp Secret>",
  "id": "<ID>",
  "ttl_in_minutes": "60"
}
```

# Working With Ping Dynamic Secrets from the Console

> 👍 Note
>
> To start working with dynamic secrets from the Akeyless Console, you need to configure the [Gateway](https://docs.akeyless.io/docs/api-gw) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

## Create a Dynamic Ping Secret

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the **Ping** secret type under **Infra** and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining settings as follows:

* **Delete Protection**: When enabled, protects the secret from accidental deletion.
* **Target mode:** In this section, you can either select an existing [Ping Target](https://docs.akeyless.io/docs/ping-target) or specify details you would fill in the target creation.
* **Client Authentication Type**: OAuth Client Authentication Type.
* **Redirect URIs**: List URIs to which the OAuth authorization server may redirect the resource owner's user-agent after authorization is obtained.
* **Grant Types** : The grant type (or list of types) given to the OAuth client.
* **Access Token Manager Instance ID**: Set a specific Access Token Management (ATM) instance for the created OAuth Client by providing the ATM Id. If no explicit value is given, the default PingFederate server ATM will be set.
* **Restricted Scopes**: Limit the OAuth client to specific scopes.
* **User TTL:** Provide a time-to-live value for a dynamic secret (i.e., a token). When TTL expires, the token becomes obsolete.
* **Time Unit:** Select the time unit (`seconds`, `minutes`, `hours`) for the TTL value.
* **Gateway:** Select the Gateway through which the dynamic secret will create users.
* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

5. If you selected the **Explicitly specify target properties** mode, click **Next**.

6. Provide details of the target Ping server:

* **Ping URL**: A URL address related to the Ping service.

* **Privileged User**: A username of a user on your Ping service that may create OAuth Clients through Ping Federate Administrative API.

* **Password**: Password related to the privileged user.

* **Administrative Port**: PingFederate administrative port, default is 9999.

* **Authorization Port**: PingFederate authorization port, default is 9031.

7. Click **Finish**.

## Fetch a Dynamic Ping Secret Value

> 🚧 Warning
>
> To authorize the producer in your gateway, add the following environment parameter as described in [Advanced Gateway Configuration](https://docs.akeyless.io/docs/advance-gw-docker-configuration):
>
> `-e PING_FEDERATE_CERTIFICATE= <Your Ping Federate server Certificate encoded in base64>`

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click **Get Dynamic Secret** button.
