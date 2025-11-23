---
title: Copy of Quick Start
deprecated: false
hidden: true
metadata:
  robots: index
---
This guide will demonstrate the most basic steps required to set up a Gateway with an SRA deployment using K8s.

However, if you already have an existing gateway, you can use it to deploy the SRA by setting the settings in the Remote Access Section.

> 🚧 Security
>
> Please note that this guide was tested with AWS EKS and **not secured** with TLS. We highly suggest you do not use this in a production environment or with real credentials.

# Prerequisites

* [Authentication method](https://docs.akeyless.io/docs/access-and-authentication-methods#/) with permissions to create items in the account.
* [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates#/) with `session_*` allowed user.
* [Helm](https://helm.sh/) Installed
* [kubectl](https://kubernetes.io/docs/tasks/tools/) installed
* Minimum 1 vCPU available with 2GB RAM per resource

> 👍 SSH connection note
>
> This is the bare minimum in order to have a required SSH Certificate Issuer and access the Remote Access Portal. For more details on connecting to a resource via SSH, please see the docs [here](https://docs.akeyless.io/docs/ssh-certificates).

# Gateway Deployment

The following steps will be used in order to deploy the K8s gateway with the **Secret Remote Access**.

For simplicity, we will use an [API Key](https://docs.akeyless.io/docs/api-key#/) auth method. 

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

Where:

* `gatewayAccessId`: The `AccessID` of the auth method with permissions. -- to be fixed by Avi
* `gatewayAccessType`: The **Access Type** of the auth method, in our case, `access_key`
* `gatewayCredentialsExistingSecret`: A [K8s Secret](https://kubernetes.io/docs/concepts/configuration/secret/) that contains the value of the `AccessKey` of the API Key, in order to create the K8s secret, run the following command:

```shell
kubectl create secret generic access-key \
  --from-literal=gateway-access-key=<plaintext-Access-Key>
```

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
      CAPublicKey: "PublicKey"
```

Where:

* `sra`: Set the `enabled` field to `true`. Note that the Remote Access deployment creates two more pods in the cluster, one for **Web** and one for **SSH**.
* `CAPublicKey`: Public key of the Encryption key you used to create the SSH Certificate Issuer in Akeyless. 

# Installation

To install the [Gateway](https://docs.akeyless.io/docs/gateway-chart#/), run the following command:

```shell
helm install gw akeyless/akeyless-gateway -f values.yaml
```

## Verify the installation

Run `kubectl get pods -w` to check that your pods are in `Running` state and that the Gateway and Remote Access services are available.

Then run `kubectl get services` and look for the `EXTERNAL-IP` of the service starting with `gw`.

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
