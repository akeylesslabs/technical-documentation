---
title: SRA Advanced Configuration
excerpt: Secure Remote Access Bastion
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
############
## Global ##
############
clusterName: defaultCluster
```

Each Bastion is uniquely identified by combining the **Privilege Access ID**  Authentication Method and the **Cluster Name**.

It means that changing the  **Privilege Access ID** or the **Cluster Name** of your Bastion instance will create an entirely new Bastion instance.

It is recommended to set a meaningful Cluster Name for your Bastion cluster from the very beginning. By default, your cluster name is **defaultCluster**.

To do that, you can set the `clusterName="meaningful-cluster-name"`field as part of the Bastion deployment.

# SSH Legacy Algorithm

```yaml
############
## Global ##
############
legacySigningAlg: "false"
```

As both classic SSH and RDP access are based on SSH certificates, to support legacy algorithms for SSH signing, please set the `legacySigningAlg` with `true` to sign the SSH certificates using the legacy '[ssh-rsa-cert-v01@openssh.com](mailto:ssh-rsa-cert-v01@openssh.com)' signing algorithm.

# RDP User Acces

Set the `usernameSubClaim` with the relevant attribute that exists inside your IDP JWT, e.g. `email`, to set the connection to your target server using the current authenticated username. 

```yaml
############
## Global ##
############
usernameSubClaim:
# Optional, This overrides (for RDP only) the global parameter usernameSubClaim
RDPusernameSubClaim:
# Optional, This overrides (for SSH only) the global parameter usernameSubClaim
SSHusernameSubClaim:
```

This will take effect on all SSH-based sessions, both for RDP and Linux-based systems. To split the use case when to extract the `usernameSubClaim` you can set instead a dedicated setting for each type. 

# Proxy

To configure your proxy settings, you can set several parameters, including proxy settings for HTTP traffic, HTTPS traffic, and Ignore Hosts, using the `no_proxy` field, to prevent local traffic from going through your proxy server.

```yaml
# Linux system HTTP Proxy
httpProxySettings:
  http_proxy: ""
  https_proxy: ""
  no_proxy: ""
```

# Session Recording

SRA supports the recording of RDP, SSH, DB & K8s sessions.

CLI-based sessions of **SSH**, **DB** & **K8s** connections provide a full transcript of Input commands and Output responses which can be forwarded to any Log Management / SIEM solution (such as Splunk, ElasticSearch, or just using Syslog) - for more information, see: [https://docs.akeyless.io/docs/ssh-log-forwarding](https://docs.akeyless.io/docs/ssh-log-forwarding)

**RDP** sessions provide video recordings that can be saved to AWS S3 buckets or Azure Blob storage -To work with session recording for RDP, provide the following settings to upload your recording to an S3 bucket or to an Azure Blob storage:  

```yaml AWS S3
config:
    rdpRecord:
      enabled: true
      keepLocalRecording: false
      # automatically upload session recordings to S3 in your AWS account
      s3:
        region: ""
        bucketName: ""
        bucketPrefix: ""
        # optional, run with explicit credentials (without AWS IAM roles)
        awsAccessKeyId: ""
        awsSecretAccessKey: ""

      # Specifies an existing secret to be used for bastion, management AWS credentials
      existingSecret: ""
```
```yaml Azure Blob
config:
    rdpRecord:
      enabled: true
      keepLocalRecording: false
      # automatically upload session recordings to Blob storage in your Azure account
      azure:
        storageAccountName: ""
        storageContainerName: ""
        # optional, run with explicit credentials (without Azure IAM roles)
        azureClientId: ""
        azureClientSecret: ""
        azureTenantId: ""
        
      # Specifies an existing secret to be used for bastion, management AWS credentials
      existingSecret: ""
```

To authenticate using an explicit **AWS Key**  provide the relevant `awsAccessKeyId` with the matching`awsSecretAccessKey`, or using an existing **K8s Secret** containing those credentials using `existingSecret` setting, alternatively the authentication against your **S3 Bucket** will be done based on the instance **IAM Role**. 

To store local recordings inside your Bastion server, set the `KeepLocalRecording` with `true`, session recordings will be stored inside the bastion under `/home/akeyless/recordings`.

# Session Management

To revoke an existing session from your [Akeyless Gateway Overview](https://docs.akeyless.io/docs/api-gw) or your IdP like Okta, or Keycloak, enable the `sessionTermination` and set the `apiURL` to your Gateway, or to your IdP URL.

```yaml
sessionTermination:
    ## Session Termination is available for Akeyless GW, okta and keycloak
      enabled: true
      apiURL: ""
      apiToken: ""
```

# Log Forwarding

To enable log forwarding to an existing log management system, please find a list of available target systems and configurations on [this](https://docs.akeyless.io/docs/ssh-log-forwarding) page.

# Redirect to Bastion URLs

To ensure only validated redirects are accepted, you can harden your bastion using the `allowedBastionUrls` variable with a list of URLs that will be considered valid for redirection from the Akeyless Zero Trust Portal back to the relevant **web-bastion**: 

```yaml
ztbConfig:
  # List of URLs that will be considered valid for redirection from the Portal back to the bastion
  allowedBastionUrls: []
```

# Concurrent Unauthenticated Connections

To specify the maximum number of concurrent unauthenticated connections to the SRA Bastion, set the following `env` variable under the  `sshConfig` as follows:

```yaml
sshConfig:
  env:
    - name: CONFIG_MAX_STARTUPS
      value: "200:30:300"
```

# SSH Fingerprint

To accept the SSH Bastion host key fingerprint automatically without re-accepting it after upgrades etc. You can set an environment variable as part of the chart deployment with a dedicated folder within your Akeyless account. The SRA bastion will automatically store the relevant fingerprints within that folder. In this example, we will store the fingerprints inside `/MY_SSH_BASTION_HOST_KEYS` folder.\
Note, please  ensure your Bastion default Auth Method has the following permissions on that folder `create`,`read`, `list`:

```yaml
sshConfig:
  env:
    - name: SSH_HOST_KEYS_PATH
      value: /MY_SSH_BASTION_HOST_KEYS
```

# Self-Hosted Zero Trust Portal

To deploy a self-hosted instance of the Akeyless Zero trust portal as part of this chart, you can enable the `ztpConfg`:

```yaml
####################################################
## Default values for akeyless-zero-trust-portal ##
####################################################
ztpConfig:
  # Enable akeyless-zero-trust-portal.
  enabled: true
  replicaCount: 1
  containerName: "zero-trust-portal"
  image:
    repository: akeyless/zero-trust-portal
    pullPolicy: Always
    # tag: latest
  service:
    # Remove the {} and add any needed annotations regarding your LoadBalancer implementation
    annotations: {}
    labels: {}
    type: LoadBalancer
    port: 8080
```

# Support for Other Keyboard Layouts

To enable support for other keyboard layouts in your remote sessions (ie Windows), find the `ztbConfig` section and add the `KEYBOARD_LAYOUT` variable name and value (the default is `en-us-qwerty`) to the `env` as follows:

```yaml
####################################################
## Default values for akeyless-zero-trust-bastion ##
####################################################

ztbConfig:

  env:
    - name: KEYBOARD_LAYOUT
      value: fr-fr-azerty # Other options can be found below
```
```yaml Layout Options
value: da-dk-qwerty # Danish (Qwerty)
value: de-ch-qwertz # Swiss German (Qwertz)
value: de-de-qwertz # German (Qwertz)
value: en-gb-qwerty # UK English (Qwerty)
value: en-us-qwerty # US English (Qwerty) default
value: es-es-qwerty # Spanish (Qwerty)
value: es-latam-qwerty # Latin American (Qwerty)
value: fr-be-azerty # Belgian French (Azerty)
value: fr-ch-qwertz # Swiss French (Qwertz)
value: fr-fr-azerty # French (Azerty)
value: hu-hu-qwertz # Hungarian (Qwertz)
value: it-it-qwerty # Italian (Qwerty)
value: ja-jp-qwerty # Japanese (Qwerty)
value: no-no-qwerty # Norwegian (Qwerty)
value: pl-pl-qwerty # Polish (Qwerty)
value: pt-br-qwerty # Portuguese Brazilian (Qwerty)
value: sv-se-qwerty # Swedish (Qwerty)
value: tr-tr-qwerty # Turkish-Q (Qwerty)
```

For further configuration, please refer to the Akeyless official [repository](https://github.com/akeylesslabs/helm-charts/blob/main/charts/akeyless-secure-remote-access/README.md#zero-trust-portal-parameters).
