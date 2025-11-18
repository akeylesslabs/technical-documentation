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
# Introduction

The Desktop Application is designed to work across Windows and macOS, It enables access to various targets using native clients such as database clients, SSH terminals, or RDP software.

Who Should benefit from using this application?

* IT Administrators & DevOps Teams
* Security Professionals
* Developers & Engineers

NOTE: currently in its Beta phase

# Pre-Requisite

## Supported OS:

* Windows
* macOS Ventura / Monterey / Big Sur

## Permissions

The Desktop Application creates a tunnel to the designated resource and injects the password securely. To support this to support this process, any user working with the Desktop Application must have [Read permission](https://docs.akeyless.io/docs/rbac#permissions-for-items-access-roles-auth-methods-and-targets) on the Secret Item.

# Installation Guide

Download the respective Desktop Application installation file from [here](https://download.akeyless.io/Akeyless_Artifacts/)

## Windows Installation

1. Open Windows command line as an Administrator and generate Private & Public SSH keys locally. You can use the following command: `ssh-keygen -t rsa`. This will create an .ssh folder with the respective `id_rsa` and `id_rsa.pub` files.
2. Run the .exe file and follow the setup wizard.
3. Grant necessary permissions if prompted

The Desktop Application will be installed at `\Users\<username>\AppData\Roaming\Akeyless-desktop`

4. Launch the application

## macOS Installation

1. After downloading the appropriate installer file, locate it in your `Downloads` folder or the directory you specified.
2. Open it and drag the Akeyless Remote Access app to the Applications folder.
3. Grant required permissions in System Preferences → Security & Privacy.

The Desktop Application will be installed at: `\Users\<username>\Library\Application Support\Akeyless-Desktop`

4. Open the app and sign in with your Akeyless credentials.

> 📘 Info
>
> The installation folder contains the following:
>
> 1. **config.json** - the configuration file (includes the basic configuration parameters required to launch the desktop application). This file can be deployed by the Admin across the organization
> 2. **Logs** - can be found at \Akeyless-desktop\logs

# How it works?

1. The Desktop Application retrieves connection details from the target item (e.g., MY-MSSQL-connection) and initiates a connection.
2. It uses the Akeyless CLI to establish a tunnel, leveraging the SSH certificate configured in the **Defaults Configuration** window

> 🚧 Important
>
> 1. If you don't have an SSH certificate yet, please follow this guide on creating an [SSH Cert issuer](https://docs.akeyless.io/docs/ssh-certificates) with Akeyless and set your `CAPublicKey` in the `values` file.
> 2. You will also need to enable Secure Remote Access on the SSH Cert Issuer either in the UI or by adding the `--secure-access-enable` `true` flag to your CLI command
> 3. Ensure that `akeyless` user is added to the list of `Allowed User(s)` in the SSH-CERT-Issuer item. Otherwise, the desktop application won't be able to establish connection.

3. Upon successfully connecting to the remote target, the Desktop Application launches the default application configured for this resource type.

> 👍 Note
>
> Applications such **Azure Data Studio**, **WindowsApp**, **DBeaver**, **Putty**, **WinSCP**, or others should already be installed on the local machine where the desktop application is installed.

# Configuration & First-Time Setup

1. Logging to the Desktop Application (using SAML, OIDC, Certificate, Access Key, etc).

You should be able to see a list of the resources you can connect to, upon your permissions. If you wish to add / remove targets from the list, you should update your permissions accordingly.

2. **Application Mapping** - In order to connect to remote resources, the user should map them to applications. When using mapped application, the Desktop application launches the native application and securely initiates the connection.
   1. Listed Below are the native clients that supported by the Desktop Application

| Operating System | Resource                                 | Application Type  | Comments                                                                                                  |
| ---------------- | :--------------------------------------- | ----------------- | --------------------------------------------------------------------------------------------------------- |
| **Windows**      | MSSQL Server                             | Azure Data Studio |                                                                                                           |
|                  | RDP                                      | Remote Desktop    |                                                                                                           |
|                  | Postgres DB                              | DBeaver           |                                                                                                           |
|                  | SSH Cert Issuer                          | Putty             | WinSCP is a pre-requisite for Putty                                                                       |
|                  | SSH username & password                  | Putty             | Specify Port 2022                                                                                         |
|                  | SSH File Transfer                        | WinSCP            | NOTE: File transfers for certificate-based targets have a known limitation and currently is not supported |
|                  | Powershell                               | Putty             | PS Tag should be configured on the secret item                                                            |
|                  | Direct Connection / Secure Remote Access | Default Browser   |                                                                                                           |
| **macOS**        | MSSQL Server                             | Azure Data Studio |                                                                                                           |
|                  | Postgres DB                              | DBeaver           |                                                                                                           |
|                  | RDP                                      | WindowsApp        |                                                                                                           |
|                  | SSH Cert Issuer                          | Terminal          |                                                                                                           |
|                  | SSH username & password                  | Terminal          |                                                                                                           |
|                  | Direct Connection / Secure Remote Access | Default Browser   |                                                                                                           |
|                  | SSH File Transfer (SFTP)                 | Terminal          |                                                                                                           |

<br />

> 🚧 Multiple Hosts / Linked Targets
>
> The Desktop Application supports the use of multiple hosts / linked targets. You can easily add / remove hosts you wish to connect to and press on `Confirm`.
>
> > NOTE - Removing host from the list only removes it from the list of hosts in the desktop application.

3. Configure the **Defaults Configuration**  - When connecting to a remote target, the Desktop Application fetches the required parameters from the resource item (aka, the target you wish to connect to). If this information is not accessible to the desktop application, it will use the information configured in the Advanced Configuration.
   1. **Web Application Dispatcher** & **Web Proxy URL** - Should be provided if working with Zero trust Web Access solution (ZTWA)
   2. **Secure SSH Access Address** (recommended) - This is the path & port for SSH deployment (my.SSH.address)
   3. **SSH Certificate Issuer** (recommended) - This is the name of the SSH Certificate Issuer the Akeyless CLI will use to initiate the connection
   4. **Control API Port** - the control API port (specify 8000 for unified Gateway, or 9900 if not)
   5. **Control API Path** - the SRA control API path (for example: /sra/ssh-config)

<br />

> 📘 Connection Failures
>
> If the desktop application fails to connect to the resource, it will display a message prompting you to verify your configuration.
>
> Please note that the Desktop log contains additional information that may help during an investigation.
