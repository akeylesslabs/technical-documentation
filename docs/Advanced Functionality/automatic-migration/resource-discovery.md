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
Akeyless Resource Discovery enables importing and managing all domain and local Users into [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets) in Akeyless Platform, while domain Servers will be imported as [SSH](https://docs.akeyless.io/docs/ssh-target) or [Windows](https://docs.akeyless.io/docs/windows-target) Targets in Akeyless based on the Migration **Target Type** setting.

The discovery process will search for domain users and migrate them as [LDAP Rotated Secrets](https://docs.akeyless.io/docs/create-an-ldap-rotated-secret) for the given [LDAP Target](https://docs.akeyless.io/docs/ldap-target). Such as Active Directory, based on the `User Base DN`, `Domain Name`, and `Privileged Users Groups`.

The [LDAP Target](https://docs.akeyless.io/docs/ldap-target) should contain a **Privilege Domain User** that has permission to perform the following:

- Run LDAP search query

- Change the domain user's password

- Connecting to Windows and Linux domain servers (through NTLM, SSH)

- Installing OpenSSH.Server by way of Windows features, **relevant** only for [SSH Targets](https://docs.akeyless.io/docs/ssh-target).

- Search for local users and change their password

When working with [SSH Target](https://docs.akeyless.io/docs/ssh-target), the migration process will try to install the `OpenSSH.Server` Windows feature on Windows servers where SSH is not installed, for domain servers using WinRM over `https` or `http` using NTLM for authentication over port `5986` or `5985` correspondingly.

<Callout icon="⚠️" theme="warn">
  ### **Warning:**

  Running WinRM over `http` should not be used on production environments.
</Callout>

Note: When using Self Signed Certificate, please mount the matching certificate to the Akeyless Gateway server at `etc/ssl/certs`

<Callout icon="ℹ️" theme="info">
  ### **Active Directory migration compatibility:**

  The OpenSSH server is available as a supported Feature-on-Demand in Windows Server 2022, Windows Server 2019, and Windows 10 (build 1809 and later)
</Callout>

## Set Up Automatic Migration for Active Directory

To create the migration from your Active Directory, log in to your **Gateway Console**, navigate to **Automatic Migration > Active Directory > Add**, and set the following:

- **Name:** A unique name for the migration object.

- **Target:** Select an existing [LDAP Target](https://docs.akeyless.io/docs/ldap-target) in Akeyless, where the `Server type` should be `Active Directory`.

- **Discovery Type**: Set the desired discovery mode. Supported options are **Domain Users**, **Local Users**, **Computers** and **Certificates**.

- **Destination Folder:** Destination folder path inside the Akeyless Platform for the migrated items. Make sure your Gateway has enough permissions to create items under this location. All migrated items, both [Targets](https://docs.akeyless.io/docs/targets) and [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets) of your Domain Servers and domain\local Users will be saved under this folder.

- **Domain Name:** Active Directory Domain Name.

- **User Base DN:** Distinguished Name of User objects to search in Active Directory<br />(For example: `OU=OU_Name`, `CN=Users`, `DC=example`, `DC=com` or `OU=User_Name,DC=example,DC=com`).

- **Domain User Name Template:** A template for the created items, where the imported Domain Users will be saved as Rotated Secrets inside the Akeyless Platform, for example, `/DomainUsers/{{USERNAME}}`. This path includes the prefix of the Destination Folder. `{{USERNAME}}` (the user's `sAMAccountName`) is always required in this template. The template can also include additional placeholders mapped to other AD attributes, such as `{{OWNER}}`, to organize Domain Users by ownership or any other attribute instead of only by OU. See [Domain User Path Template Attributes](#domain-user-path-template-attributes) below.

- **Domain User Path Attributes:** An optional, comma-separated list of `PLACEHOLDER=ldap_attribute` pairs that map every placeholder used in the **Domain User Name Template** (other than `{{USERNAME}}`) to the LDAP attribute whose value should fill it in, for example, `OWNER=managedBy`. See [Domain User Path Template Attributes](#domain-user-path-template-attributes) below.

- **Search in Privileged Users Groups:** Comma-separated list of domain groups from which privileged domain users will be migrated.

- **Discover Services:** Discover any Windows service that runs with explicit user credentials, as part of the rotated secret those services will be reflected, and upon Rotation, the relevant services will be restarted with the latest password.

- **Discover Local Users:** Enable/Disable discover local users from each domain server and migrate them as SSH Rotated Secrets. Default is false - Only domain users will be migrated.

- **Discover IIS Applications:** Discover any existing IIS Application that runs with explicit user credentials, as part of the rotated secret those IIS Application will be reflected, and upon Rotation, the relevant IIS Application will be restarted with the latest password.

- **AI Certificate Discovery:** Discover existing certificates across the environment using an AI-driven scanner as part of Active Directory Migration.

- **Automatic Sync:** Enable/Disable a recurring sync of this Active Directory Discovery migration, so that new domain or local accounts are picked up automatically, without having to manually trigger a sync. When enabled, set the sync interval in days, or switch to Cron mode to define the schedule with standard cron syntax (the two modes stay in sync, for example, an interval of 90 days shows as the equivalent expression in Cron mode, and the other way around). Default is Disabled.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  Discover Local Users might require further installations of SSH on the servers, based on the supplied Computer Base DN. This will be done automatically by the migration process
</Callout>

- **Computer Base DN:** Distinguished Name of Computer (server) objects to search in Active Directory, for example, `CN=Computers`, `DC=example`, `DC=com`.

- **Target Name Template:** A template for the created items, where the imported Domain Servers will be saved as [SSH Targets](https://docs.akeyless.io/docs/ssh-target) inside the Akeyless Platform, for example, `/Servers/{{COMPUTER_NAME}}`. This path includes the prefix of the Destination Folder.

- **Local User Name Template:** A template for the created items, where the imported Local Users will be saved as Rotated Secrets ) inside the Akeyless Platform, for example, `/LocalUsers/{{COMPUTER_NAME}}/{{USERNAME}}`. This path includes the prefix of the Destination Folder.

- **Ignore the Following Local Users:** Comma-separated list of Local Usernames to exclude while migrating.

- **Custom Password Policy:&#x20;**&#x53;et a custom password policy that will apply to the users.&#x20;

- **Target Type:** Set the Target type of the domain servers, which could be **SSH** or a **Windows** target.

- **SSH Port:** For **Target Type** of SSH, Set the default SSH Port for connecting to the Domain Servers, default `22`.

- **WinRM Port:** For **Target Type** of Windows, Set the default WinRM Port for connecting to the Domain Servers default `5986`. Note, WinRM, by default, works over `https`.

- **Enable SRA:** Enable/Disable RDP Secure Remote Access setup for the migrated local users by way of the Rotated Secrets. Default is Disabled, the Rotated Secrets will not be created with SRA configuration. **Available only for accounts with the SRA package** .

- **Skip dry-run validation:** Skip dry-run validation when creating rotated secrets for migrated Domain/Local Users.

- **Custom Password Policy:&#x20;**&#x41;pply a custom password policy when generating passwords for migrated Domain/Local Users.

- **Target Format:** Relevant only for **Computers Discovery Type**, the output Target format to migrate all discovered computers supporting [Linked Target](https://docs.akeyless.io/docs/linked-target) for Secure Remote Access.

- **Computers Grouping:** Relevant only for **Computers Discovery Type** when **Target Format** is `linked`. Controls how discovered computers are grouped into linked targets. See [Grouping Discovered Computers](#grouping-discovered-computers) below.

- **Auto Rotate:** Enable/Disable automatic/recurrent rotation for the migrated secrets. Default is Disabled. Only manual rotation is allowed for migrated secrets. If Enabled, this should be set with rotation-interval and rotation-hour settings.

## Domain User Path Template Attributes

By default, the **Domain User Name Template** only supports `{{USERNAME}}`, filled from `sAMAccountName`. You can extend the template with additional placeholders mapped to other AD attributes using **Domain User Path Attributes** (`--ad-domain-users-path-attributes` on the CLI), so Domain Users can be organized by ownership, a custom attribute, or any other single-value AD attribute, instead of only by OU.

For example, to organize Domain Users by their configured owner:

```
ad-domain-users-path-template: /Active Directory/Domain Users/{{OWNER}}/{{USERNAME}}
ad-domain-users-path-attributes: OWNER=managedBy
```

Here, `{{OWNER}}` is a placeholder, and `OWNER=managedBy` maps it to the `managedBy` LDAP attribute. Akeyless requests that attribute as part of the LDAP search for Domain Users and uses its value to fill `{{OWNER}}` in the rendered path.

Keep the following in mind when using this setting:

- `{{USERNAME}}` is always required in the **Domain User Name Template** and always resolves to `sAMAccountName`. It cannot be remapped.
- Every other placeholder used in the **Domain User Name Template** must have a matching entry in **Domain User Path Attributes**. A placeholder with no mapping is left as literal text by the path renderer, which would put every Domain User in a single folder named after the unmapped placeholder, so this configuration is rejected at validation time.
- The rendered path is the identity of the migrated item: on the next discovery run, Akeyless finds the existing Rotated Secret at that path and updates it, rather than creating a duplicate. Because of this, an empty attribute value is placed under a fixed `unassigned` folder instead of an empty path segment, since an empty segment would change the item's path and the next run would no longer find the existing item there.
- `managedBy`, and any other mapped attribute that returns a Distinguished Name (DN), is reduced to its CN, with `}}`, `{{`, `:`, and spaces stripped, the same cleanup already used for certificate names. A raw DN is not a usable folder name.
- If a mapped attribute's value changes for a user (for example, their owner changes), the rendered path changes, and the next discovery creates a new item at the new path. The importer does not move an existing Rotated Secret when its source path changes; this matches the current rediscovery behavior.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  Group membership (`memberOf`) cannot be mapped through **Domain User Path Attributes**, because a user can belong to multiple groups while Resource Discovery keeps a single item per Domain User. Mapping a multi-value attribute like `memberOf` into the template would create duplicate items for the same user. To group by domain group instead, configure an ordered list of groups so that a single `{{GROUP}}` placeholder resolves to the first group in that list that the user belongs to.
</Callout>

Computer targets, Local Users, and Certificates path templates are unaffected by this setting. Their placeholders continue to be filled from the host or the certificate rather than from a Domain User LDAP attribute:

| Resource | Template | Placeholders that are filled |
| --- | --- | --- |
| Domain Users | Domain User Name Template | `{{USERNAME}}` (`sAMAccountName`, required), plus any placeholder mapped in Domain User Path Attributes |
| Computer targets | Target Name Template | `{{COMPUTER_NAME}}` (DNS hostname) |
| Local Users | Local User Name Template | `{{COMPUTER_NAME}}`, `{{USERNAME}}` |
| Certificates | Certificates Path Template | `{{COMMON_NAME}}` (required), also `{{COMPUTER_NAME}}` and `{{MIGRATION_NAME}}` |

## Grouping Discovered Computers

When **Discovery Type** includes **Computers** and **Target Format** is `linked`, the **Computers Grouping** setting controls how discovered computers are grouped into [Linked Targets](https://docs.akeyless.io/docs/linked-target):

| Value | Result |
| --- | --- |
| `flat` (default) | All discovered computers go into a single pile, split into linked targets of at most 1,000 hosts each, named using the Target Name Template with a `-1`, `-2`, etc. suffix. |
| `ou` | Computers are grouped by their parent Organizational Unit (OU), taken from each computer's Distinguished Name, with one linked-target series created per OU that actually contains computers. |

With `ou` grouping, a computer in `OU=Payroll,OU=Finance` is grouped under `Finance/Payroll`. It does not roll up into the parent `Finance` OU, so nested OUs stay separate. Computers that sit directly under the configured **Computer Base DN**, with no intermediate OU, are grouped together under that base.

Within each OU group, the existing 1,000-host split used for `flat` grouping still applies: the target name uses the **Target Name Template**, followed by the OU path, and a numeric suffix when that OU needs more than one target. Rediscovery matches targets by this same name, so a later run that finds the same OU updates that target's host list in place instead of creating a duplicate.

<Callout icon="⚠️" theme="warn">
  ### **Note:**

  Switching **Computers Grouping** from `flat` to `ou` on an existing migration creates the new per-OU targets but does not delete the previous flat targets. Resource Discovery does not remove a linked target it no longer produces, so clean up the old targets manually if they are no longer needed.
</Callout>