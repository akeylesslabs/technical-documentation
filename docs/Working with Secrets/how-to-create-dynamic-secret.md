---
title: Dynamic Secrets
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
Dynamic secrets are secrets that are generated every time they are accessed, using permissions you've defined in advance. In this way, users can access a resource for a temporary period with a defined set of permissions. You can configure multiple dynamic secrets for the same resource to granularly control the breadth of access either per a temporary user on a specific target or for the entire target within a single action. You can revoke all temporary users immediately for a specific target as necessary.

Setting up Dynamic Secrets requires the **Dynamic Secret** permission on the Gateway.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/757eb22-Dynamic_Secret.png",
        "dynamic-secret.png",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


To create a dynamic secret, you must configure the required account and access credentials. The Akeyless Platform uses these to communicate with the resource and get short-lived passwords as required. You can configure:

- [Database Dynamic Secrets](doc:create-dynamic-secret-to-sql-db)
- [Artifactory Dynamic Secrets](doc:artifactory-dynamic-secret-producer) 
- [AWS Dynamic Secrets](doc:aws-producer) 
- [Azure AD Dynamic Secrets](doc:azure-ad-dynamic-secrets) 
- [GCP Dynamic Secrets](doc:gcp-dynamic-secrets) 
- [EKS Dynamic Secrets](doc:eks-dynamic-secret-producer) 
- [GKE Dynamic Secrets](doc:gke-dynamic-secret-producer) 
- [LDAP Dynamic Secret](doc:ldap-dynamic-secret) 
- [RabbitMQ Dynamic Secrets](doc:rabbitmq-producer) 
- [Snowflake Dynamic Secrets](doc:snowflake-dynamic-secrets) 
- [RDP Dynamic Secrets](doc:rdp-dynamic-secrets) 
- [GitHub Dynamic Secret](doc:github-dynamic-secret) 
- [GitLab Dynamic Secret](doc:gitlab-dynamic-secret)
- [Docker Hub Dynamic Secrets](doc:docker-hub-dynamic-secrets) 
- [Kubernetes Generic Dynamic Secrets](doc:k8s-generic-dynamic-secrets) 
- [Chef Infra Dynamic Secrets](doc:chef-infra-producer) 
- [Ping Dynamic Secrets](https://docs.akeyless.io/docs/ping-dynamic-secrets)
- [Custom Dynamic Secrets](doc:custom-producer) 

> 📘 Info
> 
> The configuration required to produce dynamic secrets is part of your private network, and are stored on the Akeyless Gateway.

Get the value of a dynamic secret when you need it.

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/creating-and-fetching-dynamic-secrets" target="_blank"> Creating and Using Dynamic Secrets</a>.