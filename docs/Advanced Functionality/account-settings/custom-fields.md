---
title: Custom Fields
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Custom Fields allow you to enforce structured metadata on Akeyless objects such as **Secrets**, **Keys**, and **Certificates**. These fields help align your secrets and keys management with organizational policies.

For example:

* Every Secret may require an `Owner` field.
* Keys can optionally include a `Managed By` field.

Administrators can define which fields are available for each object type in Akeyless and whether those fields are required or optional.

<Callout icon="📘" theme="info">
  _**Note:** Currently Custom Fields supports only **Items**._
</Callout>

# Manage Custom Field

## Create a custom field

Run the following CLI command to create a new custom field in the account:

```shell
akeyless custom-field create \
--object=`[items]` \
--object-type static-secret \
--required=`[false]`
```

Where:

`object`: The object to create the custom field

`object-type`: The object type to create the custom field, e.g., `static-secret`, `rotated-secret`, `encryption-keys`, etc.

`required=[false]`: Mark the custom field, as required or optional.

Once a custom field is created, it applies to all new objects of the selected type. If an existing object is updated, the defined custom field rules will also apply.

## Delete a custom field

Delete a custom field from the account:

```shell
akeyless custom-field delete --id <custom field ID>
```

## Update a custom field

Updates an existing custom field in the account:

```shell
akeyless custom-field update \
--id <custom field ID> \
--name <new name> \
--required=`[false]`
```

## Fetch a custom field

Retrieves a custom field:

```shell
akeyless custom-field get --id <custom field ID>
```

Retrieves a list of all custom fields in the account:

```shell
akeyless custom-field list --object items --object-type static-secret
```

# Manage Custom Field from Console

To manage custom fields in the account, navigate to your **Account Settings -> Custom Fields**, click **Add**

1. Provide the new custom field name
2. Choose the Object type in Akeyless to which this custom field will be attached. For example, **Items->Static Secret**
3. Select if this new custom field will be mandatory or not.

Once a custom field is created, it applies to all new objects of the selected type. If an existing object is updated, the defined custom field rules will also apply.
