---
title: Authentication Methods for Kubernetes
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
Akeyless supports multiple options to authenticate your K8s cluster with Akeyless platform:

- **[Kubernetes (K8s) Auth](https://docs.akeyless.io/docs/kubernetes-auth)**
- **[Universal Identity (UID)](https://docs.akeyless.io/docs/universal-identity)**  Not supported by the External Secret Operator (ESO).
- **[API Key](https://docs.akeyless.io/docs/api-key)**
- Cloud Authentication:
  - **[Azure Active Directory (AD)](https://docs.akeyless.io/docs/azure-ad)**
  - **[AWS-IAM](https://docs.akeyless.io/docs/aws-iam)**
  - **[GCP Auth](https://docs.akeyless.io/docs/gcp-auth-method)**

# K8s Auth

> 👍 Note
> 
> Native Kubernetes attributes such as `namespace` and `pod_name` can be leveraged as [sub-claims](doc:sub-claims) for policy segregation when using [Kubernetes Authentication](https://docs.akeyless.io/docs/kubernetes-auth).

To use the K8s Auth method for authentication:

```yaml YAML
AKEYLESS_ACCESS_TYPE: "k8s"
AKEYLESS_ACCESS_ID: "<Access Id>"
AKEYLESS_K8S_AUTH_CONF_NAME: "K8s_conf_name"
#you need to provide one of the following:
AKEYLESS_GW_CONFIG_URL: "http://<Your-Akeyless-GW-URL:8000/console>" # or using port 18888
or
AKEYLESS_API_GW_URL: "https://<Your-Akeyless-GW-URL:8000/api/v1>" # or using port 8080
```

> 📘 Zero-Knowledge
> 
> While working with Customer Fragment for Zero-Knowledge set: `AKEYLESS_API_GW_URL: "https://<Your-Akeyless-GW-URL:8000/api/v1>"`

# Universal Identity (UID)

To use UID Auth method for authentication:

```yaml YAML
AKEYLESS_ACCESS_TYPE: "universal_identity"
AKEYLESS_API_GW_URL: "https://<Your-Akeyless-GW-URL:8080>" 
AKEYLESS_INIT_TOKEN: "<token>"
```

# API Key

To use API Key Auth method for authentication:

```yaml YAML
AKEYLESS_URL: "https://vault.akeyless.io"
# to Work with Private GW
# AKEYLESS_API_GW_URL: "https://<Your-Akeyless-GW-URL:8080>" 
AKEYLESS_ACCESS_TYPE: "api_key"
AKEYLESS_API_KEY: "<Access Key>"
AKEYLESS_ACCESS_ID: "<Access Id>"
```

# Cloud Authentication

## Azure Active Directory (AD)

To use Azure AD Auth method for authentication:

```yaml YAML
AKEYLESS_URL: "https://vault.akeyless.io"
# to Work with Private GW
# AKEYLESS_API_GW_URL: "https://<Your-Akeyless-GW-URL:8080>" 
AKEYLESS_ACCESS_TYPE: "azure_ad"
AKEYLESS_ACCESS_ID: "<Access Id>"
# optional
# AKEYLESS_AZURE_OBJ_ID: "<azure-object-id>"
```

## AWS-IAM

To use AWS-IAM Auth method for authentication:

```yaml YAML
AKEYLESS_URL: "https://vault.akeyless.io"
# to Work with Private GW
# AKEYLESS_API_GW_URL: "https://<Your-Akeyless-GW-URL:8080>" 
AKEYLESS_ACCESS_TYPE: "aws_iam"
AKEYLESS_ACCESS_ID: "<Access Id>"
```

## GCP Auth

To use GCP Auth method for authentication:

```yaml
AKEYLESS_URL: "https://vault.akeyless.io"
# to Work with Private GW
# AKEYLESS_API_GW_URL: "https://<Your-Akeyless-GW-URL:8080>" 
AKEYLESS_ACCESS_TYPE: "gcp"
AKEYLESS_ACCESS_ID: "<Access Id>"
AKEYLESS_GCP_AUDIENCE: "akeyless.io"
```