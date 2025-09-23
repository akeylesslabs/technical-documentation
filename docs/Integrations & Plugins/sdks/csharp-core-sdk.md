---
title: C# .NET Core SDK
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
The Akeyless [C# .NET SDK](https://github.com/akeylesslabs/akeyless-csharp-netcore) makes it easy to integrate your **.NET** applications, libraries, or scripts with the Akeyless. The following guide shows a typical integration.

# Installation

To add the Akeyless **C# .NET** SDK to your project, add the Akeyless pacakge:

```shell Bash
dotnet add package akeyless --version <package-version>
```

> 👍 Note
> 
> For a full list of the existing versions & dependencies, see [here](https://www.nuget.org/packages/akeyless).

# Configuration

Import the following libraries:

```csharp
using akeyless.Client;
using akeyless.Api;
using akeyless.Model;
```

Create and configure an instance of Akeyless Client:

```csharp csharp
configuration config = new Configuration();
config.BasePath = "https://api.akeyless.io";
var instance = new V2Api(config);
```

To work with Your [Gateway](https://docs.akeyless.io/docs/api-gw) set the `client.BasePath` with your Gateway API endpoint on port `8081`.

# Authentication

The Akeyless **C#** SDK supports multiple [Authentication Methods](doc:access-and-authentication-methods).

## API Key

To use an [API Key](doc:api-key) for authentication set the following:

```csharp csharp
var authBody = new Auth(accessId: "<Access ID>", accessKey: "<Access Key>");
AuthOutput authResult = instance.Auth(authBody);
String token = authResult.Token;
```

Make sure to set your `Access Id` and `Access Key` in the relevant places. The received token should be provided for every request that requires authentication.

## Using cloud ID

To work with a Cloud-based Auth,  Add the Akeyless [Cloud ID package](https://github.com/akeylesslabs/akeyless-netcore-cloud-id) for **C#** :

```csharp
dotnet add package akeyless-dotnet-cloudid
```

Import the package:

```csharp
using akeyless.Cloudid;
```

### Authenticate using cloud ID

Set the relevant `accessType` based on your cloud provide, the following example uses `aws_iam`:

```csharp
// Use azure_ad/aws_iam/gcp, according to your cloud provider
var accessType = "aws_iam";
var cloudIdProvider = CloudIdProviderFactory.GetCloudIdProvider(accessType);
var cloudId = cloudIdProvider.GetCloudId();


Auth auth = new Auth();
auth.AccessId = "<Access Id>";
auth.AccessType = accessType;
auth.CloudId = cloudId;

AuthOutput result = instance.Auth(auth);
string token = result.Token;
```

Make sure to set your `Access Id` in the relevant place.

# Examples

## Create a Secret

```csharp csharp
var createSecretBody = new CreateSecret(name: "netcore", value: "value", token: token);
CreateSecretOutput createSecretResult = instance.CreateSecret(createSecretBody);
```

## Retrieve a Secret

```csharp csharp
List<String> secrets = new List<String>();
secrets.Add("netcore");
var getSecretValueBody = new GetSecretValue(names: secrets, token: token);
Dictionary<string, string> getSecretValueResult = instance.GetSecretValue(getSecretValueBody);
Console.WriteLine(getSecretValueResult["netcore"]);
```

## Delete a Secret

```csharp csharp
var deleteItemBody = new DeleteItem(name: "netcore", deleteImmediately: true, deleteInDays: -1, token: token);
DeleteItemOutput deleteItemResult = instance.DeleteItem(deleteItemBody);
```

# API Reference

For a detailed API reference, see [here](https://github.com/akeylesslabs/akeyless-csharp-netcore).