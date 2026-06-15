---
title: Creating an API Key Quickstart
deprecated: false
hidden: false
metadata:
  robots: index
next:
  pages:
    - slug: gateway-k8s-quickstart
      title: Akeyless Gateway with Kubernetes Quickstart
      type: basic
---
This Quickstart walks you through creating an **Akeyless API Key**, which can be used for programmatic access, automation, and for authenticating Akeyless Gateways or applications.

<ApiKeyWarning />

By the end of this guide, you will have:

- An Akeyless **Access ID**
- An Akeyless **Access Key**
- An Authentication Method configured to use that API Key

## Prerequisites

You will need:

- An active Akeyless account
- Access to the Internet

If you do not yet have an account, complete the [Creating an Akeyless Account Quickstart](https://docs.akeyless.io/docs/account-quickstart) first.

## Step 1: Sign In to the Akeyless Console

1. Open the Akeyless Console: [https://console.akeyless.io](https://console.akeyless.io).
2. Sign in to your existing Akeyless account.

You will be taken to the Akeyless Console homepage.

## Step 2: Open the Create Authentication Method Form

1. In the left navigation menu, select **Users & Auth Methods**.
2. Select **+ New**.

This opens the **Create Authentication Method** form.

## Step 3: Create an API Key Authentication Method

1. On the **Type** selection screen, select **API Key**.
2. Select **Next →**.
3. Enter `My API Key` in the **Name** field.
4. Select **Finish** to continue.

You will now see the new API Key displayed with two critical values:

- **Access ID**
- **Access Key**

## Step 5: Copy and Save the Access Credentials

After the API Key is created:

- Copy the **Access ID**
- Copy the **Access Key**

Store these values securely.

> ⚠️ **Warning:** The **Access Key** is shown only once.
>
> If you lose it, you must create a new API Key.

## Step 6: Assign Permissions

The API Key must be associated with **Roles** to control what it can access.

1. In the left navigation menu, select **Access Roles**.
2. Select the pre-made **admin** role to open the **Edit Role** window.
3. In the **Edit Role** window, the **General** tab is selected by default.
4. Select **+ Associate**.
5. In the **Auth Method** drop-down menu, select `/My API Key`.
6. Select **Save**.

> ℹ️ **Note:**
>
> The `/` added in this drop-down menu indicates that `My API Key` was created at the root of the Items directory in your Akeyless account. You can create subdirectories to organize your Items.

You can associate `My API Key` with a custom role later if desired.

## Step 7: Test the API Key (Optional)

You can test the API Key with the Akeyless CLI:

1. [Download the Akeyless CLI](https://docs.akeyless.io/docs/cli#download) with a Terminal or Command Prompt.
2. For Akeyless CLI Configuration:
   1. Type `n` to skip configuring a profile. You can change this later.
   2. Choose if you want to move the Akeyless CLI binary and if you want to create a user `PATH` environment variable.
3. Close and relaunch your Terminal or Command Prompt.
4. Authenticate with the Access ID and Access Key:

```shell
akeyless auth --access-id <ACCESS-ID> --access-key <ACCESS-KEY>
```

You should expect to see `Authentication succeeded.` in response to your command. You can test your access further by listing available items:

```shell
akeyless list-items
```

The output of this command should be a JSON-formatted list of all Items in your Akeyless account.

***

_Your API Key is now ready for use in your Akeyless environment._
