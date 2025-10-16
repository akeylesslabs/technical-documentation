---
title: Certificates
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Certificates
  description: ''
  robots: index
next:
  description: >-
    Make sure to associate your new Authentication Method with an Access Role to
    grant the relevant permissions within Akeyless
---
**Certificate-based authentication** is a method of verifying identity using digital certificates. A certificate contains a public key, which is validated against a trusted **Certificate Authority (CA)**, while the requester proves ownership by using the matching private key.

This method is most often used for **machine-to-machine** authentication, where servers or applications automatically prove their identity. Many organizations already operate a private CA to issue and manage certificates for their systems.

2 modes can be used for authentication:

* **CLI** / **UI**- In this mode, you only need to provide the `location` or `data` of the certificate and the matching private key locally.

* **SDK** – In this mode, to verify the possession of the client on the private key, either the private key is sent to the Akeyless Gateway to verify the certificate challenge. Alternatively, you can perform the certificate verification challenge [manually](https://docs.akeyless.io/docs/certificate-based-authentication#manual-certificate-verification). Allowing you to avoid transmitting the private key to the Gateway.

<Image align="center" border={false} src="https://files.readme.io/8191f2c-Cert_key_auth.png" />

# Prerequisites

* A **Chain of Trust** for siging a **Client** Certificate , If you don't have one, you can [build your chain of trust](https://docs.akeyless.io/docs/build-your-chain-of-trust) in Akeyless.

* A **Client** Certificate (signed by an Intermediate CA) with `clientauth` key usage, along with the corresponding Private Key, both in `PEM` format.

## Create a Certificate-based Authentication Method in the CLI

To create a certificate-based authentication method, the user must provide a signed client certificate, and a `unique identifier` that could be a value of `common_name` or `organizational_unit` parameters from the certificate.

A `unique identifier` acts as a <a href="https://docs.akeyless.io/docs/sub-claims" target="_blank">sub-claim</a> helping to uniquely identify the authenticating Identity.

To create a certificate-based authentication method, run the following command:

```shell CLI
akeyless auth-method create cert \
--name <Auth Method name> \
--unique-identifier 'common_name' \
--certificate-file-name 'ca_certificate.pem'
```

Where:

* `name`: A unique name for the authentication method. The name can include the path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

* `unique-identifier` A unique identifier parameter plays the same role as a `sub-claim` in OIDC, OAuth2, LDAP, and SAML authentication method types. It contains details that allow the system to uniquely identify the user (e.g., distinguishing between users from within the same organization).

* `certificate-file-name`: A path to the **Client** certificate.

You can find the complete list of additional parameters for this command in the [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#p-stylecolorbluecertp) section.

## Authenticate with the Certificate-based Authentication Method

To authenticate using the new certificate-based authentication method, run the following command:

```shell CLI
akeyless auth \
--access-id <Access ID> \
--access-type cert \
--cert-file-name cert.pem \
--key-file-name key.pem
```

Where:

* `access-id`: The `Access ID` of the **Certificate** Authentication Method

* `cert-file-name`: Path to the signed x509 PEM Encoded Certificate in a `PEM` format

* `key-file-name`: Matching **Private Key** for the certificate in a `PEM` format

As a result, you should get the authentication token

You can find the complete list of additional parameters for this command in the [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#p-stylecolorblueauthp) section.

## Create a Certificate-based Authentication Method in the Console

1. Log in to the Akeyless Console and go to **Users & Auth Methods > New > Application (Certificate)**.

2. Define a **Name** for the authentication method, and specify the **Location** as a path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

3. Define the remaining parameters as follows:

* **Expiration Date:** Select the access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.

* **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean CURL, SDK, etc. This parameter is optional. Leave it empty for unrestricted access.

* **Allowed Trusted Gateway IPs:** Enter a comma-separated list of CIDR blocks. When specified, the Gateway with the IP from this range will be trusted to forward original client IPs (so that they will be visible in the logs). If empty, the Gateway's IP will be used in the logs.

* **Audit Log Sub Claims:** Enter a comma-separated list of sub-claims keys to be included in the audit logs.

* **Allowed Client Type**: Specifies which clients can use this Authentication Method, available options:
  * **CLI/SDK**
  * **Web UI**
  * **Gateway Admin Console**

* **CA Certificate:** Download the CA certificate in Base64 format.

* **Bound Common Names:** Enter a list of names. At least one must exist in the Common Name of the certificate. Supports globbing.

* **Bound DNS SANs:** Enter a list of DNS names. At least one must exist in the SANs of the certificate. Supports globbing.

* **Bound Email SANs:** Enter a list of Email Addresses. At least one must exist in the SANs of the certificate. Supports globbing.

* **Bound URI SANs:** Enter a list of URIs. At least one must exist in the SANs of the certificate. Supports globbing.

* **Bound Organizational Units:** Enter a list of Organizational Units' names. At least one must exist in the OU field of the certificate.

* **Bound Extensions:** Enter a list of extensions formatted as `oid:value`. Expects the extension value to be some type of ASN1 encoded string. All values must exist in the certificate. Supports globbing on `value`.

* **Revoked Cert Ids:** Enter a list of revoked certificate IDs. It can be used to revoke specific certificates or intermediate certificates.

* **Allowed CORS Domains:** Comma-separated list of allowed CORS domains to be validated as part of the authentication flow. Relevant only when using UI, specify which CN\domain to look in the key store.

* **Unique Identifier:** A unique identifier to distinguish different users, such as `common_name` or `organizational_unit`.

4. Click **Finish**.

# Manual Certificate Verification

Instead of providing your private key directly to the Gateway, you can now prove possession of the key by completing the certificate verification challenge manually.

Use this option when you want maximum protection for your private key, or when your organization requires that private keys remain on managed endpoints.

This can be done using 2 modes:

* Manual challenge generation and signing:

Run the following command to generate a challenge for the certificate:

```shell
akeyless get-cert-challenge \
--access-id <Auth-Method-AccessID> \
--cert-data <cert data encoded in base64>
```

Running the above will produce a unique value that must be signed by the corresponding private key in order to continue the authentication process. Note, this challenge is valid for 60 seconds only.

* Automated challenge generation and signing with the SDK:

Alternatively, you can use one of the scripts below to fully automate the process. The script will generate and sign the challenge, then return an authentication token as the output.

The script requires the following parameters:

* **Certificate location** - The location of the certificate.
* **Private Key Location** - The location of the Private Key.
* **Access ID** - The Access ID of the Certificate Authentication Method.
* **Gateway URL** - Your Gateway URL followed by the `/api/v2` API path.

```go main.go
package main

import (
	"context"
	"crypto"
	"crypto/ecdsa"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"encoding/base64"
	"fmt"
	"log"
	"os"

	"github.com/akeylesslabs/akeyless-go/v3"
)

func main() {
	// --- Step 1: Initialize the API Client ---
	client := akeyless.NewAPIClient(&akeyless.Configuration{
		Servers: []akeyless.ServerConfiguration{
			{
        URL: "https//:<Akeyless-GW-URL>/api/v2",
			},
		},
	}).V2Api

	ctx := context.Background()

	// --- Step 2: Get Challenge ---
	accessID := "<YOUR_ACCESS_ID>"
	// This should be the base64 encoded content of your public certificate
	certPem, err := os.ReadFile("<YOUR_CERT_PATH>")
	if err != nil {
		log.Fatalf("failed to read certificate file: %v", err)
	}
	certData := base64.StdEncoding.EncodeToString(certPem)

	getChallengeBody := akeyless.NewGetCertChallenge()
	getChallengeBody.AccessId = &accessID
	getChallengeBody.CertData = &certData

	fmt.Println("Getting challenge...")
	challengeResult, _, err := client.GetCertChallenge(ctx).Body(*getChallengeBody).Execute()
	if err != nil {
		log.Fatalf("Failed to get challenge: %v\n", err)
	}
	fmt.Println("Received challenge!")

	challenge := challengeResult.Challenge

	// --- Step 3: Sign the Challenge ---
	// Replace with the path to your private key file
	keyFilePath := "<YOUR_KEY_PATH>"

	signedChallenge, err := signChallengeWithPrivateKey(keyFilePath, *challenge)
	if err != nil {
		log.Fatalf("Failed to sign challenge: %v", err)
	}
	fmt.Println("Challenge signed successfully!")

	// --- Step 4: Authenticate with Signed Challenge ---
	authBody := akeyless.NewAuth()
	authBody.SetAccessType("cert")
	authBody.SetAccessId(accessID)
	authBody.SetCertData(certData)
	authBody.SetCertChallenge(*challenge)
	authBody.SetSignedCertChallenge(signedChallenge)

	fmt.Println("Authenticating with signed challenge...")
	authResult, _, err := client.Auth(ctx).Body(*authBody).Execute()
	if err != nil {
		log.Fatalf("Failed to authenticate with signed challenge: %v\n", err)
	}

	fmt.Printf("Authentication successful! Token: %s\n", *authResult.Token)
}

func signChallengeWithPrivateKey(keyFilePath, challengeB64 string) (string, error) {
	// Read the private key file
	keyFileBytes, err := os.ReadFile(keyFilePath)
	if err != nil {
		return "", fmt.Errorf("failed to read private key file: %w", err)
	}

	// Parse key like the app
	parsedKey, err := parsePrivateKeyForSigning(keyFileBytes)
	if err != nil {
		return "", err
	}

	// Decode the base64 challenge
	challengeBytes, err := base64.StdEncoding.DecodeString(challengeB64)
	if err != nil {
		return "", fmt.Errorf("failed to decode challenge: %w", err)
	}

	// Hash the challenge before signing
	h := sha256.Sum256(challengeBytes)
	var sig []byte

	if rsaKey, ok := asRSA(parsedKey); ok {
		// App uses RSA with SHA-256 and PKCS#1 v1.5 in std path
		sig, err = rsa.SignPKCS1v15(rand.Reader, rsaKey, crypto.SHA256, h[:])
		if err != nil {
			return "", fmt.Errorf("rsa sign failed: %w", err)
		}
		return base64.StdEncoding.EncodeToString(sig), nil
	}
	if ecKey, ok := asECDSA(parsedKey); ok {
		sig, err = ecdsa.SignASN1(rand.Reader, ecKey, h[:])
		if err != nil {
			return "", fmt.Errorf("ecdsa sign failed: %w", err)
		}
		return base64.StdEncoding.EncodeToString(sig), nil
	}

	return "", fmt.Errorf("unsupported private key type for signing")
}
```
```go sing_key_parse.go
package main

import (
	"crypto/ecdsa"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"fmt"

	"golang.org/x/crypto/ssh"
)

// parsePrivateKeyForSigning tries multiple key formats similarly to the app’s logic.
// It supports OpenSSH, PKCS#8, PKCS#1 (RSA), and EC private keys.
func parsePrivateKeyForSigning(keyBytes []byte) (interface{}, error) {
	// Try OpenSSH / raw first
	if k, err := ssh.ParseRawPrivateKey(keyBytes); err == nil {
		return k, nil
	}

	// Fallback to PEM
	pemBlock, _ := pem.Decode(keyBytes)
	if pemBlock == nil {
		return nil, fmt.Errorf("failed to decode PEM private key")
	}

	if k, err := x509.ParsePKCS8PrivateKey(pemBlock.Bytes); err == nil {
		return k, nil
	}
	if k, err := x509.ParsePKCS1PrivateKey(pemBlock.Bytes); err == nil {
		return k, nil
	}
	if k, err := x509.ParseECPrivateKey(pemBlock.Bytes); err == nil {
		return k, nil
	}

	return nil, fmt.Errorf("unsupported or unrecognized private key format")
}

// helpers to assert types without importing in playground.go
func asRSA(k interface{}) (*rsa.PrivateKey, bool)     { v, ok := k.(*rsa.PrivateKey); return v, ok }
func asECDSA(k interface{}) (*ecdsa.PrivateKey, bool) { v, ok := k.(*ecdsa.PrivateKey); return v, ok }

```
```csharp
using System.Security.Cryptography;
using akeyless.Model;
using akeyless.Client;

namespace Playground
{
  internal static class Program
  {
    public static void Main(string[] args)
    {
      // 1) Configure SDK client (gateway URL)
      var gatewayUrl = "https//:<Akeyless-GW-URL>/api/v2"; 
      var accessId   = "<YOUR_ACCESS_ID>"; 

      // Paths to your cert and key
      var certPath   = "<YOUR_CERT_PATH>";
      var keyPath    = "<YOUR_KEY_PATH>";

      var cfg = new Configuration
      {
        BasePath = gatewayUrl
      };

      var api = new akeyless.Api.V2Api(cfg);

      try
      {
        // 2) Read certificate and base64-encode it
        var certBytes = File.ReadAllBytes(certPath);
        var certB64   = Convert.ToBase64String(certBytes);

        // 3) Get challenge
        var chalOut = api.GetCertChallenge(new GetCertChallenge
        {
          AccessId = accessId,
          CertData = certB64
        });
        var challengeB64 = chalOut.Challenge ?? throw new InvalidOperationException("Challenge is empty");

        // 4) Read private key PEM and sign the challenge with SHA-256
        var signedB64 = SignChallengeWithPem(keyPath, challengeB64);

        // 5) Authenticate with signed challenge
        var authOut = api.Auth(new Auth
        {
          AccessType           = "cert",
          AccessId             = accessId,
          CertData             = certB64,
          CertChallenge        = challengeB64,
          SignedCertChallenge  = signedB64
        });

        Console.WriteLine($"Token: {authOut.Token}");
      }
      catch (ApiException ex)
      {
        Console.Error.WriteLine($"API Error: {ex.Message}");
        if (!string.IsNullOrEmpty(ex.ErrorContent.ToString()))
        {
          Console.Error.WriteLine(ex.ErrorContent);
        }
        else if (!string.IsNullOrEmpty(ex.Message))
        {
          Console.Error.WriteLine(ex.Message);
        }
        
        Environment.Exit(1);
      }
      catch (Exception ex)
      {
        Console.Error.WriteLine($"Error: {ex.Message}");
        Environment.Exit(1);
      }
    }

    // Signs the base64-encoded challenge using the PEM private key (RSA or ECDSA).
    // - RSA: SHA-256 with PKCS#1 v1.5 (matches app default path)
    // - ECDSA: SHA-256 DER (ASN.1) signature
    private static string SignChallengeWithPem(string keyPath, string challengeB64)
    {
      var pem = File.ReadAllText(keyPath);
      var challenge = Convert.FromBase64String(challengeB64);

      // Try ECDSA first; if that fails, fallback to RSA
      if (TrySignEcdsa(pem, challenge, out var sigEcdsaB64))
        return sigEcdsaB64;

      if (TrySignRsa(pem, challenge, out var sigRsaB64))
        return sigRsaB64;

      throw new InvalidOperationException("Unsupported or unrecognized private key format. Convert to PKCS#8 if needed.");
    }

    private static bool TrySignEcdsa(string pem, byte[] data, out string signatureB64)
    {
      signatureB64 = string.Empty;
      try
      {
        using var ecdsa = ECDsa.Create();
        ecdsa.ImportFromPem(pem);
        var sig = ecdsa.SignData(data, HashAlgorithmName.SHA256);
        signatureB64 = Convert.ToBase64String(sig);
        return true;
      }
      catch
      {
        return false;
      }
    }

    private static bool TrySignRsa(string pem, byte[] data, out string signatureB64)
    {
      signatureB64 = string.Empty;
      try
      {
        using var rsa = RSA.Create();
        rsa.ImportFromPem(pem);
        // SHA-256 + PKCS#1 v1.5 (aligns with app std path)
        var sig = rsa.SignData(data, HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
        signatureB64 = Convert.ToBase64String(sig);
        return true;
      }
      catch
      {
        return false;
      }
    }
  }
}
```
```python
import base64
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, ec, rsa
from cryptography.hazmat.backends import default_backend

import akeyless
from akeyless.rest import ApiException


def load_private_key(pem_path: str):
    pem = Path(pem_path).read_bytes()
    return serialization.load_pem_private_key(pem, password=None, backend=default_backend())


def sign_challenge(priv_key, challenge_bytes: bytes) -> bytes:
    # Hash is SHA-256 in both cases
    if isinstance(priv_key, rsa.RSAPrivateKey):
        return priv_key.sign(
            challenge_bytes,
            padding.PKCS1v15(),  # matches app’s standard path
            hashes.SHA256(),
        )
    elif isinstance(priv_key, ec.EllipticCurvePrivateKey):
        return priv_key.sign(
            challenge_bytes,
            ec.ECDSA(hashes.SHA256()),  # ASN.1 DER signature
        )
    else:
        raise ValueError("Unsupported private key type (use RSA or EC)")


def main():
    # Required inputs
    gateway_url = "https//:<Akeyless-GW-URL>/api/v2"; #  set your Gateway URL, e.g. https://<gateway_url>:8081
    access_id = "<AccessID>" 
    cert_path = "<YOUR_CERT_PATH>"
    key_path = "<YOUR_KEY_PATH>"

    # 1) SDK client
    cfg = akeyless.Configuration()
    cfg.host = gateway_url
    api = akeyless.V2Api(akeyless.ApiClient(cfg))

    try:
        # 2) Read certificate and base64-encode it
        cert_b64 = base64.b64encode(Path(cert_path).read_bytes()).decode("ascii")

        # 3) Get challenge
        chal_body = akeyless.GetCertChallenge(access_id=access_id, cert_data=cert_b64)
        chal_out = api.get_cert_challenge(chal_body)
        challenge_b64 = chal_out.challenge
        if not challenge_b64:
            raise RuntimeError("Empty challenge received")

        # 4) Load key and sign the challenge (SHA-256, RSA PKCS#1 v1.5 or ECDSA)
        priv_key = load_private_key(key_path)
        challenge_bytes = base64.b64decode(challenge_b64)
        signature = sign_challenge(priv_key, challenge_bytes)
        signed_b64 = base64.b64encode(signature).decode("ascii")

        # 5) Authenticate with signed challenge
        auth_body = akeyless.Auth(
            access_type="cert",
            access_id=access_id,
            cert_data=cert_b64,
            cert_challenge=challenge_b64,
            signed_cert_challenge=signed_b64,
        )
        auth_out = api.auth(auth_body)
        print(f"Token: {auth_out.token}")

    except ApiException as e:
        print(f"API error: {e}")
        if e.body:
            print(e.body)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
```

Upon success, an authentication token will be provided.
