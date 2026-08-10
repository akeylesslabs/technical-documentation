---
title: Aerospike Target
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define an [Aerospike](https://aerospike.com/) target to be used with Database [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) and [Rotated](https://docs.akeyless.io/docs/rotated-secrets) Secrets.

# Create an Aerospike Target with the CLI&#x20;

To create an Aerospike target with the CLI, run the following command:

```shell
akeyless target create db \
--name <Target name> \
--db-type aerospike \
--host <Aerospike host> \
--port <Aerospike port> \
--user-name <Aerospike user name> \
--pwd <Aerospike password> \
--db-name <Aerospike namespace> 
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash / separators. If the folder does not exist, it will be created together with the target.
- `db-type`: Required, set to aerospike.
- `host`: The hostname or IP address of the Aerospike seed node.
- `port`: The port of the Aerospike service (default 3000).
- `user-name`: A privileged Aerospike user name with sufficient rights to create and manage users.
- `pwd`: The password of the privileged Aerospike user.
- `db-name`: The target Aerospike namespace.

  
You can find the complete list of parameters for this command in the CLI Reference - Akeyless Targets section.<br />
