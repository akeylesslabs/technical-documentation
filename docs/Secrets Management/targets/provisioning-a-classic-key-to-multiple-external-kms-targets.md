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

#### Step 1: Create or Select a Classic Key

1. In the Akeyless Console, navigate to Items
2. Create a new Classic Key or select an existing one
3. Open the key to view its details

<br />

#### Step 2: Open the Provisioning Tab

1. Inside the Classic Key view, navigate to the Provisioning tab
2. This tab displays all external targets currently attached to the key

<br />

#### Step 3: Attach an External Target

1. Click Attach
2. Enter the External Key Name

* This is the key name that will be created in the external KMS
* Each target may use a different external key name if required

3. Select the target (for example, an AWS KMS target)
4. Choose the provisioning mode:

* Single Region
* Multi-Region (if supported by the target)

5. Click Save

<br />

#### Step 4: Verify the Provisioned Target

1. After saving, return to the Provisioning tab
2. Confirm that the new target appears in the targets list
3. Verify:

* External Key Name
* Target type
* Target path

<br />

#### Step 5: Repeat for Additional Targets

To provision the same Classic Key to another external system:

1. Click Attach again
2. Select a different target (AWS, Azure, GCP, Thales, etc.)
3. Provide a new External Key Name if needed
4. Save the configuration

You can repeat this process multiple times, each time adding another external target while continuing to manage a single Classic Key in Akeyless.
