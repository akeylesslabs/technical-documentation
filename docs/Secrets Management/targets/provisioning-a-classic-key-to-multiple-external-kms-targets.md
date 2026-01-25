---
title: Multi-Target Classic Key Provisioning
deprecated: false
hidden: false
metadata:
  robots: index
---
### Overview


This feature allows a single Akeyless Classic Key to be provisioned and managed centrally while being simultaneously mapped to multiple external Key Management Systems (KMS) or secure storage services across different cloud environments.

<br />

### Prerequisites

Before provisioning a Classic Key to multiple targets, ensure the following:

* A Classic Key already exists in Akeyless  
* External KMS targets (AWS, Azure, GCP, Thales, etc.) are configured under Targets
* You have sufficient permissions to provision keys to external targets

<br />

In the Provisioning tab, you can view:

* The Classic Key details
* All external targets currently attached to this key
* The external key name used in each target  

<br />
