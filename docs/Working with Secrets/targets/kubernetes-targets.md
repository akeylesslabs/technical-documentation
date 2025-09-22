---
title: Kubernetes Targets
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
You can define Kubernetes (K8s) targets to be used with dynamic secrets for the following supported K8s types:

- [Elastic Kubernetes Service (EKS)](https://docs.akeyless.io/docs/kubernetes-targets#eks)
- [Google Kubernetes Engine (GKE)](https://docs.akeyless.io/docs/kubernetes-targets#gke)
- [Kubernetes (K8S) Generic](https://docs.akeyless.io/docs/kubernetes-targets#k8s-generic)

# EKS

You can define an EKS target to be used with [EKS Dynamic Secrets](https://docs.akeyless.io/docs/eks-dynamic-secret-producer).

## Create an EKS Target in the CLI

To create an EKS target from the CLI, run the following command:

```shell Akeyless CLI
akeyless target create eks \
--name <Target name> \
--eks-cluster-name <EKS cluster name> \
--eks-cluster-endpoint <EKS cluster endpoint> \
--eks-cluster-ca-cert <EKS cluster base64-encoded certificate>
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

- `eks-cluster-name`: The EKS cluster name.

- `eks-cluster-endpoint`: The EKS cluster endpoint. 

- `eks-cluster-ca-cert`: The EKS cluster base64-encoded certificate.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorblueeksp) section.

## Create an EKS Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Kubernetes (EKS)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.  
   For more information, [read here](doc:implement-zero-knowledge).

4. Choose your preferred authentication mode by selecting one of the options:

- Check the **Use Credentials** radio button to authenticate with the EKS admin user credentials.
- Check the **Use Gateway's Cloud Identity** radio button to authenticate with the Gateway's Cloud IAM.

> 👍 Note
> 
> For example, when you set up a [Dynamic Secret](https://docs.akeyless.io/docs/eks-dynamic-secret-producer), you must select the Target and the Gateway through which temporary users will be created on a target server.
> 
> The **Use Gateway's Cloud Identity** parameter of the Target instructs the Akeyless SaaS to use the IAM credentials of the selected Gateway for authentication with EKS.

5. Define the remaining parameters as follows:

- **Access Key ID:** If you selected the **Use Credentials** option in the previous step, specify the Access ID assigned to the admin user you created to authenticate Akeyless with the EKS cluster. 

- **Secret Access Key:** Specify the Access Key assigned to the admin user you created to authenticate Akeyless with the EKS cluster.

- **Region:** Enter the EKS region that the temporary credentials are permitted to access.

- **EKS Cluster Name:** The cluster name.

- **EKS Cluster URL Endpoint:** The URL of the cluster.

- **EKS Cluster CA Certificate:** A base64-encoded cluster CA certificate.

6. Click **Finish**.

# GKE

You can define a GKE target to be used with [GKE dynamic secrets](https://docs.akeyless.io/docs/gke-dynamic-secret-producer).

## Create a GKE Target in the CLI

To create a GKE target from the CLI, run the following command:

```shell
akeyless target create gke \
--name <Target name> \
--gke-account-email <GKE service account email> \
--gke-cluster-endpoint <GKE cluster endpoint> \
--gke-cluster-ca-cert <GKE Base64-encoded cluster CA certificate> \
--gke-account-key <GKE service account private key> \
--gke-cluster-name <GKE cluster name>
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

- `gke-cluster-name`: The name of the GKE cluster you want to connect to.

- `gke-cluster-ca-cert`: Base64-encoded GKE cluster CA certificate.

- `gke-cluster-endpoint`: GKE Cluster endpoint URL.

- `gke-account-email`: GKE service account email.

- `gke-account-key`: The **Private key** generated for this GKE service account (the value of the "private_key" field from the service-account's downloaded key `JSON` file. **Make sure** to replace all its escaped new-lines, `\\n`, with actual new lines).

> 👍 Tip
> 
> Use this command to extract the private key value from your file:
> 
> ` jq -r '.private_key | gsub("\\\\n"; "\\n")' /path/to/your/file.json`

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorbluegkep) section.

## Create a GKE Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Kubernetes (GKE)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.  
   For more information, [read here](doc:implement-zero-knowledge).

4. Choose your preferred authentication mode by selecting one of the options:

- Check the **Use Credentials** radio button to authenticate with the GKE admin user credentials.
- Check the **Use Gateway's Cloud Identity** radio button to authenticate with the Gateway's Cloud IAM.

> 👍 Note
> 
> For example, when you set up a [Dynamic Secret](https://docs.akeyless.io/docs/gke-dynamic-secret-producer), you must select the Target and the Gateway through which temporary users will be created on a target server.
> 
> The **Use Gateway's Cloud Identity** parameter of the Target instructs the Akeyless SaaS to use the IAM credentials of the selected Gateway for authentication with GKE.

5. Define the remaining parameters as follows:

- **GKE Service Account Email:** If you selected the **Use Credentials** option in the previous step, specify the email of the service account ([service_account@something.iam.gserviceaccount.com](mailto:service_account@something.iam.gserviceaccount.com)).

- **GKE Service Account Key:** Provide the RSA private key generated for this service account to access. This must be a proper PEM encoded PKCS1 or PKCS8 private key. (available under the "private_key" field within the service-account's downloaded key json-file from GCP IAM. **Make sure** to replace all its escaped new-lines, \\n, with actual new lines to avoid parsing errors)

- **GKE Cluster CA Certificate:** Provide a base64-encoded cluster CA certificate.

- **GKE Cluster URL Endpoint:** Specify the URL of the cluster.

- **GKE Cluster Name:** The GKE cluster name. If no value is configured, the default name will be used: `gks-cluster-<service account name>`.

6. Click **Finish**.

# K8S Generic

You can define a generic K8s target to be used with [Generic Kubernetes dynamic secrets](https://docs.akeyless.io/docs/k8s-generic-dynamic-secrets) using a **Bearer Token**, **Client Certificate** or using your **GW Service Account** to extract the relevant settings from a Gateway that runs on a K8s cluster.

In both cases of **Bearer Token** and **GW Service Account**, the Service Account **must** have a **K8s role** with permissions as described in the [Generic K8s](https://docs.akeyless.io/docs/k8s-generic-dynamic-secrets#prerequisites) guide.

> 📘 Note
> 
> K8s Client Certificate is not supported by EKS

## Create a Generic K8s Target in the CLI

To create a generic Kubernetes target from the CLI, run the following command to create a Taregt using a ** Token** or using **certificate**:

```shell Inline connection with token
akeyless target create k8s \
--name <Target name> \
--k8s-cluster-endpoint <K8S Cluster endpoint> \
--k8s-cluster-ca-cert <K8S Cluster certificate> \
--k8s-cluster-token <K8S Cluster authentication token>
```
```shell Inline connection with certificate
akeyless target create k8s \
--name <Target name> \
--k8s-cluster-endpoint <K8S Cluster endpoint> \
--k8s-cluster-ca-cert <K8S Cluster certificate> \
--k8s-auth-type certificate
--k8s-client-certificate <base64 PEM encoded client cert>
--k8s-client-key <base64 PEM encoded client key>
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

- `k8s-cluster-endpoint`: The DNS or IP address of the cluster, in `https://` format.

- `k8s-cluster-ca-cert`: The Base-64 encoded cluster CA certificate.

- `k8s-cluster-token`: A JWT authentication token authorized to create service account tokens.

- `k8s-auth-type`: K8s auth type, either **token** (default) or **certificate**.

- `k8s-client-certificate`: K8s client certificate (PEM format) in base64, relevant only for **k8s-auth-type=certificate**.

- `k8s-client-key`: K8s client private key (PEM format) in base64, relevant only for **k8s-auth-type=certificate**

Or using your [Gateway](doc:gateway-k8s) **Service Account**:

```shell Gateway Service Account
akeyless target create k8s \
--name <Target name> \
--use-gw-service-account 
 --k8s-cluster-endpoint <K8S Cluster endpoint> 
```

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorbluek8sp) section.

## Create a Generic K8s Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Kubernetes (Generic)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.  
   For more information, [read here](doc:implement-zero-knowledge).

4. Define the remaining parameters as follows for any selected option:

   1. **Bearer Token**

      - **Bearer Token:** Provide a JWT authentication token authorized to manage ServiceAccount tokens, Roles, and Role Binding, depending on the working mode.

      - **Cluster CA Certificate:** Provide the K8s cluster CA certificate (PEM format)

      - **Cluster Endpoint URL:** Specify the URL of the cluster.

      - **Cluster Name:** Optional. Set the K8s cluster name.
   2. ** Client Certificate**
      - **Client Certificate:** Provide the K8s client certificate (PEM format).
      - **Client Private Key :** Provide the K8s client private key (PEM format).
      - **Cluster CA Certificate:** Provide the K8s cluster CA certificate (PEM format).
      - **Cluster Endpoint URL:** Specify the URL of the cluster.
      - **Cluster Name:** Optional. Set the K8s cluster name.
   3. ** GW Service Account** to extract the connection settings from a  **Gateway** that is running on a **K8s** cluster, with a ServiceAccount with permissions as described in the [prerequisites](https://docs.akeyless.io/docs/k8s-generic-dynamic-secrets#prerequisites) section of this page. 
      - **Cluster Name: ** Optional. Set the K8s cluster name.
      - **Cluster Endpoint URL:** Specify the URL of the cluster.

5. Click **Finish**.