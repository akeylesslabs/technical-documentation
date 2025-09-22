---
title: GCP Targets
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
You can define a GCP target to be used with [GCP dynamic secrets](https://docs.akeyless.io/docs/gcp-dynamic-secrets) and [GCP rotated secrets](https://docs.akeyless.io/docs/gcp-rotated-secret). Having a GCP target will allow you to conserve the credentials chain between all of your dynamic secrets, as it is possible to point a target at a rotated secret, or to manually edit credentials in the target instead of having to change them individually for connecting items.

# Create a GCP Target in the CLI

To create a GCP target from the CLI, run the following command:

```shell Akeyless CLI
akeyless target create gcp \
--name <target name> \
--gcp-key-file-path <Path to the service account private key> \
--gcp-sa-email <GCP service account email>
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

- `gcp-key-file-path`: A path to the file with the base64-encoded private key of the service account.

- `gcp-sa-email`: The GCP service account email.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorbluegcpp) section.

# Create a GCP Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Cloud (GCP)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.  
   For more information, [read here](doc:implement-zero-knowledge).

4. Choose your preferred authentication mode by selecting one of the options:

   - Check the **Use Credentials** radio button to authenticate with the GCP admin user credentials.

   - Check the **Use Gateway's Cloud Identity** radio button to authenticate with the Gateway's Cloud IAM.

> 👍 Note
> 
> **Use Gateway's Cloud Identity** is relevant for cases where your Gateway uses a GCP service account to authenticate against Akeyless. 
> 
> For example, when you set up a [Dynamic Secret](https://docs.akeyless.io/docs/gcp-dynamic-secrets) for GCP, the target can be used for the temporary GCP service account key creation.

5. Define the remaining parameters as follows:

- **Service Account Email:** If you selected the **Use Credentials** option in the previous step, specify the super-user service account email that will be used to authenticate Akeyless with GCP.

- **Service Account Key:** Provide a base64-encoded private key of the super-user service account.

6. Click **Finish**.