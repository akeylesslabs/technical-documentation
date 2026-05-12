---
title: MCP Server
excerpt: Use the Akeyless MCP Server with MCP clients and JetBrains IDE integration.
deprecated: false
hidden: false
link:
  new_tab: false
metadata:
  title: Akeyless MCP Server
  description: Use the Akeyless MCP Server with supported MCP clients and JetBrains IDE integration.
  robots: index
---
## Overview

The Akeyless Model Context Protocol (MCP) Server is a robust integration that enables AI systems to securely interact with your Akeyless Identity Security Platform. It provides a standardized interface for AI models to access, manage, and manipulate secrets, keys, certificates, and other sensitive data stored in Akeyless.

## What Is the MCP?

The Model Context Protocol is a standardized protocol that allows AI systems to connect to external data sources and services. It provides a secure, authenticated method for AI models to:

* Access external APIs and services
* Retrieve and manage sensitive data
* Perform operations on behalf of users
* Maintain security boundaries and access controls

Read more about the [Model Context Protocol](https://modelcontextprotocol.io/).

## Akeyless MCP Server Features

The Akeyless MCP Server provides comprehensive access to Akeyless functionality, including:

### Core Capabilities

* Secrets Management: Create, read, update, and delete Static Secrets
* Encryption and Key Management: Generate, rotate, and manage encryption keys
* Certificate Lifecycle Management: Issue, renew, and manage PKI and SSH certificates
* Dynamic Secrets: Generate temporary credentials for databases and cloud services
* Access Control: Manage roles, permissions, and authentication methods
* Analytics: Retrieve usage analytics and audit data

### Supported Operations

* List and describe items (such as secrets, keys, certificates)
* Create and update secrets
* Generate Dynamic Secrets
* Manage authentication methods and roles
* Retrieve analytics data
* Handle targets and associations

## Configuration

### Prerequisites

* The Akeyless CLI must be successfully installed and **updated to version 1.130.0** or newer.
    * Read more about the [Akeyless CLI](https://docs.akeyless.io/docs/cli).
    * Learn about [updating the Akeyless CLI](https://docs.akeyless.io/docs/cli-reference#/update).
* An Akeyless account must be created and a corresponding profile configured with the Akeyless CLI.

### Client Setup

Configure the Akeyless MCP server in your MCP client configuration file. For example, Cursor uses `~/.cursor/mcp.json`. A list of supported MCP clients is available at <Anchor label="MCP clients" target="_blank" href="https://modelcontextprotocol.io/clients">https://modelcontextprotocol.io/clients</Anchor>.

If you use JetBrains IDEs, see <Anchor label="Akeyless MCP Plugin for JetBrains IDEs" href="doc:akeyless-mcp-plugin-jetbrains-ides" /> for the IDE-specific setup and usage flow.

#### Sample Configuration Structure

```json
{
  "mcpServers": {
    "akeyless": {
      "command": "/path/to/akeyless",
      "args": [
        "mcp",
        "--access-id", "your-access-id",
        "--access-key", "your-access-key",
        "--access-type", "access_key",
        "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
      ],
      "env": {}
    }
  }
}
```

#### Configuration Parameters

| Configuration | Description | Required | Default Value |
| --- | --- | --- | --- |
| `command` | Path to the Akeyless CLI binary | Yes | (none) |
| `args.--access-id` | The Akeyless access ID to authenticate with | Yes* (if using the `access_key` access type) | (none) |
| `args.--access-key` | The Akeyless access key to authenticate with | Yes* (if using the `access_key` access type) | (none) |
| `args.--access-type` | Authentication method type to use. See [Access type values](#access-type-values). | Yes | `access_key` |
| `args.--account-id` | Used to select which Akeyless account to use if the `--admin-email` is associated with more than one account | No | (none) |
| `args.--admin-password` | The Akeyless account password to authenticate with | Yes* (if using the `password` access type) | (none) |
| `args.--admin-email` | The Akeyless account email address to authenticate with | Yes* (if using the `password` access type) | (none) |
| `args.--cert-challenge` | Certificate challenge encoded in base64 (relevant only for the `cert` access type) | Yes* (if using the `cert` access type and `args.--key-file-name` or `args.--key-data` is not used) | (none) |
| `args.--cert-data` | Certificate data encoded in base64, used if a file was not provided (relevant only for the `cert` access type) | Yes* (if using the `cert` access type and `args.--cert-file-name` is not used) | (none) |
| `args.--cert-file-name` | Path to where the certificate file for certificate authentication is located | Yes* (if using the `cert` access type and `args.--cert-data` is not used) | (none) |
| `args.--cloud-id` | The identity for the chosen cloud provider. See [Cloud ID values](#cloud-id-values). | Yes* (if using the `aws_iam`, `azure_id`, `gcp`, or `oci` access types) | (none) |
| `args.--debug` | Enable debug logging | No | `false` |
| `args.--disable-kerberos-fast` | Disable Kerberos FAST negotiation | No | `true` |
| `args.--gateway-spn` | The service principal name of the gateway as registered in LDAP | No | (none) |
| `args.--gateway-url` | Akeyless Gateway URL | Yes (must be passed in-line for `akeyless mcp`) | (none) |
| `args.--gcp.audience` | GCP audience to use with signed JWT (relevant only for the `gcp` access type) | No | `akeyless.io` |
| `args.--jwt` | The JSON Web Token | Yes* (if using the `jwt` or `oidc` access type) | (none) |
| `args.--k8s-auth-config-name` | The Kubernetes Auth config name | Yes* (if using the `k8s` access type) | (none) |
| `args.--k8s-service-account-token` | The Kubernetes ServiceAccount token | Yes* (if using the `k8s` access type) | (none) |
| `args.--kerberos-token` | Kerberos token for the gateway SPN, used by SPNEGO for authentication | No | (none) |
| `args.--kerberos-username` | The username for the entry within the keytab to authenticate by way of Kerberos | No | (none) |
| `args.--key-data` | Private key data encoded in base64 | Yes* (if using the `cert` access type and `args.--key-file-name` or `args.--cert-challenge` is not used) | (none) |
| `args.--key-file-name` | Path to where the key file is located | Yes* (if using the `cert` access type and `args.--key-data` or `args.--cert-challenge` is not used) | (none) |
| `args.--keytab-file-data` | Base64-encoded content of a valid keytab file, containing the service account's entry | Yes* (if using the `kerberos` access type and `args.--keytab-file-path` is not used) | (none) |
| `args.--keytab-file-path` | The path to a valid keytab file, containing the user entry | Yes* (if using the `kerberos` access type and `args.--keytab-file-data` is not used) | (none) |
| `args.--krb5conf-file-data` | Base64-encoded content of a valid `krb5.conf` file, specifying the settings and parameters required for Kerberos authentication | Yes* (if using the `kerberos` access type and `args.--krb5conf-file-path` is not used) | (none) |
| `args.--krb5conf-file-path` | Path to a valid `krb5.conf` file, specifying the settings and parameters required for Kerberos authentication | Yes* (if using the `kerberos` access type and `args.--krb5conf-file-data` is not used) | (none) |
| `args.--ldap-proxy-url` | Address URL for LDAP proxy | Yes* (if using the `ldap` access type) | (none) |
| `args.--oci-auth-type` | The type of the OCI configuration to use. See [OCI auth type values](#oci-auth-type-values). | No | `apikey` |
| `args.--oci-group-ocid` | A list of Oracle Cloud IDs groups | Yes* (if using the `oci` access type) | (none) |
| `args.--oidc-sp` | OIDC Service Provider (relevant only for the `oidc` access type). Inferred if empty. Supported SPs: `google`, `github`. | No | (inferred) |
| `args.--password` | LDAP password | Yes* (if using the `ldap` access type) | (none) |
| `args.--profile` | The CLI profile name to use for authentication context (the profile `gateway_url` is not used by `akeyless mcp`) | No | `default` |
| `args.--signed-cert-challenge` | Signed certificate challenge encoded in base64 (relevant only for the `cert` access type) | No | (none) |
| `args.--uid-token` | The Universal Identity token | Yes* (if using the `universal_identity` access type) | (none) |
| `args.--use-remote-browser` | Returns a link to complete authentication remotely (relevant only for the `saml` and `oidc` access types) | No | (none) |
| `args.--username` | LDAP username | Yes* (if using the `ldap` access type) | (none) |

##### Access type values

Acceptable values for `args.--access-type`:

* [access_key](https://docs.akeyless.io/docs/auth-with-api-key)
* [aws_iam](https://docs.akeyless.io/docs/auth-with-aws)
* [azure_ad](https://docs.akeyless.io/docs/auth-with-azure)
* [cert](https://docs.akeyless.io/docs/auth-with-certificate)
* [gcp](https://docs.akeyless.io/docs/auth-with-gcp)
* [jwt](https://docs.akeyless.io/docs/auth-with-oauth-jwt)
* [k8s](https://docs.akeyless.io/docs/auth-with-kubernetes)
* [kerberos](https://docs.akeyless.io/docs/auth-with-kerberos)
* [ldap](https://docs.akeyless.io/docs/auth-with-ldap)
* [oci](https://docs.akeyless.io/docs/auth-with-oci)
* [oidc](https://docs.akeyless.io/docs/auth-with-oidc)
* [password](https://docs.akeyless.io/docs/auth-with-email)
* [saml](https://docs.akeyless.io/docs/auth-with-saml)
* [universal_identity](https://docs.akeyless.io/docs/auth-with-universal-identity)

##### Cloud ID values

Acceptable values for `args.--cloud-id`:

* `aws_iam`
* `azure_id`
* `gcp`
* `oci`

##### OCI auth type values

Acceptable values for `args.--oci-auth-type`:

* `apikey`
* `instance`
* `resource`

#### Example Authentication Method Configurations

The Akeyless MCP server supports multiple [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods):

##### Access Key Authentication (Default)

```json
{
  "args": [
    "mcp",
    "--access-id", "p-xxxxxxxxxxxxx",
    "--access-key", "your-access-key",
    "--access-type", "access_key",
    "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
  ]
}
```

##### Certificate Authentication

```json
{
  "args": [
    "mcp",
    "--access-type", "cert",
    "--cert-file-name", "/path/to/cert.pem",
    "--key-file-name", "/path/to/key.pem",
    "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
  ]
}
```

##### Cloud Provider Authentication

```json AWS
{
  "args": [
    "mcp",
    "--access-type", "aws_iam",
    "--cloud-id", "your-aws-role-arn",
    "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
  ]
}
```
```json Azure
{
  "args": [
    "mcp",
    "--access-type", "azure_ad",
    "--cloud-id", "your-azure-client-id",
    "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
  ]
}
```
```json GCP
{
  "args": [
    "mcp",
    "--access-type", "gcp",
    "--cloud-id", "your-gcp-service-account",
    "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
  ]
}
```

##### Kubernetes Authentication

```json
{
  "args": [
    "mcp",
    "--access-type", "k8s",
    "--k8s-auth-config-name", "your-config-object",
    "--k8s-service-account-token", "your-service-account-token",
    "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
  ]
}
```

##### LDAP Authentication

```json
{
  "args": [
    "mcp",
    "--access-type", "ldap",
    "--ldap-proxy-url", "ldap://your-ldap-server",
    "--username", "your-username",
    "--password", "your-password",
    "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
  ]
}
```

##### OIDC/JWT Authentication

```json
{
  "args": [
    "mcp",
    "--access-type", "oidc",
    "--jwt", "your-jwt-token",
    "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
  ]
}
```

##### Password Authentication

```json
{
  "args": [
    "mcp",
    "--admin-email", "user@example.com",
    "--admin-password", "your-password",
    "--access-type", "password",
    "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
  ]
}
```

##### SAML Authentication

```json
{
  "args": [
    "mcp",
    "--access-type", "saml",
    "--gateway-url", "https://<your-gateway-url>:8000/api/v2"
  ]
}
```

### Client Notes

* Pass `--gateway-url` directly in the MCP client configuration or command line.
* If you use JetBrains IDEs, install the dedicated plugin instead of wiring the server manually.
* Keep the CLI profile name consistent across your MCP clients so authentication behavior stays predictable.

## Best Practices

### Security Best Practices

* Use Environment Variables: Store sensitive credentials in environment variables rather than hardcoding them
* Principle of Least Privilege: Create dedicated access keys with minimal required permissions
* Regular Rotation: Rotate access keys regularly
* Secure Storage: Use secure credential storage solutions
* Network Security: Use HTTPS endpoints and consider VPN access

For prompt injection risk reduction guidance for agent-based workflows, see <Anchor label="Prompt Injection Protection for AI Agents" href="doc:prompt-injection-protection-for-ai-agents" />.

### Configuration Management

* Version Control: Keep MCP configuration files in version control (excluding secrets)
* Environment Separation: Use separate configurations for different environments
* Documentation: Document your configuration choices and rationale
* Testing: Test configurations in development before deploying to production

### Monitoring and Logging

* Enable Debug Mode: Use the `--debug` flag for troubleshooting
* Monitor Access: Regularly review access logs and analytics
* Set Up Alerts: Configure alerts for unusual access patterns
* Audit Trail: Maintain audit trails for compliance requirements

### Performance Optimization

* Connection Pooling: Reuse connections when possible
* Caching: Implement appropriate caching strategies
* Batch Operations: Use batch operations for multiple items
* Resource Limits: Set appropriate resource limits

## Troubleshooting: Common Issues and Solutions

### Authentication Failures

#### Akeyless MCP Server Fails to Authenticate

1. Verify access ID and access key are correct
2. Check if credentials have expired
3. Ensure proper permissions are assigned
4. Verify gateway URL is accessible

<!-- secret-stdout-scan:ok -->
```shell
# Test authentication manually
akeyless auth --access-id "your-access-id" --access-key "your-access-key"
```

### Connection Issues

#### Cannot Connect to the Akeyless Gateway

* Check network connectivity
* Verify gateway URL format
* Check firewall settings
* Test with curl or wget:

```shell
# Test connectivity
curl -I https://<your-gateway-url>:8000/api/v2
```
```text Sample Output
HTTP/2 405 
date: Fri, 03 Oct 2025 20:36:32 GMT
content-type: application/json
content-length: 68
cache-control: no-cache, no-store, must-revalidate, private
content-security-policy: img-src 'self' data:;
cross-origin-opener-policy: same-origin
cross-origin-resource-policy: same-origin
expires: 0
permissions-policy: geolocation=(self), microphone=(self), camera=(self), payment=(self)
pragma: no-cache
referrer-policy: no-referrer-when-downgrade
vary: Origin
x-content-type-options: nosniff
x-frame-options: SAMEORIGIN
```

### Permission Errors

#### Insufficient Permissions for Operations

* Review role assignments
* Check item-level permissions
* Verify authentication method permissions
* Contact administrator for access

### Configuration Errors

#### MCP Server Fails to Start

* Validate JSON configuration syntax
* Check file paths are correct
* Verify command arguments
* Review environment variables

## Related AI Guides

* <Anchor label="Prompt Injection Protection for AI Agents" href="doc:prompt-injection-protection-for-ai-agents" />
