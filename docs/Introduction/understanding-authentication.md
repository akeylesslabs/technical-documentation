---
title: 'Part 2: Authentication & Authorization'
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: rbac
      title: RBAC
---
At heart, Akeyless is all about authenticating identities and authorizing them to access secrets.

The platform serves two main types of identities: human and machine identities. When we say "machine", we are referring collectively to scripts, services, microservices, containers, VMs, and so on - anything that is not run manually using a human identity.

Each **identity** is represented by an [Authentication Method](doc:access-and-authentication-methods) object. Akeyless supports several types of authentication methods: [AWS IAM](doc:aws-iam), [Azure AD](doc:azure-ad), [GCP](doc:gcp-auth-method), [OCI IAM](doc:oci-iam), [API key](doc:api-key), [Kubernetes Auth](doc:kubernetes-auth), [SAML](doc:saml), [LDAP](doc:ldap), [OIDC](doc:openid), [OAuth2.0/JWT](doc:oauth20jwt), [Certificate](doc:certificate-based-authentication), and [Universal Identity (UID)](doc:universal-identity)™.

Each **Authentication Method object** is associated with an [Access Role](https://docs.akeyless.io/docs/rbac) that grants permission (including Create, Read, Update, Delete, List, and Deny) to this **identity** on Secrets, Targets, Roles, and Authentication Method objects stored inside the Akeyless SaaS solution.

Let's see how this process works for a machine identity.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/6f94784-Screenshot_at_Dec_19_10-54-15.png",
        "Screenshot at Dec 19 10-54-15.png",
        960
      ],
      "align": "center",
      "sizing": "smart"
    }
  ]
}
[/block]


1. A container requires credentials to connect to the SQL server. It uses its AWS IAM Role as an **Authentication Method** to authenticate with Akeyless.

2. Akeyless checks permission in the **Access Role** associated with the corresponding **Authentication Method** object to make sure that the container can access the secret.

3. Akeyless provides the secret to the container. The container uses the credentials to interact directly with the SQL database.

The process is the same for human identities.