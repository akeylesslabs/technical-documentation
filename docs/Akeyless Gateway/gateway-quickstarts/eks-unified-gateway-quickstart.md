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

> ℹ️ **Note:** The sample ARNs on this page use the standard AWS partition (`arn:aws`). For other partitions, use the partition-specific prefix (for example, `arn:aws-us-gov` or `arn:aws-cn`).

## Step 3: Choose an Access Path

### Option A: ALB with HTTPS (ACM)

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

### Option B: ALB with HTTP

Configure `values.yaml`:

```yaml values.yaml
gateway:
  ingress:
    enabled: true
    annotations:
      kubernetes.io/ingress.class: "alb"
      alb.ingress.kubernetes.io/scheme: "internet-facing"
      alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80}]'
      alb.ingress.kubernetes.io/target-type: ip
    rules:
      - servicePort: gateway
    path: "/*"
    pathType: ImplementationSpecific
    tls: false
```

### Option C: No ALB (port-forward)

Do not configure `gateway.ingress` in `values.yaml`. After Step 4, run:

```shell
kubectl -n akeyless port-forward svc/gateway-akeyless-gateway 8000:8000
```

Then access `http://localhost:8000/console`.

## Step 4: Install the Gateway

```shell
helm install gateway akeyless/akeyless-gateway -f values.yaml -n akeyless --create-namespace
```

## Step 5: Configure Access Endpoint

Then continue based on the option you used in Step 3:

* **Option A (HTTPS + ACM):**

    * Get the ALB DNS name:

      ```shell
      kubectl get ingress -n akeyless -o jsonpath='{.items[0].status.loadBalancer.ingress[0].hostname}'
      ```

    * Point `gateway.yourdomain.com` to the ALB DNS name in your DNS configuration (like Amazon Route 53).
    * Use `https://gateway.yourdomain.com/console`.

* **Option B (HTTP):**

    * Get the ALB DNS name:

      ```shell
      kubectl get ingress -n akeyless -o jsonpath='{.items[0].status.loadBalancer.ingress[0].hostname}'
      ```

    * Use the ALB DNS name directly over HTTP: `http://<alb-dns-name>/console`.

* **Option C (no ALB):**

    * Use `http://localhost:8000/console` while `kubectl port-forward` is running.

## Step 6: Access the Gateway

* Option A endpoint: `https://gateway.yourdomain.com/console`
* Option B endpoint: `http://<alb-dns-name>/console`
* Option C endpoint: `http://localhost:8000/console`

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
