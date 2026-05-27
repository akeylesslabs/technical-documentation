---
title: Docker Compose (Gateway + SRA)
slug: sra-docker
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
Use this page to deploy Akeyless Gateway with Secure Remote Access (SRA) components by using Docker Compose.

> ℹ️ **Note:**
>
> The Docker Compose SRA deployment supports a subset of the configuration options available in Kubernetes. For production workloads or advanced configuration requirements, see [Remote Access on Kubernetes](https://docs.akeyless.io/docs/sra-setup-k8s).

You can get the [configuration files](https://github.com/akeylesslabs/docker-compose/blob/main/README.md) that will be used to deploy the gateway with the SRA by cloning the following repository to your environment:

```shell
gh repo clone akeylesslabs/docker-compose
```

The following files will be used:

* `docker-compose.yaml`: Defines the Akeyless services and their setup.

* `gateway.env`: Stores environment variables for configuring the Gateway.

* `sra.env`: Stores environment variables for Secure Remote Access.

* `cache.env`: Stores Redis password (required when cache is enabled).

This guide assumes you already have a Gateway deployment and focuses on SRA-related configuration.

## Prerequisites

* [Docker Installed](https://docs.docker.com/engine/install/) (version `20.10` or higher).

* [Docker Compose](https://docs.docker.com/compose/) (version `1.29` or higher).

* Akeyless Gateway deployed on [Docker Compose](https://docs.akeyless.io/docs/gateway-deploy-docker-compose#/).

* [SSH Certificate Issuer](https://docs.akeyless.io/docs/sra-ssh-certificates) for CLI access with `session_username` allowed.

* Minimum 1 vCPU and 2 GiB memory per SRA component.

For a full list of ports, outbound dependencies, and Redis/cache requirements, see [Requirements](https://docs.akeyless.io/docs/sra-requirements).

### Deployment Overview

The Docker Compose file defines the following services:

| Service | Description | Ports |
| --- | --- | --- |
| [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-deploy-docker-compose#/) | Central access control and authentication gateway | 8000 (API), 8080 (Health), 8889 (metrics) |
| SRA Web | Web-based Zero Trust portal for remote access | As specified in YAML |
| SRA SSH Proxy | Secure SSH-based remote access | 2222 (SSH), 9900 (Internal) |

Each service runs within an isolated Docker bridge network (internal-net), ensuring secure internal communication.

## Configuration

To deploy a gateway with the SRA utility, run the following steps:

1. For SSH access, configure the following in the `docker-compose.yaml` file:

     ```yaml
     volumes:
         - /path/to/ca.pub:/var/akeyless/creds/ca.pub
     ```

    In the example above, the `ca.pub` is the public key specified in the SSH Certificate Issuer.

    [Read more about the available parameters](https://github.com/akeylesslabs/docker-compose/blob/main/docker-compose.yaml).

2. Configure the following in the `gateway.env` file:

    * `CLUSTER_NAME`: The name of the cluster that will be deployed.
    * `UNIFIED_GATEWAY`: Set to `true` to enable the SRA utility.
    * `GATEWAY_ACCESS_ID`: The `AccessID` of the authentication method that will be used for the authentication.
    * `GATEWAY_ACCESS_TYPE`: The `AccessType` of the authentication method.
    * `GATEWAY_ACCESS_KEY`: The `AccessKey` of the authentication method (relevant only for [API Key](https://docs.akeyless.io/docs/auth-with-api-key)).
    * `ALLOWED_ACCESS_PERMISSIONS`: A list of users who can manage your Gateway configuration
    * [Read more about the available parameters](https://github.com/akeylesslabs/docker-compose/blob/main/gateway.env).

3. Configure the following in the `sra.env` file:

    * `UNIFIED_GATEWAY`: Set to `true`.

    [Read more about the available parameters](https://github.com/akeylesslabs/docker-compose/blob/main/sra.env).

4. Optional - if Redis is enabled, configure the following in the `cache.env` file:

    * `REDIS_PASS=password`.

    [Read more about the available parameters](https://github.com/akeylesslabs/docker-compose/blob/main/cache.env).

## Installation

To deploy Gateway and SRA services, run this command from the directory where your configuration files are located.

```shell
docker compose --profile gateway --profile sra up -d
```

To verify the deployment, run:

```shell
docker ps
```

Upon successful installation, you will see 4 containers:

* `akeyless-sra-ssh`

* `akeyless-sra-web`

* `akeyless-gateway`

* `akeyless-cache`

## SRA Access

To start working with SRA, open your browser and login to the **Secure Remote Access** portal using the following URL: `http://Your-Akeyless-Gateway-URL:8000/sra/portal`

Log in with one of the [supported authentication methods](https://docs.akeyless.io/docs/sra-portal).

Once logged in, you will see the [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret#/) with Secure Remote Access enabled. From there, you can securely access those resources using Just-In-Time credentials, either through the web interface or by way of an SSH connection.

## Advanced Configuration

For keyboard layouts, session log forwarding, RDP recording configuration, SSH fingerprint behavior, and `CONFIG_MAX_STARTUPS`, see [Advanced Configuration on Docker Compose](https://docs.akeyless.io/docs/sra-advanced-configuration-docker).

If web application isolation is required, continue with [Zero Trust Web Access Topology](https://docs.akeyless.io/docs/sra-web-access-topology).
