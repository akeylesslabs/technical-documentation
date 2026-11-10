---
title: Zero Trust Web Access
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
This page describes the Zero Trust Web Access (ZTWA) runtime topology and the key deployment settings for Kubernetes and Docker Compose.

<Callout icon="far fa-circle-info" theme="info">
  ### Using an earlier version

  This page describes ZTWA Helm chart 4.0.0 (app version 3.0.0) and the current Docker Compose file. For earlier versions, see [Zero Trust Web Access (earlier versions)](https://docs.akeyless.io/docs/zero-trust-web-access-on-k8s-legacy).
</Callout>

## Architecture and Traffic Flow

ZTWA uses four components:

* **Dispatcher**: Entry point that authenticates requests and dispatches session traffic
* **Web worker**: Isolated browser runtime that serves user sessions
* **Web proxy**: Proxy for proxy-mode sessions (HTTP or SOCKS5), with its own Service
* **Media server**: Streams the live view of the session to the user's browser over WebRTC, and records sessions when recording is enabled. One runs on every node.

### Component Responsibilities

**Dispatcher:**

* Handles the user-side session connection from the portal flow
* Applies access policy decisions before a worker session is established
* Selects and routes traffic to an available web worker instance

**Web worker:**

* Launches and maintains the isolated browser runtime for the approved session
* Establishes outbound connectivity from the worker runtime to the target application
* Keeps user browsing activity isolated from other sessions

**Web proxy:**

* Serves proxy-mode sessions, where the user's own browser connects through ZTWA
* Uses HTTP by default, or SOCKS5

**Media Server:**

* Streams the web worker's screen to the user's browser over WebRTC
* Records the session to the shared volume when recording is enabled

### **Traffic flow**

**Isolated browser mode (default):**

1. The user requests access in the SRA Portal.
2. The dispatcher receives the request and checks authentication and policy.
3. The dispatcher selects an available web worker.
4. The web worker opens the target web application in an isolated browser.
5. The media server on the worker's node streams the live view to the user's browser over WebRTC.

**Proxy Mode:** the user's own browser connects to the target through the web proxy on port `19414`.

## Required Topology Settings

### ZTWA Authentication

ZTWA uses its own Akeyless identity to read the secrets of the web targets on the user's behalf. Users only need List permission on those secrets.

* **ZTWA Access ID**: the auth method ZTWA uses. It needs Read and List permissions on the secrets of the web targets.
* **Authorized Access IDs**: the auth methods allowed to open ZTWA sessions, for example your SAML auth method.

<Callout icon="far fa-triangle-exclamation" theme="warn">
  ### Authorized Access IDs are required

  If the list of authorized Access IDs is empty, the dispatcher and the web proxy accept no users.
</Callout>

### Redirect URLs

The SRA Portal redirects users only to URLs you allow:

* **Allowed bastion URLs**: the external URL of the dispatcher, on port `9000` or its ingress host
* **Allowed proxy URLs**: the external URL of the web proxy, on port `19414`, for proxy-mode sessions

**Proxy Mode:**

* The web proxy listens on port 19414.
* It uses HTTP by default. Set `WEB_PROXY_TYPE` to SOCKS for SOCKS5.

For SOCKS5 protocol details, see [RFC 1928](https://www.rfc-editor.org/rfc/rfc1928).

### HTTP Deployments

When the dispatcher is served over `HTTP` instead of `HTTPS`, keep the secure cookie flag disabled (`disableSecureCookie: "true"`, the default). Otherwise, the browser doesn't send the session cookie.

For browser cookie security behavior, see [MDN Set-Cookie: Secure](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#secure).

### Ports

| Port        | Component                         | Must be reachable from            |
| ----------- | --------------------------------- | --------------------------------- |
| `9000/TCP`  | Dispatcher                        | Users' browsers                   |
| `19414/TCP` | Web Proxy                         | Users' browsers (proxy mode only) |
| `8189/UDP`  | Media server (ICE), on every node | Users' browsers                   |

If your nodes aren't reachable from users' networks, add the address users can reach, for example a public IP, in `mediamtx.additionalHosts`.

## Platform Variable Mapping

| Behavior              | Docker Compose                                    | Kubernetes (Helm)                     |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| ZTWA Access ID        | `ZTWA_ACCESS_ID`                                  | `config.ztwaAuth.ztwaAccessID`        |
| Authorized Access IDs | `AUTHORIZED_ACCESS_IDS`                           | `config.ztwaAuth.authorizedAccessIDs` |
| Allowed bastion URLs  | `ALLOWED_BASTION_URLS`                            | `config.allowedBastionUrls`           |
| Allowed proxy URLs    | `ALLOWED_PROXY_URLS`                              | `config.allowedProxyUrls`             |
| Proxy protocol        | `WEB_PROXY_TYPE`                                  | `WEB_PROXY_TYPE` in `webProxy.env`    |
| HTTP cookie behavior  | `DISABLE_SECURE_COOKIE`                           | `config.disableSecureCookie`          |
| Worker discovery      | `SERVICE_DNS` (for example, `SERVICE_DNS=worker`) | Generated by the chart                |

## Platform Guides

* Kubernetes deployment and values: [Zero Trust Web Access on K8s](https://docs.akeyless.io/docs/sra-web-access-on-k8s)
* Docker Compose deployment and env values: [Zero Trust Web Access on Docker](https://docs.akeyless.io/docs/sra-web-access-docker)
* Chromium browser policies, private CA certificate handling, and advanced options: [Zero Trust Web Access Advanced Configuration](https://docs.akeyless.io/docs/sra-web-access-on-k8s-adv-config)