---
title: Secret and Target Locking
deprecated: false
hidden: false
metadata:
  robots: index
---
Locking [Static Secrets](https://docs.akeyless.io/docs/static-secrets), [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets), and [Targets](https://docs.akeyless.io/docs/targets) is available to users who have List and Update permissions for the item.

When an item is locked, only the user who locked it or a user with an **Admin** role can access it. Admins can also remove the lock.

You can choose whether the lock applies to **reading** the item or **updating** it.

If an item is locked for **reading**, users with read permission will still be able to see the item, but they will not be able to view the secret value.

# Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) version `4.48.0` or later.
* Only users with `list` and `update` permissions will be able to lock secrets.

# Locking and item using the CLI

In order to lock an item using the CLI, run the following command:

```shell
akeyless lock-item | lock target \ 
--name <The item|target name> \
--actions <[update]/[read]> \
--lock-ttl 60 
```

Where:

* `-n, name`: **Required**. The name of the object to lock.
* `--actions`: **Required**. Defines whether the item is locked for **reading** its value or **updating** its value.
* `--lock-ttl`: **Optional**. Sets a TTL for the lock.

You can find the complete list of parameters for this command in the CLI Reference.

# Locking and item using the Akeyless Console

In order to lock an item using the Akeyless console, run the following steps:

1. Log in to the Akeyless Console, and navigate to the item you wish to lock.
2. Open the action menu and click - **Lock Secret | Target**.
3. Choose if to lock the item for **Read** or **Update**.
4. Set a TTL for the lock (Optional).
5. Press **Lock Now**

<br />

<br />
