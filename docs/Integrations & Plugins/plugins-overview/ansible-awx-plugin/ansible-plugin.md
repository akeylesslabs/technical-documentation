---
title: Ansible Plugin
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
The Akeyless official [plugin for Ansible](https://galaxy.ansible.com/ui/repo/published/akeyless/secrets_management/) provides modules and plugins to securely manage secrets, credentials, and sensitive data within playbooks. It helps maintain efficient and secure automation workflows, allowing teams to simplify secret management while protecting critical information.

You can manage secrets and certificates with either [Modules](https://docs.ansible.com/ansible/latest/plugins/module.html) or [Lookup](https://docs.ansible.com/ansible/latest/plugins/lookup.html) plugins. In this guide, we will use Modules for simplicity. More information about the Lookup plugin can be found [here](https://docs.ansible.com/ansible/latest/plugins/lookup.html)

## Prerequisites

Before using the Akeyless Ansible plugin, ensure the following prerequisites are met:

* Python 3 installed on the Ansible control node.
* Ansible installed.
* For `aws_iam` authentication, install the Akeyless CLI when the playbook must generate `cloud_id` explicitly. For installation steps, see [Akeyless CLI documentation](https://docs.akeyless.io/docs/cli).
* The Akeyless Python package installed:

    ```shell
    pip install akeyless
    ```

* Access to an Akeyless Authentication Method (for example, API Key, AWS IAM, Azure AD, OIDC, or Certificate) with a valid `access_id` and required credentials.
* Network access from the Ansible control node to `https://api.akeyless.io` (or to your Akeyless Gateway endpoint if applicable).

## Installation

To install the Akeyless Ansible plugin, use one of the following methods:

The Akeyless `secrets_management` collection is available on Ansible Galaxy under the Namespace `akeyless`. You can install it using:

```shell
ansible-galaxy collection install akeyless.secrets_management
```

For more information, refer to the [Ansible Galaxy documentation](https://galaxy.ansible.com/ui/repo/published/akeyless/secrets_management/).

> ℹ️ **Note (Version Scope):**
>
> The certificate authentication examples on this page are based on `akeyless.secrets_management` collection version `1.0.0`, where `access_type: cert`, `cert_data`, and `key_data` are available in the code.

## Authentication

This plugin supports the following Authentication Methods:

* [API Key](https://docs.akeyless.io/docs/auth-with-api-key)
* [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws)
* [Azure AD](https://docs.akeyless.io/docs/auth-with-azure)
* [GCP](https://docs.akeyless.io/docs/auth-with-gcp)
* [Email](https://docs.akeyless.io/docs/auth-with-email)
* [Kubernetes](https://docs.akeyless.io/docs/auth-with-kubernetes)
* [OCI IAM](https://docs.akeyless.io/docs/auth-with-oci)
* [LDAP](https://docs.akeyless.io/docs/auth-with-ldap)
* [JWT](https://docs.akeyless.io/docs/auth-with-oauth-jwt)
* [OIDC](https://docs.akeyless.io/docs/auth-with-oidc)
* [SAML](https://docs.akeyless.io/docs/auth-with-saml)
* [Certificate](https://docs.akeyless.io/docs/auth-with-certificate)
* [Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity)

To set the Authentication Method, add the following `login` section to your [Ansible Playbook](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html):

```yaml API Key
login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_id: '<Access ID>'
        access_type: 'api_key'
        access_key: '<Access Key>'
```
```yaml AWS IAM
login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_id: '<Access ID>'
        access_type: 'aws_iam'
        cloud_id: '<cloud_id>'
```
```yaml GCP
login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_id: '<Access ID>'
        access_type: 'gcp'
        cloud_id: '<cloud_id>'
        gcp_audience: <'gcp_audience'>
```
```yaml Azure AD
login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_id: '<Access ID>'
        access_type: 'azure_ad'
        cloud_id: '<cloud_id>'
```
```yaml Email
login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_id: '<Access ID>'
        access_type: 'password'
        admin_password: '<admin_password>'
        admin_email: '<admin_email>'
        account_id: '<account_id>'
```
```yaml Kubernetes
login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_id: '<Access ID>'
        access_type: 'k8s'
        k8s_service_account_token: '<k8s_service_account_token>'
        k8s_auth_config_name: '<k8s_auth_config_name>'
        akeyless_gateway_url: 'https://Your-Akeyless-Gateway-URL:8000'
```
```yaml OCI IAM
login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_id: '<Access ID>'
        access_type: 'oci'
        oci_auth_type: '<oci_auth_type>'
        oci_group_ocid: '<oci_group_ocid>'
```
```yaml LDAP
login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_id: '<Access ID>'
        access_type: 'ldap'
        ldap_username: <'ldap_username'>
        ldap_password: <'ldap_password'>
```
```yaml JWT
login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_id: '<Access ID>'
        access_type: 'jwt'
        jwt: '<jwt value>'
        akeyless_gateway_url: 'https://Your-Akeyless-Gateway-URL:8000'
```
```yaml OIDC
login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_id: '<Access ID>'
        access_type: 'oidc'
        use_remote_browser: 'true / false'
        jwt: '<jwt value>'
        akeyless_gateway_url: 'https://Your-Akeyless-Gateway-URL:8000'
```
```yaml SAML
login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_id: '<Access ID>'
        access_type: 'saml'
        use_remote_browser: 'true | false'
        akeyless_gateway_url: 'https://Your-Akeyless-Gateway-URL:8000'
```
```yaml Certificate
login:
  akeyless_api_url: 'https://api.akeyless.io'
  access_id: '<Access ID>'
  access_type: 'cert'
  cert_data: '{{ lookup("file", "./tls/server-cert.pem") | b64encode }}'
  key_data: '{{ lookup("file", "./tls/server-key.pem") | b64encode }}'
```
```yaml Universal Identity
login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_id: '<Access ID>'
        access_type: 'universal_identity'
        use_remote_browser: 'true | false'
        uid_token: '<uid_token>'
```

### AWS IAM cloud identity for login

In some environments, `akeyless.secrets_management.login` with `access_type: 'aws_iam'` may require an explicit `cloud_id` value.

Generate the value with the Akeyless CLI, then pass it to the `login` task:

```yaml
- name: Generate cloud identity for AWS IAM
  ansible.builtin.command: akeyless get-cloud-identity --cloud-provider aws_iam
  register: aws_identity
  changed_when: false

- name: Login via AWS IAM
  login:
    akeyless_api_url: 'https://api.akeyless.io'
    access_id: '<Access ID>'
    access_type: 'aws_iam'
    cloud_id: '{{ aws_identity.stdout | trim }}'
  register: auth_res
```

> ℹ️ **Note:**
>
> `cloud_id` is the full output from `akeyless get-cloud-identity --cloud-provider aws_iam`.

Where:

* `akeyless_api_url`: Gateway URL API V2 endpoint that is `https://Your_GW_URL:8000/api/v2`.

* `access_id`: The `Access ID` of the Auth Method being used.

* `access_type`: The type of the Auth Method being used.

* `cloud_id`: The `cloud_id` can be retrieved by running `akeyless get-cloud-identity`.

* `cert_data`: Client certificate content encoded in `base64` (required when `access_type` is `cert`).

* `key_data`: Private key content encoded in `base64` (required when `access_type` is `cert`).

* `akeyless_gateway_url`: Akeyless Gateway URL (port `8000`).

## Usage

This section provides examples of fetching secrets and certificates and creating a [Static Secret](https://docs.akeyless.io/docs/static-secrets).

To create an **Ansible Playbook**, create a `yaml` file containing the configuration below.

### Static Secret Example

#### Create a Static Secret

The following will create a [Static Secret](https://docs.akeyless.io/docs/static-secrets) named `'/Ansible/MySecret'`:

```yaml
- name: Create Static Secret
  hosts: localhost
  tasks:
    - name: Get temp token using api_key auth method
      login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_type: 'api_key'
        access_id: '<Access ID>'
        access_key: '<Access Key>'
      register: auth_res

    - name: create static secret item
      create_static_secret:
        akeyless_api_url: 'https://api.akeyless.io'
        name: '/Ansible/MySecret'
        value: "AnsibleSecret"
        token: '{{ auth_res.data.token }}'
      register: response
```

Where:

* `name`: the name of the Static Secret.

* `value`: the value of the Static Secret.

* `type`: The Secret type [`generic` or `password`].

* `format`: The Secret format [`text` | `json` | `key-value`].

Additional parameters for this module can be found in the [official Ansible Repository](https://galaxy.ansible.com/ui/repo/published/akeyless/secrets_management/).

#### Fetch a Static Secret

The following will fetch a [Static Secret](https://docs.akeyless.io/docs/static-secrets) named `/Ansible/MySecret`:

```yaml static_secret.yaml
- name: Get secret value
  hosts: localhost
  tasks:
    - name: Get temp token using api_key auth method
      login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_type: 'api_key'
        access_id: '<Access ID>'
        access_key: '<Access Key>'
      register: auth_res

    - name: Get item secret value by name
      get_static_secret_value:
        akeyless_api_url: 'https://api.akeyless.io'
        names: '/Ansible/MySecret'
        token: '{{ auth_res.data.token }}'
      register: response

    - name: Display the results
      debug:
        msg: "Secret Value: {{ response.data }}"
```

Where:

* `akeyless_api_url`: Gateway URL API V2 endpoint that is `https://Your_GW_URL:8000/api/v2`.

* `names`: The name of the secret.

Additional parameters for this module can be found in the [official Ansible Repository](https://galaxy.ansible.com/ui/repo/published/akeyless/secrets_management/)

### Dynamic Secret Example

The following will fetch a [Dynamic Secret](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) named `Ansible/MyDynamicSecret`:

```yaml dynamic_secret.yaml
- name: Get secret value
  hosts: localhost
  tasks:
    - name: Get temp token using api_key auth method
      login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_type: 'api_key'
        access_id: '<Access ID>'
        access_key: '<Access Key>'
      register: auth_res

    - name: Get item secret value by name
      get_dynamic_secret_value:
        akeyless_api_url: 'https://api.akeyless.io'
        name: '/Ansible/MyDynamicSecret'
        token: '{{ auth_res.data.token }}'
      register: response

    - name: Display the results
      debug:
        msg: "Secret Value: {{ response.data }}"
```

Additional parameters for this module can be found in the [official Ansible Repository](https://galaxy.ansible.com/ui/repo/published/akeyless/secrets_management/)

### Rotated Secret Example

The following will fetch a [Rotated Secret](https://docs.akeyless.io/docs/rotated-secrets) named `Ansible/MyRotatedSecret`:

```yaml rotated_secret.yaml
- name: Get secret value
  hosts: localhost
  tasks:
    - name: Get temp token using api_key auth method
      login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_type: 'api_key'
        access_id: '<Access ID>'
        access_key: '<Access Key>'
      register: auth_res

    - name: Get item secret value by name
      get_rotated_secret_value:
        akeyless_api_url: 'https://api.akeyless.io'
        name: '/Ansible/MyRotatedSecret'
        token: '{{ auth_res.data.token }}'
      register: response

    - name: Display the results
      debug:
        msg: "Secret Value: {{ response.data }}"
```

Additional parameters for this module can be found in the [official Ansible Repository](https://galaxy.ansible.com/ui/repo/published/akeyless/secrets_management/)

### SSH Certificate Example

The following will issue and fetch an SSH Certificate:

```yaml SSH Certificate
- name: Get certificate value
  hosts: localhost
  tasks:
    - name: Get temp token using api-key auth method
      login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_type: 'api_key'
        access_id: '<Access ID>'
        access_key: '<Access Key>'
      register: auth_res

    - name: Get SSH certificate
      get_ssh_certificate:
        akeyless_api_url: 'https://api.akeyless.io'
        cert_issuer_name: "/Ansible/cert_issuer_name"
        cert_username: "<Username>"
        public_key_data: "<public_key_data>"
        token: '{{ auth_res.data.token }}'
      register: result

    - name: Display the RSA key
      debug:
        msg: "{{ result.data.data }}"
```

Where:

* `akeyless_api_url`: Gateway URL API V2 endpoint that is `https://Your_GW_URL:8000/api/v2`.

* `cert_issuer_name`: The name of the **SSH Certificate Issuer**.

* `cert_username`: The username to sign in the SSH certificate.

* `public_key_data`: SSH Public Key.

* `ttl`: **Optional**, Updated certificate lifetime in seconds (must be less than the Certificate Issuer default TTL).

* `legacy_signing_alg_name`: **Optional**, Set this option to output legacy `ssh-rsa-cert-v01@openssh.com` signing algorithm name in the certificate.

### PKI Certificate Example

The following will issue and fetch a PKI certificate:

```yaml PKI Certificate.yaml
- name: Get certificate value
  hosts: localhost
  tasks:
    - name: Get temp token using api_key auth method
      login:
        akeyless_api_url: 'https://api.akeyless.io'
        access_type: 'api_key'
        access_id: '<Access ID>'
        access_key: '<Access Key>'
      register: auth_res

    - name: Get PKI certificate
      get_pki_certificate:
        akeyless_api_url: 'https://api.akeyless.io'
        cert_issuer_name: "/Ansible/pki_issuer_name"
        csr_data_base64: "<csr_data_base64>"
        token: '{{ auth_res.data.token }}'
      register: result

    - name: Display the result of the operation
      debug:
        msg: "{{ result }}"
        
    - name: Display the RSA key
      debug:
        msg: "{{ result.data.data }}"            
```

Where:

* `akeyless_api_url`: Gateway URL API V2 endpoint that is `https://Your_GW_URL:8000/api/v2`.

* `cert_issuer_name`: The name of the **PKI Certificate Issuer**.

* `csr_data_base64`: Certificate Signing Request contents encoded in `base64` to generate the certificate with.

Additional parameters for this module can be found in the [official Ansible Repository](https://galaxy.ansible.com/ui/repo/published/akeyless/secrets_management/).
