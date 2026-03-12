---
title: Multi-Target Classic Key Provisioning
deprecated: false
hidden: false
metadata:
  robots: index
---
## Overview

This feature allows a single Akeyless Classic Key to be provisioned and managed centrally while being simultaneously mapped to multiple external KMS across different cloud environments.

Each attached target can use its own external key name and target-specific settings while continuing to reference the same Classic Key in Akeyless.

> ℹ️ **Note:**
>
> If the account does not include the required Multi-Cloud KMS entitlement, attaching additional external KMS targets can fail.

## Provisioning with the CLI

Multi-target provisioning workflow can also be performed using the Akeyless CLI. Using the CLI, a single Classic Key can be associated with multiple external targets by repeating the target association step.

### Step 1: Create a Classic Key

```shell
akeyless create-classic-key \
  --name my-shared-key \
  --alg AES256GCM
```

### Step 2: Create External Targets

AWS KMS Target

```shell
akeyless target create aws \
  --name aws-kms-target \
  --access-key-id <ACCESS_KEY_ID> \
  --access-key <ACCESS_KEY>
```

Azure Key Vault Target

```shell
akeyless target create azure \
  --name azure-kv-target \
  --tenant-id <TENANT_ID> \
  --client-id <CLIENT_ID> \
  --client-secret <CLIENT_SECRET> \
  --vault-name <KEY_VAULT_NAME>
```

GCP KMS Target

```shell
akeyless target create gcp \
  --name gcp-kms-target \
  --project-id <GCP_PROJECT_ID> \
  --location <LOCATION> \
  --key-ring <KEY_RING> \
  --service-account-key <SERVICE_ACCOUNT_JSON>
```

### Step 3: Associate the Same Classic Key with Each Target

```shell
akeyless assoc-target-item \
  --name my-shared-key \
  --target-name aws-kms-target

akeyless assoc-target-item \
  --name my-shared-key \
  --target-name azure-kv-target

akeyless assoc-target-item \
  --name my-shared-key \
  --target-name gcp-kms-target
```

Repeat this step for each additional external KMS target that should use the same Classic Key.

## Provisioning with the Web Console

### Step 1: Create or Select a Classic Key

1. In the Akeyless Console, navigate to **Items**.
2. Create a new Classic Key or select an existing one.
3. Open the key to view its details.

### Step 2: Open the Provisioning Tab

1. Inside the Classic Key view, navigate to the **Provisioning** tab.
2. This tab displays all external targets currently attached to the key.

### Step 3: Attach an External Target

1. Click **Attach**.
2. Enter the **External Key Name**. This is the key name that will be created in the external KMS.
3. Select the target.
4. Complete the target-specific provisioning fields. For example, Azure targets require **Operations**. GCP targets can require values such as **Purpose**, **Algorithm**, and **Protection level**. AWS targets can require region-specific settings, depending on the selected target configuration.

5. Save the configuration.

Each target can use a different external key name if needed.

### Step 4: Verify the Provisioned Target

1. After saving, return to the **Provisioning** tab.
2. Confirm that the new target appears in the targets list.
3. Verify the **External Key Name**, **Target type**, and **Target path**.

### Step 5: Repeat for Additional Targets

To provision the same Classic Key to another external system:

1. Click **Attach** again.
2. Select a different target (for example, AWS, Azure, GCP, or Thales).
3. Provide a new **External Key Name** if needed.
4. Complete any target-specific provisioning fields.
5. Save the configuration.

You can repeat this process multiple times, each time adding another external target while continuing to manage a single Classic Key in Akeyless.

## Considerations

* Provisioning fields vary by target type.
* The same Classic Key can be attached to multiple external KMS targets.
* Each target attachment can use a different external key name.
* If an entitlement or target-specific validation check fails, Akeyless does not create the new target association.
