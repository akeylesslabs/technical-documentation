---
title: RabbitMQ Target
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
You can define a RabbitMQ target to be used with [RabbitMQ Dynamic Secrets](https://docs.akeyless.io/docs/rabbitmq-producer) 

# Create a RabbitMQ Target in the CLI

To create a RabbitMQ target from the CLI, run the following command:

```shell Akeyless CLI
akeyless target create rabbitmq \
--name <target name> \
--user <RabbitMQ server user> \
--pwd <RabbitMQ server password> \
--uri <RabbitMQ server URI>
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `user`: The username of the privileged RabbitMQ user.

* `pwd`: The password of the privileged RabbitMQ user.

* `uri`: The URL of the RabbitMQ server. 

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorbluerabbitmqp) section.

# Create a RabbitMQ Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Infra (RabbitMQ)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.\
   For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

4. Define the remaining parameters as follows:

* **Server URI:** Enter the RabbitMQ server address. 

* **Admin User:** Enter your RabbitMQ admin credentials.

* **Admin Password:** Enter your RabbitMQ admin credentials.

5. Click **Finish**.
