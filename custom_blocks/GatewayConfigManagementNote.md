---
name: GatewayConfigManagementNote
---
<!-- markdownlint-disable MD041 -->
> ❗ **Important:**
>
> For ongoing Gateway configuration changes, always use the Gateway Configuration Manager, Akeyless CLI, or Helm values (for Kubernetes) to manage settings for the entire Gateway cluster.
>
> **Never configure only a single Gateway instance in a cluster.** All instances in a cluster must be managed together using the supported tools above. Configuring only one instance, or making changes to individual containers or pods, will result in configuration drift, inconsistent behavior, and potential security or availability risks.
>
> Avoid per-instance container startup command changes for routine updates. These should only be used for initial bootstrap or emergency recovery, not for ongoing management.
