---
title: Kubernetes External KMS
excerpt: Kubernetes (K8s) External Key Management Service (KMS)
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Kubernetes (K8s) External KMS allows you to use external secret management systems to add secrets in Kubernetes securely.

By default, Secrets are not encrypted at rest and are open to attack, either by way of the `etcd` server or by way of backups of `etcd` data. To mitigate this risk, the Akeyless Platform acts as an external secret management system with a KMS plugin to encrypt Secrets stored in `etcd`.

## Prerequisites

* Kubernetes v1.10 or higher.

* Direct access to Kubernetes control plane.

* `kube-apiserver` must be restarted after the External KMS plugin has been configured and started.

* For `kubernetes-external-secrets` to be able to retrieve your secrets it will need access to your Akeyless Platform by way of Akeyless [RBAC](https://docs.akeyless.io/docs/rbac) associated with an [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods).

* An AES [Encryption Key](https://docs.akeyless.io/docs/encryption-keys) in Akeyless Platform.

## Usage

Kubernetes external KMS plugin can be deployed using a [static pod](https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/) or a standalone Docker container both methods require direct access to the Kubernetes master nodes on the control plane where the `kube-apiserver` is running:

> 👍 Note
>
> `kube-apiserver` communicates with the plugin through a Unix socket,hence a volume must be mounted accordingly where the plugin will create the socket on, and the `kube-apiserver` will send and received requests through it.

## Akeyless Environment Variables

| Name | Value | Default |
| --- | --- | --- |
| `AKEYLESS_URL` | URL of the Akeyless REST API Gateway (port 8081) | [https://api.akeyless.io](https://api.akeyless.io) |
| `AKEYLESS_UNIX_SOCKET` | Path to listen on Unix socket | `/tmp/akeyless_kms_plugin.sock` |
| `AKEYLESS_KEY_ENCRYPTION_KEY` | The key used for encryption (decryption is handled automatically) | N/A |
| `AKEYLESS_ACCESS_ID` | Access ID of the auth method used |  |
| `AKEYLESS_ACCESS_KEY` | Access Key if `access_key` auth method is used |  |
| `AKEYLESS_AZURE_OBJECT_ID` | Azure Object ID if `azure_ad` auth method is used |  |
| `AKEYLESS_GCP_AUDIENCE` | GCP Audience if `gcp` auth method is used | `akeyless.io` |
| `AKEYLESS_UID_INIT_TOKEN` | Universal Identity init token if `universal_identity` auth method is used |  |

## Standalone Docker Container

Run the Docker image **on the same machine as the `kube-apiserver`** with the relevant environment variables, and a mounted volume for the Unix socket.

```shell
docker run -d \
  -e AKEYLESS_KEY_ENCRYPTION_KEY=<path to your encryption key in Akeyless> \
  -e AKEYLESS_ACCESS_ID=<the access id to use for authentication> \
  -v /path/to/shared/vol:/tmp
  --name akeyless-kms-plugin
  akeyless/k8s-akeyless-kms-plugin
```

Check the Docker logs to validate the plugin is running:

```shell
$ docker logs akeyless-kms-plugin
2021/08/24 12:17:01 testing authentication to https://api.akeyless.io
2021/08/24 12:17:01 running authentication
2021/08/24 12:17:02 authentication to https://api.akeyless.io succeeded!
2021/08/24 12:17:02 using <key type here (DFC / Classic)> Key <your key name here> (DisplayId: <your key display id) for encryption
2021/08/24 12:17:02 testing crypto operations with key <your key name here>
2021/08/24 12:17:03 crypto operations with key <your key name here> succeeded!
2021/08/24 12:17:03 listening on Unix socket: /tmp/akeyless_kms_plugin.sock
2021/08/24 12:17:03 Api Version: v1beta1, Runtime Name: AKEYLESS, Runtime Version: 0.0.1
```

## Static Pod

Update the below Static Pod template and run it **on the same machine as the `kube-apiserver`**

```yaml
apiVersion: v1
  kind: Pod
  metadata:
    annotations:
      scheduler.alpha.kubernetes.io/critical-pod: ""
    labels:
      k8s-app: akeyless-encryption-provider
    name: akeyless-encryption-provider
    namespace: kube-system
  spec:
    containers:
    - image: akeyless/k8s-akeyless-kms-plugin
      name: akeyless-encryption-provider
      env:
      - name: AKEYLESS_KEY_ENCRYPTION_KEY
        value: <your encryption key item name>
      - name: AKEYLESS_ACCESS_ID
        value: <the access id to use for authentication>
      volumeMounts:
      - mountPath: /tmp # The location of the Unix socket
        name: akeyless-kms-plugin
    hostNetwork: true
    priorityClassName: system-cluster-critical
    volumes:
    - name: akeyless-kms-plugin
      hostPath:
        path: /path/to/shared/vol
        type: DirectoryOrCreate
```

Check the pod logs to validate the plugin runs successfully:

```shell
$ CONTAINER=$(kubectl get pods -n kube-system | grep akeyless-kms-plugin | head -n 1 | awk '{print $1}')
$ kubectl logs $CONTAINER
2021/08/24 12:43:31 testing authentication to https://api.akeyless.io
2021/08/24 12:43:32 running authentication
2021/08/24 12:43:32 authentication to https://api.akeyless.io succeeded!
2021/08/24 12:43:32 using <key type here (DFC / Classic)> Key <your key name here> (DisplayId: <your key display id) for encryption
2021/08/24 12:43:32 testing crypto operations with key <your key name here>
2021/08/24 12:43:33 crypto operations with key <your key name here> succeeded!
2021/08/24 12:43:33 listening on Unix socket: /tmp/akeyless_kms_plugin.sock
2021/08/24 12:43:34 Api Version: v1beta1, Runtime Name: AKEYLESS, Runtime Version: 0.0.1
```

## Configure `kube-apiserver`

Once the plugin is up and running, the next step is to [configure the kube-apiserver](https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/#encrypting-your-data-with-the-kms-provider).

To do this you will need to use the below `encryption_provider_config.yaml` file.

If you want to change the location of the socket make sure to update the plugin as well as the `encryption_provider_config.yaml` file.

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - kms:
          name: "akeyless"
          endpoint: "unix:///tmp/akeyless_kms_plugin.sock"
          cachesize: 1000
          timeout: 3s
      - identity: {}
```
