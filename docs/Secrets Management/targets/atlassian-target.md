---
title: Atlassian Target
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
You can define an Atlassian target that holds the credential of one [Atlassian](https://www.atlassian.com/) site, Jira and Confluence, on Atlassian Cloud or Data Center. The target is used by the Atlassian Scanner of [Identity and Secrets Intelligence](https://docs.akeyless.io/docs/identity-and-secrets-intelligence), which inspects the Jira projects, Confluence spaces, and site settings of the site for hardcoded credentials.

The target stores the site URL and one read-only credential:

* **Atlassian Cloud**: a user API token paired with the email of the account that created it. The site URL is `https://<site>.atlassian.net`.

* **Data Center**: a personal access token (PAT). No email is needed. The site URL is the base URL of the instance, including a context path if one is configured, for example `https://jira.<company>.example/jira`.

The URL must use `https`. A URL that carries a user name, a token, a query string, or a fragment is rejected.

## Prerequisites on the Atlassian Side

* **Atlassian Cloud**: create an API token for the scanning account from [Atlassian account settings](https://id.atlassian.com/manage-profile/security/api-tokens) under **Security** > **API tokens**. Note the email address of that account. Cloud API tokens expire after one to 365 days; create a new token and update the target before it expires.

* **Data Center**: create a personal access token for the scanning account from the account **Profile** > **Personal Access Tokens** page of the Jira or Confluence instance.

* **Permissions**: the scan sees exactly what the account behind the token sees. For full coverage, make the account a Jira administrator and a Confluence administrator (on Data Center, a member of `jira-administrators` and `confluence-administrators`). A narrower account still works; the surfaces it cannot reach are reported as permission gaps on the scan.

* **Automation rules (optional)**: the Jira Automation REST API does not accept an account API token. To let the scan read the automation rules, create an Automation API key under **Jira settings** > **System** > **Automation** > **API keys** and store it in the target as the automation key. Without it, the automation rules are reported as not read.

## Create an Atlassian Target with the CLI

To create an Atlassian target with the CLI, run the following command:

```shell Atlassian Cloud
akeyless target create atlassian \
--name <target name> \
--atlassian-url https://<site>.atlassian.net \
--atlassian-email <account email> \
--atlassian-token <API token>
```
```shell Data Center
akeyless target create atlassian \
--name <target name> \
--atlassian-url https://jira.<company>.example/jira \
--atlassian-token <personal access token>
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `atlassian-url`: The Atlassian site base URL, `https://<site>.atlassian.net` for Atlassian Cloud or the base URL of a Data Center instance.

* `atlassian-email`: The email of the Atlassian Cloud account paired with the API token. Required for an Atlassian Cloud site, not needed for a Data Center personal access token.

* `atlassian-token`: The Atlassian Cloud API token or the Data Center personal access token.

* `atlassian-automation-key`: Optional. The Jira Automation REST API key that lets the scan read the automation rules.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#atlassian) section.

## Create an Atlassian Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Infra > Atlassian**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

4. Define the remaining parameters as follows:

    * **Site URL:** The Atlassian site base URL, `https://<site>.atlassian.net` or a Data Center base URL.

    * **Account Email:** The email of the Atlassian Cloud account paired with the API token. Leave it empty for a Data Center personal access token.

    * **API Token:** The Atlassian Cloud API token or the Data Center personal access token.

    * **Automation API Key:** Optional. The Jira Automation REST API key.

5. Click **Finish**.

## Create an Atlassian Target with the API

Call the `target-create-atlassian` endpoint, and `target-update-atlassian` to update an existing target. See the [API Reference](https://docs.akeyless.io/reference/targetcreateatlassian) for the full request body.

```shell
curl -X POST https://api.akeyless.io/target-create-atlassian \
  -H 'Content-Type: application/json' \
  -d '{
    "token": "<Akeyless token>",
    "name": "<target name>",
    "atlassian-url": "https://<site>.atlassian.net",
    "atlassian-email": "<account email>",
    "atlassian-token": "<API token>"
  }'
```

## Create an Atlassian Target with Terraform

Use the `akeyless_target_atlassian` resource of the [Akeyless Terraform provider](https://docs.akeyless.io/docs/terraform-provider):

```text
resource "akeyless_target_atlassian" "jira_cloud" {
  name            = "/targets/atlassian/jira-cloud"
  atlassian_url   = "https://<site>.atlassian.net"
  atlassian_email = "<account email>"
  atlassian_token = var.atlassian_api_token
}
```

For a Data Center instance, set `atlassian_url` to the instance base URL, `atlassian_token` to the personal access token, and leave `atlassian_email` unset. The optional `atlassian_automation_key` argument stores the Jira Automation API key.
