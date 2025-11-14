---
title: n8n nodes akeyless
deprecated: false
hidden: true
metadata:
  robots: index
---
The Akeyless node for n8n integrates with Akeyless Vaultless Secrets Management. Use it to retrieve, create, and manage secrets in your n8n workflows without hardcoding sensitive values.

### What You Can Do

<br />

* Retrieve secrets (static, rotated, dynamic)
* Create new secrets
* Delete secrets and items
* Create and delete folders
* Use secrets dynamically in workflows

### Installation

1. For n8n Cloud (SaaS)
2. Open your n8n instance
3. Go to Settings → Community Nodes
4. Search for n8n-nodes-akeyless
5. Click Install
6. Refresh your workflow editor

#### For Self-Hosted n8n


Install via npm in your n8n installation directory:

```shell
npm install n8n-nodes-akeyless
```

Then restart your n8n instance.

### Getting Started


#### Step 1: Configure Credentials


1. In n8n, go to Credentials → Add Credential
2. Select Akeyless Security
3. Choose an authentication method:

#### Method A: Access ID + Access Key (Recommended)


* API Base URL: [https://api.akeyless.io](https://api.akeyless.io) (or your Akeyless instance URL)
* Access ID: Your Akeyless Access ID (starts with p-)
* Access Key: Your Base64 encoded Access Key
* Ignore SSL Issues: Leave unchecked unless using self-signed certificates
* <br />

#### Method B: Token (t-token)


API Base URL: [https://api.akeyless.io](https://api.akeyless.io)
Token: Your Akeyless token (starts with t-)
Ignore SSL Issues: Leave unchecked unless using self-signed certificates
Step 2: Add the Akeyless Node
In your workflow, click Add Node
Search for "Akeyless"
Select the Akeyless node
Choose your credential from the dropdown
Select an operation
