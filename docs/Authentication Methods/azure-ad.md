---
title: Azure AD
excerpt: Azure Active Directory (AD)
deprecated: false
hidden: false
metadata:
  title: Azure Active Directory
  description: ''
  robots: index
next:
  description: >-
    Make sure to associate your new Authentication Method with an Access Role to
    grant the relevant permissions within Akeyless
---
Azure AD Authentication method enables authentication to Akeyless. Akeyless treats Azure as a trusted third party and verifies entities based on a JWT signed by the Azure AD for the configured tenant.

# Prerequisites

Depending on the Azure Identity type, enable the relevant [identity type](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview) on your Azure resource.

# Create an Azure AD Authentication Method from the CLI

Let's create a new Azure AD authentication method using the Akeyless CLI.
(You can also do this from the [Akeyless Console](https://docs.akeyless.io/docs/azure-ad#create-an-azure-active-directory-authentication-method-in-the-akeyless-console).)

To create an Azure AD authentication method from the CLI, run the following command:

```shell Akeyless CLI
akeyless auth-method create azure-ad \
--name &lt;Auth Method Name&gt;\
--bound-tenant-id &lt;Azure Tenant Id&gt;
```

Where:

* `name`: A unique name for the authentication method. The name can include the path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

* `bound-tenant-id`: A comma-separated list of Azure tenant IDs that are allowed to authenticate to Akeyless using this authentication method.

You can find the complete list of additional parameters for this command in the [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#p-stylecolorblueazure-adp) section.

# Configure Akeyless CLI with the Azure AD authentication method

To configure your CLI to work with Azure AD authentication, run the following command from an Azure VM with a system identity assigned:

```shell Akeyless CLI
akeyless configure --profile default --access-id &lt;AccessID&gt;  --access-type azure_ad 
akeyless get-cloud-identity --cloud-provider azure_ad
```

# Create an Azure AD authentication method in the Akeyless Console

1. Log in to the Akeyless Console and go to **Users & Auth Methods > New > Azure Active Directory**.

2. Define a **Name** for the authentication method, and specify the **Location** as a path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

3. Define the remaining parameters as follows:

* **Expiration Date:** Select the access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.

* **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean CURL, SDK, etc. This parameter is optional. Leave it empty for unrestricted access.

* **Allowed Trusted Gateway IPs:** Comma separated CIDR blocks. If specified, the Gateway using this IP range will be trusted to forward the original client IP. If empty, the Gateway's IP address will be used.

* **Audit Log Sub Claims:** Enter a comma-separated list of sub-claims keys to be included in the audit logs.

* **Bound Tenant ID:** Enter a comma-separated list of Azure tenant IDs for which access is allowed.

* **Custom Issuer URL:** The default value is `https://sts.windows.net/`\<bound-tenant-id>.

* **Custom JWKS URL:** The URL to the JSON Web Key Set (JWKS) containing the public keys that should be used to verify any JSON Web Token (JWT) issued by the authorization server. Default value is `https://login.microsoftonline.com/common/discovery/keys`.

* **Custom Audience URL:** The default value is `https://management.azure.com/`.

* **Bound Service Principal IDs:** Enter a comma-separated list of Azure AD Service Principal IDs for which access is allowed. This parameter is optional. Leave it empty for unrestricted access.

* **Bound Subscriptions IDs:** Enter a comma-separated list of subscription IDs for which access is allowed. This parameter is optional. Leave it empty for unrestricted access.

* **Bound Resource Groups:** Enter a comma-separated list of Resource Groups for which access is allowed. This parameter is optional. Leave it empty for unrestricted access.

* **Bound Resource Providers:** Enter a comma-separated list of resource providers for which access is allowed (e.g., `Microsoft.Compute`, `Microsoft.ManagedIdentity`, etc.). This parameter is optional. Leave it empty for unrestricted access.

* **Bound Resource Types:** Enter a comma-separated list of resource types for which access is allowed (e.g., `virtualMachines`, `userAssignedIdentities`, etc.). This parameter is optional. Leave it empty for unrestricted access.

* **Bound Resource Names:** Enter a comma-separated list of resource names for which access is allowed (e.g., a virtual machine name, scale set name, etc.). This parameter is optional. Leave it empty for unrestricted access.

* **Bound Resource Groups:** Enter a comma-separated list of Resource Groups for which access is allowed. This parameter is optional. Leave it empty for unrestricted access.

* **Bound Resource IDs:** Enter a comma-separated list of Resource IDs for which access is allowed. This parameter is optional. Leave it empty for unrestricted access.

* **Unique Identifier:** Optional, a unique identifier (ID) value that contains details uniquely identifying that resource. This sub-claim name is used to distinguish between different identities.

4. Click **Finish**.
