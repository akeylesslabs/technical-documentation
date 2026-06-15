---
title: Authentication Methods
slug: access-and-authentication-methods
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
In [Authentication and Authorization](https://docs.akeyless.io/docs/auth-overview), we saw that Authentication Methods represent machine identities or human identities.

Rather than authenticating identities directly, Akeyless typically integrates with third-party identity providers that issue authentication tokens.

For **machine** access, Akeyless supports:

* Cloud identities (CSP IAM) such as [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws), [Azure AD](https://docs.akeyless.io/docs/auth-with-azure), [GCP IAM](https://docs.akeyless.io/docs/auth-with-gcp), and [OCI IAM](https://docs.akeyless.io/docs/auth-with-oci)
* On-prem machines using [Universal Identity™](https://docs.akeyless.io/docs/auth-with-universal-identity)
* [Kubernetes](https://docs.akeyless.io/docs/auth-with-kubernetes)
* [Certificate](https://docs.akeyless.io/docs/auth-with-certificate)
* [OAuth2.0/JWT](https://docs.akeyless.io/docs/auth-with-oauth-jwt)
* [API Keys](https://docs.akeyless.io/docs/auth-with-api-key)
* [Kerberos](https://docs.akeyless.io/docs/auth-with-kerberos)

For **human** access, Akeyless supports:

* [LDAP](https://docs.akeyless.io/docs/auth-with-ldap)
* [SAML](https://docs.akeyless.io/docs/auth-with-saml)
* [OIDC](https://docs.akeyless.io/docs/auth-with-oidc)
* [OAuth2.0/JWT](https://docs.akeyless.io/docs/auth-with-oauth-jwt)
* [Email](https://docs.akeyless.io/docs/auth-with-email)
* [API Keys](https://docs.akeyless.io/docs/auth-with-api-key)

These methods are used by known identity providers such as [Okta](https://docs.akeyless.io/docs/okta-oidc), [Azure AD](https://docs.akeyless.io/docs/auth-with-azure), and others.

## Authentication Settings

Under your account settings in the console, you will find a tab titled **Authentication Settings**. Currently, this tab allows you to customize the expiration limits (TTL), and default for authentication methods that are time-sensitive.

You can set a custom range of possible TTL for your tokens, setting the minimum, default, and maximum allowed TTL for your tokens.

The default setting of your token TTL will affect all your authentication methods unless you have set a different TTL for a specific authentication method.

> ℹ️ **Note:**
>
> For an authentication method to have the necessary permissions to perform actions, you will need to attach it to a matching role.
> To learn more about this, please go to [Role-Based Access Control (RBAC)](https://docs.akeyless.io/docs/rbac).

### Product Type

Accounts with multiple products can label **each** authentication method, mostly for billing and feature access based on their products. It is recommended to set the relevant product type for the expected usage to provide your end users with the exact features for the relevant product.

## Common Optional Features

The following optional features are available across Authentication Methods:

* **Location:** Set the path to the virtual folder where the authentication method is created, using `/` separators.
* **Description:** Add a description for the authentication method.
* **Expiration Date:** Select an access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.
* **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean cURL, SDKs, and so on. This parameter is optional. Leave it empty for unrestricted access.
* **Allowed Trusted Gateway IPs:** Comma-separated CIDR blocks. If specified, the Gateway using this IP range will be trusted to forward the original client IP. If empty, the Gateway's IP address will be used.
* **Audit Log Sub-Claims:** Include selected token sub-claims in Audit Logs (for example, `email`, `username`, or `uid_comment` for UID token flows).
* **JWT TTL (in minutes):** The time span from authentication to JWT expiration.
* **Allowed Client Type:** Select the allowed client types that will be authorized to use this authentication method. Multiple options can be selected. For example, `CLI`, `Web UI`, `Extension`, `Mobile`, `Gateway Admin`, or `SDK`.
* **Delete Protection:** Enable this option to protect the authentication method from accidental deletion.
* **Require Sub Claim on role association:** Enable this checkbox to require sub-claims when a role is associated with this authentication method.

## Tutorial

Check out our tutorial video on [Authentication Methods](https://tutorials.akeyless.io/docs/authentication-methods-and-api-key-authentication).
