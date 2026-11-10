---
title: SSH Rotated Secret
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
      slug: add-a-rotated-secret-to-a-role
      title: Add a Rotated Secret to a Role
---
You can create a Rotated Secret for either SSH password or a Private key. Before you get started, ensure you have an [SSH Target](https://docs.akeyless.io/docs/ssh-target) that includes the hostname and connection settings, as well as credentials for a privileged user authorized to rotate credentials.

When a client requests a Rotated Secret value, the Akeyless Platform connects to the SSH server through your [Gateway](https://docs.akeyless.io/docs/gateway-overview) to rotate the relevant credential on your target server.

This guide applies to Linux distributions.

## Create a Rotated SSH Secret with the CLI

To create a Rotated SSH Secret using the Akeyless CLI, run the following command:

```shell
akeyless rotated-secret create ssh \
--name <Rotated Secret name>
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--target-name <target name> \
--authentication-credentials <use-user-creds|use-target-creds> \
--password-length 16 \
--rotator-type <password|target|key> \
--rotated-username <username> \
--rotated-password <password> \
--public-key-remote-path ~/.ssh/authorized_keys
--key-file-path </path/to/PRV-Key>                                
--key-data-base64 <base-64 format PRV Key>                             
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC> 
```

Where:

- `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

- `gateway-url`: Akeyless Gateway URL (port `8000`).

- `target-name`: The name of the [SSH Target](https://docs.akeyless.io/docs/ssh-target) with which the Rotated Secret should be associated.

- `authentication-credentials`: Determines how to connect to the target server.
  - `use-user-creds` - Use the credentials defined on the Rotated Secret item.
  - `use-target-creds` - Use the credentials defined on the [SSH Target](https://docs.akeyless.io/docs/ssh-target) item.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  Select `use-target-creds` if the Rotated Secret user is not authorized to change their own password, and a privileged user, like the [SSH Target](https://docs.akeyless.io/docs/ssh-target) user is required to change the password on behalf of the Rotated Secret user.
</Callout>

- `password-length`: **Optional**, The user's password length.
- `rotator-type`: The type of credentials to be rotated. For [SSH Targets](https://docs.akeyless.io/docs/ssh-target), choose:
  - `password` - to rotate the SSH user password specified in the Rotated Secret
  - `target` - to rotate the password for the user specified in the [SSH Target](https://docs.akeyless.io/docs/ssh-target).
  - `key` - to rotate the SSH key pair for the user specified in the Rotated Secret or Target.
- `rotated-username`: The SSH user whose password should be rotated.
- `rotated-password`: The password to rotate.
- `key-data-base64`: The private key encoded in Base64 format.
- `key-file-path`: The path to the private key that will be rotated.
- `public-key-remote-path`: The path of the public key that will be rotated on the server.
- `key-algorithm[=ED25519]`: The key algorithm to generate with when no private key is supplied. options: `ED25519`/ `RSA2048`/ `RSA3072`/ `RSA4096`/ `ECDSA256`/ `ECDSA384`/ `ECDSA521`]
- `auto-rotate`: Enable auto-rotation if you need to update the password regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`.

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#ssh) section.

## Create a Rotated SSH Secret in the Akeyless Console

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  To start working with Rotated Secrets from the [Akeyless Console](https://docs.akeyless.io/docs/create-an-ssh-rotated-secret#create-a-rotated-ssh-secret-in-the-akeyless-console), you need to configure the [Gateway](https://docs.akeyless.io/docs/gateway-overview) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.
</Callout>

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > SSH**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

   - **Delete Protection:** When enabled, it protects the Rotated Secret from accidental deletion.

   - **Target:** Defines the name of the [SSH Target](https://docs.akeyless.io/docs/ssh-target) to be associated with the Rotated Secret.

   - **Authenticate with the following credentials:** Determines how to connect to the target server:
     - **User credentials:** Use the credentials defined inside the Rotated Secret item.

     - **Target credentials:** Use the credentials defined inside the [SSH Target](https://docs.akeyless.io/docs/ssh-target) item.

   <Callout icon="👍" theme="okay">
     ### Note

     Select **Target credentials** if the Rotated Secret user is not authorized to change their own password, and a privileged user, like the [SSH Target](https://docs.akeyless.io/docs/ssh-target) user, is required to change the password on behalf of the Rotated Secret user.
   </Callout>

   - **Rotator type:** Determines the rotator type:
     - **Password**: Rotates the password defined inside the Rotated Secret item.
     - **Key**: Rotates the private key defined inside the Rotated Secret item .
     - **Target**: Rotates the password defined inside the [SSH Target](https://docs.akeyless.io/docs/ssh-target) item.

   - **Username:** Defines the SSH username which password should be rotated (Relevant only for **Password** mode).

   - **Password:** Defines the password to rotate (Relevant only for **Password** mode).

   <Callout icon="👍" theme="okay">
     ### Note

     You can rotate the password for the [SSH Target](https://docs.akeyless.io/docs/ssh-target) too, by creating a Rotated Secret with the **Rotator type** set to **Target**. When you're using a **Target** rotator, the access role with which this Rotated Secret is associated must have read and update permissions on the corresponding Target.
   </Callout>

   - **Private Key:** The private key that will be rotated (Relevant only for **Key** mode).
   - **Public Key:&#x20;**&#x54;he public key that corresponds to the private key, in `OpenSSH authorized_keys`\` format. Derived automatically and not editable.
   - **Algorithm:&#x20;**&#x54;he key algorithm this secret uses. Applied when Akeyless generates the key pair, and preserved on every rotation.
   - **Authorized Keys Remote Path :&#x20;**&#x54;he file on the target server where the public key is written. By Default: `~/.ssh/authorized_keys` .
   - **Rotation Statement:** In this field you can provide a [Custom Rotation Statement](https://docs.akeyless.io/docs/create-an-ssh-rotated-secret#custom-rotation-statement).
   - **Password Length**: Set the user's password length.
   - **Gateway:** Select the Gateway through which the secret will be rotated.
   - **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).
   - **Auto rotate:** Determines if automatic rotation is enabled.
   - **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic password rotations when **Auto Rotate** is enabled.
   - **Rotation hour (local time zone):** Defines the time when the password should be rotated if **Auto Rotate** is enabled.
   - **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click **⊕ Add Notification** and adjust the day count to any number you prefer. This can be done multiple times to be notified more than once.

4. Click **Finish**.

## Custom Rotation Statement

Akeyless Rotated Secret for an [SSH Target](https://docs.akeyless.io/docs/ssh-target) supports a Custom Rotation Statement. This script or command will be executed on the target server after the Secret Rotation operation completes. You can specify any command you need.

For example, you can provide a command that will be executed instead of the default command to perform a Secret Rotation operation and specify three different arguments for it: **USERNAME, NEW_PASSWORD, OLD_PASSWORD**.

Where:

- `USERNAME`: The configured username within the [SSH Target](https://docs.akeyless.io/docs/ssh-target) or Rotated Secret which password should be rotated.

- `OLD_PASSWORD`: The username old password.

- `NEW_PASSWORD`: The new password generated by Akeyless.

(These arguments can also be used within any command or script that will run upon a password rotation attempt on the target server. )

Upon successful execution of your script, the Rotated Secret will be updated.

Syntax:

```shell Custom Rotation Statement
exec_command {{USERNAME}} {{NEW_PASSWORD}} {{OLD_PASSWORD}}
```

Where `exec_command` should be replaced with the path to your script or any existing command your target OS supports.

For example, to rotate a user on some Linux distribution like **RedHat**, the following statement can be used:

```shell
echo '{{USERNAME}}:{{NEW_PASSWORD}}'| chpasswd
```

Another example of rotating Windows service password:

```shell
net user /domain "{{USERNAME}}" {{NEW_PASSWORD}} && sc config "lfsvc" obj= "ad\{{USERNAME}}" password= "{{NEW_PASSWORD}}" && net stop lfsvc && net start lfsvc
```

## Provisioning SSH Keys

In addition to rotating the key(s), you can provision the SSH key(s) to a remote server using any [Target](https://docs.akeyless.io/docs/targets), similarly to [Certificate Provisioning](https://docs.akeyless.io/docs/certificate-provisioning). Target support priority is:

1. **Custom** - A web endpoint invoked using `POST`.
2. **SSH Target**
3. **Windows Target**
4. **Linked Target**

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  For **Custom** targets, provisioning is managed by the customer, so there is no default location to confirm.
</Callout>

For all targets except **Custom**, you're asked to confirm the location where the key(s) should be placed. The default location is taken from the Rotated Secret's default setting, for example, `~/.ssh/authorized_keys`.

By default, only the **public key** is provisioned. You can also choose to include the **private key**, and when you do, you can set a separate remote location for it.

<Callout icon="⚠️" theme="warning">
  ### **Note:**

  If you provision the private key without setting a passphrase, the following warning is displayed: "No passphrase set. The private key will be stored unencrypted on the server. We recommend setting a passphrase". We recommend setting a passphrase to protect the private key at rest on the target server.
</Callout>

### Provisioning SSH Keys Using the Akeyless CLI

To create a provisioning configuration for an SSH Rotated Secret, run the following command:

```shell
akeyless rotated-secret provision create \
--name <Rotated Secret name> \
--target-name <Target name> \
--provision-keys[=public] <public-key/private-key> \
--public-key-remote-path <path> \
--private-key-remote-path <path> \
--private-key-passphrase <passphrase>
```

Where:

- `name`: The SSH Rotated Secret item name.
- `target-name`: The Target to provision the key(s) to.
- `provision-keys`: Which key(s) to provision. Options: `public-key` (default) or `private-key`. Set to `private-key` to also provision the private key.
- `public-key-remote-path`: The path on the target where the public key will be provisioned.
- `private-key-remote-path`: The path on the target where the private key will be provisioned (relevant only when `provision-keys` includes `private-key`).
- `private-key-passphrase`: A passphrase to encrypt the private key with before it's provisioned. If not set, the private key is stored unencrypted on the target.

To update an existing provisioning configuration, run:

```shell
akeyless rotated-secret provision update \
--name <Rotated Secret name> \
--target-name <Target name> \
--provision-keys[=public] <public-key/private-key> \
--public-key-remote-path <path> \
--private-key-remote-path <path> \
--private-key-passphrase <passphrase>
```

To delete a provisioning configuration, run:

```shell
akeyless rotated-secret provision delete \
--name <Rotated Secret name> \
--target-name <Target name>
```

To provision the key(s) immediately, run:

```shell
akeyless rotated-secret provision push \
--name <Rotated Secret name> \
--target-name <Target name>
```

You can find the complete list of parameters for these commands in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#provisioning) section.

### Provisioning SSH Keys Using the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**, find the SSH Rotated Secret you wish to provision.
2. Click on the Rotated Secret item, click on the **Provisioning** tab, and then **Attach**.
3. **Target Name** - Choose an existing [SSH](https://docs.akeyless.io/docs/ssh-target), [Windows](https://docs.akeyless.io/docs/windows-target), or [Linked](https://docs.akeyless.io/docs/linked-target-rotated-secret) Target from the drop-down list, or select **Custom** to provision to a web endpoint using `POST`.
4. For any target other than **Custom**, confirm the **Location** where the public key should be placed. By default, this is taken from the Rotated Secret's default setting (for example, `~/.ssh/authorized_keys`).
5. **Include Private Key** - Enable this option to also provision the private key, then confirm the **Location** where it should be placed.
6. If you enable **Include Private Key** without setting a **Passphrase**, the following warning is displayed: "No passphrase set. The private key will be stored unencrypted on the server. We recommend setting a passphrase".
7. Click **Save**.

### Provisioning Events

SSH key provisioning triggers the following events, which can be monitored from the [Event Center](https://docs.akeyless.io/docs/event-center):

- `ssh-keys-provisioning-success`: When the SSH key(s) are successfully provisioned.
- `ssh-keys-provisioning-failure`: Upon SSH key(s) provisioning failure.

Click **View Details** on an event to see the name of the associated Target.

## Tutorial

Check out our tutorial video on [Creating and Using SSH Rotated Secrets](https://tutorials.akeyless.io/docs/creating-and-using-rotated-secrets).
