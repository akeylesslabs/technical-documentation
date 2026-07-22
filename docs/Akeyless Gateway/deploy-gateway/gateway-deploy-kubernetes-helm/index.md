---
title: Kubernetes with Helm Deployment
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: gateway-kubernetes-helm-values-reference
      title: Helm Values Reference
slug: gateway-deploy-kubernetes-helm
---
Akeyless provides a [Helm chart](https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-gateway) to bootstrap the Akeyless Gateway deployment.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  This guide describe the flow using the **latest** chart of the Akeyless Gateway.

  The documentation for the legacy charts is available [here](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment)
</Callout>

## Choose Your Platform

Use this page for shared Helm setup and installation, then apply provider-specific delta steps:

| Platform                       | Use this when                                                                  | Provider guide                                                                                               |
| ------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Amazon EKS                     | The cluster runs in Amazon EKS and uses AWS IAM or IRSA for workload identity. | [Amazon EKS Deployment](https://docs.akeyless.io/docs/gateway-deploy-amazon-eks)                             |
| Azure Kubernetes Service (AKS) | The cluster runs in AKS and uses Microsoft Entra workload identity.            | [Azure Kubernetes Service Deployment](https://docs.akeyless.io/docs/gateway-deploy-azure-kubernetes-service) |
| Google Kubernetes Engine (GKE) | The cluster runs in GKE and uses Google Workload Identity.                     | [Google Kubernetes Engine Deployment](https://docs.akeyless.io/docs/gateway-deploy-google-kubernetes-engine) |

## Prerequisites

- An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) with an [Access Role](https://docs.akeyless.io/docs/rbac) to create and manage [Secrets, Keys](https://docs.akeyless.io/docs/manage-your-secrets-overview), and [Targets](https://docs.akeyless.io/docs/targets)

- [Helm](https://helm.sh/) Installed

- Kubernetes installed with the [Kubernetes Metrics Server](https://github.com/kubernetes-sigs/metrics-server)

- Minimum 1 vCPU available with 2 GB RAM

- For **Argo CD–based** deployments, verify that your configuration meets the required settings as [documented](https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-gateway#argo-cd-instructions).

- Network connection to [Akeyless SaaS Core Services](https://docs.akeyless.io/docs/gateway-network-connectivity) from your cluster.

- Network port `8000` on the cluster must be open **only for internal network access**, allowing access to the following services using the corresponding endpoints:

| Service                                                                      | Endpoint   |
| ---------------------------------------------------------------------------- | ---------- |
| [Gateway Console](https://docs.akeyless.io/docs/configure-gateway)           | `/console` |
| [HashiCorp Vault Proxy](https://docs.akeyless.io/docs/hashicorp-vault-proxy) | `/hvp`     |
| Akeyless V1 REST API                                                         | `/api/v1`  |
| Akeyless V2 REST API                                                         | `/api/v2`  |
| [KMIP Server](https://docs.akeyless.io/docs/kmip-server)                     | `5696`     |

## Helm Chart Configuration

1. Add the following repository to the Helm repository list:

   ```shell
   helm repo add akeyless https://akeylesslabs.github.io/helm-charts
   helm repo update
   ```

2. Fetch the `values.yaml` file from the Akeyless repository:

   ```shell
   helm show values akeyless/akeyless-gateway > values.yaml
   ```

3. Set the relevant parameters in the `values.yaml` file with a text editor or IDE.

## Authentication

Configure the Akeyless Gateway with a default [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) to control the level of access your Gateway instance will have to your Akeyless account.

The following [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) are supported for Kubernetes deployments:

- [API Key](https://docs.akeyless.io/docs/auth-with-api-key)

- [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws)

- [Azure Active Directory](https://docs.akeyless.io/docs/auth-with-azure)

- [Certificates](https://docs.akeyless.io/docs/auth-with-certificate)

- [GCP](https://docs.akeyless.io/docs/auth-with-gcp)

- [Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity)

### API Key Authentication

The API Key Authentication Method requires a dedicated [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) to store the corresponding `Access Key` where the key name of the secret has to be `gateway-access-key`.

#### Create the Secret

Run the following command to create a new Kubernetes Secret to store the Access Key:

```shell
kubectl create secret generic access-key \
  --from-literal=gateway-access-key=<plaintext-Access-Key>
```

Alternatively, use YAML to define the Kubernetes Secret with a Base64-encoded version of your Access Key:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: access-key
  namespace: akeyless # Change this to your actual namespace
type: Opaque
data:
  gateway-access-key: <Base64-encoded value>
```

#### Provide the Secret to the Gateway Config

Once the secret is created, set the relevant Access ID as your `gatewayAccessId` and add the name of the Kubernetes Secret that was created as the `gatewayCredentialsExistingSecret`:

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID>
    gatewayAccessType: access_key
    gatewayCredentialsExistingSecret: access-key
```

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#installation) instructions.

### CSP IAM Authentication

While running your Kubernetes cluster inside your cloud environment, you can use [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws), [GCP](https://docs.akeyless.io/docs/auth-with-gcp), or [Azure Active Directory](https://docs.akeyless.io/docs/auth-with-azure), using machine-to-machine authentication between Akeyless and your Cloud Service Provider with a list of [admin users](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#gateway-admins) who can manage your Gateway.

Set the `gatewayAccessId` with your IAM [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) `Access ID`, where you can define a list of users who can manage your Gateway settings by way of the `allowedAccessPermissions` setting with any other `Access ID` of your [SAML](https://docs.akeyless.io/docs/auth-with-saml), [OIDC](https://docs.akeyless.io/docs/auth-with-oidc), or an [API Key](https://docs.akeyless.io/docs/auth-with-api-key), as described [here](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#access-permissions).

### AWS IAM

AWS IAM can be used in the following approaches:

- Instance IAM Role

- Service Account IAM Role

In both cases, provide your [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws) Authentication Method's Access ID as your `gatewayAccessId`, and at least one other Access ID in the `allowedAccessPermissions` section to provide human users access to [manage your Gateway](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm):

`allowedAccessPermissions` also supports wildcard access IDs with `access_id: "*"`. For details, see [Authentication and Access](https://docs.akeyless.io/docs/gateway-authentication-and-access).

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID>
    gatewayAccessType: aws_iam
  allowedAccessPermissions: {}
```

When working from an AWS instance with an IAM Role associated with it (which is the default state for EKS clusters that leverage the IAM Role of their Node group), nothing else is required, as the Gateway will be leveraging the IAM Role of the AWS instance itself where Kubernetes is running.

Alternatively, you can also leverage an IAM Role assumed by a Kubernetes ServiceAccount in your Cluster. For that, you must either [create an IAM Role bound to a Kubernetes ServiceAccount](https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html), or use an existing IAM role for annotating the Service Account in the Gateway's `values.yaml` Helm chart:
Set the `serviceAccountName` with the desired Kubernetes ServiceAccount name, and set its `eks.amazonaws.com/role-arn` annotation to the ARN of the IAM Role in question (which is constructed using the following format: `arn:aws:iam::<AWS-Account-ID>:role/<IAM-Role-Name>`).

You can also create a new Service Account by simply setting the `create` field to `true`, so the `serviceAccountName` you defined will be created upon deployment. Furthermore, if the `serviceAccountName` is left empty, by default - the chart will create a new Service Account called `<release name>-akeyless-gateway`.
Make sure to set the required role-arn `annotation` to connect your IAM Role with the Service Account in **any** of the scenarios.

```yaml values.yaml
deployment:
  annotations: {}
  labels: {}
  
serviceAccount:
  create: true
  serviceAccountName: <EKS SA name>
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::<AWS Account ID>:role/<IAM Role Name>
```

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#installation) instructions.

### GCP

Google Kubernetes Engine (GKE) can run Akeyless Gateway in its secured and managed Kubernetes Service in standard or autopilot mode.

Deploying Akeyless Gateway by way of the Helm chart using the authentication between your Gateway and Akeyless SaaS using our [GCP Authentication method](https://docs.akeyless.io/docs/auth-with-gcp) can be done using the GCP Workload Identity mechanism.

Workload Identity allows workloads in your GKE clusters to impersonate Identity and Access Management (IAM) Service Accounts to access Google Cloud services. Workload Identity is enabled by default on Autopilot clusters.

Follow the [GKE workload identities guide](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#authenticating_to) to enable GKE workload identities on your cluster.

Create a Kubernetes ServiceAccount for Akeyless Gateway to use. You can also use the default Kubernetes ServiceAccount in the default or any existing Namespace.

Use the existing IAM service account that is bound to your [GCP](https://docs.akeyless.io/docs/auth-with-gcp) Auth Method.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  When authenticating from a pod inside a Google Kubernetes Engine (GKE) cluster using GKE Workload Identity enabled, any `bounded rules` other than `Bound Service Accounts` will not apply. GKE Workload Identity conceals metadata information about the running instance.

  To work with the GKE Workload Identity you must configure **only** the `Bound Service Accounts` field in your [GCP Auth Method](https://docs.akeyless.io/docs/auth-with-gcp).
</Callout>

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

And set your [GCP](https://docs.akeyless.io/docs/auth-with-gcp) `Access ID` as your `gatewayAccessId` and at least one another `Access ID` in the `allowedAccessPermissions` section, to provide human users access to [manage your Gateway](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#gateway-admins):

```yaml Deployment
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID>
    gatewayAccessType: gcp
  allowedAccessPermissions: {}

deployment:
  annotations: {}
  labels: {}

serviceAccount:
  create: false
  serviceAccountName: <GKE SA Name>
  annotations:
    iam.gke.io/gcp-service-account: <GCP SA Name>

nodeSelector:
  iam.gke.io/gke-metadata-server-enabled: "true"
```

<Callout icon="ℹ️" theme="info">
  ### **Info:**

  **NodeSelector** - For Autopilot clusters, omit the `nodeSelector` field. Autopilot rejects this `nodeSelector` because all nodes use Workload Identity.
</Callout>

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#installation) instructions.

### Azure Active Directory

Azure AD authentication is provided to AKS clusters with OpenID Connect. OpenID Connect is an identity layer built on top of the OAuth 2.0 protocol. Akeyless treats Azure as a trusted third party and verifies entities based on a JWT signed by the Azure Active Directory for the configured tenant.

To use [Azure workload identity](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster) for your Gateway deployment, add the following label: `azure.workload.identity/use: "true"`, set the AKS Service Account name and the Azure Client ID using the annotation `azure.workload.identity/client-id`, and set your [Azure Active Directory](https://docs.akeyless.io/docs/auth-with-azure) `Access ID` as your `gatewayAccessId` and at least one another `Access ID` in the `allowedAccessPermissions` section, to provide human users access to [manage your Gateway](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#gateway-admins):

```yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID>
    gatewayAccessType: azure_ad
  allowedAccessPermissions: {}

deployment:
  annotations: {}
  labels:
    azure.workload.identity/use: "true"

serviceAccount:
  create: false
  serviceAccountName: <AKS SA Name>
  annotations:
    azure.workload.identity/client-id: <user assigned client id>
```

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#installation) instructions.

### Universal Identity

Akeyless support [Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity) authentication method for on-premise Kubernetes cluster environments, eliminating the secret zero problems within your config files.

Universal Identity Authentication Method requires a dedicated [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) to store the `UID-Token` where the key of the secret has to be `gateway-uid-token`.

Run the following command to store the Kubernetes Secret that stores the `UID-Token`:

```shell
kubectl create secret generic uid-token \
  --from-literal=gateway-uid-token=<raw-UID-Token>
```

With `--from-literal`, provide the UID token as a raw value. Do not pre-Base64-encode the token.

Set your [Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity) `Access ID` as your `gatewayAccessId` and at least one another `Access ID` in the `allowedAccessPermissions` section, to provide human users access to [manage your Gateway](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#gateway-admins), and set the **Kubernetes Secret** name under `gatewayCredentialsExistingSecret`. Set the rotation interval and choose either to generate a child token for your pods using `uidCreateChildTokenPerPod` field.

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID>
    gatewayAccessType: uid
    gatewayCredentialsExistingSecret: uid-token
    
    universalIdentity:
      # interval im minutes, if empty the token will be rotated in token-ttl/3 max=10 
      uidRotationInterval: "5m" 
      uidCreateChildTokenPerPod: "disable"
      
  allowedAccessPermissions: {}
```

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#installation) instructions.

### Certificates

[Certificate](https://docs.akeyless.io/docs/auth-with-certificate) Authentication Method requires a dedicated [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) to store the `certificate.pem` and the corresponding `private_key.pem` files, where the key of the secret has to be `gateway-certificate` for the `certificate` and `gateway-certificate-key` for the `private_key`:

```shell
kubectl create secret generic certificate-auth \
  --from-literal=gateway-certificate=<base64-encoded-certificate> \
  --from-literal=gateway-certificate-key=<base64-encoded-private_key>
```

Set your [Certificate](https://docs.akeyless.io/docs/auth-with-certificate) `Access ID` as your `gatewayAccessId`, and at least one other `Access ID` defined the `allowedAccessPermissions` to provide human users access to [manage your Gateway](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#access-permissions):

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID>
    gatewayAccessType: certificate
    gatewayCredentialsExistingSecret: certificate-auth
  allowedAccessPermissions: {}
```

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment#installation) instructions.

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

In our example, `test01@testhost.com` and `test02@testhost` will be authorized, and any member of `group=Devops` will also be authorized.

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

Alternatively, you can use a Kubernetes Secret to delegate user permissions over the gateway.

First, define the access permissions as a JSON structure:

```shell
[
  {
    "name": "Administrators",
    "access_id": <Access_ID>,
    "sub_claims": {
      "email": ["test01@testhost.com"],
      "group": ["DevOps"]
    },
    "permissions": ["admin"]
  }
]

```

Then, encode the JSON structure in Base64 and create a Kubernetes Secret:

```shell
kubectl create secret generic allowed-permissions \
  --from-literal=allowed-access-permissions=<base64-encoded-json>
```

Set the name of the secret `allowed-permissions` under `allowedAccessPermissionsExistingSecret` where the key has to be `allowed-access-permissions`.

For the complete and current list, see [Gateway Access Permissions Reference](https://docs.akeyless.io/docs/gateway-access-permissions-reference).

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  Only Gateway **Admins** can delegate permissions to additional users. Any pre-provisioned settings will not be editable from the Akeyless Console.
</Callout>

You may also edit this parameter on your console, by going to the Gateways tab and selecting the desired Gateway. On the right of the screen, you will see the Gateway details, including **Access Permissions**.

### CBA

To work with CBA flow for your Gateway-allowed users, In addition to the list of `allowedAccessPermissions` you provided, set your chart with the `enableSniProxy: true` setting under the `TLSConf` section as follow:

```yaml
TLSConf:
  enableSniProxy: true
```

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  All changes to allowed access IDs, such as editing, removing, and so on, can only be performed on **post-deployment allowed access IDs**. If an ID was defined during deployment it can't be removed or changed.
</Callout>

## Installation

1. To deploy the Gateway using the edited `values.yaml` file, run the following command:

   ```shell
   helm install gw akeyless/akeyless-gateway -f values.yaml
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

<Callout icon="❗" theme="error">
  ### **Important:**

  Unified Gateway chart upgrades use the `gw` image by default.
  If an existing deployment requires `akeyless/base`, set an explicit override in your `values.yaml` before running `helm upgrade`:

  ```yaml values.yaml
  gateway:
    deployment:
      image:
        repository: akeyless/base
        tag: latest # use latest-akeyless for non-root
  ```
</Callout>

To upgrade your Gateway, when working with a specific version, first edit the version in your `values.yaml` file for example:

```yaml
 version: x.y.z 
```

Update the Helm repo and upgrade the Helm deployment.

```shell
helm repo update
helm upgrade gw akeyless/akeyless-gateway -f values.yaml
```

Check that the new pods are starting.

## Tutorial

Check out our tutorial video on [Installing and Configuring the Gateway on Kubernetes](https://tutorials.akeyless.io/docs/installing-and-configuring-akeyless-gateway).
