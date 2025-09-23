---
title: GitLab Plugin
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
[GitLab](https://www.gitlab.com) is a web-based DevOps lifecycle tool that provides a Git-repository manager including a wiki, issue-tracking, and continuous integration and deployment pipeline features.

The Akeyless plugin for GitLab enables a secure, easy, and integrative way to fetch Secrets into GitLab pipelines.

# Authentication

Each job has a [JSON Web Token (JWT)](https://docs.gitlab.com/ee/ci/secrets/id_token_authentication.html#id-tokens) provided as CI/CD variable named `CI_JOB_JWT_V2` or `ID_TOKEN` on version 16 and higher.

When a pipeline is about to run, GitLab uses the job token and generates a unique token for it.

> 👍 Note
>
> **GitLab v16 and higher** - `CI_JOB_JWT_V2` is replaced by [ID tokens](https://docs.gitlab.com/ee/ci/secrets/id_token_authentication.html#id-tokens) which are the JSON Web Tokens (JWTs) that can be added to a GitLab CI/CD job. For more details please find the relevant config file below.

The token is valid only while the pipeline job runs. After the job finishes, you can’t use the token anymore.

To work with the Akeyless GitLab plugin, we will use an OAuth 2.0 / JWT Authentication Method

### OAuth 2.0 / JWT

In Akeyless Platform, create a new [OAuth 2.0 / JWT](https://docs.akeyless.io/docs/oauth20jwt) Authentication Method with the following parameters:

```shell
akeyless create-auth-method-oauth2 --name /Dev/GitLabAuth \ 
--jwks-uri https://gitlab.com/oauth/discovery/keys \
--unique-identifier user_login
--force-sub-claims
```

Where:

* `--jwks-uri` - The URL to the `JWKS` that contains the public keys that should be used for JWT verification.

* `--unique-identifier` - A unique claim name that contains details uniquely identifying the request. In the following example, we will use the GitLab `user_login` claim.

* `--force-sub-claims` - Enforce [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) on role association.

Create a dedicated Access Role, please note that you will assign it the necessary permissions in a later stage of this guide:

```shell
akeyless create-role --name /Dev/GitLabRole 
```

Associate your new Role with the created Authentication Method, and assign it Sub Claims:

```shell
akeyless assoc-role-am --role-name /Dev/GitLabRole \ 
--am-name /Dev/GitLabAuth \ 
--sub-claims user_login=&lt;YOUR GitLab USERNAME&gt;
```

> 🚧 Warning
>
> **Sub Claims** - It is mandatory to add an appropriate [Sub Claim](https://docs.akeyless.io/docs/sub-claims) based on the [claims available in the GitLab documentation](https://docs.gitlab.com/ee/ci/examples/authenticating-with-hashicorp-vault/) to prevent access of unauthorized users.

Set `Read` and `List` permissions for **Items**:

```shell
akeyless set-role-rule --role-name /Dev/GitLabRole \ 
--path /Path/To/your/secret/'*' \
--capability read --capability list
```

# Usage

Open your GitLab project and make sure you have a `yaml` file named `.gitlab-ci.yml` and update it to contain the following steps while making sure that the path to the relevant secrets, as well as the access-id value with your matching JWT access-id, was replaced.

> 👍 Note
>
> **GitLab Versions and Tokens** - GitLab v15 and above, supports `CI_JOB_JWT_V2`, for older versions you can use the legacy environment `CI_JOB_JWT` instead.
>
> In GitLab v16 and above, `CI_JOB_JWT_V2` is replaced by [ID tokens](https://docs.gitlab.com/ee/ci/secrets/id_token_authentication.html#id-tokens).
>
> The image is `akeyless/ci_base` which is a public docker image based on `ruby:2.4` that contains the Akeyless CLI as well as other essential components.

```yaml .gitlab-ci.yml
variables: 
  ACCESS_ID: &lt;access_id&gt;

akeyless:
  image: 
    name:  akeyless/ci_base:latest-alpine
  before_script:
    - export MY_SECRET=akeyless://path/to/secret # Static / Dynamic secret
    - export TOKEN=$(akeyless auth --access-id $ACCESS_ID --access-type jwt --jwt $CI_JOB_JWT_V2 --json --jq-expression='.token') 
    # script will replace any env var with prefix of "akeyless:" like above
    - source ~/.akeyless/akeyless_env.sh
  script:
    - echo "Fetching Secrets is Easy [$MY_SECRET]"
```

```yaml v16_gitlab-ci.yml
variables:
  ACCESS_ID: &lt;access-id&gt;

akeyless:
  id_tokens:
   FIRST_ID_TOKEN:
    aud: https://gitlab.com
  image:
    name:  akeyless/ci_base:latest-alpine
  before_script:
    - export MY_SECRET=akeyless://gitlab/mySecret
    - export TOKEN=$(akeyless auth --access-id $ACCESS_ID --access-type jwt --jwt $FIRST_ID_TOKEN --json --jq-expression='.token')
    # script will replace any env var with prefix of "akeyless:" like above
    - source ~/.akeyless/akeyless_env.sh
  script:
    - echo "Fetching Secrets is Easy [$MY_SECRET]"
```

Sample output of a successful job:

<Image align="center" src="https://files.readme.io/d82b92c-gitlab-docs.png" />

Success! - the secrets are accessible to use within the job logic (in this example, they are just being printed).

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/managing-secrets-in-gitlab-pipelines" target="_blank" style={{ color: "#00e" }}>Managing Secrets in GitLab Pipelines</a>.