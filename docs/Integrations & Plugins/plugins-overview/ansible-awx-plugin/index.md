---
title: ansible-awx-plugin
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
A common usage pattern is the use of a third-party credential management system for managing passwords and keys for accessing hosts and services. In the past, this sort of environment was tricky to manage with Ansible AWX. Now, with the combination of Ansible AWX Custom Credentials, it has become simple.

> ℹ️ **Note (Supported Ansible Version):**
>
> The minimum Ansible version for Akeyless is `2.18.0`

## Choose the right option

Use the following guidance to select the best integration path.

| Option | Best for | Authentication pattern | Secret and certificate operations |
| --- | --- | --- | --- |
| [Ansible Plugin](https://docs.akeyless.io/docs/ansible-plugin) | Teams running playbooks directly with Ansible CLI or automation pipelines that execute native Ansible modules | Direct login in playbooks through `akeyless.secrets_management.login` using supported `access_type` values (including `cert`) | Full module-level workflow, including login, secret retrieval, secret creation, and certificate operations |
| [Ansible AWX Plugin](https://docs.akeyless.io/docs/ansible-awx-plugin-secret-fetch-via-playbook-using-universal-identity) | Teams using AWX or Ansible Automation Platform custom credential workflows | Token-based Vault lookup flow with `VAULT_ADDR` and `VAULT_TOKEN`; token can be generated with API key, Certificate, or other supported auth methods before AWX execution | Optimized for lookup and secret injection into AWX jobs through the Vault Secret Lookup credential type |

## Key differences

1. **Execution model**:
Ansible Plugin runs native Akeyless collection modules inside playbooks. AWX Plugin relies on the AWX Vault Secret Lookup credential flow.
2. **Authentication handling**:
Ansible Plugin performs login inside the playbook. AWX Plugin consumes a pre-generated token in `VAULT_TOKEN`.
3. **Certificate authentication usage**:
Ansible Plugin supports direct certificate login in the playbook. AWX Plugin supports certificate authentication for preflight token generation, then uses that token in the Vault lookup flow.
4. **Operational scope**:
Ansible Plugin is better when jobs need direct Akeyless module actions. AWX Plugin is better when AWX credential management and centralized secret injection are the primary requirements.
