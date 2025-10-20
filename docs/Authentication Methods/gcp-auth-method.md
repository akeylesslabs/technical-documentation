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
The Google Cloud Platform (GCP) authentication method enables GCP entities to authenticate to the Akeyless Platform. Akeyless treats Google Cloud as a trusted third party and verifies entities requesting to authenticate against the Google Cloud APIs. It supports both Google Cloud Identity and Access Management (IAM) service accounts and Google Compute Engine (GCE) instances for authentication.

# Prerequisites

You will need a GCP Service Account with the following permissions:

```shell
iam.serviceAccounts.get
iam.serviceAccountKeys.get
compute.instances.get
compute.instanceGroups.list
```

> 👍 Note
>
> **GKE Workloads Authentication**
>
> When authenticating from a pod inside a Google Kubernetes Engine (GKE) cluster using GKE Workload Identity enabled, any bounded rules other than `Bound Service Accounts` **will not apply**. GKE Workload Identity conceals metadata information about the running instance.
>
> To work with the GKE Workload Identity with bounded rules, please configure **only** the `Bound Service Accounts` rule.
>
> Be sure to follow the <a href="https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity" target="_blank">GKE Guide</a> when configuring the GKE Workload Identity.

# Create a GCP Authentication Method from the CLI

Let's create a new GCP authentication method using the Akeyless CLI. (You can do this also from the [Akeyless Console](https://akeyless.readme.io/docs/gcp-auth-method#create-a-gcp-authentication-method-in-the-akeyless-console).)

To create a GCP authentication method from the CLI, run the following command:

```shell Akeyless CLI
akeyless auth-method create gcp \
--name <Auth Method Name> \
--type <iam|gce> \
--bound-projects <GCP Project> \
--audience <audience to verify in the JWT received by the client>
```

Where:

* `name`: A unique name for the authentication method. The name can include the path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

* `type`: The authentication method type. It should be either `iam` or `gce`.

* `audience`: The audience to verify the JWT received by the client. By default, `akeyless.io`.

* `bound-projects`:  A list of GCP Project IDs.

You can find the complete list of additional parameters for this command in the [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#p-stylecolorbluegcpp) section.

# Configure Akeyless CLI with the GCP authentication method

To configure your CLI to work with GCP authentication, run the following command from a GCP resource:

```shell Akeyless CLI
akeyless configure --profile default --access-id <AccessID>  --access-type gcp --gcp-audience akeyless.io
akeyless get-cloud-identity --cloud-provider gcp
```

# Create a GCP Authentication Method in the Akeyless Console

1. Log in to the Akeyless Console and go to **Users & Auth Methods > New > GCP**.

2. Define a **Name** for the authentication method, and specify the **Location** as a path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

3. Define the remaining parameters as follows:

* **Expiration Date:** Select the access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.

* **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean CURL, SDK, etc. This parameter is optional. Leave it empty for unrestricted access.

* **Allowed Trusted Gateway IPs:** Comma separated CIDR blocks. If specified, the Gateway using this IP range will be trusted to forward the original client IP. If empty, the Gateway's IP address will be used.

* **Audit Log Sub Claims:** Enter a comma-separated list of sub-claims keys to be included in the audit logs.

* **Allowed Client Type:** Select the allowed client type that will be authorized to use this authentication method. e.g. `CLI`, `SDK`,  `Gateway Admin`.

* **GCP Type:** Select the type of GCP authentication method to create, either `IAM` or `GCE`.

* **Bound Projects:** Enter a comma-separated list of GCP project IDs. The client must belong to one of these projects to authenticate. By "client," we mean CURL, SDK, etc. This parameter is optional. Leave it empty for unrestricted access.

* **Audience:** Enter the audience to verify in the JWT received by the client. By default,
  the **Audience** is `akeyless.io`.

* **Service Account Credentials:** Enter a Base64-encoded string of the service account credentials or upload a JSON file with the service account credentials. Required in case no project is provided.

* **Bound Service Accounts:** Enter a valid Service Account. This parameter is only relevant for **IAM** authentication methods. Leave it empty for unrestricted access.

* **Bound Zones:** Enter a comma-separated list of zones. The GCE instance must belong to one of these zones to authenticate. This parameter is only relevant for **GCE** authentication methods. Leave it empty for unrestricted access.

* **Bound Regions:** Enter a comma-separated list of regions. The GCE instance must belong to one of these regions to authenticate. This parameter is only relevant for **GCE** authentication methods. Leave it empty for unrestricted access.

* **Bound Labels:** Enter a `key:value` list of GCP labels. The GCE instance must have one of these labels to authenticate. This parameter is only relevant for **GCE** authentication methods. Leave it empty for unrestricted access.

* **Unique Identifier:** Optional, a unique identifier (ID) value that contains details uniquely identifying that resource. This sub-claim name is used to distinguish between different identities.

4. Click **Finish**.
