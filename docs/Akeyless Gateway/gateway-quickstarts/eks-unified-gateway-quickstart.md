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

* [Amazon EKS cluster](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html) with [kubectl access to the cluster](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html).
* [Helm 3 installed.](https://helm.sh/docs/intro/install/)
* [AWS CLI configured with an identity that has permissions for IAM, ACM, and EKS resources.](https://docs.aws.amazon.com/eks/latest/userguide/install-awscli.html)
* [AWS Load Balancer Controller installed on the cluster.](https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html)
* [Akeyless Authentication Method configured for AWS IAM.](https://docs.akeyless.io/docs/auth-with-aws)

## Step 1: Add the Akeyless Helm Repository

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
helm show values akeyless/akeyless-gateway > values.yaml
```

## Step 2: Configure Gateway Identity (IRSA)

Use IAM Roles for Service Accounts (IRSA) by annotating the Gateway Kubernetes ServiceAccount in `values.yaml`:

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
gateway:
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
    tls: false
```

  When ALB handles TLS termination with `alb.ingress.kubernetes.io/certificate-arn` and HTTPS listen ports, keep `gateway.ingress.tls: false`.

## Step 4: Install the Gateway

```shell
helm install gateway akeyless/akeyless-gateway -f values.yaml -n akeyless --create-namespace
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

Validation criteria:

* The ingress address resolves for `gateway.yourdomain.com`.
* `https://gateway.yourdomain.com/console` is reachable.

## Step 7: Access the Gateway

* Gateway endpoint: `https://gateway.yourdomain.com/console`

### Troubleshooting

If the Gateway login shows **Authentication failed**:

* Verify `globalConfig.gatewayAuth.gatewayAccessType` and `globalConfig.gatewayAuth.gatewayAccessId` match the auth method you intend to use.
* Ensure the login identity is included in `globalConfig.allowedAccessPermissions`.
* Re-apply your chart values:

  ```shell
  helm upgrade gateway akeyless/akeyless-gateway -f values.yaml -n akeyless
  ```

## Related Reference Pages

* [Gateway on Kubernetes](https://docs.akeyless.io/docs/gateway-chart)
* [Advanced Chart Configuration](https://docs.akeyless.io/docs/advanced-chart-configuration)
* [Gateway Configuration Manager](https://docs.akeyless.io/docs/gateway-configuration-manager)
