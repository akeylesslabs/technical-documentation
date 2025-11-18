---
title: GitLab Component Plugin
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
[GitLab](https://www.gitlab.com) is a web-based DevOps lifecycle tool that provides a Git-repository manager including a wiki, issue-tracking, and continuous integration and deployment pipeline features.

The Akeyless plugin for GitLab Component enables a secure, easy, and intuitive way to fetch Secrets and certificates into GitLab pipelines using a [GitLab CI/CD component](https://docs.gitlab.com/ee/ci/components/) .

# Authentication

Each job has a [JSON Web Token (JWT)](https://docs.gitlab.com/ee/ci/secrets/id_token_authentication.html#id-tokens) provided as a CI/CD variable named `ID_TOKEN`. When a pipeline is about to run, GitLab uses the job token and generates a unique token for it.

> 👍 Note
>
> **GitLab v16 and higher** - `CI_JOB_JWT_V2` is replaced by [ID tokens](https://docs.gitlab.com/ee/ci/secrets/id_token_authentication.html#id-tokens)  which are the JSON Web Tokens (JWTs) that can be added to a GitLab CI/CD job.

The token is valid only while the pipeline job is running. After the job finishes, you can’t use the token anymore.

In this guide, we will use [OAuth 2.0 / JWT](https://docs.akeyless.io/docs/oauth20jwt) **Auth Method** to work with the plugin but you can use any [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) that is listed in the **Usage** section below.

## OAuth 2.0 / JWT

Create a new [OAuth 2.0 / JWT](https://docs.akeyless.io/docs/oauth20jwt) **Authentication Method** using the CLI:

```shell
akeyless create-auth-method-oauth2 --name /Dev/GitLabAuth-JWT \ 
--jwks-uri https://gitlab.com/oauth/discovery/keys \
--unique-identifier user_login
--force-sub-claims
```

Where:

* `--jwks-uri` - The URL to the `JWKS` that contains the public keys that should be used for JWT verification.

* `--unique-identifier` - A unique claim name that contains details uniquely identifying the request. In the following example, we will use the GitLab `user_login` claim.

* `--force-sub-claims` - Enforce [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) on role association.

Create an [Access Role](https://docs.akeyless.io/docs/rbac):

```shell
akeyless create-role --name /Dev/GitLabRole
```

Associate your new Role with the created Authentication Method, and assign it Sub-Claims:

```shell
akeyless assoc-role-am --role-name /Dev/GitLabRole \ 
--am-name /Dev/GitLabAuth-JWT \ 
--sub-claims user_login=<YOUR GitLab USERNAME>
```

> 🚧 Warning
>
> **Sub Claims** - It is mandatory to add an appropriate [Sub Claim](https://docs.akeyless.io/docs/sub-claims) based on the available [GitLab claims ](https://docs.gitlab.com/ci/secrets/hashicorp_vault/) to prevent access of unauthorized users.

Set `Read` and `List`  permissions for **Items**:

```shell
akeyless set-role-rule --role-name /Dev/GitLabRole \ 
--path /Path/To/your/secret/'*' \
--capability read --capability list
```

We can now continue with configuring a **GitLab project** to fetch **secrets** and **certificates** to your pipeline.

# Usage

Open your project and create a folder named `templates`, under this folder create a file named `fetch-secret.yml` and add the following content to the file:

```yaml fetch-secret.yml
spec:
  inputs:
    access-type:
      description: 'The method to use to authenticate with Akeyless, Unless token is provided, it is required.'
      default: 'jwt'
    access-id:
      description: 'Akeyless Access ID, Unless token is provided, it is required.'
      default: ''
    access-key:
      description: 'Akeyless Access Key'
      default: ''
    gcp-audience:
      description: 'GCP audience to use in signed JWT (relevant only for access-type=gcp)'
      default: 'akeyless.io'  
    api-url:
      description: 'The API endpoint to use, defaults to https://api.akeyless.io.'
      default: https://api.akeyless.io
    token:
      description: 'Akeyless authentication token.'
      default: ''
    uid-token:
      description: 'The universal identity token, Required only for universal_identity authentication'
      default: ''
    azure-object-id:
      description: 'Azure Active Directory ObjectId (relevant only for access-type=azure_ad)'
      default: ''
    k8s-service-account:
      description: 'The K8S service account token'
      default: ''
    k8s-auth-config-name:
      description: 'The K8S Auth config name (relevant only for access-type=k8s)'
      default: ''
    gateway-ca-cert:
      description: 'The CA certificate for the authentication to gateway'
      default: ''  
    static-secrets:
      description: 'A YAML list representing static secrets to fetch'
      type: array
      default: [] 
    dynamic-secrets:
      description: 'A YAML list representing dynamic secrets to fetch'
      type: array
      default: []
    rotated-secrets:
      description: 'A YAML list representing rotated secrets to fetch'
      type: array
      default: []
    ssh-certificates:
      description: 'A YAML list representing ssh certificates to fetch.'
      type: array
      default: []
    pki-certificates:
      description: 'A YAML list representing pki certificates to fetch.'
      type: array
      default: []
    env-file:
      type: boolean
      default: true
---

akeyless_secrets:
  stage: get-akeyless-secret
  id_tokens:
    AKEYLESS_JWT:
      aud: 'https://api.akeyless.io'
  image: 
    name: akeyless/gitlab-component:v0.0.3
    pull_policy: always
  script:  
    - STATIC_SECRETS=`echo '$[[ inputs.static-secrets ]]' | base64`
    - DYNAMIC_SECRETS=`echo '$[[ inputs.dynamic-secrets ]]' | base64`
    - ROTATED_SECRETS=`echo '$[[ inputs.rotated-secrets ]]' | base64`
    - SSH_CERTIFICATES=`echo '$[[ inputs.ssh-certificates ]]' | base64`
    - PKI_CERTIFICATES=`echo '$[[ inputs.pki-certificates ]]' | base64`
    - ENV_FILE=$[[ inputs.env-file ]]
    - touch akeyless.env
    - touch akeyless.json
    - |
      if [ "$ENV_FILE" = true ]; then
        /app/akeylessci -type $[[ inputs.access-type ]] -id=$[[ inputs.access-id ]] -key=$[[ inputs.access-key ]] -jwt ${AKEYLESS_JWT} -token=$[[ inputs.token ]] -api-url $[[ inputs.api-url ]] -uid-token="$[[ inputs.uid-token ]]" -azure-object-id="$[[ inputs.azure-object-id ]]" -k8s-service-account="$[[ inputs.k8s-service-account ]]" -k8s-auth-config-name="$[[ inputs.k8s-auth-config-name ]]" -gateway-ca-cert="$[[ inputs.gateway-ca-cert ]]" -static-secrets="${STATIC_SECRETS}" -dynamic-secrets="${DYNAMIC_SECRETS}" -rotated-secrets="${ROTATED_SECRETS}" -ssh-certificates="${SSH_CERTIFICATES}" -pki-certificates="${PKI_CERTIFICATES}" -env-file=$[[ inputs.env-file ]] > akeyless.env
      else
        /app/akeylessci -type $[[ inputs.access-type ]] -id=$[[ inputs.access-id ]] -key=$[[ inputs.access-key ]] -jwt ${AKEYLESS_JWT} -token=$[[ inputs.token ]] -api-url $[[ inputs.api-url ]] -uid-token="$[[ inputs.uid-token ]]" -azure-object-id="$[[ inputs.azure-object-id ]]" -k8s-service-account="$[[ inputs.k8s-service-account ]]" -k8s-auth-config-name="$[[ inputs.k8s-auth-config-name ]]" -gateway-ca-cert="$[[ inputs.gateway-ca-cert ]]" -static-secrets="${STATIC_SECRETS}" -dynamic-secrets="${DYNAMIC_SECRETS}" -rotated-secrets="${ROTATED_SECRETS}" -ssh-certificates="${SSH_CERTIFICATES}" -pki-certificates="${PKI_CERTIFICATES}" -env-file=$[[ inputs.env-file ]] > akeyless.json
      fi  
  artifacts:
    reports:
      dotenv: akeyless.env
    paths:
      - akeyless.json  
```

where the plugin can be used in the following modes:

* `env-file`: This mode stores **secrets**  in environment variables, which are stored inside an `env` file for future usage across jobs, this mode has character and structure limitations, for example, it's not possible to fetch **certificates** items.

* `json`:  This mode stores **secrets** and **certificates** in a `json` file where any format can be fetched. It is recommended to use with `jq` for easier parsing of the`JSON` content.

Your secrets are stored either in `akeyless.env` or `akeyless.json` accordingly, enabling secret usage across different jobs.

> 📘 Pull Policy
>
> Note that the `pull_policy` should be kept to `always` when using a shared runner.

# Examples

In the following example, we will use the `env-file` mode. where the secrets will be stored in environment variables. Additionally, upon a successful authentication, the value of the **Akeyless Token**   will be saved automatically into the `AKEYLESS_TOKEN` environment variable, so it can be reused.

Create a file named `.gitlab-ci.yml`, as follows:

```yaml .gitlab-ci.yml
stages:
  - get-akeyless-secret
  - use_secret

include:
  # include the component located in the current project from the current SHA
  - component: gitlab.com/$CI_PROJECT_PATH/fetch-secret@$CI_COMMIT_SHA
    inputs:
      access-type: jwt
      access-id: <Access_ID>
      api-url: https://api.akeyless.io
      static-secrets:
        - name: 'path/to/static_secret'
          output-name: 'SECRET_VALUE'
      dynamic-secrets:
        - name: 'path/to/dynamic_secret'
          output-name: 'DYNAMIC_SECRET_VALUE'
      rotated-secrets:
        - name: 'path/to/rotated_secret'
          output-name: 'ROTATED_SECRET_VALUE'

     
use_secret:
  stage: use_secret
  needs:
    - job: akeyless_secrets
      artifacts: true
  script:
    - echo "Fetching Secrets From Akeyless"
```

In this example, we demonstrated using both [Static](https://docs.akeyless.io/docs/static-secrets), [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret), and [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets) while using the [JWT](https://docs.akeyless.io/docs/oauth20jwt) auth method which we created earlier.

> 👍 Tip
>
> Use [GitLab CI/CD variables](https://docs.gitlab.com/ee/ci/variables/#for-a-project) to store your **Access ID** for easier future reference.

In this example, we will use the `json` mode by setting the `env-file` setting to `false`  in order to fetch [PKI](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) or [SSH](https://docs.akeyless.io/docs/ssh-certificates#issuing-a-certificate) certificates:

```yaml PKI
stages:
  - get-akeyless-secret
  - use_secret

include:
  # include the component located in the current project from the current SHA
  - component: gitlab.com/$CI_PROJECT_PATH/fetch-secret@$CI_COMMIT_SHA
    inputs:
      access-type: jwt
      access-id: <Access_ID>
      api-url: https://api.akeyless.io
      env-file: false
      pki-certificates:
        - name: '/Path/to/Certificate Issuer'
          output-name: 'Certificate_Value'
          csr-data: <Base64 CSR data>

use_secret:
  stage: use_secret
  needs:
    - job: akeyless_secrets
      artifacts: true
  image: alpine:latest    
  before_script:
    - apk update
    - apk add jq

  script:    
    - echo "Fetching certificates from Akeyless" 
```
```yaml SSH
stages:
  - get-akeyless-secret
  - use_secret

include:
  # include the component located in the current project from the current SHA
  - component: gitlab.com/$CI_PROJECT_PATH/fetch-secret@$CI_COMMIT_SHA
    inputs:
      access-type: jwt
      access-id: <Access_ID>
      api-url: https://api.akeyless.io
      env-file: false
      ssh-certificates:
        - name: '/Path/to/Certificate Issuer'
          output-name: 'Certificate_Value'
          cert-user-name: <Allowed users>
          public-key-data: <Base64 Public key data>

use_secret:
  stage: use_secret
  needs:
    - job: akeyless_secrets
      artifacts: true
  image: alpine:latest    
  before_script:
    - apk update
    - apk add jq

  script:
    - echo "Fetching certificates from Akeyless" 
```

Where:

* `csr-data`: **Base64 Encoded CSR**  for issuing the certificate. **Relevant only for PKI Certificate**, alternatively you can use `public-key-data` instead.

* `public-key-data`**public key** for issuing a certificate, only for **PKI Certificate** must be in a **Base64** format

* `cert-user-name`: Users who will be allowed to use the certificate. **Relevant only for SSH Certificate**.

# Working with Gateway

To work directly with your Gateway URL  you can set  the variable `api_url` with the Rest API V2 endpoint i.e. port `8081`. When working with a self-signed certificate you can provide your `gateway_ca_certificate` as well.
