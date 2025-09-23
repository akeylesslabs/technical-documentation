---
title: CircleCI Plugin
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
The Akeyless plugin for CircleCI enables a secure, easy, and integrative way to fetch [Secrets](doc:manage-your-secrets-overview) into [CircleCI](https://circleci.com/docs/pipelines/) pipelines, either integrating the native CircleCI short-lived [OIDC](doc:openid) authentication tokens, or using any other [Authentication Methods](doc:access-and-authentication-methods) with Akeyless native [RBAC](doc:rbac).

# Prerequisites

* A GitHub, GitLab, or Bitbucket project set up in CircleCI

* Permissions to create CircleCI [context](https://circleci.com/docs/contexts/?utm_source=google\&utm_medium=sem\&utm_campaign=sem) that will be used to secure and share environment variables across projects

# Authentication

## OpenID Connect tokens

In CircleCI jobs that use at least one context, the OpenID Connect ID token is available in the environment variable `$CIRCLE_OIDC_TOKEN`. The OpenID Provider is unique to your organization. The URL is `https://oidc.circleci.com/org/ORGANIZATION_ID`, where `ORGANIZATION_ID` is the organization ID (a universally unique identifier) representing your organization.

You can find your CircleCI organization ID by navigating to **Organization Settings > Overview** on the CircleCI web app.

The OpenID Connect ID tokens issued by CircleCI have a fixed audience which is also the organization ID. A full list of available claims can be found [here](https://circleci.com/docs/openid-connect-tokens#format-of-the-openid-connect-id-token), and can be later used for the [Access Roles](doc:rbac) setup.

In Akeyless Platform, create a new [OAuth2.0/JWT](doc:oauth20jwt) Authentication Method with the following settings:

```shell Shell
akeyless create-auth-method-oauth2 --name /Dev/CI/CircleCIAuth \ 
--jwks-uri https://oidc.circleci.com/org/&lt;ORGANIZATION ID&gt;/.well-known/jwks-pub.json \
--unique-identifier iss \
--force-sub-claims
```

Where:

* `--jwks-uri` - The CirclCI OIDC  `JWKS` URL contains the public keys that should be used for JWT verification. Make sure to replace the `ORGANIZATION ID`  with your organization id.

* `--unique-identifier` - A unique claim name that contains details uniquely identifying the request. In the following example, we will use the **CircleCI** OIDC  `iss` claim.

* `--force-sub-claims` - Enforce [Sub-Claims](doc:sub-claims) on role association.

Create a dedicated Access Role. Please note that you will assign it the necessary permissions in a later stage of this guide:

```shell
akeyless create-role --name /Dev/CI/CircleCIRole
```

Associate your new Role with the created Authentication Method, and assign it Sub Claims:

```shell
akeyless assoc-role-am --role-name /Dev/CI/CircleCIRole \
--am-name \Dev\CI\CircleCIAuth \
--sub-claims iss=https://oidc.circleci.com/org/<ORGANIZATION_ID>
```

> 🚧 Warning
>
> **Sub Claims** - It is **mandatory** to add an appropriate [Sub Claim](https://docs.akeyless.io/docs/sub-claims) based on the [claims available in the CircleCI documentation](https://circleci.com/docs/openid-connect-tokens#format-of-the-openid-connect-id-token) to prevent access of unauthorized users. This can also be used to limit access to specific workflows as described on the same CircleCI page under **Additional Claims**.

Grant `Read` and `List` permissions for **Items**:

```shell
akeyless set-role-rule --role-name /Dev/CI/CircleCIRole \
--path /Path/To/your/secret/'*' \
--capability read --capability list
```

# CircleCI Global Configuration

Instead of checking your Auth Method `access Id`, or your [Gateway](doc:api-gw) `URL` into version control, we can store them securely in CircleCI environment variables.

Go to **Project Settings** > **Environment variables** > **Add Environment Variable**

Create an environment variable in CircleCI called `ACCESS_ID` and store your Auth Method's `access-id` in it.

While working with [Zero Knowledge](doc:implement-zero-knowledge) encryption based on your fragment, store your Akeyless Gateway Restful API URL (i.e. port `8080`) in an environment variable named `AKEYLESS_GATEWAY_URL`.

> 👍 Note
>
> **Zero Knowledge** - The Akeyless Gateway should be reachable within your network. Working with your Gateway can be used when running CircleCI with self-hosted runners.

In jobs using a context, CircleCI provides OpenID Connect ID (OIDC) tokens in environment variables. A job can use these tokens to access Akeyless without storing long-lived credentials in CircleCI.

Go to **Organization Settings** > **Contexts** > **Add a context**\
Name it  `akeyless`, we will later add this context to a job by adding the context key to the workflows section of your `circleci/config.yml` file.

# Usage

Open your CircleCI project and create/update your `.circleci/config.yml` file for CircleCI.

```yaml config.yml
# Use the latest 2.1 version of CircleCI pipeline process engine.
# See: https://circleci.com/docs/2.0/configuration-reference
version: 2.1

# Define a job to be invoked later in a workflow.
# See: https://circleci.com/docs/2.0/configuration-reference/#jobs
jobs:
  say-hello:
    docker:
      - image: 'akeyless/ci_base:latest-alpine'
    # Add steps to the job
    # See: https://circleci.com/docs/2.0/configuration-reference/#steps
    steps:
      - checkout
      - run:
          name: "Authenticate To Akeyless"
          command: export TOKEN=$(akeyless auth --access-id $ACCESS_ID --access-type jwt --jwt $CIRCLE_OIDC_TOKEN) >> $BASH_ENV
      - run:
          name: "Fetch Akeyless secrets"
          command: akeyless get-secret-value -n /CI/CircleCI-secret
# Invoke jobs via workflows
# See: https://circleci.com/docs/2.0/configuration-reference/#workflows
workflows:
  say-hello-workflow:
    jobs:
      - say-hello:
          context:
            - akeyless
```

> 👍 Note
>
> It is best practice to use environment variables instead of writing the actual variable values inside the pipeline

![](https://files.readme.io/1329672-Screenshot_2023-03-19_100113.png "Screenshot 2023-03-19 100113.png")

**Success!** - the secrets are accessible to use within the job logic (in this example, they are just being printed).

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/managing-secrets-in-circleci-pipelines" target="_blank" style={{ color: "#00e" }}>Managing Secrets in CircleCI Pipelines</a>.