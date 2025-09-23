---
title: Resource Discovery
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
Akeyless Resource Discovery enables importing and managing all domain and local Users into [Rotated Secrets](doc:rotated-secrets) in Akeyless Platform, while domain Servers will be imported as [SSH](doc:ssh-target) or [Windows](doc:windows-target) Targets in Akeyless based on the Migration **Target Type** setting.

The discovery process will search for domain Users and migrate them as [LDAP Rotated Secret](doc:create-an-ldap-rotated-secret), from the given [LDAP Target](doc:ldap-target), i.e., Active Directory, based on the `User Base DN`, `Domain Name`, and  `Privileged Users Groups`.

The [LDAP Target](doc:ldap-target) should contain a **Privilege Domain User** that has permission to perform the following:

- Run LDAP search query

- Change the domain user's password

- Connecting to Windows and Linux domain servers (through NTLM, SSH)

- Installing OpenSSH.Server via Windows features, **relevant** only for [SSH Targets](doc:ssh-target).

- Search for local users and change their password 

When working with [SSH Target](doc:ssh-target), the migration process will try to install the `OpenSSH.Server` windows feature on Windows servers where SSH is not installed, for domain servers using WinRM over `https`or `http` using NTLM for authentication over port `5986` or `5985` correspondingly. 

> 🚧 Warning
> 
> Running WinRM over `http` should not be used on production environments.

Note: When using Self Signed Certificate, please mount the matching certificate to the Akeyless Gateway server at `etc/ssl/certs` 

> 📘 Note
> 
> **Active Directory migration compatibility**  
> The OpenSSH server is available as a supported Feature-on-Demand in Windows Server 2022, Windows Server 2019, and Windows 10 (build 1809 and later)

# Set Up Automatic Migration for Active Directory

To create the migration from your Active Directory, login to your Gateway on port `8000`, navigate to the **Automatic Migration -> Active Directory -> Add**, and set the following:

- **Name:** A unique name for the migration object. 

- **Target:** Select an existing [LDAP Target](doc:ldap-target) in Akeyless, where the `Server type` should be `Active Directory`.

- **Discovery Type** : Set the desired discovery mode. Supported options are **Domain Users**, **Local Users**, and **Computers**. 

- **Destination Folder:** Destination folder path inside the Akeyless Platform for the migrated items. Make sure your Gateway has enough permissions to create items under this location. All migrated items, both [Targets ](https://docs.akeyless.io/docs/targets)and [Rotated Secrets](doc:rotated-secrets) of your Domain Servers and domain\\local Users will be saved under this folder.

- **Domain Name:** Active Directory Domain Name.

- **User Base DN:** Distinguished Name of User objects to search in Active Directory  
  (e.g: `OU=OU_Name`, `CN=Users`,`DC=example`,`DC=com`or `OU=User_Name,DC=example,DC=com`).

- **Domain User Name Template:** A template for the created items, where the imported Domain Users will be saved as Rotated Secrets inside the Akeyless Platform, e.g: `/DomainUsers/{{USERNAME}}`. This path includes the prefix of the Destination Folder. 

- **Search in Privileged Users Groups:** Comma-separated list of domain groups from which privileged domain users will be migrated.

- **Discover Services:** Discover any Windows service that runs with explicit user credentials, as part of the rotated secret those services will be reflected, and upon Rotation, the relevant services will be restarted with the latest password. 

- **Discover Local Users:** Enable/Disable discover local users from each domain server and migrate them as SSH Rotated Secrets. Default is false - Only domain users will be migrated. 

> 👍 Note
> 
> Discover Local Users might require further installations of SSH on the servers, based on the supplied Computer Base DN. This will be done automatically by the migration process

- **Computer Base DN:** Distinguished Name of Computer (server) objects to search in Active Directory, e.g. `CN=Computers`,`DC=example`,`DC=com`.

- **Target Name Template:** A template for the created items, where the imported Domain Servers will be saved as [SSH Targets](doc:ssh-target) inside the Akeyless Platform, i.e: `/Servers/{{COMPUTER_NAME}}`. This path includes the prefix of the Destination Folder.

- **Local User Name Template:** A template for the created items, where the imported Local Users will be saved as Rotated Secrets ) inside the Akeyless Platform, i.e: `/LocalUsers/{{COMPUTER_NAME}}/{{USERNAME}}`,  This path includes the prefix of the Destination Folder.

- **Ignore the Following Local Users:** Comma-separated list of Local Usernames to exclude while migrating.

- **Target Type:** Set the Target type of the domain servers, which could be **SSH** or a **Windows** target.

- **SSH Port:** For **Target Type** of SSH, Set the default SSH Port for connecting to the Domain Servers, default `22`.

- **WinRM Port:** For **Target Type** of Windows, Set the default WinRM Port for connecting to the Domain Servers default `5986`. Note, WinRM, by default, works over `https`.

- **Enable SRA:** Enable/Disable RDP Secure Remote Access setup for the migrated local users via the Rotated Secrets. Default is Disabled, the Rotated Secrets will not be created with SRA configuration. **Available only for accounts with the SRA package **.

- **Target Format:** Relevant only for  **Computers Discovery Type**, the output Target format to migrate all discovered computers supporting [Linked Target](doc:linked-target)  for Secure Remote Access. 

- **Auto Rotate:** Enable/Disable automatic/recurrent rotation for the migrated secrets. Default is Disabled. Only manual rotation is allowed for migrated secrets. If Enabled, this should be set with rotation-interval and rotation-hour settings.