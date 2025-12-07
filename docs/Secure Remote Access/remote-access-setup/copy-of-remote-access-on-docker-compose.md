---
title: 'SRA On Docker Compose '
deprecated: false
hidden: true
metadata:
  robots: index
---
In this guide, we will deploy the SRA utility on docker using docker compose. 

You can get the configuration files that will be used to deploy the gateway with the SRA by cloning the following repository to your environment:

```shell
gh repo clone akeylesslabs/docker-compose
```

The following files will be used:

* `docker-compose.yaml`: Defines the Akeyless services and their setup.
* `gateway.env` : Stores environment variables for configuring the Gateway.
* `sra.env`: Stores environment variables for Secure Remote Access.
* `cache.env`: Stores Redis password (required when cache is enabled).

<br />
