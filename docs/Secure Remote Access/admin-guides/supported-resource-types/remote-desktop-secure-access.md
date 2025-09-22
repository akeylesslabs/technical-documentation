---
title: Remote Desktop Access
excerpt: Secure remote access to a Windows machine
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
You can enable secure remote access to a Windows machine with a [Dynamic Secret](doc:rdp-dynamic-secrets) that generates ephemeral credentials for the machine or a [Rotated Secret](https://docs.akeyless.io/docs/windows-rotated-secret). Users can access the Windows machine from the Secure Remote Access Portal over the web.

# Prerequisites

To enable secure remote access to a Windows machine you need:

- [Secure Remote Access](https://docs.akeyless.io/docs/remote-access-setup-overview) deployed.

# Create an RDP Secret

If you don't already have an RDP secret, see the following docs to either create a [Dynamic Secret](https://docs.akeyless.io/docs/rdp-dynamic-secrets) or [Rotated Secret](https://docs.akeyless.io/docs/windows-rotated-secret) that specifies the Windows machine details and access credentials.

If you already have a relevant secret, continue below.

# Set Up Remote Access to a Windows Machine from the Akeyless CLI

Let's set up remote access to a Windows Machine using the Akeyless CLI. If you’d prefer, see how to do this from the [Akeyless Console](https://docs.akeyless.io/docs/remote-desktop-secure-access#set-up-remote-access-to-a-windows-machine-from-the-akeyless-console) instead.

Run the relevant command to define the following fields to the secret that specifies the Windows machine details and access credentials:

```shell Dynamic Secret
akeyless dynamic-secret update rdp \
--name <dynamic secret name> \
--secure-access-enable true \
--secure-access-host <hostname or IP> \
--secure-access-rdp-domain <domain name>
```
```shell Rotated Secret
akeyless rotated-secret update windows \
--name <rotated secret name> \
--secure-access-enable true \
--secure-access-host <hostname or IP> \
--secure-access-rdp-domain <domain name> \
--rotate-after-disconnect <true|false>
```

where:

- **secure-access-host:** The hostname (or IP address) for accessing the Windows machine as defined in the dynamic secret. For multiple values repeat this flag.
- **secure-access-rdp-domain:** Optional, only required when the dynamic secret is configured to create credentials for a fixed user. This option defines the domain to which the Windows user for whom credentials are created belongs.

Optional: 

- **secure-access-rdp-user :** Override the RDP Domain username. 
- **secure-access-allow-external-user:** Allow providing external user for a domain users [true/false].
- **rotate-after-disconnect:** Optional for Rotated Secret. Rotate the secret value when the SRA session ends.
- **secure-access-rd-gateway-server:** Optional for Dynamic Secret, to connect from SRA to the remote host via an RD-Gateway server.

# Set Up Remote Access to a Windows Machine from the Akeyless Console

Let's set up remote access to a Windows Machine from the Akeyless Console. If you'd prefer, see how to do this from the [Akeyless CLI](https://docs.akeyless.io/docs/remote-desktop-secure-access#set-up-remote-access-to-a-windows-machine-from-the-akeyless-cli) instead.

1. Log in to the Akeyless Console and go to **Items**.

2. Select the Dynamic Secret or the Rotated Secret that specifies the Windows machine details and access credentials.

3. Click on the **Secure Remote Access** tab, select the pencil icon and enable **Secure Remote Access**, then fill in the following fields:

- `Host(s)`: The hostname (or IP address) for accessing the Windows machine as defined in the dynamic secret.
- `Domain`: Optional for Dynamic Secret. Only required when the dynamic secret is configured to create credentials for a fixed user. This option defines the domain to which the Windows user for whom credentials are created belongs.
- `Override User`: Optional for Dynamic Secret. Override the RDP Domain username. 
- `Allow Providing External Username`: Optional for Dynamic Secret. Select to enable an external username to log in to the target host.
- `RD Gateway`: Optional for Dynamic Secret. Connect from SRA to the remote host via an RD-Gateway server.
- `Rotate after disconnection`: Optional for Rotated Secret. Rotate the secret value when the SRA session ends.

4. To the right of the ** Enable Secure Remote Access ** field, select the tick mark icon to save your changes.

# Access a Windows Machine Over the Web from the Secure Remote Access Portal

1. [Log in](https://docs.akeyless.io/docs/access-resources-remotely#connect-from-the-secure-remote-access-portal) to the Secure Remote Access Portal and select **Remote Desktop**.

2. Select the Windows machine hostname or IP address, then select **Connect**.  
   A new tab opens, in which you can interact with the Windows machine according to your permissions.

3. To lock the RDP screen, you can leverage the **On-Screen Keyboard (OSK)**- when using your own keyboard, press “Ctrl + Alt” and hit “Del” on the OSK inside your RDP session. Alternatively, you can simply close the relevant tab to disconnect the session.

4. If you are locked out of a session, click on the "Unlock" button at the top of your screen and you will be given the option to reconnect to your session. **IMPORTANT** This option is only supported with the installation of our [Remote Access (SRA) Web Extension](https://chromewebstore.google.com/search/Akeyless%20SRA) on your browser.

> 📘 Session In Use Indicator
> 
> For RDP sessions using a **Rotated Secret** or **Static Secret**, there will be a text indicator showing "In use" next to any sessions that are currently occupied by another user.
> 
> To enable this feature, the Auth Method used for the Gateway-SRA privileged Access-ID requires an Access Role with the _Update_ permission on the relevant items' path

# Inject a Fixed User Password Automatically

While working with fixed users, Secure Remote Access can automatically inject your **own** password if stored under your **[personal folder](https://docs.akeyless.io/docs/password-manager#personal-folder)**.

Create a new [Static Secret](doc:static-secrets) under your **personal** folder with the exact full name of the relevant [Dynamic Secret](doc:how-to-create-dynamic-secret).

# Download & Upload Files

Based on your permissions, you will have the ability to upload files from your local machine into the remote Windows machine or download files from the remote Windows machine to your local machine.

To download files from a remote server, simply drag the desired files into the `Download` folder inside the mounted virtual disk named `file-share on Guacamole RDP` located under `This PC`, and a download process will start immediately where the file will be put into your local machine's Download folder. To upload files, use the **Upload** button on top of your session actions bar menu. The files you upload will be located in the same shared drive. 

> 📘 Info
> 
> **Mounted Folder**  
> Notice that upload stores (temporarily) the file on the secure remote access server, please make sure it has enough disk space. The files will be cleared after the user disconnects.