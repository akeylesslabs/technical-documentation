---
title: Go SDK
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
The Akeyless [Go SDK](https://github.com/akeylesslabs/akeyless-go) makes it easy to integrate your **Go** applications, libraries, or scripts with Akeyless.

The following guide shows a typical integration.

# Installation

Get the Akelyess package for **Go**:

```go
go get github.com/akeylesslabs/akeyless-go/v3
```

Import the package into your project:

```go
go import "github.com/akeylesslabs/akeyless-go/v3"
```

# Configuration

Create and configure an instance of Akeyless Client:

```go
go
func main() {
	client := akeyless.NewAPIClient(&akeyless.Configuration{
		Servers: []akeyless.ServerConfiguration{
			{
        URL: "https://api.akeyless.io",
			},
		},
	}).V2Api
}
```

To work with Your [Gateway](https://docs.akeyless.io/docs/api-gw) set `host` with your Gateway API endpoint on port `8081`.

# Authentication

The Akeyless **Go** SDK supports multiple [Authentication Methods](doc:access-and-authentication-methods).

## API Key

To use an [API Key](doc:api-key) for authentication set the following:

```go
go
func authWithAPIKey(id, key string) (string, error) {
	auth := akeyless.NewAuth()
	auth.SetAccessType("api_key")
	auth.SetAccessId(id)
	auth.SetAccessKey(key)

	out, _, err := client.V2ApiService.Auth(context.Background()).Body(*auth).Execute()
	if err != nil {
		return "", fmt.Errorf("can't authenticate with api key: %w", err)
	}

	return out.GetToken(), nil
}
```

Make sure to set your `Access ID` and `Access Key` in the relevant places. The received token should be provided for every request that requires authentication.

## Using cloud ID

To work with a Cloud-based Auth, import the `akeyless-go-cloud-id` [package](https://github.com/akeylesslabs/akeyless-go-cloud-id):

```go
go get "github.com/akeylesslabs/akeyless-go-cloud-id"
```

### Authenticate using cloud ID

Set the relevant `accessType` based on your cloud provider, the following example uses `aws_iam`:

```go
go
import (
    cloudid "github.com/akeylesslabs/akeyless-go-cloud-id"
)

func authWithAWS(accessID string) (string, error) {
	id, err := cloudid.GetCloudId()
	if err != nil {
		return "", fmt.Errorf("can't get cloud identity: %w", err)
	}

	auth := akeyless.NewAuth()
	auth.SetAccessType("aws_iam")
	auth.SetCloudId(id)
	auth.SetAccessId(accessID)

	out, _, err := client.V2ApiService.Auth(context.Background()).Body(*auth).Execute()
	if err != nil {
		return "", fmt.Errorf("can't authenticate with aws: %w", err)
	}

	return out.GetToken(), nil
}
```

Make sure to set your `accessID` in the relevant place.

# Example

A basic example demonstrating the `ListItems` command:

```go
go
func main() {
	// retrieve authToken using one of supported auth methods
	authToken := ""

	listOut, _, err := client.ListItems(context.Background()).
  Body(akeyless.ListItems{Token: akeyless.PtrString(authToken),
		}).Execute()
	if err != nil {
		log.Fatalln(err)
	}

	for _, item := range listOut.GetItems() {
		log.Println(item.GetItemName())
	}
}
```

Or to retrieve a Dynamic Secret:

```go
go
func main() {
	// retrieve authToken using one of supported auth methods
	authToken := ""

	out, _, err := client.GetDynamicSecretValue(context.Background()).
		Body(akeyless.GetDynamicSecretValue{
			Name:  "my-secret",
			Token: akeyless.PtrString(authToken),
		}).Execute()
	if err != nil {
		log.Fatalln(err)
	}

	log.Println(out)
}
```

# API Reference

For a detailed API reference, see [here](https://akeyless.readme.io/reference).