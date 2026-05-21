---
title: Certificate Discovery
deprecated: false
hidden: false
metadata:
  robots: index
---
Certificate Discovery helps you continuously locate and inventory certificates across your environments by scanning targets such as individual **IPs**, **CIDR** ranges, and **DNS** names. You can configure discovery to probe specific ports or port ranges, enabling coverage for both standard and custom TLS deployments.

When a certificate is found, Akeyless automatically creates a corresponding certificate record with all available metadata, including where it was discovered (target and endpoint details) and the certificate’s key attributes. You can also predefine expiration event settings so newly discovered certificates are immediately tracked and monitored without manual onboarding.

> ✅ **Tip:** This feature is **Early Access** and is available only when using a [Gateway](https://docs.akeyless.io/docs/gateway-overview) running version `4.46.0` or later.

Certificate Discovery requires an Akeyless Gateway deployment running version `4.46.0` or later. If the environment reports only `akeyless-api-proxy`, confirm compatibility with Product or Support before troubleshooting network and DNS behavior.

Certificate Discovery visibility in the Akeyless Console depends on account permissions and enabled product capabilities.

## Discovery Behavior by Source Type

Certificate Discovery behavior depends on the source type:

* Public domain sources use public certificate transparency data and certificate authority logs.
* Internal domain sources are queried directly by fully qualified domain name (FQDN).
* Internal subdomains must be provided explicitly. Discovery does not infer unregistered private subdomains.
* IP and CIDR sources follow direct network-based discovery from the gateway.

For internal and network-based sources, the gateway must have network and DNS access to each target endpoint.

## Running a Certificate Discovery with the CLI

To run a certificate discovery using the CLI, run the following command:

```shell
akeyless certificate-discovery \
--hosts <IPs, CIDR ranges, or DNS names> \
--port-ranges[=443] <80,8080-8085> \
--target-location 'Discovery-Folder' \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--debug
```

Where:

* `hosts`: **Required**, A comma-separated list of **IPs**, **CIDR ranges**, or **DNS names** to scan.

* `port-ranges[=443]`: A comma-separated list of port ranges. Example: `80`, `8080`-`8085`.

* `target-location`: **Required**, The folder the certificates that were found in the scan will be saved at.

* `expiration-event-in`: How many days before the expiration of the certificate would you like to be notified. To specify multiple events, use argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`.

* `debug`: Optional, Enables debug output for troubleshooting.

### UI and CLI field mapping

Use the following mapping when translating Console fields to CLI flags:

| Console field | CLI flag |
| --- | --- |
| Sources | `--hosts` |
| Ports | `--port-ranges` |
| Target Location | `--target-location` |

## Setting a Certificate Discovery in the Akeyless Console

1. Log in to the Akeyless Console, and go to **Discovery & Migration**, then **New**, then **Certificate Discovery**.
2. Define a Name for the certificate discovery, and specify the **Target Location** as a path to the virtual folder where you want the scanned certificates to be saved in. If the folder does not exist, it will be created together with the scanned certificates.
3. Add the **Sources** of the scan, such as: **IPs**, **CIDR ranges**, or **DNS names**
4. Add the relevant ports, the default value is `443`.
5. Press **Finish**.

## Run the Certificate Discovery

To run the discovery, select the discovery item and choose **Action Menu**, then **Start Scan**. If the scan completes successfully, a new folder will appear under **Items** containing all the certificates that were found.

## Troubleshooting Certificate Discovery

Use the following checks when discovery results are incomplete or unclear:

1. Confirm deployment type. Certificate Discovery requires an Akeyless Gateway deployment. If the environment reports only `akeyless-api-proxy`, confirm compatibility with Product or Support before proceeding.
2. Confirm network path from the gateway. Discovery traffic originates from the gateway container, not from the local client session.
3. Check discovery and migration logs in the gateway Docker container.
4. Run discovery with debug output:

  ```shell
  akeyless certificate-discovery \
  --hosts <IPs, CIDR ranges, or DNS names> \
  --port-ranges[=443] <80,8080-8085> \
  --target-location '<target-location>' \
  --gateway-url 'https://<your-akeyless-gw-url>:8000' \
  --debug
  ```

1. Interpret report counters by target execution status. For example, `4 total, 4 failed` indicates four scan targets failed processing. It does not indicate that four certificates were discovered and then failed import.
2. Use AI Insights in the Active Directory migration flow when local file system certificate discovery is required for internal processes that are not reachable over the network.

> ℹ️ **Note:** Discovery and migration logs are currently written inside the gateway container. A future update is expected to move logging to STDOUT-only output.
