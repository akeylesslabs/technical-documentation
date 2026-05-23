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
This page discusses creating and using an Azure AD-based authentication method in Akeyless.

[Azure AD](https://learn.microsoft.com/en-us/entra/fundamentals/whatis) authentication enables Azure workloads to authenticate to Akeyless by using Azure-issued identity tokens.

## Creating an Azure AD Authentication Method

This action is distinct from creating a new Akeyless account: it creates an additional Azure AD-based authentication method for an existing account.

Required Azure AD setting:

* **Bound Tenant ID:** Configure the Azure tenant ID that is allowed to authenticate by using this authentication method.

Required Azure AD fields with default values:

* **Custom Issuer URL:** Prefilled with `https://sts.windows.net/<bound-tenant-id>/`.
* **Custom JWKS URL:** Prefilled with `https://login.microsoftonline.com/common/discovery/keys`.
* **Custom Audience URL:** Prefilled with `https://management.azure.com/`.

### Azure Identity Prerequisite

Enable a [managed identity](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview) on the Azure resource that authenticates to Akeyless. You can use either a **system-assigned** identity (tied to a single resource lifecycle) or a **user-assigned** identity (reusable across multiple resources). Make sure the identity is enabled on the source workload before running `akeyless configure` or `akeyless auth` with `azure_ad`.

### Creating an Azure AD Authentication Method with the Console

To create a new Azure AD-based authentication method with the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select **+ New**. This opens the **Create Authentication Method** form.
3. On the **Type** selection screen, select **Azure AD**, then **Next →**.
4. Enter a name for the Authentication Method in the **Name** field. Optionally, include a path using `/` separators to place the Authentication Method in a virtual folder, then select **Next →**.
5. Configure Azure AD-specific fields, such as **Bound Tenant ID**. For field details, see [Azure AD-Specific Optional Features](#azure-ad-specific-optional-features), then select **Next →**.
6. Configure Advanced Azure AD-specific fields, then select **Finish**.

### Creating an Azure AD Authentication Method with the CLI

To create an Azure AD-based authentication method with the CLI:

```shell
akeyless auth-method create azure-ad \
  --name <Azure AD Auth Method Name> \
  --bound-tenant-id <Azure Tenant ID>
```

[Read about more parameters available when creating an Azure AD-based authentication method.](https://docs.akeyless.io/docs/cli-ref-auth#create)

## Using an Azure AD Authentication Method

### Using an Azure AD Authentication Method with the CLI

To use an Azure AD-based authentication method with a CLI profile, run the [Akeyless configure command](https://docs.akeyless.io/docs/cli-reference#configure) from an Azure resource with managed identity enabled:

```shell
akeyless configure \
  --profile default \
  --access-id <Access ID> \
  --access-type azure_ad
```

For Azure US Government or Azure China, also set `--azure-cloud` to `AzureUSGovernment` or `AzureChinaCloud`.

> ℹ️ **Note:**
>
> Identities that require `--azure-cloud` (for example, Azure US Government or Azure China) are not supported for use as a Gateway identity.

To inspect the cloud identity token, run the [Akeyless get-cloud-identity command](https://docs.akeyless.io/docs/cli-ref-auth#get-cloud-identity):

```shell
akeyless get-cloud-identity \
  --cloud-provider azure_ad
```

For Azure US Government or Azure China, also set `--azure-cloud` to `AzureUSGovernment` or `AzureChinaCloud`.

To authenticate and retrieve a temporary Akeyless token, run the [Akeyless auth command](https://docs.akeyless.io/docs/cli-ref-auth#auth):

<!-- secret-stdout-scan:ok -->
```shell
akeyless auth \
  --access-id <Access ID> \
  --access-type azure_ad
```

For Azure US Government or Azure China, also set `--azure-cloud` to `AzureUSGovernment` or `AzureChinaCloud`.

## Associate with Access Roles

After creating the authentication method, associate it with one or more Access Roles so authenticated identities can perform actions in Akeyless.

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select the Azure AD authentication method.
3. Add the required Access Roles.
4. Save the changes.

For role configuration details, see [Access Roles](https://docs.akeyless.io/docs/rbac).

## Update an Existing Azure AD Authentication Method

Azure AD authentication methods can require updates over time, for example when tenant boundaries, resource constraints, or custom issuer and key endpoints change.

To update in the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select the Azure AD authentication method to update.
3. Update the required fields.
4. Save the changes.

To update with the CLI, use the relevant `akeyless auth-method update azure-ad` flags in [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth).

## Troubleshooting

If Azure AD authentication fails, check the following:

* The managed identity is enabled on the authenticating Azure resource.
* The tenant, subscription, and resource bounds match the authenticating identity context.
* Custom issuer, JWKS, and audience values are correct for the cloud environment.
* The authentication method is associated with the required Access Roles.

## Optional Features

For optional features that apply across Authentication Methods, see [Common Optional Features](https://docs.akeyless.io/docs/access-and-authentication-methods#common-optional-features).

### Azure AD-Specific Optional Features

* **Bound Group IDs:** Limit authentication to one or more Azure AD group IDs.
  In the Console, enter values as a comma-separated list. With the CLI, repeat `--bound-group-id`.
* **Bound Resource Groups:** Limit authentication to resources in one or more Azure resource groups.
  In the Console, enter values as a comma-separated list. With the CLI, repeat `--bound-rg-id`.
* **Bound Resource IDs:** Limit authentication to one or more full Azure resource IDs.
  In the Console, enter values as a comma-separated list. With the CLI, repeat `--bound-resource-id`.
* **Bound Resource Names:** Limit authentication to one or more Azure resource names.
  In the Console, enter values as a comma-separated list. With the CLI, repeat `--bound-resource-names`.
* **Bound Resource Providers:** Limit authentication to one or more Azure resource providers (for example, `Microsoft.Compute`, `Microsoft.ManagedIdentity`).
  In the Console, enter values as a comma-separated list. With the CLI, repeat `--bound-providers`.
* **Bound Resource Types:** Limit authentication to one or more Azure resource types (for example, `virtualMachines`, `userAssignedIdentities`).
  In the Console, enter values as a comma-separated list. With the CLI, repeat `--bound-resource-types`.
* **Bound Service Principal IDs:** Limit authentication to one or more Azure AD service principal IDs.
  In the Console, enter values as a comma-separated list. With the CLI, repeat `--bound-spid`.
* **Bound Subscription IDs:** Limit authentication to one or more Azure subscription IDs.
  In the Console, enter values as a comma-separated list. With the CLI, repeat `--bound-sub-id`.
* **Custom Audience URL:** Override the expected audience claim value.
  Global default is `https://management.azure.com/`.
  For Azure US Government, use `https://management.usgovcloudapi.net/`.
  For Azure China, use `https://management.chinacloudapi.cn/`.
  CLI note: the `--audience` flag is supported but marked deprecated.
* **Custom Issuer URL:** Override the issuer URL used to validate Azure-issued tokens. If not set, the default pattern is `https://sts.windows.net/<bound-tenant-id>/`.
* **Custom JWKS URL:** Override the JSON Web Key Set (JWKS) endpoint used for JWT signature verification.
  Global default is `https://login.microsoftonline.com/common/discovery/keys`.
  For Azure US Government, use `https://login.microsoftonline.us/common/discovery/keys`.
  For Azure China, use `https://login.chinacloudapi.cn/common/discovery/keys`.
* **Unique Identifier:** Set a sub-claim key used to uniquely identify authenticated Azure principals.
