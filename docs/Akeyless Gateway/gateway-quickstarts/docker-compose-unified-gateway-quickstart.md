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

Edit `gateway.env` and set the following values:

```dotenv
GATEWAY_ACCESS_ID="p-xxxxxx"
GATEWAY_ACCESS_TYPE="access_key"
GATEWAY_ACCESS_KEY="<your-access-key>"
CLUSTER_NAME="my-gateway"
```

Also ensure `ALLOWED_ACCESS_PERMISSIONS` in `gateway.env` includes the users or auth methods that will sign in to Gateway/SRA web.

For example:

```dotenv
ALLOWED_ACCESS_PERMISSIONS='[{"access_id":"p-xxxxxxxxxxxx","name":"Gateway Admin"}]'
```

If `ALLOWED_ACCESS_PERMISSIONS` is not modified, Gateway and SRA sign-in flows can fail authentication.

<ApiKeyWarning />

## Step 3: Prepare SSH CA Key for SRA

```shell
mkdir -p ssh-config
ssh-keygen -t rsa -b 4096 -f ssh-config/ca -C "akeyless-ca"
```

When prompted for a passphrase, either:

* Press `Enter` twice to create the key without a passphrase, or
* Enter a passphrase twice if your environment requires encrypted key files.

Ensure the public key is available as `ssh-config/ca.pub`. This is the default behavior.

Expected output includes lines similar to:

```text
Enter passphrase for "ssh-config/ca" (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in ssh-config/ca
Your public key has been saved in ssh-config/ca.pub
```

## Step 4: Set Redis Password Input

1. Create a `.env` file in the same directory and set `REDIS_PASS`:

    ```shell
    echo "REDIS_PASS=RedisPass_ChangeMe_2026" > .env
    ```

2. Create the secret file used by the sample Compose definition:

    ```shell
    mkdir -p secrets
    echo "RedisPass_ChangeMe_2026" > secrets/redis_password
    ```

Use your own strong value instead of the example, and keep both values identical.

## Step 5: Start Services

```shell
docker compose --profile gateway --profile sra up -d
```

> ℹ️ **Note: Windows troubleshooting**
>
> If you see the following error, Docker Desktop is not connected to the Linux engine:
>
> ```text
> open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified
> ```
>
> * Start Docker Desktop and wait until it reports that Docker is running.
> * Verify the CLI can reach Docker:
>
>     ```shell
>     docker info
>     ```
>
> * Run the compose command again.

## Step 6: Validate Deployment

```shell
docker compose --profile gateway --profile sra ps
curl -f http://localhost:8080/health
```

Expected output includes lines similar to (some columns were removed from the sample output):

```text
NAME               SERVICE            STATUS
akeyless-gateway   akeyless-gateway   Up ## seconds (healthy)
akeyless-sra-web   akeyless-web       Up ## seconds
akeyless-sra-ssh   akeyless-ssh       Up ## seconds
redis-cache        redis-cache        Up ## seconds

Health Check Ok
```

Validation criteria:

* `curl -f http://localhost:8080/health` returns `Health Check Ok`.
* `docker compose --profile gateway --profile sra ps` shows `akeyless-gateway`, `akeyless-sra-web`, `akeyless-sra-ssh`, and `redis-cache` as `Up`.
* `redis-cache` must not be in `Restarting` state.

## Step 7: Access the Services

* Gateway endpoint: `http://localhost:8000`
* SRA portal: `http://localhost:8000/sra/portal/`

> ℹ️ **Note: Windows troubleshooting**
>
> The SRA portal's supported authentication methods are: Certificate, LDAP, OIDC, and SAML.

### Troubleshooting

If `http://localhost:8000` shows **Authentication failed** when using the same API key from `gateway.env`:

* Verify `GATEWAY_ACCESS_ID`, `GATEWAY_ACCESS_TYPE`, and `GATEWAY_ACCESS_KEY` are correct and from the same auth method.
* Ensure the login identity is included in `ALLOWED_ACCESS_PERMISSIONS` (configured in Step 2).
* If needed, test with another authorized Akeyless auth method configured in `ALLOWED_ACCESS_PERMISSIONS`.
* Recreate services after env-file changes:

    ```shell
    docker compose --profile gateway --profile sra down
    docker compose --profile gateway --profile sra up -d
    ```

## Related Reference Pages

* [Docker Compose](https://docs.akeyless.io/docs/gateway-compose)
* [Advanced Configuration (Docker)](https://docs.akeyless.io/docs/advanced-configuration)
* [Gateway Configuration Manager](https://docs.akeyless.io/docs/gateway-configuration-manager)
