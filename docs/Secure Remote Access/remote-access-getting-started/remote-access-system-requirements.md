---
title: System Requirements
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
# System Architecture

Akeyless Secure Remote Access offers two types of solutions, each providing distinct capabilities as follows:

## Remote Access

This provides secure access to resources using just-in-time dynamic secrets, rotated secrets, or SSH certificates. 

It can be deployed on Docker Compose or Kubernetes and creates two types of deployments:

### Web-SRA

The web-sra component allows access to RDP/SSH/DB target hosts from the [Zero-Trust Portal](https://zerotrust.akeyless.io) website as well as the internal portal at `http://<Your-Akeyless-GW-URL:8000>/sra/portal`.

### SSH-SRA

The ssh-sra component enables end-users to connect to targets that support CLI access (over SSH) from their own native Terminal/CLI tool with the [`akeyless connect`](https://docs.akeyless.io/docs/remote-access-akeyless-connect) command.

> Although SRA can be deployed with Docker Compose or Kubernetes, this document focuses on deploying to Kubernetes 

## Zero-Trust Web-Access (ZTWA)

This solution provides Secure Remote Access to [Web application](https://docs.akeyless.io/docs/web-applications-secure-remote-access) targets via the Zero-Trust Portal, also leveraging the Akeyless [Browser Extension](https://docs.akeyless.io/docs/browser-extensions), which opens a browser session and injects credentials into the browser for the user.

These targets are accessed using one of three methods: [Secure Web Browsing](https://docs.akeyless.io/docs/web-applications-secure-remote-access), [Secure Web Proxy](https://docs.akeyless.io/docs/web-applications-secure-remote-access), or [Direct Connections](https://docs.akeyless.io/docs/web-applications-secure-remote-access). This solution creates two types of applications as well:

- **Web Dispatcher**: Acts as a load balancer service that dispatches requests to _web-workers_ to take on secure web-browsing sessions. It enables secure web browsing by launching a Firefox browser inside the pod.
- **Web Workers**: These containers host the isolated browser sessions (for "secure web browsing") and each such container supports a single isolated browser session.

The [Akeyless SRA Browser Extension](https://docs.akeyless.io/docs/installation-of-akeyless-web-extension) is installed locally on the user's browser (Chrome, Firefox, or Edge). It provides password management capabilities and supports the SRA by managing and adapting seamless configuration to the browser.

# Minimum Resource Requirements

Each pod in the Akeyless SRA solution has the following minimum resource requirements:

- **CPU**: 1 CPU (1000m)
- **Memory**: 2 GiB

These minimum resource allocations are designed to optimize performance and ensure stable operations. Adjustments may be needed based on the specific workload and deployment size.

# Connection Handling Capabilities

- **Web-SRA and SSH-SRA Pods**: These are capable of handling between 70 to 100 simultaneous connections with a mix of SSH, DB, and other applications under the recommended resource allocation.
- **Web Dispatcher Pods**: The Web Dispatcher enables proxy protocol support and can handle hundreds of simultaneous connections, efficiently distributing the load.
- **Web Worker Pods**: Each 'web-worker' pod is designed to handle one secure web connection. For multiple secure web connections, additional 'web-worker' pods are required (e.g., 5 simultaneous secure web connections require 5 web-worker pods).

The number of pods and replication is managed with the values file during Helm installation. Multiple `ssh-sra` pods previously required a dedicated persistent volume, but it is now replaced with a local Redis deployment. This will simplify the solution and reduce the dependency on a persistent volume.

## Browser Extension Requirements

The Browser Extension is installed on the local browser and is highly recommended for the SRA environment. It enables Direct & Proxy connections for Web-Access, including advanced features such as auto-injection of passwords and additional RDP features.

## Storage Requirements

Akeyless does not require extensive storage for basic operation. However, if session recording is enabled, additional storage will be necessary. RDP session recordings are captured and saved as .m4v video files. These files can be stored locally, requiring a persistent volume, or uploaded to an S3 bucket for remote storage. The recording output rate is approximately 4 MB per minute, resulting in a file size of around 240 MB for a one-hour session.

## Recommended Server Specifications

Based on the components and their respective resource allocations, the following server specifications are recommended for deploying the Akeyless Remote Access solution:

### Minimum Specifications for Small Deployments

- **vCPUs**: 4
- **Memory**: 16 GiB
- **Storage**: 100 GiB (SSD recommended)
- **Networking**: 1 Gbps NIC

This setup is suitable for small deployments, supporting up to ~100 simultaneous ssh/application connections and several secure web applications with a combination of web-sra, ssh-sra, and web-worker pods.

### Medium to Large Deployments

- **vCPUs**: 16
- **Memory**: 32 GiB
- **Storage**: 500 GiB (SSD recommended)
- **Networking**: 10 Gbps NIC

This configuration is ideal for medium to large deployments, supporting hundreds of simultaneous connections and multiple web-worker pods.

## Additional Considerations

- **High Availability**: For production environments, it is recommended to deploy the Akeyless SRA solution in a high-availability configuration, utilizing multiple nodes and load balancers to distribute the traffic.
- **Scaling**: As the number of users and connections grows, additional resources may be required. The Kubernetes infrastructure should be monitored regularly, and autoscaling policies should be implemented to automatically adjust the number of pods based on demand.
- **Security**: Ensure that the Kubernetes cluster is secured following best practices, including network segmentation, pod security policies, and regular security audits.
- **Network**
  Long SRA sessions (SSH/RDP/Web) might be cut off early by default LB/Ingress timeouts. Set your LB/Ingress idle/response timeout ≥ your intended session TTL (e.g., 15-60 minutes):
  - **Google Cloud (GKE / Google Load Balancer)** - Default backend service timeout is 30s. Increase via BackendConfig (or GCPBackendPolicy) using `spec.timeoutSec`. Apply to the Service/Ingress used by SRA. See vendor information [here](https://cloud.google.com/kubernetes-engine/docs/how-to/ingress-configuration?utm_source=chatgpt.com)
  - **AWS (EKS / Elastic Load Balancing)** - ALB (HTTP/HTTPS): Default idle timeout = 60s. Set higher using LB attributes; with AWS Load Balancer Controller use: alb.ingress.kubernetes.io/load-balancer-attributes: idle_timeout.timeout_seconds=600 (example = 10m). See vendor information [here](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html?utm_source=chatgpt.com)
  - **NLB (TCP/TLS)**: Default TCP idle timeout = 350s; now configurable 60-6000s. Adjust if sessions may be idle, and enable TCP keepalives. See vendor information [here](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/update-idle-timeout.html?utm_source=chatgpt.com)
  - **Microsoft Azure (AKS)** - 
    - **Azure Load Balancer (L4)**: Default idle timeout = 4 minutes; configurable up to 100 minutes (Standard). Increase for SRA sessions. See vendor information [here](https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-tcp-idle-timeout?utm_source=chatgpt.com&tabs=tcp-reset-idle-portal)
    - **Application Gateway (L7):** TCP idle timeout default 4 minutes (configurable up to 30 minutes); HTTP request timeout default 20s (backend response wait). Tune both as needed. See vendor information [here](https://learn.microsoft.com/en-us/azure/application-gateway/application-gateway-faq?utm_source=chatgpt.com)
  - **NGINX Ingress (generic)** - Defaults commonly close connections around 60s without traffic. Raise with annotations / ConfigMap (e.g., nginx.ingress.kubernetes.io/proxy-read-timeout, proxy-send-timeout). See vendor information [here](https://nginx.org/en/docs/http/websocket.html?utm_source=chatgpt.com)

## Conclusion

The Akeyless Remote Access solution is designed to be flexible and scalable, capable of meeting the needs of a wide range of environments. By following the recommended server specifications and resource allocations, organizations can ensure that their deployment is both performant and reliable, providing secure remote access to their critical resources. Further information can be found on the [SRA online document page](https://docs.akeyless.io/docs/remote-access-overview).