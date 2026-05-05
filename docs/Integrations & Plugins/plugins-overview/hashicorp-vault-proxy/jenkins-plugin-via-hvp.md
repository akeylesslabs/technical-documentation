---
title: Jenkins Plugin by way of HashiCorp Vault Proxy
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
The Jenkins plugin adds a build wrapper to set Jenkins environment variables from secrets that are stored within Akeyless. Secrets are masked in the build log, so you can't accidentally print them.

The Jenkins plugin can also inject credentials into a build pipeline or freestyle job for fine-grained vault interactions.

To use the Jenkins plugin, you need to add the Akeyless plugin to Jenkins and enter credentials for authenticating against Akeyless. In this example, we will use an [API Key](https://docs.akeyless.io/docs/auth-with-api-key) for authentication.

> ℹ️ **Note:**
>
> You can use any of the [authentication methods](https://docs.akeyless.io/docs/access-and-authentication-methods) supported by Akeyless. Ensure that the authentication method you use is associated with an [access role](https://docs.akeyless.io/docs/rbac) with access to the required secrets.

## Configure the Akeyless Plugin in Jenkins

> ℹ️ **Note:**
>
> Akeyless developed API compatibility with HashiCorp Vault OSS, enabling the use of Vault OSS community plugins for both Static and Dynamic Secrets, you can find more information [here](https://docs.akeyless.io/docs/hashicorp-vault-proxy)

1. Log in to Jenkins and go to **Manage Jenkins > Manage Plugins**.

    ![Illustration for: > Akeyless developed API compatibility with HashiCorp Vault OSS, enabling the use of Vault OSS community plugins for both Static and Dynamic Secrets, you can find more…](https://files.readme.io/a9975df-2.png)

2. Find and install the HashiCorp Vault plugin.

    ![Illustration for: > Akeyless developed API compatibility with HashiCorp Vault OSS, enabling the use of Vault OSS community plugins for both Static and Dynamic Secrets, you can find more…](https://files.readme.io/1e80fe6-3.png)

3. From the main Jenkins page, select **New Item > Freestyle project**, then add a name for the project and select **OK**.

    ![Illustration for: 2. Find and install the HashiCorp Vault plugin. 3. From the main Jenkins page, select New Item > Freestyle project, then add a name for the project and select OK.](https://files.readme.io/6fd3690-Screenshot_at_Feb_24_17-17-46.png)

4. In the **Build Environment** tab, select the **Vault Plugin** radio button. Then, enter the [Akeyless Proxy](https://docs.akeyless.io/docs/hashicorp-vault-proxy) URL: `https://hvp.akeyless.io`

    > 📘 Info
    >
    > If you are using a customer [key fragment](https://docs.akeyless.io/docs/dfc-overview-overview) with your Akeyless Platform, set your Vault URL with the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) on port `8200`.

    ![Illustration for: > If you are using a customer key fragment with your Akeyless Platform, set your Vault URL with the Akeyless Gateway on port 8200.](https://files.readme.io/a390eba-Screenshot_at_Feb_24_17-42-02.png)

5. To set your Jenkins Vault credentials provider, to the right of the **Vault Credentials** field, select **Add**, then select **Jenkins**.

    ![Illustration for: > If you are using a customer key fragment with your Akeyless Platform, set your Vault URL with the Akeyless Gateway on port 8200. 5. To set your Jenkins Vault credentials…](https://files.readme.io/6ba1561-Screenshot_at_Feb_24_17-30-59.png)

6. In the **Add Credentials** window, from the **Kind** dropdown list, select **Vault Token Credential**, then enter your credentials and select **Add**.

    > 📘 Info
    >
    > The **Token** value is a concatenation of your Access ID and your Access Key in the following format:
    > `< Access ID >..< Access Key >`
    >
    > For example:`p-xxxxxx..accessKey`

    ![Illustration for: > Note that you can always use any of the Akeyless authentication methods by way of the Vault Token File Credential where the temporary token is read from a file on your Jenkins…](https://files.readme.io/4540e75-Screenshot_at_Feb_24_17-49-08.png)

    > 👍 Note
    >
    > The Credential Kind you select determines which authentication backend will be used. If you wish to use another [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods), see the different [Credential Types supported using the Vault plugin](https://plugins.jenkins.io/hashicorp-vault-plugin/#plugin-content-plugin-usage).
    >
    > Note that you can always use any of the Akeyless authentication methods by way of the [Vault Token File Credential](https://plugins.jenkins.io/hashicorp-vault-plugin/#plugin-content-vault-token-file-credential) where the temporary token is read from a file on your Jenkins host. You can use this in combination with a script (using the `akeyless auth` [CLI command](https://docs.akeyless.io/docs/cli-ref-auth#auth) for example) to output a periodically refreshing **temporary access token** into the file in question.

7. In the **Build Environment** tab, from the **Vault Credential** dropdown list, select the new credential, then select **Advanced**.

8. Add the following information, then select **Add a vault secret**:

    * **KV Engine Version**: Enter **1**.
    * **Skip SSL verification**: Select the checkbox.

    ![Illustration for: 8. Add the following information, then select Add a vault secret: KV Engine Version: Enter 1. Skip SSL verification: Select the checkbox.](https://files.readme.io/b1aaa6e-Screenshot_at_Feb_24_17-56-21.png)

### Dynamic Secret

To use your Jenkins Plugin to fetch Dynamic Secrets:

The **Path** should be in the following format: `<Dynamic Secret type>/creds/<Full Secret Name>`

The returned JSON object will have keys named `password` and `username`. For example:

```json
{
  "password": "BbDUelj%Z1~UH1YS",
  "username": "tmp_ProdDB_p-csdsffer"
}
```

In this example, we are fetching a dynamic secret named **ProdDB** using [MySQL Dynamic Secrets](https://docs.akeyless.io/docs/create-dynamic-secret-to-sql-db).

![Illustration for: Static Secrets To work with Static Secrets, the Vault Secret Path should be in this format for KV 1](https://files.readme.io/1af62b9-Screenshot_at_Feb_24_18-06-43.png)

To test the plugin, in Build, click “Execute shell”:

![Illustration for: To test the plugin, in Build, click Execute shell.](https://files.readme.io/05d58ab-11.png)

Provide your MySQL server IP, modify the query, and so on.

```shell
mysql --host <your MySQL server ip> --port 3306 --user=$USER --password=$PASS -e 'show databases;'
exit 0
```

Click “Apply” and “Save”.
Click “Build Now” and expect to see the following Console Output:

![Illustration for: The Key name should be set to data and the Path is secret/data/DevOps/Jenkins. If the secret value itself is a JSON-structured object, the Path must be in the…](https://files.readme.io/6f82e9a-Screenshot_at_Feb_24_18-18-31.png)

### Static Secrets

To work with Static Secrets, the Vault Secret Path should be in this format for **KV 1**:

`secret/data/<Full Secret Name>`, where the Key in the returned JSON name is `data`.

For example, let's create a secret:

```shell Jenkins
akeyless create-secret -n /DevOps/Jenkins -v 'AkeylessIsGr8'
```

The **Key name** should be set to `data` and the **Path** is `secret/data/DevOps/Jenkins`.

![Illustration for: The Key name should be set to "data" and the Path is "secret/data/DevOps/Jenkins".](https://files.readme.io/ec122e2-Screenshot_at_Jan_05_20-52-23.png)

If the secret value itself is a JSON-structured object, the **Path** must be in the following format:

 `secret/<Full Secret Name>`, without the `data/` prefix, you can use the internal JSON keys as the **Key names** for example, let's create a secret that contains a JSON-structured value:

```shell ExampleJsonSecret
akeyless create-secret -n /DevOps/JenkinsJson -v '{"username":"john","password":"secret"}'
```

The **Key names** can be: `username` and `password` where the **Path** is `secret/DevOps/JenkinsJson`

![Illustration for: For example, to fetch the secret /DevOps/JenkinsJson: The Path should be secret/DevOps/JenkinsJson, and the Key name should be set with the relevant JSON keys.](https://files.readme.io/6670afe-Screenshot_at_Jan_05_21-07-11.png)

To work with **KV 2** use the following format:

To fetch the secret **/DevOps/Jenkins**:

 The **Path** is `secret/DevOps/Jenkins`, where the Key in the returned JSON name is `DevOps/Jenkins` without the `/` prefix.

![Illustration for: For example, to fetch the secret /DevOps/JenkinsJson: The Path should be secret/DevOps/JenkinsJson, and the Key name should be set with the relevant JSON keys.](https://files.readme.io/31a52cd-Screenshot_at_Jan_05_21-12-04.png)

For example, to fetch the secret **/DevOps/JenkinsJson**:

The **Path** should be `secret/DevOps/JenkinsJson`, and the **Key name** should be set with the relevant JSON keys.

![Illustration for: For example, to fetch the secret /DevOps/JenkinsJson: The Path should be secret/DevOps/JenkinsJson, and the Key name should be set with the relevant JSON keys.](https://files.readme.io/98d3115-Screenshot_at_Jan_05_21-15-42.png)
