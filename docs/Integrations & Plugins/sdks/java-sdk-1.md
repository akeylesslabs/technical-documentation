---
title: Java SDK
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
The Akeyless [Java SDK](https://github.com/akeylesslabs/akeyless-java) makes it easy to integrate your **Java** applications, libraries, or scripts with Akeyless. The following guide shows a typical integration.

# Installation

Building the API client library requires:

* Java version 1.7+.
* Maven (3.8.3+)/Gradle (7.2+)

### Maven Users

If your project uses **Maven**, add the following repository to your **Maven** configuration file by default, it is located at `~/.m2/settings.xml`):

```xml
<repository>
    <id>central</id>
    <url>https://akeyless.jfrog.io/artifactory/akeyless-java</url>
    <snapshots><enabled>false</enabled></snapshots>
</repository>
```

Then, add the following dependency to your project's `pom.xml` file:

```xml
<dependency>
  <groupId>io.akeyless</groupId>
  <artifactId>akeyless-java</artifactId>
  <version>Specify the SDK version here</version>
  <scope>compile</scope>
</dependency>
```

> 👍 Note
>
> Don't forget to modify the value of the `<version>` element in the `pom.xml` file to specify the dependency version you want to include.

## Build from Source

Clone the <a href="https://github.com/akeylesslabs/akeyless-java" target="_blank">SDK Repository</a> and execute:

```shell
mvn clean package
```

Then, manually install the **JAR** files under the `target` folder.

# Configuration

The example below uses the following imported packages:

```java
import io.akeyless.client.ApiClient;
import io.akeyless.client.ApiException;
import io.akeyless.client.Configuration;
import io.akeyless.client.model.Configure;
import io.akeyless.client.model.ConfigureOutput;
import io.akeyless.client.model.ListItems;
import io.akeyless.client.model.ListItemsInPathOutput;
```

Create and configure an instance of Akeyless Client:

```java
ApiClient client = Configuration.getDefaultApiClient();
client.setBasePath("https://api.akeyless.io");
V2Api api = new V2Api(client);
```

To work with Your [Gateway](https://docs.akeyless.io/docs/api-gw) set the `client.setBasePath` with your Gateway API endpoint on port `8081`.

# Authentication

The Akeyless **Java** SDK supports multiple [Authentication Methods](doc:access-and-authentication-methods).

## API Key

To use an [API Key](doc:api-key) for authentication set the following:

```java
Configure body = new Configure();
body.accessId("<Access Id>").accessKey("<Access Key>");
ConfigureOutput out;
out = api.configure(body);
String token = out.getToken();
```

Make sure to set your `Access Id` and `Access Key` in the relevant places. The received token should be provided for every request that requires authentication.

## Using cloud ID

To work with a Cloud-based Auth,  Add the Akeyless [Cloud ID library](https://akeyless.jfrog.io/ui/native/akeyless-java/io/akeyless/cloudid) for **Java** and set the following dependency on your project's `pom`:

```java
<dependency>
  <groupId>io.akeyless</groupId>
  <artifactId>cloudid</artifactId>
  <version>"CloudId package version"</version>
</dependency>
```

Make sure to set the relevant `CloudId` package version.

Import the [Cloud ID library ](https://akeyless.jfrog.io/ui/native/akeyless-java/io/akeyless/cloudid)into your project:

```java
import io.akeyless.client.ApiException;
import io.akeyless.cloudid.CloudProviderFactory;
import io.akeyless.cloudid.CloudIdProvider;
```

### Authenticate using cloud ID

Set the relevant `accessType` based on your cloud provide, the following example uses `azure_ad`:

```java
String accessType = "azure_ad"; // azure_ad/aws_iam/gcp 
CloudIdProvider idProvider = CloudProviderFactory.getCloudIdProvider(accessType);
try {
    String cloudId = idProvider.getCloudId();
    
    V2Api api = new V2Api(client);
    Auth auth = new Auth();
    auth.accessId("<Access Id>");
    auth.accessType(accessType);
    auth.cloudId(cloudId);

    AuthOutput out = api.auth(auth);
    String token = out.getToken();
} catch (ApiException e) {
    System.err.println("Status code: " + e.getCode());
    System.err.println("Reason: " + e.getResponseBody());
    System.err.println("Response headers: " + e.getResponseHeaders());
    e.printStackTrace();
} catch (Exception e) {
    System.err.println("Reason: " + e.getMessage());
    e.printStackTrace();
}
```

Make sure to set your `Access Id` in the relevant place.

# Example

Wrapping everything together, here is a basic example demonstrating the `ListItems` command:

```java
import io.akeyless.client.ApiException;
import io.akeyless.cloudid.CloudProviderFactory;
import io.akeyless.cloudid.CloudIdProvider;

import io.akeyless.client.ApiClient;
import io.akeyless.client.Configuration;
import io.akeyless.client.model.*;
import io.akeyless.client.api.V2Api;

public class Main {
    public static void main(String[] argv) {
        // Use azure_ad/aws_iam/gcp, according to your cloud provider
        String accessType = "azure_ad";
        CloudIdProvider idProvider = CloudProviderFactory.getCloudIdProvider(accessType);
        try {
            String cloudId = idProvider.getCloudId();

            ApiClient client = Configuration.getDefaultApiClient();
            client.setBasePath("https://api.akeyless.io");

            V2Api api = new V2Api(client);
            Auth auth = new Auth();
            auth.accessId("<Your access id>");
            auth.accessType(accessType);
            auth.cloudId(cloudId);

            AuthOutput result = api.auth(auth);


            ListItems listBody = new ListItems();
            listBody.setToken(result.getToken());
            ListItemsInPathOutput listOut = api.listItems(listBody);
            System.out.println(listOut.getItems().size());
        } catch (ApiException e) {
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        } catch (Exception e) {
            System.err.println("Reason: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

# API Reference

For a detailed API reference, see [here](https://github.com/akeylesslabs/akeyless-java).
