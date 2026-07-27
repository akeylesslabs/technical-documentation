---
title: RDP Dynamic Secrets
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
You can define a Remote Desktop Protocol (RDP) dynamic secret to dynamically generate user credentials for connecting to a specified Windows host.

When a client requests a dynamic secret value, the Akeyless Platform, through your Gateway, connects to the target Windows host over SSH and creates a new user.

## Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview)

- [SSH](https://docs.akeyless.io/docs/ssh-target) or [Windows](https://docs.akeyless.io/docs/windows-target) Target

- SSH access is enabled on the target Windows host (see [Install OpenSSH for Windows](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=gui#install-openssh-for-windows))

- Privileged Windows user with permission to create and remove users

## Create a Dynamic RDP Secret with the CLI

To create a dynamic RDP secret with the CLI using an existing [RDP Target](https://docs.akeyless.io/docs/ssh-target), run the following command:

```shell
akeyless dynamic-secret create rdp \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rdp-user-groups <Group Name> \
--password-length 16
```

Where:

- `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

- `target-name`: A name of the target that enables connection to the Windows host. The name can include the path to the virtual folder where this target resides.

- `gateway-url`: Akeyless Gateway URL (port `8000`).

- `rdp-user-groups`: RDP **UserGroup** name(s). For **Domain Group**s, insert: `DomainName\GroupName`.

- `password-length`: **Optional** The temporary user password length.

- `fixed-user-only[=false]`: Allow access using externally (IdP) provided username

- `fixed-user-claim-keyname[=ext_username]`: For externally provided users, denotes the key-name of IdP claim to extract the username from (relevant only for fixed-user-only=true)

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#rdp) section.

## Fetch a Dynamic RDP Secret Value with the CLI

To fetch a dynamic RDP secret value with the CLI, run the following command:

```shell
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

## Create a Dynamic RDP Secret in the Akeyless Console

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  To start working with Dynamic Secrets from the [Akeyless Console](https://docs.akeyless.io/docs/rdp-dynamic-secrets#create-a-dynamic-rdp-secret-in-the-akeyless-console), you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.
</Callout>

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the RDP secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

   - **Delete Protection**: When enabled, protects the secret from accidental deletion.
   - **Target:** Select an existing [SSH Target](https://docs.akeyless.io/docs/ssh-target) or [Windows Target](https://docs.akeyless.io/docs/windows-target).

     - **Groups:** A comma-separated list of RDP user groups to which the new user should be added.
   - **Display message to the user before TTL expires:** Select this checkbox to allow displaying messages to the user before TTL expires.
   - **Allow user to extend session periodically:** Select this checkbox to allow the user to extend session periodically.
   - **Externally Provided Username:** Select this checkbox to add an existing user based on the user identity which issues the secret value. It is relevant only when authenticating using an external IdP.
   - **Sub Claim Name:** From which Sub Claim configured on your IdP to extract the user, where the default value is `ext_username`
   - **Custom Username Template:** Set a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) for the generated user.
   - **User TTL:** Provide a time-to-live value for a dynamic secret (that is, a token). When TTL expires, the token becomes obsolete.
   - **Temporary Password Length:** Set the length of the temporary password.
   - **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.
   - **Gateway:** Select the Gateway through which the dynamic secret will create users.
   - **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

5. Click **Finish**.

## Fetch a Dynamic RDP Secret Value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click the **Get Dynamic Secret** button.

<br />
