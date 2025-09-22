---
title: Signing Images - Sigstore
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
Signing container images is a process that ensures their authenticity and integrity. This is achieved by adding a digital signature to the container image, which can be validated during deployment. The signature helps to verify that the image is from a trusted publisher and has not been modified.

[Sigstore ](https://docs.sigstore.dev/about/overview/)is an open-source project for improving software supply chain security. The Sigstore framework and tooling empower software developers and consumers to securely sign and verify software artifacts such as release files, container images, binaries, software bills of materials (SBOMs), and more.

To sign software artifacts and verify signatures using Sigstore, you need to install [Cosign](https://docs.sigstore.dev/system_config/installation/), which is a command line utility that can sign and verify software artifacts, such as container images and blobs.

The following registries are compatible with the Sigstore signature specification and its implementation in **Cosign**:

- **Gitlab**
- **DockerHub**

> 📘 Gateway Version
> 
> This procedure is supported starting from Gateway version **3.59.0**

# Install Cosign CLI

To install **Cosign CLI**, follow the relevant doc according to your environment OS as described in the Cosign [official docs](https://docs.sigstore.dev/system_config/installation/). In the following example for simplicity, we will use **Homebrew** package manager.

```shell
brew install cosign
```

# Akeyless Plugin Installation

Download the official **Sigstore** plugin for Akeyless public artifacts:

```shell
curl command for build
chmod +x <build name>
```

# Configuration

Create a folder for the Akeyless **Sigstore **plugin configuration:

```shell Ubuntu
mkdir /var/akeyless/conf/
```
```shell MacOS
mkdir -p /var/akeyless/conf/
```

Create a file named `/var/akeyless/conf/sigstore.conf` that will store the credentials for authenticating with Akeyless:

```shell Linux \\ MacOS
cat <<EOF > sigstore.conf
akeyless_url="https://<Your Gateway URL>:8081"
[auth]
access_id="<Access_ID>"
access_key="<Access_Key>"
access_type="access_key"
EOF
```
```shell Windows
cd C:\Users\<USER>\.akeyless\profiles
echo akeyless_url="https://<Your Gateway URL>:8081" > sigstore.conf
echo [auth] >> sigstore.conf
echo access_id="<AccessID>" >> sigstore.conf
echo access_key="<AccessKey>" >> sigstore.conf
echo access_type="access_key" >> sigstore.conf
```

Where:

- `akeyless_url` - Your Akeyless Gateway `API v2` endpoint (port `8081`), if not set, by default will work with Akeyless public API endpoint `https://api.akeyless.io`.

- `access_id` - The Auth method **Access ID**.

- `access_key` - Relevant only for [API Key](https://docs.akeyless.io/docs/api-key) Auth method.

- `access_type` - The Authentication Method type.

# Create an Encryption Key

Create an Encryption Key in Akeyless, using supported algorithms:

- `RSA2048`
- `RSA3072`
- `RSA4096`
- `EC256`

Both [DFC ](https://docs.akeyless.io/docs/encryption-keys)and [Classic key](https://docs.akeyless.io/docs/classic-keys) are supported. 

```shell
akeyless create-classic-key -n Cosign -a RSA2048 --gateway-url https://<Your-Gateway-URL:8000>
```

# Importing the Image

Log in to your DockerHub account, and [pull the image](https://docs.docker.com/engine/reference/commandline/image_pull/) from your repository. If there is no existing image in the repository, [build one](https://docs.docker.com/docker-hub/quickstart/#step-5-build-and-push-a-container-image-to-docker-hub-from-your-computer):

```shell
docker pull <DockerHubUser>/<Image:Tag>
```

Save the `sha256` value as it will be required for the signing and verifying of the image.

# Signing & Verifying the Image

Sign the image with cosign by executing the following command (Ensure that you run this command in the directory where the file `cosign_linux_amd64` is located):

```shell
./cosign_linux_amd64 sign --key akeyless://Cosign <DockerHubUser>/<Image:Tag>@sha256:<sha>
```

After executing the above command, you will be prompted to accept the terms of use. Once accepted, cosign will sign the image, and a new signature will be uploaded to your DockerHub repository

To verify the signature, use the following command:

```shell
./cosign_linux_amd64 verify --key akeyless://Cosign <DockerHubUser>/<Image:Tag>@sha256:<sha>
```

Example of a valid output: 

```shell Validation output
Verification for index.docker.io/<DockerHubUser>/<Image:Tag>@sha256:<sha> --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - Existence of the claims in the transparency log was verified offline
  - The signatures were verified against the specified public key

[{"critical":{"identity":{"docker-reference":"index.docker.io/<DockerHubUser>/<Image>"},"image":{"docker-manifest-digest":"sha256:351752acbb4aec202bcc30f7c78b57d4f5739d7d0e872b439757066204009a9b"},"type":"cosign container image signature"},"optional":{"Bundle":{"SignedEntryTimestamp":"MEQCIFYeShPI6v0K4VvNWXZ454aspDjc6DxlBcOp0ieQF+7XAiAPYfgHRVYqn0KTKMA7NSFJWSd769MXHLlNvWib7yAZ5A==","Payload":{"body":"eyJhcGlWZXJzaW9uIjoiMC4wLjEiLCJraW5kIjoiaGFzaGVkcmVrb3JkIiwic3BlYyI6eyJkYXRhIjp7Imhhc2giOnsiYWxnb3JpdGhtIjoic2hhMjU2IiwidmFsdWUiOiJiMjc1OTFhMDdkZTEzOWZmYjI0ZGIyYjgxNjYyNzlmNmNhMWM4N2Q1NzVkOWU0MDU3MWM0NzU3NmY2ZTllZDhlIn19LCJzaWduYXR1cmUiOnsiY29udGVudCI6Ik01aHZGQXZDLzhYaXR3cEQyT0dQOVNvb2pIWHdtVUdUVE0yZkN4ZkFVbWpCN2lDc3dFVzVpbEx2UHNqTTJ3OFpTck9CRTRCWHR0REp5cEtCYVkrdUxTMURUOEZMT2FBSVZtVU5oT05Lek5OaDc1OGovSWlxTjFCSlNQdjljVTl5MEkyOWErdmVZNi9kaFIwNDJuZk5IMTJuTzJGVzY5aFNDRm9pd1MxQ0pnR1QrZUVJblgxck5xTjRGQk5uVGN1ZmxXNGJvUTBsRkZTdWEvZklyVzZJWmZhOGd3bjZTWXFUTytudFkxdXZuOWlnNmRBTEhJTnV2bWhSaWhOaGcwbXNKT2FQQ05aVDF4cE9halkzQnJBSmxLb1NNaW5NTGJZWWtYSTQrT29NTzhsNUlrbzBVcEtsK2I4MThIbTdXZ3NBUnJWanFVSHNQbU1ZbGp2dmsxUzJsZz09IiwicHVibGljS2V5Ijp7ImNvbnRlbnQiOiJMUzB0TFMxQ1JVZEpUaUJRVlVKTVNVTWdTMFZaTFMwdExTMEtUVWxKUWtscVFVNUNaMnR4YUd0cFJ6bDNNRUpCVVVWR1FVRlBRMEZST0VGTlNVbENRMmRMUTBGUlJVRjZSSFp1ZFRoT2NqaHVXVWs1YzFsa1ZHaHNkUXBDVjBOVWR6aEZXSFZ6VkVKcE9WZ3paM1Y0ZGt3MWNsRjViRnBwWjBwQ1pXMVVablJuVlhRMWVXZFBhMnRRVjA5dWRuVm5ja1J5VEZCcGFrZG1hRTlrQ2tORGMzSldTbkZpYlRRMVJWUkJORTg1T1docVpuaDNkbmQxVEZscFYzSlVLMDVMWnpWbVdUaHhXRTlSZW5NNGIwSlNjRlZwWldGUlduSlpkR2hGYTJNS1EzQnRXR1Y1Y0M5c01XWjZjbE5ZWkhadVozUm9ObXRSYWtKNmNsWk5URWhSTlhwbFp6ZG5ZMGhSYUdvMGNVRXllRTl4VGtoM2FIY3JlRkJuVWtaUVlncEVXVXhWVFRsVGVrZDZSMlJCZWxSR1dqaEZZMlVyZURaU1ZqZE1WM2RNUTJkek5HcGxha05RWm5CVk5rTXJlRWRFWkZaa1ZIVmxVelpuWjFCbVNFTnhDalU1VVdaUWRYRjBjRTVxTTJWWlZXVTVibU4zVmxCUlREVXdhVFoxTTJoamEyUlJWM2RqT1cxUGFuZHBSbWxCYm5RMFRYVkViMGhvYnpCaGQzTmpaR2dLVlZGSlJFRlJRVUlLTFMwdExTMUZUa1FnVUZWQ1RFbERJRXRGV1MwdExTMHRDZz09In19fX0=","integratedTime":1706178518,"logIndex":66371780,"logID":"c0d23d6ad406973f9559f3ba2d1ca01f84147d8ffc5b8445c224f98b9591801d"}}}}]
```

Additionally, the signature will appear in your DockerHub account under the "Tags" tab.