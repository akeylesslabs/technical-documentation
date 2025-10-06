---
title: CLI Reference - KMIP
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
This section outlines the CLI commands relevant to KMIP.

<CLIGeneralFlags />

# Commands

## `kmip-client-delete-rule`

Delete an RBAC rule from a client

### Usage

```shell
akeyless kmip-client-delete-rule \
--path &lt;Access path&gt; \
--name &lt;KMIP client name&gt; \
--client-id &lt;KMIP client ID&gt; \
--gateway-url &lt;API Gateway URL:8000&gt;
```

### Flags

`-p, --path`: **Required**, Access path, e.g /* or /some-key

`-n, --name`: KMIP client name (either name or id are required)

`-i, --client-id`: KMIP client ID (either name or id are required)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

## `kmip-client-set-rule`

Add a new RBAC rule to a client

Supported capabilities are:
`DENY`
`CREATE`
`REGISTER`
`REKEY`
`LOCATE`
`GET`
`GET_ATTRIBUTES`
`ACTIVATE`
`REVOKE`
`DESTROY`

### Usage

```shell
akeyless kmip-client-set-rule \
--path &lt;Access path&gt; \
--capability &lt;Access capability&gt; \
--name &lt;KMIP client name&gt; \
--client-id &lt;KMIP client ID&gt; \
--gateway-url &lt;API Gateway URL:8000&gt;
```

### Flags

`-p, --path`: **Required**, Access path, e.g /* or /some-key

`-c, --capability`: **Required**, Access capability (see command description for supported values)

`-n, --name`: KMIP client name (either name or id are required)

`-i, --client-id`: KMIP client ID (either name or id are required)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

## `kmip-create-client`

Create a new KMIP client

### Usage

```shell
akeyless kmip-create-client \
--name &lt;Client name&gt; \
--certificate-ttl &lt;Server certificate TTL in days (Deafult = 90)&gt; \
--gateway-url &lt;API Gateway URL:8000&gt;
```

### Flags

`-n, --name`: **Required**, Client name

`-t, --certificate-ttl[=90]`: Client certificate TTL in days

`-p, --output-file-folder`: Folder path to save client certificate files (for example, '.'). Two files are created: \<client-name>.key and \<client-name>.cert

`-a, --activate-keys-on-creation"h-0": "`: If set to 'true', newly created keys on the client will be set to an 'active' state

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

## `kmip-delete-client`

Delete a KMIP client

### Flags

`-n, --name`: KMIP client name (either name or id are required)

`-i, --client-id`: KMIP client ID (either name or id are required)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

## `kmip-describe-client`

Show KMIP client details

### Flags

`-n, --name`: KMIP client name (either name or id are required)

`-i, --client-id`: KMIP client ID (either name or id are required)

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

## `kmip-describe-server`

Show KMIP environment details

### Flags

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port).

## `kmip-list-clients`

Show existing KMIP clients

### Flags

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port).

## `kmip-renew-client-certificate`

Renew KMIP client certificate

### Flags

`-n, --name`: KMIP client name (either name or id are required)

`-i, --client-id`: KMIP client ID (either name or id are required)

`-p, --output-file-folder`: Folder path to save client certificate files (for example, '.'). Two files are created: \<client-name>.key and \<client-name>.cert

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

## `kmip-renew-server-certificate`

Renew KMIP server certificate

### Flags

`-u, --gateway-url[=http://localhost:8000]`:  Akeyless API Gateway URL (Configuration Management port)

## `kmip-server-delete`

Delete the kmip server (allowed only if it has no clients nor associated items)

### Flags

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port).

<br />

## `kmip-server-move`

Move the root location of the kmip server and all associated items to a new root location

### Usage

```shell
akeyless kmip-server-move \
--new-root &lt;New root for the kmip server&gt; \
--gateway-url &lt;API Gateway URL:8000&gt;
```

### Flags

`-u, --gateway-url[=http://localhost:8000]`: Gateway URL (Configuration Management port).

`-n, --new-root`: **Required**, New root for the kmip server

## `kmip-server-setup`

Create a new KMIP environment

### Usage

```shell
akeyless kmip-server-setup \
--hostname &lt;KMPI server hostname&gt; \
--certificate-ttl &lt;Server certificate TTL in days (Deafult = 90)&gt; \
--root &lt;Root path of KMIP Objects&gt; \
--gateway-url &lt;API Gateway URL:8000&gt;
```

### Flags

`-n, --hostname`: **Required**, Hostname of this KMIP server

`-t, --certificate-ttl[=90]`: Server certificate TTL in days

`-r, --root`: **Required**, Root path of KMIP Objects

`-p, --output-file-folder`: Folder path to save CA certificate file (for example, '.'). A new file will be created in that folder: ca.cert.

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

## `kmip-set-server-state`

Set the server state to enabled/disabled

### Usage

```shell
akeyless kmip-set-server-state \ 
--state &lt;Enabled / Disabled&gt; \
--gateway-url &lt;API Gateway URL:8000&gt;
```

### Flags

`-s, --state`: **Required**, Make the server enabled or disabled [use 'enabled' or 'disabled']

`-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

> 📘 Info
>
> **Writing commands - generating secrets**
>
> The default Akeyless Vault behavior is that the write commands (generate secrets) are performed to the main region of Akeyless Vault, while the read commands (fetch secrets) are performed on the nearest region to you, in order to minimize latency.
> If you wish to change that, in order to work only with the main region, please add
> `optimize_dns_disable=true` in the settings file.
