---
title: Java JAR & APK Signing with Akeyless
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
This guide explains how to build and validate the Akeyless PKCS#11 shared library (libakeyless.so) for use with Oracle TDE and Java JAR/APK signing.
It covers both compilation steps and signing workflows for JAR and Android APK files.

## Overview

* Purpose: Build a portable shared library (libakeyless.so) compatible with Oracle TDE and Java PKCS#11 integrations.
* Minimum Oracle version supported: Oracle 21c (21.3.0) this is the oldest version customers should have.
* Target platform: Linux (amd64) compiled on Oracle Linux 7 for maximum compatibility.

In your Akeyless account, create the following items under Secret Management:

| **Item Type** | **Path**        | **Description**         |
| ------------- | --------------- | ----------------------- |
| Key           | `/jarsign/key`  | Private key for signing |
| Certificate   | `/jarsign/cert` | Associated certificate  |

Copy both items into the same local directory (e.g. /work).

## Environment Setup for JAR Signing

### Define PKCS#11 Configuration Files

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
key_item = "/jarsign/key"
cert_item = "/jarsign/cert"

[auth]
access_type = "access_key"
access_id = "p-texample"
access_key = "***********************************"

```

## Run JAR Signing

```shell
jarsigner -debug -verbose \
  -keystore NONE \
  -storetype PKCS11 \
  -providerClass sun.security.pkcs11.SunPKCS11 \
  -providerArg /work/pkcs11.cnf \
  -tsa http://timestamp.digicert.com \
  -signedjar tika-app-signed.jar \
  tika-app-4.0.0-SNAPSHOT.jar \
  /jarsign/key-cert
```

Notes

* The alias must match the private key name, suffixed with `-cert`.
* Use `-signedjar` to output a separate signed file (otherwise the input JAR is modified).
* The `-tsa` parameter adds a trusted timestamp to the signature.

## Validate Signed JAR

```shell
jarsigner -verify tika-app-signed.jar
```

## Android APK Signing

### Sign APK (V1 Signature)

```shell
jarsigner -debug -verbose \
  -keystore NONE \
  -storetype PKCS11 \
  -providerClass sun.security.pkcs11.SunPKCS11 \
  -providerArg /work/pkcs11.cnf \
  -tsa http://timestamp.digicert.com \
  -signedjar app-signed-v1.apk \
  app-release-unsigned.apk \
  /jarsign/key-cert
```

### Install Android SDK and Tools

```shell
apt-get update && apt-get install -y openjdk-17-jdk unzip wget

cd /work
wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O cmdline-tools.zip
unzip cmdline-tools.zip -d android-sdk
mkdir -p android-sdk/cmdline-tools/latest
mv android-sdk/cmdline-tools/* android-sdk/cmdline-tools/latest/
```

### Environment Variables

```shell
export ANDROID_SDK_ROOT=/work/android-sdk
export PATH=$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools:$PATH
```

### Verify Tool Installation

```shell
$ANDROID_SDK_ROOT/build-tools/35.0.0/apksigner --version
$ANDROID_SDK_ROOT/build-tools/35.0.0/zipalign -h
```

### Add PKCS#11 As Java Security Provider

Create `/work/java.security.additions:`

```text ini
security.provider.13=SunPKCS11 /work/pkcs11.cnf
```

Verify:

```shell
java -Djava.security.properties=/work/java.security.additions \
  -XshowSettings:security -version 2>&1 | grep SunPKCS11
```

### Align APK

```shell
cd /work
$ANDROID_SDK_ROOT/build-tools/35.0.0/zipalign -p 4 app-release-unsigned.apk app-aligned.apk
```

### Sign APK (V2/v3 Signature)

```shell
java -Djava.security.properties=/work/java.security.additions \
  -jar "$ANDROID_SDK_ROOT/build-tools/35.0.0/lib/apksigner.jar" sign \
  --ks-type PKCS11 \
  --ks-provider-name SunPKCS11-Akeyless \
  --ks NONE \
  --ks-key-alias "/jarsign/key-cert" \
  --v2-signing-enabled true \
  --v3-signing-enabled true \
  --out app-signed-v2v3.apk \
  app-aligned.apk
```

### Verify Signed APK

```shell
$ANDROID_SDK_ROOT/build-tools/35.0.0/apksigner verify \
  --verbose \
  --print-certs \
  app-signed-v2v3.apk
```
