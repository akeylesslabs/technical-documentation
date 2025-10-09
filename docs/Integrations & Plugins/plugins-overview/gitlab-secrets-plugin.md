---
title: GitLab Secrets Plugin
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
The Akeyless <Anchor label="Official plugin" target="_blank" href="https://archives.docs.gitlab.com/18.0/ci/secrets/akeyless/">Official plugin</Anchor> for GitLab securely and easily fetches secrets into GitLab pipelines.

Using Gitlab <Anchor label="ID tokens" target="_blank" href="https://docs.gitlab.com/ci/yaml/#id_tokens">ID tokens</Anchor> when a pipeline runs, GitLab generates a unique token for the job. This token is valid only for the duration of the job and expires once the job is complete. Each job is assigned a <Anchor label="JSON Web Token (JWT)" target="_blank" href="https://docs.gitlab.com/ci/secrets/id_token_authentication/#id-tokens">JSON Web Token (JWT)</Anchor> as a `CI/CD` variable called `ID_TOKEN` which can be used to authenticate to Akeyless.

# Prerequisites

* GitLab Version  **17.4** or higher.

> 📘 Enable Akeyless CI Secret Plugin
>
> This plugin availability is currently controlled by GitLab Feature Flag, to enable this on your GitLab environment you might need to contact your GitLab Account Manager

# Authentication

This plugin supports the following Authentication Methods:

* [JWT](https://docs.akeyless.io/docs/oauth20jwt)
* [AWS IAM](https://docs.akeyless.io/docs/aws-iam)
* [Azure AD](https://docs.akeyless.io/docs/azure-ad)
* [GCP](https://docs.akeyless.io/docs/gcp-auth-method)
* [K8s](https://docs.akeyless.io/docs/kubernetes-auth)
* [Universal Identity](https://docs.akeyless.io/docs/universal-identity)
* [Access Key](https://docs.akeyless.io/docs/api-key)
* [Certificate](https://docs.akeyless.io/docs/certificate-based-authentication)

To utilized the plugin you need to use the `secrets:akeyless` keyword to authenticate and retrieve secrets from Akeyless.

By default, when using `ID_TOKEN` the `akeyless_access_type` will be set to `jwt`.  Where the Auth Method `Access ID`  should be stored inside a GitLab **CI/CD** variable.

For example:

* In your GitLab project, navigate to **Settings > CI/CD > Variables** and click the **Add Variable** button.
* Enter the Key for the variable, for example, `AKEYLESS_ACCESS_ID` with your Auth Method's **Access ID**.
* Click **Add Variable**.

The following examples demonstrate the declaration format of different Auth methods:

```yaml JWT
secrets:
    AKEYLESS_SECRET:
      token: $AKEYLESS_JWT
      akeyless:
        akeyless_api_url: '<https://Your-Gateway-URL:8080/v2>'
        name: '</SecretName>'
```
```yaml API Key
secrets:
    AKEYLESS_SECRET:
      akeyless:
        name: '</SecretName>'
        akeyless_access_type: 'api_key'
        access_key: $AKEYLESS_ACCESS_KEY
```
```yaml AWS IAM
secrets:
    AKEYLESS_SECRET:
      akeyless:
        name: '</SecretName>'
        akeyless_access_type: 'aws_iam'
```
```yaml Azure
secrets:
    AKEYLESS_SECRET:
      akeyless:
        name: '</SecretName>'
        akeyless_access_type: 'azure_ad'
        azure_object_id: 'azure_object_id'
```
```yaml GCP
secrets:
    AKEYLESS_SECRET:
      akeyless:
        name: '</SecretName>'
        akeyless_access_type: 'gcp'
        gcp_audience: 'gcp_audience'
```
```yaml K8s
secrets:
    AKEYLESS_SECRET:
      akeyless:
        name: '</SecretName>'
        akeyless_access_type: 'k8s'
        k8s_service_account_token: 'k8s_service_account_token'
        k8s_auth_config_name: 'k8s_auth_config_name'
        akeyless_api_url: '<https://Your-Gateway-URL:8080/v2>'
```
```yaml Universal Identity
secrets:
    AKEYLESS_SECRET:
      akeyless:
        name: '</SecretName>'
        akeyless_access_type: 'universal_identity'
        uid_token: 'uid_token'
```
```yaml Akeyless Token
secrets:
    AKEYLESS_SECRET:
      akeyless:
        name: '</SecretName>'
        akeyless_token: '<t-token>'
```

Where make sure to set the relevant `access_type` according to the Auth Method type you are using. for example the [API Key](https://docs.akeyless.io/docs/api-key) example demonstrates the use of **CI/CD** variable to store the Access Key. i.e. `access_key: $AKEYLESS_ACCESS_KEY`.

<br />

> 🚧 Warning
>
> For JWT authentication, it is required to add appropriate [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) based on the [claims available in the JWT](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#understanding-the-oidc-token) to prevent access by unauthorized users.
>
> Sub-Claim configuration allows Akeyless to grant access to specific workflows, based on the claims that GitLab provides in the JWT.

# Usage

Open your GitLab project and make sure you have a `yaml` file named `.gitlab-ci.yml`  and edit the Job according to your use case. All examples below will use the GitLab [ID tokens](https://docs.gitlab.com/ee/ci/yaml/index.html#id_tokens) to authenticate using [OAuth2.0/JWT](https://docs.akeyless.io/docs/oauth20jwt) Auth method.

> 📘 Tip
>
> Working with GitLab Token payload can be used with Access Roles [path templates ](https://docs.gitlab.com/ee/ci/secrets/id_token_authentication.html#token-payload) for easier management of your CI/CD project access using the `sub (subject)` field from your token.

## Secret Example

In the following example, we will fetch a [Static Secret](https://docs.akeyless.io/docs/static-secrets), this example will also work with [Rotated](https://docs.akeyless.io/docs/rotated-secrets) or [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) Secrets:

```yaml .gitlab-ci.yml
job:
  id_tokens:
    AKEYLESS_JWT:
      aud: 'https://gitlab.com'
  secrets:
    AKEYLESS_SECRET:
      akeyless:
        name: '/MyFirstSecret'
  script:
    - "echo 'Fetching secrets from akeyless'"
```

Where:

* `AKEYLESS_JWT`:  An environment variable to store the JWT to authenticate with Akeyless. It's configured with an `audience` field set to `https://gitlab.com`, if you are running your instance, make sure to adjust it accordingly

* `AKEYLESS_SECRET`: An environment variable that will store the fetched secret.

* `name`: The full name of the secret in Akeyless e.g. `/MyFirstSecret`

* `akeyless_api_url`: **Optional** Your Gateway URL **API** endpoint i.e.`<https://Your_GW_URL:8080/v2>`, by default works with the public API: `https://api.akeyless.io`.

* `gateway_ca_certificate`: **Optional**, Gateway CA Certificate when your Gateway TLS is set with **Private CA** .

> 📘 Working with Gateway
>
> To fetch **Dynamic** and **Rotated** Secrets make sure your **GitLab Runner** has network access to the relevant Akeyless Gateway.

## JSON Example

The following examples fetch a static secret named `/JSON/Secret` with a JSON key named: `imp` :

```yaml
job:
  id_tokens:
    AKEYLESS_JWT:
      aud: 'https://gitlab.com'
  secrets:
    AKEYLESS_SECRET:
      akeyless:
        name: '/JSON/Secret'
        data_key: 'imp'
    script:
    - "echo 'Fetching secrets from akeyless'"
```

## JWT reuse

When reusing the same token for multiple use the following format:

```yaml
job:  # This job fetches the Akeyless Token  
  id_tokens:  
    AKEYLESS_JWT:  
      aud: '<https://gitlab.com'>  
  secrets:  
    AKEYLESS_TOKEN:  
      token: $AKEYLESS_JWT  
      akeyless:
```

Where the `token` should hold the pre-existing **JWT token**

## Issue SSH Certificate

```yaml
job:
  id_tokens:
    AKEYLESS_JWT:
      aud: 'https://gitlab.com'
  secrets:
    SSH_CERT:
      akeyless:
        name: '/SSH_Issuer_Name'
        cert_user_name: 'cert_user_name'
        public_key_data: 'public_key_data'
```

Where the `cert_user_name` value should match the [SSH Issuer](https://docs.akeyless.io/docs/how-to-configure-ssh) allowed username list. Should be provided with a `public_key_data` to issue the certificate.

## Issue a PKI Certificate

```yaml
job:
  id_tokens:
    AKEYLESS_JWT:
      aud: 'https://gitlab.com'
  secrets:
    PKI_CERT:
      akeyless:
        name: '/PKI_Issuer_Name'
        csr_data: 'public_key_data'
```

Where the `csr_data` should contain the **CSR**, alternatively you can provide the `public_key_data` with a public key.
