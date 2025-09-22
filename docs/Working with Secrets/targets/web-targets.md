---
title: Web Target
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
You can define a Web target to be used with [custom dynamic secrets](https://docs.akeyless.io/docs/custom-producer) or [custom rotated secrets](https://docs.akeyless.io/docs/create-a-custom-rotated-secret).

# Create a Web Target in the CLI

To create a Web target from the CLI, run the following command:

```shell Akeyless CLI
akeyless target create web \
--name <target name> \
--url <url of your web application>
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

- `url`: The URL of your web application.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorbluewebp) section.

# Create a Web Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Web (Web)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.  
   For more information, [read here](doc:implement-zero-knowledge).

4. Define **URL** to specify the URL of your web application.

5. Click **Finish**.