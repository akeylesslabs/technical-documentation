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

1. Open:  
   <Anchor label="[https://console.akeyless.io](https://console.akeyless.io)" target="_blank" href="https://console.akeyless.io">[https://console.akeyless.io](https://console.akeyless.io)</Anchor>
2. Enter your email and password.
3. Select **Sign In**.

## Step 2: Open the Authentication Methods Page

1. In the left navigation menu, select **Access Management**.
2. Select **Auth Methods**.
3. Select **+ New**.

This opens the **Create Auth Method** form.

## Step 3: Create an API Key Authentication Method

1. In the **Type** dropdown, select **API Key**.
2. Enter a descriptive name, such as **Gateway API Key**.
3. (Optional) Add a description or tags.

Select **Next** to continue.

## Step 4: Configure the API Key

1. Set an expiration value, or leave it as **Never Expire** if desired.
2. (Optional) Restrict by:
   * Allowed CIDRs
   * Allowed environments
   * Time-based access settings  
     These restrictions can help secure the key.

Select **Finish**.

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

1. Open the API Key Auth Method you just created.
2. Navigate to the **Roles** tab.
3. Select **Assign Roles**.
4. Choose one or more roles, such as:
   * **Admin**
   * **Reader**
   * Custom-defined roles

Permissions can be adjusted later as needed.

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