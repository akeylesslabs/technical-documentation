---
title: 'Part 2: Authentication & Authorization'
excerpt: ''
deprecated: true
hidden: true
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
Akeyless is primarily about authenticating identities and authorizing them to access secrets.

The platform serves two main types of identities: human and machine identities. "Machine" refers collectively to scripts, services, microservices, containers, VMs, and anything that is not run manually using a human identity.

Each **identity** is represented by an [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) object. Akeyless supports several types of authentication methods: [AWS IAM](https://docs.akeyless.io/docs/aws-iam), [Azure AD](https://docs.akeyless.io/docs/azure-ad), [GCP](https://docs.akeyless.io/docs/gcp-auth-method), [OCI IAM](https://docs.akeyless.io/docs/oci-iam), [API key](https://docs.akeyless.io/docs/api-key), [Kubernetes Auth](https://docs.akeyless.io/docs/kubernetes-auth), [SAML](https://docs.akeyless.io/docs/saml), [LDAP](https://docs.akeyless.io/docs/ldap), [OIDC](https://docs.akeyless.io/docs/openid), [OAuth2.0/JWT](https://docs.akeyless.io/docs/oauth20jwt), [Certificate](https://docs.akeyless.io/docs/certificate-based-authentication), and [Universal Identity (UID)](https://docs.akeyless.io/docs/universal-identity)™.

Each **Authentication Method object** is associated with an [Access Role](https://docs.akeyless.io/docs/rbac) that grants permission (including Create, Read, Update, Delete, List, and Deny) to this **identity** on Secrets, Targets, Roles, and Authentication Method objects stored inside the Akeyless SaaS solution.

An example process with a machine identity is explored here:

<Image align="center" alt="The Akeyless platform begins with an authentication method creating an Identity. An Access Role is associated with the Identity. If the Identity is authorized, the secret data can be provided." border={false} src="https://files.readme.io/6f94784-Screenshot_at_Dec_19_10-54-15.png" />

1. A container requires credentials to connect to the SQL server. It uses its AWS IAM Role as an **Authentication Method** to authenticate with Akeyless.

2. Akeyless checks permission in the **Access Role** associated with the corresponding **Authentication Method** object to make sure that the container can access the secret.

3. Akeyless provides the secret to the container. The container uses the credentials to interact directly with the SQL database.

The process is the same for human identities.