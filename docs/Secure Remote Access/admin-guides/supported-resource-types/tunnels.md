---
title: Tunnels
excerpt: Using Akeyless Connect
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Akeyless Secure Remote Access solution has a built-in `Tunnel` mode, which can be used to connect with various native and thick clients to remote hosts via Akeyless SRA SSH server, supported with a complete audit trail.

While your local machine uses the [Akeyless Connect](https://docs.akeyless.io/docs/remote-access-akeyless-connect) CLI, any thick client can be used to establish the connection to a remote server within your internal network via the Akeyless SRA SSH server.

# Prerequisites

* [Akeyless Connect](https://docs.akeyless.io/docs/remote-access-akeyless-connect) configured.

* The [Secure Remote Access server](https://docs.akeyless.io/docs/remote-access-setup-k8s) deployed.

# Usage

> 🚧 Warning
>
> For security reasons, please bind services only to the **local interface**. You can use local port forwarding to access the service that is listening on the remote server.

Connections on the local machine made to the forwarded port will, in effect, connect to the remote machine.

```shell Tunnel usage
akeyless connect --target <user>@<targetserver> \
--via-sra sra-host:port\
--tunnel='-L 127.0.0.1:<port>:<targetserver>:<port>' \
--cert-issuer-name "<Path/To/SSHCertIssuer>" \
--name "</Path/To/Secret>" \
 --sra-ctrl-port "http\https"
```

Where: 

* **target:**  The target resource, e.g. `user@ssh-server[:port]`, `us-east-2`, `mysql-server:3306`, etc.

* **--via-sra:** SRA host, which the connection will go through. e.g.: sra-host:port\`.
  * NOTE - With unified Gateway, you should be using `-g <your-gateway-ip[:port]>`instead of `--via-sra`

* **tunnel:** SSH tunnel setting e.g. `-T='-L 127.0.0.1:<port>:127.0.0.1:<port>'`

* **cert-issuer-name:** Optional. If already configured inside `akeyless-connect.rc` file, alternativity provide\
  the full path to the [SSH Cert Issuer](https://docs.akeyless.io/docs/ssh-certificates) to establish the connection to the bastion. 

* **name :** Full name of the secret item to use in order to connect. i.e. Dynamic or a Rotated Secret for Database,RDP etc. Or a static secret which contains the credentials of the target system.

* **command:** Command to execute on the target remote host (useful for non-interactive mode). e.g. `-C='ls -al'`

* **ssh-extra-args:** Additional SSH arguments (except -i).

## RDP

To connect to a remote desktop server via the Akeyless SRA server from your local terminal, run the following command, and open your Remote Desktop client, where you should use the localhost endpoint to connect to your remote server.

```shell
akeyless connect -t <RDP User>@<RDP Host> \
--via-sra: sra-host:port [for example, 2222] \
--tunnel='-L 127.0.0.1:3389:<RDP Host>:3389'\
-c "<Path/To/SSHCertIssuer>" \
-n "/Path/To/RDP/Dynamic/Secret"
```

Once the tunnel is opened, you can connect with your local RDP client to the `TargetServer` using your localhost port via SRA.

## K8s

### kubectl

To connect with a remote K8s cluster using a thick client, you can leverage the Akeyless K8s Tunnel that will start a proxy service on your remote K8s server, via the SRA.

First, you can use the following template as an example to add to your `~/.kube/config` file:

```yaml ~/.kube/config
apiVersion: v1
clusters:
- cluster:
    server: http://127.0.0.1:2345
  name: test-tunnel
contexts:
- context:
    cluster: test-tunnel
    user: test-tunnel
  name: testunnel
current-context: testunnel
kind: Config
preferences: {}
users:
- name: test-tunnel
```

Then, use the following command to create the tunnel using the same port number as your local server (2345) in the `kubeconfig` file:

```shell
akeyless connect -t <k8s.server.host> \
 -n "/Path/To/K8s/Dynamic/Secret" \
 -c "/Path/To/SSHCertIssuer" \
 --via-sra: sra-host:port [for example, 2222] \
 --bastion-ctrl-proto=https \
 --k8s-tunnel 2345
```

> 📘 Note
>
> A remote port on the SSH bastion will automatically be allocated based on availability.

Once that's done, **in a new terminal tab** you can run `kubectl` commands as normal after switching to the above `kubectl` context.

### Lens

Similarly, after having run the `akeyless connect` command as in the previous section, to work with [Lens](https://k8slens.dev/) K8s IDE, open your Lens Settings > Proxy and set the proxy server with your localhost interface in the following format: [http://127.0.0.1:2345](http://127.0.0.1:2345).

Now, you can start interacting with your remote K8s API server using the tunnel.

For example, to add a new cluster to Lens add, you can use the following `kubeconfig` reference: 

```yaml
apiVersion: v1
clusters:
- cluster:
    server: http://127.0.0.1:2345
  name: AKEYLESS_Lens_K8S
contexts:
- context:
    cluster: AKEYLESS_Lens_K8S
    user: AKEYLESS_Lens_K8S
  name: AKEYLESS_Lens_K8S
current-context: AKEYLESS_Lens_K8S
kind: Config
preferences: {}
users:
- name: AKEYLESS_Lens_K8S
```

Where the `server` should point to your local tunnel port.

## SSH Tools

To work with your native SSH tools, you can run a local tunnel on your host:

```shell
akeyless connect -t <user>@<targetServer> \
 --via-sra: sra-host:port [for example, 2222]  \
--tunnel='-L 127.0.0.1:<localPort>:<targetServer>:<targetPort>'
```

Then, any SSH client (such as **SecureCRT**, **PuTTY**, **tmux**, etc.) can be used to establish connections to the remote `targetServer`. After running the above command to open the tunnel, on your SSH client, open a connection to `127.0.0.1:localPort` to connect with your remote server.
