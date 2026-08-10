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

You can find the complete list of parameters for this command in the CLI Reference - Akeyless Targets section.

# Create an Aerospike Target in the Console&#x20;

1. Log in to the Akeyless Console, and go to **Targets** > **New** > **Database** **(Aerospike)**.
2. Define a **Name** of the target, and specify the Location as a path to the virtual folder where you want to create the new target, using slash / separators. If the folder does not exist, it will be created together with the target.
3. Select a **Protection key** with a Customer Fragment to enable [Zero-Knowledge Encryption](https://docs.akeyless.io/docs/gateway-zero-knowledge) and click Next.
4. Define the remaining parameters as follows:
   - **DB Username**: Privileged Aerospike user name with sufficient rights to create and manage users.
   - **DB Hostname**: Target Aerospike seed node hostname or IP address.
   - **DB Password**: Password of the privileged Aerospike user.
   - **DB Port**: Target Aerospike port (default 3000).
   - **DB Name**: Target Aerospike namespace.
   - **SSL**: Check to enable TLS to the Aerospike cluster, requires an SSL certificate.
   - **mTLS**: Enable mTLS to present a client certificate and key during authentication.
   - **Client Certificate**: Client certificate in Base64 format. Relevant only when mTLS is enabled.
   - **Client Private Key**: Client private key in Base64 format. Relevant only when mTLS is enabled.<br />Client Private Key Passphrase: Optional passphrase for the client private key. Relevant only when mTLS is enabled.
   - **DB Server Name**: The server name used to verify the hostname on the returned certificates unless InsecureSkipVerify is provided. It is also included in the client's handshake to support virtual hosting unless it is an IP address.

5.Click **Finish**.

# <br />
