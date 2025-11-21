---
title: GitLab Dynamic Secrets
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
You can define a GitLab Dynamic Secret to generate just-in-time access tokens, those access tokens will be associated with a [scope](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#personal-access-token-scopes)  and a [role](https://docs.gitlab.com/ee/user/permissions.html), which will define their permissions.

There are two modes for this Dynamic Secret:

* [Group Access Token](https://docs.gitlab.com/ee/user/group/settings/group_access_tokens.html) - an access token that is used to perform actions for groups and manage projects within the group.
* [Project Access Token](https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html)  - an access token that is scoped to a project, and cannot be used to access resources from other projects.

# Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw)
* **Access Token** - Access Token that will be used for authentication with GitLab

# Create a Dynamic GitLab Secret from the CLI

> 👍 Note
>
> We recommend using dynamic secrets with [Targets](https://docs.akeyless.io/docs/targets). While it saves time for multiple secret-level configurations by not requiring you to provide an [inline connection string](https://docs.akeyless.io/docs/rdp-dynamic-secrets#github-connection-strings) each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.

To create a dynamic GitLab secret from the CLI using an existing [GitLab Target](https://docs.akeyless.io/docs/gitlab-target) , run the following command: 

```shell Akeyless CLI
akeyless dynamic-secret create gitlab \ 
--name <Dynamic Secret Name>
--target-name <Target Name>
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--gitlab-access-type <project| group> \
--project-name <Project Name> \                           
--group-name <Group Name> \  
--gitlab-token-scopes <Access Token Scopes> \
--gitlab-token-role <Access Token Role> \
```

 Or using an inline connection string:

```shell Akeyless CLI
akeyless dynamic-secret create gitlab \ 
--name <Dynamic Secret Name>
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--gitlab-access-type <project | group> \
--project-name <Project Name> \                           
--group-name <Group Name> \  
--gitlab-token-scopes <Accesds Token Scopes> \
--gitlab-token-role <Accesds Token Role> \
--gitlab-access-token <GitLab Token> \
```

Where:

* `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

* `target-name`: A name of the target that enables connection to the GitLab repository. The name can include the path to the virtual folder where this target resides.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `gitlab-access-type`: the `access-type` to create the access token to, Available options are:  `project` / `group`

* `project-name` Name of the project to assign the access token to, Relevant only for `project` access-type

* `group-name`: Name of the groups to assign the access token to, Relevant only for `group` access-type

* `gitlab-token-scopes`: Name of the `scope` to assign to the access token

* `gitlab-token-role`: Name of the `role` to assign to the access token

### Inline connection string

If you don't have [GitLab Target](https://docs.akeyless.io/docs/gitlab-target) yet, you can use the command with your GitLab connection string:

* `gitlab-access-token`: **Required,** Access Token that will be used for authentication

# Fetch a Dynamic GitLab Secret value from the CLI

To fetch a dynamic GitLab secret value from the CLI, run the following command: 

```shell Akeyless CLI
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

# Create a Dynamic Secret for GitLab in the Akeyless Console

> 👍 Note
>
> To start working with dynamic secrets from the [Akeyless Console](https://docs.akeyless.io/docs/github-dynamic-secret#create-a-dynamic-github-secret-in-the-akeyless-console), you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the **GitLab** secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

* **Delete Protection**: When enabled, protects the secret from accidental deletion.
* **Target mode:** In this section, you can either select an existing GitLab Target or specify details of the target GitLab repository explicitly (e.g., if you are not authorized to create and access Targets in the Akeyless Console).

  * Use the **Choose an existing target** drop-down list to select the existing GitLab Target.

  * Select the **Explicitly specify target properties** option, to provide details of the target GitLab repository in the next step.
* **Access Type**: Choose one of the following Access-Types:
  * **Group**:  Creates an access token for [GitLab Groups](https://docs.gitlab.com/ee/user/group/)
  * **Project**: Creates an access token for [GitLab Project](https://docs.gitlab.com/ee/user/get_started/get_started_projects.html)
* **Scopes**:  Provide a comma-separated list of [GitLab Scopes](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#personal-access-token-scopes)  to be assigned to the access token
* **Role**: [GitLab Role](https://docs.gitlab.com/ee/user/permissions.html) to be assigned to the access token
* **Group Name**: Name of the group, Relevant for `group` Access Type
* **Project Name**: Name of the project, Relevant for `project` Access Type
* **User TTL:** Provide a time-to-live value for a dynamic secret (i.e., a token). When TTL expires, the access token becomes obsolete.
* **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.
* **Gateway:** Select the Gateway through which the dynamic secret will create users.
* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

5. If you checked the **Explicitly specify target properties** radio button, click **Next**.

6. Provide details of the target GitLab repository:

* **Access Token**: Access Token that will be used for authentication with GitLab.

# Fetch a Dynamic GitLab Secret value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click **Get Dynamic Secret** button.