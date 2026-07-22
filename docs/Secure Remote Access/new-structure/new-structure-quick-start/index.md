---
title: Quick Start
---
This quick start guide deploys an [Akeyless Gateway](doc:gateway-overview) with Secure Remote Access on Kubernetes cluster via CLI commands, all Akeyless commands can be executed via Akeyless console or API's.&#x20;

for more deployment model check our \[choosing a deployment model]

## Prerequisites

- An Akeyless account ([Creating an Akeyless Account Quickstart](doc:account-quickstart))
- Akeyless CLI installed. ([Download CLI](doc:cli))
- A Kubernetes Cluster&#x20;
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed context pointing to the Kubernetes Cluster
- [Helm](https://helm.sh/) Installed
- Minimum 1 vCPU available with 2 GB RAM per resource
- The following ports need to be open on the cluster to **internal network access only**:

| Service                                                                          | Port |
| -------------------------------------------------------------------------------- | ---- |
| [Gateway Configuration Manager](https://docs.akeyless.io/docs/configure-gateway) | 8000 |
| SSH Access                                                                       | 22   |

<br />

## Create Authentication Method

This [Authentication Method](doc:access-and-authentication-methods) will be used to authenticate your Akeyless Gateway to your Akeyless account. <br />For this guide, API key authentication is used for simplicity.

<ApiKeyWarning />

Create an API Key authentication method:

```shell
akeyless auth-method create api-key --name MyFirstAPIKey
```

## Create Access Role

This Access Role will be used to authorized your Gateway to execute actions in the Akeyless account.

1. Create a new access role:

   ```shell
   akeyless create-role --name MyFirstRole
   ```

2. Set the role with access to all Items under /path/to/folder/ with Read and List permissions:

   ```shell
   akeyless set-role-rule --role-name MyFirstRole --path "/path/to/folder/\*" --capability read --capability list
   ```

3. Also, set the role with access to Targets:

   ```shell
   akeyless set-role-rule --role-name MyFirstRole --path "/path/to/folder/\*" --rule-type target-rule --capability read --capability list
   ```

4. Associate the Authentication Method with the Role:

   ```shell
   akeyless assoc-role-am --role-name MyFirstRole --am-name MyFirstAPIKey
   ```

Now you have an Authentication Method with the right access to deploy the Gateway.

## Create Your SSH Certificate Issuer

Follow the below commands:

1. Create a new RSA DFC Key in your Akeyless account:

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

### Add the Akeyless Helm Repo

Add the following repository to your Helm repository list:

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
```

### Configure the Helm Chart

Fetch the Helm chart from helm repo:

```shell
helm show values akeyless/akeyless-gateway > values.yaml
```

Below is an explanation of the minimum required fields by section. Find them in the file and edit them as per the instructions.

#### Global Section

```yaml values.yaml
############
## Global ##
############

akeylessGatewayAuth:
  gatewayAccessId: <your_access_id>
  gatewayAccessType: access_key
  gatewayCredentialsExistingSecret: akeyless-auth

```

`gatewayAccessId`: here we will use the [API Key](https://docs.akeyless.io/docs/auth-with-api-key) authentication method we created. Add your API Key's `Access ID`.

`gatewayAccessType`: This is already set to `access_key` for API Key authentication.

`gatewayCredentialsExistingSecret`: The value is already set to `akeyless-auth`. A Kubernetes Secret is **required** for the deployment. To create this, follow the steps described in [API Key Authentication in the Akeyless Gateway chart](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm#api-key-authentication).

#### Gateway Section

There is no need to change anything here. Note that the Gateway deployment creates two pods (replicas) in the cluster by default. You can customize that by changing the `replicaCount` variable.

#### Remote Access Section

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

To configure Remote Access, follow these steps:

`sra`: Set the `enabled` field to `true`. Note that the Remote Access deployment creates two more pods in the cluster, one for Web and one for SSH.

`CAPublicKey`: For this to work properly, you are also required to provide the matching public key of the key you used to create the SSH Certificate Issuer in Akeyless. You can provide one or more CA public keys. More info can be found [here](https://docs.akeyless.io/docs/sra-ssh-certificates). Add each `ssh-rsa` value on a new line.

## Deployment

### Deploy the Helm Chart

Once you have finished those steps, run the following command to create your deployment:

```shell
helm install quick-start-gw akeyless/akeyless-gateway -f values.yaml
```

### Verify Deployment Success

Run `kubectl get pods -w` to check that your pods are in `Running` state and that the Gateway and Remote Access services are available.<br /><br />צריך להוסיף תמונה של איך אמור להיראות&#x20;

#### Gateway URL

run `kubectl get services` and look for the `EXTERNAL-IP` of the service starting with `quick-start-gw`. Copy the `EXTERNAL-IP` and paste that into your browser with port 8000/console (for example, `http://<Your-Akeyless-GW-URL>:8000/console`). If you get the login page, you have successfully deployed the Gateway!

####

#### Remote Access URLs

For Remote Access, you can access the following:

- The Remote Access Internal Web Portal is located at `http://<Your-Akeyless-GW-URL>:8000/sra/portal`

- Remote Access can also be accessed using our public URL: `https://zerotrust.akeyless.io`. If you are using the public URL for RDP, Web, or similar sessions, you will be required to add your Web URL endpoint: `http://<Your-Akeyless-GW-URL>:8000/sra/web-client`<br />

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  This guide deployment is **not secured with TLS**.  <br />If you are using `https://console.akeyless.io`, you will not be able to interact with this Gateway as it is not secured with TLS.<br />We strongly recommend not using this setup in production or with real credentials.

  To configure Gateway with TLS check our [TLS Settings](doc:gateway-tls-settings) doc.
</Callout>

<br />
