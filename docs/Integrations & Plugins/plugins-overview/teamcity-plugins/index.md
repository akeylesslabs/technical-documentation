---
title: TeamCity Plugins
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
Akeyless supports two TeamCity integration paths.

Choose the plugin that matches your architecture and migration stage.

* [TeamCity Plugin](https://docs.akeyless.io/docs/teamcity-akeyless-plugin): Native Akeyless TeamCity plugin that connects directly to the Akeyless API.
    * The native TeamCity plugin is available in JetBrains Marketplace: [Akeyless Secrets Management](https://plugins.jetbrains.com/plugin/30559-akeyless-secrets-management).
* [TeamCity Plugin by way of HashiCorp Vault Proxy](https://docs.akeyless.io/docs/teamcity-hcv-plugin): HashiCorp Vault-compatible integration path through the Akeyless HashiCorp Vault Proxy.

Use the native plugin for new implementations.

Use the HashiCorp Vault Proxy plugin path if you need compatibility with existing Vault-based TeamCity workflows.
