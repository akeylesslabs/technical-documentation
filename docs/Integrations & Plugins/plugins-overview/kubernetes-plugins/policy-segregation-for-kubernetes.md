---
title: Policy Segregation for Kubernetes
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
# Overview

When using Akeyless [Kubernetes Authentication](https://docs.akeyless.io/docs/kubernetes-auth), policy segregation of resources can be done based on Kubernetes attributes via Akeyless [RBAC](https://docs.akeyless.io/docs/rbac) using the relevant [sub-claims](https://docs.akeyless.io/docs/sub-claims), such as `namespace` and `pod_name`.

The following guide will demonstrate the usage of namespace segregation.

# Controlling the Capabilities of a Workload

Authorization in Kubernetes is intentionally high level, focused on coarse actions on resources. However, *policies* enable you to limit, by use case, how objects act on the cluster, themselves, and other resources. You can use policies, together with the Akeyless native secrets injector, to support full and flexible segregation.

# Namespace and Pod Segregation

To fully segregate your cluster workloads so that your cluster namespaces/pods have different authorizations for the Akeyless Platform, you can use Akeyless [Kubernetes Auth](https://docs.akeyless.io/docs/kubernetes-auth). 

For each required policy: 

1. Create an authentication method. For details about the authentication methods that are supported for K8s, see [Authentication Methods for K8s](https://docs.akeyless.io/docs/auth-meth-k8s). 

The following example uses a pre-defined Kubernetes Auth method called K8s\_Auth in the K8s folder. Follow this guide to create a [Kubernetes Auth](https://docs.akeyless.io/docs/kubernetes-auth) method.

> 👍 Note
>
> While it is not mandatory to separate the authentication methods and access roles into separate folders, we recommend that you do this to keep things organized.

2. Create a static secret in the Akeyless Platform.\
   For example, the following command creates a static secret called **namespace1** in the **K8s/NameSpaces/Folder/Secrets** folder.

```shell
akeyless create-secret --name K8s/NameSpaces/Folder/Secrets/namespace1  --value MySecret
```

3. Create an access role to provide the authentication method with access to the required secret. For example, the following commands create the **namespace1role** role in the **Role** folder found in **/K8s/NameSpaces/Folder/**, associate the role with the **namespace1auth** authentication method, and grant **read**, **list**, access to the **namespace1** secret in the **Secrets** folder found in **/K8s/NameSpaces/Folder/**. Where on the association specify the desired sub-claims such as `namespace={NAMESPACE}` or `pod_name={NAME}`.

```shell
akeyless create-role --name /K8s/NameSpaces/Folder/Role/namespace1role
```

4. Associate the role with your authentication method and the relevant sub claim, in the following example only pods from `namespace1` will be authorized: 

```shell
akeyless assoc-role-am --role-name /K8s/NameSpaces/Folder/Role/namespace1role --am-name /K8s/NameSpaces/Folder/Auth/namespace1auth --sub-claims namespace=namespace1
```

5. Set the role rule and capabilities: 

```shell
akeyless set-role-rule --role-name /K8s/NameSpaces/Folder/Role/namespace1role --path /K8s/NameSpaces/Folder/Secrets/namespace1 --capability read --capability list
```

The Akeyless webhook validates the Role-based Access Control (RBAC) rule for each namespace.\
If the namespace is authorized, Akeyless searches in the secrets folder you defined for the appropriate secret.

```shell Create your namespace
kubectl create namespace namespace1
```

For example, if we deploy the example below under `namespace1`, and we will try to fetch the `namespace1` secret:

```yaml SegregationForNamespace1.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-secrets
  template:
    metadata:
      labels:
        app: hello-secrets
      annotations:
        akeyless/enabled: "true"
    spec:
      containers:
      - name: alpine
        image: alpine
        command:
          - "sh"
          - "-c"
          - "echo $MY_SECRET && echo going to sleep... && sleep 10000"
        env:
        - name: MY_SECRET
          value: akeyless:K8s/Path/To/NameSpaces/Folder/Secrets/namespace1secret
```

```shell
kubectl apply -f SegregationForNamespace1.yaml -n namespace1
```
