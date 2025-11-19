---
title: Copy of Quick Start
deprecated: false
hidden: true
metadata:
  robots: index
---
This quick start guide is intended to get you started with deploying a Gateway (with Remote Access) using the most basic, required parameters and a clean Kubernetes cluster. Within just a few minutes you will see how easy it is to complete the Gateway deployment and secure your user and machine access. You will also be able to use just-in-time credentials with remote access to log into your various applications and services.

Akeyless Gateway can be deployed on a Kubernetes cluster using the Helm package manager with or without Remote Access. This can also be deployed on Docker using docker-compose, but this guide will focus on K8s.

Akeyless provides a Helm chart to bootstrap the Akeyless Gateway deployment. In K8s deployments, the configuration process takes place before the actual installation.

> 🚧 Security
>
> Please note that this guide was tested with AWS EKS and **not secured** with TLS. We highly suggest you do not use this in a production environment or with real credentials.

# Prerequisites

* [Authentication method](https://docs.akeyless.io/docs/access-and-authentication-methods#/) with permissions to create items in the platform.
* A K8s Cluster
* [Helm](https://helm.sh/) Installed
* [kubectl](https://kubernetes.io/docs/tasks/tools/) installed
* Minimum 1 vCPU available with 2GB RAM per resource
* The following ports need to be open on the cluster:

| Service                                                                                      | Port |
| :------------------------------------------------------------------------------------------- | :--- |
| [Gateway Configuration Manager](https://docs.akeyless.io/docs/gateway-configuration-manager) | 8000 |
| SSH Access                                                                                   | 22   |

# Configuration

The following steps will be used to prepare the environment.

## Create an API Key

In this guide, for simplicity, we will use an [API Key](https://docs.akeyless.io/docs/api-key#/) for the authentication, however, you can use each of the following [auth methods](https://docs.akeyless.io/docs/gateway-chart#/).

To create an API Key, run the following command:

```shell
akeyless auth-method create api-key --name MyFirstKey
```

The output will print the `AccessID` and `AccessKey` of the **API Key**.

## Create an SSH Certificate Issuer

Next, we will create an SSH Certificate Issuer that will be used for SSH access to your resources:

* Create a new [DFC Key](https://docs.akeyless.io/docs/encryption-keys#/):

```shell
akeyless create-dfc-key -n MyRSAKey -a RSA2048
```

2. Create the **SSH Certificate Issuer**:

```shell
akeyless create-ssh-cert-issuer --name MySSHIssuer --signer-key-name MyRSAKey --allowed-users 'ubuntu' --ttl 300
```

> 👍 SSH connection note
>
> This is the bare minimum in order to have a required SSH Certificate Issuer and access the Remote Access Portal. For more details on connecting to a resource via SSH, please see the docs [here](https://docs.akeyless.io/docs/ssh-certificates).

# Gateway Deployment

The following steps will be used in order to deploy the K8s gateway with the Secret Remote Access to resources in your account.

## Helm Chart Configuration

Add the following repository to the Helm repository list:

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
```

Fetch the `values.yaml` file from the Akeyless repository:

```shell
helm show values akeyless/akeyless-gateway > values.yaml
```

Below is an explanation of the minimum required fields by section. Find them in the file and edit them as per the instructions:

```yaml values.yaml
############
## Global ##
############

akeylessGatewayAuth:
  gatewayAccessId: <AccessID>
  gatewayAccessType: access_key
  gatewayCredentialsExistingSecret: access-key
```

`gatewayAccessId`: The `AccessID` of the [API Key](https://docs.akeyless.io/docs/api-key) that was created earlier.

`gatewayAccessType`: The access type, for API Key use `access_key`.

`gatewayCredentialsExistingSecret`: A [K8s Secret](https://kubernetes.io/docs/concepts/configuration/secret/) that contains the value of the `AccessKey` of the API Key, for more information, click [here](https://docs.akeyless.io/docs/gateway-chart#/api-key-authentication).

### Remote Access Section

```yaml values.yaml
######################################################
## Default values for akeyless-secure-remote-access ##
######################################################
sra:
  # Enable secure-remote-access. Valid values: true/false.
  enabled: true
  
    sshConfig:
    replicaCount: 1

    config:
      CAPublicKey: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAPzDVmeABzsGd0lEl9m2fdgmCzOLVmEGcLxNkn..."
```

To configure Remote Access, follow these steps:

`sra`: Set the `enabled` field to `true`. Note that the Remote Access deployment creates two more pods in the cluster, one for **Web** and one for **SSH**.

`CAPublicKey`: For this to work properly, you are also required to provide the matching public key of the key you used to create the SSH Certificate Issuer in Akeyless. More info can be found [here](https://docs.akeyless.io/docs/ssh-certificates). Add the `ssh-rsa` value.

# Installation

To install the [Gateway](https://docs.akeyless.io/docs/gateway-chart#/), run the following command:

```shell
helm install gw akeyless/akeyless-gateway -f values.yaml
```

## Verify the installation

Run `kubectl get pods -w` to check that your pods are in `Running` state and that the Gateway and Remote Access services are available.

Then run `kubectl get services` and look for the `EXTERNAL-IP` of the service starting with `gw`.

<Image align="center" border={false} src="https://files.readme.io/cbcf9b1-Screenshot_2024-08-06_at_10.42.34.png" />

Copy the `EXTERNAL-IP` and paste that into your browser with port `8000/console` (i.e. `http://<Your-Akeyless-GW-URL:8000/console>`). If you get the login page, you have successfully deployed the Gateway.

### Gateway URLs

For the Gateway, you can access the following:

* The Gateway's Internal Console is located at `http://<Your-Akeyless-GW-URL:8000/console>`. The internal console means you are working from inside the Gateway and talking directly with the SaaS. If you are using [https://console.akeyless.io](https://console.akeyless.io), you will not be able to interact with this Gateway as it is not secured with TLS.

### Remote Access URLs

For Remote Access, you can access the following:

* The Remote Access Internal Web Portal is located at `http://<Your-Akeyless-GW-URL:8000>/sra/portal`
* Remote Access can also be accessed using our public URL: [https://zerotrust.akeyless.io](https://zerotrust.akeyless.io). If you are using the public URL for RDP, Web, or similar sessions, you will be required to add your Web URL endpoint: `http://<Your-Akeyless-GW-URL:8000>/sra/web-client`

# Testing Out Remote Access

Here we will lay out the steps to get a SAML user to access the Remote Access Portal.

1. Firstly, you need to make sure you have your SAML application set up, e.g. an **Okta account** set up with the Akeyless application configured. You will also need to retrieve your `Metadata URL` for this.
2. Next, run the following command to create your [SAML ](https://docs.akeyless.io/docs/saml#/)Auth Method and make sure to input your `Kubernetes Service External-IP address`:

```shell
akeyless auth-method create saml --name mySamlAuth --unique-identifier email --idp-metadata-url <your-okta-metadata-url> --allowed-redirect-uri https://console.akeyless.io/login-saml, http://127.0.0.1>:*, http://<EXTERNAL-IP-of-K8s-Service>:*
```

3. Create a role for the **SAML** Auth Method:

```shell
akeyless create-role --name MySamlRole 
```

4. Set access to Items with **List** permissions only:

```shell
akeyless set-role-rule --role-name MySamlRole --path "/*" --capability list
```

5. Set **Secure Remote Access** with Allow Access permissions:

```shell
akeyless set-role-rule --role-name MySamlRole --path "/\*" --rule-type sra-rule --capability allow_access
```

4. Associate your Auth Method to the new rule as follows:

```shell
akeyless assoc-role-am --role-name MySamlRole --am-name MySamlAuth
```

5. Next, open your browser and go to your Remote Access internal endpoint: `http://\<Your-Akeyless-GW-URL:8000>>/sra/portal`
6. Enter your SAML `AccessID` and click **Sign In**, You will be redirected to your SAML service login page to log in and then when you finish that it will redirect you to a page with the various types of resources you have permissions to.

# Next Steps

With a Gateway deployed, you can now test out using just-in-time [dynamic secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) for various applications and services by setting up [Targets](https://docs.akeyless.io/docs/targets). If you are also using Remote Access, you can also set up Remote Access on those Targets and log into those [Resources](https://docs.akeyless.io/docs/supported-resource-types) securely from anywhere by reading the docs [here](https://docs.akeyless.io/docs/remote-access-overview).
