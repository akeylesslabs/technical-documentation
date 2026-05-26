---
title: SSH Access
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
Certificate-based authentication eliminates the need to approve and distribute keys. Instead of scattering public keys across static files, you bind a public key to a username with a certificate.

Akeyless SSH Secure Remote Access enables traffic connections to servers that are not directly accessible by way of SSH but directed through a `ssh-sra` host, which proxies the connection between the SSH client and the remote servers. In addition, you can record all SSH sessions traffic and expose them to the filesystem for log forwarding.

In this guide, we will connect to a remote target using an [SSH Certificate](https://docs.akeyless.io/docs/sra-ssh-certificates).

> ℹ️ **Note (Legacy Mode):**
>
> For legacy applications that do not support SSH certificates, Akeyless offers a unique hybrid solution that involves certificates and keys.
> For more details, please refer to [Legacy mode section](https://docs.akeyless.io/docs/sra-ssh#legacy-mode) at the bottom of this page.

## Prerequisites

* [Secure Remote Access](https://docs.akeyless.io/docs/sra-setup-overview) deployment.

* An [SSH Cert Issuer](https://docs.akeyless.io/docs/sra-ssh-certificates) for certificate authentication.

* SSH sessions behind a **GKE HTTP(S)** Load Balancer may disconnect after `30` seconds due to the default backend timeout. You can increase it by configuring a BackendConfig (`spec.timeoutSec`) and annotating your Service as described in the GCP docs on [backend service timeouts](https://docs.cloud.google.com/load-balancing/docs/backend-service#timeout-setting) and [Ingress BackendConfig](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/ingress-configuration#backendconfig).

## Set Up Certificate-Based SSH Access from the Akeyless CLI

Let's set up remote access to an SSH host using the Akeyless CLI.

1. Run the `update-item` command to set the following fields on the SSH Certificate Issuer item:

```shell
akeyless update-ssh-cert-issuer \
--name <SSH Cert Issuer Name > \
--secure-access-enable true \
--secure-access-api <ssh-sra service control API endpoint URL> \
--secure-access-ssh  <ssh-sra service server IP and Port> \
--secure-access-ssh-creds-user <SSH username> \
--host-provider[=explicit] \
--secure-access-host <remote host> 
```

where:

* `secure-access-api`: Secure Access SSH control API endpoint. For example, `https://my.sra-server:9900`.

* `secure-access-ssh`: Secure Access SSH server. For example, `my.sra-server:22`.

* `secure-access-ssh-creds-user`: SSH username to connect to a target server, based on the `Allowed Users` list. Starting with Gateway **v4.45.0**, Secure Remote Access (SRA) works out of the box with any **SSH Cert Issuer** where SRA is enabled. If you’re using an older Gateway version, make sure the SSH Cert Issuer `allowed_users` includes `session_*`, so just in time users are authorized.

* `host-provider`: Host provider type by default works with explicit hosts, if you wish to work with [Linked Targets](https://docs.akeyless.io/docs/linked-target) instead, set this parameter to `target`. When `target` is selected, use the `assoc-target-item` command to attach the relevant Linked Target.

* `secure-access-host`: Target servers for connections. Repeat this flag for multiple values. Starting with SRA v2.9.0, CIDR notation is supported in addition to individual hostnames and IP addresses (for example, `192.168.1.0/24`).

* `secure-access-enforce-hosts-restriction`: When set to `true`, restricts SRA connections to only the hosts specified in `--secure-access-host`. Users attempting to connect to unlisted hosts are denied.

## Set Up Certificate-Based SSH Access from the Akeyless Console

Let's set up remote access to an SSH host from the Akeyless Console.

1. Log in to the Akeyless Console and go to **Items**.

2. Select the SSH Cert Issuer item that specifies the SSH host details and access credentials.

3. Click on the **Secure Remote Access** tab, select the pencil icon, and enable **Secure Remote Access**, then fill in the following fields:

   * Choose the right mode to work with either:

     * `Explicit Hosts`: The hostnames (or IP addresses) of your SSH target servers.

     * `Target`: Select a [Linked Target](https://docs.akeyless.io/docs/linked-target) that stores the relevant hosts, multiple Targets can be selected.

   * `Secure Access API`: Secure Access SSH control API endpoint. For example, `https://my.sra-server:9900`.

   * `Secure Access SSH`: Secure Access SSH server. For example, `my.sra-server:22`.

   * `Username`: SSH username to connect to the target server, based on the 'Allowed Users' list.

4. To the right of the **Enable Secure Remote Access** field, select the tick mark icon to save your changes.

## Akeyless Secure Access from CLI

Akeyless enables CLI access from any Unix terminal.

> ℹ️ **Note:**
>
> Starting from Windows 10, Microsoft supports the native feature "Windows subsystem for Linux."
> This feature enables users to use their Windows OS environment as a Unix-like system.
>
> To work with `Akeyless connect` command from Windows machine, place the `.akeyless-connect.rc` script on your home directory.

1. Download and install the latest version of [Akeyless CLI](https://docs.akeyless.io/docs/cli).

2. Create your `~/.akeyless-connect.rc`:

   ```shell
   IDENTITY_FILE=""
   CERT_ISSUER_NAME=""
   AKEYLESS_PROFILE="default"
   AKEYLESS_GW_REST_API=""

   # Following are used for control service, to configure the temporary session:
    # ${SRA_API_PROTO}://"${SRA_API_PREFIX}${SRA_HOST}${SRA_API_PATH}":"${SRA_API_PORT}
   #
   SRA_API_PREFIX=""
    SRA_API_PATH=""
    SRA_API_PROTO=http
    SRA_API_PORT=9900
   SRA_SSH_PORT=22

   # Allow caching of temp session creds
   SESSION_CACHING=no

   # Display connection stages
   DISPLAY_STAGES=yes
   ```

   Where:

   * `IDENTITY_FILE`: The path to the `ssh-key` to be signed and used for Zero Trust session (if empty, a default of `ssh-key` is used).

   * `CERT_ISSUER_NAME`: Full path to the Akeyless SSH Cert Issuer to use for Zero Trust session.

   * `AKEYLESS_PROFILE`: Akeyless CLI profile to be used. For profile creation, precedence, and default-profile behavior, see [CLI Profiles](https://docs.akeyless.io/docs/cli-profiles).

   * `AKEYLESS_GW_REST_API`: URL for Akeyless API Gateway (REST API).

3. Use `akeyless connect` command to perform SSH authentication to the target server by way of Akeyless [Secure Remote Access Bastion](https://docs.akeyless.io/docs/sra-web-access-on-k8s):

    ```shell General Template
   akeyless connect -t <[user@]target/hostname/ip[:port]> -n [/path/to/dynamic-secret] -g <your-gateway-ip[:port]>
   ```

## Legacy SSH Versions

Customers who have upgraded their Secure Remote Access (SRA) to the latest may experience SSH connection failures when using [Akeyless Connect](https://docs.akeyless.io/docs/sra-akeyless-connect)to access remote machines running OpenSSH version `7.4` or `7.6`. This occurs both in CLI and the Web portal.

It is possible to bypass this issue by setting the following environment variable in the SSH and Web bastion deployments, to all outgoing SSH connections:

```shell values.yaml
env:
  - name: SSH_EXTRA_ARGS
    value: -o PubkeyAcceptedKeyTypes=+ssh-rsa-cert-v01@openssh.com
```

This workaround explicitly enables legacy SSH key types that are deprecated and **not aligned** with modern security best practices.

## Legacy Mode

To support legacy applications, Akeyless enables a hybrid mode based on SSH certificates and SSH keys. Where your client will connect to the Akeyless SRA bastion by way of SSH certificate, and the Akeyless SRA bastion will use your SSH keys\password to connect to your legacy server.

To work with SSH keys, you will have to create a Static Secret in an Akeyless account to store your SSH private key or SSH password. The secret value should be either your SSH password or your SSH private key.

> ℹ️ **Note:**
>
> SSH password authentication brings with it risks. Please make sure you are connecting to the correct target server.

To enable Secure SSH Access for your target, set the following fields on your secret:

Run the `update-item` command to set the following fields on the static secret that stores the SSH password or private key details:

```shell
akeyless update-item --name <Path/to/static/secret> \
--secure-access-enable true \
--secure-access-ssh-creds <password/private-key> \
--secure-access-bastion-issuer </Path/of/SSH Cert Issuer> \
--secure-access-host <Target SSH host>
```

Where:

* `secure-access-ssh-creds`: Static-Secret values contain SSH Credentials, either Private Key or Password [`password`/`private-key`].

* `secure-access-certificate-issuer`: Path to the SSH Certificate Issuer for your Akeyless SRA.

* `secure-access-host`: Target servers for connections. For multiple values, repeat this flag.

Now, you can connect to your target SSH host by way of the `akeyless connect` command:

```shell
akeyless connect -t <[user@]target/hostname/ip[:port]> -n [/path/to/secret] -v <professional-bastion-hostname/ip[:port]>
```

## Upload/Download Files Using SSH

We support upload and download of files in SSH sessions through the Zero Trust Web Portal. To support this, **the remote server must support SFTP**.

### Upload

To upload a file, click on `Upload` button at the top and choose the file to upload from your local machine. The uploaded file will be placed in the user's $HOME directory on the remote machine.

> ℹ️ **Note (Temporary files):**
>
> Files are created as temporary items inside the SSH server during the upload process, and are deleted upon completion.

### Download

To download a file:

* First, copy the file to the download directory `/akl-downloads` which is already created in the user's $HOME directory on the remote machine (For example, `cp file-to-download.json /akl-downloads`).
* Then, click on the `Download` button at the top which will open a menu with all files located in that directory. Click on a file to start the download to your local machine. Note that larger files will only appear upon completion.

> ℹ️ **Note (File size and free space):**
>
> If there is a size limit issue on the SRA SSH server (exceeding 90% of space), a file named `NOT_ENOUGH_FREE_SPACE` is created in the `akl-downloads` folder, and the user will not be able to download it.

**Transfer behavior:** File transfer authorization is controlled by SRA permissions for upload and download operations. The Gateway SRA configuration model does not expose a dedicated file-size limit setting for SSH upload and download. Transfer speed and completion time can vary by network conditions, target host performance, and available resources on the SRA SSH service.
