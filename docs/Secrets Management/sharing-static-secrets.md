---
title: Sharing Secrets
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
You can securely share copies of [Static](https://docs.akeyless.io/docs/static-secrets) and [Rotated](https://docs.akeyless.io/docs/rotated-secrets#/) secret items saved in Akeyless with anyone, even if they don’t use Akeyless or are part of your organization based on a well-defined TTL. When you share an item, you can choose either to share it by way of email or to wrap the value of the secret with a temporary token. Upon item sharing, a temporary [Access Role](https://docs.akeyless.io/docs/rbac) will be created automatically, so as a break glass solution, this can be revoked immediately. Upon access to the shared secret, a log entry will be recorded with the relevant details.

When sharing by way of **emails**, you’ll get a unique link to share with those users, choose when the share expires, and specify which users can access it. When sharing using **wrapping tokens**, you'll get a temporary token that can be shared on the wire without exposing the real secret.

You can define a list of allowed email domains in the **Global Settings**. Secrets can only be shared with users whose email addresses belong to these domains. By default, sharing is allowed with all domains.

> **Note:**
>
> You can define a list of allowed email domains in the Global Settings. Secrets can only be shared with users whose email addresses belong to these domains. For security purposes, when working with email-based sharing, only users whose email addresses you’ve specified can access the item using the shared link. By default, sharing is allowed with all domains.

## Sharing Secrets from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items > Choose the relevant Secret**.

2. Click on the item menu on the upper right and click **Share**.

3. Choose the share flow either **Email** or by way of **Token**

4. Choose when the link expires and who to share it with. If you want to share the item with only specific people by email, enter each email address, then press **Enter**.

5. Click **Copy**, then send the link or token to the recipient you want to share the item with. If you share the item by email, recipients must verify their email address before they can access it.

To view an email-based shared item, click or tap the link you were sent to open it in your browser. After you’ve verified your email address, you can view and copy the item or other item details that were shared with you until the link expires.

To view the secret that was wrapped by the temporary token, you can run the `unwrap-token` API call.

## Sharing Secrets from the Akeyless CLI

To share an item by way of **Email**, use the following command:

```shell
akeyless share-item --item-name <item name> --action share --email <email address>
```

Where:

* `item-name`: The name of the item to examine, this parameter is mandatory

* `action`: The action to perform on the item, you may choose `share` to share an item, `stop` to stop sharing an item, or `describe` to see with what addresses it was already shared, this parameter is mandatory.

* `email`: List of emails to start/stop sharing the secret with, To specify multiple emails use argument multiple times (`--email email1 --email email2` and so on). This parameter is mandatory for `start` or `stop` actions.

To share an item by way of **Token** run the following:

```shell
akeyless share-item --item-name <item name> --action <action to perform> --share-type token
```

Where:

* `item-name`: The name of the item to examine, this parameter is mandatory
* `action`: The action to perform on the item, you may choose `share` to share an item, `stop` to stop sharing an item, or `describe` to see with what addresses it was already shared, this parameter is mandatory.
* `share-type`: The share type set to `token`, by default set to `email`.

You can find the complete list of parameters for these commands in the [CLI Reference section](https://docs.akeyless.io/docs/cli-reference-static-secrets#share-item)

## Access Shared Secret

Secrets that were shared by way of **Email** can be accessed directly from any browser, when working with **Token** flow, the recipient can use the CLI or using `curl` to unwrap the wrapping token for example using the CLI:

```shell
akeyless unwrap-token --shared-token <shared token>
```

You can find the complete list of parameters for these commands in the [CLI Reference section](https://docs.akeyless.io/docs/cli-reference-static-secrets#unwrap-token)

## Managing Shared Items

Once an item has been shared, a full auditing activity is logged into Akeyless Audit Logs, to remove a user from an item, **Admins** or the item owners can remove those users from the sharing list.

Navigate to the shared item, and remove the relevant email address from the **Recipient email address** list.

**Admins** can easily find new temporary **Access Roles** for those users who received temporary access. Simply delete those temporary **Access Roles** to revoke the share.

## Tutorial

Check out our tutorial video on [Sharing a Secret](https://tutorials.akeyless.io/docs/sharing-a-static-secret) .
