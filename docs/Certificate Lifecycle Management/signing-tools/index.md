---
title: Code Signing with Akeyless
slug: signing-tools
deprecated: false
hidden: false
metadata:
  robots: index
---
Akeyless provides a centralized, secure platform for code signing across various environments. By integrating with native signing tools, Akeyless ensures that private keys often generated using Distributed Fragments Cryptography (DFC) never leave the secure vault, while developers can continue using standard workflows.

The following sections summarize the integration methods for Java, Container Images, and Windows executables.

## Java & Android Signing (JAR/APK)

Integration Method: PKCS#11 Interface Tools Used: `jarsigner`, `apksigner`, `libakeyless.so`

This solution allows you to sign Java artifacts and Android applications without exporting private keys to the CI/CD environment.

* Mechanism: A custom-built shared library (`libakeyless.so`) acts as a PKCS#11 provider for the Java runtime.
* Setup:
    * **Build Library:** Compile the `libakeyless.so` driver (typically by way of a containerized build process on Oracle Linux 7 for compatibility).
    * **Configuration:** Define `pkcs11.cnf` to point to the library and `pkcs11.conf` to define Akeyless credentials and key paths.
    * **Execution:** Run standard `jarsigner` or `apksigner` commands, specifying the `sun.security.pkcs11.SunPKCS11` provider.

Read more about [Java and Android Signing (JAR/APK)](https://docs.akeyless.io/docs/java-jar-signing-wpkcs11).

## Container Image Signing

Integration Method: Notation Plugin (Notary Project) Tools Used: `notation` CLI, Akeyless Notation Plugin

Akeyless secures the software supply chain by integrating with Notation, an open-source tool for signing OCI-compliant container images.

* Mechanism: A dedicated Akeyless plugin for the Notation CLI handles cryptographic operations.
* Setup:
    * **Install Plugin:** Download and install the `notation-akeyless` binary for your OS.
    * **Configuration:** Create a `notation.conf` file with your Akeyless Gateway URL and authentication credentials.
    * **Key Management:** Map an Akeyless DFC key to a local Notation alias (`notation key add --plugin akeyless ...`).
    * **Execution:** Use `notation` sign and `notation verify` directly on your container images.

Read more about [Container Image Signing](https://docs.akeyless.io/docs/signing-image).

## Windows Code Signing

Integration Method: Key Storage Provider (KSP) Tools Used: `signtool.exe`, `certutil`, and Akeyless KSP Installer.

For Windows environments, Akeyless acts as a registered cryptographic provider, allowing standard Microsoft tools to sign executables and DLLs transparently.

* Mechanism: The Akeyless KSP (Key Storage Provider) is installed on the Windows machine, intercepting cryptographic calls from the OS.
* Setup:
    * **Infrastructure:** Generate Root Keys, Issuers, and Certificates within Akeyless.
    * **Installation:** Install the Akeyless KSP by way of MSI, which registers the provider in the Windows Registry.
    * **Sync:** Use the `akeyless-ksp-cert-helper.exe` to sync the signing certificate from Akeyless to the local Windows Certificate Store (My/Personal store).
    * **Execution:** Use standard `signtool` sign commands. The tool finds the certificate in the local store, but the private key operation is offloaded to Akeyless by way of the KSP.

Read more about [Windows Code Signing](https://docs.akeyless.io/docs/windows-code-signing-with-akeyless-v2).
