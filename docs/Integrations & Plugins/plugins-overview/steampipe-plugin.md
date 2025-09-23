---
title: Steampipe Plugin
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
Steampipe is an open source tool to instantly query cloud services with SQL. This integration enables users to query the Akeyless API to view their Akeyless account information in table format using the CLI.

# Prerequisites

* [Steampipe](https://steampipe.io/) installed
* A supported Akeyless [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods)

# Installation

Download and install the latest Akeyless plugin from your terminal. Installing the plugin will create a configuration file at `~/.steampipe/config/akeyless.spc`.

```shell
steampipe plugin install akeyless-community/akeyless
```

# Authentication

The Steampipe plugin supports the following Authentication Methods:

* [JWT](https://docs.akeyless.io/docs/oauth20jwt)
* [AWS IAM](https://docs.akeyless.io/docs/aws-iam)
* [Azure AD](https://docs.akeyless.io/docs/azure-ad)
* [GCP](https://docs.akeyless.io/docs/gcp-auth-method)
* [K8S](https://docs.akeyless.io/docs/kubernetes-auth)
* [Universal Identity](https://docs.akeyless.io/docs/universal-identity)
* [Access Key](https://docs.akeyless.io/docs/api-key)

Edit the `akeyless.spc` file with your chosen Authentication Method. The only required fields are `access_type` and `access_id`:

```Text JWT
connection "akeyless" {
  plugin = "akeyless-community/akeyless"  

  access_type = "jwt"

  access_id = "<your-jwt-auth-access-id>"
  
  jwt = "<your-akeyless-jwt-token>"
```
```YAML AWS IAM
connection "akeyless" {
  plugin = "akeyless-community/akeyless"  

  access_type = "aws_iam"

  access_id = "<your-aws-iam-access-id>"
```
```YAML Azure
connection "akeyless" {
  plugin = "akeyless-community/akeyless"  

  access_type = "azure_ad"

  access_id = "<your-azure-access-id>"
  
  azure_object_id = "<your-azure-object-id>"
```
```YAML GCP
connection "akeyless" {
  plugin = "akeyless-community/akeyless"  

  access_type = "gcp"

  access_id = "<your-gcp-access-id>"
  
  gcp_audience = "<your-gcp-audience>"
```
```YAML K8s
connection "akeyless" {
  plugin = "akeyless-community/akeyless"  

  access_type = "k8s"

  access_id = "<your-k8s-access-id>"
  
  k8s_service_account_token = "<your-k8s-service-acct-token>"

  k8s_auth_config_name = "<your-k8s-auth-config-name>"
  
  api_url = "<your-gw-url>:8081"

  # Optional, when working with a self-signed certifiate. CA certificate for TLS verification of the Akeyless Gateway.
  #gateway_ca_cert = ""
```
```YAML Universal Identity
connection "akeyless" {
  plugin = "akeyless-community/akeyless"  

  access_type = "universal_identity"

  access_id = "<your-uid-access-id>"

  uid_token = "<your-uid-token>"
```
```Text Access Key
connection "akeyless" {
  plugin = "akeyless-community/akeyless"  

  access_type = "api_key"

  access_id = "<your-api-key-access-id>"

  access_key = "<your-api-key-access-key>"
```

## Working with Gateway

For every Authentication Method, you have the option to work directly through your Gateway. To do this, set the `api_url` variable with your Gateway's Rest API V2 endpoint `https://Your-Akeyless-GW-URL:8000/api/v2`. (or use your gateway URL at port `8081`)

When working with a self-signed certificate, you can provide your `gateway_ca_certificate` as well.

# Testing

Run a quick test to ensure the plugin is working. From your terminal run the following:

```shell
steampipe query "select role_name from akeyless_role;"
```

This will show all your `Roles` by `Role Name`.

You can also run `steampipe query` which will open the query shell where you can simply run `select role_name from akeyless_role;`.

> 📘 Note
>
> A query will output only the information your Authentication Method has access to based on its Access Role.

## Examples

You can find more examples on our Steampipe Hub page [here](https://hub.steampipe.io/plugins/akeyless-community/akeyless/tables).

# Tables

The following tables are available for querying.

| Table                    | Description                     |
| ------------------------ | ------------------------------- |
| *akeyless\_auth\_method* | Akeyless Authentication Methods |
| *akeyless\_gateway*      | Akeyless Gateways               |
| *akeyless\_item*         | Akeyless Items                  |
| *akeyless\_role*         | Akeyless Access Roles           |
| *akeyless\_target*       | Akeyless Targets                |
