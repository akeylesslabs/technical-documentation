---
title: Universal Identity
excerpt: Universal Identity (UID)
deprecated: false
hidden: false
metadata:
  title: Universal Identity
  description: ''
  robots: index
next:
  description: >-
    Make sure to associate your new Authentication Method with an Access Role to
    grant the relevant permissions within Akeyless
---
# Introduction

The Akeyless Universal Identity (UID) authentication method enables you to identify your machines without the need for an initial secret. This authentication method solves the **secret zero** problem by providing an inherited identity derived from the parent system together with an ephemeral token for continuous authentication.

The following diagram describes the flow of credentials when using UID tokens, demonstrating the elimination of the secret zero problem:

![](https://files.readme.io/e362078-image_1.png "image (1).png")

While the process has an initiation phase where the Admin creates the original authentication method, the secret zero problem is avoided by repeatedly rotating the UID, to the point where the original credentials are unusable, and constant rotation protects any vulnerability.

# Create a Universal Identity Authentication Method in the CLI

Let's create a new Universal Identity authentication method using the Akeyless CLI. (You can do this also from the [Akeyless Console](https://docs.akeyless.io/docs/universal-identity#create-a-iniversal-identity-authentication-method-in-the-akeyless-console).)

To create a new Universal Identity authentication method from the CLI, run the following command:

```shell Akeyless CLI
akeyless auth-method create universal-identity \
--name <Auth Method Name> \
--ttl 60 
```

Where:

* **name:** A unique name for the authentication method. The name can include the path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

* **ttl:** The root token time-to-live in minutes. The TTL is renewed with every rotation.

You can find the complete list of additional parameters for this command in the [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-reference-universal-identity) section.

## Generate a Token

The UID authentication functions via tokens that can be used to access the assigned permissions. To generate a new token, use the following command:

```shell CLI
akeyless uid-generate-token --auth-method-name uidAuth --profile adminProfile
```

## Using Universal Identity Tokens

In order to use the token you generated, add it to your Akeyless commands in one of the following ways:

```shell CLI
akeyless list-items --uid-token u-XXXXXXXX
akeyless get-secret-value -n MyFirstSecret --uid-token u-XXXXXXXX
```
```curl
curl https://<Gateway-URL>:8080 -d "cmd=get-secret-value&name=MyFirstSecret&&uid-token=u-XXXXX"
curl https://<Gateway-URL>:8080 -d "cmd=list-items&&uid-token=u-XXXXX"
```

## Revoke a Token

To disable the permissions of a certain token, use the following command:

```shell CLI
akeyless uid-revoke-token --uid-token u-XXXX --revoke-token u-XXXX --revoke-type revokeSelf
```

You can find the complete list of additional parameters for this command in the [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-reference-universal-identity#p-stylecolorblueuid-revoke-tokenp) section.

## Rotate a Token

Like with secrets and encryption keys, tokens can also be rotated. Once the token has been rotated its TTL will reset, but other than that the new version of the token retains all assigned functions and permissions.

To rotate a token use the following command:

```shell CLI
akeyless uid-rotate-token --uid-token u-XXXXXXXX
```
```curl CURL
curl https://<Gateway-URL>:8080 -d "cmd=uid-rotate-token&&uid-token=u-XXXXX"
```

### Rotation Flow

It is considered a best practice to rotate tokens often, and with tokens being a machine identity authentication method, you may set up an automated script that will rotate your token in pre-scheduled intervals.

While you can write your own script, we have a compatible one-minute interval token rotation script in the <a href="https://download.akeyless.io/Akeyless_Artifacts/Linux/Universal_Identity/" target="_blank">Akeyless Downloads</a> folder.\
This script is Linux/MacOS compatible, and has the following flow:

1. Write the token to a path
2. Take the token from path to perform commands
3. Rotate token
4. Replace the token in path\
   After downloading the `.sh` file, execute it and select `init` and insert the token you generated to start the process. From this point on the script can be run automatically to rotate the token by itself.

If you wish to write your own script, here are some useful parts you might want to include:

To read a token from a file or to write a token to a file:

```shell Shell
echo u-XXXXXXXX > /tmp/token
akeyless uid-rotate-token -i /tmp/token -o /tmp/token
```

To rotate a token with backward compatibility:

```shell CLI
akeyless rotate-token --token u-XXXXXXXX
```
```curl
curl https://<Gateway-URL>:8080 -d "cmd=rotate-token&&token=u-XXXXX"
```

## Create a Child Token

Child tokens are not mandatory.  They are optional and meant for users who want to use the token with a tree structure to control and monitor multiple services.

When using the following command:

```shell CLI
akeyless uid-create-child-token --uid-token u-XXXXXXXX
```

You will get the following result with the child token:

```shell
$ "Child Token: u-XXXXXXXX2"
```

You can find the complete list of additional parameters for this command in the [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-reference-universal-identity#p-stylecolorblueuid-create-child-tokenp) section.

## Get the Token Tree

If you use child tokens and want to see the structure of your token tree, use the following command:

```shell CLI
akeyless uid-list-children --uid-token u-XXXXXXXX
```
```shell Result
akeyless uid-list-children --uid-token u-XXXXXXXX
Universal Identity Details:
 {
  "number_of_tokens": 2,
  "max_depth": 1,
  "root": {
    "id": "ywzsub3u4tbu",
    "comment": "root token",
    "ttl": 1000,
    "last_rotate": "2020-10-13 13:36:47 UTC",
    "expired_date": "2020-10-14 06:16:47 UTC",
    "children": {
      "ywzsub3u4tbunVCo": {
        "depth": 1,
        "id": "ywzsub3u4tbunVCo",
        "ttl": 1000,
        "last_rotate": "2020-10-13 13:41:00 UTC",
        "expired_date": "2020-10-14 06:21:00 UTC"
      }
    }
  }
}
```

# Create a Universal Identity Authentication Method in the Console

1. Log in to the Akeyless Console and go to **Users & Auth Methods** > **⊕ New** > **Akeyless (Universal Identity)** .

2. Define a **Name** for the authentication method, and specify the **Location** as a path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

3. Define the remaining parameters as follows:

* **Expiration Date:** Select the access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.

* **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean CURL, SDK, etc. This parameter is optional. Leave it empty for unrestricted access.

* **Allowed Trusted Gateway IPs:** Enter a comma-separated list of CIDR blocks. When specified, the Gateway with the IP from this range will be trusted to forward original client IPs (so they will be visible in the logs).\
  If empty, the Gateway's IP will be used in the logs.

* **Audit Log Sub Claims:** Enter a comma-separated list of sub-claims keys to be included in the audit logs.

* Check **Deny Rotate** if you want to forbid token rotation.

* Check **Deny Inheritance** if you want to forbid creating child tokens.

* **TTL (minutes):** Specify token TTL (between 1min to 43200min).

4. Click **Finish**.

## Generate a Token

To generate a token in the Console, 

1. Open the corresponding authentication method
2. Go to **UID Tree** tab and then click**Generate**.

> 🚧 Warning
>
> If a UID token already exists, generating a new UID token will reset the existing token

## Revoke a Token

To revoke a token in the Console, 

1. Open the corresponding authentication method 
2. Go to **UID Tree** tab.
3. Right-click the node and click **Revoke token**.
4. Select **Revoke self** if you want to revoke the selected node only or select **Revoke self and children** if you want to revoke the selected node and its children node/s. Click **Save**.

## Create a Child Token

To create a child token in the Console, 

1. Open the corresponding authentication method, 
2. Go to **UID Tree** tab.
3. Right-click the root node and click **Create child token**.
4. Define the parameters as follows:

   * Check **Deny Rotate** if you want to forbid child token rotation.

   * Check **Deny Inheritance** if you want to forbid creating child tokens.

   * **Child TTL (minutes):** Specify child token TTL.
5. Click **Save**.

## Get the Token Tree

To get the token tree in the Console, 

1. Open the corresponding authentication method, 
2. Go to **UID Tree** tab.

> 📘 Note
>
> When your Token Tree becomes complex, you can use your mouse and **zoom in** to see specific Token better or **zoom out** to see the whole Token Tree

# Best practice

A UID token is initially used to authenticate a client with Akeyless. The UID token includes essential authentication information, ensuring that the client's identity has been verified.

Once authenticated, the best practice is to exchange the UID token for a **t-token** (Temporary Token). The **t-token** is a short-lived token used for subsequent API requests enabling better performance using the token for subsequent requests minimizes the need for repeated authentication processes, while using a shorter lifespan token reduces the opportunity for potential misuse.
