---
title: Creating an API Key Quickstart
excerpt: Harrison to test this out.
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

By the end of this guide, you will have:

* An Akeyless **Access ID**
* An Akeyless **Access Key**
* An Authentication Method configured to use that API Key

## Prerequisites

You will need:

* An active Akeyless account
* Access to the Akeyless Console  
  <Anchor label="[https://console.akeyless.io](https://console.akeyless.io)" target="_blank" href="https://console.akeyless.io">[https://console.akeyless.io](https://console.akeyless.io)</Anchor>

If you do not yet have an account, complete the **Creating an Akeyless Account Quickstart** first.

## Step 1: Sign In to the Akeyless Console

1. Open the Akeyless Console:  
   <Anchor label="[[https://console.akeyless.io](https://console.akeyless.io)](https://console.akeyless.io)" target="_blank" href="https://console.akeyless.io"><Anchor label="[https://console.akeyless.io](https://console.akeyless.io)" target="_blank" href="https://console.akeyless.io">[https://console.akeyless.io](https://console.akeyless.io)</Anchor></Anchor>
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

* **Access ID**
* **Access Key**

## Step 5: Copy and Save the Access Credentials

After the API Key is created:

* Copy the **Access ID**
* Copy the **Access Key**

Store these values securely.

<Callout icon="⚠️" theme="warning">
  The **Access Key** is shown only once.  
  If you lose it, you must create a new API Key.
</Callout>

## Step 6: Assign Permissions

The API Key must be associated with **Roles** to control what it can access.

1. In the left navigation menu, select **Access Roles**.
2. Select the pre-made **admin** role to open the **Edit Role** window.
3. In the **Edit Role** window, the **General** tab is selected by default.
4. Select **+ Associate**.
5. In the **Auth Method** drop-down menu, select **/My API Key**.

<Callout icon="📘" theme="info">
  The `/` added in this drop-down menu indicates that **My API Key** 
</Callout>

You can associate **My API Key** with a custom role later if desired.

## Step 7: Test the API Key (Optional)

You can test the API Key with the Akeyless CLI:

1. Log in with Access ID and Access Key:

```bash
akeyless login --access-id <ACCESS-ID> --access-key <ACCESS-KEY>
```

2. List available items:

```bash
akeyless list-items
```

If authentication succeeds, the API Key is functioning.

***

_Your API Key is now ready for use in your Akeyless environment._
