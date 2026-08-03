---
title: Quick Start
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
This quick start guide deploys an [Akeyless Gateway](doc:gateway-overview) with [Secure Remote Access](doc:new-structure-overview) on Kubernetes cluster via CLI commands, all Akeyless commands can be executed via Akeyless console (<Anchor target="_blank" href="https://console.akeyless.io">console.akeyless.io</Anchor>) or <Anchor target="_blank" href="https://docs.akeyless.io/reference">API's</Anchor>.&#x20;

for more deployment model check our \[Choose a deployment model]

## Prerequisites

- Akeyless [CLI installed](doc:cli).
- A Kubernetes Cluster&#x20;
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed context pointing to the Kubernetes Cluster
- [Helm](https://helm.sh/) Installed
- Minimum 1 vCPU available with 2 GB RAM per resource
- The following ports need to be open on the cluster to **internal network access only**:

| Service                                                                          | Port |
| -------------------------------------------------------------------------------- | ---- |
| [Gateway Configuration Manager](https://docs.akeyless.io/docs/configure-gateway) | 8000 |
| SSH Access                                                                       | 22   |

## Create an Authentication Method

This [Authentication Method](doc:access-and-authentication-methods) will be used to authenticate your [Akeyless Gateway ](doc:gateway-overview)to your Akeyless account. <br />For this guide, [API Key](doc:auth-with-api-key) authentication is used for simplicity.

<ApiKeyWarning />

Create an API Key authentication method:

```shell
akeyless auth-method create api-key --name MyFirstAPIKey
```

## Create an Access Role

This [Access Role](doc:rbac) will be used to authorized your Gateway to execute actions in the Akeyless account.

1. Create a new access role:

   ```shell
   akeyless create-role --name MyFirstRole
   ```

2. Set the role with access to all Items under `/path/to/folder/` with Read and List permissions:

   ```shell
   akeyless set-role-rule --role-name MyFirstRole --path "/path/to/folder/\*" --capability read --capability list
   ```

3. Also, set the role with access to Targets:

   ```shell
   akeyless set-role-rule --role-name MyFirstRole --path "/path/to/folder/\*" --rule-type target-rule --capability read --capability list
   ```

4. Associate the [Authentication Method](doc:access-and-authentication-methods) with the Role:

   ```shell
   akeyless assoc-role-am --role-name MyFirstRole --am-name MyFirstAPIKey
   ```

   Now you have an Authentication Method with the right access to deploy the Gateway.

## Create Your SSH Certificate Issuer

In order to create an [SSH Certificates issuer](doc:sra-ssh-certificates), run the following commands:

1. Create a new RSA [DFC](doc:dfc-deep-dive) Key in your Akeyless account:

   ```shell
   akeyless create-dfc-key -n MyRSAKey -a RSA2048
   ```

2. Create the SSH Certificate Issuer:

   ```shell
   akeyless create-ssh-cert-issuer --name your-ssh-cert-issuer-name --signer-key-name MyRSAKey --allowed-users 'ubuntu' --ttl 300
   ```

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  This is the bare minimum required to have an SSH Certificate Issuer and access the Remote Access Portal. For more details on connecting to a resource by way of SSH, please see the docs [here](https://docs.akeyless.io/docs/sra-ssh-certificates).
</Callout>

## Configuration

Add the Akeyless Helm repository and configure your `values.yaml` before deploying the Gateway and Secure Remote Access.

### Add the Akeyless Helm Repo

In order to Add the following repository to your Helm repository list, run the following commands:

1. Add the Akeyless Helm repository to your local Helm client:
   ```shell
   helm repo add akeyless https://akeylesslabs.github.io/helm-charts
   ```
2. Update your local Helm repo cache so it picks up the latest chart version:
   ```shell
   helm repo update
   ```

### Configure the Helm Chart

Below is an explanation of the minimum required fields by section. Find them in the file and edit them as per the instructions:

1. Fetch the Default Values File:<br />
   ```shell
   helm show values akeyless/akeyless-gateway > values.yaml
   ```
2. Configure the Global Section:
   ```yaml values.yaml
   ############
   ## Global ##
   ############

   akeylessGatewayAuth:
     gatewayAccessId: <your_access_id>
     gatewayAccessType: access_key
     gatewayCredentialsExistingSecret: akeyless-auth

   ```
   Where:
   - `gatewayAccessId`: Add your API Key's `Access ID`.
   - `gatewayAccessType`: keep as `access_key` for API Key authentication.
   - `gatewayCredentialsExistingSecret`: References a Kubernetes Secret that stores your API Key's Access Key. create it first by following [API Key Authentication in the Akeyless Gateway chart](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm#api-key-authentication).&#x20;
3. Review the Gateway Section:

   The Gateway section controls the core Gateway deployment and needs no changes for a standard setup. By default it creates two Gateway replicas for high availability, You can customize that by changing the `replicaCount` variable.
4. Configure the Secure Remote Access Section:
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
            CAPublicKey: |
               ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAPzDVmeABzsGd0lEl9m2fdgmCzOLVmEGcLxNkn...
               ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD9SkmW9Ay7YwWQk9o3r6a4qQ7pI2Yw1M...
   ```
   Where:
   - `sra`: Set the `enabled` field to `true`. Note that the Remote Access deployment creates two more pods in the cluster, one for Web and one for SSH.
   - `CAPublicKey`: For this to work properly, you are also required to provide the matching public key of the key you used to create the SSH Certificate Issuer in Akeyless. You can provide one or more CA public keys. More info can be found [here](https://docs.akeyless.io/docs/sra-ssh-certificates). Add each `ssh-rsa` value on a new line.

## Deployment

In order to deploy the Helm chart with `values.yaml` configured and verify the Gateway and Remote Access pods come up correctly, run the following commands:

1. Deploy the Helm Chart:
   ```shell
   helm install quick-start-gw akeyless/akeyless-gateway -f values.yaml
   ```
2. Verify the Deployment:
   ```shell
   kubectl get pods -w
   ```
   Confirm the Gateway and Remote Access pods reach `Running` state
   ```shell
   kubectl get services
   ```
   ```text
   ```
   &#x20;Confirm that the Gateway and Remote Access services are available.

### Retrieve the Gateway URL

In order to retrieve the Gateway URL run the following commands:

1. Get the external IP:
   ```shell
   kubectl get services
   ```
   &#x20;Look for the `EXTERNAL-IP `of the service starting with `quick-start-gw`.
2. Open the Gateway console:<br />Copy the EXTERNAL-IP and open it in your browser on port 8000/console, for example:<br />`http://<Gateway-EXTERNAL-IP>:8000/console`
3. Confirm success:<br />If you see the login page, you've successfully deployed the Gateway.

### Remote Access URLs

For Remote Access, you can access the following:

- The Secure Remote Access Internal Web Portal is located at `http://<Gateway-EXTERNAL-IP>:8000/sra/portal`

- Secure Remote Access can also be accessed using our public URL: `https://zerotrust.akeyless.io`. If you are using the public URL for RDP, Web, or similar sessions, you will be required to add your Web URL endpoint: `http://<Gateway-EXTERNAL-IP>:8000/sra/web-client`

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  This guide deployment is **not secured with TLS**.  <br />If you are using `https://console.akeyless.io`, you will not be able to interact with this Gateway as it is not secured with TLS.<br />We strongly recommend not using this setup in production or with real credentials.

  To configure Gateway with TLS check our [TLS Settings](doc:gateway-tls-settings) doc.
</Callout>
