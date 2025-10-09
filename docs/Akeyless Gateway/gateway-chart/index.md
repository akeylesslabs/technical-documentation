---
title: Gateway on Kubernetes
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Akeyless provides a [Helm chart](https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-gateway)  to bootstrap the Akeyless Gateway deployment.

> 📘 New Chart
>
> This guide describe the flow using the **latest** chart of the Akeyless Gateway.
>
> The documentation for the legacy charts is available [here](https://docs.akeyless.io/docs/gateway-k8s)

# Prerequisites

* An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) with an [Access Role](https://docs.akeyless.io/docs/rbac) to create and manage [Secrets, Keys,](https://docs.akeyless.io/docs/manage-your-secrets-overview) and [Targets](https://docs.akeyless.io/docs/targets)

* [Helm](https://helm.sh/) Installed

* Kubernetes installed with the [Kubernetes metrics server](https://github.com/kubernetes-sigs/metrics-server)

* Minimum 1 vCPU available with 2 GB RAM

* Network connection to [Akeyless SaaS Core Services](https://docs.akeyless.io/docs/api-gateway-network-connectivity) from your cluster.

* Network port `8000` on the cluster must be open **only for internal network access**, allowing access to the following services using the corresponding endpoints:

| Service                                              | Endpoint   |
| :--------------------------------------------------- | :--------- |
| [Gateway Console](https://docs.akeyless.io/docs/gateway-configuration-manager) | `/console` |
| [HashiCorp Vault Proxy](https://docs.akeyless.io/docs/hashicorp-vault-proxy)   | `/hvp`     |
| Akeyless V1 REST API                                 | `/api/v1`  |
| Akeyless V2 REST API                                 | `/api/v2`  |
| [KMIP Server](https://docs.akeyless.io/docs/kmip-server)                       | `5696`     |

# Helm Chart configuration

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

# Authentication

Configure the Akeyless Gateway with a default [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) to control the level of access your Gateway instance will have to your Akeyless account.

The following [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) are supported for Kubernetes deployments:

* [API Key](https://docs.akeyless.io/docs/api-key)

* [AWS IAM](https://docs.akeyless.io/docs/aws-iam)

* [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad)

* [Certificates](https://docs.akeyless.io/docs/certificate-based-authentication)

* [GCP](https://docs.akeyless.io/docs/gcp-auth-method)

* [Universal Identity](https://docs.akeyless.io/docs/universal-identity)

## API Key Authentication

The API Key Authentication Method requires a dedicated [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) to store the corresponding `Access Key` where the key name of the secret has to be `gateway-access-key`.

### Create the Secret

Run the following command to create a new Kubernetes secret to store the Access Key:

```shell
kubectl create secret generic access-key \
  --from-literal=gateway-access-key=<plaintext-Access-Key>
```

Alternatively, use YAML to define the Kubernetes Secret with a Base64 encoded version of your Access Key:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: access-key
  namespace: akeyless  # Change this to your actual namespace
type: Opaque
data:
  gateway-access-key: <Base64 encoded value>
```

### Provide the Secret to the Gateway Conf

Once the secret is created, set the relevant Access ID as your `gatewayAccessId` and add the name of the Kubernetes Secret that was created as the `gatewayCredentialsExistingSecret`:

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID>
    gatewayAccessType: access_key
    gatewayCredentialsExistingSecret: access-key
```

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-k8s#installation) instructions.

## CSP IAM Authentication

While running your Kubernetes cluster inside your cloud environment, you can use [AWS IAM](https://docs.akeyless.io/docs/aws-iam), [GCP](https://docs.akeyless.io/docs/gcp-auth-method), or [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad), using machine-to-machine authentication between Akeyless and your Cloud Service Provider with a list of [admin users](https://docs.akeyless.io/docs/gateway-k8s#gateway-admins) that will be able to manage your Gateway.

Set the `gatewayAccessId` with your IAM [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) `Access ID`, where you can define a list of users that will be able to manage your Gateway settings via the  `allowedAccessPermissions` setting with any other `Access ID` of your  [SAML](https://docs.akeyless.io/docs/saml) ,[OIDC](https://docs.akeyless.io/docs/openid) or an [API Key](https://docs.akeyless.io/docs/api-key) as described [here](https://docs.akeyless.io/docs/gateway-k8s#access-permissions).

## AWS IAM

AWS IAM can be used in the following approaches:

* Instance IAM Role

* Service Account IAM Role

In both cases, provide your [AWS IAM](https://docs.akeyless.io/docs/aws-iam) Authentication Method's Access ID as your `gatewayAccessId`, and at least one other Access ID in the `allowedAccessPermissions` section  to provide human users access to [manage your Gateway](https://docs.akeyless.io/docs/gateway-on-k8s-copy-1#access-permissions):

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID>
    gatewayAccessType: aws_iam
  allowedAccessPermissions: {}
```

When working from an AWS instance with an IAM Role associated with it (which is the default state for EKS clusters that leverage the IAM Role of their Node group), nothing else is required, as the Gateway will be leveraging the IAM Role of the AWS instance itself where K8s is running.

Alternatively, you can also leverage an IAM Role assumed by a K8s Service Account in your Cluster. For that, you must either [create an IAM Role bound to a K8s Service Account](https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html), or use an existing IAM role for annotating the Service Account in the Gateway's `values.yaml` helm-chart:
Set the `serviceAccountName` with the desired Kubernetes Service Account name, and set its `eks.amazonaws.com/role-arn` annotation to the ARN of the IAM Role in question (which is constructed using the following format: `arn:aws:iam::<AWS-Account-ID>:role/<IAM-Role-Name>`).

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

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-k8s#installation) instructions.

## GCP

Google Kubernetes Engine (GKE) can run Akeyless Gateway in its secured and managed Kubernetes service in standard or autopilot mode.

Deploying Akeyless Gateway via the Helm chart using the authentication between your Gateway and Akeyless SaaS using our [GCP Authentication method](https://docs.akeyless.io/docs/gcp-auth-method) can be done using the GCP Workload Identity mechanism.

Workload Identity allows workloads in your GKE clusters to impersonate Identity and Access Management (IAM) Service Accounts to access Google Cloud services. Workload Identity is enabled by default on Autopilot clusters.

Follow the [GKE workload identities guide](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#authenticating_to) to enable GKE workload identities on your cluster.

Create a Kubernetes service account for Akeyless Gateway to use. You can also use the default Kubernetes service account in the default or any existing namespace.

Use the existing IAM service account that is bound to your [GCP](https://docs.akeyless.io/docs/gcp-auth-method) auth method.

> 👍 Note
>
> When authenticating from a pod inside a Google Kubernetes Engine (GKE) cluster using GKE Workload Identity enabled, any `bounded rules` other than `Bound Service Accounts` will not apply. GKE Workload Identity conceals metadata information about the running instance.
>
> To work with the GKE Workload Identity you must configure **only** the `Bound Service Accounts`  field in your [GCP Auth Method](https://docs.akeyless.io/docs/gcp-auth-method).

Allow the Kubernetes service account to impersonate the IAM service account by adding an IAM policy binding between the two service accounts. This binding allows the Kubernetes service account to act as the IAM service account.

Replace the following:
`PROJECT_ID`: your Google Cloud project ID.
`GSA_NAME `: the name of your IAM service account.
`GSA_PROJECT`: the project ID of the Google Cloud project of your IAM service account.
`KSA_NAME`: the name of your new Kubernetes service account.
`NAMESPACE`: the name of the Kubernetes namespace for the service account.

```shell GKE
gcloud iam service-accounts add-iam-policy-binding GSA_NAME@GSA_PROJECT.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:PROJECT_ID.svc.id.goog[NAMESPACE/KSA_NAME]"
```

Annotate the Kubernetes service account with the email address of the IAM service account.

```shell GKE
kubectl annotate serviceaccount KSA_NAME \
    --namespace NAMESPACE \
    iam.gke.io/gcp-service-account=GSA_NAME@GSA_PROJECT.iam.gserviceaccount.com
```

Set the relevant K8s `serviceAccountName` or leave it empty to use the `default` K8s Service Account, update the `annotations`, and enable the `nodeSelector` to schedule the workloads on nodes that use Workload Identity and to use the annotated Kubernetes service account.

And set your [GCP](https://docs.akeyless.io/docs/gcp-auth-method) `Access ID`  as your `gatewayAccessId` and at least one another `Access ID` in the `allowedAccessPermissions` section, to provide human users access to [manage your Gateway](https://docs.akeyless.io/docs/gateway-k8s#gateway-admins) :

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

> 📘 Info
>
> **NodeSelector** - For Autopilot clusters, omit the `nodeSelector` field. Autopilot rejects this `nodeSelector` because all nodes use Workload Identity.

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-k8s#installation) instructions.

## Azure Active Directory

Azure AD authentication is provided to AKS clusters with OpenID Connect. OpenID Connect is an identity layer built on top of the OAuth 2.0 protocol. Akeyless treats Azure as a trusted third party and verifies entities based on a JWT signed by the Azure Active Directory for the configured tenant.

To use [Azure workload identity](https://learn.microsoft.com/en-us/azure/aks/learn/tutorial-kubernetes-workload-identity) for your Gateway deployment, add the following label: `azure.workload.identity/use: "true"`, set the AKS Service Account name and the Azure Client ID using the annotation `azure.workload.identity/client-id` , and set your [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad) `Access ID`  as your `gatewayAccessId` and at least one another `Access ID` in the `allowedAccessPermissions` section, to provide human users access to [manage your Gateway](https://docs.akeyless.io/docs/gateway-k8s#gateway-admins):

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

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-k8s#installation) instructions.

## Universal Identity

Akeyless support [Universal Identity](https://docs.akeyless.io/docs/universal-identity) authentication method for on-premise K8s cluster environments, eliminating the secret zero problems within your config files.

Universal Identity Authentication Method requires a dedicated [K8s Secret](https://kubernetes.io/docs/concepts/configuration/secret/) to store the `UID-Token` where the key of the secret has to be `gateway-uid-init-token`.

Run the following command to store the  K8s secret that stores the `UID-Token`:

```shell
kubectl create secret generic uid-token \
  --from-literal=gateway-uid-token=<base64-encoded-UID-Token>
```

Set your [Universal Identity](https://docs.akeyless.io/docs/universal-identity) `Access ID`  as your `gatewayAccessId` and at least one another `Access ID` in the `allowedAccessPermissions` section, to provide human users access to [manage your Gateway](https://docs.akeyless.io/docs/gateway-k8s#gateway-admins), and set the **K8s Secret** name under `gatewayCredentialsExistingSecret`. Set the rotation interval and choose either to generate a child token for your pods using `uidCreateChildTokenPerPod` field.

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID>
    gatewayAccessType: uid
    gatewayCredentialsExistingSecret: uid-token
    
    universalIdentity:
  # interval im minutes, if empty the token will be rotated in token-ttl/3  max=10 
      uidRotationInterval: "5m" 
      uidCreateChildTokenPerPod: "disable"
      
  allowedAccessPermissions: {}
```

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-k8s#installation) instructions.

## Certificates

[Certificate ](https://docs.akeyless.io/docs/certificate-based-authentication) Authentication Method requires a dedicated [K8s Secret](https://kubernetes.io/docs/concepts/configuration/secret/) to store the `certificate.pem` and the corresponding `private_key.pem` files, where the key of the secret has to be `gateway-certificate` for the `certificate` and `gateway-certificate-key` for the `private_key`:

```shell
kubectl create secret generic certificate-auth \
  --from-literal=gateway-certificate=<base64-encoded-certificate> \
  --from-literal=gateway-certificate-key=<base64-encoded-private_key>
```

Set your [Certificate](https://docs.akeyless.io/docs/certificate-based-authentication) `Access ID` as your `gatewayAccessId`, and at least one other `Access ID` defined the `allowedAccessPermissions` to provide human users access to [manage your Gateway](https://docs.akeyless.io/docs/gateway-k8s#access-permissions):

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID>
    gatewayAccessType: certificate
    gatewayCredentialsExistingSecret: certificate-auth
  allowedAccessPermissions: {}
```

Save the file and proceed with the [installation](https://docs.akeyless.io/docs/gateway-k8s#installation) instructions.

# Gateway Admins

To support local management of your Gateway configuration, you can set a list of  `Access ID` that will be able to log in and manage your Gateway. This setting can also work with [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) (when a shared authentication method is used), where for each entry you need to define a unique `name` which should describe the **Access Permission** object, with an `access-id` , `sub_claims` when applicable, and a list of `permissions`.

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

In this case, the above will create an **Access Permission** object named **Administrators**,  associated with an Auth method `p-yyyyyy` which for example is your [SAML](https://docs.akeyless.io/docs/saml) or [OIDC](https://docs.akeyless.io/docs/openid) `Access ID`, where a user that at least matches one [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) attribute, will be authorized to access the Gateway with **Admin** permissions:

In our example, `test01@testhost.com` and `test02@testhost` will be authorized, and any member of `group=Devops` will also be authorized.

In this case, the `Access ID` belongs to the authentication method created for the certain Identity Provider.
**If you don't specify the sub-claims, every user authenticated by this IdP will be able to log in to the Gateway with admin privileges.**

To work with [API Key](https://docs.akeyless.io/docs/api-key) as an `allowedAccessPermissions` simply provide your [API Key](https://docs.akeyless.io/docs/api-key) `Access ID` with a `name` for the **Access Permission** object, with a set of `permissions`.

## Access Permissions

To delegate the exact permissions users will have on your Gateway components you can explicitly grant permissions, for example, to grant permissions to a user to manage only your Gateway [Log Forwarding](https://docs.akeyless.io/docs/log-forwarding) settings:

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

In the above example, your Gateway **Admins** are `test01@testhost.com,test01@testhost.com` or any user which is part of your `Devops` group in your **IdP**, where `test03@testhost.com` have permission to manage **only** your Gateway [Log Forwarding](https://docs.akeyless.io/docs/log-forwarding) settings.

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

Then, encode the JSON structure in Base64 and create a Kubernetes secret:

```shell
kubectl create secret generic allowed-permissions \
  --from-literal=allowed-access-permissions=<base64-encoded-json>
```

Set the name of the secret `allowed-permissions` under `allowedAccessPermissionsExistingSecret` where the key has to be `allowed-access-permissions`.

Full list of available permissions:

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Permission
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `admin`
      </td>

      <td>
        Admin permission can manage all Gateway components, including **Access Permissions**
      </td>
    </tr>

    <tr>
      <td>
        `defaults`
      </td>

      <td>
        Management of the defaults settings of your Gateway
        Including `GatewayUrl`,`TLS`,`Default Encryption Key` & `Default AccessID` for login.
      </td>
    </tr>

    <tr>
      <td>
        `classic_keys`
      </td>

      <td>
        Management of [Classic Keys](https://docs.akeyless.io/docs/classic-keys)
      </td>
    </tr>

    <tr>
      <td>
        `dynamic_secret`
      </td>

      <td>
        Management of [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret)
      </td>
    </tr>

    <tr>
      <td>
        `rotated_secret`
      </td>

      <td>
        Management of [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets)
      </td>
    </tr>

    <tr>
      <td>
        `rotate-secret-value`
      </td>

      <td>
        Permission to only rotate the secret value without editing it.
      </td>
    </tr>

    <tr>
      <td>
        `targets`
      </td>

      <td>
        Management of all Targets items that were created using your Gateway
      </td>
    </tr>

    <tr>
      <td>
        `automatic_migration`
      </td>

      <td>
        Management of  [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) settings
      </td>
    </tr>

    <tr>
      <td>
        `log_forwarding`
      </td>

      <td>
        Management of [Log Forwarding](https://docs.akeyless.io/docs/log-forwarding) settings
      </td>
    </tr>

    <tr>
      <td>
        `zero_knowledge_encryption`
      </td>

      <td>
        Management of [Zero-Knowledge](https://docs.akeyless.io/docs/zero-knowledge)
      </td>
    </tr>

    <tr>
      <td>
        `caching`
      </td>

      <td>
        Management of [Gateway Cache](https://docs.akeyless.io/docs/configure-the-gateway-cache) settings
      </td>
    </tr>

    <tr>
      <td>
        `event_forwarding`
      </td>

      <td>
        Management of [Event](https://docs.akeyless.io/docs/event-center) Forwarding settings
      </td>
    </tr>

    <tr>
      <td>
        `ladp_auth`
      </td>

      <td>
        Management of [LDAP](https://docs.akeyless.io/docs/ldap) Auth Gateway configuration.
      </td>
    </tr>

    <tr>
      <td>
        `k8s_auth`
      </td>

      <td>
        Management of [Kubernetes](https://docs.akeyless.io/docs/kubernetes-auth) Auth Gateway configuration
      </td>
    </tr>

    <tr>
      <td>
        `kmip`
      </td>

      <td>
        Management of [KMIP Servers](https://docs.akeyless.io/docs/kmip-server)
      </td>
    </tr>
  </tbody>
</Table>

> 👍 Note
>
> Only Gateway **Admins** can delegate permissions to additional users. Any pre-provisioned settings will not be editable from the Akeyless Console.

You may also edit this parameter on your console, by going to the Gateways tab and selecting the desired Gateway. On the right of the screen, you will see the Gateway details, including **Access Permissions**.

## CBA

To work with CBA flow for your Gateway-allowed users, In addition to the list of `allowedAccessPermissions` you provided, set your chart with the `enableSniProxy: true` setting under the `TLSConf` section as follow:

```yaml
TLSConf:
  enableSniProxy: true
```

> 👍 Note
>
> All changes to allowed access IDs, such as editing, removing, and so on, can only be performed on **post-deployment allowed access IDs**. If an ID was defined during deployment it can't be removed or changed.

# Installation

1. To install the Gateway using the edited `values.yaml` file, run the following command:

```shell
helm install gw akeyless/akeyless-gateway -f values.yaml
```

2. Check if the pods are up and running:

```shell
kubectl get pod

NAME                                       READY   STATUS    RESTARTS       AGE
gw-akeyless-gateway-6554f7c66c-56fgs   1/1     Running   0   						5s
gw-akeyless-gateway-6554f7c66c-7jt8r   1/1     Running   0              5s
```

3. Log in to the Gateway using your browser (`http://Your-Akeyless-Gateway-URL:8000`)  with your Gateway admin credentials.

# Upgrade Gateway

To upgrade your Gateway, when working with a specific version, first edit the version in your `values.yaml` file for example:

```yaml
 version: x.y.z 
```

Update the helm repo and upgrade the helm deployment.

```shell
helm repo update
helm upgrade gw akeyless/akeyless-gateway -f values.yaml
```

Check that the new pods are starting.
