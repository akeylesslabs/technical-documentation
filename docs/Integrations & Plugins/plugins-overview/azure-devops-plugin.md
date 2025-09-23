---
title: Azure DevOps Plugin
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
To install this plugin you'll have to add the Vault Interaction task to your organization using this [link](https://marketplace.visualstudio.com/items?itemName=Fizcko.azure-devops-vault-interaction).

# Configuration & Usage

In your project, under Pipelines, select the relevant pipeline and click "Edit".

1. Search for the "Vault - Read KV Secrets" Task, select it and configure it as follows:

Under **Vault Server Settings**: add the following Akeyless host as your Vault URL: `https://hvp.akeyless.io`, to work with your own [Akeyless Gateway](doc:api-gw) set the Vault URL URL of your Gateway HVP endpoint: `https://Your-Gateway-URL:8000/hvp` (or using your gateway url at port 8200)

> 👍 Note
>
> Akeyless developed API compatibility with Hashicorp Vault OSS, enabling the use of Vault OSS community plugins for both Static & Dynamic Secrets, you can find more information [here](doc:hashicorp-vault-proxy)

Under **Authentication Method**: choose **Client Token** and provide the Akeyless token following this format:\
The Token value can be a concatenation of your Access ID and your Access Key for an [API Key](doc:api-key) authentication in the following format: `< Access ID >".."< Access Key >`. And should be used more securely as an environment variable.

Alternatively, to work with any other [Authentication Methods](doc:access-and-authentication-methods) you can extract your token using Akeyless `auth` command: 

```shell
akeyless auth --access-id <Access ID> --access-type <Auth method type>
```

To work with [Static Secrets](doc:static-secrets) edit the following **KV Settings**:

For **KV engine path**, set `secret/data`.  **KV version** should be set to `v1` and **Secret path** should contain your secret full path in Akeyless.\
The final task should look like this:

```shell
- task: VaultReadKV@2
 inputs:
   strUrl: 'https://hvp.akeyless.io'
   ignoreCertificateChecks: true
   strAuthType: 'clientToken'
   strToken: 'access_id..access_key'
   strKVEnginePath: '/secret/data'
   kvVersion: 'v1'
   strSecretPath: '/test'
   strPrefixType: 'custom'
   replaceCR: 'false'
```

After running your pipeline, you’ll see this input in the VaultReadKV step:

![](https://files.readme.io/cbd4b8b-pasted_image_0_3.png "pasted image 0 (3).png")

To fetch [Dynamic Secrets](doc:how-to-create-dynamic-secret) edit the following **KV Settings**:

For **KV engine path** set `mysql/creds`.  **KV version** should be set to `v1` and **Secret path** should contain your secret full path in Akeyless.

The final task should look in this fashion:

```shell
- task: VaultReadKV@2
 inputs:
   strUrl: 'https://hvp.akeyless.io'
   ignoreCertificateChecks: false
   strAuthType: 'clientToken'
   strToken: 'access_id..access_key'
   strKVEnginePath: 'mysql/creds'
   kvVersion: 'v1'
   strSecretPath: '/test'
   strPrefixType: 'custom'
   replaceCR: false
```

Add a script block for using the mysql credentials:

```shell
- script: |
   mysql --host XXXXX --port 3306 --user=$(username) --password='$(password)' -e 'show databases;'
 displayName: 'Show Databases in DB'
```

After running your pipeline, you’ll see this input in Show Databases in DB step:

![](https://files.readme.io/c775c07-Capture222.JPG "Capture222.JPG")
