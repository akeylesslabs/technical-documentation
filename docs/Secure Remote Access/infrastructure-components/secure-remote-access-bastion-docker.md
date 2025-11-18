---
title: Secure Remote Access Bastion on Docker
excerpt: Docker Setup
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
> 📘 Legacy Chart
>
> This guide describe the flow using the **Legacy** chart of the Akeyless Secure Remote Access.
>
> A new and updated chart is soon to be released.

The Akeyless Secure Remote Access Bastion provides secure remote access to resources using Just In Time credentials (dynamic, rotated secrets, and SSH certificates). This guide provides guidance for a **Docker** deployment of Akeyless Secure Remote Access Bastions both **Web-bastion**  and **SSH-bastion**.

# Prerequisites

* Docker Installed

* [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates) for CLI Access.

* At least 1 vCPU available with 1 GB RAM per Docker container. 

\***\*Network\*\***

* Make sure to use sticky session.

* Cloud Provider Load Balancer - Make sure to config the Load Balancer to support sticky sessions, for example, in AWS, using ELB: [https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html)

When using SSH sessions behind a load balancer such as AWS ELB, the session can be closed due to an idle connection timeout, so we recommend increasing it to a reasonably high value or even unlimited.

e.g., when running on AWS with ELB: [https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs\_elb\_console](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console)

\***\*Storage\*\***

Currently, this setup requires a **Volume** storage mechanism of [Docker](https://docs.docker.com/storage/volumes/).

> 🚧 Note:
>
> To enable Secure Remote Access features, you will have to get an access key to Akeyless private docker repository. Please contact your Account Manager for more details.

# Configuration

The Secure Remote Access Bastion should be set with a **privileged** `AccessID` with **Read** and **list** permissions to fetch the relevant secret on behalf of your users. Set the `PRIVILEGED_ACCESS_ID` variable with the relevant `AccessID` as described in the Authentication section of this page. 

Users can have only `list` permissions on their secrets. Upon successful authentication against your IDP, the bastion will fetch the requested secret from Akeyless and will inject them directly for your users transparently.\
To control who will be the relevant users that will be allowed to request access from the Akeyless Bastion, set the `ALLOWED_ACCESS_IDS` variable with a list of `AccessIDs` that will be authorized to request access. 

For RDP access that uses the **Fixed user** feature, rely on the username sub-claims to figure out **Windows** username to use. If you use a different sub-claim, it should be specified at deployment time using `USERNAME_SUB_CLAIM` environment variable. To use this mode, separately for either `SSH` or for `RDP` only, you can use instead `SSH_USERNAME_SUB_CLAIM` and `RDP_USERNAME_SUB_CLAIM` correspondingly. 

To provide just-in-time native CLI access for your users using [Keyless SSH](https://docs.akeyless.io/docs/ssh-certificates) set the `CA_PUB` variable with the matching public key of the key you used to create the [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates)

> 📘 Info
>
> If you don't have an SSH certificate ready, please follow this guide on creating [SSH Cert issuer](https://docs.akeyless.io/docs/how-to-configure-ssh) with Akeyless Platform and set your CA.

## Authentication

The following [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) are supported: 

* [API Key](https://docs.akeyless.io/docs/api-key) 

* [AWS IAM](https://docs.akeyless.io/docs/aws-iam) 

* [GCP GCE](https://docs.akeyless.io/docs/gcp-auth-method)   

* [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad)

## API Key Authentication

To set your Bastion default authentication based on [API Key](https://docs.akeyless.io/docs/api-key), set the `PRIVILEGED_ACCESS_ID` and the matching `PRIVILEGED_ACCESS_KEY`  with a list of `ALLOWED_ACCESS_IDS` that will be authorized to request access:

```shell web-bastion
docker run --name web-bastion -d -p 8888:8888  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e PRIVILEGED_ACCESS_KEY="<AccessKey>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>" \
  -e CLUSTER_NAME="Akeyless Bastion" \
  -e USERNAME_SUB_CLAIM="FIXED_USER_KEY_NAME" \
  --restart unless-stopped akeyless/zero-trust-bastion:latest
```
```shell ssh-bastion
docker run --name ssh-bastion -d -p 0.0.0.0:2222:22 -p 0.0.0.0:9900:9900  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e PRIVILEGED_ACCESS_KEY="<AccessKey>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>"  \
  -e CA_PUB="<CA Public Key>" \
  -e CLUSTER_NAME="Akeyless Bastion" \
  --cap-add=SYS_ADMIN --privileged --restart unless-stopped akeyless/ssh-proxy:latest
```

## CSP IAM Authentication

While running your Dockers inside your cloud environment, you can use [AWS IAM](https://docs.akeyless.io/docs/aws-iam), [GCP](https://docs.akeyless.io/docs/gcp-auth-method), or [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad), using machine-to-machine authentication between Akeyless and your Cloud Service Provider with a list of allowed `AccessIDs` that will be authorized to request access.

## AWS IAM

AWS IAM can be used for an instance with an IAM Role. While working with an IAM Role associated with the instance itself, you can provide your [AWS IAM](https://docs.akeyless.io/docs/aws-iam) `Access ID` as your <code>PRIVILEGED\_ACCESS\_ID</code>, with a list of `ALLOWED_ACCESS_IDS` that will be authorized to request access:

```shell web-bastion
docker run --name web-bastion -d -p 8888:8888  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>" \
  -e USERNAME_SUB_CLAIM="FIXED_USER_KEY_NAME" \
  -e CLUSTER_NAME="Akeyless Bastion" \
  --restart unless-stopped akeyless/zero-trust-bastion:latest
```
```shell ssh-bastion
docker run --name ssh-bastion -d -p 0.0.0.0:2222:22 -p 0.0.0.0:9900:9900  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>"  \
  -e CA_PUB="<CA Public Key>" \
  -e CLUSTER_NAME="Akeyless Bastion" \
  --cap-add=SYS_ADMIN --privileged --restart unless-stopped akeyless/ssh-proxy:latest
```

## GCP GCE

Deploying Akeyless Bastion over Docker using the authentication between your Bastion and Akeyless SaaS using our [GCP Authentication method](https://docs.akeyless.io/docs/gcp-auth-method) can be done using the GCP.\
Set your [GCP GCE](https://docs.akeyless.io/docs/gcp-auth-method) `Access ID`  as your `PRIVILEGED_ACCESS_ID` and at least one another `Access ID` in the `ALLOWED_ACCESS_IDS` list.

```shell web-bastion
docker run --name web-bastion -d -p 8888:8888  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e GCP_AUDIENCE="akeyless.io" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>" \
  -e USERNAME_SUB_CLAIM="FIXED_USER_KEY_NAME" \
  -e CLUSTER_NAME="Akeyless Bastion" \
  --restart unless-stopped akeyless/zero-trust-bastion:latest
```
```shell ssh-bastion
docker run --name ssh-bastion -d -p 0.0.0.0:2222:22 -p 0.0.0.0:9900:9900  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>"  \
  -e CA_PUB="<CA Public Key>" \
  -e CLUSTER_NAME="Akeyless Bastion" \
  --cap-add=SYS_ADMIN --privileged --restart unless-stopped akeyless/ssh-proxy:latest
```

## Azure Active Directory

Set your [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad) `Access ID` as your <code>PRIVILEGED\_ACCESS\_ID</code> with the matching service principal `azureobjectID', with a list of `ALLOWED\_ACCESS\_IDS\` that will be authorized to request access.

```shell web-bastion
docker run --name web-bastion -d -p 8888:8888  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e AZURE_OBJECT_ID="<AzureObjectID>" \
  -e GCP_AUDIENCE="akeyless.io" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>" \
  -e USERNAME_SUB_CLAIM="FIXED_USER_KEY_NAME" \
  -e CLUSTER_NAME="Akeyless Bastion" \
  --restart unless-stopped akeyless/zero-trust-bastion:latest
```
```shell ssh-bastion
docker run --name ssh-bastion -d -p 0.0.0.0:2222:22 -p 0.0.0.0:9900:9900  \
  -e AKEYLESS_GW_URL = "https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>"  \
  -e CA_PUB="<CA Public Key>" \
  -e CLUSTER_NAME="Akeyless Bastion" \
  --cap-add=SYS_ADMIN --privileged --restart unless-stopped akeyless/ssh-proxy:latest
```

## Session Recording

To enable session recording on your **web-bastion**, you can export the recordings into an S3 bucket or to an Azure Blob storage: 

```shell web-bastion-AWS-IAM
docker run --name web-bastion -d -p 8888:8888  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>" \
  -e USERNAME_SUB_CLAIM="FIXED_USER_KEY_NAME" \
  -e AWS_REGION="<aws region>" \
  -e AWS_S3_BUCKET="<bucket name>" \
  -e AWS_S3_PREFIX="akeyless-zero-trust-bastion" \
  -e CLUSTER_NAME="Akeyless Bastion" \
  --restart unless-stopped akeyless/zero-trust-bastion:latest
```
```shell s3-Inline connection string
docker run --name web-bastion -d -p 8888:8888  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>" \
  -e USERNAME_SUB_CLAIM="FIXED_USER_KEY_NAME" \
  -e AWS_REGION="<aws region>" \
  -e AWS_S3_BUCKET="<bucket name>" \
  -e AWS_S3_PREFIX="akeyless-zero-trust-bastion" \
  -e AWS_ACCESS_KEY_ID="<AWS ACCESS KEY ID>" \
  -e AWS_SECRET_ACCESS_KEY="<AWS ACCESS KEY>" \
  -e CLUSTER_NAME="Akeyless Bastion" \
  --restart unless-stopped akeyless/zero-trust-bastion:latest
```
```shell Azure Blob
docker run --name web-bastion -d -p 8888:8888  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>" \
  -e USERNAME_SUB_CLAIM="FIXED_USER_KEY_NAME" \
  -e AZURE_STORAGE_ACCOUNT="<Azure Storage Name>" \
  -e AZURE_STORAGE_CONTAINER_NAME="<Azure Storage Container Name>" \    
  -e CLUSTER_NAME="Akeyless Bastion" \
  --restart unless-stopped akeyless/zero-trust-bastion:latest
```
```shell Azure Blob-Inline connection string
docker run --name web-bastion -d -p 8888:8888  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>" \
  -e USERNAME_SUB_CLAIM="FIXED_USER_KEY_NAME" \
  -e AZURE_TENANT_ID="<Azure Tenant ID>" \
  -e AZURE_CLIENT_ID="<Azure Client ID>" \
  -e AZURE_CLIENT_SECRET="<Azure Client Secret>" \
  -e AZURE_STORAGE_ACCOUNT="<Azure Storage Account>" \
  -e AZURE_STORAGE_CONTAINER_NAME="<Azure Storage Container Name>" \  
  -e CLUSTER_NAME="Akeyless Bastion" \
  --restart unless-stopped akeyless/zero-trust-bastion:latest
```

Alternatively, to save a local copy of your session recording, use the following variables:

`KEEP_LOCAL_RECORDINGS="true"` with a target folder destination `$BASE_DIR/recordings:/home/akeyless/recordings`, for example:

```shell
docker run --name web-bastion -d -p 8888:8888  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>" \
  -e USERNAME_SUB_CLAIM="FIXED_USER_KEY_NAME" \
  -e KEEP_LOCAL_RECORDINGS="true" \
  -v $BASE_DIR/recordings:/home/akeyless/recordings \
  -e CLUSTER_NAME="Akeyless Bastion" \
  --restart unless-stopped akeyless/zero-trust-bastion:latest
```

## Log Forwarding

To forward all your users session logs from the **ssh-bastion**, mount a local file which hold the setting of your target log server as described in [this](https://docs.akeyless.io/docs/ssh-log-forwarding) guide, for example: 

```shell ssh-bastion
docker run --name ssh-bastion -d -p 0.0.0.0:2222:22 -p 0.0.0.0:9900:9900  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>"  \
  -e CA_PUB="<CA Public Key>" \
  -e CLUSTER_NAME="Akeyless Bastion" \
  -v &PWD/log_forwarding.conf:/var/akeyless/conf/logand.conf \
  --cap-add=SYS_ADMIN --privileged --restart unless-stopped akeyless/ssh-proxy:latest
```
```shell log_forwarding.conf
cat <<EOT>> log_forwarding.conf
enable="true"
target_log_type="logz_io"
target_logz_io_token=""
target_logz_io_protocol="tcp"
EOT
```

## Redirect to Bastion URLs

To ensure only validated redirects are accepted, you can harden your bastion using the `ALLOWED_BASTION_URLS` variable with a list of URLs that will be considered valid for redirection from the Akeyless Zero Trust Portal back to the relevant **web-bastion**: 

```shell web-bastion
docker run --name web-bastion -d -p 8888:8888  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>" \
  -e USERNAME_SUB_CLAIM="FIXED_USER_KEY_NAME" \
  -e CLUSTER_NAME="Akeyless Bastion" \
  -e ALLOWED_BASTION_URLS="https://mybastion-url.com" \
  --restart unless-stopped akeyless/zero-trust-bastion:latest
```

## Concurrent Unauthenticated Connections

To specify the maximum number of concurrent unauthenticated connections to the SSH Bastion, set the  `CONFIG_MAX_STARTUPS` variable:

```shell ssh-bastion
docker run --name ssh-bastion -d -p 0.0.0.0:2222:22 -p 0.0.0.0:9900:9900  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>"  \
  -e CA_PUB="<CA Public Key>" \
  -e CONFIG_MAX_STARTUPS="200:30:300" \
  -e CLUSTER_NAME="Akeyless Bastion" \
  -v &PWD/log_forwarding.conf:/var/akeyless/conf/logand.conf \
  --cap-add=SYS_ADMIN --privileged --restart unless-stopped akeyless/ssh-proxy:latest
```

Verify that both **web-bastion** and **ssh-bastion** containers are up and running.

## SSH Fingerprint

To accept the SSH Bastion host key fingerprint automatically without re-accepting it after upgrades etc. You can set an environment variable as part of the Docker deployment with a dedicated folder within your Akeyless account. The SSH bastion will automatically store the relevant fingerprints within that folder. In this example, we will store the fingerprints inside `/MY_SSH_BASTION_HOST_KEYS` folder.\
Note, please  ensure your Bastion default Auth Method has the following permissions on that folder `create`,`read`, `list`:

```shell
docker run --name ssh-bastion -d -p 0.0.0.0:2222:22 -p 0.0.0.0:9900:9900  \
  -e AKEYLESS_GW_URL="https://rest.akeyless.io" \
  -e PRIVILEGED_ACCESS_ID="<AccessID>" \
  -e ALLOWED_ACCESS_IDS="<AccessIDs>"  \
  -e CA_PUB="<CA Public Key>" \
  -e CONFIG_MAX_STARTUPS="200:30:300" \
  -e CLUSTER_NAME="Akeyless Bastion" \
  -e SSH_HOST_KEYS_PATH=/MY_SSH_BASTION_HOST_KEYS \
  -v &PWD/log_forwarding.conf:/var/akeyless/conf/logand.conf \
  --cap-add=SYS_ADMIN --privileged --restart unless-stopped akeyless/ssh-proxy:latest
```
