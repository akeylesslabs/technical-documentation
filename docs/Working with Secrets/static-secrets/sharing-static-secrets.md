---
title: Sharing Static Secrets
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
You can securely share copies of static secret items saved in Akeyless with anyone, even if they don’t use Akeyless or are part of your organization based on a well-defined TTL. When you share an item, you can choose either to share it via email or to wrap the value of the secret with a temporary token. Upon item sharing, a temporary [Access Role](doc:rbac) will be created automatically, so as a break glass solution, this can be revoked immediately. Upon access to the shared secret, a log entry will be recorded with the relevant details.

When sharing via **emails** you’ll get a unique link you need to share with those users, choose when the share expires and who are the specific users that will be able to access it. When sharing using **wrapping tokens**, you'll get a temporary token that can be shared on the wire without exposing the real secret.

> 🚧 Note
> 
> For security purposes, when workin with share based on emails, only the users you've specified their **email** will be able to access the item using this link

# Sharing Static Secret from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items > Choose the relevant Static Secret**.

2. Click on the item menu on the upper right and click **Share**.

3. Choose the share flow either **Email** or via **Token**

4. Choose when the link expires and who to share it with. If you choose to share the item with only some people via **Email**, enter each email address and press Return or Enter

5. Click Copy, then send the link or token to the recipient you want to share the item with. When sharing via **Email**  the recipients must verify their email address first, to get access to the item.

To view an email-based shared item, click or tap the link you were sent to open it in your browser. After you’ve verified your email address, you can view and copy the item or other item details that were shared with you until the link expires.

To view the secret that was wrapped by the temporary token, you can run the `unwrap-token` API call.

# Sharing Static Secret from the Akeyless CLI

To share an item via **Email**, use the following command:

```shell Akeyless CLI
akeyless share-item --item-name <item name> --action share --email <email address>
```

Where:

- `item-name`:  The name of the item to examine, this parameter is mandatory

- `action`: The action to perform on the item, you may choose `share` to share an item, `stop` to stop sharing an item, or `describe` to see with what addresses it was already shared, this parameter is mandatory.

- `email`: List of emails to start/stop sharing the secret with, To specify multiple emails use argument multiple times (`--email email1 --email email2` etc.). This parameter is mandatory for `start` or `stop` actions.

To share an item via **Token** run the following: 

```shell Akeyless CLI
akeyless share-item --item-name <item name> --action <action to perform> --share-type token
```

Where:

- `item-name`:  The name of the item to examine, this parameter is mandatory
- `action`: The action to perform on the item, you may choose `share` to share an item, `stop` to stop sharing an item, or `describe` to see with what addresses it was already shared, this parameter is mandatory.
- `share-type`: The share type set to `token`, by default set to `email`.

You can find the complete list of parameters for these commands in the [CLI Reference section](https://docs.akeyless.io/docs/cli-reference-static-secrets#p-stylecolorblueshare-itemp)

# Access Shared Secret

Secrets that were shared via **Email** can be accessed directly from any browser, when working with **Token** flow, the recipient can use the CLI or using `curl` to unwrap the wrapping token for example using the CLI:

```shell
akeyless unwrap-token --shared-token <shared token>
```

You can find the complete list of parameters for these commands in the [CLI Reference section](https://docs.akeyless.io/docs/cli-reference-static-secrets#p-stylecolorblueunwrap-tokenp)

# Managing Shared Items

Once an item has been shared, a full auditing activity is logged into Akeyless audit logs, to remove a user from an item, **Admins** or the item owners can remove those users from the sharing list. 

Navigate to the shared item, and remove the relevant email address from the **Recipient email address** list. 

**Admins** can easily find new temporary **Access Roles** for those users who received temporary access. Simply delete those temporary **Access Roles** to revoke the share.

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/sharing-a-static-secret" target="_blank">Sharing a Static Secret</a>.