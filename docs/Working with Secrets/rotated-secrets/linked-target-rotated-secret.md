---
title: Linked Target Rotated Secret
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
A Rotated Secret that is associated with a [Linked Target](doc:linked-target) offers an easier way to manage automated password rotation for Local users with the same login credentials across different servers simultaneously.

This type of Linked Target by default **Authenticates** using the **Parent** Target credentials, supporting only   **Rotator Types** of **Password** or **Target**.

When using ** Password** as the **Rotator Type**, the Rotated Secret's **username & password** will be rotated on all hosts that are listed inside the [Linked Target](doc:linked-target), where you can choose to either rotate those **Local** users to all have the **same** password or give each of them a **different** password to ensure the best practices of periodic rotation for users across different machines. In this mode, the **Parent Target** credentials will not be rotated as part of the **Linked Target** rotation. Those credentials should be rotated using a dedicated [Rotated Secret](doc:rotated-secrets) for that Target.

When using **Target** as the **Rotator Type** the **Parent** credentials will be rotated, and **all** Local users will have the **same** password on all hosts. Therefore, the best practice in this mode is not to use the credentials of a **domain** user.

When a new server is created in your environment, simply add the relevant hostname to your [Linked Target](doc:linked-target) to gain automated rotation for any new server.

> 📘 Info
> 
> Only Windows/SSH Target are currently supported for Rotated Secrets with Linked Target. In case one of the hosts in a Linked Target item is accessible over a different port from the one that is configured in the Parent Target, make sure to specify the port as part of the host in the Linked Target. e.g: `server01.com:443`.

# Rotator Type Password

To rotate **Local users**  e.g. `ubuntu` or `administrator`, across your servers using a **privileged Domain user** which has access to all servers found in the [Linked Target](doc:linked-target), start by creating an [SSH](doc:ssh-target) or [Windows](doc:windows-target) Target to store your **Domain user **credentials: 

```shell Windows Target
akeyless create-windows-target \
--name <WindowsTargetName> \ 
--hostname <Windows Hostname\IP> \
--username <Domain@WindowsUsername> \
--password <Password>
--domain <YourDomain>
```
```shell SSH Target
akeyless create-ssh-target \
--name <SSHTargetName> \
--host <SSH hostname> \
--port <SSH port> \
--ssh-username <SSH username@domain> \
--ssh-password <SSH password>
```

> 👍 Note
> 
> The **Parent** Target `hostname` will be the first host whose **Local user's ** password will be rotated.
> 
> To Rotate the **Domain user** password, best practice is to create a dedicated Rotated Secret for that Target.

Create a [Linked Target](doc:linked-target)  with the relevant **hosts** to rotate your **Local users'** passwords :

```shell Windows Linked Target
akeyless create-linked-target -n <LinkedTargetName> -p <WindowsTargetName> -s <hosts>
```
```shell SSH Linked Target
akeyless create-linked-target -n <LinkedTargetName> -p <SSHTargetName> -s <hosts> 
```

Create a [Rotated Secret](doc:rotated-secrets) with `rotator-type ` set to `password`: 

```shell Windows
akeyless rotated-secret create windows \
--name <Rotated secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--target-name <LinkedTargetName> \
--authentication-credentials <use-target-creds> \
--rotator-type password \
--rotated-username <Local username> \
--rotated-password <password> \
--same-password false \
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC>
```
```shell SSH
akeyless rotated-secret create ssh \
--name <Rotated secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--target-name <LinkedTargetName> \
--authentication-credentials <use-target-creds> \
--rotator-type password \
--rotated-username <Local username> \
--rotated-password <password> \
--same-password false \
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC>
```

The **Local user**  will be rotated using the **Parent** Target credentials as well across all hosts defined in the Linked Target.

# Rotator Type Target

While working with **Local** users for a wide password rotation, all **Local** users must have the same password on all hosts. 

Create an [SSH](doc:ssh-target) or [Windows](doc:windows-target) Target to store your **Local user **credentials:

```shell Windows Target
akeyless create-windows-target \
--name <WindowsTargetName> \ 
--hostname <Windows Hostname\IP> \
--username <Windows Local Username> \
--password <Password>
```
```shell SSH Target
akeyless create-ssh-target \
--name <SSHTargetName> \
--host <SSH hostname> \
--port <SSH port> \
--ssh-username <SSH username> \
--ssh-password <SSH password>
```

Create a [Linked Target](doc:linked-target)  with the relevant **hosts** to rotate your **local users'** passwords :

```shell Windows Linked Target
akeyless create-linked-target -n <LinkedTargetName> -p <WindowsTargetName> -s <hosts>
```
```shell SSH Linked Target
akeyless create-linked-target -n <LinkedTargetName> -p <SSHTargetName> -s <hosts> 
```

Create a [Rotated Secret](doc:rotated-secrets) with `rotator-type ` as `target-rotator` to rotate the **Parent** Target:

```shell
akeyless create-rotated-secret --name <secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--target-name <ParentTargetName> \
--authentication-credentials <use-target-creds> \
--rotator-type target \
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC>
```

The rotation will generate a new password for the **Parent** Target and will use it for all hosts for the same **Local** user. 

> 🚧 Warning
> 
> Working with `--rotator-type target` supports only Rotated Secret for the **Parent** Target which will trigger rotation on **all** associated **Linked Targets** hosts.

# Fetching a Linked Target Rotated Secret

The secret value format of the Linked Target Rotated Secret is a **key/value** map where `host:port` are the map keys, with `username/password` as their values.

To fetch a Rotated Secret value run the following command:

```shell
akeyless get-rotated-secret-value -name <Rotated secret name>
```

```shell Output
{
    "value":
    {
        "linked_hosts":
        {
            "server01.example:22":
            {
                "username": "ubuntu",
                "password": "zjdd#WM0aOay"
            },
            "server02.example:22":
            {
                "username": "ubuntu",
                "password": "zjdd#WM3a2ax"
            }
        }
    }
}
```

Where you can filter the exact host using `--host <host>`  as part of the `get-rotated-secret-value` command.  For example:

```shell
akeyless get-rotated-secret-value -n <Rotated secret name> --host server02.example:22
{
  "value": {
    "username": "ubuntu",
    "password": "2fWpffSgke#M"
  }
}
```

# Rotation Policy

Rotation across multiple hosts will work on a best-effort approach to rotate at least one host from the given hosts' list. After successful rotation across all hosts, the rotation status will be `RotationSucceeded`. Upon a failure in one or more hosts, the rotation status will be `RotationPartialSucceeded`. In case of failure on all hosts, the rotation status will be `RotationFailed`. Each of those results will trigger events in the [Event Center](doc:event-center).

In case of failure on one or more hosts, the Rotated Secret item will keep the old password on the hosts which ended with an error, when working with `rotator type target` the old password will be saved as an old version in the **Parent** Target. 

The Akeyless best practice flow is to generate different passwords for each **Local** user. You can set an identical password for **all** users by using the flag`same-password true`.