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

Akeyless SSH Secure Remote Access enables traffic connections to servers that are not directly accessible via SSH but directed through a ssh-sra host, which proxies the connection between the SSH client and the remote servers. In addition, you can record all SSH sessions traffic and expose them to the filesystem for log forwarding.

> 👍 Note
> 
> **Legacy Mode**  
> For legacy applications that do not support SSH certificates, Akeyless offers a unique hybrid solution that involves certificates and keys.  
> For more details, please refer to [Legacy mode section](#section-legacy-mode) at the bottom of this page.

# Prerequisites

To enable Secure Remote Access for SSH servers you need: 

- The [Secure Remote Access](https://docs.akeyless.io/docs/remote-access-setup-overview).

- An  [SSH Cert Issuer](https://docs.akeyless.io/docs/ssh-certificates) for certificate authentication.

> 🚧 SSH session ends after ~30s on GKE/Ingress
> 
> If you’re running SRA behind a GKE HTTP(S) Load Balancer, the backend service timeout defaults to 30 seconds. Long-lived SSH (and WebSocket-based) sessions will close around this time.
> 
> To fix it, you should set a higher backend timeout with a BackendConfig (spec.timeoutSec) and annotate your Service. 
> 
> See GCP docs on backend service timeout and Ingress BackendConfig. After updating, your SSH session lifetime should match your intended TTL

# Set Up Remote Access to an SSH server from the Akeyless CLI

Let's set up remote access to an SSH server using the Akeyless CLI. 

1. Run the `update-item` command to set the following fields on the SSH Certificate Issuer item:

```shell Akeyless CLI
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

- **secure-access-api:** Secure Access SSH control API endpoint. E.g. <https://my.sra-server:9900>.
- **secure-access-ssh: ** Secure Access SSH server. E.g. my.sra-server:22.
- **secure-access-ssh-creds-user:** SSH username to connect to a target server, based on the `Allowed Users`list.
- **host-provider:**  Host provider type by default works with explicit hosts, if you wish to work with [Linked Targets](doc:linked-target) instead, set this parameter to `target`. When `target` is selected, use the `assoc-target-item` command to attach the relevant Linked Target. 

> 👍 Note
> 
> **Akeyless Secure Remote Access**
> 
> While working with Secure Remote Access, make sure to set `allowed_users` with `session_*` to ensure JIT users will be authorized for access.
> 
> You will also need to enable Secure Remote Access on the SSH Cert Issuer.

# Set Up Remote Access to an SSH server from the Akeyless Console

Let's set up remote access to an SSH server from the Akeyless Console.

1. Log in to the Akeyless Console and go to **Items**.

2. Select the SSH Cert Issuer item that specifies the SSH server details and access credentials.

3. Click on the **Secure Remote Access** tab, select the pencil icon and enable **Secure Remote Access**, then fill in the following fields:

- Choose the right mode to work with either:
  - `Explicit Hosts`:  The hostnames (or IP addresses) of your SSH target servers.
  - `Target`: Select a [Linked Target](doc:linked-target) that stores the relevant hosts, multiple Targets can be selected.
- `Secure Access API`: Secure Access SSH control API endpoint. E.g. <https://my.sra-server:9900>..
- `Secure Access SSH`: Secure Access SSH server. E.g. my.sra-server:22.
- `Username`: SSH username to connect to the target server, based on the 'Allowed Users' list.

4. To the right of the **Enable Secure Remote Access** field, select the tick mark icon to save your changes.

# Akeyless Secure Access from CLI

Akeyless enables CLI access from any UNIX terminal. 

> 👍 Note
> 
> Starting from Windows 10, Microsoft supports the native feature "Windows subsystem for Linux."  
> This feature enables users to utilize their Windows OS environment as a UNIX-like system. 
> 
> To work with `Akeyless connect` command from Windows machine, place the <code>.akeyless-connect.rc</code> script on your home directory.

1. Download and install the latest version of Akeyless CLI.

2. Create your ~/.akeyless-connect.rc : 

```shell
# ---------------------------------------------------------------------
# Copyright © 2023  Akeyless Security LTD.
#
# All rights reserved
# ----------------------------------------------------------------------

#
# This file is a user-specific configuration file for akeyles-connect Secure Remote Access
# it should be located in user home directory named .akeyless-connect.rc
#

# IDENTITY_FILE - the path to the ssh-key to be signed and used for Zero Trust session (if empty, default ssh-key is used)
IDENTITY_FILE=""

# CERT_ISSUER_NAME - full path to the Akeyless SSH Cert Issuer to use for Zero Trust session
CERT_ISSUER_NAME=""

# AKEYLESS_PROFILE - Akeyless CLI profile to be used
AKEYLESS_PROFILE="default"

# AKEYLESS_GW_REST_API - URL for Akeyless API Gateway (RestAPI)
AKEYLESS_GW_REST_API=""

# Following are used for control service, to configure the temporary session:
# ${SRA-CTRL-PROTO}://"${SRA_API_PREFIX}${SRA_HOST}${SRA-CTRL-PATH}":"${SRA-CTRL-PORT}
#
SRA_API_PREFIX=""
SRA-CTRL-PATH=""
SRA-CTRL-PROTO=http
SRA-CTRL-PORT=9900
SRA_SSH_PORT=22

# Allow caching of temp session creds
SESSION_CACHING=no

# Display connection stages
DISPLAY_STAGES=yes
```

3. Use `akeyless connect` command to perform SSH authentication to the target server via Akeyless [Secure Remote Access Bastion](https://docs.akeyless.io/docs/web-access-on-k8s):

```shell General template
akeyless connect -t  <[user@]target/hostname/ip[:port]> -n [/path/to/dynamic-secret] -g <your-gateway-ip[:port]>
```

<br />

> 🚧 Compatibility Issue with Legacy SSH Versions (7.4 & 7.6)
> 
> Customers who have upgraded their Secure Remote Access (SRA) to the latest may experience SSH connection failures when using Akeyless Connect to access remote machines running OpenSSH version 7.4 or 7.6. This occurs both in CLI and the Web portal.
> 
> It is possible to bypass this issue by setting the following environment variable in the SSH \& Web bastion deployments, to all outgoing SSH connections:
> 
> ```shell values.yaml
> env:
>   - name: SSH_EXTRA_ARGS
>     value: -o PubkeyAcceptedKeyTypes=+ssh-rsa-cert-v01@openssh.com
> ```
> 
> NOTE that this workaround explicitly enables legacy SSH key types that are deprecated and **not aligned **with modern security best practices.

# Legacy Mode

> ❗️ Critical
> 
> SSH password authentication brings with it risks. Please make sure you are connecting to the correct target server.

To support legacy applications, Akeyless enables a hybrid mode based on SSH certificates and SSH keys. Where your client will connect to the Akeyless SRA bastion via SSH certificate, and the Akeyless SRA bastion will utilize your SSH keys\\password to connect to your legacy server. 

To work with SSH keys, you will have to create a static secret in an Akeyless to store your SSH private key or SSH password. i.e., the secret value should be either your SSH password or your SSH private key. 

To enable Secure SSH Access for your target, set the following fields on your secret: 

Run the `update-item` command to set the following fields on the static secret that stores the ssh password or private key details:

```shell Akeyless CLI
akeyless update-item --name <Path/to/static/secret> \
--secure-access-enable true \
--secure-access-ssh-creds  <password/private-key> \
--secure-access-bastion-issuer </Path/of/SSH Cert Issuer> \
--secure-access-host <Target SSH server>
```

where:

- **secure-access-ssh-creds:** Static-Secret values contain SSH Credentials, either Private Key or Password [password/private-key].
- **--secure-access-certificate-issuer** Path to the SSH Certificate Issuer for your Akeyless SRA.
- **secure-access-host:** Target servers for connections. For multiple values, repeat this flag.

Now, you can connect to your target SSH server via the `akeyless connect` command: 

```shell
akeyless connect -t  <[user@]target/hostname/ip[:port]> -n [/path/to/secret] -v <professional-bastion-hostname/ip[:port]>
```

<br />

# Upload/Download Files Using SSH

We support upload and download of files in SSH sessions through the Zero Trust Web Portal. To support this, **the remote server must support SFTP**.

## Upload

To upload a file, click on `Upload` button at the top and choose the file to upload from your local machine. The uploaded file will be placed in the user's $HOME directory on the remote machine.

> 📘 Temporary files
> 
> Files are created as temporary items inside the SSH server during the upload process, and are deleted upon completion.

## Download

To download a file:

- First, copy the file to the download directory `/akl-downloads` which is already created in the user's $HOME directory on the remote machine (e.g `cp file-to-download.json /akl-downloads`).
- Then, click on the `Download` button at the top which will open a menu with all files located in that directory. Click on a file to start the download to your local machine. Note that larger files will only appear upon completion.

> 🚧 File size and free space
> 
> In case there is a size limit issue on the SRA SSH server, (exceeding over 90% of space) a file will be created in the `akl-downloads` folder saying `NOT_ENOUGH_FREE_SPACE` and the user won't be able to download it.