---
title: Java JAR & APK Signing with Akeyless
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
This guide explains how to build and validate the Akeyless PKCS#11 shared library (libakeyless.so) for use with Oracle TDE and Java JAR/APK signing.
It covers both compilation steps and signing workflows for JAR and Android APK files.

<br />

#### Overview

* Purpose: Build a portable shared library (libakeyless.so) compatible with Oracle TDE and Java PKCS#11 integrations.
* Minimum Oracle version supported: Oracle 21c (21.3.0) this is the oldest version customers should have.
* Target platform: Linux (amd64) compiled on Oracle Linux 7 for maximum compatibility.

#### Build the Library (Go → C Shared Library)

```shell
docker run --rm -it --platform=linux/amd64 \
  -v "$PWD":/src -w /src oraclelinux:7-slim /bin/bash -lc '
    set -euo pipefail

    # Install toolchain
    yum -y install gzip curl tar gcc make glibc-devel

    # Install Go 1.22.5
    curl -fsSL https://go.dev/dl/go1.22.5.linux-amd64.tar.gz | tar -C /usr/local -xz
    export PATH=/usr/local/go/bin:$PATH

    # Clean previous build
    rm -f libakeyless.so libakeyless.h

    # Build shared library
    CGO_ENABLED=1 GOOS=linux GOARCH=amd64 CC=gcc \
      go build -buildmode=c-shared \
      -ldflags "-linkmode external -extldflags -Wl,-rpath,\$ORIGIN" \
      -o libakeyless.so .

    # Validate dependencies
    echo "== ldd (should have no: not found) =="
    ldd libakeyless.so || true

    echo "== highest required GLIBC symbol (should be <= GLIBC_2.17) =="
    strings -a libakeyless.so | grep -E GLIBC_ | sort -V | tail -1
'

```

#### Validate Library Compatibility

| **Build Environment** | **Validation Environment** | **Result** | **Notes**             |
| --------------------- | -------------------------- | ---------- | --------------------- |
| OracleLinux 7 (2014)  | Ubuntu 22 (2022)           | Pass       | Compatible            |
| Ubuntu 22 (2022)      | OracleLinux 7 (2014)       | Fail       | Requires GLIBC ≥ 2.32 |

Example of failed validation:

```shell
/lib64/libc.so.6: version `GLIBC_2.32' not found
/lib64/libc.so.6: version `GLIBC_2.34' not found
```

Always compile on OracleLinux 7 (2014) or equivalent to maintain backward compatibility.

#### Oracle TDE Integration Setup

In your Akeyless account, create the following items under Secret Management:

| **Item Type** | **Path**            | **Description**         |
| ------------- | ------------------- | ----------------------- |
| Key           | `/jarsign/gadikey`  | Private key for signing |
| Certificate   | `/jarsign/gadicert` | Associated certificate  |

Copy both items into the same local directory (e.g. /work).

#### Environment Setup for JAR Signing

##### Define PKCS#11 Configuration Files

`/work/pkcs11.cnf`

```text ini
name = Akeyless
library = /work/libakeyless.so
slotListIndex = 0
```

`/work/pkcs11.conf`

```text ini
akeyless_url = "http://host.docker.internal:8080/v2"
base_item_path = "/jarsign"
log_level = "debug"
key_item = "/jarsign/gadikey"
cert_item = "/jarsign/gadicert"

[auth]
access_type = "access_key"
access_id = "p-t4l0patwex6tal"
access_key = "***********************************"

```

#### Run JAR Signing

```shell
jarsigner -debug -verbose \
  -keystore NONE \
  -storetype PKCS11 \
  -providerClass sun.security.pkcs11.SunPKCS11 \
  -providerArg /work/pkcs11.cnf \
  -tsa http://timestamp.digicert.com \
  -signedjar tika-app-signed.jar \
  tika-app-4.0.0-SNAPSHOT.jar \
  /jarsign/gadikey-cert
```

Notes

* The alias must match the private key name, suffixed with `-cert`.
* Use `-signedjar` to output a separate signed file (otherwise the input JAR is modified).
* The `-tsa` parameter adds a trusted timestamp to the signature.

#### Validate Signed JAR

```shell
jarsigner -verify tika-app-signed.jar
```

#### Android APK Signing

##### Sign APK (v1 Signature)

```shell
jarsigner -debug -verbose \
  -keystore NONE \
  -storetype PKCS11 \
  -providerClass sun.security.pkcs11.SunPKCS11 \
  -providerArg /work/pkcs11.cnf \
  -tsa http://timestamp.digicert.com \
  -signedjar app-signed-v1.apk \
  app-release-unsigned.apk \
  /jarsign/gadikey-cert
```

#### Install Android SDK and Tools

```shell
apt-get update && apt-get install -y openjdk-17-jdk unzip wget

cd /work
wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O cmdline-tools.zip
unzip cmdline-tools.zip -d android-sdk
mkdir -p android-sdk/cmdline-tools/latest
mv android-sdk/cmdline-tools/* android-sdk/cmdline-tools/latest/
```

##### Environment Variables

```shell
export ANDROID_SDK_ROOT=/work/android-sdk
export PATH=$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools:$PATH
```

##### Verify Tool Installation

```shell
$ANDROID_SDK_ROOT/build-tools/35.0.0/apksigner --version
$ANDROID_SDK_ROOT/build-tools/35.0.0/zipalign -h
```

##### Add PKCS#11 as Java Security Provider

Create `/work/java.security.additions:`

```text ini
security.provider.13=SunPKCS11 /work/pkcs11.cnf
```

Verify:

```shell
java -Djava.security.properties=/work/java.security.additions \
  -XshowSettings:security -version 2>&1 | grep SunPKCS11
```
