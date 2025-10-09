---
title: Kubectl Access
excerpt: Short-lived certificate for accessing a Kubernetes cluster via kubectl
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Below we will describe how to configure Kubectl to work with short-lived certificates to access a Kubernetes (K8s) cluster using an Akeyless PKI Cert Issuer. The advantage of this approach is that there is no need to manage client certificates. Clients identify to the Akeyless account with one of the available Auth Methods and receive a short-lived certificate that can be used to access the Kubernetes cluster via Kubectl.

## Setup

1. Upload the CA key together with the CA certificate of the Kubernetes cluster into your Akeyless account (in case you are using Minikube they are located in `~/.minikube/ca.key` and `~/.minikube/ca.crt`)

```shell
akeyless upload-rsa --name myK8SCA --alg RSA2048 --rsa-key-file-path ~/.minikube/ca.key --cert ~/.minikube/ca.crt
```

2. Create a new PKI Cert Issuer:

```shell
akeyless create-pki-cert-issuer --name myK8SCertIssuer --signer-key-name myK8SCA --ttl 300 --allowed-domains minikube-user --organizations system:masters
```

To read more about PKI Certificate Issuers, follow this [link.](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) 

In this case, we created an Issuer that will issue a certificate with an expiration time of up to 5 minutes with `system:masters` access permissions. For further reading, check [this page](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation.

3. On the client side, generate a client private key, from which the public key will be extracted (note that this key is useless without a signed certificate)

```shell
openssl genrsa -out /home/user/kubectl-client.key 2048
```

4. On the client side, set the kubeconfig file to work with the Akeyless PKI Cert Issuer in order to fetch the client access certificate as follows:

```yaml
users:
- name: minikube
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      args:
      - get-kube-exec-creds
      - --cert-issuer-name
      - myK8SCertIssuer
      - --key-file-path
      - /home/user/kubectl-client.key
      - --common-name
      - minikube-user
      command: akeyless
```
