---
title: Docker Compose Unified Gateway Quickstart
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
This quickstart deploys the Akeyless Unified Gateway with Secure Remote Access (SRA) by using Docker Compose and the sample deployment files.

## Prerequisites

* Docker Engine 20.10 or later.
* Docker Compose 2.0 or later.
* `curl`, `git`, and `ssh-keygen` available on the host.
* An Akeyless Authentication Method with permissions to manage required resources.

## Step 1: Clone Deployment Sample Files

```shell
git clone https://github.com/akeylesslabs/technical-documentation.git
cd technical-documentation/samples/unified-gateway/docker-compose-deploy
```

## Step 2: Configure `gateway.env`

Set core authentication values:

```shell
GATEWAY_ACCESS_ID="p-xxxxxx"
GATEWAY_ACCESS_TYPE="access_key"
GATEWAY_ACCESS_KEY="<your-access-key>"
CLUSTER_NAME="my-gateway"
```

## Step 3: Configure `sra.env`

Set SRA service endpoints:

```shell
USE_CLUSTER_CACHE="true"
REMOTE_ACCESS_WEB_SERVICE_INTERNAL_URL="http://akeyless-web:8888"
REMOTE_ACCESS_SSH_SERVICE_INTERNAL_URL="http://akeyless-ssh:9900"
```

## Step 4: Prepare SSH CA Key for SRA

```shell
mkdir -p ssh-config
ssh-keygen -t rsa -b 4096 -f ssh-config/ca -C "akeyless-ca"
```

Ensure the public key is available as `ssh-config/ca.pub`.

## Step 5: Set Redis Password Input

Create a `.env` file in the same directory and set `REDIS_PASS`:

```shell
echo "REDIS_PASS=<strong-random-password>" > .env
```

Create the Docker Compose secret file expected by the sample:

```shell
mkdir -p secrets
echo "<strong-random-password>" > secrets/redis_password
```

The current sample uses both `REDIS_PASS` and `secrets/redis_password`, so set both values.

## Step 6: Start Services

```shell
docker compose --profile gateway --profile sra up -d
```

## Step 7: Validate Deployment

```shell
docker ps
curl -f http://localhost:8080/health
```

Expected result: the health endpoint returns `OK` and all required containers are running.

## Step 8: Access the Services

* Gateway endpoint: `http://localhost:8000`
* SRA web endpoint: `http://localhost:8888`

## Related Reference Pages

* [Docker Compose](https://docs.akeyless.io/docs/gateway-compose)
* [Advanced Configuration (Docker)](https://docs.akeyless.io/docs/advanced-configuration)
* [Gateway Configuration Manager](https://docs.akeyless.io/docs/gateway-configuration-manager)
