---
title: Advanced Path Templates for Resource Discovery
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
By default, [Active Directory Resource Discovery](https://docs.akeyless.io/docs/resource-discovery) organizes migrated domain users and computers using a fixed set of placeholders, such as `{{USERNAME}}` and `{{COMPUTER_NAME}}`. This page describes two additional ways to customize how discovered items are organized: mapping extra placeholders in the **Domain User Name Template** to LDAP attributes, and grouping discovered computers by organizational unit (OU).

## Domain User Attribute Placeholders

The **Domain User Name Template** supports `{{USERNAME}}` (mapped to `sAMAccountName`) out of the box. You can add further placeholders mapped to any single-value LDAP attribute of the domain user, for example `managedBy` or a custom attribute, so discovered accounts can be organized by ownership or another attribute instead of only by OU.

To use an attribute placeholder:

- Add the placeholder to the **Domain User Name Template**, for example: `/Active Directory/Domain Users/{{OWNER}}/{{USERNAME}}`.

- Map the placeholder to an LDAP attribute using the **Domain User Path Attributes** setting (CLI: `--ad-domain-users-path-attributes`), for example: `OWNER=managedBy`.

Notes:

- `{{USERNAME}}` is always required in the template and always maps to `sAMAccountName`. It does not need to be added to **Domain User Path Attributes**.

- Every other placeholder used in the template must be mapped in **Domain User Path Attributes**. An unmapped placeholder is left as literal text, which would put every discovered user into a single folder named after the placeholder, so the migration is rejected at validation time instead.

- If the mapped attribute has no value for a given user, Akeyless uses `unassigned` for that path segment, rather than leaving it empty, since an empty segment would change the item's identity and cause the next discovery run to miss the existing item.

- `managedBy`, and other attributes whose value is a Distinguished Name (DN), are resolved to their Common Name (CN), with `{{`, `}}`, `:`, and spaces stripped, the same way certificate names are cleaned up.

- Group membership (`memberOf`) cannot be used as an attribute placeholder, because a user can belong to multiple groups while discovery keeps one item per user. Mapping a multi-value attribute this way would create duplicate accounts.

<Callout icon="⚠️" theme="warn">
  ### Rediscovery behavior

  The rendered path is the item's identity. If a mapped attribute's value changes for a user, the rendered path changes, and the next discovery run creates a new item at the new path instead of moving the existing one.
</Callout>

## Grouping Discovered Computers by OU

When **Discovery Type** is **Computers** and **Target Format** is **Linked**, the **Computers Grouping** setting controls how discovered computers are split into linked targets:

- **Flat (default):** All discovered computers are grouped into a single series of linked targets, split into targets of up to 1,000 hosts each, named using the **Target Name Template** suffixed with `-1`, `-2`, and so on, the same as today.

- **By OU:** Computers are grouped by their parent organizational unit, taken from each computer's Distinguished Name (DN), and every OU that contains computers gets its own series of linked targets, again split into targets of up to 1,000 hosts. For example, a computer in `OU=Payroll,OU=Finance` is grouped under `Finance/Payroll`; nested OUs are kept separate and are not rolled up into their parent. Computers located directly under **Computer Base DN** are grouped together.

<Callout icon="ℹ️" theme="info">
  ### Note

  Switching an existing migration from **Flat** to **By OU** creates the new per-OU linked targets but does not remove the previous flat targets, since discovery does not delete a linked target it no longer produces.
</Callout>