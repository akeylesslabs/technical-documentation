---
title: OCI IAM
excerpt: Oracle Cloud Infrastructure (OCI) IAM
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
[OCI IAM](https://docs.oracle.com/en-us/iaas/Content/Identity/Concepts/overview.htm) authentication method provides an automated flow to retrieve an Akeyless token for Oracle Cloud Infrastructure IAM principals like API Key, instances or resources using OCI IAM group or dynamic group [components](https://docs.oracle.com/en-us/iaas/Content/Identity/Concepts/overview.htm#Componen).

# Configuration

To authenticate **OCI** resources to Akeyless, the following configuration is required: 

* Create a [Dynamic Group](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingdynamicgroups.htm) for authenticating resources 
* Create a [Group](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managinggroups.htm) to authenticate users 

Once the group is created, a policy needs to be added to it:

```shell Dynamic Group
allow dynamic-group <Dynamic-Group-Name> to {AUTHENTICATION_INSPECT} in tenancy
allow dynamic-group <Dynamic-Group-Name> to {GROUP_MEMBERSHIP_INSPECT} in tenancy
```
```shell Group
allow group <Group-Name> to {AUTHENTICATION_INSPECT} in tenancy
allow group <Group-Name> to {GROUP_MEMBERSHIP_INSPECT} in tenancy
```

More information about the policies can be found [here](https://docs.oracle.com/en-us/iaas/mysql-database/doc/mandatory-policies-and-permissions.html#GUID-2D9D3C84-07A3-4BEE-82C7-B5A72A943F53).

Once set, you can continue creating the authentication method.

# Create an OCI IAM Authentication Method from the CLI

To create an OCI IAM authentication method from the CLI, run the following command:

```shell Akeyless CLI
akeyless auth-method create oci \
--name <Auth Method Name> \
--tenant-ocid <Oracle Tenant Id> \
--group-ocid <Oracle Group Id> 
```

Where:

* `name`: A unique name for the authentication method. The name can include the path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

* `tenant-ocid`: An OCI tenant ID to authenticate to Akeyless using this authentication method. 

* `group-ocid`: An OCI group ID that is allowed to authenticate to Akeyless using this authentication method. (You can provide more than one Group ID by repeating this parameter.

You can find the complete list of additional parameters for this command in the [CLI Reference - Authentication section](https://docs.akeyless.io/docs/cli-ref-auth#p-stylecolorblueocip).

# Configure Akeyless CLI with the OCI IAM authentication method

To configure your CLI to work with OCI IAM authentication, run the following command **from an Oracle Cloud resource**: 

```shell Akeyless CLI
akeyless configure --profile default --access-id <AccessID> --access-type oci --oci-auth-type apikey 

akeyless get-cloud-identity --oci-auth-type apikey 
```

Where: 

* `oci-auth-type`: Represents the [OCI Authentication type  ](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdk_authentication_methods.htm) , supporting `apikey`,`resource` and `instance`.

> 📘 Note:
>
> When the `group-ocid` explicitly provided, the authentication flow will use them, if no **group** provided, the CLI will send a preliminary request to verify that the user is a member of the same tenant,  and will extract the required **group** from the response.

# Create an OCI IAM authentication method in the Akeyless Console

1. Log in to the Akeyless Console and go to **Users & Auth Methods > New > OCI IAM**.

2. Define a **Name** for the authentication method, and specify the **Location** as a path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

3. Define the remaining parameters as follows:

* **Tenant OCID:** Enter the Oracle Cloud tenant IDs for which access is allowed.

* **Group OCIDs:** Enter a comma-separated list of full OCI groups IDs for which access is allowed. For example: `ocid1.group.oc1..abc,ocid1.group.oc1..xyz`.

* **Expiration Date:** Select the access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.

* **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean CURL, SDK, etc. This parameter is optional. Leave it empty for unrestricted access.

* **Allowed Trusted Gateway IPs:** Comma separated CIDR blocks. If specified, the Gateway using this IP range will be trusted to forward the original client IP. If empty, the Gateway's IP address will be used.

* **Audit Log Sub Claims:** Enter a comma-separated list of sub-claims keys to be included in the audit logs.

4. Click **Finish**.
