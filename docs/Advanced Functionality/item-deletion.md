---
title: Item Deletion
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
# Introduction

Item deletion is pretty similar, using the same command formats, with a default of immediate deletion. Items can be set for a scheduled deletion instead.\
Some types of items or deletion flows have special rules for their deletion:

* If the item is an `AES` or `RSA` key, By default, there will be a waiting period of 7 days before deleting the item with all its versions. This can be adjusted.

* If the item is a key that encrypts a different item in the system (Static Secret, Dynamic Secret, Certificate Issuer, etc.), it cannot be deleted until items that are encrypted with it are also deleted.

* If you have a key that is pending deletion but has not yet been deleted, you may cancel this deletion with the [Set Item State](https://docs.akeyless.io/docs/cli-reference-encryption-keys#p-stylecolorblueset-item-statep) command.

* You may replace the `delete-item` command with `delete-items` to delete all items in a specific path, or to delete multiple items explicitly, however, this only supports immediate deletion.

* [Targets](https://docs.akeyless.io/docs/cli-reference-akeyless-targets#p-stylecolorbluedelete-targetp) and [Event Forwarders](https://docs.akeyless.io/docs/cli-reference#p-stylecolorbluedelete-event-forwarderp) are deleted with a separate command, and not with the standard `delete-item` / `delete-items`

# Deleting an Item in the CLI

When deleting an item from the CLI, there are two main things to consider, which item to delete and when.

Which:

* If you are deleting a single item, use the parameter `-n` and insert the name of the item you wish to delete.

* If you are deleting multiple items, use the parameter `-p` and insert the path to the items you wish to delete.

When:\
Scheduling a future deletion can only be done for **single key deletion**.\
The relevant parameters are:

* `version`: Delete a specific version of the item (i.e - after a rotate-key operation, cannot be the last item version)

* `delete-in-days`: The number of days to wait before deleting the item, default 7  for keys. To delete a key immediately use the value `delete-in-days=-1`.

* `delete-immediately`: When trying to delete a key immediately with `delete-in-days=-1`, this flag must be supplied as well

## Usage Examples

Example 1 - Deleting key1:

```shell
date
Wed Jan 1 10:00:00 IDT 2020

akeyless delete-item -n key1
--output--
Item key1 set to be deleted on 2020-01-07 08:00:00 +0000 UTC
```

Example 2 - Deleting key1 with non-default values:

```shell
date
Wed Jan 1 10:05:00 IDT 2020

akeyless delete-item -n key1 --delete-in-days=30
--output--
Item key1 set to be deleted on 2020-01-30 08:05:00 +0000 UTC
```

Example 3 - Deleting key1 immediately without waiting:

```shell
date
Wed Jan 1 10:10:00 IDT 2020

akeyless delete-item -n key1 --delete-in-days=-1 --delete-immediately
--output--
Item key1 was successfully deleted
```

Example 4 - Deleting key1 first version after a rotate-key operation:

```shell
date
Wed Jan 1 10:10:00 IDT 2020

akeyless delete-item -n key1 --version=1 --delete-in-days=30
--output--
Item key1 version 1 set to be deleted on 2020-01-30 08:10:00 +0000 UTC
```

Example 5 - Deleting multiple items: 

```shell
# Delete an entire folder 

akelyess delete-items --path /Path/To/Folder

# Explicitly deleting multiple items 

akeyless delete-items --item /Path/To/ItemA --item /Path/To/ItemB --item /Different/Path/ItemC
```

# Deleting an Item in the Console

1. Go to the containing folder and select the item you want to delete.

2. Select the trash bin icon on the top right corner of the item details.

3. Type in the item name for verification.

4. **For keys only**, Select if you wish to delete the key immediately or within a specific number of days.

5. Select **Delete \{item type}**.
