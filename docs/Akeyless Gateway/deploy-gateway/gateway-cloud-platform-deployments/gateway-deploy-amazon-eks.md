---
title: Amazon EKS Deployment
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
      slug: advanced-k8s-gateway-configuration
      title: Advanced Kubernetes Configuration
    - type: basic
      slug: configuring-tls
      title: Configuring TLS
---
This page includes only Amazon EKS-specific delta steps.

Review the [Kubernetes Helm deployment page](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm) first, then apply the EKS changes in this guide.

For AWS partition guidance and deployment pattern coverage, see [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws#aws-deployment-pattern-support).

## Scope

This guide assumes that the baseline Helm deployment flow is complete, including:

* Helm chart setup
* base `values.yaml` preparation
* installation and upgrade flow
* Gateway admin and permission model

This page focuses on EKS identity integration and EKS-specific `values.yaml` changes.

## Prerequisites

Complete all baseline prerequisites from the main Helm deployment page, and add:

* An [AWS IAM authentication method](https://docs.akeyless.io/docs/auth-with-aws) in Akeyless.
* An EKS IAM role strategy:
    * Node IAM role, or
    * IAM Roles for Service Accounts (IRSA).
* If using IRSA, a role bound to the target Kubernetes ServiceAccount as documented in the [EKS IRSA guide](https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html).

## EKS Identity Delta

Set the Gateway auth type to `aws_iam` and provide your AWS IAM Access ID:

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <AWS IAM Access ID>
    gatewayAccessType: aws_iam
  allowedAccessPermissions: {}
```

For IRSA, set ServiceAccount annotations with the IAM role ARN:

```yaml values.yaml
deployment:
  annotations: {}
  labels: {}

serviceAccount:
    create: true
    serviceAccountName: <EKS ServiceAccount Name>
    annotations:
      eks.amazonaws.com/role-arn: arn:aws:iam::<AWS Account ID>:role/<IAM Role Name>
```

## Validation Delta

After deployment, validate that the Gateway pod uses AWS identity successfully:

1. Confirm the pod is running:

    ```shell
    kubectl get pods -n <namespace>
    ```

2. If using IRSA, verify the ServiceAccount annotation:

    ```shell
    kubectl get sa <EKS ServiceAccount Name> -n <namespace> -o yaml
    ```

3. Validate Gateway connectivity and login through the management endpoint after install.

## Related Tasks

* For shared Helm install and upgrade commands, use the main Kubernetes Helm deployment page.
* For advanced chart settings, use [Advanced Kubernetes Configuration](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference).
* For TLS configuration, use [Configuring TLS](https://docs.akeyless.io/docs/gateway-tls-settings).
