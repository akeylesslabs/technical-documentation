---
title: K8s External Secrets
excerpt: Kubernetes (K8s) External Secrets
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
> 🚧 Warning
>
> The [Kubernetes External Secrets](https://github.com/external-secrets/kubernetes-external-secrets) project has been **deprecated**.\
> It is recommended to use the [External Secrets Operator (ESO)](https://docs.akeyless.io/docs/external-secret-operator) instead.\
> (see official Git: [https://github.com/external-secrets/external-secrets](https://github.com/external-secrets/external-secrets))

[Kubernetes External Secrets](https://github.com/external-secrets/kubernetes-external-secrets) enable you to use external secret management systems, such as the Akeyless Platform, to securely add secrets in Kubernetes.

> 👍 Note
>
> **External Secrets Operator (ESO)**\
> Check out Akeyless official [Provider](https://external-secrets.io/v0.7.0-rc1/provider/akeyless/) of [External Secret project](https://external-secrets.io/v0.7.0-rc1/)

Complete the following steps to allow Akeyless to add secrets in Kubernetes.

1. Add the K8s external secrets repository:

```shell
helm repo add external-secrets https://external-secrets.github.io/kubernetes-external-secrets/
```

2. Modify the access credential values in the **charts/kubernetes-external-secrets/values.yaml** file.

```yaml
#Akeyless rest-v2 endpoint 
AKEYLESS_API_ENDPOINT: https://api.akeyless.io 
AKEYLESS_ACCESS_ID:
#AKEYLESS_ACCESS_TYPE can be one of the following: k8s/aws_iam/azure_ad/gcp/api_key
AKEYLESS_ACCESS_TYPE:
#AKEYLESS_ACCESS_TYPE_PARAM can be one of the following: gcp-audience/azure-obj-id/access-key
AKEYLESS_ACCESS_TYPE_PARAM:
```

> 👍 Note
>
> * Ensure that an Access Role is defined in Akeyless for the credentials you specify, and that the Access Role is associated with an Authentication Method that allows access to the required secret.
>
> * If you use a customer fragment, define the value of `AKEYLESS_API_ENDPOINT` as the URL of your Akeyless Gateway in the following format: **https\:/your.akeyless.gw:8080/v2**.
>
> * If you define the value of `AKEYLESS_ACCESS_TYPE` as **api\_key**, define the\
>    value of  `AKEYLESS_ACCESS_TYPE_PARAM` as your access key.

3. Deploy the helm chart by running:

```shell
helm install <RELEASE NAME> external-secrets/kubernetes-external-secrets -f charts/kubernetes-external-secrets/values.yaml
```

> 👍 Note
>
> Define the value of `data.key` as the path to the required secret in Akeyless.

4. Create an **ExternalSecret.yaml** file using the following format:

```yaml ExternalSecretExample.yaml:
apiVersion: 'kubernetes-client.io/v1'
kind: ExternalSecret
metadata:
  name: hello-secret
spec:
  backendType: akeyless
  data:
    - key: </Path/To/Your/Secret>
      name: creds
```

5. Apply the **ExternalSecret.yaml** resource by running:

```shell
kubectl apply -f ExternalSecret.yaml
```

6. Retrieve your secret value by running: 

```shell
kubectl get secret hello-secret -o=yaml
```
