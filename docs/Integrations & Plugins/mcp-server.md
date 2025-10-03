---
title: MCP Server
deprecated: false
hidden: false
metadata:
  robots: index
---
# Overview

The Akeyless Model Context Protocol (MCP) Server is a robust integration that allows AI systems to securely interact with your Akeyless secrets management platform. It provides a standardized interface for AI models to access, manage, and manipulate secrets, keys, certificates, and other sensitive data stored in Akeyless.

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

* The Akeyless CLI must be successfully installed and **updated to version 1.130.0+.**
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

* `command`
  * Path to the Akeyless CLI binary
  * Required: Yes | Default: –
* `--access-id`
  * Your Akeyless access ID
  * Required: Yes* (if using the access_key access-type)
  * Default: (none)
* `--access-key`
  * Your Akeyless access key
  * Required: Yes* (if using the access_key access-type)
  * Default: (none)
* `--access-type`
  * Authentication method
  * Required: Yes
  * Default: `access_key`
* `--gateway-url`
  * Akeyless Gateway URL
  * Required: No
  * Default: [https://api.akeyless.io](https://api.akeyless.io)
* `--profile`
  * CLI profile name to use
  * Required: No
  * Default: default
* `--debug`
  * Enable debug logging
  * Required: No
  * Default: false

### Authentication Methods

Akeyless MCP server supports multiple authentication methods:

1. Access Key Authentication (Default)

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

2. Password Authentication

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

3. SAML Authentication

```json JSON
{
  "args": [
    "mcp",
    "--access-type", "saml",
    "--gateway-url", "https://your-gateway.com"
  ]
}
```

4. OIDC/JWT Authentication

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

5. Kubernetes Authentication

```json JSON
{
  "args": [
    "mcp",
    "--access-type", "aws_iam",
    "--cloud-id", "your-aws-role-arn"
  ]
}
```

6. Cloud Provider Authentication
   1. AWS IAM:
   <br />
   ```json JSON
   {
     "args": [
       "mcp",
       "--access-type", "aws_iam",
       "--cloud-id", "your-aws-role-arn"
     ]
   }
   ```
   1. Azure AD:
   <br />
   ```json JSON
   {
     "args": [
       "mcp",
       "--access-type", "azure_ad",
       "--cloud-id", "your-azure-client-id"
     ]
   }
   ```
   1. Google Cloud:
   <br />
   ```json JSON
   {
     "args": [
       "mcp",
       "--access-type", "gcp",
       "--cloud-id", "your-gcp-service-account"
     ]
   }
   ```

<br />

7. Certificate Authentication

```json JSON
{
  "args": [
    "mcp",
    "--access-type", "cert",
    "--cert-file-name", "/path/to/cert.pem",
    "--key-file-name", "/path/to/key.pem"
  ]
}
```

8. LDAP Authentication

```json JSON
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

1. Security Best Practices
   1. Use Environment Variables: Store sensitive credentials in environment
   2. variables rather than hardcoding them
   3. Principle of Least Privilege: Create dedicated access keys with minimal required permissions
   4. Regular Rotation: Rotate access keys regularly
   5. Secure Storage: Use secure credential storage solutions
   6. Network Security: Use HTTPS endpoints and consider VPN access

<br />

2. Configuration Management
   1. Version Control: Keep MCP configuration files in version control (excluding secrets)
   2. Environment Separation: Use separate configurations for different environments
   3. Documentation: Document your configuration choices and rationale
   4. Testing: Test configurations in development before deploying to production
3. Monitoring and Logging
   1. Enable Debug Mode: Use --debug flag for troubleshooting
   2. Monitor Access: Regularly review access logs and analytics
   3. Set Up Alerts: Configure alerts for unusual access patterns
   4. Audit Trail: Maintain audit trails for compliance requirements
4. Performance Optimization
   1. Connection Pooling: Reuse connections when possible
   2. Caching: Implement appropriate caching strategies
   3. Batch Operations: Use batch operations for multiple items
   4. Resource Limits: Set appropriate resource limits

# Troubleshooting

**Common Issues and Solutions**

1. Authentication Failures
   1. Problem: MCP server fails to authenticate
      Solutions:
      1. Verify access ID and access key are correct
      2. Check if credentials have expired
      3. Ensure proper permissions are assigned
      4. Verify gateway URL is accessible
      <br />
      ```shell CLI
      # Test authentication manually
      akeyless auth --access-id "your-access-id" --access-key "your-access-key"
      ```
2. Connection Issues
   1. Problem: Cannot connect to Akeyless gateway
      Solutions:
      * Check network connectivity
      * Verify gateway URL format
      * Check firewall settings
      * Test with curl or wget
      <br />
      ```shell CLI
      # Test connectivity
      curl -I https://api.akeyless.io
      ```

<br />

3. Permission Errors
   1. Problem: Insufficient permissions for operations
      Solutions:
      * Review role assignments
      * Check item-level permissions
      * Verify authentication method permissions
      * Contact administrator for access
4. Configuration Errors
   1. Problem: MCP server fails to start
      Solutions:
      * Validate JSON configuration syntax
      * Check file paths are correct
      * Verify command arguments
      * Review environment variables
