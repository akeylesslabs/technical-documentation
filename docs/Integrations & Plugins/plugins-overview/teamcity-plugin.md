---
title: TeamCity Plugin
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
When performing integration tests and deployments, build scripts need credentials to access external servers and services. The [TeamCity plugin](https://blog.jetbrains.com/teamcity/2017/09/vault/) allows connecting TeamCity to the Akeyless Platform, requesting new credentials when a build starts, passing them to the build script, and revoking them immediately when it finishes.

> 👍 Note
>
> Akeyless developed API compatibility with Hashicorp Vault OSS, enabling the use of Vault OSS community plugins for both Static & Dynamic Secrets, you can find more information [here](doc:hashicorp-vault-proxy)

# Prerequisites

1. A TeamCity server with an authorized BuildAgent. 

2. An [Authentication Methods](doc:access-and-authentication-methods) configured in the Akeyless Platform with access to secrets that will be used by the build agent.

> 📘 Info
>
> Currently, TeamCity plugin supports three authentication methods:
>
> * [AWS IAM](doc:aws-iam)
> * [LDAP](doc:ldap)
> * Akeyless [API Key](doc:api-key)
>
> Ensure that your [Authentication Methods](doc:access-and-authentication-methods) is associated with an [access role](https://docs.akeyless.io/docs/rbac) that has sufficient permissions to access the required secrets.

# Configure The TeamCity Plugin

1. Log in to TeamCity and go to **Administration > Plugins**.

<Image align="center" className="border" width="80%" border={true} src="https://files.readme.io/b6836f5-TC-Plugin-01.png" />

2. Click **Browse plugins repository** to find and download the `HashiCorp Vault` plugin.

<Image align="center" className="border" width="80%" border={true} src="https://files.readme.io/9748a1d-TC-Plugin-02.png" />

3. Then click **Upload plugin ZIP** to install the `Hashicorp Vault` plugin.

<Image align="center" className="border" width="80%" border={true} src="https://files.readme.io/3525c64-TC-Plugin-03.png" />

4. Go to **Administration > Projects** and create a new project.

<Image align="center" className="border" width="80%" border={true} src="https://files.readme.io/55d4b83-TC-Plugin-04.png" />

5. Open the created project and go to the Connections section.

<Image align="center" className="border" width="80%" border={true} src="https://files.readme.io/a0acacb-TC-Plugin-05.png" />

6. Click **Add Connection** to connect your project to the `Vault` plugin.

<Image align="center" className="border" width="80%" border={true} src="https://files.readme.io/6c9b5cd-TC-Plugin-06.png" />

7. Provide connection parameters to the Akeyless Platform in the pop-up window.

<Image align="center" className="border" width="80%" border={true} src="https://files.readme.io/d23f619-TC-Plugin-07.png" />

Where:

* **Vault URL:** Specify your Gateway URL with the HVP port: `https://<Your-Gateway-URL>:8200` or use the public endpoint of Akeyless HVP: `https://hvp.akeyless.io`.

* **Authentication method:** Select the authentication method to use when authenticating with Akeyless. 

Available options: AWS IAM, LDAP, or Akeyless [API Key](doc:api-key) (Vault AppRole).

For example, to use [API Key](doc:api-key) set the following:

* **AppRole Role ID:** Your [API Key](doc:api-key) `Access ID` .

* **AppRole Secret ID**: `Access Key` of the provided `Access ID`.

# Static Secrets

Let's create a static secret first. For that, run the following command:

```shell
akeyless create-secret --name hvp/test --value '{"password":"1234","username":"abcd"}'
```

After that, you need to create an environment variable in your TeamCity project that will be used by build scripts to fetch a secret.

1. Go to the Parameters section to declare a new build parameter which will refer to the Akeyless secret. Currently, these values can be used in the build parameter declaration only and cannot be specified in build steps.

<Image align="center" className="border" width="80%" border={true} src="https://files.readme.io/19f7283-TC-parameters.png" />

2. Click **Add new parameter** and provide the settings in the pop-up window.

<Image align="center" className="border" width="80%" border={true} src="https://files.readme.io/ea40d72-TC-New-Parameter.png" />

Where:

* **Name:** Specify your parameter name (without any prefixes). 

* **Kind:** Select the **Environment variable (env.)** parameter type. This will add an **env.** prefix to the parameter name, but later in the build script, you should specify the name without a prefix.

* **Value:** Provide the full path to your secret in Akeyless using the following format:

Syntax: 

`%vault:secret/PATH!KEY%` where **PATH** is the secret full name, and **KEY** is the specific value inside.

In our example: `%vault:secret/hvp/test!/password%`

Finally, let's create a simple build script using this environment variable and run it:

<Image align="center" className="border" width="80%" border={true} src="https://files.readme.io/359e8ae-TC-GenSettings.png" />

In the Audit Logs screen, you'll see that the script requested and successfully received the `hvp/test` secret value:

<Image align="center" className="border" width="80%" border={true} src="https://files.readme.io/eb25fc4-TC-Results.png" />

# Dynamic Secrets

1. Go to the Parameters section to declare new build parameters for username and password which will refer to the corresponding dynamic secret values.

<Image align="center" className="border" width="80%" border={true} src="https://files.readme.io/c51a015-TC-parameters.png" />

2. Click **Add new parameter** and provide the settings in the pop-up window.

Where:

* **Name:** Specify your parameter name (without any prefixes). 

* **Kind:** Select the **Environment variable (env.)** parameter type. This will add an **env.** prefix to the parameter name, but later in the build script, you should specify the name without a prefix.

* **Value:** Provide the full path to your secret in Akeyless using the following format:

Syntax: 

`%vault:/<dynamic-secret-type>/creds/<path/to/secretname>!/<JSON Entry>%`

In our example: `%vault:/mysql/creds/hvp/mysql!/username%` and `%vault:/mysql/creds/hvp/mysql!/password%` where the dynamic secret name is `/mysql`.

Another example: 

`%vault:azure/creds/<path/to/secretname>!/user.password%`\
`%vault:azure/creds/<path/to/secretname>!/user.userPrincipalName%`

Finally, create a simple build script using this environment variable, and run it:

<Image align="center" className="border" width="80%" border={true} src="https://files.readme.io/fb23889-TC-Dynamic3.png" />