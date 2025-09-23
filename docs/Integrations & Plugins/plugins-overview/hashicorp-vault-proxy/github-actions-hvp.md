---
title: GitHub Actions via HVP
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
The GitHub Actions plugin enables you to automate workflows for your GitHub-hosted repositories. With this plugin, you can pull secrets from the Akeyless Platform directly into your workflows.

To work with the GitHub Actions plugin:

1. [Create a GitHub Repository](doc:github-actions-hvp#create-a-github-repository) 
2. [Set Up Akeyless Authentication Credentials for the Repository](doc:github-actions-hvp#set-up-akeyless-authentication-credentials-for-the-repository) 
3. [Set Up a GitHub Self-Hosted Runner](doc:github-actions-hvp#set-up-a-github-self-hosted-runner)
4. [Define a Workflow for the GitHub Action](doc:github-actions-hvp#define-a-workflow-for-the-github-action)
5. [Trigger the GitHub Runner](doc:github-actions-hvp#trigger-the-github-runner) 

# Create a GitHub Repository

1. Create a new directory and initialize it as a git repository by running: 

```shell
git init
```

2. Stage all the files in the directory by running:

```shell
git add .
```

3. Commit all the staged files by running:

```shell
git commit -m "Initial Commit"
```

4. On GitHub, create a new repository. In this example, it's called **Akeyless-vault-example**.

<Image align="center" className="border" border={true} src="https://files.readme.io/3258bde-Screenshot_at_May_25_14-24-05.png" />

5. Perform an initial commit to the new repository by running:

```shell
git remote add origin https://github.com/<your_account>/<your_repository>.git
git branch -M main
git push -u origin main
```

# Set Up Akeyless Authentication Credentials for the Repository

1. On GitHub, navigate to the main page of the repository, and select **Settings** > **Secrets** > **New repository secret**.

2. Name the secret  **VAULT\_TOKEN**. 

3. Set the secret value in the following format : **\<access\_id>..\<access\_key>**. For example:

<Image align="center" className="border" border={true} src="https://files.readme.io/51a6336-image-20210524-1247311.png" />

4. Select **Add secret**.

The GitHub repository is now configured with an access token for Akeyless. 

# Set Up a GitHub Self-Hosted Runner

The GitHub [self-hosted runner](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners) enables you to start a runner instance on an instance that you manage. Your workstation can be used if it is supported.

1. On GitHub, navigate to the main page of the repository, and select **Settings** > **Actions** > **Runners** > **Add runner**.

2. Select the operating system and architecture of your self-hosted runner machine.

3. Follow the instructions in the **Download** section to prepare a directory for the GitHub runner and then download the runner.

4. Follow the instructions in the **Configure** section to configure the runner to connect to GitHub with a token GitHub generates for the runner.

# Define a Workflow for the GitHub Action

1. In a terminal, within the repository directory, create the directory **.github/workflows**.

2. In the new directory, create a workflow file named **image-builder.yml** with the following content, to define the name of the workflow and the frequency at which it triggers.

```yaml
name: ImageBuilder
# Run this workflow every time a new commit pushed to your repository.
on: push
jobs:
  build:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v2
      - name: Import Secrets
        uses: hashicorp/vault-action@v2.2.0
        env:
            ACTIONS_ALLOW_UNSECURE_COMMANDS: 'true'
        with:
          url: https://hvp.akeyless.io
          tlsSkipVerify: true
          token: ${{ secrets.VAULT_TOKEN }}
          secrets: |
            secret/data/ci/Gitsecret/actions ci/Gitsecret/actions | action ;
      - name: Secret from Akeyless
        run: echo "${{ env.app_secret }}"
```

> 📘
>
> If you are working with your own Akeyless Gateway, set the value of the **url** field as your Akeyless Gateway URL of your Gateway HVP endpoint `https://Your-Gateway-URL:8000/hvp` (or using your gateway url at port 8200)

Note that the token used to authenticate is set to the **VAULT\_TOKEN** secret you defined in the GitHub repository.

where **secret/data** is a required prefix, followed by the secret path.  In this example, the secret <code>actions</code> in the Akeyless Platform is stored in the <code>/ci/Gitsecret/</code> folder. Therefore, the secret path is <code>/ci/Gitsecret/actions</code>, the selector is `ci/Gitsecret/actions`, and `action` is an environment variable that can be used in the workflow. 

> 🚧 Warning
>
> The selector format must not start with the `/` prefix.

```yaml
secrets: |
  secret/data/ci/Gitsecret/actions ci/Gitsecret/actions | action ;
```

Another example of pulling a secret `ci/Gitsecret` where the secret value is a `JSON` object with a key name `app_secret` using the following format:

```yaml
secrets: |
  secret/data/ci/Gitsecret app_secret | secret_app ;
```

<code>app\_secret</code> is the key name and <code>secret\_app</code> is the environment variable to store the secret value within your flow. 

# Trigger the GitHub Runner

The workflow is triggered on every push to any branch of the repository.

Add the unstated files to be committed by running:

```shell
git add .
git commit -m "adds workflow to repo"
git push origin main
```

The GitHub self-hosted runner polls GitHub for changes. When a change is detected, the runner begins execution on the workflow. The build result can be seen in GitHub, in the **Actions** section.
