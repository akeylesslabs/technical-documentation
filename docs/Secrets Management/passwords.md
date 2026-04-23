---
title: Create a Password
deprecated: false
hidden: true
metadata:
  robots: index
---
You can create a **Password** item to store the username, password, and the websites associated with those credentials.

# Create a Password from the Akeyless CLI

To create a password with the CLI, run the following command:

```shell
akeyless create-secret \
--name <Item-Name> \
--type <password> \
--url <Associated-URL> \
--password <Password> \
--username <Username> 
```

Where:

* `name`: A unique name of the password. The name can include the path to the virtual folder where you want to create the new password, using the slash / separators. If the folder does not exist, it will be created together with the password.
* `type`: The type of the item, either `static secret` or `password`.
* `url`: Comma separated list of URLs associated with the password.
* `password`: Password value.
* `username`: Username value.

You can find the complete list of parameters for this command in the CLI Reference - [Static Secrets](https://docs.akeyless.io/docs/cli-reference-static-secrets#create-secret) section.

# Create a Password from the Akeyless Console

To create a password using the Console, run the following steps:

1. Log in to the Akeyless Console, and go to **Items** > **New** > **Password**.
2. Define a Name of the password, and specify the Location as a path to the virtual folder where you want to create the new password, using slash / separators. If the folder does not exist, it will be created together with the password.
3. Define the remaining parameters as follows:
   * **Delete Protection**: When enabled, protects the secret from accidental deletion.
   * **Username**: Username value.
   * **Password**: Password value.
   * **Website**: Comma separated list of URLs associated with the password.

<br />
