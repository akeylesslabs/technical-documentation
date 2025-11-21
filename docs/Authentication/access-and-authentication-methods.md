---
title: Authentication Methods Introduction
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Authentication Methods Introduction
  description: ''
  robots: index
next:
  description: ''
---
In [Authentication & Authorization](https://docs.akeyless.io/docs/understanding-authentication) we saw that Authentication Methods represent machine identities or human identities.

Instead of authenticating identities itself, in most cases, Akeyless integrates with 3rd party identity providers that provide tokens of authentication.

For **machine** access, Akeyless supports:

* Cloud identities (CSP IAM) such as [AWS IAM](https://docs.akeyless.io/docs/aws-iam), [Azure AD](https://docs.akeyless.io/docs/azure-ad), [GCP IAM](https://docs.akeyless.io/docs/gcp-auth-method), and [OCI IAM](https://docs.akeyless.io/docs/oci-iam)
* On-prem machines using [Universal Identity™](https://docs.akeyless.io/docs/universal-identity)
* [Kubernetes](https://docs.akeyless.io/docs/kubernetes-auth)
* [Certificate](https://docs.akeyless.io/docs/certificate-based-authentication)
* [OAuth2.0/JWT](https://docs.akeyless.io/docs/oauth20jwt)
* [API Keys](https://docs.akeyless.io/docs/api-key)
* [Kerberos](https://docs.akeyless.io/docs/kerberos)

For **human** access, Akeyless supports:

* [LDAP](https://docs.akeyless.io/docs/ldap)
* [SAML](https://docs.akeyless.io/docs/saml)
* [OIDC](https://docs.akeyless.io/docs/openid)
* [OAuth2.0/JWT](https://docs.akeyless.io/docs/oauth20jwt)
* [Email](https://docs.akeyless.io/docs/email)
* [API Keys](https://docs.akeyless.io/docs/api-key)

which are used by known identity providers such as [Okta](https://docs.akeyless.io/docs/okta), [Azure AD](https://docs.akeyless.io/docs/azure-ad-saml-authentication), and others.

# Authentication Settings

Under your account settings in the console, you will find a tab titled **Authentication Settings**. Currently, this tab allows you to customize the expiration limits AKA Time to Live (TTL), and default for authentication methods that are time-sensitive.

You can set a custom range of possible TTL for your tokens, setting the minimum, default, and maximum allowed TTL for your tokens.

The default setting of your token TTL will affect all your authentication methods unless you have set a different TTL for a specific authentication method.

> 👍 Note
>
> For an authentication method to have the necessary permissions to perform actions, you will need to attach it to a matching role.
> To learn more about this, please go to [Role-based Access Control (RBAC)](https://docs.akeyless.io/docs/rbac).

## Product Type

Accounts with multiple products can label **each** of their Authentication methods usage, mostly for billing and feature access based on their products. It is recommended to set the relevant product type with the expected usage purposes to provide your end users with the exact features according to the relevant product.

# Multi-Factor Authentication (MFA)

MFA is a process in which users are prompted during the sign-in process for an additional form of identification, such as a code on their email, or using any authenticator application.

If you only use an [Email](https://docs.akeyless.io/docs/email) and password to authenticate to Akeyless, either using your Account email or any users who were invited using the [Email Auth](https://docs.akeyless.io/docs/email) it leaves an insecure vector for attack. Those Auth methods can be set with MFA by default.

To enable MFA on your email, navigate to the Account Settings page and choose the right flow you'd like to receive those temporary tokens, either over email, or using an authenticator app. Once enabled, any time you'll log in using your email, you'll have to provide this one-time password to log in to Akeyless services such as our [Command Line Interface (CLI)](https://docs.akeyless.io/docs/cli), Web applications, and our [Browser Extension](https://docs.akeyless.io/docs/browser-extensions).

# Tutorial

Check out our tutorial video on [Authentication Methods](https://tutorials.akeyless.io/docs/authentication-methods-and-api-key-authentication).
