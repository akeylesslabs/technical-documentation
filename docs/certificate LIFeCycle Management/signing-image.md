---
title: Signing Images
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
Signing container images is a process that ensures their authenticity and integrity. This is achieved by adding a digital signature to the container image, which can be validated during deployment. The signature helps to verify that the image is from a trusted publisher and has not been modified.

Notation is an open-source supply chain tool developed by the [Notary Project](https://notaryproject.dev/), which supports signing and verifying container images and other artifacts. 

The following registries are compatible with the Notary Project OCI signature specification and its implementation in Notation:

- **Azure Container Registry**
- **Amazon Elastic Container Registry**
- **GitHub Container Registry**
- **ORAS Distribution Registry**
- **Zot registry**

Akeyless can be used to store certificates with signing keys that can be used by Notation with the Akeyless plugin for Notation, to sign and verify container images and other artifacts for the [supported](https://notaryproject.dev/docs/faq/) container registries.

# Install the Notation CLI

To install the Notation CLI, follow the relevant doc according to your environment OS as described in the Notation [official](https://notaryproject.dev/docs/user-guides/installation/) docs. In the following example for simplicity, we will use [Homebrew](https://brew.sh/) package manager.

```shell
brew install notation
```

# Akeyless Plugin Installation

The plugin directory varies depending on the operating system being used. The directory path in our example assumes Ubuntu. Please read the Notation [directory structure](https://notaryproject.dev/docs/user-guides/how-to/directory-structure/) for system configuration for more information.

Create a folder for the Akeyless Notation plugin configuration:

```shell Ubuntu
mkdir -p ~/.config/notation/plugins/akeyless
```
```shell MacOS
mkdir -p $HOME/Library/Application\ Support/notation/plugins/akeyless
```
```shell Windows
mkdir %AppData%/notation/plugins
```

Download the Akeyless official Notation plugin for Akeyless public artifacts:

```shell Ubuntu
cd ~/.config/notation/plugins/akeyless
curl -o notation-akeyless https://rest.akeyless.io/Akeyless_Artifacts/Linux/notation-akeyless/notation-akeyless-linux-amd64
chmod +x notation-akeyless
```
```shell MacOS
cd $HOME/Library/Application\ Support/notation/plugins/akeyless
curl -o notation-akeyless https://rest.akeyless.io/Akeyless_Artifacts/MacOS/notation-akeyless/notation-akeyless-darwin-arm64
chmod +x notation-akeyless
```
```shell Windows
cd  %AppData%/notation/plugins
curl -o notation-akeyless https://rest.akeyless.io/Akeyless_Artifacts/Windows/notation-akeyless/notation-akeyless-windows-amd64.exe
```

> 📘 Note
> 
> For **AMD** architecture download the relevant binaries from [here](https://rest.akeyless.io/Akeyless_Artifacts/)

List the Notation Plugins list to verify that Akeyless is listed. 

```shell
notation plugin ls
```

## Configuration

Notation Plugins configuration supports the use of environment variables or static config file, our example will use a config file.  

Depending on your OS type create the relevant config file accordingly:

```shell Linux \\ MacOS
cd /var/akeyless/conf
cat <<EOF > notation.conf
akeyless_url="https://<Your Gateway URL>:8000/api/v2 # Or using port :8081"
[auth]
access_id="<AccessID>"
access_key="<AccessKey>"
access_type="access_key"
EOF
```
```shell Windows
cd C:\Users\<USER>\.akeyless\profiles
echo akeyless_url="https://<Your Gateway URL>:8081" > notation.conf
echo [auth] >> notation.conf
echo access_id="<AccessID>" >> notation.conf
echo access_key="<AccessKey>" >> notation.conf
echo access_type="access_key" >> notation.conf
```

Where: 

- `akeyless_url` - Your Akeyless Gateway `API v2` endpoint `8000/api/v2 ` (or using your gateway url at port `8081`).,  if not set, by default will work with Akeyless public API endpoint `https://api.akeyless.io`. 

- `access_type` - The [Authentication Method](doc:access-and-authentication-methods) type, supporting:`access_key`,`aws_iam`,`gcp`,`azure_ad` `certificate`,`jwt` and `k8s`. 

- `access_id` - The Auth method **Access ID**.  

- `access_key` - Relevant only for  [API Key](doc:api-key) Auth method.

- `k8s_conf_name` - Relevant only for [Kubernetes](doc:kubernetes-auth) Auth method. 

## Create a Self-Signed Certificate

The Notary project specified the [requirements](https://github.com/notaryproject/specifications/blob/v1.0.0/specs/signature-specification.md#certificate-requirements) for different types of certificates, the following examples will use a **Self Signed CA** certificate. 

> 📘 Note
> 
> It is possible to work with Akeyless  [PKI Issuer](doc:ssh-and-pkitls-certificates)  to generate the certificates, the PKI Issuer must be set with the `Code Signing` flag , and `Key Usage List` of `critical,DigitalSignature`.

Akeyless Supports both **EC** and **RSA** algorithms, run the following commands to create a key with a self signed certificate.

Create a **CSR** config file:

```shell
cat <<EOF > csr.conf
countryName	= US
stateOrProvinceName	= NY
localityName	= NY
organizationName  = Akeyless
organizationalUnitName	= Security
commonName = akeylessSign

[ v3_req ]
basicConstraints = critical, CA:FALSE
keyUsage = critical, digitalSignature
EOF
```

Create a key with a self-signed certificate: 

```shell
akeyless create-dfc-key -n CodeSign -a RSA2048 --generate-self-signed-certificate true --certificate-format pem --conf-file-path csr.conf --certificate-ttl 30
```

## Set Notation Default Key

```shell
notation key add  --plugin akeyless  --id /CodeSign --default Akeyless
```

Where: 

- `id`- The full key name or the key `item id`, as stored inside Akeyless. In our example, we used the created key named `CodeSign`.

- `default` - Optional, to mark this key for Notation as a default key, with a friendly name for notation, in this example, we simply named it`Akeyless`.

Verify that the key is added to the Notation keys:

```shell
notation key ls
```

# Sign Image

For the simplicity of this example, the following steps will demonstrate the simple creation of a trust policy to sign docker artifacts.

```shell
docker run -d -p 5001:5000 ghcr.io/oras-project/registry:v1.0.0-rc.4
```

Use `docker build`  and `docker push` to build and push a sample image to your registry.

```shell
docker build -t localhost:5001/net-monitor:v1 https://github.com/wabbit-networks/net-monitor.git#main
docker push localhost:5001/net-monitor:v1
IMAGE=$(docker inspect --format='{{index .RepoDigests 0}}' localhost:5001/net-monitor:v1)
```

Use `notation ls` to list the current signatures for your image. The following example sets the value of `$IMAGE` to the name of the image and its digest value.

```shell
notation ls $IMAGE
```

Confirm there are no signatures listed. And use `notation sign` command to sign the image:

```shell
notation sign $IMAGE
```

# Verify Image Signatures

To verify the container image, add the root certificate that signs the leaf certificate to the trust store and create trust policies for verification. For the self-signed certificate used in this tutorial, the root certificate is the self-signed certificate itself.

> 📘 Note
> 
> Depending on your OS the follow the folder structure as described [here](https://notaryproject.dev/docs/user-guides/tutorials/trust-policy/#create-a-trust-policy)

Get the certificate from Akeyless: 

```shell
 akeyless describe-item -n CodeSign --json --jq-expression .certificates | base64 -d > certificate.pem
```

Add the public certificate to a named trust store for signature verification:

```shell
notation certificate add --type ca --store selfSigned certificate.pem 
```

Create a `trustpolicy.json` with the following trust policy in the notation configuration directory.

Note: this is a very permissive trust policy. Read more on creating trust policies and trust stores [here](https://github.com/notaryproject/specifications/blob/v1.0.0/specs/trust-store-trust-policy.md): 

```json
{
 "version": "1.0",
 "trustPolicies": [
     {
         "name": "trust-policy-example",
         "registryScopes": [ "*" ],
         "signatureVerification": {
             "level" : "strict" 
         },
         "trustStores": [ "ca:selfSigned" ],
         "trustedIdentities": [
             "*"
         ]
     }
 ]
}
```

Add the policy to `notation`

```shell
notation policy import trustpolicy.json
```

Verify the signature

```shell
notation verify $IMAGE
```