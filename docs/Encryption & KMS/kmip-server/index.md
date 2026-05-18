---
title: KMIP Server
excerpt: Key Management Interoperability Protocol (KMIP) Server
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: kmip-for-vsphere
      title: KMIP for Vsphere
---
The [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) built-in Key Management Interoperability Protocol (KMIP) server handles the lifecycle of KMIP-managed objects.

By default, cryptographic objects managed by the KMIP server are stored under `/kmip/default/`. The [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) authentication method used for KMIP operations must include `create`, `list`, `delete`, and `read` permissions for `/kmip/default/*`.

This default path can be changed during KMIP server setup.

## KMIP Certificate Expiry Events

KMIP server and KMIP client certificates are time-bound objects. To reduce renewal failures and service interruptions, monitor certificate expiration events in the [Event Center](https://docs.akeyless.io/docs/event-center).

For KMIP certificate observability, use the following event types:

* `kmip-cert-pending-expiration`: Triggered before certificate expiration based on the certificate's configured expiration-notification window. Set that window when you create or update the certificate, then use [Event Forwarders](https://docs.akeyless.io/docs/event-center) to route the alert.
* `kmip-cert-expired`: Triggered when a certificate has expired.

To route these events to operational channels, configure an [Event Forwarder](https://docs.akeyless.io/docs/event-center).

For audit action taxonomy, see [Log Actions](https://docs.akeyless.io/docs/log-actions).

> ℹ️ **Note:**
>
> Only users from your Gateway admins list can configure the KMIP server.

## Command Model

Use the following command model for certificate lifecycle operations:

* Provision server: `kmip-server-setup`
* Provision client: `kmip-create-client`
* Renew server certificate: `kmip-renew-server-certificate`
* Renew client certificate: `kmip-renew-client-certificate`

For complete command flags, see [CLI Reference - KMIP](https://docs.akeyless.io/docs/cli-reference-akeyless-kmip-server).

> ℹ️ **Note (API and CLI naming):**
>
> In REST API schemas, certificate lifecycle updates can appear as `kmip-server-update` and `kmip-client-update` operations. In CLI workflows, use the KMIP renew commands shown above.

## CLI Quickstart

### Step 1: Create a KMIP server

To start the Akeyless KMIP server using Akeyless CLI, run the following command:

```shell
akeyless kmip-server-setup \
--hostname <akeyless.gateway.hostname> \
--gateway-url 'https://<Your_Akeyless_GW_URL>:8000' \
--root /kmip/default
```

Flags:

* `hostname`: Hostname of this KMIP server.
* `root[=/kmip/default]`: Path to store all KMIP Objects.
* `gateway-url[=http://localhost:8000]`: Akeyless Gateway URL.

You can find the complete list of settings for this command in the [CLI Reference - Akeyless KMIP Server](https://docs.akeyless.io/docs/cli-reference-akeyless-kmip-server#kmip-server-setup) section.

> ℹ️ **Note:**
>
> Make sure to replace the `hostname` field with your **Akeyless Gateway** hostname.

This returns the CA certificate:

```shell
A new KMIP environment was successfully created.
Please store the certificate someplace safe:
-----BEGIN CERTIFICATE-----
MIIDCTCC...jOVHG8Og==
-----END CERTIFICATE-----
```

This command automatically creates two items under the KMIP root path:

1. `ca.key` (the CA certificate that was the output of the `kmip-server-setup`)
2. A [PKI Cert Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) named **server**

### Step 2: Create a KMIP client

This guide uses MongoDB Enterprise as an example KMIP client.

> ℹ️ **Note:**
>
> This guide was created using MongoDB version 4.2 or earlier.
>
> **Activate Keys** - Akeyless supports an optional setting to enable keys upon creation automatically. To set this function by default for your client, provide the `--activate-keys-on-creation=true` setting as part of your client creation command.

```shell
akeyless kmip-create-client \
--name mongodb \
--gateway-url 'https://<Your_Akeyless_GW_URL>:8000' \
--output-file-folder /current/working/dir
```

Flags:

* `name`: A unique name of the KMIP client. The name can include the path to the virtual folder where you want to create the new client, using slash `/` separators. If the folder does not exist, it will be created together with the client.
* `gateway-url[=http://localhost:8000]`: Akeyless Gateway URL (port `8000`).
* `output-file-folder`: Folder path to save client certificate files locally (for example, `.` for current working dir).
  Two files are created: `<client-name>.key` and `<client-name>.cert`.

You can find the complete list of settings for this command in the [CLI Reference - Akeyless KMIP Server](https://docs.akeyless.io/docs/cli-reference-akeyless-kmip-server#kmip-create-client) section.

This returns the `client ID`, `key`, and `certificate`:

```shell
New client successfully created.
Client ID: Zvzw0...VM2u
Client Key:
-----BEGIN RSA PRIVATE KEY-----
MIIEpA...yRCF8UQ==
-----END RSA PRIVATE KEY-----

Client Certificate:
-----BEGIN CERTIFICATE-----
MIIDSz...0otOEQQ==
-----END CERTIFICATE-----
```

> ℹ️ **Note:**
>
> Save the received certificate and key in a safe place. They will be used to set up the connection.

After creation, the key and certificate are not shown again. To retrieve KMIP client IDs:

```shell
akeyless kmip-list-clients --gateway-url 'https://<Your-Akeyless-Gateway-URL>:8000'
```

### Step 3: Set client access permissions

By default, KMIP clients have no permissions. To grant your KMIP client minimal access permissions, execute the following command:

```shell
akeyless kmip-client-set-rule \
--gateway-url 'https://<Your-Akeyless-Gateway-URL>:8000' \
--client-id kc-5BL...7yVP \
--path "/*" \
--capability CREATE \
--capability GET
```

Flags:

* `path`: The path in the Akeyless KMIP server folder, where your client objects will be stored.
* `capability`: The capabilities of your KMIP client (`DENY`, `CREATE`, `REGISTER`, `REKEY`, `LOCATE`, `GET`, `GET_ATTRIBUTES`, `ACTIVATE`, `REVOKE`, `DESTROY`).
* `name`: KMIP client name (either name or ID is required).
* `client-id`: KMIP client ID (either name or ID is required).
* `gateway-url[=http://localhost:8000]`: Akeyless Gateway URL (port `8000`).

This command grants our MongoDB KMIP client the ability to create and retrieve objects under the `/kmip/default/` path.

You can find the complete list of settings for this command in the [CLI Reference - Akeyless KMIP Server](https://docs.akeyless.io/docs/cli-reference-akeyless-kmip-server#kmip-client-set-rule) section.

> ℹ️ **Note:**
>
> These roles and permissions are only valid for **the selected KMIP Server**, not for all Akeyless functions.

### Step 4: Renew certificates

Renew the server certificate:

```shell
akeyless kmip-renew-server-certificate \
--gateway-url 'https://<Your_Akeyless_GW_URL>:8000'
```

Renew a client certificate:

```shell
akeyless kmip-renew-client-certificate \
--name mongodb \
--gateway-url 'https://<Your_Akeyless_GW_URL>:8000' \
--output-file-folder /current/working/dir
```

## MongoDB Encryption Configuration

MongoDB Enterprise supports [integration with KMIP Servers](https://docs.mongodb.com/manual/tutorial/configure-encryption/). To set up MongoDB integration with the Akeyless KMIP server, the following settings need to be provided (see the linked guide for details):

```shell
mongod --enableEncryption \
  --kmipServerName <akeyless.gateway.hostname> \
  --kmipServerCAFile '/<path to>/ca.cert' \
  --kmipClientCertificateFile '/<path to>/mongodb.pem'
```

Where:

* `kmipServerName` is the address you specified when setting up the KMIP Server.

* `kmipServerCAFile` is the file that contains the KMIP CA Certificate received earlier
  (can be retrieved using the `akeyless kmip-describe-server` command).

* `kmipClientCertificateFile` is the file with both private key and certificate that were created during the `kmip-create-client` step. Simply `cat key-file cert-file > mongodb.pem` and use the resulting file to connect.

To use an existing key for encryption, please upload the key to Akeyless as a new [Classic Keys](https://docs.akeyless.io/docs/classic-keys) and pass it as a value of the `kmipKeyIdentifier` parameter. If not provided, MongoDB will create a new encryption key in Akeyless and use it for encryption.

The command output shows the created KMIP key ID:

`Encryption key manager initialized using KMIP key with id: feu...uoz.`

## Console Workflow

### Create a KMIP server

1. Log in to the Akeyless Console and navigate to **Data Protection > New**.

2. Define KMIP server settings as follows:

    * **Gateway:** Select the Gateway where you will set up your KMIP server.

    * **Custom hostname:** Select this checkbox if you want to provide an alternative hostname for the KMIP server.

    * **Hostname:** Provide the hostname for the KMIP server. By default, use the hostname of the selected Gateway.

    * **Location:** Specify the path to the Akeyless folder where you want to create the new KMIP server objects, using the slash `/` separators. If the folder does not exist, it will be created together with the server.

    * **Certificate TTL:** Specify the TTL of the KMIP Server certificate (in days).

3. Click **Setup** to save the changes.

### Create a KMIP client

1. Click on your **KMIP Server > Clients > New Client**.

2. Define the KMIP client settings as follows:

    * **Name:** Define the name of the KMIP client.

    * **Certificate TTL:** Specify the TTL of the Client certificate (in days).

    * **Restrict to the following path:** Provide a path where this client will store all its objects. Default value is /KMIP/data.

    * **Allow the following actions:** Select all the actions that are allowed to this client on the relevant path.

3. Click **Setup** to save the changes.

4. Save the private key and certificate of the client to set up the connection with your KMIP Client system.

## Troubleshooting

> ℹ️ **Note (Handling the "Cannot Parse Attribute: Unique Identifier" Error):**
>
> If you see the following error when starting MongoDB:
>
> `errmsg: Cannot parse attribute: Unique Identifier. Not implemented.`
>
> This means the KMIP server is returning the key ID in a format MongoDB doesn’t support (for example, as a `ByteString` instead of `TextString`).

Resolution Steps

1. Avoid using .system as the default KMIP key.
2. Create a new AES256-CBC key in Akeyless (do not use AES256-GCM unless using MongoDB ≤ 4.2).
3. Specify the correct key ID in the MongoDB config file using `keyIdentifier`.
4. Ensure the Akeyless Gateway returns the Unique Identifier as a `TextString`. If not, please contact Akeyless Support.

Example `mongod.conf` Configuration

```yaml
# mongod.conf

# Storage Configuration
storage:
  dbPath: "/data/db" # MongoDB data path

# Enable Encryption and KMIP Configuration
security:
  enableEncryption: true
  encryptionCipherMode: AES256-CBC # GCM is not supported in newer MongoDB versions
  kmip:
    keyIdentifier: "<your_kmip_key_id>"  # Replace with your actual KMIP key ID
    serverName: "<your_host_ip>"         # Replace with your KMIP server IP or hostname
    port: 5696
    serverCAFile: "/config/ca.cert"
    clientCertificateFile: "/config/mongodb.pem"
    # useLegacyProtocol: true  # Enable only if required by your KMIP server

# Network Configuration
net:
  bindIp: localhost
  port: 27017
```

To launch MongoDB with this configuration:

```shell
mongod --config <path_to_mongod.conf>
```
