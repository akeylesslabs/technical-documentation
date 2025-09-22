---
title: Java JAR Code Signing with Akeyless & JarSigner
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
### Primary Goals & Functionality

Java JAR code signing ensures the integrity and authenticity of Java Archive (JAR) files. By digitally signing JAR files with tools like Java JarSigner, developers and organizations can guarantee that:

* The file contents have not been tampered with since signing.
* The JAR originates from a trusted source.

### Role of PKCS#11 in Code Signing

Java’s JarSigner tool is not designed to directly call vendor-specific APIs. Instead, it relies on PKCS#11 as a bridge to communicate with external cryptographic providers. Without PKCS#11, JarSigner has no way to locate and use private keys and certificates stored securely inside Akeyless.

#### Why This Matters

* Key Security:\
  With PKCS#11, private keys remain inside Akeyless platform, JarSigner never exports them. It simply asks the PKCS#11 library to perform the signing operation.
* Compatibility with Java Security APIs:\
  Java’s PKCS11 provider can only work with libraries that implement PKCS#11. This means supporting PKCS#11 is essential for using Akeyless keys in standard Java signing flows.
* Certificate Handling:\
  JarSigner expects both the key and the certificate to be available through PKCS#11 objects. 

PKCS#11 acts as the translation layer between:

* JarSigner’s expectations (standard Java cryptography provider interface).
* Akeyless’s cryptographic capa4bilities (keys and certificates stored securely, operations executed within Akeyless).

With its PKCS#11 support, Akeyless enables JarSigner to seamlessly access and use Akeyless-managed keys and certificates for signing. This ensures that private keys remain securely protected within the Akeyless platform, while still allowing developers to perform standard Java JAR signing operations safely and without code changes.

#### Configuration

PKCS#11 Extension Compilation

```shell Shell
export GOOS=linux
export GOARCH=amd64
go build -buildmode=c-shared -o libakeyless.so
go build -buildmode=c-shared -o out/pkcs11.so
```

Extension Configuration (pkcs11.conf)

```shell Shell
akeyless_url = "http://host.docker.internal:8080/v2"
base_item_path = "/jarsign"
log_level = "debug"
key_item = "/jarsign/mykey"
cert_item = "/jarsign/mycert"

[auth]
access_type = "access_key"
access_id = "p-xxxxxxxxxxxxxx"
access_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

JarSigner Provider Configuration (pkcs11.cnf)

```shell Shell
name = Akeyless
library = /work/libakeyless.so
slotListIndex = 0
```

#### Usage

Example JarSigner Command

```shell Shell
jarsigner -debug -verbose \
  -keystore NONE \
  -storetype PKCS11 \
  -providerClass sun.security.pkcs11.SunPKCS11 \
  -providerArg /work/pkcs11.cnf \
  -tsa http://timestamp.digicert.com \
  -signedjar signed-output.jar \
  unsigned-input.jar \
  /jarsign/mykey-cert
```

Key & Certificate Creation

```shell Shell
openssl genpkey \
  -algorithm RSA \
  -out mykey.pem \
  -pkeyopt rsa_keygen_bits:2048
```

Certificate Signing Request (CSR)

```shell Shell
openssl req \
  -new \
  -key mykey.pem \
  -out mykey.csr \
  -subj "/CN=Example User/OU=DevTeam/O=ExampleOrg/L=City/C=US"
```

Self-Signed Certificate

```shell Shell
openssl x509 \
  -req \
  -in mykey.csr \
  -signkey mykey.pem \
  -out mycert.pem \
  -days 365
```
