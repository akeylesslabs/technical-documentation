---
title: Docker Hub Target
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
You can define a Docker Hub target to be used with [Docker Hub dynamic secrets](https://docs.akeyless.io/docs/docker-hub-dynamic-secrets) or [Docker Hub rotated secrets](https://docs.akeyless.io/docs/create-a-docker-hub-rotated-secret).

# Create a Docker Hub Target in the CLI

To create a Docker Hub target from the CLI, run the following command:

```shell Docker Hub Target
akeyless target create dockerhub \
--name <target name> \
--dockerhub-username <Dockerhub username> \
--dockerhub-password <Dockerhub password> \
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `dockerhub-username`: Provide the username of the Docker repository user with privileges to create temporary access tokens.

* `dockerhub-password`: The password of the privileged user.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorbluedockerhubp) section.

# Create a Docker Hub Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Infra (Docker Hub)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.\
   For more information, [read here](doc:implement-zero-knowledge).

4. Define the remaining parameters as follows:

* **Username:** Provide the username of the Docker repository user with privileges to create temporary access tokens.

* **Password:** Provide the password of the privileged user.

5. Click **Finish**.
