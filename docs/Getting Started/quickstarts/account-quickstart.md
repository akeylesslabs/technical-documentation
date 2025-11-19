---
title: Creating an Akeyless Account Quickstart
deprecated: false
hidden: false
metadata:
  robots: index
---
This Quickstart guides you through creating a new Akeyless account, verifying your email address, and signing in to the Akeyless Console for the first time. Completing this setup is required before you can create secrets, configure an Akeyless Gateway, or integrate Akeyless with applications.

## Prerequisites

You will need:

* A modern web browser
* An email address you can access
* Internet connectivity

No prior Akeyless account or configuration is required.

## Step 1: Open the Akeyless Signup Page

1. Navigate to the Akeyless signup page:  
   **<Anchor label="https://console.akeyless.io/registration" target="_blank" href="https://console.akeyless.io/registration">https://console.akeyless.io/registration</Anchor>**
2. Enter your email address, accept the <Anchor label="End User License Agreement" target="_blank" href="https://www.akeyless.io/end-user-license-agreement/">End User License Agreement</Anchor> & <Anchor label="Privacy Policy" target="_blank" href="https://www.akeyless.io/terms-of-service/">Privacy Policy</Anchor>,  and select **Let's Get Started** (or select a social sign-in option).
   1. You may also have to complete a reCAPTCHA.

<Callout icon="📘" theme="info">
  You do *not* need to change the **Environment** drop-down menu's value.
</Callout>

3. Text.

## Step 2: Verify Your Email Address

1. Open the verification email sent by Akeyless.
2. Select the **Verify Email** link inside the message.

If you do not receive the verification email:

* Check spam or junk folders.
* Confirm the email address was entered correctly.
* Request another verification email from the signup screen.

Once your email is verified, your account becomes active.

## Step 3: Sign In to the Akeyless Console

1. Go to: **[https://console.akeyless.io/](https://console.akeyless.io/)**
2. Enter your email and password.
3. Select **Sign In**.

You are now logged in to the Akeyless Console.

## Step 4: Complete Initial Console Setup

When signing in for the first time, you may be prompted to:

* Accept the Terms of Service
* Review the onboarding introduction screen
* Choose whether to enable optional usage analytics

After completing these steps, you are taken to the Akeyless Console homepage.

## What You Should See Next

From the console, you can access:

* **Secrets** — store and manage static or dynamic secrets
* **Gateways** — deploy gateways for private or isolated networks
* **Access Management** — configure authentication methods and permissions
* **Key Management** — create and manage encryption keys and certificates

You are now ready to continue to the next quickstart.

## Next Steps

Once your account is created, you can proceed to:

* **Create a Static Secret**  
  `getting-started/static-secret-quickstart.md`

or if you are integrating with Kubernetes:

* **Install and Configure the Akeyless Gateway with Kubernetes**  
  `getting-started/gateway-kubernetes-quickstart.md`
