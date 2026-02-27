---
title: EKS Unified Gateway Quickstart
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
This quickstart deploys the Akeyless Unified Gateway on Amazon Elastic Kubernetes Service (Amazon EKS), with ingress handled by AWS Application Load Balancer (ALB) and TLS handled by AWS Certificate Manager (ACM).

## Prerequisites

* Amazon EKS cluster with `kubectl` access.
* Helm 3 installed.
* AWS CLI configured with permissions for IAM, ACM, and EKS resources.
* AWS Load Balancer Controller installed on the cluster.
* Akeyless Authentication Method configured for AWS IAM.

## Step 1: Add the Akeyless Helm Repository

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
helm show values akeyless/akeyless-gateway > values.yaml
```

## Step 2: Configure Gateway Identity (IRSA)

Use IAM Roles for Service Accounts (IRSA) by annotating the Gateway Kubernetes ServiceAccount:

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessType: aws_iam
    gatewayAccessId: <aws-iam-auth-method-access-id>
  allowedAccessPermissions:
    - name: Administrators
      access_id: <admin-access-id>
      permissions:
        - admin

serviceAccount:
  create: true
  serviceAccountName: akeyless-gateway-sa
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::<aws-account-id>:role/<gateway-role-name>
```

## Step 3: Configure Ingress for ALB and ACM

```yaml values.yaml
ingress:
  enabled: true
  annotations:
    kubernetes.io/ingress.class: "alb"
    alb.ingress.kubernetes.io/scheme: "internet-facing"
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:<region>:<account-id>:certificate/<certificate-id>
  rules:
    - hostname: "gateway.yourdomain.com"
      servicePort: gateway
      path: "/*"
      pathType: ImplementationSpecific
  tls: true
```

## Step 4: Install the Gateway

```shell
helm install gateway akeyless/akeyless-gateway -f values.yaml -n akeyless
```

## Step 5: Configure DNS

Point `gateway.yourdomain.com` to the ALB DNS name created by the ingress resource.

```shell
kubectl get ingress -n akeyless
```

## Step 6: Validate Deployment

```shell
curl -vk https://gateway.yourdomain.com/console
```

Expected result: the Gateway login page or a valid response from the Gateway endpoint.

## Related Reference Pages

* [Gateway on Kubernetes](https://docs.akeyless.io/docs/gateway-chart)
* [Advanced Chart Configuration](https://docs.akeyless.io/docs/advanced-chart-configuration)
* [Gateway Configuration Manager](https://docs.akeyless.io/docs/gateway-configuration-manager)
