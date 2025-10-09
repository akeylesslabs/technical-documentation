---
title: GitHub Actions Plugin
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
Akeyless Official [GitHub Actions](https://github.com/marketplace/actions/akeyless-authentication-and-fetching-secrets) plugin enables you to automate workflows for your GitHub-hosted repositories. With the GitHub Actions plugin, you can fetch secrets directly from Akeyless into your workflows. This guide describes how to use our various [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) to fetch [Static](https://docs.akeyless.io/docs/static-secrets), [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret), and [Rotated](https://docs.akeyless.io/docs/rotated-secrets) secrets, as well as [SSH](https://docs.akeyless.io/docs/how-to-configure-ssh) and [PKI](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) certificates, from Akeyless.

# Prerequisites

* Job permissions requirement: **(Relevant for OAuth 2.0 / JWT Authentication only)**

The default usage relies on using the GitHub `JWT` (JSON Web Token) to authenticate to Akeyless. To make this available, you must configure it inside your job workflow.

```yaml
jobs:
  my_job:
    #---------Required---------#
    permissions: 
      id-token: write
      contents: read
    #--------------------------#
```

## Runner Configuration

Configure a [self-hosted-runner](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners):

* In GitHub - navigate to the main page of the repository and select  **Settings > Actions > Runners > New self-hosted runner**.
* Select the operating system and architecture of your self-hosted-runner machine.
* Follow the instructions in the **Download** section to prepare a directory for the GitHub runner, and then download the runner.
* Follow the instructions in the **Configure** section to configure the runner to connect to GitHub with a token GitHub generates for the runner.

# Authentication

This Action plugin supports the following Authentication Methods:

* [JWT](https://docs.akeyless.io/docs/oauth20jwt)
* [AWS IAM](https://docs.akeyless.io/docs/aws-iam)
* [Azure AD](https://docs.akeyless.io/docs/azure-ad)
* [GCP](https://docs.akeyless.io/docs/gcp-auth-method)
* [K8S](https://docs.akeyless.io/docs/kubernetes-auth)
* [Universal Identity](https://docs.akeyless.io/docs/universal-identity)
* [Access Key](https://docs.akeyless.io/docs/api-key)
* [Certificate](https://docs.akeyless.io/docs/certificate-based-authentication)

## GitHub Repository Variable

You can store the `Access ID` as a GitHub variable inside the repository to use in your workflow.

In the following examples, instead of explicitly specifying the `Access ID` of the **Authentication Method** inside the workflow, we store it as a variable in the repository called `AKEYLESS_ACCESS_ID`.

* On GitHub, navigate to the main page of the repository, and select **Settings > Secrets and variables > Actions > Variables tab >  New repository variable**.
* Enter the name for the variable (for example, `AKEYLESS_ACCESS_ID` ) and set the value to your Auth Method **Access ID**.
* Select **Add Variable**.

This is only part of the `YAML` action. More complete examples are given in the next section.

```yaml JWT
        with:
          access-id: ${{ vars.AKEYLESS_ACCESS_ID }}
          access-type: jwt
          static-secrets: |
            - name: "/akeyless-github-action/github-static-secret-json"
              output-name: "my_first_secret"
```
```yaml AWS IAM
        with:
          access-id: ${{ vars.AKEYLESS_ACCESS_ID }}
          access-type: aws_iam
          static-secrets: |
            - name: "/akeyless-github-action/github-static-secret-json"
              output-name: "my_first_secret"
              key: "imp"
```
```yaml Azure
        with:
          access-id: ${{ vars.AKEYLESS_ACCESS_ID }}
          access-type: azure_ad
          static-secrets: |
            - name: "/akeyless-github-action/github-static-secret-json"
              output-name: "my_first_secret"
              key: "imp"
```
```yaml GCP
        with:
          access-id: ${{ vars.AKEYLESS_ACCESS_ID }}
          access-type: gcp
          gcp-audience: "gcp-audience"
          static-secrets: |
            - name: "/akeyless-github-action/github-static-secret-json"
              output-name: "my_first_secret"
              key: "imp"
```
```yaml K8s
        with:
          access-id: ${{ vars.AKEYLESS_ACCESS_ID }}
          access-type: k8s
          k8s-auth-config-name: "k8s-auth-config-name"
          gateway-url: "<https://Your-Akelyess-Gateway-URL:8000>"
          static-secrets: |
            - name: "/akeyless-github-action/github-static-secret-json"
              output-name: "my_first_secret"
              key: "imp"
```
```yaml Universal Identity
        with:
          access-id: ${{ vars.AKEYLESS_ACCESS_ID }}
          access-type: universal_identity
          uid_token: "uid_token"
          static-secrets: |
            - name: "/akeyless-github-action/github-static-secret-json"
              output-name: "my_first_secret"
              key: "imp" 
```
```yaml Access Key
        with:
          access-id: ${{ vars.AKEYLESS_ACCESS_ID }}
          access-type: access_key
          access-key: ${{ secrets.AKEYLESS_ACCESS_KEY }}
          static-secrets: |
            - name: "/akeyless-github-action/github-static-secret-json"
              output-name: "my_first_secret"
              key: "imp"
```
```yaml TLS Certificate
        with:
          access-id: ${{ vars.AKEYLESS_ACCESS_ID }}
          access-type: universal_identity
          uid_token: "uid_token"
          ca-certificate: ${{ secrets.AKEYLESS_CA_CERTIFICATE }}
          static-secrets: |
            - name: "/akeyless-github-action/github-static-secret-json"
              output-name: "my_first_secret"
              key: "imp"
```

> 🚧 Warning
>
> For JWT authentication, it is required to add appropriate [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) based on the [claims available in the JWT](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#understanding-the-oidc-token) to prevent access by unauthorized users.
>
> Sub-Claim configuration allows Akeyless to grant access to specific workflows, based on the claims that GitHub provides in the JWT.

For example, Create and Associate your Authentication Method with an Access Role to grant the relevant permissions within Akeyless.

```shell Oauth2.0
akeyless create-auth-method-oauth2 --name /Dev/GitHubAuth  \
--jwks-uri https://token.actions.githubusercontent.com/.well-known/jwks \
--unique-identifier repository \
--force-sub-claims

akeyless assoc-role-am --role-name /Dev/GitHubRole
--am-name /Dev/GitHubAuth
--sub-claims <your-sub-claims> 
```

For example: `repository=octo-org/octo-repo` where `octo-org = {GitHub Account}` and `octo-repo = {GitHub Repository}`.

# Usage

Although this repository's workflows use placeholder values, it is still a real Akeyless account and a real provider. The approaches demonstrated in these examples are still valid as-is for real implementations. Use these to your advantage!

> 👍 Zero-Knowledge Encryption
>
> If you are working with your own Akeyless Gateway, set the parameter `api-url` to point your Gateway Rest API endpoint e.g.  `<https://Your_GW_URL:8000/api/v2>` (or using your gateway URL at port `8081`).

## Static Secrets Example

In this example, you will fetch two static secrets from Akeyless, `my_first_secret` and `my_second_secret`. Just define each secret's path and output name. The secret values can be found in the `secrets.txt` file created in that directory (note the "key" is only relevant for JSON formatted secrets, see [below](https://docs.akeyless.io/docs/github-action#parsing-json-secrets-examples)).

```yaml
jobs:
  fetch_secrets:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read

    steps:
      - name: Fetch static secrets from Akeyless
        uses: akeyless-community/akeyless-github-action@v1.1.2
        id: fetch-secrets
        with:
          access-id: ${{ vars.AKEYLESS_ACCESS_ID }}
          access-type: jwt
          api-url: https://api.akeyless.io
          static-secrets: |
            - name: "/path/to/secret"
              output-name: "my_first_secret"
              key: "imp"
            - name: "/path/to/another/secret"
              output-name: "my_second_secret"
      - name: Use Akeyless secret
        run: |
            echo "Step Outputs"
            echo "my_first_secret: ${{ steps.fetch-secrets.outputs.my_first_secret }}" >> secrets.txt
            echo "my_second_secret: ${{ steps.fetch-secrets.outputs.my_second_secret }}" >> secrets.txt
            
            echo "Environment Variables"
            echo "my_first_secret: ${{ env.my_first_secret }}" >> secrets.txt
            echo "my_second_secret: ${{ env.my_second_secret }}" >> secrets.txt
```

## Dynamic Secrets Example

In this example, you will fetch an AWS Dynamic Secret from Akeyless, called `aws_dynamic_secret`. Just define the secret path and output name. The secret's values can be found in the `secrets.txt` file created in that directory.

```yaml
  fetch_aws_dynamic_secrets:
    runs-on: ubuntu-latest
    name: Fetch AWS dynamic secrets
    
    permissions:
      id-token: write
      contents: read
      
    steps:
    - name: Fetch dynamic secrets from Akeyless
      id: fetch-dynamic-secrets
      uses: akeyless-community/akeyless-github-action@v1.1.2
      with:
        access-id: ${{ vars.AKEYLESS_ACCESS_ID }}
        access-type: jwt        
        dynamic-secrets: |
          - name: "/path/to/dynamic/aws/secret"
            output-name: "aws_dynamic_secret"
        
# ********* KEY TAKEAWAY  ********* #
# STEP 1 - Export Dynamic Secret's keys to env vars
    - name: Export Secrets to Environment
      run: |
        echo '${{ steps.fetch-dynamic-secrets.outputs.aws_dynamic_secret }}' | jq -r 'to_entries|map("AWS_\(.key|ascii_upcase)=\(.value|tostring)")|.[]' >> $GITHUB_ENV

# STEP 2 - You can now access each secret separately as environment variables
    - name: Verify Vars
      run: |
        echo "access_key_id: ${{ env.AWS_ACCESS_KEY_ID }}" >> secrets.txt
        echo "id: ${{ env.AWS_ID }}" >> secrets.txt
        echo "secret_access_key: ${{ env.AWS_SECRET_ACCESS_KEY }}" >> secrets.txt
        echo "security_token: ${{ env.AWS_SECURITY_TOKEN }}" >> secrets.txt
        echo "ttl_in_minutes: ${{ env.AWS_TTL_IN_MINUTES }}" >> secrets.txt
        echo "type: ${{ env.AWS_TYPE }}" >> secrets.txt
        echo "user: ${{ env.AWS_USER }}" >> secrets.txt
```

## Rotated Secrets Example

In this example, you will fetch an AWS Rotated Secret from Akeyless, called `aws_rotated_secret`.

```yaml
  fetch_aws_rotated_secrets:
    runs-on: ubuntu-latest
    name: Fetch AWS rotated secrets
    
    permissions:
      id-token: write
      contents: read
      
    steps:
    - name: Fetch rotated secrets from Akeyless
      id: fetch-rotated-secrets
      uses: akeyless-community/akeyless-github-action@v1.1.2
      with:
        access-id: ${{ vars.AKEYLESS_ACCESS_ID }}
        access-type: jwt
      rotated-secrets: |
        - name: "/path/to/rotated/aws/secret"
          output-name: "aws_rotated_secret"
```

## SSH Certificates Example

In this example, you will fetch two SSH Certificates from Akeyless, called `ssh_secret1` and `ssh_secret2`.

```yaml
  fetch_ssh_secrets:
    runs-on: ubuntu-latest
    name: Fetch ssh certificate

    permissions:
      id-token: write
      contents: read

    steps:
      - name: Fetch ssh certificates from Akeyless
        id: fetch-ssh-certificate
        uses: akeyless-community/akeyless-github-action@v1.1.2
        with:
          access-type: jwt
          ssh-certificate-secrets: |
            - name: "/path/to/ssh/secret1"
              output-name: "ssh_secret1"
              cert-username: "ubuntu",
              public-key-data: "public_key_data",
            - name: "/path/to/ssh/secret2"
              output-name: "ssh_secret2"
              cert-username: "ubuntu",
              public-key-data: "public_key_data",
```

## PKI Certificates Example

In this example, you will fetch two PKI Certificates from Akeyless, called `pki_secret1` and `pki_secret2`.

```yaml
  fetch_pki_secrets:
    runs-on: ubuntu-latest
    name: Fetch pki certificate

    permissions:
      id-token: write
      contents: read

    steps:
      - name: Fetch pki certificates from Akeyless
        id: fetch-pki-certificates
        uses: akeyless-community/akeyless-github-action@v1.1.2
        with:
          access-type: jwt
          pki-certificate-secrets: |
            - name: "/path/to/pki/secret1"
              output-name: "pki_secret1"
              csr-data-base64: "csr_data_base64"
            - name: "/path/to/pki/secret2"
              output-name: "pki_secret2"
              csr-data-base64: "csr_data_base64"
```

## Create Secret Example

In this example, you will create a new static secret in Akeyless using the GitHub Action.

```yaml
name: Create Secret With Akeyless

on:
  workflow_dispatch:

jobs:
  create_secret:
    runs-on: ubuntu-latest
    name: Create Akeyless Secret

    permissions:
      id-token: write
      contents: read

    steps:
      - name: Enable Debug Logging
        run: |
          echo "ACTIONS_STEP_DEBUG=true" >> $GITHUB_ENV
          echo "ACTIONS_RUNNER_DEBUG=true" >> $GITHUB_ENV

      - name: Create a new secret in Akeyless
        uses: Akeyless-Product-Team/akeyless-github-action@main
        with:
          access-type: access_key
          access-id: ${{ secrets.AKEYLESS_ACCESS_ID }}
          access-key: ${{ secrets.AKEYLESS_ACCESS_KEY }}
          create-secret-name: "/my_new_secret"
          create-secret-value: "SuperSecretValue"
```

## Update Secret Example

In this example, you will update the value of an existing static secret in Akeyless.

```yaml
name: Update Secret With Akeyless

on:
  workflow_dispatch:

jobs:
  update_secret:
    runs-on: ubuntu-latest
    name: Update Akeyless Secret

    permissions:
      id-token: write
      contents: read

    steps:
      - name: Enable Debug Logging
        run: |
          echo "ACTIONS_STEP_DEBUG=true" >> $GITHUB_ENV
          echo "ACTIONS_RUNNER_DEBUG=true" >> $GITHUB_ENV

      - name: Update an existing secret in Akeyless
        uses: Akeyless-Product-Team/akeyless-github-action@main
        with:
          access-type: access_key
          access-id: ${{ secrets.AKEYLESS_ACCESS_ID }}
          access-key: ${{ secrets.AKEYLESS_ACCESS_KEY }}
          update-secret-name: "/my_secret"
          update-secret-value: "UpdatedSuperSecretValue"
```

## Parsing JSON Secrets Examples

By default, the action sets the environment variable value to the entire JSON string in the secret value. You can set `parse-json-secrets` to `true` to create environment variables for each key/value pair in the secret JSON.

* If the JSON uses case-sensitive keys such as "name" and "Name", the action will have duplicate name conflicts. In this case, set `parse-json-secrets` to `false` and parse the JSON secret value separately.
* You can still use the `key` and `output-name` for extracting a specific `key` with a specific name.
* The default env `name` will be the path to the secret. If your secret name is `/dev/test`, the default name will be `env.DEV_TEST_{key}`.

For a secret with JSON values:

```json secret
{
  "key1":"val1",
  "key2":"val2"
}
```

Using the following inside your `yaml`:

```yaml
   with:
      access-id: ${{ vars.AKEYLESS_ACCESS_ID }}
      access-type: jwt
      static-secrets: |
       - name: "/path/to-secret"
       - name: "/path/to-secret"
         key: "key1"
         output-name: "SECRET"
      parse-json-secrets: true
 - name: Use Akeyless secret
   run: |
     echo "key1:${{ env.PATH_TO-SECRET_KEY1 }} >> secrets.txt
     echo "key2:${{ env.PATH_TO-SECRET_KEY2 }}" >> secrets.txt
     echo "key1:${{ env.SECRET }}" >> secrets.txt
```

In this example, the output in `secrets.txt` will be:

```Text secrets.txt
key1:val1
key2:val2
key1:val1
```

If you don't want the prefix to be the secret name, you can add `prefix-json-secrets` with the prefix you would like:

```yaml
   with:
      access-id: ${{ vars.AKEYLESS_ACCESS_ID }}
      access-type: jwt
      static-secrets: |
       - name: "/path/to-secret"
         prefix-json-secrets: "MYSQL"
      parse-json-secrets: true
 - name: Use Akeyless secret
   run: |
     echo "key1 == ${{ env.MYSQL_KEY1 }}" >> secrets.txt
     echo "key2 == ${{ env.MYSQL_KEY2 }}" >> secrets.txt
```

In this example, the output in `secrets.txt` will be:

```Text secrets.txt
key1 == val1 
key2 == val2
```

### Extracting from JSON by field name

For each Akeyless secret, you can extract a specific field out of the JSON by adding the field key name.

For example, for the following static secret value name `github-static-secret-json`:

```json
{
  "imp": "value",
  "no": "no_value"
}
```

We can use the following example:

```yaml
    - name: "/akeyless-github-action/github-static-secret-json"
      output-name: "my_first_secret"
      key: "imp"
```

and in `steps.output.my_first_secret` the value will be `value`.
