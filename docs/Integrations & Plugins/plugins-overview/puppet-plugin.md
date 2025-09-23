---
title: Puppet Plugin
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
# Prerequisites

* **Puppet** version 6 or later.
* **Puppet/vault\_lookup** module installed

The **puppet/vault\_lookup** module can be installed by running the following command on your server:

```shell
puppet module install puppet/vault_lookup
```

> 👍 Note
>
> Akeyless developed API compatibility with Hashicorp Vault OSS, enabling the use of Vault OSS community plugins for both Static & Dynamic Secrets, you can find more information [here](doc:hashicorp-vault-proxy)

# Create a sample module

Create `init.pp`  on your Puppet server as follows: 

```shell
$variables = {
 'token' => Deferred('vault_lookup::lookup', 
	['secret/<path/to/secret_name>', 
	{
  		'vault_addr'  => 'https://hvp.akeyless.io',
  		'auth_method' => 'approle',
  		'role_id'     => 'Access ID',
  		'secret_id'   => 'Access Key',
		'approle_path_segment' => 'v1/auth/approle/login',
	}
	])
}

file { '/tmp/secret.txt':
  ensure  => file,
  content => Deferred('inline_epp',
               ['<%= $token.unwrap %>', $variables]),
} 

```

Where: 

* `secret/<path/to/secret_name>`: A full secret name, with `secret` prefix. 
* `vault-addr`: either the public `/8000/hvp` endpoint, or your Gateway URL on port `8200`.
* `role_id`: Set with your [API Key](doc:api-key) auth method AccessID.
* `secret_id`: Set with the matching API Key value. 

The following logic will create a `txt` file with the secret value, where for the sake of simplicity we are running `cat` command to print the value, this should not be used as is in a production environment. 

## Secret fetch

Retrieve the secret at the Puppet agent using the following command:

```shell
puppet agent -t
```
