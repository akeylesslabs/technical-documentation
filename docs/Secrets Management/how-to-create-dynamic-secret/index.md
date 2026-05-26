---
title: Dynamic Secrets
slug: how-to-create-dynamic-secret
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
Dynamic Secrets are secrets that are generated every time they are accessed, using permissions you've defined in advance. In this way, users can access a resource for a temporary period with a defined set of permissions. You can configure multiple Dynamic Secrets for the same resource to granularly control the breadth of access either per a temporary user on a specific target or for the entire target within a single action. You can revoke all temporary users immediately for a specific target as necessary.

For supported producers, you can configure password policies (for example, length and complexity requirements) when generating dynamic credentials. For the supported producers list and details, see [Password Policy for Dynamic and Rotated Secrets](https://docs.akeyless.io/docs/secrets-password-policy).

Setting up Dynamic Secrets requires the **Dynamic Secret** permission on the Gateway.

![Illustration for: Dynamic Secrets are secrets that are generated every time they are accessed, using permissions you've defined in advance. In this way, users can access a resource for a…](https://files.readme.io/757eb22-Dynamic_Secret.png)

To create a dynamic secret, you must configure the required account and access credentials. The Akeyless Platform uses these to communicate with the resource and get short-lived passwords as required. You can configure:

* [Database Dynamic Secrets](https://docs.akeyless.io/docs/create-dynamic-secret-to-sql-db)
* [Artifactory Dynamic Secrets](https://docs.akeyless.io/docs/artifactory-dynamic-secret-producer)
* [AWS Dynamic Secrets](https://docs.akeyless.io/docs/aws-producer)
* [Azure AD Dynamic Secrets](https://docs.akeyless.io/docs/azure-ad-dynamic-secrets)
* [GCP Dynamic Secrets](https://docs.akeyless.io/docs/gcp-dynamic-secrets)
* [EKS Dynamic Secrets](https://docs.akeyless.io/docs/eks-dynamic-secret-producer)
* [GKE Dynamic Secrets](https://docs.akeyless.io/docs/gke-dynamic-secret-producer)
* [LDAP Dynamic Secret](https://docs.akeyless.io/docs/ldap-dynamic-secret)
* [RabbitMQ Dynamic Secrets](https://docs.akeyless.io/docs/rabbitmq-producer)
* [Snowflake Dynamic Secrets](https://docs.akeyless.io/docs/snowflake-dynamic-secrets)
* [RDP Dynamic Secrets](https://docs.akeyless.io/docs/rdp-dynamic-secrets)
* [GitHub Dynamic Secret](https://docs.akeyless.io/docs/github-dynamic-secret)
* [OpenAI Dynamic Secret](https://docs.akeyless.io/docs/openai-dynamic-secrets)
* [GitLab Dynamic Secret](https://docs.akeyless.io/docs/gitlab-dynamic-secret)
* [Docker Hub Dynamic Secrets](https://docs.akeyless.io/docs/docker-hub-dynamic-secrets)
* [Kubernetes Generic Dynamic Secrets](https://docs.akeyless.io/docs/k8s-generic-dynamic-secrets)
* [Chef Infra Dynamic Secrets](https://docs.akeyless.io/docs/chef-infra-producer)
* [Ping Dynamic Secrets](https://docs.akeyless.io/docs/ping-dynamic-secrets)
* [Custom Dynamic Secrets](https://docs.akeyless.io/docs/custom-producer)

> ℹ️ **Info:**
>
> The configuration required to produce Dynamic Secrets is part of your private network, and are stored on the Akeyless Gateway.

Get the value of a dynamic secret when you need it.

## Tutorial

Check out our tutorial video on [Creating and Using Dynamic Secrets](https://tutorials.akeyless.io/docs/creating-and-fetching-dynamic-secrets).
