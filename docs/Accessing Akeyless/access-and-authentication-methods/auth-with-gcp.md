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

## Creating a GCP Authentication Method

This action is distinct from creating a new Akeyless account: it creates an additional GCP-based authentication method for an existing account.

Required GCP settings:

* **GCP Type:** Select either **IAM** or **GCE**. These options are mutually exclusive.
* Configure at least one of the following:
    * **Bound Projects**
    * **Service Account Credentials** (`--service-account-creds-file` or `--service-account-creds-data`)
* **Audience:** Required. This value is used to validate the `aud` claim in the GCP identity token and helps ensure the token was minted for this authentication flow. The default prefilled value is `akeyless.io`.

### Decision Guide

Use this guidance to select the right GCP authentication settings for your workload.

#### Choosing GCP Type: IAM or GCE

* Choose **IAM** when authentication should be based on service account identity (for example, CI/CD workloads, GKE workloads, or other services that authenticate as a service account principal).
* Choose **GCE** when authentication should be scoped to Compute Engine instance context, and you plan to use instance-oriented constraints such as **Bound Zones**, **Bound Regions**, or **Bound Labels**.

#### Choosing Identity Source: Bound Projects or Service Account Credentials

* Choose **Bound Projects** when project-level scoping is sufficient and you prefer simpler setup without supplying credential material.
* Choose **Service Account Credentials** when you need explicit validation using a service account JSON key, or when your policy requires stronger identity verification than project-only scoping.
* You can configure both for layered controls, but at least one is required.

### Creating a GCP Authentication Method with the Console

To create a new GCP-based authentication method with the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select **+ New**. This opens the **Create Authentication Method** form.
3. On the **Type** selection screen, select **GCP**, then **Next →**.
4. Enter a name for the Authentication Method in the **Name** field. Optionally, include a path using `/` separators to place the Authentication Method in a virtual folder, then select **Next →**.
5. In the **GCP Type** field, select either **IAM** or **GCE** (mutually exclusive), then configure required and optional fields. For field details, see [GCP-Specific Optional Features](#gcp-specific-optional-features), then select **Finish**.

### Creating a GCP Authentication Method with the CLI

To create a GCP-based authentication method with the CLI using bound projects:

```shell
akeyless auth-method create gcp \
  --name <GCP Auth Method Name> \
  --type <iam|gce> \
  --bound-projects <GCP Project ID> \
  --audience akeyless.io
```

Or, use service account credentials instead of bound projects:

```shell
akeyless auth-method create gcp \
  --name <GCP Auth Method Name> \
  --type <iam|gce> \
  --service-account-creds-file <Path to Service Account JSON> \
  --audience akeyless.io
```

Where:

* `--name`: Authentication Method name. You can include a folder-like path by using `/` separators.
* `--type`: Authentication type. Set to `iam` or `gce`.
* `--bound-projects`: One or more GCP project IDs. Repeat the flag for multiple values. Required if service account credentials are not provided.
* `--service-account-creds-file` or `--service-account-creds-data`: Service account credentials. Required if bound projects are not provided.
* `--audience`: JWT audience value to validate against the token `aud` claim. Use this to scope tokens to the intended relying party and reduce token replay across unintended services. The default value is `akeyless.io`.

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

Use this reference when creating or editing a GCP authentication method with the Console.

* **GCP Type (Required):** Select either `IAM` or `GCE`. These options are mutually exclusive.
* **Bound Projects:** Enter one or more project IDs. Required if **Service Account Credentials** is not provided.
* **Service Account Credentials:** Provide Base64-encoded credentials data or upload a JSON credentials file. Required if **Bound Projects** is not provided.
* **Audience (Required):** Enter the expected JWT audience value. Akeyless validates this value against the token `aud` claim to confirm the token was intended for this authentication flow. The default prefilled value is `akeyless.io`.
* **Bound Service Accounts (Optional):** Available for both `IAM` and `GCE`.
* **Unique Identifier (Optional):** Available for both `IAM` and `GCE`.
* **Bound Zones (Optional):** Available for `GCE`.
* **Bound Regions (Optional):** Available for `GCE`.
* **Bound Labels (Optional):** Available for `GCE`. Use `key:value` format.

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
