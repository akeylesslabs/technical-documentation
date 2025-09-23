---
title: Ansible HVP Plugin
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
Install the following package: 

```shell
pip install hvac
```

> 👍 Note
>
> Akeyless developed API compatibility with Hashicorp Vault OSS, enabling the use of Vault OSS community plugins for both Static & Dynamic Secrets, you can find more information [here](doc:hashicorp-vault-proxy)

## Create Playbook

In the below example the name of the secret is test. 

```shell
---
# This playbook fetches a secret from Akeyless Platform
- name: Echo
  hosts: all
  tasks:
   - name: Fetching a secret named test from Akeyless Vault
     debug:
      msg: "{{ lookup('hashi_vault', 'secret=secret/data/test:data') }}"
```

Set your Akeyless token in `~/.vault-token` within your Ansible machine, where it can be extracted directly using the `akeyless auth` command:

```shell
VAULT_TOKEN=$(akeyless auth --access-id "Access ID" --access-type="Auth Method type" --json true | awk '/token/ { gsub(/[",]/,"",$2); print $2}' > ~/.vault-token)
```

In the response, you can extract your token. Note that this token will be revoked upon TTL expiration. 

Setting up Akeyless Platform endpoint:

```shell
export VAULT_ADDR=https://hvp.akeyless.io
```

## Run Playbook

To run your playbook simply run the command:

```shell
ansible-playbook -i <hostname>, -u ubuntu secret_fetch.yml
```
