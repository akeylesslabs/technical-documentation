---
title: Release Notes
deprecated: false
hidden: false
link:
  new_tab: true
  url: https://updates.akeyless.io/
metadata:
  robots: index
---

## Release Highlights (2026-04-29)

The latest product release details are published at [Akeyless Product Updates](https://updates.akeyless.io/).

### Gateway 4.50.0

#### Features

* Targets: Added mTLS support for PostgreSQL and MySQL targets ([ASM-17758](https://akeyless.atlassian.net/browse/ASM-17758))
* Usage Reports: Added contract start and renewal indication ([ASM-14436](https://akeyless.atlassian.net/browse/ASM-14436))
* RBAC: Added wildcard support for Gateway allowed access permissions ([ASM-17656](https://akeyless.atlassian.net/browse/ASM-17656), [PRM-1574](https://akeyless.atlassian.net/browse/PRM-1574))
* UX/UI: Added multi-line support for key/value pairs ([ASM-17820](https://akeyless.atlassian.net/browse/ASM-17820), [PRM-1738](https://akeyless.atlassian.net/browse/PRM-1738))

#### Bug Fixes

* Automatic Migration: Fixed an issue where secret metadata was not updated during re-sync ([ASM-17845](https://akeyless.atlassian.net/browse/ASM-17845))
* Multi-Vault Governance: Improved Azure USC pagination in the UI ([ASM-17976](https://akeyless.atlassian.net/browse/ASM-17976))
* Targets: Fixed an issue with server certificate verification for PostgreSQL, Amazon Redshift, and MySQL targets ([ASM-13718](https://akeyless.atlassian.net/browse/ASM-13718))

### CLI 1.143.0

#### Features

* Targets: Added mTLS support for PostgreSQL and MySQL targets ([ASM-17758](https://akeyless.atlassian.net/browse/ASM-17758))
* RBAC: Added wildcard support for Gateway allowed access permissions ([ASM-17656](https://akeyless.atlassian.net/browse/ASM-17656), [PRM-1574](https://akeyless.atlassian.net/browse/PRM-1574))
