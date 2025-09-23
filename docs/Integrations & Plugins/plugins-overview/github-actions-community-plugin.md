---
title: GitHub Actions Community Plugin
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
# Overview

GitHub Actions enables you to automate workflows for your GitHub-hosted repositories. 

With [this](https://github.com/LanceMcCarthy/akeyless-action) **community** plugin, you can fetch secrets directly from the Akeyless Platform into your workflows.

This guide will demonstrate the uses of [ OAuth 2.0 / JWT](https://docs.akeyless.io/docs/oauth20jwt) and [AWS IAM](https://docs.akeyless.io/docs/aws-iam) **Authentication Methods** to fetch both [Static ](https://docs.akeyless.io/docs/static-secrets)and [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) secrets from Akeyless.

# Prerequisites

- Job permissions requirement: **(Relevant for OAuth 2.0 / JWT Authentication only)**

The default usage relies on using the GitHub JWT (JSON Web Token) to authenticate to Akeyless. To make this available, you must configure it inside your job workflow.

```yaml
jobs:
  my_job:
    #---------Required---------#
    permissions: 
      id-token: write
      contents: read
    #--------------------------#
```

- For Dynamic Secrets, [jq](https://stedolan.github.io/jq/) must be installed on the runner host.

# Authentication

The following Authentication Methods can be used for authentication:

## OAuth 2.0 / JWT

Create a new [OAuth 2.0 / JWT](https://docs.akeyless.io/docs/oauth20jwt) **Authentication Method** using the CLI:

```shell
akeyless create-auth-method-oauth2 --name /Dev/GitHubAuth  \
--jwks-uri https://token.actions.githubusercontent.com/.well-known/jwks \
--unique-identifier repository \
--force-sub-claims
```

Where:

- `--jwks-uri` - The URL to the `JWKS` that contains the public keys that would be used for JWT verification.

- `--unique identifier`, A unique ID, usually a value such as `email`, `username` or `upn` for example. Whenever a user logs in with a token, these authentication types issue [Sub-Claims](doc:sub-claims)  that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value you configured and is used to distinguish between users from within the same organization.

- `--force-sub-claims` -  Enforce role association to include sub-claims.

Create an **[Access Role](https://docs.akeyless.io/docs/rbac)**:

```shell
akeyless create-role --name /Dev/GitHubRole
```

> 🚧 Warning
> 
> ** It is required ** to add appropriate [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) based on the [claims available in the JWT](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#understanding-the-oidc-token) to prevent access by unauthorized users.
> 
> Sub-Claim configuration allows Akeyless to grant access to specific workflows, based on the claims that GitHub provides in the JWT.

Attach your `OAuth 2.0 / JWT` **Authentication Method** to the **Access Role** that was created and add an appropriate **Sub-Claim**, for example: `repository=octo-org/octo-repo` where `octo-org = {GitHub Account}` and `octo-repo = {GitHub Repository}`.

```shell
akeyless assoc-role-am --role-name /Dev/GitHubRole \
--am-name /Dev/GitHubAuth  \
--sub-claims repository=<octo-org/octo-repo>
```

Set `Read` permissions for **Items **for the **Access Role**:     

```shell
akeyless set-role-rule --role-name /Dev/GitHubRole \
--path /Path/To/your/secret/'*' \
--capability read
```

## AWS IAM

Create an [AWS IAM](https://docs.akeyless.io/docs/aws-iam) **Authentication Method** using the CLI:

```shell
akeyless create-auth-method-aws-iam \
--name /Dev/AWSAuth  \
--bound-aws-account-id <AWS Account ID>
```

Create an  [Access Role ](https://docs.akeyless.io/docs/rbac):

```shell
akeyless create-role --name /Dev/AWSRole
```

Attach the AWS IAM **Authentication Method** to the **Access Role** :

```shell
akeyless assoc-role-am --role-name /Dev/AWSRole \
--am-name /Dev/AWSAuth
```

Set `Read` permissions for **Items** for the **Access Role**:     

```shell
akeyless set-role-rule --role-name /Dev/AWSRole \
--path /Path/To/your/secret/'*' \
--capability read
```

### **Runner Configuration**

Configure a [self-hosted-runner](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners):

- In GitHub - navigate to the main page of the repository and select  **Settings > Actions > Runners > New self-hosted runner**.
- Select the operating system and architecture of your self-hosted-runner machine.
- Follow the instructions in the **Download** section to prepare a directory for the GitHub runner, and then download the runner.
- Follow the instructions in the **Configure** section to configure the runner to connect to GitHub with a token GitHub generates for the runner.

## GitHub Repository Secret

You can store the `AccessID` as a GitHub secret inside the repository to use in your workflow.

In the following examples, instead of explicitly specifying the `AccessID` of the **Authentication Method** inside the workflow, we store it as a secret in the repository as a variable called `ACCESS_ID`.

- On GitHub, navigate to the main page of the repository, and select **Settings > Secrets and variables > Actions > New repository secret**.
- Enter the name for the secret (for example, `ACCESS_ID` ) and set the secret value to your Auth Method **Access ID**.
- Select **Add secret**.

# Usage

The following examples will demonstrate how to fetch [Static](https://docs.akeyless.io/docs/static-secrets) and [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) secrets from Akeyless.

## Fetching Static Secrets

Create a static secret using the following command:

```shell
akeyless create-secret --name /GitHub/MyGitSecret --value <Secret value>
```

Example of fetching a static secret using OAuth 2.0 / JWT and AWS_IAM Authentication Methods :

```yaml JWT
name: 'Static-Secret'
on: push

jobs:
  fetch_secrets:
    runs-on: 'ubuntu-latest'
    permissions:  # IMPORTANT - both of these are required
      id-token: write
      contents: read
    name: Fetch some static secrets
    steps:
    - name: Fetch secrets from AKeyless
      id: fetch-secrets
      uses: LanceMcCarthy/akeyless-action@v3
      with:
        access-id: ${{ secrets.ACCESS_ID}}
        static-secrets: '{"/GitHub/MyGitSecret":"MY_SECRET"}'
        
    - name: Use Outputs
      run: |
        echo "Step Outputs"
        echo "MY_SECRET: ${{ steps.fetch-secrets.outputs.MY_SECRET }}"
        echo "Environment Variables"
        echo "MY_SECRET: ${{ env.MY_SECRET }}"
```
```yaml AWS_IAM
name: 'Static-Secret'
on: push

jobs:
  fetch_secrets:
    runs-on: 'self-hosted'
    name: Fetch some static secrets
    steps:
    - name: Fetch secrets from AKeyless
      id: fetch-secrets
      uses: LanceMcCarthy/akeyless-action@v3.1.1
      with:
        access-id: ${{ secrets.ACCESS_ID}}
        access-type: 'aws_iam'
        static-secrets: '{"GitHub/MyGitSecret":"MY_SECRET"}'
        
    - name: Use Outputs
      run: |
        echo "Step Outputs"
        echo "MY_SECRET: ${{ steps.fetch-secrets.outputs.MY_SECRET }}"
        echo "Environment Variables"
        echo "MY_SECRET: ${{ env.MY_SECRET }}"
```

## Fetching Dynamic Secrets

The key difference with dynamic secrets is that the output value is typically a JSON object. There are two ways you can handle this: default output or parsed output.

Example of fetching AWS Dynamic Secret using OAuth 2.0 / JWT Authentication Method:

```yaml Default
name: 'MyDynamicSecret'
on: push

jobs: 
	fetch_dynamic_secrets:
    runs-on: 'ubuntu-latest'
    name: Fetch dynamic secrets
    
    permissions:
      id-token: write
      contents: read
      
    steps:
    - name: Fetch dynamic secrets from Akeyless
      id: fetch-dynamic-secrets
      uses: LanceMcCarthy/akeyless-action@v3
      with:
        access-id: ${{ secrets.ACCESS_ID }}
        dynamic-secrets: '{"/GitHub/MyGitSecret":"MY_SECRET"}'
        
    - name: Export Secrets to Environment Vars
      run: |
        echo '${{ steps.fetch-dynamic-secrets.outputs.MY_SECRET }}' | jq -r 'to_entries|map("JWT_\(.key)=\(.value|tostring)")|.[]' >> $GITHUB_ENV
# You can now access each secret separately as environment variables
    - name: Verify Vars
      run: |
        echo "access_key_id: ${{ env.JWT_access_key_id }}"
        echo "id: ${{ env.JWT_id }}"
        echo "secret_access_key: ${{ env.JWT_secret_access_key }}"
        echo "type: ${{ env.JWT_type }}"
```
```yaml Parsed
name: 'MyDynamicSecret'
on: push

jobs: 
  fetch_dynamic_secrets:
    runs-on: 'ubuntu-latest'
    name: Fetch dynamic secrets
    
    permissions:
      id-token: write
      contents: read
      
    steps:
    - name: Fetch dynamic secrets from Akeyless
      id: fetch-dynamic-secrets
      uses: LanceMcCarthy/akeyless-action@v3.1.1
      with:
        access-id: ${{ secrets.ACCESS_ID }}
        dynamic-secrets: '{"/GitHub/MyGitSecret":"MY_SECRET"}'
        parse-dynamic-secrets: true

    - name: Verify Job Outputs
      run: |
        echo "access_key_id: ${{ steps.fetch-dynamic-secrets.outputs.access_key_id }}"
        echo "id: ${{ steps.fetch-dynamic-secrets.outputs.id }}"
        echo "secret_access_key: ${{ steps.fetch-dynamic-secrets.outputs.secret_access_key }}"
        echo "type: ${{ steps.fetch-dynamic-secrets.outputs.type }}"
        
    - name: Verify Environment Variables
      run: |
        echo "access_key_id: ${{ env.access_key_id }}"
        echo "id: ${{ env.id }}"
        echo "secret_access_key: ${{ env.secret_access_key }}"
        echo "type: ${{ env.type }}"
```

For additional information use this [link](https://github.com/LanceMcCarthy/akeyless-action).

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/managing-secrets-in-github-pipelines" target="_blank" style="color: #00e">Managing Secrets in Github Pipelines</a>.