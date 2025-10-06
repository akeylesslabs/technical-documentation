---
title: MCP Server
deprecated: false
hidden: false
link:
  new_tab: false
metadata:
  robots: index
---
# Overview

The Akeyless Model Context Protocol (MCP) Server is a robust integration that enables AI systems to securely interact with your Akeyless secrets management platform. It provides a standardized interface for AI models to access, manage, and manipulate secrets, keys, certificates, and other sensitive data stored in Akeyless.

# What is the MCP?

The Model Context Protocol is a standardized protocol that allows AI systems to connect to external data sources and services. It provides a secure, authenticated method for AI models to:

* Access external APIs and services
* Retrieve and manage sensitive data
* Perform operations on behalf of users
* Maintain security boundaries and access controls

Read more about the <Anchor label="Model Context Protocol" target="_blank" href="https://modelcontextprotocol.io/">Model Context Protocol</Anchor>.

# Akeyless MCP Server Features

The Akeyless MCP Server provides comprehensive access to Akeyless functionality, including:

**Core Capabilities**

* Secrets Management: Create, read, update, and delete static secrets
* Encryption & Key Management: Generate, rotate, and manage encryption keys
* Certificate Lifecycle Management: Issue, renew, and manage PKI and SSH certificates
* Dynamic Secrets: Generate temporary credentials for databases and cloud services
* Access Control: Manage roles, permissions, and authentication methods
* Analytics: Retrieve usage analytics and audit data

**Supported Operations**

* List and describe items (such as secrets, keys, certificates)
* Create and update secrets
* Generate dynamic secrets
* Manage authentication methods and roles
* Retrieve analytics data
* Handle targets and associations

# Configuration

## Prerequisites

* The Akeyless CLI must be successfully installed and **updated to version 1.130.0** or newer.
  * Read more about the <Anchor label="Akeyless CLI" target="_blank" href="https://docs.akeyless.io/update/docs/cli">Akeyless CLI</Anchor>.
  * Learn about <Anchor label="updating the Akeyless CLI" target="_blank" href="https://docs.akeyless.io/docs/cli-reference#/update">updating the Akeyless CLI</Anchor>.
* An Akeyless account must be created and a corresponding profile configured with the Akeyless CLI.

## Configuration and Setup

Access to the Akeyless MCP server is setup for a MCP client with a configuration file (for example, `~/.cursor/mcp.json` for Cursor). A list of some available MCP clients is available <Anchor label="here" target="_blank" href="https://modelcontextprotocol.io/clients">here</Anchor>.

### Sample Configuration Structure

```json JSON
{
  "mcpServers": {
    "akeyless": {
      "command": "/path/to/akeyless",
      "args": [
        "mcp",
        "--access-id", "your-access-id",
        "--access-key", "your-access-key",
        "--access-type", "access_key",
        "--gateway-url", "https://api.akeyless.io"
      ],
      "env": {}
    }
  }
}
```

### Configuration Parameters

<Table align={["left","left","left","left"]}>
  <thead>
    <tr>
      <th>
        Configuration
      </th>

      <th>
        Description
      </th>

      <th>
        Required
      </th>

      <th>
        Default Value
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `command`
      </td>

      <td>
        Path to the Akeyless CLI binary
      </td>

      <td>
        Yes
      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--access-id`
      </td>

      <td>
        The Akeyless access ID to authenticate with
      </td>

      <td>
        Yes*
        (if using the access_key access-type)
      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--access-key`
      </td>

      <td>
        The Akeyless access key to authenticate with
      </td>

      <td>
        Yes*
        (if using the `access_key` access type)
      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--access-type`
      </td>

      <td>
        Authentication method type to use
        Acceptable values are:

        * `access_key`
        * `aws_iam`
        * `azure_ad`
        * `cert`
        * `jwt`
        * `k8s`
        * `kerberos`
        * `ldap`
        * `oci`
        * `oidc`
        * `password`
        * `saml`
        * `universal_identity`
      </td>

      <td>
        Yes
      </td>

      <td>
        `access_key`
      </td>
    </tr>

    <tr>
      <td>
        `args.--account-id`
      </td>

      <td>
        Used to select which Akeyless account to use if the `--admin-email` is associated with more than one account
      </td>

      <td>
        No
      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--admin-password`
      </td>

      <td>
        The Akeyless account password to authenticate with
      </td>

      <td>
        Yes*
        (if using the `password` access type)
      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--admin-email`
      </td>

      <td>
        The Akeyless account email address to authenticate with
      </td>

      <td>
        Yes*
        (if using the `password` access type)
      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--cert-challenge`
      </td>

      <td>
        Certificate challenge encoded in base64 (relevant only for the `cert` access type)
      </td>

      <td>

      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--cert-data`
      </td>

      <td>
        Certificate data encoded in base64, used if file was not provided (relevant only for the `cert` access-type)
      </td>

      <td>

      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--cert-file-name`
      </td>

      <td>
        Path to where the certificate file for certificate authentication is located
      </td>

      <td>
        Yes* (if using the `cert` access type)
      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--cloud-id`
      </td>

      <td>
        The identity for the chosen cloud provider.

        * `aws_iam`: The ARN of the AWS IAM Role to authenticate with[^1]
        * `azure_ad`: The Azure Client ID to authenticate with[^2]
        * `gcp`: The GCP service account to authenticate with[^3]
        * `oci`
      </td>

      <td>
        Yes* (if using the `aws_iam`, `azure_id`, or `gcp` access types)
      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--debug`
      </td>

      <td>
        Enable debug logging
      </td>

      <td>
        No
      </td>

      <td>
        `false`
      </td>
    </tr>

    <tr>
      <td>
        `args.--disable-kerberos-fast`
      </td>

      <td>
        Disable Kerberos FAST negotiation
      </td>

      <td>
        No
      </td>

      <td>
        `true`
      </td>
    </tr>

    <tr>
      <td>
        `args.--gateway-spn`
      </td>

      <td>
        The service principal name of the gateway as registered in LDAP
      </td>

      <td>
        No
      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--gateway-url`
      </td>

      <td>
        Akeyless Gateway URL
      </td>

      <td>
        No
      </td>

      <td>
        `https://api.akeyless.io`
      </td>
    </tr>

    <tr>
      <td>
        `args.--gcp.audience`
      </td>

      <td>
        GCP audience to use with signed JWT (relevant only for the `gcp` access type)
      </td>

      <td>
        No
      </td>

      <td>
        `akeyless.io`
      </td>
    </tr>

    <tr>
      <td>
        `args.--jwt`
      </td>

      <td>
        The JSON Web Token
      </td>

      <td>

      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--k8s-auth-config-name`
      </td>

      <td>
        The Kubernetes Auth config name
      </td>

      <td>

      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--k8s-service-account-token`
      </td>

      <td>
        The Kubernetes service account token
      </td>

      <td>

      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--kerberos-token`
      </td>

      <td>
        Kerberos token for the gateway SPN, used by SPNEGO for authentication
      </td>

      <td>
        No
      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--kerberos-username`
      </td>

      <td>
        The username for the entry within the keytab to authenticate via Kerberos
      </td>

      <td>
        No
      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--key-data`
      </td>

      <td>
        Private key data encoded in base64
      </td>

      <td>
        Yes* (if using the `cert` access type and `args.--key-file-data` is not used)
      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--key-file-name`
      </td>

      <td>
        Path to where the key file is located
      </td>

      <td>
        Yes* (if using the `cert` access type and `args.--key-file-name` is not used)
      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--keytab-file-data`
      </td>

      <td>
        Base64-encoded content of a valid keytab file, containing the service account's entry
      </td>

      <td>

      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--keytab-file-path`
      </td>

      <td>
        The path to a valid keytab file, containing the user entry
      </td>

      <td>

      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--krb5conf-file-data`
      </td>

      <td>
        The path to a valid krb5.conf file, specifying the settings and parameters required for Kerberos authentication
      </td>

      <td>

      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--krb5conf-file-path`
      </td>

      <td>
        The path to a valid krb5.conf file, specifying the settings and parameters required for Kerberos authentication
      </td>

      <td>

      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--ldap-proxy-url`
      </td>

      <td>
        Address URL for LDAP proxy
      </td>

      <td>

      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--oci-auth-type`
      </td>

      <td>
        The type of the OCI configuration to use:

        * `apikey`
        * `instance`
        * `resource`
      </td>

      <td>
        No
      </td>

      <td>
        `apikey`
      </td>
    </tr>

    <tr>
      <td>
        `args.--oci-group-ocid`
      </td>

      <td>
        A list of Oracle Cloud IDs groups
      </td>

      <td>

      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--oidc-sp`
      </td>

      <td>
        OIDC Service Provider (relevant only for the `oidc` access type). Inferred if empty. Supported SPs: `google`, `github`
      </td>

      <td>
        No
      </td>

      <td>
        (inferred)
      </td>
    </tr>

    <tr>
      <td>
        `args.--profile`
      </td>

      <td>
        The CLI profile name to use
      </td>

      <td>
        No
      </td>

      <td>
        `default`
      </td>
    </tr>

    <tr>
      <td>
        `args.--signed-cert-challenge`
      </td>

      <td>
        Signed certificate challenge encoded in base64 (relevant only for the `cert` access type)
      </td>

      <td>

      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--uid-token`
      </td>

      <td>
         The Universal Identity token
      </td>

      <td>
        Yes* (if using the `universal_identity` access type)
      </td>

      <td>
        (none)
      </td>
    </tr>

    <tr>
      <td>
        `args.--use-remote-browser`
      </td>

      <td>
        Returns a link to complete the authentication remotely (relevant only for the `saml` and `oidc` access types).
      </td>

      <td>

      </td>

      <td>
        (none)
      </td>
    </tr>
  </tbody>
</Table>

### Example Authentication Method Configurations

The Akeyless MCP server supports multiple <Anchor label="Authentication Methods" target="_blank" href="doc:access-and-authentication-methods">Authentication Methods</Anchor>:

#### Access Key Authentication (Default)

```json JSON
{
  "args": [
    "mcp",
    "--access-id", "p-xxxxxxxxxxxxx",
    "--access-key", "your-access-key",
    "--access-type", "access_key"
  ]
}
```

#### Certificate Authentication

```json
{
  "args": [
    "mcp",
    "--access-type", "cert",
    "--cert-file-name", "/path/to/cert.pem",
    "--key-file-name", "/path/to/key.pem"
  ]
}
```

#### Cloud Provider Authentication

```json AWS
{
  "args": [
    "mcp",
    "--access-type", "aws_iam",
    "--cloud-id", "your-aws-role-arn"
  ]
}
```
```json Azure
{
  "args": [
    "mcp",
    "--access-type", "azure_ad",
    "--cloud-id", "your-azure-client-id"
  ]
}
```
```json GCP
{
  "args": [
    "mcp",
    "--access-type", "gcp",
    "--cloud-id", "your-gcp-service-account"
  ]
}
```

#### Kubernetes Authentication

```json JSON
{
  "args": [
    "mcp",
    "--access-type", "k8s",
    "--k8s-auth-config-name", "your-config-object",
    "--k8s-service-account-token", "your-service-account-token"
  ]
}
```

#### LDAP Authentication

```json
{
  "args": [
    "mcp",
    "--access-type", "ldap",
    "--ldap_proxy_url", "ldap://your-ldap-server",
    "--username", "your-username",
    "--password", "your-password"
  ]
}
```

#### OIDC/JWT Authentication

```json JSON
{
  "args": [
    "mcp",
    "--access-type", "oidc",
    "--jwt", "your-jwt-token",
    "--gateway-url", "https://your-gateway.com"
  ]
}
```

#### Password Authentication

```json JSON
{
  "args": [
    "mcp",
    "--admin-email", "user@example.com",
    "--admin-password", "your-password",
    "--access-type", "password"
  ]
}
```

#### SAML Authentication

```json JSON
{
  "args": [
    "mcp",
    "--access-type", "saml",
    "--gateway-url", "https://your-gateway.com"
  ]
}
```

# Best Practices

## Security Best Practices

* Use Environment Variables: Store sensitive credentials in environment variables rather than hardcoding them
* Principle of Least Privilege: Create dedicated access keys with minimal required permissions
* Regular Rotation: Rotate access keys regularly
* Secure Storage: Use secure credential storage solutions
* Network Security: Use HTTPS endpoints and consider VPN access

## Configuration Management

* Version Control: Keep MCP configuration files in version control (excluding secrets)
* Environment Separation: Use separate configurations for different environments
* Documentation: Document your configuration choices and rationale
* Testing: Test configurations in development before deploying to production

## Monitoring and Logging

* Enable Debug Mode: Use the `--debug` flag for troubleshooting
* Monitor Access: Regularly review access logs and analytics
* Set Up Alerts: Configure alerts for unusual access patterns
* Audit Trail: Maintain audit trails for compliance requirements

## Performance Optimization

* Connection Pooling: Reuse connections when possible
* Caching: Implement appropriate caching strategies
* Batch Operations: Use batch operations for multiple items
* Resource Limits: Set appropriate resource limits

# Troubleshooting: Common Issues and Solutions

## Authentication Failures

### Akeyless MCP Server fails to authenticate

1. Verify access ID and access key are correct
2. Check if credentials have expired
3. Ensure proper permissions are assigned
4. Verify gateway URL is accessible

```shell CLI
# Test authentication manually
akeyless auth --access-id "your-access-id" --access-key "your-access-key"
```

## Connection Issues

### Cannot connect to the Akeyless Gateway

* Check network connectivity
* Verify gateway URL format
* Check firewall settings
* Test with curl or wget:

```shell CLI
# Test connectivity
curl -I https://api.akeyless.io
```

```Text Sample Output
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

## Permission Errors

### Insufficient permissions for operations

* Review role assignments
* Check item-level permissions
* Verify authentication method permissions
* Contact administrator for access

## Configuration Errors

### MCP server fails to start

* Validate JSON configuration syntax
* Check file paths are correct
* Verify command arguments
* Review environment variables

<br />

[^1]: AWS <Anchor label="Amazon Resource Names (ARNs)" target="_blank" href="https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html">Amazon Resource Names (ARNs)</Anchor>  are used to uniquely identify resources across all AWS partitions, regions, and accounts. AWS <Anchor label="Identity and Access Management (IAM) roles" target="_blank" href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html">Identity and Access Management (IAM) roles</Anchor>  are one options for authenticating with AWS.

[^2]: Azure Client IDs, also known as Application IDs, uniquely identity applications when they are registered in Microsoft Entra ID (formerly Azure Active Directory). Read more about [registering a client application in Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application)  .

[^3]: [GCP service accounts](https://cloud.google.com/iam/docs/service-account-overview)  are how applications uniquely authenticate to access GCP services.
