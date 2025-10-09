---
title: Chef Infra Target
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
You can define a Chef Infra target to be used with [Chef Infra dynamic secrets](https://docs.akeyless.io/docs/chef-infra-producer).

# Create a Chef Infra Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Infra (Chef Infra)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.\
   For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

4. Define the remaining parameters as follows:

* **Server Username:** Specify the username of the privileged Chef Infra user authorized to generate temporary credentials.

* **Server Key:** Provide the access key of the privileged Chef Infra user.

* **Server URL:** Provide the URL of the Chef Infra server.

* **Skip SSL:** Select this checkbox to skip SSL.

5. Click **Finish**.
