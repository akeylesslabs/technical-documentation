---
title: Kubernetes Legacy Deployment
excerpt: ''
deprecated: true
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: advanced-k8s-gateway-configuration
      title: Advanced Kubernetes Configuration
    - type: basic
      slug: configuring-tls
      title: Configuring TLS
---
> ℹ️ **Note (Gateway New Chart):**
>
> The Gateway new chart docs is now available [here](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm).

This page applies only to the legacy `akeyless-api-gateway` Helm chart and the legacy `akeylessUserAuth` values schema.

The Akeyless Gateway can be deployed on a Kubernetes (K8s) cluster using the Helm package manager. Akeyless provides a [Helm Chart](https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-api-gateway) to bootstrap deployment. In the case of a Kubernetes Deployment, configuration occurs before installation by modifying values in the Helm Chart.

## Prerequisites

* An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) with an [Access Role](https://docs.akeyless.io/docs/rbac) to create and manage [Secrets, Keys](https://docs.akeyless.io/docs/manage-your-secrets-overview), and [Targets](https://docs.akeyless.io/docs/targets)

* [Helm](https://helm.sh/) Installed

* Kubernetes Installed with [Kubernetes Metrics Server](https://github.com/kubernetes-sigs/metrics-server)

* Minimum 1 vCPU available with 2 GB RAM.

* Network connection to [Akeyless SaaS Core Services](https://docs.akeyless.io/docs/gateway-network-connectivity) from your cluster

> ⚠️ **Warning:**
>
> Make sure that this server is not globally opened to the public network. Akeyless Gateway requires only connections to Akeyless SaaS Core Services.

* The following ports need to be open on the cluster **only for internal** network access:

| Service | Port |
| --- | --- |
| [Gateway Configuration Manager](https://docs.akeyless.io/docs/configure-gateway) | 8000 |
| Gateway Console | 18888 |
| [HashiCorp Vault Proxy](https://docs.akeyless.io/docs/hashicorp-vault-proxy) | 8200 |
| Akeyless V1 REST API | 8080 |
| [Akeyless V2 REST API](https://docs.akeyless.io/reference) | 8081 |
| [KMIP Server](https://docs.akeyless.io/docs/kmip-server) | 5696 |

## Helm Chart Configuration

1. Add the following repository to your Helm repository list:

    ```shell
    helm repo add akeyless https://akeylesslabs.github.io/helm-charts
    helm repo update
    ```

2. Fetch the `values.yaml` file from Akeyless repository:

    ```shell
    helm show values akeyless/akeyless-api-gateway > values.yaml
    ```

3. Use your favorite editor to set the relevant parameters in the `values.yaml` file:

    ```shell
    vi values.yaml
    ```

## Authentication

Set a default [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) for the Gateway to control the level of access the Gateway instance will have inside your Akeyless account.

The following [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) are supported for Kubernetes deployments:

* [API Key](https://docs.akeyless.io/docs/auth-with-api-key)

* [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws)

* [GCP](https://docs.akeyless.io/docs/auth-with-gcp)

* [Azure Active Directory](https://docs.akeyless.io/docs/auth-with-azure)

* [Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity)

### API Key Authentication

To set your Gateway default authentication based on [API Key](https://docs.akeyless.io/docs/auth-with-api-key), provide the relevant `Access ID` and `Access Key`:

```yaml values.yaml
akeylessUserAuth:
  # adminAccessId is a required field. Supported types: access_key, password, or cloud identity (aws_iam / azure_ad / gcp_gce)
  adminAccessId: <API Key Access ID>
  adminAccessKey: <Access Key>
```

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#installation) instructions.

### CSP IAM Authentication

While running your Kubernetes cluster inside your cloud environment, you can use [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws), [GCP](https://docs.akeyless.io/docs/auth-with-gcp), or [Azure Active Directory](https://docs.akeyless.io/docs/auth-with-azure), using machine-to-machine authentication between Akeyless and your Cloud Service Provider with a list of [admin users](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#gateway-admins) who can manage your Gateway.

Set the `adminAccessId` with your IAM [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) `Access ID`, where you can define a list of users who can manage your Gateway by setting the `allowedAccessPermissions` field with any other `Access ID` of your [SAML](https://docs.akeyless.io/docs/auth-with-saml), [OIDC](https://docs.akeyless.io/docs/auth-with-oidc), or an [API Key](https://docs.akeyless.io/docs/auth-with-api-key), as described [here](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#access-permissions).

### AWS IAM

AWS IAM can be used in the following approaches:

* Instance IAM Role

* Service Account IAM Role

In both cases, provide your [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws) Auth Method's `Access ID` as your `adminAccessId`, and at least one other `Access ID` in the `allowedAccessPermissions` section - to provide human users access to [config and manage your Gateway](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#gateway-admins):

```yaml values.yaml
akeylessUserAuth:
  adminAccessId: <AWS IAM Access ID>
  allowedAccessPermissions: {}
```

When working from an AWS instance with an IAM Role associated with it (which is the default state for EKS clusters that leverage the IAM Role of their Node group), nothing else is required - as the Gateway will be leveraging the IAM Role of the AWS instance itself where Kubernetes is running.

Alternatively, you can also leverage an IAM Role assumed by a Kubernetes ServiceAccount in your Cluster. For that, you must either [create an IAM Role bound to a Kubernetes ServiceAccount](https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html), or use an existing IAM role for annotating the Service Account in the Gateway's `values.yaml` Helm chart:
Set the `serviceAccountName` with the desired Kubernetes ServiceAccount name, and set its `eks.amazonaws.com/role-arn` annotation to the ARN of the IAM Role in question (which is constructed using the following format: `arn:aws:iam::<AWS-Account-ID>:role/<IAM-Role-Name>`).

You can also create a new Service Account by simply setting the `create` field to `true`, so the `serviceAccountName` you defined will be created upon deployment. Furthermore, if the `serviceAccountName` is left empty, by default - the chart will create a new ServiceAccount called `<release name>-akeyless-gateway`.
Make sure to set the required role-arn `annotation` to connect your IAM Role with the ServiceAccount in **any** of the scenarios.

```yaml values.yaml
deployment:
  annotations: {}
  labels: {}
  service_account:
    create: true
    serviceAccountName: <EKS SA name>
    annotations:
      eks.amazonaws.com/role-arn: arn:aws:iam::<AWS Account ID>:role/<IAM Role Name>

akeylessUserAuth:
  adminAccessId: <AWS IAM Access ID>
  allowedAccessPermissions: {}
```

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#installation) instructions.

### GCP

Google Kubernetes Engine (GKE) can run Akeyless Gateway in its secured and managed Kubernetes Service in standard or autopilot mode.

Deploying Akeyless Gateway by way of the Helm chart using the authentication between your Gateway and Akeyless SaaS using our [GCP Authentication method](https://docs.akeyless.io/docs/auth-with-gcp) can be done using the GCP Workload Identity mechanism.

Workload Identity allows workloads in your GKE clusters to impersonate Identity and Access Management (IAM) Service Accounts to access Google Cloud services. Workload Identity is enabled by default on Autopilot clusters.

Follow the [GKE workload identities guide](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#authenticating_to) to enable GKE workload identities on your cluster.

Create a Kubernetes ServiceAccount for Akeyless Gateway to use. You can also use the default Kubernetes ServiceAccount in the default or any existing Namespace.

Use the existing IAM service account that is bound to your [GCP](https://docs.akeyless.io/docs/auth-with-gcp) Auth Method.

> ℹ️ **Note:**
>
> When authenticating from a pod inside a Google Kubernetes Engine (GKE) cluster using GKE Workload Identity enabled, any `bounded rules` other than `Bound Service Accounts` will not apply. GKE Workload Identity conceals metadata information about the running instance.
>
> To work with the GKE Workload Identity you must configure **only** the `Bound Service Accounts` field in your [GCP Auth Method](https://docs.akeyless.io/docs/auth-with-gcp).

Allow the Kubernetes ServiceAccount to impersonate the IAM service account by adding an IAM policy binding between the two service accounts. This binding allows the Kubernetes ServiceAccount to act as the IAM service account.

Replace the following:
`PROJECT_ID`: your Google Cloud project ID.
`GSA_NAME`: the name of your IAM service account.
`GSA_PROJECT`: the project ID of the Google Cloud project of your IAM service account.
`KSA_NAME`: the name of your new Kubernetes ServiceAccount.
`NAMESPACE`: the name of the Kubernetes Namespace for the service account.

```shell GKE
gcloud iam service-accounts add-iam-policy-binding GSA_NAME@GSA_PROJECT.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:PROJECT_ID.svc.id.goog[NAMESPACE/KSA_NAME]"
```

Annotate the Kubernetes ServiceAccount with the email address of the IAM service account.

```shell GKE
kubectl annotate serviceaccount KSA_NAME \
    --namespace NAMESPACE \
    iam.gke.io/gcp-service-account=GSA_NAME@GSA_PROJECT.iam.gserviceaccount.com
```

Set the relevant Kubernetes `serviceAccountName` or leave it empty to use the `default` Kubernetes ServiceAccount, update the `annotations`, and enable the `nodeSelector` to schedule the workloads on nodes that use Workload Identity and to use the annotated Kubernetes ServiceAccount.

And set your [GCP](https://docs.akeyless.io/docs/auth-with-gcp) `Access ID` as your `adminAccessId` and at least one another `Access ID` in the `allowedAccessPermissions` section, to provide human users access to [config and manage your Gateway](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#gateway-admins):

```yaml values.yaml
deployment:
  annotations: {}
  labels: {}
  service_account:
    create: false
    serviceAccountName: <GKE SA Name>
   annotations:
        iam.gke.io/gcp-service-account: <GCP SA Name>
  nodeSelector:
         iam.gke.io/gke-metadata-server-enabled: "true"    
akeylessUserAuth:
  adminAccessId: <GCP GCE Access ID>
  allowedAccessPermissions: {}
```

> ℹ️ **Info:**
>
> **NodeSelector** - For Autopilot clusters, omit the `nodeSelector` field. Autopilot rejects this `nodeSelector` because all nodes use Workload Identity.

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#installation) instructions.

### Azure Active Directory

Azure AD authentication is provided to AKS clusters with OpenID Connect. OpenID Connect is an identity layer built on top of the OAuth 2.0 protocol. Akeyless treats Azure as a trusted third party and verifies entities based on a JWT signed by the Azure Active Directory for the configured tenant.

To use [Azure workload identity](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster) for your Gateway deployment, add the following label: `azure.workload.identity/use: "true"`, set the AKS Service Account name and the Azure Client ID using the annotation `azure.workload.identity/client-id`, and set your [Azure Active Directory](https://docs.akeyless.io/docs/auth-with-azure) `Access ID` as your `adminAccessId` and at least one another `Access ID` in the `allowedAccessPermissions` section, to provide human users access to [config and manage your Gateway](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#gateway-admins):

```yaml
deployment:
  annotations: {}
  labels:
    azure.workload.identity/use: "true"
  service_account:
    create: false
    serviceAccountName: <AKS SA Name> 
    annotations:
      azure.workload.identity/client-id: <user assigned client id>
akeylessUserAuth:
  # adminAccessId is required field, supported types: access_key,password or cloud identity(aws_iam/azure_ad/gcp_gce)
  adminAccessId: < Azure AD Access ID>
  allowedAccessPermissions: {}
```

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#installation) instructions.

### Universal Identity

Akeyless supports the [Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity) Authentication Method for on-premises Kubernetes cluster environments, eliminating the secret zero problem within configuration files.

Set the `adminUIDInitToken` field with your initial root [Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity) token. Set the rotation interval and choose either to generate a child token for your pods using `uidCreateChildTokenPerPod` field.

```yaml values.yaml
akeylessUserAuth:
  adminUIDInitToken: u-xxxxxxxxxxxx
universalIdentity:
  # interval im minutes, if empty the token will be rotated in token-ttl/3  max=10 
  uidRotationInterval: "5m" 
  uidCreateChildTokenPerPod: "disable"
```

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#installation) instructions.

### Certificates

To set your Gateway default authentication based on [Certificates](https://docs.akeyless.io/docs/auth-with-certificate) provide the relevant `Access ID` as your `adminAccessId`, with a Base64-encoded `Certificate`, and `Certificate Key`, with at least one another `Access ID` in the `allowedAccessPermissions` section, to provide human users access to [config and manage your Gateway](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#gateway-admins):

```yaml
akeylessUserAuth:
  adminAccessId: <Access ID>
  adminBase64Certificate: <Base64 Certificate>
  adminBase64CertificateKey: <Base64 Cert key>
  allowedAccessPermissions: {}
```

Alternatively, you can provide the `certificate` and your `certificate key` as `k8s` secrets, as described in [this](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference#working-with-k8s-secrets) guide.

## Gateway Admins

To support local management of your Gateway configuration, you can set a list of `Access ID` values that can log in and manage your Gateway. This setting can also work with [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) (when a shared authentication method is used), where for each entry you need to define a unique `name` which should describe the **Access Permission** object, with an `access-id`, `sub_claims` when applicable, and a list of `permissions`.

For example:

```yaml values.yaml
  allowedAccessPermissions: 
    - name: Administrators
      access_id: p-yyyyyy
      sub_claims:
        email:
          - test01@testhost.com
          - test02@testhost.com
        group:
          - Devops
      permissions:
        - admin
```

In this case, the above will create an **Access Permission** object named **Administrators**, associated with an Auth Method `p-yyyyyy` which for example is your [SAML](https://docs.akeyless.io/docs/auth-with-saml) or [OIDC](https://docs.akeyless.io/docs/auth-with-oidc) `Access ID`, where a user that at least matches one [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) attribute, will be authorized to access the Gateway with **Admin** permissions:

In our example, `test01@testhost.com` and `test02@testhost.com` will be authorized, and any member of `group=Devops` will also be authorized.

In this case, the `Access ID` belongs to the authentication method created for a certain Identity Provider. **If you don't specify the sub-claims, every user authenticated by this IdP can log in to the Gateway with admin privileges.**

To work with [API Key](https://docs.akeyless.io/docs/auth-with-api-key) as an `allowedAccessPermissions` simply provide your [API Key](https://docs.akeyless.io/docs/auth-with-api-key) `Access ID` with a `name` for the **Access Permission** object, with a set of `permissions`.

### Access Permissions

To delegate the exact permissions users will have on your Gateway components you can explicitly grant permissions, for example, to grant permissions to a user to manage only your Gateway [Log Forwarding](https://docs.akeyless.io/docs/gateway-log-forwarding) settings:

```yaml values.yaml
  allowedAccessPermissions: 
    - name: Administrators
      access_id: p-yyyyyy
      sub_claims:
        email:
          - test01@testhost.com
          - test02@testhost.com
        group:
          - Devops
      permissions:
        - admin
    - name: LogForwarding
      access_id: p-xxxxxx
      sub_claims:
        email:
          - test03@testhost.com
      permissions:
        - log_forwarding
```

In the above example, your Gateway **Admins** are `test01@testhost.com,test01@testhost.com` or any user which is part of your `Devops` group in your **IdP**, where `test03@testhost.com` have permission to manage **only** your Gateway [Log Forwarding](https://docs.akeyless.io/docs/gateway-log-forwarding) settings.

Full list of available permissions:

For the complete and current list, see [Gateway Access Permissions Reference](https://docs.akeyless.io/docs/gateway-access-permissions-reference).

> ℹ️ **Note:**
>
> Only Gateway **Admins** can delegate permissions to additional users. Any pre-provisioned settings will not be editable from the Akeyless Console.

You may also edit this parameter on your console, by going to the Gateways tab and selecting the desired Gateway. On the right of the screen, you will see the Gateway details, including **Access Permissions**.

### CBA

To work with the CBA flow for Gateway-allowed users, in addition to the list of `allowedAccessPermissions` you provided, set the chart with the `enableSniProxy: true` setting under the `TLSConf` section as follows:

```yaml
TLSConf:
  enableSniProxy: true
```

> ℹ️ **Note:**
>
> All changes to allowed access IDs, such as editing, removing, and so on, can only be performed on **post-deployment allowed access IDs**. If an ID was defined during deployment it can't be removed or changed.

## Installation

1. To deploy the Gateway using the edited `values.yaml` file, run the following command:

    ```shell
    helm install gw akeyless/akeyless-api-gateway -f values.yaml
    ```

2. Check if the pods are up and running:

    ```shell
    kubectl get pod

    NAME                                       READY   STATUS    RESTARTS       AGE
    gw-akeyless-gateway-6554f7c66c-56fgs       1/1     Running   0              5s
    gw-akeyless-gateway-6554f7c66c-7jt8r       1/1     Running   0              5s
    ```

3. Log in to the Gateway using your browser (`http://Your-Akeyless-Gateway-URL:8000`) with your Gateway admin credentials.

## Upgrade Gateway

To upgrade your Gateway, when working with a specific version, first edit the version in your `values.yaml` file for example:

```yaml
# Akeyless API Gateway application version
 version: 3.36.2 # Or any other version number
```

Update the Helm repo and upgrade the Helm deployment.

```shell
helm repo update
helm upgrade gw akeyless/akeyless-api-gateway -f values.yaml
```

Check that the new pods are starting.
