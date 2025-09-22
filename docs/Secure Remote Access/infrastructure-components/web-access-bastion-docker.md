---
title: Web Access Bastion on Docker
excerpt: Docker Setup
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Akeyless Web Access Bastion provides Secure Remote Access to any web application with session recording, including proxy service acting as an entry point to your internal web applications, where only after successful authentication users will get access, either via an isolated remote browser or directly to your target server based on your secret configuration. 

Working with isolated browsers provides a complete zero-knowledge where users do not have any knowledge about the access credentials.  

This guide provides guidance for the deployment of the Akeyless-Web-Access-Bastion on **Docker** using **Docker Compose**

# Prerequisites

* Docker Compose installed.

* Web Access Bastion - `docker-compose.yml` file.

* Minimum 1 vCPU available with 2GB RAM for the `WebWorker` and  1 vCPU available with 1GB RAM for the `WebDispatcher`.

***Network***

When using an Embedded browser session behind a load balancer such as ELB, the session can be closed due to an idle connection timeout, it's advised to increase it to a reasonably high value or even unlimited.

e.g, when running on AWS with ELB: [https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs\_elb\_console](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console)

***Storage***

To be able to download files to your local machine, the Docker engine requires mounted volumes.\
e.g, when running on AWS with EKS: [https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html](https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html)

For security reasons, please limit the volume mount permissions to `0650`.

> 🚧 Note:
>
> To enable Secure Remote Access features, you will have to get an access key to Akeyless's private repository. Please contact your Account Manager for more details.

# Configuration

Download the **Docker Compose** file using this link: [https://github.com/akeylesslabs/helm-charts/blob/main/docker-compose/akeyless-zero-trust-web-access/docker-compose.yml](https://github.com/akeylesslabs/helm-charts/blob/main/docker-compose/akeyless-zero-trust-web-access/docker-compose.yml)

To work with a specific Gateway, set the environment variable that points to your Gateway URL on port `8080`. Alternatively, you can work with Akeyless public Gateway endpoint instead. To support `HTTP` connections, set the `DISABLE_SECURE_COOKIE` variable with `true` otherwise, only `HTTPS` connection will be supported, and set your policy for internal authentication using `ALLOW_INTERNAL_AUTH`. In the following example, internal authentication is blocked:

```yaml
services:
  dispatcher:
    image: "akeyless/zero-trust-web-dispatcher"
    ports:
      - "9000:9000"
      - "19414:19414"
    volumes:
      - $PWD/shared:/etc/shared
    environment:
      - CLUSTER_NAME=compose-ztwa
      - SERVICE_DNS=worker
      - AKEYLESS_GW_URL=https://rest.akeyless.io
      - ALLOW_INTERNAL_AUTH=false
      - DISABLE_SECURE_COOKIE=true
      - WEB_PROXY_TYPE=http
      - AKEYLESS_URL=https://vault.akeyless.io
```

The Web Access Bastion should be set with a **privileged** `AccessID` with **Read** and **list** permissions, to fetch the relevant secret on behalf of your users, set the `PRIVILEGED_ACCESS_ID` variable with the relevant `AccessID` as described in the Authentication section of this page. 

Users then can have only `list` permissions on their secrets. Upon successful authentication against your IDP, the bastion will fetch the requested secret from Akeyless and will inject them directly for your users transparently. 

To control who will be the relevant users that will be allowed to request access from the Akeyless Bastion, set the `ALLOWED_ACCESS_IDS` variable with a list of `AccessIDs` comma separated that will be authorized to request access. 

```yaml
services:
  dispatcher:
    image: "akeyless/zero-trust-web-dispatcher"
    ports:
      - "9000:9000"
      - "19414:19414"
    volumes:
      - $PWD/shared:/etc/shared
    environment:
      - CLUSTER_NAME=compose-ztwa
      - SERVICE_DNS=worker
      - AKEYLESS_GW_URL=https://rest.akeyless.io
      - PRIVILEGED_ACCESS_ID=<accessID>
      - ALLOWED_ACCESS_IDS=[AccessID1,AccessID2]
      - ALLOW_INTERNAL_AUTH=false
      - DISABLE_SECURE_COOKIE=true
      - WEB_PROXY_TYPE=http
```

## Authentication

The following [Authentication Methods](doc:access-and-authentication-methods) are supported: 

* [API Key](doc:api-key) 

* [AWS IAM](doc:aws-iam) 

* [Azure Active Directory](doc:azure-ad)

* [GCP GCE](doc:gcp-auth-method) 

## API Key Authentication

To set your Bastion default authentication based on [API Key](doc:api-key), set the `PRIVILEGED_ACCESS_ID` and the matching `PRIVILEGED_ACCESS_KEY` as environment variables with a list of `ALLOWED_ACCESS_IDS` that will be authorized to request access:

```yaml Shell
services:
  dispatcher:
    image: "akeyless/zero-trust-web-dispatcher"
    ports:
      - "9000:9000"
      - "19414:19414"
    volumes:
      - $PWD/shared:/etc/shared
    environment:
      - CLUSTER_NAME=compose-ztwa
      - SERVICE_DNS=worker
      - AKEYLESS_GW_URL=https://rest.akeyless.io
      - PRIVILEGED_ACCESS_ID=<AccessID>
      - PRIVILEGED_ACCESS_KEY=<AccessKey>
      - ALLOWED_ACCESS_IDS=[AccessIds]
      - ALLOW_INTERNAL_AUTH=false
      - DISABLE_SECURE_COOKIE=true
      - WEB_PROXY_TYPE=http
```

## CSP IAM Authentication

While running your Docker inside your cloud environment, you can use [AWS IAM](doc:aws-iam), [GCP](doc:gcp-auth-method), or [Azure Active Directory](doc:azure-ad), using machine-to-machine authentication between Akeyless and your Cloud Service Provider with a list of allowed `AccessIDs` that will be authorized to request access.

## AWS IAM

AWS IAM can be used in the following approach: 

* Instance IAM Role 

While working with an IAM Role associated with the instance himself, you can provide your [AWS IAM](doc:aws-iam) `Access ID`  as your <code>PRIVILEGED\_ACCESS\_ID</code>, with a list of `ALLOWED_ACCESS_IDS` that will be authorized to request access:

```yaml Shell
services:
  dispatcher:
    image: "akeyless/zero-trust-web-dispatcher"
    ports:
      - "9000:9000"
      - "19414:19414"
    volumes:
      - $PWD/shared:/etc/shared
    environment:
      - CLUSTER_NAME=compose-ztwa
      - SERVICE_DNS=worker
      - AKEYLESS_GW_URL=https://rest.akeyless.io
      - PRIVILEGED_ACCESS_ID=<AWS_IAM_AccessID>
      - ALLOWED_ACCESS_IDS=[AccessIds]
      - ALLOW_INTERNAL_AUTH=false
      - DISABLE_SECURE_COOKIE=true
      - WEB_PROXY_TYPE=http
```

## Azure Active Directory

Azure AD authentication is provided with OpenID Connect. OpenID Connect is an identity layer built on top of the OAuth 2.0 protocol. Akeyless treats Azure as a trusted third party and verifies entities based on a JWT signed by the Azure Active Directory for the configured tenant.

Set your [Azure Active Directory](doc:azure-ad) `Access ID` as your <code>PRIVILEGED\_ACCESS\_ID</code> with a list of `ALLOWED_ACCESS_IDS` that will be authorized to request access:

```yaml Shell
services:
  dispatcher:
    image: "akeyless/zero-trust-web-dispatcher"
    ports:
      - "9000:9000"
      - "19414:19414"
    volumes:
      - $PWD/shared:/etc/shared
    environment:
      - CLUSTER_NAME=compose-ztwa
      - SERVICE_DNS=worker
      - AKEYLESS_GW_URL=https://rest.akeyless.io
      - PRIVILEGED_ACCESS_ID=<Azure_AD_AccessID>
      - ALLOWED_ACCESS_IDS=[AccessIds]
      - ALLOW_INTERNAL_AUTH=false
      - DISABLE_SECURE_COOKIE=true
      - WEB_PROXY_TYPE=http
```

## GCP GCE

Deploying Akeyless Bastion over Docker using the authentication between your Bastion and Akeyless SaaS using our [GCP Authentication method](doc:gcp-auth-method) can be done using the GCP.\
 Set your [GCP GCE](doc:gcp-auth-method) `Access ID`  as your `PRIVILEGED_ACCESS_ID` and at least one another `Access ID` in the `ALLOWED_ACCESS_IDS` list.

```yaml
services:
  dispatcher:
    image: "akeyless/zero-trust-web-dispatcher"
    ports:
      - "9000:9000"
      - "19414:19414"
    volumes:
      - $PWD/shared:/etc/shared
    environment:
      - CLUSTER_NAME=compose-ztwa
      - SERVICE_DNS=worker
      - AKEYLESS_GW_URL=https://rest.akeyless.io
      - PRIVILEGED_ACCESS_ID=<GCP_GCE_AccessID>
      - ALLOWED_ACCESS_IDS=AccessIds]
      - ALLOW_INTERNAL_AUTH=false
      - DISABLE_SECURE_COOKIE=true
      - WEB_PROXY_TYPE=http
```

## Redirect to Bastion URLs

To ensure only validated redirects are accepted, you can harden your bastion using the `ALLOWED_BASTION_URLS` variable with a list of URLs that will be considered valid for redirection from the Akeyless Zero Trust Portal back to the relevant **web-dispatcher-bastion**:

```yaml
services:
  dispatcher:
    image: "akeyless/zero-trust-web-dispatcher"
    ports:
      - "9000:9000"
      - "19414:19414"
    volumes:
      - $PWD/shared:/etc/shared
    environment:
      - CLUSTER_NAME=compose-ztwa
      - SERVICE_DNS=worker
      - AKEYLESS_GW_URL=https://rest.akeyless.io
      - PRIVILEGED_ACCESS_ID=<AccessID>
      - ALLOWED_ACCESS_IDS=[AccessIds]
      - ALLOW_INTERNAL_AUTH=false
      - DISABLE_SECURE_COOKIE=true
      - ALLOWED_BASTION_URLS=[https://Web-Access-Bastion-URL]
      - LOG_FORWARDING=
      - WEB_PROXY_TYPE=http
```

# Advanced Configuration

## Cluster Name

Each Bastion is uniquely identified by combining the **Privilege Access ID**  Authentication Method and the **Cluster Name**.

It means that changing the  **Privilege Access ID** or the **Cluster Name** of your Bastion instance will create an entirely new Bastion instance.

It is recommended to set a meaningful Cluster Name for your Bastion cluster from the very beginning. By default, your cluster name is **compose-ztwa**.

To do that, you can set the <code>clusterName="meaningful-cluster-name"</code> field as part of the Bastion Docker Compose `yaml` file.

```yaml docker-compose.yml
services:
  dispatcher:
    environment:
      - CLUSTER_NAME=compose-ztwa
```

## Proxy

To configure your proxy settings, you can set several parameters, including proxy settings for HTTP traffic, HTTPS traffic, and Ignore Hosts, using the `no_proxy` field, to prevent local traffic from going through your proxy server. You can set both services `dispatcher` and `worker` accordingly.

```yaml docker-compose.yml
services:
  dispatcher:
    environment:
      - CLUSTER_NAME=compose-ztwa
      - http_proxy=
      - https_proxy=
      - no_proxy=
  worker:
    environment:
      - http_proxy=
      - https_proxy=
      - no_proxy=
```

## Log Forwarding

To enable log forwarding to an existing log management system, please find a list of available target systems and configurations on [this](https://docs.akeyless.io/docs/ssh-log-forwarding) page. Set the `LOG_FORWARDING` variable inside the  **Docker Compose** deployment file as follow: 

```yaml docker-compose.yml
services:
  dispatcher:
    image: "akeyless/zero-trust-web-dispatcher"
    ports:
      - "9000:9000"
      - "19414:19414"
    volumes:
      - $PWD/shared:/etc/shared
    environment:
      - CLUSTER_NAME=compose-ztwa
      - SERVICE_DNS=worker
      - AKEYLESS_GW_URL=https://rest.akeyless.io
      - PRIVILEGED_ACCESS_ID=<AccessID>
      - ALLOWED_ACCESS_IDS=[AccessIds]
      - ALLOW_INTERNAL_AUTH=false
      - DISABLE_SECURE_COOKIE=true
      - ALLOWED_BASTION_URLS=https://Web-Access-Bastion-URL
      - WEB_PROXY_TYPE=http
      - LOG_FORWARDING='enable="true"\n target_log_type="logz_io"\n target_logz_io_token=""\n target_logz_io_protocol="tcp" \n'
```

## WebWorker

This section enables global settings of the internal dedicated remote browsers your users will use. You can customize the settings to provide a more flexible experience for your users. 

Default `policies` sections aimed to provide the most secure work mode. By default, all `URLs` are blocked hence users will not be able to navigate inside the remote browser to different sites. If needed, set the relevant `URLs` in the `Exceptions` list. 

```shell policies.json
cat <<EOT > policies.json
{
  "policies": {
    "BlockAboutConfig": true,
    "BlockAboutAddons": true,
    "BlockAboutProfiles": true,
    "BlockAboutSupport": true,
    "DisableDeveloperTools": true,
    "DisableFirefoxAccounts": true,
    "DisablePasswordReveal": true,
    "DisablePrivateBrowsing": true,
    "DisableProfileImport": true,
    "DisableSafeMode": true,
    "OfferToSaveLogins": false,
    "OfferToSaveLoginsDefault": false,
    "PasswordManagerEnabled": false,
    "Proxy": {
      "Mode": "system",
      "Locked": true
    },
    "Preferences": {},
    "Certificates": {
#      "Install": ["/etc/ssl/certs/yourOrgRootCA.crt"]
    },
    "WebsiteFilter": {
      "Block": [
        "<all_urls>"
      ],
      "Exceptions": [
        "https://*.akeyless.io/*"
      ]
    }
  }
}
EOT
```

> 🚧 Notice:
>
> The `policies.json` **must** be provided for the isolated web browsing to work.

**Notice:** If your organization uses private certificate authorities (CAs) to issue certificates for your internal web apps, and you either wish to access those websites through the web-access-bastion, or if your AKEYLESS\_GW\_URL is pointing to a **Gateway** that uses such a certificate, you must configure the WebWorkers as follows:

1. Mount your organization's Root CA certificate to the containers (in the docker-compose.yml, under services.worker.volumes)
2. In the `policies.json` above, uncomment the *Certificates.Install* line and set it to the relevant certificates' paths inside the container

## DLP

To work with Data Leak Protection tools, you can explicitly set the target settings of your DLP server, as well as with dedicated audit logs forwarding.

```yaml
worker:
    image: "akeyless/zero-trust-web-worker"
    security_opt:
      - seccomp=unconfined
    shm_size: '2gb'
    volumes:
      - $PWD/policies.json:/usr/lib/firefox/distribution/policies.json:ro
      - $PWD/shared:/etc/shared
    environment:
      - INTERNAL_DISPATCHER_IP=10.5.0.2
      - DISPLAY_WIDTH=2560
      - DISPLAY_HEIGHT=1200
      - DLP_CONF=
      - LOG_FORWARDING=
```

# Install

Run the following command to apply your settings as part of the **Docker Compose** command:

```shell
docker-compose up -d --scale worker=3
```

Verify that both containers are up and running: 

<code>web-worker-deployment</code>\ <code>web-dispatcher-deployment</code>
