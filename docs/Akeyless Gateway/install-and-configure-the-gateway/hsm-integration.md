---
title: HSM Integration
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
In any encryption system, the ability to generate pseudo-random numbers is crucial, particularly for tasks like creating encryption keys. Akeyless addresses this need by offering a solution that not only generates pseudo-random numbers, but also enhances overall data security by leveraging **Hardware Security Modules (HSMs)** to generate and securely store these pseudo-random numbers for encryption keys, ensuring maximum data security.

The integration of the Akeyless Gateway with an **HSM ** utilizes the `PKCS#11` protocol to provide a seamless solution. This integration can also be leveraged for the derivation of [Zero-Knowledge](doc:zero-knowledge) **Customer Fragments** from the **HSM** to the **Gateway**, using the [HKDF](https://en.wikipedia.org/wiki/HKDF) function.

> 📘 HSM Entropy
> 
> For setting the **HSM** to generate random numbers for the cryptographic operations, the **HSM** must support the `C_GenerateRandom` operation.

# Prerequisites

- **HSM** configured to work with `PKCS#11`. 

- An `AES` encryption key that supports the `hmac 256` mechanism (**Relevant for Customer Fragment **)

# HSM Configuration

To configure the Gateway for your **HSM**, specify the **HSM token** using one of the following parameters during deployment: `HSM_SLOT`, `HSM_TOKEN_LABEL`, or `HSM_TOKEN_SERIAL`.  Only one parameter is required.  

The following example uses the`HSM_SLOT`:

```shell
docker run -d -p 8000:8000 -p 5696:5696 \
-e ADMIN_ACCESS_ID="<Access ID>" \
-e HSM_PIN="<HSM PIN>" \
-e HSM_SLOT="<slot number>" \
-e HSM_USE_RAND="true" \
-e PKCS11_LIB_PATH="/opt/cloudhsm/lib/libcloudhsm_pkcs11.so" \
-v /opt/cloudhsm:/opt/cloudhsm \
--name akeyless-gw akeyless/base:latest-akeyless
```

Where:

- `HSM_PIN` -  The **HSM** PIN for login, for example: a `user:pass` or `wwwww-xxxx-yyyy-zzzz`.

- `HSM_SLOT` - The slot number to use within the **HSM** that holds cryptographic objects.

- `HSM_TOKEN_LABEL` - The token label to use within the **HSM** that holds cryptographic objects.

- `HSM_TOKEN_SERIAL` - The token serial to use within the **HSM** that holds cryptographic objects.

- `HSM_USE_RAND` - Boolean flag, setting this to `true` will direct the Gateway to get the entropy randomness of the pseudo-random numbers from the **HSM**.

- `PKCS11_LIB_PATH` - The path to a `PKCS#11` library file which should be mounted to the container filesystem. Must be a fixed path and imported along with the entire folder, since it contains configuration information. In our example, the source folder `/opt/cloudhsm` is mounted completely with all subdirectories.

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

- `name`: **Customer Fragment** name.

- `type`: The **HSM** mode for the **Customer Fragment** either: 

  - `hsm_wrapped`: Will derive the fragment once, when the gateway starts up, and keep the result in memory

  - `hsm_secured`: Will derive the value on each use of the key, and will not save the value.

- `hsm-key-label`: The label of the key inside the **HSM**.

Save the output in a new file called `customer_fragments.json` in a directory of your choice. Once you have your `customer_fragments.json` file saved, you'll need to provide a path to the file containing your fragment as part of the Gateway installation command, as described in [this](doc:implement-zero-knowledge) guide.