---
title: Connecting Your First SRA Resource
deprecated: false
hidden: false
metadata:
  robots: index
---
This guide walks you through connecting your first protected resource for SRA.<br />As a concrete example, it walks through an SSH session to a target host and connecting to it using the [Akeyless Connect](doc:new-structure-akeyless-console) CLI command. In this example, the target host is an Ubuntu server. <br />check our [Supported Resource Types](doc:sra-resource-types).

Configuration takes place in the Akeyless Console. Connection is established via CLI using an [API Key](doc:auth-with-api-key).

By the end, you'll have a real SSH session open from your terminal, proxied through SRA to your target host.

***

## Prerequisites

- [Gateway with SRA](doc:sra-quick-start-guide).
- An existing [SSH Certificates Issuer](doc:sra-ssh-certificates)&#x20;
- A target host reachable over SSH.
- Console access with permission to edit [SSH Certificate Issuers](doc:sra-ssh-certificates).
- The `akeyless` CLI installed locally.

***

## **Allow Gateway Access to the Host**

1. Allow outbound traffic from the gateway pod to the target host on `port 22`, In your cluster, this pod is named `ssh-gw-akeyless-gateway-....`
2. Allow inbound traffic on the target host's firewall or security group from the gateway pod's IP/CIDR or node/subnet range on `port 22` .

If this step is skipped, every step that follows will still appear correctly configured, but the connection will fail.

***

## Enable SRA on SSH Certificate Issuer and set the target

Edit the existing SSH Certificate Issuer created during the Gateway deployment directly in the Akeyless Console.

**Navigation:** Console → **Items** → locate the existing SSH Certificate Issuer → **Secure Remote Access**

1. Click **Edit&#x20;**&#x70;en.
2. Check the **Enable Secure Remote Access** checkbox.
3. Click **Add** and enter the target host's IP address.
4. Set **Default SSH Username** to `ubuntu`.
5. Click **Save**.

***

## Create an Authentication Method

This [Authentication Method](doc:access-and-authentication-methods) authenticates the user connecting to your resource. For this guide, API key authentication is used for simplicity.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  To connect using Akeyless's SRA web portal - <br />either the public facing ZeroTrust portal at `https://zerotrust.akeyless.io` or your internal GW SRA Portal at `https://<gateway-host>:8000/sra/portal` <br />you must use SAML, OIDC, or certificate-based authentication. Note that LDAP is supported only on the GW SRA Portal.
</Callout>

```shell
akeyless auth-method create api-key --name MySraAPIKey
```

## Create an Access Role

This [Access Role](doc:rbac) authorizes your SRA user to connect to the resource.

1. Create a new access role:

   ```shell
   akeyless create-role --name MySraRole
   ```

2. Grant the role `list` and `allow_access` permissions on the SSH Certificate Issuer's path:

   ```shell
   akeyless set-role-rule --role-name MySraRole --path "/path/to/ssh-certificate-issuer" --capability list --capability allow_access
   ```

3. Associate the authentication method with the role:

   ```shell
   akeyless assoc-role-am --role-name MySraRole --am-name MySraAPIKey
   ```

## Connect to Resource via CLI

Authenticate the CLI with your API key (Access ID and Access Key):

```bash
akeyless auth --access-id <your-access-id> --access-key <your-access-key>
```

Copy the user t-token and connect:

```bash
akeyless connect \
  -t "ubuntu@<host-ip-address>:22" \
  -c <cert-issuer-name> \
  -v <Gateway-SSH-EXTERNAL-IP>:22 \
	-g http://<Gateway-EXTERNAL-IP>
  --token <t-token>
```

where:

- `-t`   The OS user and target host/port to connect to. Must match the SSH username and host configured on the certificate issuer.
- `-c` The existing SSH Certificate Issuer with Secure Remote Access enabled.
- `-v` The external endpoint of your Gateway's SSH Access service, the `EXTERNAL-IP` (or DNS name) retrieved via `kubectl get services` of the service starting with `ssh-quick-start-gw,` and port `22` exposed by the SRA SSH service.
- `-g` The base URL of your Akeyless Gateway, the endpoint the CLI uses to authenticate the session and issue the SSH certificate, e.g. `http://<Gateway-EXTERNAL-IP>:8080`.
- `--token`  The user token to Akeyless.

Landing in a real shell on your target host confirms that SRA is working end-to-end.

***

## Troubleshooting

| Symptom                                | Likely cause                                                                                                               | Fix                                                                                                      |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Connection times out                   | Step 1 (network/firewall) was skipped or the pod's IP/CIDR isn't actually allow-listed on the target host                  | Re-check the target's firewall/security group against the SRA SSH gateway pod's real egress IP or subnet |
| "Permission denied" when session opens | Username not included in **Allowed Users**, or **Secure Access SSH Creds User** doesn't match a real OS user on the target | Re-check both fields on the issuer against the actual OS username on the target host                     |

<br />

<br />
