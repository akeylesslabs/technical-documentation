---
title: GCP
excerpt: Google Cloud Platform (GCP)
deprecated: false
hidden: false
metadata:
  title: GCP
  description: ''
  robots: index
next:
  description: >-
    Make sure to associate your new Authentication Method with an Access Role to
    grant the relevant permissions within Akeyless
---
This page discusses creating and using a GCP-based authentication method in Akeyless.

The Google Cloud Platform (GCP) authentication method enables GCP entities to authenticate to Akeyless. Akeyless treats Google Cloud as a trusted third party and verifies entities requesting authentication against Google Cloud APIs. It supports both Google Cloud Identity and Access Management (IAM) service accounts and Google Compute Engine (GCE) instances for workload authentication.

> TODO(DOCS-98): Confirm product guidance for direct interactive Console sign-in with GCP auth. This behavior is not explicitly documented in CLI source.

## Creating a GCP Authentication Method

This action is distinct from creating a new Akeyless account: it creates an additional GCP-based authentication method for an existing account.

Required GCP settings:

* Configure at least one of the following:
    * **Bound Projects** (`--bound-projects`)
    * **Service Account Credentials** (`--service-account-creds-file` or `--service-account-creds-data`)
* If you use **Bound Labels** (`--bound-labels`), service account credentials are required.

### Creating a GCP Authentication Method with the Console

To create a new GCP-based authentication method with the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select **+ New**. This opens the **Create Authentication Method** form.
3. On the **Type** selection screen, select **GCP**, then **Next ->**.
4. Enter a name for the Authentication Method in the **Name** field. Optionally, include a path using `/` separators to place the Authentication Method in a virtual folder, then select **Next ->**.
5. Configure GCP-specific fields as needed. For field details, see [GCP-Specific Optional Features](#gcp-specific-optional-features), then select **Finish**.

### GCP Console Field Reference

In the Console form, define fields as follows:

* **Expiration Date:** Optional. Set an access expiration date, or leave empty for no expiration.
* **Allowed Client IPs:** Optional. Comma-separated CIDR blocks from which clients can issue calls.
* **Allowed Trusted Gateway IPs:** Optional. Comma-separated CIDR blocks. If set, Gateway IPs in these ranges are trusted to forward the original client IP.
* **Audit Log Sub Claims:** Optional. Comma-separated sub-claim keys to include in audit logs.
* **Allowed Client Type:** Optional. Client type authorized to use this method (for example, `CLI`, `SDK`, `Gateway Admin`).
* **GCP Type:** Required. `IAM` or `GCE`.
* **Bound Projects:** Optional unless no service account credentials are provided. Comma-separated project IDs.
* **Audience:** Optional. JWT audience claim to verify. Default is `akeyless.io`.
* **Service Account Credentials:** Optional if bound projects are provided. Provide Base64-encoded credentials or upload JSON.
* **Bound Service Accounts:** Optional. Relevant for IAM.
* **Bound Zones:** Optional. Relevant for GCE.
* **Bound Regions:** Optional. Relevant for GCE.
* **Bound Labels:** Optional. Relevant for GCE. Use `key:value` format.
* **Unique Identifier:** Optional. Sub-claim key used to distinguish identities.

> TODO(DOCS-98): Re-validate Console labels/field names against current UI. CLI/source confirms server behavior, but Console copy can change independently.

### Creating a GCP Authentication Method with the CLI

To create a GCP-based authentication method with the CLI:

```shell
akeyless auth-method create gcp \
  --name <GCP Auth Method Name> \
  --type <iam|gce> \
  --bound-projects <GCP Project ID> \
  --audience akeyless.io
```

Where:

* `--name`: Authentication Method name. You can include a folder-like path by using `/` separators.
* `--type`: Authentication type (`iam` or `gce`).
* `--bound-projects`: One or more GCP project IDs. Repeat the flag for multiple values.
* `--audience`: JWT audience to verify. Default is `akeyless.io`.

Read about more parameters available when creating a GCP-based authentication method: [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#create).

## Using a GCP Authentication Method

### Using a GCP Authentication Method with the CLI

To use a GCP-based authentication method with a CLI profile, run the [Akeyless configure command](https://docs.akeyless.io/docs/cli-reference#configure) from a GCP resource (for example, a GCE instance or a workload running in GKE):

```shell
akeyless configure \
  --profile default \
  --access-id <Access ID> \
  --access-type gcp \
  --gcp-audience akeyless.io
```

To inspect the cloud identity token, run the [Akeyless get-cloud-identity command](https://docs.akeyless.io/docs/cli-ref-auth#get-cloud-identity):

```shell
akeyless get-cloud-identity \
  --cloud-provider gcp \
  --gcp-audience akeyless.io
```

To authenticate and retrieve a temporary Akeyless token, run the [Akeyless auth command](https://docs.akeyless.io/docs/cli-ref-auth#auth):

```shell
akeyless auth \
  --access-id <Access ID> \
  --access-type gcp \
  --gcp-audience akeyless.io
```

## Optional Features

For optional features that apply across Authentication Methods, see [Common Optional Features](https://docs.akeyless.io/docs/access-and-authentication-methods#common-optional-features).

### GCP-Specific Optional Features

* **GCP Type:** Choose `iam` or `gce`.
* **Audience:** Set the audience claim expected in the JWT. If not set, Akeyless uses `akeyless.io`.
* **Service Account Credentials:** Set `--service-account-creds-file` or `--service-account-creds-data` (base64-encoded JSON).
* **Bound Service Accounts:** Limit IAM authentication to one or more specific service accounts.
* **Bound Zones:** Limit GCE authentication to instances in specific zones.
* **Bound Regions:** Limit GCE authentication to instances in specific regions.
* **Bound Labels:** Limit GCE authentication to instances that match specific labels.
* **Unique Identifier:** Set a sub-claim key used to uniquely identify authenticated GCP principals.

## GKE Workload Identity Considerations

When authenticating from a pod inside a Google Kubernetes Engine (GKE) cluster with GKE Workload Identity enabled, bound rules other than **Bound Service Accounts** do not apply.

To use GKE Workload Identity with bounded rules, configure only **Bound Service Accounts**.

For setup guidance, follow the [GKE Workload Identity guide](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity).

## Prerequisites

If you provide service account credentials, the authentication implementation validates this permission set:

```shell
iam.serviceAccounts.get
iam.serviceAccountKeys.get
compute.instances.get
compute.instanceGroups.list
```

These permissions are validated through Google Cloud Resource Manager `testIamPermissions` in the service account validation path.

> TODO(DOCS-98): Confirm whether additional permissions are required in production flows beyond the validation checks in `gcp_auth`.

## Related Pages

* [Access and Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods)
* [Access Role-Based Access Control (RBAC)](https://docs.akeyless.io/docs/rbac)
* [Kubernetes with Helm Deployment](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm)
* [Google Kubernetes Engine Deployment](https://docs.akeyless.io/docs/gateway-deploy-google-kubernetes-engine)
* [Gateway Authentication and Access](https://docs.akeyless.io/docs/gateway-authentication-and-access)
