---
title: BitBucket Plugin
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
[Bitbucket](https://bitbucket.org/product/) is a web-based Git repository hosting service by Atlassian that supports code review, branching workflows, and issue tracking, with built-in continuous integration and delivery via Bitbucket Pipelines.

The Akeyless integration for Bitbucket Pipelines enables a secure, simple, and native way to fetch secrets just-in-time into pipeline steps—avoiding secrets in code or config while keeping deployments seamless.

Using the **BitBucket** plugin enables you to work with [Static](https://docs.akeyless.io/docs/static-secrets), [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) and [Rotated](https://docs.akeyless.io/docs/rotated-secrets) secrets, as well as [PKI](https://docs.akeyless.io/docs/certificate-lifecycle-management) and [SSH](https://docs.akeyless.io/docs/ssh-certificates) certificates.

Each pipeline step runs in isolation, so secrets don’t carry over automatically. The Akeyless Bitbucket Pipe stores them in `bitbucket-pipes-exports.env`, declaring it as an artifact lets later steps access them without re-fetching.

# Supported Authentication Methods

* [OAuth 2.0/JWT](https://docs.akeyless.io/docs/oauth20jwt)
* [API Key](https://docs.akeyless.io/docs/api-key)

> 👍 Note
>
> It is best practice to use environment variables instead of writing the actual variable values inside the pipeline.
>
> You can store your `AccessID` and `AccessKey` as secured [repository variables](https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/) in your Bitbucket repository settings.

In this guide, for simplicity, we will use an **API Key**.

# Examples

The section below will demonstrate how to work with items from your Akeyless account in your Bitbucket pipeline.

## Working With Secrets

In order to fetch a secret from your Akeyless account, set the following configuration:

```yaml Static
pipelines:
  default:
    - step:
        name: Fetch Secrets from Akeyless
        script:
          - pipe: akeyless/akeyless-bitbucket-pipe:latest
            variables:
              ACCESS_ID: $ACCESS_ID
              ACCESS_KEY: $ACCESS_KEY
              STATIC_SECRETS: |
                - name: "/path/to/secret"        # The full path of the secret in Akeyless
                  output-name: "MY_OUTPUT_NAME"  # name of the environment variable to create
                - name: "/path/to/json/secret"
                  output-name: "MY_JSON_VALUE"
                  key: "database.password"       # Optional: key to extract from a JSON secret
        artifacts: # This section is required to pass secrets to the next step
          - bitbucket-pipes-exports.env

    - step:
        name: Use the Secrets
        script:
          - echo "MY_OUTPUT_NAME=$MY_OUTPUT_NAME"
          - echo "MY_JSON_VALUE=$MY_JSON_VALUE"

```
```yaml Dynamic
pipelines:
  default:
    - step:
        name: Fetch Secrets from Akeyless
        script:
          - pipe: akeyless/akeyless-bitbucket-pipe:latest
            variables:
              ACCESS_ID: $ACCESS_ID
              ACCESS_KEY: $ACCESS_KEY
              DYNAMIC_SECRETS: |
                - name: "/path/to/secret"        # The full path of the secret in Akeyless
                  output-name: "MY_OUTPUT_NAME"  # name of the environment variable to create
                - name: "/path/to/json/secret"
                  output-name: "MY_JSON_VALUE"
                  key: "database.password"       # Optional: key to extract from a JSON secret
        artifacts: # This section is required to pass secrets to the next step
          - bitbucket-pipes-exports.env

    - step:
        name: Use the Secrets
        script:
          - echo "MY_OUTPUT_NAME=$MY_OUTPUT_NAME"
          - echo "MY_JSON_VALUE=$MY_JSON_VALUE"

```
```yaml Rotated
pipelines:
  default:
    - step:
        name: Fetch Secrets from Akeyless
        script:
          - pipe: akeyless/akeyless-bitbucket-pipe:latest
            variables:
              ACCESS_ID: $ACCESS_ID
              ACCESS_KEY: $ACCESS_KEY
              ROTATED_SECRETS: |
                - name: "/path/to/secret"        # The full path of the secret in Akeyless
                  output-name: "MY_OUTPUT_NAME"  # name of the environment variable to create
                - name: "/path/to/json/secret"
                  output-name: "MY_JSON_VALUE"
                  key: "database.password"       # Optional: key to extract from a JSON secret
        artifacts: # This section is required to pass secrets to the next step
          - bitbucket-pipes-exports.env

    - step:
        name: Use the Secrets
        script:
          - echo "MY_OUTPUT_NAME=$MY_OUTPUT_NAME"
          - echo "MY_JSON_VALUE=$MY_JSON_VALUE"

```

## Working With Certificates

In order to fetch a certificate from your Akeyless account, set the following configuration:

```yaml PKI Certificate
pipelines:
  default:
    - step:
        name: Fetch PKI Certificate from Akeyless
        script:
          - pipe: akeyless/akeyless-bitbucket-pipe:latest
            variables:
              ACCESS_ID: $ACCESS_ID
              ACCESS_KEY: $ACCESS_KEY
              PKI_CERTIFICATES: |
                - name: "/path/to/pki-issuer"        # name of the PKI Certificate Issuer
                  output-name: "MY_SSL_CERT"         # output variable name for the certificate
                  csr-data-base64: "LS0tLS1CRUdJ...=="  # CSR in Base64 format
        artifacts: # This section is required to pass secrets to the next step
          - bitbucket-pipes-exports.env

    - step:
        name: Use the PKI Certificate
        script:
          - echo "The PKI certificate is $MY_SSL_CERT"

```
```yaml SSH Certificate
pipelines:
  default:
    - step:
        name: Fetch SSH Certificate from Akeyless
        script:
          - pipe: akeyless/akeyless-bitbucket-pipe:latest
            variables:
              ACCESS_ID: $ACCESS_ID
              ACCESS_KEY: $ACCESS_KEY
              SSH_CERTIFICATES: |
                - name: "/path/to/ssh-issuer"       # name of the SSH Certificate Issuer
                  output-name: "MY_SSH_CERT"        # output variable name for the certificate
                  cert-username: "root"               # The use the certificate is issued to
                  public-key-data: "ssh-rsa AAAAB..." # The public key to be signed
        artifacts: # This section is required to pass secrets to the next step
          - bitbucket-pipes-exports.env

    - step:
        name: Use the SSH Certificate
        script:
          - echo "The SSH certificate is $MY_SSH_CERT"

```
