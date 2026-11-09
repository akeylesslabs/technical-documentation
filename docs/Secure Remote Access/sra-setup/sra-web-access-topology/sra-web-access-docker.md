---
title: Zero Trust Web Access on Docker
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
Akeyless Zero Trust Web Access (ZTWA) gives users secure access to internal web applications through an isolated Chromium browser, with optional session recording. Users never see the target's credentials.

This guide deploys ZTWA with Docker Compose. For how the components fit together, see [Zero Trust Web Access](https://docs.akeyless.io/docs/sra-web-access-topology).

## Before you begin

### Requirements

* Docker with Docker Compose installed.
* The ZTWA [`docker-compose.yml`](https://github.com/akeylesslabs/helm-charts/blob/main/docker-compose/akeyless-zero-trust-web-access/docker-compose.yml) file.
* At least 1 vCPU and 1 GB RAM for the dispatcher, and 1 vCPU and 2 GB RAM for each web worker.

<Callout icon="⚠️" theme="warn">
  ### **Warning:**

  To enable Secure Remote Access features, request access to the Akeyless private repository from your account manager.
</Callout>

### Services

The `docker-compose.yml` file runs these services:

| Service      | Purpose                                                  | Host port  |
| ------------ | -------------------------------------------------------- | ---------- |
| `dispatcher` | Entry point; checks authentication and assigns sessions  | `9000`     |
| `worker`     | Isolated Chromium browser that runs the user's session   | —          |
| `proxy`      | Web proxy for proxy-mode sessions                        | `19414`    |
| `mediamtx`   | Media server; streams the live view and records sessions | `8189/UDP` |
| `autoheal`   | Restarts containers whose health check fails             | —          |

### Network

* **UDP&#x20;**`8189` on the Docker host must be reachable from users' browsers. The live view of each session uses it.
* Set the address users reach the host on in the `mediamtx` service. See [Set the media server address](https://docs.akeyless.io/docs/sra-web-access-docker#set-the-media-server-address).

### Network timeout settings

When an embedded browser session runs behind a load balancer (for example, ELB), idle timeout settings can close active sessions. Set the load balancer idle timeout to a high value or unlimited.

For AWS ELB guidance, see [Configure idle connection timeout](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console).

### Shared storage

The dispatcher, the web workers and the media server mount the `$PWD/shared` folder at `/etc/shared`, for file downloads and session recordings. Limit its permissions to `0650`, and make it owned by group `10000`.

## Configure docker-compose.yml

### Credentials

Create a `.env` file next to `docker-compose.yml`. Docker Compose reads it automatically. Don't commit it to source control.

```shell .env
# Auth method ZTWA uses to read the secrets of the web targets (Read and List permissions)
ZTWA_ACCESS_ID=<ZTWA_ACCESS_ID>
# Only for an API Key auth method
ZTWA_ACCESS_KEY=<ACCESS_KEY>
# Auth methods allowed to open sessions, comma separated, for example your SAML auth method
AUTHORIZED_ACCESS_IDS=<ACCESS_ID_1>,<ACCESS_ID_2>
```

The dispatcher and the web proxy both read `AUTHORIZED_ACCESS_IDS` from this file.

### ZTWA authentication

ZTWA reads the secrets of the web targets with its own auth method, the **ZTWA Access ID**. It needs **Read** and **List** permissions on those secrets. Users only need **List**.

<Callout icon="⚠️" theme="warn">
  ### **Warning:**

  `AUTHORIZED_ACCESS_IDS` is required. If it's empty, the dispatcher and the web proxy accept no users.
</Callout>

Supported auth method types: [API Key](https://docs.akeyless.io/docs/auth-with-api-key), [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws), [Azure AD](https://docs.akeyless.io/docs/auth-with-azure) and [GCP](https://docs.akeyless.io/docs/auth-with-gcp).

* **API key:** set `ZTWA_ACCESS_ID` and `ZTWA_ACCESS_KEY` in `.env`.
* **Cloud identity (AWS IAM, Azure AD, GCP):** set only `ZTWA_ACCESS_ID`. ZTWA detects the cloud through the instance metadata service. If the container can't reach it, set `ZTWA_ACCESS_TYPE` on the dispatcher:

  ```yaml docker-compose.yml
  services:
    dispatcher:
      environment:
        - ZTWA_ACCESS_TYPE=aws_iam   # or azure_ad, gcp
  ```

### Set the media server address

In the `mediamtx` service, replace `<MUST_BE_PROVIDED>` with the IP or hostname users' browsers reach the Docker host on:

```yaml docker-compose.yml
services:
  mediamtx:
    environment:
      - MTX_WEBRTCADDITIONALHOSTS=<HOST_IP_OR_HOSTNAME>
```

### Redirect URLs

The SRA Portal redirects users only to the URLs you allow. In the `dispatcher` service, set them comma separated:

```yaml docker-compose.yml
services:
  dispatcher:
    environment:
      - ALLOWED_BASTION_URLS=https://<HOST>:9000
      - ALLOWED_PROXY_URLS=https://<HOST>:19414
```

Use the same URLs in the [SRA Portal](https://docs.akeyless.io/docs/sra-portal):

* **Web Application Dispatcher**: the dispatcher URL
* **Web Proxy URL**: the web proxy URL, for proxy-mode sessions

### Akeyless API URL

Keep the default for the Akeyless SaaS, or set the API URL of your Akeyless Gateway. Set the same value on the `dispatcher` and the `proxy` services:

```yaml docker-compose.yml
services:
  dispatcher:
    environment:
      - GATEWAY_URL=https://api.akeyless.io
  proxy:
    environment:
      - GATEWAY_URL=https://api.akeyless.io
```

If your Gateway's certificate isn't signed by a public CA, mount the CA bundle and set `GATEWAY_CERT` on the `dispatcher`, `proxy` and `worker` services:

```yaml docker-compose.yml
    volumes:
      - /path/to/your-ca-bundle.pem:/var/akeyless/certs/ca-bundle.pem:ro
    environment:
      - GATEWAY_CERT=/var/akeyless/certs/ca-bundle.pem
```

### Proxy mode

The web proxy uses HTTP by default. For SOCKS5, set on the `proxy` service:

```yaml docker-compose.yml
services:
  proxy:
    environment:
      - WEB_PROXY_TYPE=SOCKS
```

### HTTP deployments

`DISABLE_SECURE_COOKIE=true` (the default) lets the dispatcher work over HTTP. Set it to `false` to send the session cookie only over HTTPS.

`ALLOWED_INTERNAL_AUTH=false` (the default) makes the dispatcher accept only requests with preemptive JWT authentication.

### Session recording

The media server records each session to the shared folder, and the dispatcher uploads it to S3 or S3-compatible storage.

1. Turn on recording in both services:

   ```yaml docker-compose.yml
   services:
     mediamtx:
       environment:
         - MTX_PATHDEFAULTS_RECORD=yes
     dispatcher:
       environment:
         - ENABLE_RECORDING=true
   ```

2. To upload to S3, set on the `dispatcher` service:

   ```yaml docker-compose.yml
   services:
     dispatcher:
       environment:
         - ENABLE_RECORDING_UPLOAD=true
         - RECORDING_S3_BUCKET=<S3_BUCKET_NAME>
         - RECORDING_S3_REGION=<AWS_REGION>
         - RECORDING_S3_PREFIX=          # optional
         - RECORDING_S3_ENDPOINT=        # S3-compatible service, for example MinIO. Empty for AWS S3
         - RECORDING_COMPRESS=false      # gzip before upload
         - RECORDING_SSE_TYPE=           # empty, sse-s3 or sse-kms
         - RECORDING_SSE_KMS_KEY_ID=     # for sse-kms. Empty uses the default KMS key
   ```

3. Put the S3 credentials in `.env`. Without them, the dispatcher uses the AWS default credential chain, for example an instance profile:

   ```shell .env
   RECORDING_S3_ACCESS_KEY_ID=<ACCESS_KEY_ID>
   RECORDING_S3_ACCESS_KEY_SECRET=<SECRET_ACCESS_KEY>
   ```

## Advanced configuration

### Cluster name

```yaml docker-compose.yml
services:
  dispatcher:
    environment:
      - CLUSTER_NAME=compose-ztwa
```

Each ZTWA bastion is identified by its **ZTWA Access ID** together with its **cluster name**. Changing either one registers a new bastion. Set a meaningful cluster name from the start. The default is `compose-ztwa`.

### Outbound proxy

To send a service's outbound traffic through your proxy server, set `http_proxy`, `https_proxy` and `no_proxy` on that service:

```yaml docker-compose.yml
services:
  dispatcher:
    environment:
      - http_proxy=
      - https_proxy=
      - no_proxy=
```

This is the containers' own outbound proxy. It isn't the ZTWA web proxy that users connect through in proxy mode.

### Display size

Set the screen size of the isolated browser on the `worker` service:

```yaml docker-compose.yml
services:
  worker:
    environment:
      - DISPLAY_WIDTH=2560
      - DISPLAY_HEIGHT=1200
```

## Install

1. Start ZTWA:

   ```shell
   docker compose up -d
   ```

2. Check that all services are running:

   ```shell
   docker compose ps
   ```
