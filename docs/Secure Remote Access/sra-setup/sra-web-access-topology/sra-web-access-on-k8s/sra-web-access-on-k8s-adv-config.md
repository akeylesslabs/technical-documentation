---
title: Zero Trust Web Access on K8s Advanced Configuration
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
<Callout icon="far fa-circle-info" theme="info">
  ### Using an earlier version

  This page describes ZTWA Helm chart 4.0.0 (app version 3.0.0) and the current Docker Compose file. For earlier versions, see [Zero Trust Web Access on K8s Advanced Configuration (earlier versions)](https://docs.akeyless.io/docs/zero-trust-web-access-on-k8s-advanced-configuration-legacy).
</Callout>

## Cluster name

```yaml values.yaml
config:
  clusterName: defaultCluster
```

Each ZTWA bastion is identified by its **ZTWA Access ID** (`config.ztwaAuth.ztwaAccessID`) together with its **cluster name**. Changing either one registers a new bastion.

Set a meaningful cluster name from the start, for example `ztwa-us-west-prod`. The default is `defaultCluster`.

## Outbound proxy

To send the pods' outbound traffic through your proxy server, set the proxy for HTTP and HTTPS traffic, and use `no_proxy` for hosts that should bypass it, such as cluster-internal addresses:

```yaml values.yaml
httpProxySettings:
  http_proxy: ""
  https_proxy: ""
  no_proxy: ""
```

This is the pods' own outbound proxy. It isn't the ZTWA web proxy that users connect through in proxy mode.

## Browser policies

The web workers run Chromium. `webWorker.config.policies` sets its managed policies, in [Chrome Enterprise policy](https://chromeenterprise.google/policies/) JSON format.

By default, every site is blocked (`"URLBlocklist": ["*"]`) except the ones in `URLAllowlist`, so users can't browse away from the target inside the isolated browser. To allow more sites, add them to `URLAllowlist`:

```yaml values.yaml
webWorker:
  config:
    policies: |
        {
          ...
          "URLBlocklist": ["*"],
          "URLAllowlist": [
            "akeyless.io",
            ...
            "internal-app.example.com"
          ]
        }
```

<Callout icon="⚠️" theme="warn">
  ### **Warning:**

  `webWorker.config.policies` replaces the whole policies JSON. Copy the default `policies` from the chart's `values.yaml` and add to it, so you keep the security defaults and the entries ZTWA needs, such as `localhost:12411`.
</Callout>

The chart checks the policies JSON with `jq`. If it isn't valid JSON, the web workers don't start.

## Private CA for the Gateway

If your Akeyless Gateway's certificate isn't signed by a public CA, create a Secret with the CA certificate under the key `tls.crt`:

```shell
kubectl create secret generic gateway-ca \
  --from-file=tls.crt=<PATH_TO_CA_CERT> \
  --namespace <NAMESPACE>
```

Then set:

```yaml values.yaml
config:
  gatewayCert:
    tlsExistingSecret: gateway-ca
```

The chart mounts the certificate in the dispatcher, the web workers and the web proxy.

## Redirect URLs

The SRA Portal redirects users only to the URLs you allow:

```yaml values.yaml
config:
  # External URLs of the dispatcher, on port 9000 or its ingress host
  allowedBastionUrls:
    - "https://ztwa.example.com:9000"
  # External URLs of the web proxy, on port 19414, for proxy-mode sessions
  allowedProxyUrls:
    - "https://ztwa-proxy.example.com:19414"
```

With a `LoadBalancer` Service, the external address is known only after the first install. Set the URLs then, and run `helm upgrade`.

## Media server

The media server runs on every node and streams the live view of each session to the user's browser.

```yaml values.yaml
mediamtx:
  # UDP port opened on every node. Users' browsers must reach it.
  iceUDPPort: 8189
  # More addresses to offer browsers, for example a public IP,
  # when users can't reach the nodes' IPs.
  additionalHosts: []
  # Limit the media server to some nodes. It must run on every node that runs web workers.
  nodeSelector: {}
  tolerations: []
```

A media server restart ends the live view and the recording of every session on its node, so `helm upgrade` doesn't restart it. To move a node's media server to a new version, delete its pod when the node has no active sessions:

```shell
kubectl delete pod <MEDIAMTX_POD_NAME> --namespace <NAMESPACE>
```

## Display size

Set the screen size of the isolated browser:

```yaml values.yaml
webWorker:
  config:
    displayWidth: 2560
    displayHeight: 1200
```

## Disable fullscreen mode

When set to `true`, this option disables the default fullscreen mode for web access sessions and shows the browser address bar:

```yaml values.yaml
webWorker:
  env:
    - name: DISABLE_FULLSCREEN
      value: "true"
```

## IPv6 and dual-stack

ZTWA runs on IPv4, dual-stack and IPv6-only clusters. To expose the Services on both IP families on a dual-stack cluster, set:

```yaml values.yaml
ipFamilyPolicy: PreferDualStack
ipFamilies: [IPv6, IPv4]
```

Leave both empty to use the cluster default. On an IPv6-only cluster, pods need NAT64/DNS64 to reach IPv4-only endpoints, such as the Akeyless Gateway or S3.