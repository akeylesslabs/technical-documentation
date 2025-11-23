---
title: SRA Quick Start
deprecated: false
hidden: true
metadata:
  robots: index
---
This guide explains how to deploy the SRA using the most basic configuration. SRA can be deployed either by using an existing gateway or by creating a new one.

In this guide, we will deploy the gateway using a K8s cluster.

# Prerequisites

* An Akeyless Gateway - Either [K8s](https://docs.akeyless.io/docs/gateway-chart#/) or [Docker Compose](https://docs.akeyless.io/docs/gateway-compose#/).
* [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates#/) - With `session_*` allowed user.
* [Helm](https://helm.sh/) installed - Relevant only for K8s.

# Deployment

The following steps including the Gateway deployment, if you already have a running gateway, you can go to the [Remote Access](https://docs.akeyless.io/docs/copy-of-quick-start#/remote-access-configuration) section.

<Callout icon="📘" theme="info">
  ## Note

  When using an existing gateway, verify that the Admin auth method is granted **Read** permission on all items intended for use with SRA.
</Callout>

## Helm Chart Configuration

1. Add the following repository to the Helm repository list:

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
```

2. Fetch the `values.yaml` file from the Akeyless repository:

```shell
helm show values akeyless/akeyless-gateway > values.yaml
```

## Gateway Configuration

Set the Authentication Method (for this example, we will use an [API Key](https://docs.akeyless.io/docs/api-key#/)):

```shell
akeylessGatewayAuth:
  gatewayAccessId: <AccessID>
  gatewayAccessType: access_key
  gatewayCredentialsExistingSecret: access-key
```

Where

* `gatewayAccessId`: The `AccessID` of the API Key.

* `gatewayAccessType`: The `AccessType` of the API Key.

* `gatewayCredentialsExistingSecret`: [K8s secret](https://kubernetes.io/docs/concepts/configuration/secret/) that stores sensitive information (in our case, the `AccessKey`).

```shell
kubectl create secret generic access-key \
  --from-literal=gateway-access-key=<plaintext-Access-Key>
```

## Remote Access Configuration

In order to set your gateway with **Remote Access**, add the following to your deployment:

```shell
sra:
  enabled: true
  
    sshConfig:
    replicaCount: 1

    config:
      CAPublicKey: "<PublicKey>"
```

Where:

* `sra`: set to `enable` in order to deploy the remote access functionality.

* `CAPublicKey`: The Public Key set on the SSH Certificate Issuer.

# Installation

To install the Gateway using the edited `values.yaml` file, run the following command:

```shell
helm install gw akeyless/akeyless-gateway -f values.yaml
```

Once installed, check if the pods are running:

```shell
kubectl get pods
```

Upon successful installation, you will see the **Gateway** pods as well as the **Remote Access** pods, which include the `web` and `ssh` components.

Log in to the Gateway using your browser `http://Your-Akeyless-Gateway-URL:8000` with your Gateway admin credentials, If you get the login page, you have successfully deployed the Gateway.

# Working With SRA

To start working with SRA, open your browser and log in using the following URL:

* `http://<Your-Akeyless-GW-URL:8000>/sra/portal`

You will need to log in with [SAML](https://docs.akeyless.io/docs/saml#/), [OIDC](https://docs.akeyless.io/docs/openid#/) or a [Certificate](https://docs.akeyless.io/docs/certificate-based-authentication#/) authentication method.

Once logged in, you will see the Dynamic Secrets that has the **Secure Remote Access** option enabled, and you will be able to log in to those resources in a secure way using Just In Time credentials.

<br />
