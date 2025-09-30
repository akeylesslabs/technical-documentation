---
title: RabbitMQ Dynamic Secrets
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
You can define a dynamic RabbitMQ secret to generate user credentials dynamically based on configured permissions.

When a client requests a dynamic secret value, the Akeyless Platform connects to the target RabbitMQ server through the Gateway and creates a new user.

# Prerequisites

* An [Akeyless Gateway](doc:api-gw)

* A RabbitMQ privileged user

Before creating a dynamic RabbitMQ secret, ensure that the RabbitMQ user has sufficient privileges to create users.

# Create a Dynamic RabbitMQ Secret from the CLI

> 👍 Note
>
> We recommend using dynamic secrets with [Targets](doc:targets). While it saves time for multiple secret-level configurations by not requiring you to provide an [inline connection string](https://docs.akeyless.io/docs/rabbitmq-producer#inline-connection-strings) each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.

To create a dynamic RabbitMQ secret from the CLI using an existing [RabbitMQ Target](doc:rabbitmq-targets) , run the following command:

```shell Akeyless CLI
akeyless dynamic-secret create rabbitmq \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rabbitmq-user-conf-permission <User configuration permission> \
--rabbitmq-user-write-permission <User write permission> \
--rabbitmq-user-read-permission <User read permission> \
--password-length 16
```

Or using an inline connection string:

```shell Akeyless CLI
akeyless dynamic-secret create akeyless dynamic-secret get-valuerabbitmq \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--rabbitmq-user-conf-permission <User configuration permission> \
--rabbitmq-user-write-permission <User write permission> \
--rabbitmq-user-read-permission <User read permission> \
--rabbitmq-server-uri <RabbitMQ server URI> \
--rabbitmq-admin-user <RabbitMQ server admin> \
--rabbitmq-admin-pwd <RabbitMQ server password>
```

Where:

* `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

* `target-name`: A name of the target that enables connection to the RabbitMQ server. The name can include the path to the virtual folder where this target resides.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `rabbitmq-user-conf-permission`: User configuration permissions, for example: `.*,queue-name`.

* `rabbitmq-user-write-permission`: User write permissions, for example: `.*,queue-name`.

* `rabbitmq-user-read-permission`: User read permissions, for example: `.*,queue-name`.

* `password-length`: **Optional** The temporary user password length.

### Inline connection string

If you don't have [RabbitMQ Target](doc:rabbitmq-targets) yet, you can use the command with your RabbitMQ target server connection settings:

* `rabbitmq-server-uri`: URI of the RabbitMQ server.

* `rabbitmq-admin-user`: Admin username for the RabbitMQ server.

* `rabbitmq-admin-pwd`: Admin password for the RabbitMQ server.

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#p-stylecolorbluerabbitmqp) section.

# Fetch a Dynamic RabbitMQ Secret value from the CLI

To fetch a dynamic RabbitMQ secret value from the CLI, run the following command:

```shell Akeyless CLI
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

# Create a Dynamic RabbitMQ Secret in the Akeyless Console

> 👍 Note
>
> To start working with dynamic secrets from the [Akeyless Console](https://docs.akeyless.io/docs/rabbitmq-dynamic-secrets#create-a-dynamic-rabbitmq-secret-in-the-akeyless-console), you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the RabbitMQ secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

* **Delete Protection:** When enabled, it protects the secret from accidental deletion.

* **Target mode:** In this section, you can either select an existing [RabbitMQ Target](doc:rabbitmq-targets) or specify details of the target RabbitMQ server explicitly.

  * Use the **Choose an existing target** drop-down list to select the existing [RabbitMQ Target](doc:rabbitmq-targets).

  * Select the **Explicitly specify target properties**  to provide details of the target RabbitMQ server in the next step.

RabbitMQ distinguishes between `configure`, `write`, and `read` operations on a resource. To perform an operation on a resource, the user must be granted the appropriate permissions for it. The [RabbitMQ permissions reference](https://www.rabbitmq.com/access-control.html#:~:text=Permissions%20are%20expressed%20as%20a,names%20matching%20the%20regular%20expressions.\&text=and%20server%20generated%20names%20are%20prefixed%20with%20amq) outlines the relevant resources and operations.

* **User Configuration Permission:** Enter the resources for which the `configure` operation can be performed when accessed using the relevant dynamic key.

* **User Write Permission:** Enter the resources for which the `write` operation can be performed when accessed using the relevant dynamic key.

* **User Read Permission:** Enter the resources for which the `read` operation can be performed when accessed using the relevant dynamic key.

* **User Virtual Host:** In RabbitMQ, user permissions are granted per virtual host. Bind the user to the specific virtual host (default “/”).

* **User Tags:** Access to management UI in RabbitMQ can be controlled with user tags. Insert relevant user tags in a comma-separated list, including these tags: management, administrator, monitoring, and policymaker.

* **User TTL:** Provide a time-to-live value for a dynamic secret (i.e., a key). When TTL expires, the key becomes obsolete.

* **Temporary Password Length** Set the length of the temporary password.

* **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.

* **Gateway:** Select the Gateway through which the dynamic secret will create users.

* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](doc:implement-zero-knowledge).

5. If you checked the **Explicitly specify target properties**  option, click **Next**.

6. Provide details of the target RabbitMQ server:

* **Server URI:** Enter the RabbitMQ server address.

* **Admin User:** Enter your RabbitMQ admin credentials.

* **Admin Password:** Enter your RabbitMQ admin credentials.

7. Click **Finish**.

# Fetch a Dynamic RabbitMQ Secret Value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click the **Get Dynamic Secret** button.
