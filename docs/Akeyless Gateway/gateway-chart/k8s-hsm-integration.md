---
title: HSM Integration
excerpt: HSM Integration on K8s
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
In any encryption system, the ability to generate pseudo-random numbers is crucial, particularly for tasks like creating encryption keys. Akeyless addresses this need by offering a solution that not only generates pseudo-random numbers, but also enhances overall data security by leveraging **Hardware Security Modules (HSMs)** to generate and securely store these pseudo-random numbers for encryption keys, ensuring maximum data security.

The integration of the Akeyless Gateway with an **HSM** utilizes the `PKCS#11` protocol to provide a seamless solution. This integration can also be leveraged for the derivation of [Zero-Knowledge](https://docs.akeyless.io/docs/zero-knowledge) **Customer Fragments** from the **HSM** to the **Gateway**, using the [HKDF](https://en.wikipedia.org/wiki/HKDF) function.

> 📘 HSM Entropy
>
> For setting the **HSM** to generate random numbers for the cryptographic operations, the **HSM** must support the `C_GenerateRandom` operation.

# Prerequisites

* **HSM** configured to work with `PKCS#11`. 

* An `AES` encryption key that supports the `hmac 256` mechanism ( **Relevant for Customer Fragment**)

* [Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

# HSM Configuration

To set the Gateway to work with your **HSM** a persistence volume must be used in order to load the  `pkcs11.so` file, you can either create a PVC manually and provide it using the  `existingClaim` or set the `storageClass` for automatic provisioning with your k8s provider. The `accessMode` should be `ReadWriteMany`. 

In addition, the **HSM pin** must be provided using a **K8s Secret** which holds the `pin`, **note** the **K8s secret** key name must be set to `pin`

```shell
kubectl create secret generic hsm-pin \
  --from-literal=pin=<hsm pin>
```

Set the following parameters as part of the `values.yaml` file:

**Note**  there are three options for identifying the **HSM Token** to work with: `slot`, `tokenLabel`, or`tokenSerial` - only one of these options needs to be set.

```yaml
## HSM configuration
hsm:
  enabled: true
  pinExistingSecret: "hsmpin"
  pkcs11LibPath:
  slot:
  ## tokenLabel:
  ## tokenSerial: 
  ## useRand: false

## Persistent volume section
persistence:
  enabled: true
  ## existingClaim: ""  
  ## mountPath: ""
  accessMode: "ReadWriteMany"
  ## storageClass: "" 
  size: 100Mi
```

Where:

* `pinExistingSecret` - A k8s secret which includes the **HSM** pin, the secret key must be `pin`.

* `pin` -  The **HSM** PIN for login, for example a `user:pass` or `wwwww-xxxx-yyyy-zzzz`.

* `slot` - The slot number to use within the **HSM** that holds cryptographic objects.

* `tokenLabel` - The token label to use within the **HSM** that holds cryptographic objects.

* `tokenSerial` - The token serial to use within the **HSM** that holds cryptographic objects.

* `useRand` - Boolean flag, setting this to `true` will direct the Gateway to get the entropy randomness of the pseudo-random numbers from the **HSM**.

* `pkcs11LibPath` - The path to a `PKCS#11` library file which should be mounted to the container filesystem. Must be a fixed path and imported along with the entire folder, since it contains configuration information. In our example, the source folder `/opt/cloudhsm` is mounted completely with all subdirectories.

# Customer Fragments

Akeyless offers two modes for integrating the customer fragment with the **HSM**: `hsm_wrapped` and `hsm_secured`. Both modes use the same mechanism: the fragment value itself is used as a seed for a [key derivation function](https://en.wikipedia.org/wiki/Key_derivation_function), which is executed with the **HSM key** performing `HMAC` signing operations. The derived value is then used as the actual customer fragment value, meaning the fragment itself is not stored in the HSM.

To derive the **Customer Fragment** into the Gateway from the **HSM**, generate the **Customer Fragment** using the following command:

```shell
akeyless gen-customer-fragment \
--name HSM_CF \
--type <hsm_wrapped|hsm_secured> \
--hsm-key-label <"akeyless_hsm">
```

Where:

* `name`: **Customer Fragment** name.

* `type`: The **HSM** mode for the **Customer Fragment** either: 

  * `hsm_wrapped`: Will derive the fragment once, when the gateway starts up, and keep the result in memory

  * `hsm_secured`: Will derive the value on each use of the key, and will not save the value.

* `hsm-key-label`: The label of the key inside the **HSM**.

Save the output in a new file called `customer_fragments.json` in a directory of your choice. Once you have your `customer_fragments.json` file saved, you'll need to save it as a k8s secret to upload them to your Gateway as described [here](https://docs.akeyless.io/docs/advanced-chart-configuration#customer-fragment)
