---
title: Alibaba Cloud ACK Deployment
deprecated: false
hidden: false
metadata:
  robots: index
---
This page includes only Alibaba Cloud Container Service for Kubernetes (ACK)-specific delta steps.

Review the [Kubernetes Helm deployment page](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm) first, then apply the ACK changes in this guide.

## Scope

This guide assumes that the baseline Helm deployment flow is complete, including:

- Helm chart setup
- base `values.yaml` preparation
- installation and upgrade flow
- Gateway admin and permission model

This page focuses on ACK RAM identity integration and ACK-specific `values.yaml` changes.

## Prerequisites

Complete all baseline prerequisites from the main Helm deployment page, and add:

- An [AliCloud authentication method](https://docs.akeyless.io/docs/alicloud) in Akeyless.
- An ACK RAM role strategy:
  - Worker node RAM role, or
  - RAM Roles for Service Accounts (RRSA).
- If using RRSA, RRSA enabled on the cluster, the `ack-pod-identity-webhook` add-on installed, and a RAM role bound to the target Kubernetes ServiceAccount as documented in the [ACK RRSA guide](https://www.alibabacloud.com/help/en/ack/serverless-kubernetes/user-guide/use-rrsa-to-authorize-pods-to-access-different-cloud-services).

## ACK Identity Delta

Set the Gateway auth type to `alicloud` and provide your AliCloud Access ID:

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <AliCloud Access ID>
    gatewayAccessType: alicloud
  allowedAccessPermissions: {}
```

With a worker node RAM role, nothing else is required: the Gateway uses the RAM role of the ECS instance it runs on.

For RRSA, enable automatic injection on the Gateway namespace:

```shell
kubectl label namespace <namespace> pod-identity.alibabacloud.com/injection=on
```

Then set the ServiceAccount annotation with the RAM role name:

```yaml values.yaml
globalConfig:
  serviceAccount:
    create: true
    serviceAccountName: <ACK ServiceAccount Name>
    annotations:
      pod-identity.alibabacloud.com/role-name: <RAM Role Name>
```

<Callout icon="ℹ️" theme="info">
  ### Info:

  The chart applies ServiceAccount annotations only when `create` is `true`. With an existing ServiceAccount (`create: false`), add the annotation to it yourself.
</Callout>

## Validation Delta

After deployment, validate that the Gateway pod uses AliCloud identity successfully:

1. Confirm the pod is running:

   ```shell
   kubectl get pods -n <namespace>
   ```

2. If using RRSA, verify the ServiceAccount annotation:

   ```shell
   kubectl get sa <ACK ServiceAccount Name> -n <namespace> -o yaml
   ```

3. If using RRSA, verify that the role and OIDC token were injected into the pod:

   ```shell
   kubectl get pod <Gateway Pod Name> -n <namespace> -o yaml | grep ALIBABA_CLOUD_
   ```

4. Validate Gateway connectivity and login through the management endpoint after install.

## Related Tasks

- For shared Helm install and upgrade commands, use the main Kubernetes Helm deployment page.
- For advanced chart settings, use [Advanced Kubernetes Configuration](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference).
- For TLS configuration, use [Configuring TLS](https://docs.akeyless.io/docs/gateway-tls-settings).
