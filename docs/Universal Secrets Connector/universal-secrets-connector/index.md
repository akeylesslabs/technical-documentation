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
---
While Akeyless is built to store, manage, and protect your secrets internally, it can also be used to manage secrets stored on other Secret Management services like AWS, GCP, Azure, or Kubernetes. This can be done **seamlessly** by creating a Universal Secrets Connector (USC) that utilizes [Targets](doc:targets) to create local "windows" into the related services, effectively letting you manage them indirectly. Each **USC** item derives its permissions from the identity linked to its [Target](doc:targets). 

When a user is granted `read` access to a **USC** item, they can act using the permissions of that underlying identity. With **USC**, you can unify governance and visibility across fragmented secret stores without migrating data or altering existing workflows.

Universal Secret Connector is also supported by the Akelyess [K8s Injector](https://docs.akeyless.io/docs/how-to-provision-secret-to-your-k8s), allowing Kubernetes applications and workloads to access secrets and credentials sourced through USC securely.

After connecting to your Universal Secrets source, you will be able to manage them from Akeyless, including viewing, adding, updating, deleting, and [syncing secrets](doc:sync-secret). The exact secret information that can be displayed in Akeyless varies between providers according to their unique attributes.

The **USC** solution works in a governance loop model, supporting and reflecting any changes made to your secrets, either from the Akeyless side or from the remote Secret Management solution. This is done automatically as Akeyless doesn't store a copy of the external secrets, ensuring that data residency and security policies remain untouched. The **USC** simply reflects them in real time, without any requirements or changes that should be made on the remote Secret Management endpoint.

Setting up Universal Secret Connector requires the **Defaults** permission on the Gateway.

<Image align="center" src="https://files.readme.io/80a2ad6-External_Secrets_-_Architecture.png" />

Akeyless currently supports creating Universal Secrets Connectors for the following services:

* [AWS Universal Secrets Connector](doc:aws-external-secrets-manager) 

* [GCP Universal Secrets Connector](doc:gcp-external-secrets-manager) 

* [Azure Universal Secrets Connector](doc:azure-external-secrets-manager) 

* [Kubernetes Universal Secrets Connector](doc:kubernetes-external-secrets-manager)

* [Hashicorp Vault Universal Secret Connector ](https://docs.akeyless.io/docs/hc-vault-universal-secrets-connector)

To view all your Universal Secret Connectors, log in to the **Console** and navigate to **Items** > **Universal Secrets Connector**.

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/managing-secrets-stored-in-aws-azure-gcp-k8s" target="_blank">Universal Secrets Connectors</a>.
