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

<GatewayConfigManagementNote />
In any encryption system, the ability to generate pseudo-random numbers is crucial, particularly for tasks like creating encryption keys. Akeyless addresses this need by offering a solution that not only generates pseudo-random numbers, but also enhances overall data security by leveraging **Hardware Security Modules (HSMs)** to generate and securely store these pseudo-random numbers for encryption keys, ensuring maximum data security.

The integration of the Akeyless Gateway with an **HSM** uses the `PKCS#11` protocol to provide a seamless solution. This integration can also be leveraged for the derivation of **Customer Fragments** from the **HSM** to the **Gateway**, using the [HKDF](https://en.wikipedia.org/wiki/HKDF) function. For related guidance, see [Zero Knowledge](https://docs.akeyless.io/docs/zero-knowledge) and [Gateway Zero-Knowledge](https://docs.akeyless.io/docs/gateway-zero-knowledge).

> ℹ️ **Note (HSM Entropy):**
>
> For setting the **HSM** to generate random numbers for the cryptographic operations, the **HSM** must support the `C_GenerateRandom` operation.

## Prerequisites

* **HSM** configured to work with `PKCS#11`.

* An `AES` encryption key that supports the `hmac 256` mechanism ( **Relevant for Customer Fragment**)

* [Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) (for Kubernetes deployments)

## HSM Configuration

To configure the Gateway for your **HSM**, specify the **HSM token** using one of the following parameters during deployment: `HSM_SLOT`, `HSM_TOKEN_LABEL`, or `HSM_TOKEN_SERIAL`. Only one parameter is required.  

The following example uses the `HSM_SLOT`:

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

* `HSM_PIN` - The **HSM** PIN for login, for example: a `user:pass` or `wwwww-xxxx-yyyy-zzzz`.

* `HSM_SLOT` - The slot number to use within the **HSM** that holds cryptographic objects.

* `HSM_TOKEN_LABEL` - The token label to use within the **HSM** that holds cryptographic objects.

* `HSM_TOKEN_SERIAL` - The token serial to use within the **HSM** that holds cryptographic objects.

* `HSM_USE_RAND` - Boolean flag, setting this to `true` will direct the Gateway to get the entropy randomness of the pseudo-random numbers from the **HSM**.

* `PKCS11_LIB_PATH` - The path to a `PKCS#11` library file which should be mounted to the container filesystem. Must be a fixed path and imported along with the entire folder, since it contains configuration information. In our example, the source folder `/opt/cloudhsm` is mounted completely with all subdirectories.

## Kubernetes Deployment Settings

For Kubernetes deployments, you can configure HSM integration directly in the Helm `values.yaml` file.

To set the HSM PIN in Kubernetes, create a secret where the secret key is named `pin`:

```shell
kubectl create secret generic hsm-pin \
  --from-literal=pin=<hsm-pin>
```

You can then reference that secret and configure persistence in `values.yaml`.

Use the values structure that matches your chart:

### akeyless-gateway chart (`gateway.hsm`)

```yaml
gateway:
  hsm:
    enabled: true
    pinExistingSecret: "hsm-pin"
    pkcs11LibPath: "/opt/cloudhsm/lib/libcloudhsm_pkcs11.so"
    slot: "<slot-number>"
    # tokenLabel: "<token-label>"
    # tokenSerial: "<token-serial>"
    # useRand: false

persistence:
  enabled: true
  accessMode: "ReadWriteMany"
  # existingClaim: ""
  # storageClass: ""
  size: 100Mi
```

### akeyless-api-gateway chart (`hsm`)

```yaml
hsm:
  enabled: true
  pinExistingSecret: "hsm-pin"
  pkcs11LibPath: "/opt/cloudhsm/lib/libcloudhsm_pkcs11.so"
  slot: "<slot-number>"
  # tokenLabel: "<token-label>"
  # tokenSerial: "<token-serial>"
  # useRand: false

persistence:
  enabled: true
  accessMode: "ReadWriteMany"
  # existingClaim: ""
  # storageClass: ""
  size: 100Mi
```

Where:

* `pinExistingSecret` - The Kubernetes secret name that includes the `pin` key.

* `pkcs11LibPath` - The `PKCS#11` library path mounted in the Gateway container.

* `slot`, `tokenLabel`, `tokenSerial` - HSM token identification options. Set one of these values.

* `useRand` - Boolean flag. If set to `true`, Gateway uses the HSM as an entropy source.

* `persistence` - Persistent storage settings for mounting HSM client libraries and related files in Kubernetes.

* `gateway.hsm` and `hsm` - Chart-specific value paths. Use the one that matches your deployed chart.

## Customer Fragments

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

Save the output in a new file called `customer_fragments.json` in a directory of your choice. Once you have your `customer_fragments.json` file saved, you'll need to provide a path to the file containing your fragment as part of the Gateway deployment command, as described in [this](https://docs.akeyless.io/docs/zero-knowledge) guide.
