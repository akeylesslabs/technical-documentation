---
title: Cursor-AI / VS Code IDE Plug-In
excerpt: >-
  Find and fix hardcoded secrets in your code by integrating directly with
  Akeyless
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
### Akeyless Secrets Manager for Cursor

This extension helps you find and fix hardcoded secrets (like API keys and passwords) in your code by integrating directly with Akeyless.

<Image border={false} src="https://files.readme.io/8f791b6d749c7143a20f17d544592b57aa3b04ffd690c75dfcbb113fe3470bcc-Screenshot_2025-08-04_at_14.24.37.png" />

<br />

#### What It Does

The Akeyless Secrets Manager extension brings enterprise-grade secret management directly into your Cursor development environment. It automatically detects hardcoded secrets in your code and provides seamless integration with your Akeyless vault.

#### Key Features

#### Automatic Secret Detection

Scans your code and highlights potential secrets as you type.

<Image border={false} src="https://files.readme.io/7776cce54a76236bc12a091bd8e2bc5a84d32c3d62b9cd4489b6615246dccfaf-scan_for_secrets.gif" />

<br />

#### Save to Akeyless

Right-click on a highlighted secret to move it securely to your Akeyless vault.

<Image border={false} src="https://files.readme.io/153f8d1518ecd7095146d63ca9fa65a94a90ac328d8642919b6ecf03907016e0-save_secrets_to_akeyless.gif" />

<br />

#### Integrated Experience

View alerts in the “Problems” panel and manage all your Akeyless secrets from a dedicated sidebar within Cursor.

Command Palette Integration
Use Cursor’s command palette to scan your entire codebase for hardcoded secrets.

#### Getting Started

**Step 1: Install Akeyless CLI**
Before using the extension, you must have the Akeyless CLI installed and be authenticated.

```shell
# Install Akeyless CLI (macOS)
brew install akeyless/tap/akeyless

# Or follow instructions on the Akeyless docs for other platforms
# https://docs.akeyless.io/docs/install-cli

# Authenticate with your Akeyless account
akeyless auth
```

**Step 2: Install the Extension**

1. Open Cursor
2. Go to Extensions (Ctrl+Shift+X)
3. Search for “Akeyless Secrets Manager”
4. Click Install

**Step 3: Start Using**

1. Open any code file
2. Press Ctrl+Shift+P and run “Akeyless: Scan for Hardcoded Secrets”
3. Right-click on highlighted secrets to save them to Akeyless
4. Use the sidebar to browse and manage your secrets

#### How to Use

**Scan for Secrets**
Press Ctrl + Shift + P and run “Akeyless: Scan for Hardcoded Secrets”, or simply save the file (Cmd + S) to trigger a scan on the edited file.

<Image border={false} src="https://files.readme.io/8c249761d389466aa3dcc9a5abfaee6740bc42ed689aa69d7d482c97db367187-Oct-06-2025_12-41-23.gif" />

<br />

**Save to Akeyless**
Right-click a detected secret in your code and select “Save to Akeyless”.

**Manage Secrets**

Click the Akeyless icon in the sidebar to browse, search, and copy secrets without leaving your editor.

[Link to Akeyless Secrets Manager on open-vsx](https://open-vsx.org/extension/akeyless/akeyless-secrets-manager)
