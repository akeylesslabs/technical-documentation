---
title: Zero Knowledge
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: gateway-caching
      title: Caching
---

<GatewayConfigManagementNote />
## Introduction

To implement [Zero-Knowledge Encryption](https://docs.akeyless.io/docs/zero-knowledge), you must set up a [Gateway](https://docs.akeyless.io/docs/gateway-overview).

Once you have a Gateway up and running, you can generate a component called the **Customer Fragment**. The customer fragment is a unique piece of any encryption key you create using it that only you can access, and even the Akeyless team cannot see it. These Customer Fragments allow you to create our special type of key called the DFC key, which can only be used by an allowed user on the gateway that holds the corresponding Customer Fragment.

Using our unique Zero-Knowledge architecture, you can deploy multiple [Gateway](https://docs.akeyless.io/docs/gateway-overview) on several different geographical jurisdictions with different fragments to comply with the regulatory requirements applied in those jurisdictions.

> ⚠️ **Warning:**
>
> When working with Customer Fragments, it is **your responsibility to back them up** securely and in a safe place.
>
> Encryption keys created with the Customer Fragment cannot be reconstructed without it. Any and all information that is encrypted with those keys will not be recoverable if the Customer Fragment is lost.

## Generate Customer Fragment from the Akeyless CLI

To generate a Customer Fragment, run the following command:

```shell
akeyless gen-customer-fragment --name <CF-Name> --description MyFirstCF --json
```

You'll get the following output:

```json
{
    "customer_fragments": [
        {
            "id": "cf-xyzxyzxyzxyzxyzxyz",
            "value": "SomE/CUstOmer/FrAGMenTvALue==",
            "description": "MyFirstCF",
            "name": "<CF-Name>"
        }
    ]
}
```

Save the output in a new file called `customer_fragments.json` in a directory of your choice.

## Deploy a Gateway With Mounted Fragments

Once you have your `customer_fragments.json` file saved, you'll need to provide a path to the file containing your fragment as part of the Gateway deployment command each time you want to update your Gateway instance.

Run the following command to create the Gateway with the mounted fragment:

```shell
docker run -d -p 8000:8000 -p 5696:5696 -v /path/of/customer_fragments.json:/home/akeyless/.akeyless/customer_fragments.json -e ADMIN_ACCESS_ID="identity-access-id" -e ADMIN_ACCESS_KEY="identity-access-key" --name akeyless-gw akeyless/base:latest-akeyless
```

## Network Reachability Model

A Customer Fragment determines whether a Gateway can perform cryptographic operations for keys and items associated with that fragment. It does not create a network boundary by itself.

If a client can reach a Gateway over the network, and that Gateway has the required Customer Fragment and is allowed to serve that caller, the client can decrypt or otherwise use the protected item through that Gateway. This behavior is expected and does not indicate a misconfiguration.

To reduce exposure across environments:

* Place each Gateway on the private network for the environment it serves.
* Limit which clients and services can reach each Gateway.
* Restrict which Access IDs each Gateway can serve. For more information, see [Restrict Gateway Access](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration#restrict-gateway-access).
* Use different Gateways and Customer Fragments for separate trust boundaries when isolation is required.

For additional hardening guidance, see [Akeyless Gateway Best Practices](https://docs.akeyless.io/docs/gateway-best-practices).

## Create a Zero-Knowledge DFC Encryption Key

Once the **Customer Fragment** is mounted in the Gateway, it can be used to secure your DFC Encryption Keys for full Zero Knowledge Encryption.

> ⚠️ **Warning:**
>
> To create a DFC encryption key with Customer Fragment, the Auth Method that's being used needs to be on the list of allowed access IDs for the gateway.

### Create DFC Key from the Akeyless Console

To create a DFC Encryption Key:

1. Open the Akeyless Gateway Console at `https://Your-Akeyless-Gateway-URL:8000/console`

2. On the menu bar at the left, click **Items**.

3. On the **Items** page, click **New** -> **Encryption Key** -> **DFC**.

4. In the pop-up, specify the parameters of the new key and select a Customer Fragment to be used with this key.

5. Click **Save**.

### Create Zero Knowledge Key from the Akeyless CLI

To generate a key using a Customer Fragment, run the following command:

```shell
akeyless create-dfc-key --name MyKeyWithMyCF --alg AES256GCM -f <customer-fragment-id>
```

Where:

* `name`: The name of the DFC Encryption Key
* `alg`: The algorithm of the DFC Encryption Key
* `customer-frg-id`: The customer fragment ID that will be used to create the DFC key

You'll get the following output:

```text
A new AES256GCM key named MyKeyWithMyCF was successfully created
```

### Set Up a Default Encryption Key

To set a default Encryption Key based on your Customer Fragment to enforce Zero-Knowledge by default for all your secrets that will be created using your Gateway. This will ensure that any item created with Akeyless (by way of Web UI, CLI, or SDKs) will be encrypted using your encryption key.

> ℹ️ **Note:**
>
> Only Symmetric encryption keys of `AESGCM` algorithm can be used as Default Encryption Keys.

To set up a default Encryption Key:

1. Open the Gateway Console by going to **Gateways -> Your-Gateway -> Manage Gateway**.

2. On the menu bar at the left, click **Defaults**.

3. In the **Default Encryption Key** drop-down list, select one of the available encryption keys.

4. Click **Save Changes**.
