---
title: Universal Secrets Connector
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
slug: universal-secrets-connector
---
While Akeyless is built to store, manage, and protect your secrets internally, it can also be used to manage secrets stored in other secret management services such as AWS, GCP, Azure, or Kubernetes. This can be done seamlessly by creating a Universal Secrets Connector (USC) that uses [Targets](https://docs.akeyless.io/docs/targets) to establish secure logical access to the related services, enabling indirect management of those secrets. Each USC item derives its permissions from the identity linked to its Target.

When a user is granted `read` access to a **USC** item, they can act using the permissions of that underlying identity. With **USC**, you can unify governance and visibility across fragmented secret stores without migrating data or altering existing workflows.

Universal Secret Connector is also supported by the Akeyless [Kubernetes Injector](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector), allowing Kubernetes applications and workloads to access secrets and credentials sourced through USC securely.

After connecting to your Universal Secrets source, you can manage them from Akeyless, including viewing, adding, updating, deleting, and [syncing secrets](https://docs.akeyless.io/docs/sync-secret). The exact secret information that can be displayed in Akeyless varies between providers according to their unique attributes. For HashiCorp Vault connectors, you can also review secret versions in the console and sync the contents of an entire folder to the connected USC.

The **USC** solution operates in a governance loop model. It automatically detects and reflects changes to your secrets, whether those changes are made in Akeyless or in the remote secret management system. Akeyless does not store a copy of external secrets; therefore, data residency and security policies remain unchanged. The USC reflects updates in real time and does not require any configuration changes on the remote secret management endpoint.

Setting up Universal Secret Connector requires the **Defaults** permission on the Gateway.

![Illustration for: The USC solution operates in a governance loop model. It automatically detects and reflects changes to your secrets, whether those changes are made in Akeyless or in the…](https://files.readme.io/80a2ad6-External_Secrets_-_Architecture.png)

Akeyless currently supports creating Universal Secrets Connectors for the following services:

* [AWS Universal Secrets Connector](https://docs.akeyless.io/docs/aws-universal-secrets-connector)

* [GCP Universal Secrets Connector](https://docs.akeyless.io/docs/gcp-universal-secrets-connector)

* [Azure Universal Secrets Connector](https://docs.akeyless.io/docs/azure-universal-secrets-connector)

* [Kubernetes Universal Secrets Connector](https://docs.akeyless.io/docs/kubernetes-universal-secrets-connector)

* [HashiCorp Vault Universal Secret Connector](https://docs.akeyless.io/docs/hc-vault-universal-secrets-connector)

* [GitHub Universal Secret Connector](https://docs.akeyless.io/docs/github-universal-secret-connector)

To view all your Universal Secret Connectors, log in to the **Console** then navigate to **Items**, then **Universal Secrets Connector**.

## Tutorial

Check out our tutorial video on [Universal Secrets Connectors](https://tutorials.akeyless.io/docs/managing-secrets-stored-in-aws-azure-gcp-k8s).
