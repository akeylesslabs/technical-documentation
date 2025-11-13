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

### Overview

* Purpose: Build a portable shared library (libakeyless.so) compatible with Oracle TDE and Java PKCS#11 integrations.
* Minimum Oracle version supported: Oracle 21c (21.3.0) this is the oldest version customers should have.
* Target platform: Linux (amd64) compiled on Oracle Linux 7 for maximum compatibility.

### Build the Library (Go → C Shared Library)

<br />
