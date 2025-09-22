---
title: SSH Target
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: create-an-ssh-rotated-secret
      title: Create an SSH Rotated Secret
---
You can define an SSH target that will be used with an [SSH Rotated Secret](doc:create-an-ssh-rotated-secret) or [RDP Dynamic Secrets](doc:rdp-dynamic-secrets)

# Create an SSH Target in the CLI

To create an SSH target from the CLI, run the following command:

```shell
akeyless target create ssh \
--name <Target name> \
--host <SSH hostname> \
--port <SSH port> \
--ssh-username <SSH username> \
--ssh-password <SSH password>
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

- `host`: The SSH hostname.

- `port`: The SSH port.

- `ssh-username`: The SSH username.

- `ssh-password`: The SSH password.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorbluesshp) section.

# Create an SSH Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Operating System (SSH)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.  
   For more information, [read here](doc:implement-zero-knowledge).

4. Define the remaining parameters as follows:

- **Hostname**, **Port** and **Username** to set up the connection. 

- **Authentication Type:** In this section, you can select the preferred type of authentication with the SSH server either `SSH Key` or `Password`:

  - Select the **SSH Key** radio button to authenticate with the Private Key and an optional Passphrase.

  - Select the **Password** radio button to authenticate with the password.

Set the following details accordingly: 

- **Private Key:** Provide an SSH private key.

- **Private Key Passphrase:** Enter a passphrase for the SSH key.

- **Password:** Provide a password for the above-mentioned username.

5. Click **Finish**.