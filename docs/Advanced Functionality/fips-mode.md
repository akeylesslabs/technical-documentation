---
title: FIPS Mode
excerpt: Akeyless Gateway & CLI
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
> 📘 Note
>
> Currently, FIPS mode is supported only for Linux OS

While working within a FIPS compliant environment, the following features are **not** supported:

* `RSA` asymmetric encryption key with a length of `1024 bits`.

* `AES SIV` symmetric encryption keys.

* `TLS` version lower than `TLS 1.2`

To run your Gateway in a FIPS compliant environment, run your Gateway deployment with this setting enabled: 

For Docker, run the following command with the variable `FIPS=true` : 

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e FIPS=true --name akeyless-gw akeyless/base
```

For K8s, set the chart `values.yaml`  with the following setting enabled: 

```yaml
deployment:
  fips:
    enabled: true
```

To work with our CLI in FIPS mode, download and install the following binary: 

```shell
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-fips-linux-amd64
chmod +x akeyless
./akeyless
```
