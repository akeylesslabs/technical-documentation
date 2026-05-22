---
title: n8n nodes akeyless
deprecated: false
hidden: false
metadata:
  robots: index
---
The Akeyless node for n8n integrates with Akeyless Secrets Management. Use it to retrieve, create, and manage secrets in your n8n workflows without hardcoding sensitive values.

## What You Can Do

* Retrieve secrets (static, rotated, dynamic)
* Create new secrets
* Delete secrets and items
* Create and delete folders
* Use secrets dynamically in workflows

## Installation

### n8n Cloud (SaaS)

1. Open the n8n instance.
2. Go to **Settings** → **Community Nodes**.
3. Enter `n8n-nodes-akeyless-io` as the npm package name.
4. Accept the risk notice, and click **Install**.
5. Reload or restart the editor if prompted.

### Self-hosted n8n

On the host where n8n loads custom nodes, run:

```shell
cd ~/.n8n/nodes && npm install n8n-nodes-akeyless-io
```

Restart n8n.

## Getting Started

### Step 1: Configure Credentials

In n8n, go to Credentials → Add Credential

Select Akeyless Security

Choose an authentication method:

#### Method A: Access ID + Access Key (Recommended)

* API Base URL: `https://api.akeyless.io` (or your Akeyless instance URL)
* Access ID: Your Akeyless Access ID (starts with p-)
* Access Key: Your Base64-encoded Access Key
* Ignore SSL Issues: Leave unchecked unless using self-signed certificates

#### Method B: Token (T-token)

* API Base URL: `https://api.akeyless.io`
* Token: Your Akeyless token (starts with t-)
* Ignore SSL Issues: Leave unchecked unless using self-signed certificates

### Step 2: Add the Akeyless Node

1. In your workflow, click Add Node
2. Search for "Akeyless"
3. Select the Akeyless node
4. Choose your credential from the dropdown
5. Select an operation

## Available Operations

1. Get Static Secret Value
   Retrieves a static secret from Akeyless.
   Configuration:

   * Secret Name: The full path to your secret (For example, /production/api-key)
   * Accessibility: Choose regular or personal
   * Ignore Cache: Set to true to bypass cache
     Output Example:

   ```text
   {
     "/production/api-key": "your-secret-value"
   }
   ```

   Use Case: Retrieve API keys, database passwords, or other Static Secrets.

2. Get Rotated Secret Value
   Retrieves a rotated secret (automatically rotated by Akeyless).
   Configuration:

   * Secret Name: The full path to your rotated secret
   * Ignore Cache: Set to true to bypass cache

   Output: Returns the current rotated secret value.
   Use Case: Retrieve database credentials that rotate automatically.

3. Get Dynamic Secret Value
   Retrieves a dynamic secret (generated on-demand).
   Configuration:

   * Secret Name: The full path to your dynamic secret
   * Timeout: Maximum seconds to wait for secret generation (default: 15)

   Output: Returns the dynamically generated secret value.
   Use Case: Generate temporary database access credentials or API tokens.

4. Create Secret
   Creates a new secret in Akeyless.
   Configuration:
   * Secret Name: Full path where the secret will be stored
   * Type: Choose Generic or Password
   * Format: Choose Text or JSON
   * Accessibility: Choose regular or personal
     For Generic Secrets:
   * Secret Value: The value to store
     For Password Secrets:
   * Username: The username
   * Password: The password
     Additional Options:
   * Secure Access Web Browsing: Enable if needed
   * Secure Access Web Proxy: Enable if needed
     Use Case: Store new API keys, create database credentials, or save configuration values.

5. Delete Items
   Deletes one or more items from Akeyless.
   Configuration:
   * Path: The path/name of the item(s) to delete (supports wildcards)
     Use Case: Remove old secrets or clean up unused items.

6. Create Folder
   Creates a new folder in Akeyless.
   Configuration:
   * Folder Name: The name/path of the folder to create
   * Accessibility: Choose regular or personal
     Use Case: Organize secrets into folders (For example, /production/, /staging/).

7. Delete Folder
   Deletes a folder from Akeyless.
   Configuration:
   * Folder Name: The name/path of the folder to delete
   * Accessibility: Choose regular or personal
     Use Case: Remove empty or unused folders.

## Using Secrets in Your Workflows

### Method 1: Direct Expression (Simple Cases)

When the Akeyless node returns a secret, access it directly in the next node:
Example: Get API Key and Use in HTTP Request

_Add Akeyless node:_

* Operation: Get Static Secret Value
* Secret Name: `/myapp/api-key`

_Add HTTP Request node:_

In the Authorization header,

```text
{{$node["Akeyless"].json["/myapp/api-key"]}}
```

### Method 2: Using Set Node (Recommended for Complex Workflows)

Extract the secret value first for cleaner, reusable workflows:

1. Akeyless → Set → HTTP Request
2. Configure Set Node:
   * Add Field: `apiKey`
   * `Value: ={{$json["/myapp/api-key"]}}`
3. Configure HTTP Request:
   * Header: `X-API-Key: {{$json.apiKey}}`

## Resources

* Package on npm: [https://www.npmjs.com/package/n8n-nodes-akeyless-io](https://www.npmjs.com/package/n8n-nodes-akeyless-io)
* GitHub Repository: [https://github.com/akeyless-community/N8N_PlugIn](https://github.com/akeyless-community/N8N_PlugIn)

## Restored Visuals

![Restored visual: Screenshot 2025 11 14 at 16.45.51](https://files.readme.io/ccc9b3bfe271d41087a408b69547c7f8234bd6354fb286c270fdb60a008c5139-Screenshot_2025-11-14_at_16.45.51.png)

![Restored visual: Screenshot 2025 11 17 at 19.22.46](https://files.readme.io/0cb8dee191ebe3c1562733b78e71d9f3c6cf7d0f798953dfb4608119027853c7-Screenshot_2025-11-17_at_19.22.46.png)
