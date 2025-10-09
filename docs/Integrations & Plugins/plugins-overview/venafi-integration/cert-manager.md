---
title: Venafi Cert Manager
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
Akeyless officially integrates with **Cert Manager**, and this guide demonstrates the integration based on Venafi Dynamic Secret, for a direct integration with Akeyless, follow the main [Cert Manager](https://docs.akeyless.io/docs/kubernetes-cert-manager) guide.

## Using cert-manager with Akeyless and Veanfi Dynamic Secret

You can have [Cert Manager](https://cert-manager.io/docs/) deployed in a cluster and use Akeyless to generate certificates.

To do so, you first need to [install Cert Manager](https://cert-manager.io/docs/installation/) custom resource definitions for your cluster to support using cert-manager.

Once cert-manager is installed and running in your K8s cluster, you’ll need to create the following three K8s objects to work with the dynamic secret:

**Secret** - The credentials to your Akeyless account.

**Issuer** - The name of your Venafi Dynamic secret.

**Certificate(s)** - Certificates created based on your previously created Issuer.

**Authentication**

The following Authentication Methods are supported:

* [K8s Auth](https://docs.akeyless.io/docs/kubernetes-auth)
* [API Key](https://docs.akeyless.io/docs/api-key)

The Secret object allows cert-manager to connect to Akeyless:

```yaml
apiVersion: v1
kind: Secret
type: Opaque
metadata:
  name: my-secret
data:
  token: "<Token>"
```

The token in the Secret object is expected to be a base64 encoding of an API KEY used to access Akeyless in the following format:

```shell
access_id..acces_key | base64
```

> 👍 Note
>
> The API Key token should be a concatenation of your `access_id` and your `access_key` with double dots as a delimiter.
>
> Make sure this [Authentication method](https://akeyless.readme.io/docs/understanding-authentication) is set with the appropriate [RBAC](https://akeyless.readme.io/docs/rbac) in Akeyless, to grant access to your dynamic secret.
> The path in the yaml should always start with the prefix `pki/sign/` prior to the item path in Akeyless

The Issuer object is what allows the cert-manager to call Akeyless with the appropriate dynamic secret.

```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: my-issuer
spec:
  vault:
    path: pki/sign/my-cert-automation-dynamic-secret
    server: http://my-akeyless-gw.example.company.com:8000/hvp # or using 8200 post
    auth:
      tokenSecretRef:
          name: my-secret
          key: token
```

The `my-cert-automation-dynamic secret` under the **path** entry is the full name of the Dynamic Secret in Akeyless.

The **Server** entry sets with the Akeyless Gateway where the Venafi dynamic secret has been created, using port `8200`.

The **tokenSecretRef** key is a reference to the previously created secret for credentials.

Now that these 2 have been created you can start issuing certificate requests to Akeyless.

The **Certificate** object is a certificate request to send to Akeyless.

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: my-certificate
spec:
  commonName: cert-man.example.company.com
  dnsNames:
    - cert-man.example.company.com
  secretName: secret-my-certificate
  issuerRef:
    name: my-issuer
```

The keys are cert-manager related and there are no special keys required by Akeyless at this point. For more information see [here](https://cert-manager.io/docs/concepts/certificate/).

When finished, validate your Certificate has been issued via `kubectl get my-certificate`.

```shell
$ kubectl get my-certificate
NAME             READY   SECRET                  AGE
my-certificate   True    secret-my-certificate   1m
```
