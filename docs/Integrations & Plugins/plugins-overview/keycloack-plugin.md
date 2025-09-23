---
title: Keycloak Plugin
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
Akeyless provides an additional way of user authentication in the [Keycloak Identity Platform](https://www.keycloak.org/) using signed JWT tokens. 

Users that have a valid JWT token issued by Akeyless, which includes their email address, can use this token to authenticate in Keycloak platform instead of using their username/password.

# Installing Akeyless Keycloak Authenticator

Download the latest version of the plugin from:

<https://akeyless.jfrog.io/artifactory/akeyless-keycloak/io/akeyless/akeyless-keycloak/>

Or use the following Maven dependency definition:

```xml dependency definition
<dependency>
  <groupId>io.akeyless</groupId>
  <artifactId>akeyless-keycloak</artifactId>
  <version>Specify the plugin version here</version>
  <scope>compile</scope>
</dependency>
```

In order to deploy this plugin into a Keycloak environment copy the `akeyless-keycloak-<version>-jar-with-dependencies.jar` into your Keycloak `deployments` folder.

Verify your deployment in Keycloak logs: 

```shell
[org.jboss.as.repository] (DeploymentScanner-threads - 1) WFLYDR0001: Content added at location /opt/bitnami/keycloak/standalone/data/content/4d/ab9072c416eabb61fe0aa72f94bbc44acb1110/content
[org.jboss.as.server.deployment] (MSC service thread 1-2) WFLYSRV0027: Starting deployment of "akeyless-keycloak-jar-with-dependencies.jar" (runtime-name: "akeyless-keycloak-jar-with-dependencies.jar"
[org.keycloak.subsystem.server.extension.KeycloakProviderDeploymentProcessor] (MSC service thread 1-2) Deploying Keycloak provider: akeyless-keycloak-jar-with-dependencies.jar
[org.keycloak.services] (MSC service thread 1-2) KC-SERVICES0047: akeyless-authenticator (io.akeyless.AkeylessAuthenticatorFactory) is implementing the internal SPI authenticator. This SPI is internal and may change without notice
[org.jboss.as.server] (DeploymentScanner-threads - 1) WFLYSRV0010: Deployed "akeyless-keycloak-jar-with-dependencies.jar" (runtime-name : "akeyless-keycloak-jar-with-dependencies.jar")
```

> 👍 Note
> 
> When working with ephemeral containers, `deployments` folder should be mounted using persistent volumes.

# Setting up Akeyless Keycloak Authenticator

After successful deployment, Keycloak administrator must configure the browser authentication flow to use Akeyless Authenticator as an alternative to other authentication methods. 

Navigate to "Authentication", Select "Browser" in the combo-box, and click "Copy":

![](https://files.readme.io/7b9f1f2-image-20210621-110924.png "image-20210621-110924.png")

Name the flow as **Akeyless Browser **and click **Save**.

Click **Add execution**, select **Akeyless** from the combo-box and save:

![](https://files.readme.io/7e6d515-image-20210621-111212.png "image-20210621-111212.png")

Move "Akeyless" up and mark it as "Alternative" instead of "Disabled":

![](https://files.readme.io/ed77185-image-20210621-111323.png "image-20210621-111323.png")

On the "Bindings" tab, select "Akeyless Browser" in the combo box next to the "Browser Flow" label. Click "Save":

![](https://files.readme.io/1822f2f-image-20210621-111437.png "image-20210621-111437.png")

# Using Keycloak Authenticator

Akeyless Keycloak Authenticator uses JWT tokens signed by Akeyless to establish user identity. 

Tokens used by Akeyless Authenticator must include user’s email address. 

The token can be extracted via SAML authentication, and then retrieving the token from temporary credentials file:

```shell
$ akeyless auth --access-type saml --access-id <saml-access-id>
Authentication succeeded.
Token: <temporary token>

$ cat ~/.akeyless/.tmp_creds/<same-random-string-as-above> | jq .uam_creds -r
<JWT Token value>
```

This JWT token value should be used in Keycloak.

Initiate SAML authentication using your Keycloak deployment, and instead of using username/password on Keycloak login page, modify the URL by adding `&creds=<jwt token value>` parameter, and hit “Enter”.

If the provided JWT token is valid, and includes an email address of an existing Keycloak user, that user will be authenticated successfully, and the user will be redirected to the final address.