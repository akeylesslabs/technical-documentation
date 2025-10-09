---
title: Secure Remote Access Bastion
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: secure-remote-access-advance
      title: SRA Advanced Configuration
---
The Akeyless Secure Remote Access Bastion provides secure remote access to resources using Just In Time credentials (dynamic secrets, rotated secrets, and SSH certificates).

This chart bootstraps the Secure Remote Access Bastion deployment on a Kubernetes cluster using the Helm package manager.

# Prerequisites

* Helm Installed

* Kubernetes Installed

* [SSH Certificate Issuer](https://docs.akeyless.io/docs/how-to-configure-ssh) for CLI Access.

* Minimum 1 vCPU available with 2 GB RAM per resource. This can be explicitly specified inside the chart for the Zero Trust bastion- `ztbConfig` section and the SSH bastion under `sshConfig`.

* Optional: If Horizontal Pod Autoscaler (HPA) usage is desired, you must set requests values.

_**Network**_

* Ingress - Make sure to use sticky session annotation, for example, nginx.ingress.kubernetes.io/affinity: "cookie" in Nginx

* Cloud Provider Load Balancer - Make sure to config the Load Balancer to support sticky sessions, for example, in AWS, using ELB: [https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html)

When using SSH sessions behind a load balancer such as ELB, the session can be closed due to an idle connection timeout, so we recommend increasing it to a reasonably high value or even unlimited.

e.g., when running on AWS with ELB: [https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs\_elb\_console](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console)

_**Storage**_

To be able to make more than 1 SSH-bastion pod work, the chart requires a persistent storage, with the `ReadWriteMany` access mode.

Since a storage class is more environment-specific, you will need to provide one before proceeding. In addition, please provide a **PersistentVolumes** with <code>persistentVolumeReclaimPolicy: retain</code> and reference those PVs in the chart `values` file

```yaml
persistence: 
  shareStorageVolume:
    name: share-storage
    storageClassName: "efs-sc"
    accessModes:
      - ReadWriteMany
    persistentVolumeReclaimPolicy: Retain
    annotations: {}
    mountOptions:
      - dir_mode=0650
      - file_mode=0650
    size: 2Gi
```

e.g., when running on AWS with EKS: [https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html](https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html)

_**Horizontal Auto-Scaling**_

Horizontal auto-scaling is based on the HorizontalPodAutoscaler object.
For it to work correctly, the Kubernetes metrics server must be installed in the cluster - [https://github.com/kubernetes-sigs/metrics-server](https://github.com/kubernetes-sigs/metrics-server), as well as the above Storage PV must be defined for the `sshConfig` Statefulset (HPA can not support multiple pods without defining a shared persistent storage volume).

> 🚧 Warning
>
> To enable Secure Remote Access features you will have to get an access key to Akeyless private repository. Please contact your Account Manager for more details.

# Installing the Chart

Add Akeyless helm charts repository to your Helm repository list:

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
```

The values.yaml file holds default values. Copy the file from:

[https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-secure-remote-access](https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-secure-remote-access)

Or run the following helm command to generate the values file locally:

```shell
helm show values akeyless/akeyless-sra > values.yaml
```

# Configuration

To connect to Akeyless private repository, set the `dockerRepositoryCreds` field to access the Akeyless internal image and the relevant `apiGatewayURL` to point your Gateway REST API port `8080`.

```yaml
############
## Global ##
############
dockerRepositoryCreds:
apiGatewayURL: https://rest.akeyless.io
```

The Secure Remote Access Bastion should be set with a **privileged** `AccessID` with **Read**, **List** and **Update** permissions, to fetch the relevant secret on behalf of your users, set the `privilegedAccess` field with the relevant `AccessID` as described in the Authentication section of this page.

> 📘 Update permissions
>
> The requirement for "update" permissions is to allow SRA to display information about sessions.

Users can have only `list` permissions on their secrets. Upon successful authentication against your IDP, the bastion will fetch the requested secret from Akeyless and will inject them directly for your users transparently.

To control which users will be allowed to request access from the Akeyless Bastion, set the `allowedAccessIDs` field with a list of `AccessIDs` that will be authorized to request access.

```yaml
privilegedAccess:
  accessID: "<Access ID>"
  allowedAccessIDs: []
```

To provide just-in-time native CLI access for your users using [Keyless SSH](https://docs.akeyless.io/docs/how-to-configure-ssh) set the `CAPublicKey` field with the matching public key of the key you used to create the [SSH Certificate Issuer](https://docs.akeyless.io/docs/how-to-configure-ssh).

```yaml
#############################################
## Default values for akeyless-ssh-bastion ##
#############################################
sshConfig:
# Enable akeyless-ssh-bastion. Valid values: true/false.
  enabled: true
  config:
    CAPublicKey: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCu8RWf5bFDlLhPljsYEKFQAt6cFLdAVOy..."
```

> 📘 Info
>
> If you don't have an SSH certificate ready, please follow this guide on creating [SSH Cert issuer](https://docs.akeyless.io/docs/how-to-configure-ssh) with Akeyless Platform and set your CA Public key in the chart `values`.
>
> You will also need to enable Secure Remote Access on the SSH Cert Issuer.

## Authentication

The following [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) are supported:

* [API Key](https://docs.akeyless.io/docs/api-key)

* [AWS IAM](https://docs.akeyless.io/docs/aws-iam)

* [GCP GCE](https://docs.akeyless.io/docs/gcp-auth-method)

* [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad)

## API Key Authentication

To set your Bastion default authentication based on [API Key](https://docs.akeyless.io/docs/api-key), set the `accessID` and the matching `accessKey`  with a list of `allowedAccessIDs` that will be authorized to request access:

```yaml values.yaml
privilegedAccess:
  accessID: "<API Key Access ID>"
  accessKey: "<Access Key>"
  allowedAccessIDs: 
    - p-xxxxxxx
```

## CSP IAM Authentication

While running your K8s cluster inside your cloud environment, you can use [AWS IAM](https://docs.akeyless.io/docs/aws-iam), [GCP](https://docs.akeyless.io/docs/gcp-auth-method), or [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad), using machine-to-machine authentication between Akeyless and your Cloud Service Provider with a list of allowed `AccessIDs` that will be authorized to request access.

## AWS IAM

AWS IAM can be used in the following approaches:

* Instance IAM Role

* Service Account IAM Role

While working with an IAM Role associated with the instance itself, you can simply provide your [AWS IAM](https://docs.akeyless.io/docs/aws-iam) `Access ID`  as your <code>accessID</code>, with a list of `allowedAccessIDs` that will be authorized to request access:

```yaml values.yaml
privilegedAccess:
  accessID: "<AWS IAM Access ID>"
  allowedAccessIDs: 
    - p-xxxxxxx
```

When working from an AWS instance with an IAM Role associated with it (which is the default state for EKS clusters that leverage the IAM Role of their Node group), nothing else is required - as the Bastion will be leveraging the IAM Role of the AWS instance itself where K8s is running.

Alternatively, you can leverage an IAM Role assumed by a K8s Service Account in your Cluster. For that, you must either [create an IAM Role bound to a K8s Service Account](https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html), or use an existing IAM role for annotating the Service Account in the Bastion's `values.yaml` helm-chart:

Set the `serviceAccountName` with the desired Kubernetes Service Account name, and set its `eks.amazonaws.com/role-arn` annotation to the ARN of the IAM Role in question (which is constructed using the following format: `arn:aws:iam::<AWS-Account-ID>:role/<IAM-Role-Name>`).

You can also create a new Service Account by simply setting the `create` field to `true`, so the `serviceAccountName` you defined will be created upon deployment. Furthermore, if the `serviceAccountName` is left empty, by default - the chart will create a new Service Account called `<release name>-akeyless-sra`.
Make sure to set the required role-arn `annotation` to connect your IAM Role with the Service Account in **any** of the scenarios.

```yaml values.yaml
privilegedAccess:
  accessID: "<AWS IAM Access ID>"
  allowedAccessIDs: 
    - p-xxxxxxx    
  serviceAccount:
    create: false
    serviceAccountName: <EKS SA name>
    annotations:
        eks.amazonaws.com/role-arn: arn:aws:iam::<AWS Account ID>:role/<IAM Role Name>
```

## GCP GCE

Google Kubernetes Engine (GKE) can run Akeyless Bastion in its secured and managed Kubernetes service in standard or autopilot mode.

Deploying Akeyless Bastion via the Helm chart using the authentication between your Bastion and Akeyless SaaS using our [GCP Authentication method](https://docs.akeyless.io/docs/gcp-auth-method) can be done using the GCP Workload Identity mechanism.

Workload Identity allows workloads in your GKE clusters to impersonate Identity and Access Management (IAM) Service Accounts to access Google Cloud services. Workload Identity is enabled by default on Autopilot clusters.

Follow the [GKE workload identities guide](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#authenticating_to) to enable GKE workload identities on your cluster.

Create a Kubernetes service account for Akeyless Bastion to use. You can also use the default Kubernetes service account in the default or any existing namespace.

Use the existing IAM service account as provided in your [GCP GCE](https://docs.akeyless.io/docs/gcp-auth-method) auth method.

> 👍 Note
>
> When authenticating from a pod inside a Google Kubernetes Engine (GKE) cluster using GKE Workload Identity enabled, any `bounded rules` other than `Bound Service Accounts` will not apply. GKE Workload Identity conceals metadata information about the running instance.
>
> To work with the GKE Workload Identity with `bounded rules`, please configure **only** the `Bound Service Accounts`  field in your [GCP Auth Method](https://docs.akeyless.io/docs/gcp-auth-method).

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

And set your [GCP GCE](https://docs.akeyless.io/docs/gcp-auth-method) `Access ID`  as your `adminAccessId` and at least one another `Access ID` in the `allowedAccessIDs` list.

```yaml values.yaml
privilegedAccess:
  accessID: "<GCP GCE Access ID>"
  allowedAccessIDs: 
    - p-xxxxxxx    
  serviceAccount:
    create: false
    serviceAccountName: "<GKE SA Name>"
   annotations:
        iam.gke.io/gcp-service-account: "<GCP SA Name>"
  nodeSelector:
         iam.gke.io/gke-metadata-server-enabled: "true"     
  gcpAudience: "akeyless.io"
```

## Azure Active Directory

Azure AD authentication is provided to AKS clusters with OpenID Connect. OpenID Connect is an identity layer built on top of the OAuth 2.0 protocol. Akeyless treats Azure as a trusted third party and verifies entities based on a JWT signed by the Azure Active Directory for the configured tenant.

Set your [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad) `Access ID` as your <code>accessID</code> with the matching service principal `azureobjectID`, with a list of `allowedAccessIDs` that will be authorized to request access:

```yaml values.yaml
privilegedAccess:
  accessID: "Azure AD Access ID"
  azureObjectID: ""
  allowedAccessIDs: 
    - p-xxxxxxx
```

# Install

```shell
helm install <RELEASE NAME> akeyless/akeyless-sra -f values.yaml
```

Verify that both **ssh-sra-akeyless** and **web-sra-akeyless** pods are up and running.

> 👍 Note
>
> Akeyless supports session termination, which can be configured as part of this chart deployment.
> To enable session termination, please set your Gateway URL or your Okta\Keycloak  `apiURL` and `apiToken` under `sessionTermination` section.

# Upgrade SRA Bastion

To upgrade your SRA Bastion, run the following:

```shell
helm repo update  
helm upgrade <RELEASE NAME> akeyless/akeyless-sra -f values.yaml
```

Check that the new pods are starting.

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/install-and-configure-remote-access-bastion" target="_blank">Install and Configure Remote Access Bastion</a>.
