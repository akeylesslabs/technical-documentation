---
title: GitLab Target
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
You can define a GitLab target to be used with [GitLab Dynamic Secret](doc:gitlab-dynamic-secret).

# Create a GitLab Target in the CLI

To create a GitLab target from the CLI, run the following command:

```shell GitLab Target
akeyless target create gitlab \
--name <target name> \
--gitlab-access-token <GitLab Access Token> \
--gitlab-url https://gitlab.com
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `gitlab-access-token`: Provide GitLab access token. 

* `gitlab-url`: Provide the GitLab base URL, default is ` https://gitlab.com`

# Create a GitLab Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Infra > GitLab**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.\
   For more information, [read here](doc:implement-zero-knowledge).

4. Define the remaining parameters as follows:

* **Access Token:** Provide the GitLab Access Token.

* **GitLab URL:** Provide the GitLab base URL, the default is `https://gitlab.com`

5. Click **Finish**.
