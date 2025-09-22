---
title: Artifactory Target
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
You can define an Artifactory target to be used with [Artifactory dynamic secrets](https://docs.akeyless.io/docs/artifactory-dynamic-secret-producer).

# Create an Artifactory Target in the CLI

To create an Artifactory target from the CLI, run the following command:

```shell
akeyless target create artifactory \
--name <Target name> \
--base-url <Artifactory REST URL> \
--artifactory-admin-name <Admin name> \
--artifactory-admin-pwd <Admin API Key/Password>
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `base-url`: The JFrog Artifactory REST URL, which must end with the `artifactory` postfix. For example, if you use your JFrog URL, this could be `http://myjfrog.acme.org/artifactory/`.

* `artifactory-admin-name`: The Artifactory user with privileges to create JWT tokens.

* `artifactory-admin-pwd`: The API key or password of the admin user.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorblueartifactoryp) section.

# Create an Artifactory Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Infra (Artifactory)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.\
   For more information, [read here](doc:implement-zero-knowledge).

4. Define the remaining parameters as follows:

* **Base URL:** Specify the JFrog Artifactory REST URL, which must end with the **artifactory** postfix.\
  For example, if you use your JFrog URL, this could be **[http://myjfrog.acme.org/artifactory/](http://myjfrog.acme.org/artifactory/)**.\
  Or, if you use your JFrog Artifactory server hostname and port, this could be `https://ARTIFACTORY_SERVER_HOSTNAME:8081/artifactory/`.

* **Admin Username:** Provide the name of the Artifactory user with privileges to create JWT tokens.

* **Admin API Key/Password:** Provide the API key or password of the admin user.

5. Click **Finish**.
