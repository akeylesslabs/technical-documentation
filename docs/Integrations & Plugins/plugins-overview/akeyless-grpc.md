---
title: Akeyless gRPC
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
**gRPC** is a modern open-source high-performance Remote Procedure Call (RPC) framework that can run in any environment. Akeyless provides **gRPC** client libraries for Akeyless API core functionality.

To work with **gRPC** clients  make sure your [Gateway](doc:api-gw) runs on version `4.14` or higher. The **gRPC** runs  on Gateway port `8085`.

> 👍 Enabling gRPC
>
> gRPC is not enabled by default on Gateway, make sure to [enable](https://docs.akeyless.io/docs/advance-gw-docker-configuration#grpc) this as part of your Gateway deployment.

The following clients' libraries are currently supported: 

* [GO](https://github.com/akeylesslabs/akeyless-grpc-go)
* [Rust](https://github.com/akeylesslabs/akeyless-grpc-rust)
* [Java](https://github.com/akeylesslabs/akeyless-grpc-java)
* [PHP](https://github.com/akeylesslabs/akeyless-grpc-php)
* [.NET](https://github.com/akeylesslabs/akeyless-grpc-dotnet)

# Installation

This flow will describe the uses of the official [GO](https://github.com/akeylesslabs/akeyless-grpc-go) client `akeyless_grpc`.

Run the following command:

```go
go get github.com/akeylesslabs/akeyless-grpc-go
```

# Example

This example demonstrates the uses of [API Key](doc:api-key) for authentication, make sure to set the following:

Your  `AccessId` and `AccessKey`, as well as your Gateway URL on port `8085`.

```go
package main

import (
	"context"
	"fmt"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	akeyless_grpc "github.com/akeylesslabs/akeyless-grpc-go/akeyless_grpc"
)

func main() {

	ctx := context.Background()
  conn, err := grpc.NewClient("https://<Your-Gateway-URL>:8085", grpc.WithTransportCredentials(insecure.NewCredentials()))

	if err != nil {
		return
	}

	client := akeyless_grpc.NewAkeylessV2ServiceClient(conn)

	authOutput, err := client.Auth(ctx, &akeyless_grpc.AuthRequest{
		Body: &akeyless_grpc.Auth{
			AccessId:   "<>",
			AccessKey:  "<>",
			AccessType: "access_key",
		},
	})

	if err != nil {
		return
	}

	listItemsResp, err := client.ListItems(ctx, &akeyless_grpc.ListItemsRequest{Body: &akeyless_grpc.ListItems{Token: authOutput.Token}})

	if err != nil {
		return
	}

	for _, item := range listItemsResp.Items {
		fmt.Println(item.ItemName)
	}

	secretResponse, err := client.GetSecretValue(ctx, &akeyless_grpc.GetSecretValueRequest{Body: &akeyless_grpc.GetSecretValue{Token: authOutput.Token, Names: []string{"/MyFirstSecret"}}})

	if err != nil {
		return
	}

	for secretName, item := range secretResponse.Data.Fields {
		fmt.Println(secretName, item.GetStringValue())
	}
}

```

This example simply lists all items and fetches the `/MyFirstSecret` value.
