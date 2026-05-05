---
title: Desktop Application
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
The Desktop Application is designed to work across Windows and macOS. It enables access to various targets using native clients such as database clients, SSH terminals, or RDP software.

Who benefits from using this application?

* IT Administrators and DevOps Teams
* Security Professionals
* Developers and Engineers

> ℹ️ **Note:**
>
> The Desktop Application is currently in beta.

## Prerequisites

* **Windows** or **macOS Ventura** / **Monterey** / **Big Sur** operating system.

### Permissions

The Desktop Application creates a tunnel to the designated resource and securely injects the password. To support this process, any user working with the Desktop Application must have [read permission](https://docs.akeyless.io/docs/rbac#permissions-for-items-access-roles-auth-methods-and-targets) on the Secret Item.

> ℹ️ **Note (Tunnel-Based Connections):**
>
> The Desktop Application establishes connections by way of an encrypted tunnel. Because the bastion cannot inspect tunnel traffic, **session recordings are not captured** for Desktop Application sessions. Additionally, **secretless access does not apply**—users must have explicit `Read` permission on the secret item. See [Tunnels](https://docs.akeyless.io/docs/sra-tunnels) for details.

## Installation Guide

Download the relevant Desktop Application installer from ([https://download.akeyless.io/Akeyless_Artifacts/](https://download.akeyless.io/Akeyless_Artifacts/)).

### Windows Installation

1. Open Windows Command Prompt as an administrator and generate private and public SSH keys locally. You can use the following command: `ssh-keygen -t rsa`. This creates an `.ssh` folder with the `id_rsa` and `id_rsa.pub` files.

2. Run the `.exe` file and follow the setup wizard.

3. Grant necessary permissions if prompted.

    The Desktop Application installs at `C:/Users/<username>/AppData/Roaming/Akeyless-desktop`.

4. Open the app and sign in with your Akeyless credentials.

### macOS Installation

1. After downloading the appropriate installer file, locate it in your `Downloads` folder or the directory you specified.

2. Open it and drag the Akeyless Remote Access app to the Applications folder.

3. Grant required permissions in **System Preferences** → **Security & Privacy**.

    The Desktop Application installs at `~/Library/Application Support/Akeyless-Desktop`.

4. Open the app and sign in with your Akeyless credentials.

> ℹ️ **Note (Installation Folder):**
>
> The installation folder contains the following:
>
1. **`config.json`** - The configuration file (contains the basic parameters required to launch the Desktop Application). This file can be deployed by an admin across the organization.
>
> 1. **Logs** - Located at `Akeyless-desktop/logs`.

## How It Works

1. The Desktop Application retrieves connection details from the target item (For example, `MY-MSSQL-connection`) and initiates a connection.

2. It uses the Akeyless CLI to establish a tunnel, leveraging the SSH certificate configured in the **Defaults Configuration** window.

    > ⚠️ **Warning (Important):**
    >
    > 1. If you don't have an SSH certificate yet, please follow this guide on creating an [SSH Cert issuer](https://docs.akeyless.io/docs/sra-ssh-certificates) with Akeyless and set your `CAPublicKey` in the `values` file.
    > 2. You also need to enable Secure Remote Access on the SSH Cert Issuer either in the UI or by adding the `--secure-access-enable true` flag to your CLI command.
    > 3. Ensure that the `akeyless` user is added to the list of `Allowed User(s)` in the SSH Cert Issuer item. Otherwise, the desktop application will not be able to establish a connection.

3. Upon successfully connecting to the remote target, the Desktop Application launches the default application configured for this resource type.

> ℹ️ **Note:**
>
> Applications such as **Azure Data Studio**, **Windows App**, **DBeaver**, **PuTTY**, **WinSCP**, and others should already be installed on the local machine where the desktop application is installed.

## Configuration & First-Time Setup

1. Log in to the Desktop Application (using SAML, OIDC, Certificate, Access Key, and so on). You should see a list of the resources you can connect to based on your permissions. If you want to add or remove targets from the list, update your permissions accordingly.
2. **Application Mapping** - To connect to remote resources, users should map them to applications. When using a mapped application, the desktop application launches the native application and securely initiates the connection.
3. Listed below are the native clients that are supported by the Desktop Application:

    | Operating System | Resource | Application Type | Comments |
    | --- | --- | --- | --- |
    | **Windows** | MSSQL Server | Azure Data Studio |  |
    |  | RDP | Remote Desktop |  |
    |  | Postgres DB | DBeaver |  |
    |  | SSH Cert Issuer | PuTTY | WinSCP is a prerequisite for PuTTY. |
    |  | SSH username and password | PuTTY | Specify port `2022`. |
    |  | SSH File Transfer | WinSCP | Note: File transfers for certificate-based targets have a known limitation and are currently not supported. |
    |  | PowerShell | PuTTY | PS tag should be configured on the secret item. |
    |  | Direct Connection and Secure Remote Access | Default Browser |  |
    | **macOS** | MSSQL Server | Azure Data Studio |  |
    |  | Postgres DB | DBeaver |  |
    |  | RDP | Windows App |  |
    |  | SSH Cert Issuer | Terminal |  |
    |  | SSH username and password | Terminal |  |
    |  | Direct Connection and Secure Remote Access | Default Browser |  |
    |  | SSH File Transfer (SFTP) | Terminal |  |

    > ⚠️ **Warning (Multiple hosts and linked targets):**
    >
    > The Desktop Application supports multiple hosts and linked targets. You can add or remove hosts you want to connect to, and then select **Confirm**.
    >
    > Removing a host from the list only removes it from the Desktop Application host list.

4. Configure the **Defaults Configuration** - When connecting to a remote target, the Desktop Application fetches the required parameters from the resource item (the target you want to connect to). If this information is not accessible to the Desktop Application, it uses the information configured in Advanced Configuration.

    * **Web Application Dispatcher** and **Web Proxy URL** - Should be provided if working with the Zero Trust Web Access solution (ZTWA).
    * **Secure SSH Access Address** (recommended) - This is the path and port for SSH deployment (`my.SSH.address`).
    * **SSH Certificate Issuer** (recommended) - This is the name of the SSH Certificate Issuer that the Akeyless CLI uses to initiate the connection.
    * **Control API Port** - The control API port (specify `8000` for a unified Gateway, or `9900` otherwise).
    * **Control API Path** - The SRA control API path (for example, `/sra/ssh-config`).

> ℹ️ **Note (Connection Failures):**
>
> If the desktop application fails to connect to the resource, it will display a message prompting you to verify your configuration.
>
> The Desktop log contains additional information that can help during an investigation.
