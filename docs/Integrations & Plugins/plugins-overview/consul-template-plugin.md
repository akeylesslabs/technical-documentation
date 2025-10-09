---
title: Consul Template Plugin
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
Consul Template is a key tool for generating configurations and managing infrastructure. Consul Template is a standalone application that renders data from Consul onto the file system.\
The integration with Akeyless allows users seamlessly to integrate secret data into the configurations.

> 👍 Note
>
> Akeyless developed API compatibility with Hashicorp Vault OSS, enabling the use of Vault OSS community plugins for both Static & Dynamic Secrets, you can find more information [here](https://docs.akeyless.io/docs/hashicorp-vault-proxy)

## Prerequisites

1. Set the Akeyless URL in the `VAULT_ADDR` environment variable:

```shell
export VAULT_ADDR=https://hvp.akeyless.io
```

2. You'll need to configure the authentication token that Consul Template would use to fetch secrets from Akeyless Platform. Set your Akeyless token in a file `~/.vault-token` 

You can either use Akelyess [API Key](https://docs.akeyless.io/docs/api-key) in the following format as your **Token**:\
A concatenation of your `Access ID` and your `Access Key` with two dots as a delimiter: `< Access ID >..< Access Key >`, For example:`p-xxxxx..accessKey`

Alternatively, to extract your authorization tokens directly using the [Akelyess CLI](https://docs.akeyless.io/docs/cli) `auth` command : 

```shell
akeyless auth --access-id "Access ID" --access-type="Auth Method type" --json true | awk '/token/ { gsub(/[",]/,"",$2); print $2}'>> ~/.vault-token
```

## Configuring Consul Template Plugin

1. Create a secret in Akeyless that you can further use in the Consul Template:

```shell
akeyless create-secret --name my-app/production --value '{"your_secret_value":"1234","your_secret_name":"abcd"}'
```

Consul Template's powerful abstraction and templating language are perfect for creating dynamic configurations.

2. Write to a template:

```shell
{{ with secret "secret/data/my-app/production" }}
 		adapter: xyzt 
    xyzt_your_secret_name: {{.Data.data.your_secret_name}}
    xyzt_your_secret_value: {{.Data.data.your_secret_value}}
{{ end }}
```

This example combines the existing functionality of watching a key in Consul and the new function that queries Akeyless Platform for a secret. Consul Template transparently handles the authentication, retrieval, and renewal of secrets. 

3. Execute the template

```shell
consul-template -template="my.tmpl:output.txt" -once -dry
> output.txt

    adapter: xyzt
    your_secret_name: abcd
    your_secret_value: 1234
```

> 📘 Info
>
> **Configuring Consul Template with Akeyless Gateway** - For Zero-Knowledge please configure [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) and set `VAULT_ADDR` to your private Akeyless Gateway:\
> `export VAULT_ADDR=https://Your-Akeyless-Gateway:8200`
