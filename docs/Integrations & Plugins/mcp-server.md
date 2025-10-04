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
        `args >
                        --access-id`
      </td>

      <td>
        Your Akeyless access ID
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
        `args >
                        --access-key`
      </td>

      <td>
        Your Akeyless access key
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
        `args >
                        --access-type`
      </td>

      <td>
        Authentication method
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
        `args >
                        --gateway-url`
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
        `args >
                        --profile`
      </td>

      <td>
        CLI profile name to use
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
        `args >
                        --debug`
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
  </tbody>
</Table>

### Authentication Methods

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
    "--access-type", "aws_iam",
    "--cloud-id", "your-aws-role-arn"
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
