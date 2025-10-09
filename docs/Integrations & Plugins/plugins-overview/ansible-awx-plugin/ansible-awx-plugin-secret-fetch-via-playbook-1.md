---
title: Ansible AWX Plugin
excerpt: using Ansible AWX with Akeyless Platform for storing credentials.
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
This article uses the **Vault Secret Lookup** plugin for Ansible AWX.

There are two main parameters used to configure the connection to Akeyless - the **URL**, and a **Token** for access. 

The lookup plugin uses these via the environment variables `VAULT_ADDR` and `VAULT_TOKEN`.

> 👍 Note
>
> Akeyless developed API compatibility with Hashicorp Vault OSS, enabling the use of Vault OSS community plugins for both Static & Dynamic Secrets, you can find more information [here](https://docs.akeyless.io/docs/hashicorp-vault-proxy)

## Prepare AWX Environment

Clone the latest stable version of the project and check all the dependencies as mentioned in the [getting started ](https://github.com/ansible/awx/blob/17.0.1/INSTALL.md#getting-started)section: 

```shell
git clone -b <x.y.z> https://github.com/ansible/awx.git
```

Choose the desired [deployment platform](https://github.com/ansible/awx/blob/17.0.1/INSTALL.md#docker-compose), the following guide will describe the use of Docker Compose: 

```shell
sudo mkdir /root/.awx/awxcompose
sudo ansible-playbook -i inventory install.yml
```

## Configure Akeyless Platfrom Settings

On AWX UI, navigate to **Resources** and create new **Credentials**.  Select HashiCorp Vault Secret Lookup as your **Credentials Type** and set the **SERVER URL** to `https://hvp.akeyless.io` or work directly with your [Gateway](https://docs.akeyless.io/docs/api-gw) URL on port `8200`:

You can either use Akelyess [API Key](https://docs.akeyless.io/docs/api-key) in the following format as your **Token**:

A concatenation of your `Access ID` and your `Access Key` with two dots as a delimiter i.e.: `< Access ID >..< Access Key >`.

Alternatively, to extract your authorization tokens directly using the [Akelyess CLI](https://docs.akeyless.io/docs/cli) `auth` command as part of your workflow variables : 

```shell
VAULT_TOKEN=$(akeyless auth --access-id "Access ID" --access-type="Auth Method type" --json true | awk '/token/ { gsub(/[",]/,"",$2); print $2}')
```

![](https://files.readme.io/9e55048-ansible1.png "ansible1.png")

To fetch a secret from the Akeyless platform, for example, for AWX Tower credentials that will be used to establish a remote connection to an AWX node, create a new **Credentials**  and set the **Credentials Type** as **Ansible Tower**:

![](https://files.readme.io/714572a-Ansible3.png "Ansible3.png")

You can now select to populate the Username and Password fields from an external Secret Management system.

![](https://files.readme.io/55c1fee-ansible_2.png "ansible 2.png")

## Static Secrets

To work with Static secrets, the Path to Secret should be in this format for **KV 1**: 

`secret/data/<Full Secret Name>`, where the Key Name in the returned JSON name is `data`. 

For example, let's create a secret:

```shell
akeyless create-secret -n /DevOps/Ansible -v 'AkeylessIsGr8'
```

The **Key name** should be set to `data` and the **Path** is `secret/data/DevOps/Ansible`.

![](https://files.readme.io/2958df1-ansible5.png "ansible5.png")

In case the secret value itself is a JSON-structured object, the **Path** must be in the following format:

 `secret/<Full Secret Name>`, without the `data/` prefix, you can use the internal JSON keys as the **Key Names** for example, let's create a secret that contains a JSON-structured value:

```shell
akeyless create-secret -n /DevOps/AnsibleJson -v '{"username":"john","password":"secret"}'
```

The **Key names** can be: `username` and `password` where the **Path** is `secret/DevOps/AnsibleJson` 

![](https://files.readme.io/4ce297c-Ansible6.png "Ansible6.png")

To work with **KV 2** use the following format: 

To fetch the secret **/DevOps/Ansible** :

 The **Path** is `secret/DevOps/Ansible`, where the Key in the returned JSON name is `DevOps/Ansible` without the `/` prefix.

![](https://files.readme.io/486bb56-Ansible7.png "Ansible7.png")

For example, to fetch the secret **/DevOps/AnsibleJson** :

The **Path** should be `secret/DevOps/AnsibleJson`, and the **Key name** should be set with the relevant JSON keys. 

## Dynamic Secrets

To use your Ansible Plugin to fetch Dynamic Secrets: 

The **Path** should be in the following format: `<Dynamic Secret type>/creds/<Full Secret Name>`

The returned JSON object will have keys named `password` and `username`.e.g. 

```json
{
  "password": "BbDUelj%Z1~UH1YS",
  "username": "tmp_ProdDB_p-csdsffer"
}
```

In this example, we are fetching a dynamic secret named **/databases/Mysql** using [MySQL Dynamic Secrets](https://docs.akeyless.io/docs/create-dynamic-secret-to-sql-db). 

![](https://files.readme.io/c79f90c-AnsibleDynamicSecret.png "AnsibleDynamicSecret.png")
