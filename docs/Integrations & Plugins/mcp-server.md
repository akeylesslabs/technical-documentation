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

Read more about the [Model Context Protocol](https://modelcontextprotocol.io/).

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

* The Akeyless CLI must be successfully installed and **updated to version 1.130.0+**.
  * Read more about the [Akeyless CLI](https://docs.akeyless.io/update/docs/cli).
  * Learn about [updating the Akeyless CLI](https://docs.akeyless.io/docs/cli-reference#/update).
* An Akeyless account must be created, and a corresponding profile configured with the Akeyless CLI.

## Configuration and Setup

Access to the Akeyless MCP server is set up for an MCP client with a configuration file (for example, `~/.cursor/mcp.json` for Cursor). A list of some available MCP clients is available [here](https://modelcontextprotocol.io/clients).

### Sample Configuration Structure

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
        "--gateway-url", "https://api.akeyless.io"
      ],
      "env": {}
    }
  }
}
```

### Configuration Parameters

| Configuration | Description | Required | Default Value |
|---------------|-------------|----------|---------------|
| `command` | Path to the Akeyless CLI binary | Yes | (none) |
| `args > --access-id` | Your Akeyless access ID | Yes* (if using the access_key access-type) | (none) |
| `args > --access-key` | Your Akeyless access key | Yes* (if using the access_key access-type) | (none) |
| `args > --access-type` | Authentication method | Yes | `access_key` |
| `args > --gateway-url` | Akeyless Gateway URL | No | `https://api.akeyless.io` |
| `args > --profile` | CLI profile name to use | No | `default` |
| `args > --debug` | Enable debug logging | No | `false` |

### Authentication Methods

The Akeyless MCP server supports multiple [Authentication Methods](doc:access-and-authentication-methods):

#### Access Key Authentication (Default)

```json
{
  "args": [
    "mcp",
    "--access-id", "p-xxxxxxxxxxxxx",
    "--access-key", "your-access-key",
    "--access-type", "access_key"
  ]
}
```

#### Password Authentication

```json
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

```json
{
  "args": [
    "mcp",
    "--access-type", "saml",
    "--gateway-url", "https://your-gateway.com"
  ]
}
```

#### OIDC/JWT Authentication

```json
{
  "args": [
    "mcp",
    "--access-type", "oidc",
    "--jwt", "your-jwt-token",
    "--gateway-url", "https://your-gateway.com"
  ]
}
```

#### Kubernetes Authentication

```json
{
  "args": [
    "mcp",
    "--access-type", "aws_iam",
    "--cloud-id", "your-aws-role-arn"
  ]
}
```

#### Cloud Provider Authentication

```json
AWS
{
  "args": [
    "mcp",
    "--access-type", "aws_iam",
    "--cloud-id", "your-aws-role-arn"
  ]
}
```
```json
Azure
{
  "args": [
    "mcp",
    "--access-type", "azure_ad",
    "--cloud-id", "your-azure-client-id"
  ]
}
```
```json
GCP
{
  "args": [
    "mcp",
    "--access-type", "gcp",
    "--cloud-id", "your-gcp-service-account"
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

# Best Practices

## Security Best Practices

1. Use Environment Variables: Store sensitive credentials in environment variables rather than hardcoding them.
2. Principle of Least Privilege: Create dedicated access keys with minimal required permissions.
3. Regular Rotation: Rotate access keys regularly.
4. Secure Storage: Use secure credential storage solutions.
5. Network Security: Use HTTPS endpoints and consider VPN access.

## Configuration Management

1. Version Control: Keep MCP configuration files in version control (excluding secrets).
2. Environment Separation: Use separate configurations for different environments.
3. Documentation: Document your configuration choices and rationale.
4. Testing: Test configurations in development before deploying to production.

## Monitoring and Logging

1. Enable Debug Mode: Use the --debug flag for troubleshooting.
2. Monitor Access: Regularly review access logs and analytics.
3. Set Up Alerts: Configure alerts for unusual access patterns.
4. Audit Trail: Maintain audit trails for compliance requirements.

## Performance Optimization

1. Connection Pooling: Reuse connections when possible.
2. Caching: Implement appropriate caching strategies.
3. Batch Operations: Use batch operations for multiple items.
4. Resource Limits: Set appropriate resource limits.

# Troubleshooting: Common Issues and Solutions

## Authentication Failures

### Akeyless MCP Server fails to authenticate

1. Verify access ID and access key are correct.
2. Check if credentials have expired.
3. Ensure proper permissions are assigned.
4. Verify gateway URL is accessible.

```shell
# Test authentication manually
auth --access-id "your-access-id" --access-key "your-access-key"
```

## Connection Issues

### Cannot connect to the Akeyless Gateway

* Check network connectivity.
* Verify gateway URL format.
* Check firewall settings.
* Test with curl or wget:

```shell
# Test connectivity
curl -I https://api.akeyless.io
```

```text
Sample Output
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

* Review role assignments.
* Check item-level permissions.
* Verify authentication method permissions.
* Contact administrator for access.

## Configuration Errors

### MCP server fails to start

* Validate JSON configuration syntax.
* Check file paths are correct.
* Verify command arguments.
* Review environment variables.