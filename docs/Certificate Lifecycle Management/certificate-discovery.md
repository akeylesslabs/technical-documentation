---
title: Certificate Discovery
deprecated: false
hidden: true
metadata:
  robots: index
---
**Certificate discovery** can be used to find every **TLS/SSL** certificate in your organization, including the ones existing on old servers, load balancers, K8s, and internal apps. It scans your environments and pulls the details:

* Where each cert lives
* Which domains it covers
* Who issued it
* When it expires. 

# Prerequisites

An [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) running version `4.46.0` or older.

# Running a Certificate Discovery with the CLI

In order to run a certificate discovery using the CLI, run the following command:

```shell
akeyless certificate-discovery \ 
--hosts <IPs, CIDR ranges, or DNS names> \
--port-ranges[=443] <80,8080-8085> \
--target-location 'Discovery-Folder' \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

Where:

* `-o, --hosts`: **Required**, A comma separated list of **IPs**, **CIDR ranges**, or **DNS names** to scan.
* `-p, --port-ranges[=443]`: A comma separated list of port ranges. Example: `80`, `8080`-`8085`.
* `-f, --target-location`: **Required**, The folder the certificates that were found in the scan will be saved at.
* `-e, --expiration-event-in`: How many days before the expiration of the certificate would you like to be notified. To specify multiple events, use argument multiple times: `--expiration-event-in 1` `--expiration-event-in 5`.
* `-k, --protection-key`: The name of the key that protects the certificate value (if empty, the account default key will be used).
* `-d, --debug`: Use this flag to run the command in **Debug mode**.
