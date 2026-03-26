---
title: GitHub Universal Secret Connector
deprecated: false
hidden: false
metadata:
  robots: index
---
This page discusses the creation of GitHub [Universal Secrets Connectors](https://docs.akeyless.io/docs/universal-secrets-connector). If you wish to create a Universal Secrets Connector for a different cloud service, please go to the matching doc, as they have varying parameters.

Unlike other **USCs**, GitHub does not let you view secret values outside GitHub. With this USC, you can **create new secrets**, **update existing secrets**, and **delete secrets** in the repository.

GitHub USC setup and management has 3 scopes:

* **Repository**: Choose a repository by **Name**, **Topic**, or **Custom Property**.
* **Organization**: Choose **Private**, **Public**, or **Selected**.
  * **Private**: Manage secrets for **Private** repositories.
  * **Public**: Manage secrets for **Public** repositories.
  * **Selected**: Manage secrets for the repositories you choose.
* **Environment Repository**: Choose the Environment Repository where you want to manage secrets.

## Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) version `4.48.0` or later.
* [GitHub target](https://docs.akeyless.io/docs/github-target)

<br />

<br />
