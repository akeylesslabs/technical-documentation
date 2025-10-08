---
title: Update and Version Static Secrets
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
When updating a static secret, you can update the current version, create a new version, or roll back to the previous version of a secret (for example, if the most recent version was configured incorrectly).

Let’s update a static secret using the Akeyless CLI. If you’d prefer, see how to do this from the [Akeyless Console](doc:oc:staticversions#updates-and-versions-from-the-ui) instead.

## Update a Static Secret from the CLI

The CLI command to update a static secret is:

```shell Shell
> akeyless update-secret-val --name <secret name> --value <new secret value>

The value of secret <secret name>  was successfully updated
```

```shell
```

When you update a static secret, by default the latest version is updated. To keep the previous version of the secret stored in Akeyless, run the `--keep-prev-version=true`option.

> 🚧 Warning
>
> **Metadata changes**
>
> Changing the metadata of a secret does not change its version. To change the version and store the previous version, you must explicitly run `--keep-prev-version=true`.

The rest of this section shows examples of how to manage secret versions directly from your CLI with different examples based on the assumption you've already created a secret called `/secret1` with `value1`.

Examples are as follows:

* Create a new version of **secret1** with the new value **value2** and keep previous version
* Getting a secret value always returns the current value.
* Get a specific version of the secret value
* Delete a specific version of the secret value
* Roll back to a previous secret version

### Create a new version of _secret1_ with the new value _value2_ and keep previous version:

```shell retrieve-and-view-from-the-ui
$ akeyless update-secret-val -n /secret1 -v value2 --keep-prev-version=true
The value of secret /secret1 was successfully updated
...
$ akeyless describe-item -n /secret1 --show-versions
{
   "item_name": "/secret1",
   "item_type": "STATIC_SECRET",
   ...
   "last_version": 2,
   ...
   "item_versions": [
      {
         "version": 1,
         "creation_date": "2020-01-30T13:00:00Z"
      },
      {
         "version": 2,
         "creation_date": "2020-01-30T14:00:00Z"
      }
   ],
   ...
}
```

### Get a secret value always returns the current value:

```shell
$ akeyless get-secret-value -n /secret1
value2
```

### Get a specific version of the secret value:

```shell
$ akeyless get-secret-value -n /secret1 --version 1
value1
```

### Get the last N versions of the secret value:

To get the last **N** versions of a secret values, use `--version=-N`, where `-N` represents the last versions you wish to retrieve, supporting up to the last 20 versions of the secret.

```shell
$ akeyless get-secret-value -n /secret1  --version=-4
{
"1": "value1",
"2": "value2",
"3": "value3",
"4": "value4"
}
```

### Delete a specific version of the secret value:

```shell
$ akeyless delete-item -n /secret1 --version 1
Item /secret1 version 1 was successfully deleted
...
$ akeyless describe-item -n /secret1 --show-versions
{
   "item_name": "/secret1",
   "item_type": "STATIC_SECRET",
   ...
   "last_version": 2,
   ...
   "item_versions": [
      {
         "version": 2,
         "creation_date": "2020-01-30T14:00:00Z"
      }
   ],
   ...
}
```

### Roll back to a previous secret version:

```shell
$ akeyless update-secret-val -n /secret1 -v value3 --keep-prev-version=true
The value of secret /secret1 was successfully updated

$ akeyless get-secret-value -n /secret1
value3

$ akeyless rollback-secret -n /secret1 --old-version 2
Secret /secret1 was successfully rolled back to version 2

$ akeyless describe-item -n /secret1 --show-versions
{
   "item_name": "/secret1",
   "item_type": "STATIC_SECRET",
   ...
   "last_version": 4,
   ...
   "item_versions": [
      {
         "version": 2,
         "creation_date": "2020-01-30T14:00:00Z"
      },
      {
         "version": 3,
         "creation_date": "2020-01-30T15:00:00Z"
      },
      {
         "version": 4,
         "creation_date": "2020-01-30T16:00:00Z"
      }
   ],
   ...
}

$ akeyless get-secret-value -n /secret1
value2
```

## Updates and versions from the UI

From the UI, click the pencil icon next to the **Value** of the secret and toggle **Create new version** to update the value and create a new version of the secret.

Once a secret has more than one version, a list of all previous values is available within the secret at the **Versions** tab.

From the version history, click the eye icon next to a specific version to open a pop-up and view its value.

To delete a specific secret version from that same list, click the **Delete** icon and then confirm the deletion.

To restore a specific secret version, from the list of secret versions, click the **Restore** icon to open a pop-up and confirm. This rolls the selected version back, overriding the current version.

## Change Event

To get an event when a static secret value is changed, click on the action menu (top right corner)on the item itself, and turn on the **Change Event**.  Any time the secret value is changed it will trigger an [Event](doc:event-center).
