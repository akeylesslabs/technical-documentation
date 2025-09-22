---
title: Web Access Advanced Configuration
excerpt: Web Access Bastion
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
# Cluster Name

```yaml
clusterName: defaultCluster
```

Each Bastion is uniquely identified by combining the **Privilege Access ID**  Authentication Method and the **Cluster Name**.

It means that changing the  **Privilege Access ID** or the **Cluster Name** of your Bastion instance will create an entirely new Bastion instance.

It is recommended to set a meaningful Cluster Name for your Bastion cluster from the very beginning. By default, your cluster name is **defaultCluster**.

To do that, you can set the <code>clusterName="meaningful-cluster-name"</code> field as part of the Bastion deployment.

# Proxy

To configure your proxy settings, you can set several parameters, including proxy settings for HTTP traffic, HTTPS traffic, and Ignore Hosts, using the `no_proxy` field, to prevent local traffic from going through your proxy server.

```yaml
# Linux system HTTP Proxy
httpProxySettings:
  http_proxy: ""
  https_proxy: ""
  no_proxy: ""
```

# Log Forwarding

To enable log forwarding to an existing log management system, please find a list of available target systems and configurations on [this](https://docs.akeyless.io/docs/ssh-log-forwarding) page.

```yaml
logForward: |
       target_log_type="splunk"
       target_splunk_sourcetype=""
       target_splunk_source=""
       target_splunk_index=""
       target_splunk_token=""
       target_splunk_url=""
```

# WebWorker

This section enables global settings of the internal dedicated remote browsers your users will use. You can customize the settings to provide a more flexible experience for your users. 

Default `policies` sections aimed to provide the most secure work mode. By default, all `URLs` are blocked hence users will not be able to navigate inside the remote browser to different sites. If needed, set the relevant `URLs` in the `Exceptions` list. 

```yaml
webWorker:
  config:
    displayWidth: 2560
    displayHeight: 1200
    policies: |
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
              "Mode": "none",
              "Locked": true
            },
            "Preferences": {},
            "Certificates": {
#              "Install": ["/etc/ssl/certs/yourOrgRootCA.crt"]
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
```

**Notice:** If your organization uses private certificate authorities (CAs) to issue certificates for your internal web apps, and you either wish to access those websites through the web-access-bastion, or if your **apiGatewayURL** is pointing to a **Gateway** that uses such a certificate, you must configure the WebWorkers as follows:

1. Mount your organization's Root CA certificate to the pods. For the **Gateway** specifically, in the helm-chart, you can specify an existing k8s-secret for the gateway tls certificate under **apiGatewayCert.tlsCertsSecretName** (see [ztwa/values.yaml](https://github.com/akeylesslabs/helm-charts/blob/main/charts/akeyless-zero-trust-web-access/values.yaml))
2. In the `policies.json` above, uncomment the _Certificates.Install_ line and set it to the relevant certificates' paths inside the pod

# DLP

To work with Data Leak Protection (DLP) tools, you can explicitly set the target settings of your DLP server, as well as with dedicated audit logs forwarding.

```yaml
dlp:
  enabled: false
  config:
    hostAddress: ""
    # host/{pathPrefix}
    pathPrefix: ""
    # FORCING or LEARNING
    mode: ""
    logLevel: "INFO"
  audit: |
    target_log_type="splunk"
    target_splunk_sourcetype=""
    target_splunk_source=""
    target_splunk_index=""
    target_splunk_token=""
    target_splunk_url=""
```

# Redirect to Bastion URLs

To ensure only validated redirects are accepted, you can harden your bastion using the `allowedBastionUrls` variable with a list of URLs that will be considered valid for redirection from the Akeyless Zero Trust Portal back to the relevant **web-dispatcher-bastion**: 

```yaml
dispatcher:
config:
    # List of URLs that will be considered valid for redirection from the Portal back to the bastion
    allowedBastionUrls: []
```

# Disable Fullscreen Mode

When set to `true`, this option disables the default fullscreen mode for Web Access sessions and also shows the internal browser address bar. To use this feature, the following should be added in the `webWorker` section under `env`:

```yaml
webWorker:
	env:
  - name: DISABLE_FULLSCREEN
  	value: "true"
```