---
title: adding your first target
deprecated: false
hidden: false
metadata:
  robots: index
---
1. SAML auth method
2. create item
3. enable SRA on item
4. enable SRA on cert issuer
5. connect (can i run it with token from auth that arent SAML OIDC cert LDAP?)<br /><br /><br />akeyless create-secret --name /sra/ec2-password --value '\<EC2_PASSWORD>'<br /><br /><br /><br />Akeyless SSH Secure Remote Access enables traffic connections to servers that are not directly accessible by way of SSH but directed through a `ssh-sra` host, which proxies the connection between the SSH client and the remote servers. In addition, you can record all SSH sessions traffic and expose them to the filesystem for log forwarding.

In this guide, we will connect to a remote target using an [SSH Certificate](https://docs.akeyless.io/docs/sra-ssh-certificates).

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  For legacy applications that do not support SSH certificates, Akeyless offers a unique hybrid solution that involves certificates and keys.
  For more details, please refer to [Legacy mode section](https://docs.akeyless.io/docs/sra-ssh#legacy-mode) at the bottom of this page.
</Callout>

## Prerequisites

- [Secure Remote Access](https://docs.akeyless.io/docs/sra-setup-overview) deployment.

- An [SSH Cert Issuer](https://docs.akeyless.io/docs/sra-ssh-certificates) for certificate authentication.

- SSH sessions behind a **GKE HTTP(S)** Load Balancer may disconnect after `30` seconds due to the default backend timeout. You can increase it by configuring a BackendConfig (`spec.timeoutSec`) and annotating your Service as described in the GCP docs on [backend service timeouts](https://docs.cloud.google.com/load-balancing/docs/backend-service#timeout-setting) and [Ingress BackendConfig](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/ingress-configuration#backendconfig).

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

- `secure-access-api`: Secure Access SSH control API endpoint. For example, `https://my.sra-server:9900`.

- `secure-access-ssh`: Secure Access SSH server. For example, `my.sra-server:22`.

- `secure-access-ssh-creds-user`: SSH username to connect to a target server, based on the `Allowed Users` list. Starting with Gateway **v4.45.0**, Secure Remote Access (SRA) works out of the box with any **SSH Cert Issuer** where SRA is enabled. If you’re using an older Gateway version, make sure the SSH Cert Issuer `allowed_users` includes `session_*`, so just in time users are authorized.

- `host-provider`: Host provider type by default works with explicit hosts, if you wish to work with [Linked Targets](https://docs.akeyless.io/docs/linked-target) instead, set this parameter to `target`. When `target` is selected, use the `assoc-target-item` command to attach the relevant Linked Target.

- `secure-access-host`: Target servers for connections. Repeat this flag for multiple values. Starting with SRA v2.9.0, CIDR notation is supported in addition to individual hostnames and IP addresses (for example, `192.168.1.0/24`).

- `secure-access-enforce-hosts-restriction`: When set to `true`, restricts SRA connections to only the hosts specified in `--secure-access-host`. Users attempting to connect to unlisted hosts are denied.

<br /><br />add a guide with reference to [Resource Types](doc:new-structure-resource-types)

<br /><br />

Then run `kubectl get services` and look for the `EXTERNAL-IP` of the service starting with `quick-start-gw`. Copy the `EXTERNAL-IP` and paste that into your browser with port 8000/console (for example, `http://<Your-Akeyless-GW-URL>:8000/console`). If you get the login page, you have successfully deployed the Gateway!

#### Gateway URLs

For the Gateway, you can access the following:

- The Gateway's Internal Console is located at `http://<Your-Akeyless-GW-URL>:8000/console`. The internal console means you are working from inside the Gateway and talking directly with the SaaS. If you are using `https://console.akeyless.io`, you will not be able to interact with this Gateway as it is not secured with TLS.

#### Remote Access URLs

For Remote Access, you can access the following:

- The Remote Access Internal Web Portal is located at `http://<Your-Akeyless-GW-URL>:8000/sra/portal`

- Remote Access can also be accessed using our public URL: `https://zerotrust.akeyless.io`. If you are using the public URL for RDP, Web, or similar sessions, you will be required to add your Web URL endpoint: `http://<Your-Akeyless-GW-URL>:8000/sra/web-client`

## Testing Out Remote Access

Here we will lay out the steps to get a SAML user to access the Remote Access Portal.

1. Firstly, you need to make sure you have your SAML application set up, for example, an Okta account set up with the Akeyless application configured. You will also need to retrieve your Metadata URL for this.

2. Next, run the following command to create your SAML Auth Method and make sure to input your Kubernetes Service External-IP address:

   ```shell
   akeyless auth-method create saml --name mySamlAuth --unique-identifier email --idp-metadata-url <your-okta-metadata-url> --allowed-redirect-uri https://console.akeyless.io/login-saml,http://127.0.0.1:*,http://<EXTERNAL-IP-of-K8s-Service>:*
   ```

3. Create a role with access to Items with Secure Remote Access with Allow Access permissions.

   ```shell
   akeyless set-role-rule --role-name MySamlRole --path "/\*" --rule-type sra-rule --capability allow_access
   ```

4. Associate your Auth Method as follows:

   ```shell
   akeyless assoc-role-am --role-name MySamlRole --am-name MySamlAuth
   ```

5. Next, open your browser and go to your Remote Access internal endpoint: `http://<Your-Akeyless-GW-URL>:8000/sra/portal`

6. Enter your SAML AccessID and click “Sign In”. You will be redirected to your SAML service login page to log in and then when you finish that will redirect you to a page with various resources you can set at a later time.

## Next Steps

With a Gateway deployed, you can now test out using just-in-time [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) for various applications and services by setting up [Targets](https://docs.akeyless.io/docs/targets). If you are also using Remote Access, you can also set up Remote Access on those Targets and log into those [Resources](https://docs.akeyless.io/docs/supported-resource-types) securely from anywhere by [reading the docs](https://docs.akeyless.io/docs/sra-overview).<br /><br />

- [Admin Guides](https://docs.akeyless.io/docs/sra-admin-guides)

- [Accessing Resources](https://docs.akeyless.io/docs/sra-accessing-resources)

<br />
