---
title: Creating a Static Secret Quickstart
deprecated: false
hidden: false
metadata:
  robots: index
next:
  pages:
    - slug: api-key-creation-quickstart
      title: Creating an API Key Quickstart
      type: basic
---
This Quickstart guides you through creating a Static Secret in Akeyless. A Static Secret is a user-defined value, such as an API key or password, that you store and retrieve as needed. This is the most basic operation in Akeyless and is often the first step before integrating secrets with applications or automation.

## Prerequisites

You will need:

* An active Akeyless account
* Access to the Akeyless Console

If you do not yet have an account, complete the **Creating an Akeyless Account Quickstart** first.

## Step 1: Sign In to the Akeyless Console

1. Open the [Akeyless Console](https://console.akeyless.io).
2. Sign in to your existing Akeyless account.

You will be taken to the Akeyless Console homepage.

## Step 2: Open the Items Page

1. In the left navigation menu, select **Items**.
2. Select **+ New**.
3. Select **Static Secret** from the presented menu.

This opens the **Create Static Secret** form.

## Step 3: Configure the Static Secret

1. In the **Name** field, type `QuickSecret`.
2. In the **Value** field (toward the bottom of the form), type `Super Secret`.
3. Leave all other fields as their default values.
4. Select **Finish**.

Your Static Secret has been created.

## Step 4: Verify your Secret

The details of your Static Secret should be open in the right half of your browser. If not, select the `QuickSecret` item.

1. In the **General** tab of your Static Secret, scroll to the bottom and look for the **Value** field.
2. Select the <svg width="16" height="16" viewBox="0 0 24 24" aria-label="Show value" role="img"><path d="M 12 4.5 C 7 4.5 2.73 7.61 1 12 c 1.73 4.39 6 7.5 11 7.5 s 9.27 -3.11 11 -7.5 c -1.73 -4.39 -6 -7.5 -11 -7.5 Z M 12 17 c -2.76 0 -5 -2.24 -5 -5 s 2.24 -5 5 -5 s 5 2.24 5 5 s -2.24 5 -5 5 Z m 0 -8 c -1.66 0 -3 1.34 -3 3 s 1.34 3 3 3 s 3 -1.34 3 -3 s -1.34 -3 -3 -3 Z" /></svg> icon next to **Value** to retrieve and decrypt the value of `QuickSecret`.

`Super Secret` should be displayed.

***

_You have successfully created a Static Secret in the Akeyless Console._
