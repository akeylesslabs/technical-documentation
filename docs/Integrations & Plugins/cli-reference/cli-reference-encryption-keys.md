---
title: CLI Reference - Encryption Keys
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
This section outlines the CLI commands relevant to Encryption Keys.

General Flags:

`--profile, --token`:  Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

### <p style="color:blue">_assoc-target-item_</p>

Create an association between a [Target](doc:targets) and a [Classic Key](doc:classic-keys) for [External KMS Integration](doc:external-kms) 

##### Usage

```shell
akeyless assoc-target-item \
--target-name <Target to associate> \
--name <Item to associate> \
--vault-name <Name of the vault used> \
--key-operations <A list of allowed operations for the key> \
--project-id <Project id of the GCP KMS> \
--location-id <Location id of the GCP KMS> \
--keyring-name <Keyring name of the GCP KMS> \
--purpose <Purpose if the key in GCP KMS>
```

#### Flags

 `-t, --target-name`: **Required**, The target to associate                                                                                                                                                                 

 `-n, --name`: **Required**, The item to associate                                                                                                                                                                   

 `--vault-name`: Name of the vault used. (Relevant only for Classic Key and target association. Required for azure targets)                                                                                              

 `--key-operations`: A list of allowed operations for the key. (Relevant only for Classic Key and target association. Required for azure targets)                                                                            

 `--project-id`: Project id of the GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)                                                                                             

 `--location-id`: Location id of the GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)                                                                                            

 `--keyring-name`: Keyring name of the GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)                                                                                           

 `--purpose`: Purpose if the key in GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)                                                                                         

 `--kms-algorithm`: Algorithm of the key in GCP KMS. (Relevant only for Classic Key and target association, Required for gcp targets)                                                                                       

 `--tenant-secret-type`: Set to 'true' to create a multi-region managed key. (Relevant only for Classic Key AWS targets)                                                                                                         

 `--multi-region[=false]`: The list of regions in which to create a copy of the key. (Relevant only for Classic Key AWS targets). To specify multiple regions use argument multiple times: --regions us-east-1 --regions us-west-1 

 `--protection-level[=software]`: Protection level of the key [software/hardware]. (Relevant only for Classic Key and target association, for gcp targets)

### <p style="color:blue">_create-classic-key_</p>

Creates a new Classic Key in the current account

##### Usage

```shell
akeyless create-classic-key \
--name <Key Name> \
--alg <Key type> \
--gateway-url <API Gateway URL:8000> \
--generate-self-signed-certificate <True/False> \
--certificate-ttl <Certificate TTL> \
--certificate-common-name <Certificate common name> 
--certificate-format <pem / der>
```

##### Flags

 `-n, --name`: **Required**,  Classic key name/path.                                                                                                  

 `-a, --alg `: **Required**, Key type; options: `[AES128GCM, AES256GCM, AES128SIV, AES256SIV, RSA1024, RSA2048, RSA3072, RSA4096, EC256, EC384, GPG]` 

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)                                                                                          

 `-p, --key-file-path `: Path to file with the classic key value provided by user                                                                                 

 `--key-data`: Base64-encoded classic key value provided by user                                                                                        

 `-c, --cert`: Path to a file that contain the certificate in a PEM format.                                                                             

 `--cert-file-data`: PEM Certificate in a Base64 format.                                                                                                      

 `--gpg-alg`: gpg alg: Relevant only if GPG key type selected; options: [RSA1024, RSA2048, RSA3072, RSA4096, Ed25519]                                  

 `-k, --protection-key-name`: The name of the key that protects the classic key value (if empty, the account default key will be used)                                 

 `--generate-self-signed-certificate[=false]`: Whether to generate a self signed certificate with the key. If set, `--certificate-ttl` must be provided.                                

 `--certificate-ttl`: TTL in days for the generated certificate. Required only for generate-self-signed-certificate.                                           

 `--certificate-common-name`: Common name for the generated certificate. Relevant only for generate-self-signed-certificate.                                           

`--cerificate-format`: The format of the returned certificate can be `pem` or `der`

 `--certificate-organization`: Organization name for the generated certificate. Relevant only for generate-self-signed-certificate.                                     

 `--certificate-country`: Country name for the generated certificate. Relevant only for generate-self-signed-certificate.                                          

 `--certificate-locality`: Locality for the generated certificate. Relevant only for generate-self-signed-certificate.                                              

 `--certificate-province`: Province name for the generated certificate. Relevant only for generate-self-signed-certificate.                                         

 `--hash-algorithm[=SHA256]`: Specifies the hash algorithm used for the encryption key's operations, available options: [`SHA256`, `SHA384`, `SHA512`] \(only for RSA and EC keys)

 `--conf-file-path`: Path to the configuration file that contains csr config data                                                                             

 `--conf-file-data`: The csr config data in base64 encoding

`--certificate-format` : The format of the returned certificate can be pem or der.

`-e, --expiration-event-in` : How many days before the expiration of the certificate would you like to be notified. To specify multiple events, use argument multiple times: `--expiration-event-in 1 --expiration-event-in 5`

`--auto-rotate`: Whether to automatically rotate every --rotation-interval days, or disable existing automatic rotation [true/false]

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365)

`--rotation-event-in`: How many days before the rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

 `-t, --tag`: List of the tags attached to this secret. To specify multiple tags use argument multiple times: -t Tag1 -t Tag2                          

 `--delete-protection`: Protection from accidental deletion of this item, [true/false]

### <p style="color:blue">_create-dfc-key_</p>

Creates a new DFC key in the current account

##### Usage

```shell
akeyless create-dfc-key \
--name <Key name> \
--alg <Key type> \
--generate-self-signed-certificate <True/False> \
--certificate-ttl <Certificate TTL> \
--certificate-common-name <Certificate common name> 
--certificate-format <pem / der>
```

##### Flags

 `-n, --name`: **Required**,  DFCKey name                                                                                                                 

 `-a, --alg`: **Required**, DFCKey type; options: [AES128GCM, AES256GCM, AES128SIV, AES256SIV, AES128CBC, AES256CBC, RSA1024, RSA2048, RSA3072, RSA4096] 

 `-t, --tag`: List of the tags attached to this DFC key. To specify multiple tags use the argument multiple times: -t Tag1 -t Tag2                         

 `-s, --split-level[=3]`: The number of fragments that the item will be split into (not includes customer fragment)                                                    

 `-f, --customer-frg-id`: The customer fragment ID that will be used to create the DFC key (if empty, the key will be created independently of a customer fragment)    

 `--generate-self-signed-certificate[=false]`: Whether to generate a self signed certificate with the key. If set, `--certificate-ttl` must be provided.                                    

 `--certificate-ttl`: TTL in days for the generated certificate. Required only for generate-self-signed-certificate.                                               

 `--certificate-common-name`: Common name for the generated certificate. Relevant only for generate-self-signed-certificate.                                               

`--cerificate-format`: The format of the returned certificate can be `pem` or `der`

 `--certificate-organization`: Organization name for the generated certificate. Relevant only for generate-self-signed-certificate.                                         

 `--certificate-country`: Country name for the generated certificate. Relevant only for generate-self-signed-certificate.                                              

 `--certificate-locality`: Locality for the generated certificate. Relevant only for generate-self-signed-certificate.                                                  

 `--certificate-province`: Province name for the generated certificate. Relevant only for generate-self-signed-certificate.          

 `--hash-algorithm[=SHA256]`: Specifies the hash algorithm used for the encryption key's operations, available options: [`SHA256`, `SHA384`, `SHA512`] \(only for **RSA** keys)

 `--conf-file-path`: Path to the configuration file that contains csr config data                                                                                 

 `--conf-file-data`: The csr config data in base64 encoding

`--certificate-format` : The format of the returned certificate can be pem or der.

`-e, --expiration-event-in` : How many days before the expiration of the certificate would you like to be notified. To specify multiple events, use argument multiple times: `--expiration-event-in 1 --expiration-event-in 5`

`--auto-rotate`: Whether to automatically rotate every --rotation-interval days, or disable existing automatic rotation [true/false]

`--rotation-interval`: The number of days to wait between every automatic rotation (1-365)

`--rotation-event-in`: How many days before the rotation of the item would you like to be notified. To specify multiple events, use argument multiple times: `--rotation-event-in 1 --rotation-event-in 5`

 `--delete-protection`: Protection from accidental deletion of this item, [true/false]                                                                               

### <p style="color:blue">_decrypt_</p>

Decrypts ciphertext into plaintext by using an AES key

##### Usage

```shell
akeyless decrypt \
--key-name <Key Name> \
--display-id <Display id of the key> \
--item-id <Item id of the key>
```

##### Flags

 `-k, --key-name`: **Required**, The name of the key to use in the decryption process.                                                                 

 `-d, --display-id`: The display id of the key to use in the decryption process                                                                            

 `-I, --item-id`: The item id of the key to use in the decryption process                                                                               

 `-i, --in`: Path to the file to be decrypted (base64 encoded)                                                                                     

 `-o, --out`: Path to the output file. If not provided, the output will be printed as text.                                                         

 `-c, --ciphertext`: Ciphertext to be decrypted in base64 encoded format, if a file was not provided                                                       

 `-X, --encryption-context`: The encryption context. If this was specified in the encrypt command, it must be specified here or the decryption operation will fail 

 `-F, --output-format`: If specified, the output will be formatted accordingly. options: [base64]                                                             

### <p style="color:blue">_decrypt-file_</p>

Decrypts a file by using an AES key

##### Usage

```shell
akeyless decrypt-file \
--key-name <key name> \
--in <file to decrypt> \
--out <Path to the output file> \
--display-id <Display id of the key to use in the decryption process> \ 
--item-id <Item id of the key to use in the encryption process>
```

##### Flags

 `--key-name`: **Required**, The name of the key to use in the decryption process                                                                  

 `-d, --display-id`: The display id of the key to use in the decryption process                                                                            

 `-I, --item-id`: The item id of the key to use in the decryption process                                                                               

 `-i, --in`: Path to the file to be decrypted. If not provided, the content will be taken from stdin                                               

 `-o, --out`: Path to the output file. If not provided, the output will be sent to stdout                                                           

 `-F, --output-format[=base64]`: The output will be formatted accordingly. options: [base64, raw]                                                                      

 `-X, --encryption-context`: The encryption context. If this was specified in the encrypt command, it must be specified here or the decryption operation will fail 

`-v, --version`: key version (relevant only for classic key)

### <p style="color:blue">_decrypt-gpg_</p>

Decrypts the given GPG message using an RSA key

##### Usage

```shell
akeyless decrypt-gpg \
--key-name <Key Name> \
--display-id <Display id of the key> \
--item-id <Item id of the key>
```

##### Flags

 `-k, --key-name`: **Required**, The name of the key to use in the decryption process.           

 `-d, --display-id`: The display id of the key to use in the decryption process                      

 `-I, --item-id`: The item id of the key to use in the decryption process                         

 `-i, --in`: Path to the file to be decrypted (base64 encoded)                               

 `-o, --out`: Path to the output file. If not provided, the output will be printed as text.   

 `-c, --ciphertext`: Ciphertext to be decrypted in base64 encoded format, if a file was not provided 

 `-N, --input-format[=base64]`: Select default assumed format for the ciphertext. Currently supported options: [base64,raw]

 `-p, --passphrase`: Passphrase to decrypt the message                                               

 `-F, --output-format`: If specified, the output will be formatted accordingly. options: [base64]

### <p style="color:blue">_decrypt-pkcs1_</p>

Decrypts a plaintext using RSA and the padding scheme from PKCS#1 v1.5

##### Usage

```shell
akeyless decrypt-pkcs1 \
--key-name <Key Name> \
--ciphertext <Ciphertxt to decrypt> \
--display-id <Display id of the key> \ 
--item-id <Item id of the key>
```

##### Flags

 `-k, --key-name`: **Required**, The name of the key to use in the decryption process      

 `-d, --display-id`: The display id of the key to use in the decryption process                

 `-I, --item-id`: The item id of the key to use in the decryption process                   

 `-c, --ciphertext`: **Required**, Ciphertext to be decrypted in base64 encoded format       

 `-F, --output-format`: If specified, the output will be formatted accordingly. options: [base64]

### <p style="color:blue">_encrypt_</p>

Encrypts plaintext into ciphertext by using an AES key

##### Usage

```shell
akeyless encrypt \
--key-name <Key name> \
--display-id <Display id of the key to use in the encryption process \
--item-id <Item id of the key to use in the encryption process> \
--in <Path to the file to be encrypted in base64 format> 
```

##### Flags

 `-k, --key-name`: The name of the key to use in the encryption process                                                                                                                                        

 `-d, --display-id`: The display id of the key to use in the encryption process                                                                                                                                  

 `-I, --item-id`: The item id of the key to use in the encryption process                                                                                                                                     

 `-i, --in`: Path to the file to be encrypted in base64 format                                                                                                                                           

 `-o, --out`: Path to the output file. If not provided, the output will be printed as base64                                                                                                              

 `-p, --plaintext`: Data to be encrypted, if a file was not provided                                                                                                                                            

 `-X, --encryption-context`: name-value pair that specifies the encryption context to be used for authenticated encryption. If used here, the same value must be supplied to the decrypt command or decryption will fail 

 `-F, --input-format`: If specified, the plaintext input is assumed to be formatted accordingly. Current supported options: [base64]                                                                               

### <p style="color:blue">_encrypt-file_</p>

Encrypts a file by using an AES key

##### Usage

```shell
akeyless encrypt-file \
--key-name <Key Name> \
--in <File to be encrypted> \ 
--out <Output file> \
--display-id <Display id of the key> 
```

##### Flags

 `-k, --key-name`: **Required**, The name of the key to use in the encryption process                                                                                                                        

 `-d, --display-id`: The display id of the key to use in the encryption process                                                                                                                                  

 `-I, --item-id`: The item id of the key to use in the encryption process                                                                                                                                     

 `-i, --in`: **Required**, Path to the file to be encrypted. If not provided, the content will be taken from stdin                                                                                     

 `-o, --out`: **Required**, Path to the output file. If not provided, the output will be sent to stdout                                                                                                 

 `-F, --output-format[=base64]`: The output will be formatted accordingly. options: [base64, raw]                                                                                                                            

 `-X, --encryption-context`: name-value pair that specifies the encryption context to be used for authenticated encryption. If used here, the same value must be supplied to the decrypt command or decryption will fail

### <p style="color:blue">_encrypt-gpg_</p>

Encrypts the given message with GPG using an RSA key

##### Usage

```shell
akeyless encrypt-gpg \
--key-name <Key name> \
--display-id <Display id of the key> \
--item-id <Item id of the key> \
--in <Path to the file to be encrypted in base64 format> 
```

##### Flags

 `-k, --key-name`: **Required**, The name of the key to use in the encryption process                                          

 `-d, --display-id`: The display id of the key to use in the encryption process                                                    

 `-I, --item-id`: The item id of the key to use in the encryption process                                                       

 `-i, --in`: Path to the file to be encrypted in base64 format                                                             

 `-o, --out`: Path to the output file. If not provided, the output will be printed as base64                                

 `-p, --plaintext`: Data to be encrypted, if a file was not provided                                                              

 `-F, --input-format`: If specified, the plaintext input is assumed to be formatted accordingly. Current supported options: [base64] 

### <p style="color:blue">_encrypt-pkcs1_</p>

Encrypts the given message with RSA and the padding scheme from PKCS#1 v1.5

##### Usage

```shell
akeyless encrypt-pkcs1 \
--key-name <key Name> \
--plaintext <Data to encrypt> \
--display-id <Display id of the key> \
--item-id <Item id of the key>
```

##### Flags

 `-k, --key-name`: **Required**,The name of the key to use in the encryption process                 

 `-d, --display-id`: The display id of the key to use in the encryption process                          

 `-I, --item-id`: The item id of the key to use in the encryption process                             

 `-p, --plaintext`: **Required**, Data to be encrypted 

### <p style="color:blue">_export-classic-key_</p>

Returns the Classic Key material

##### Usage

```shell
akeyless export-classic-key \
--name <Key name> \
--version <Key version> \
--gateway-url <API Gateway URL:8000> 
```

#### Flags

 `-n, --name`: **Required**, Classic key name                                                                                  

 `-v, --version`: Classic key version                                                                                               

 `--export-public-key[=false]`: Export only the public key                                                                                        

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)                                                                   

 `--ignore-cache[=false]`: Retrieve the Secret value without checking the Gateway's cache. This flag is only relevant when using the RestAPI 

 `--wrapping-key-name`: Classic key name to wrap the key material with. This feature enables users to specify the name of a Key Encryption Key (KEK) to encrypt a Data Encryption Key (DEK) during the export process.

### <p style="color:blue">_gateway-download-customer-fragments_</p>

Download gateway customer fragments

##### Usage

```shell
akeyless gateway-download-customer-fragments \
--file-folder <path to download to> \
--gateway-url <API Gateway URL:8000>
```

### <p style="color:blue">_gen-customer-fragment_</p>

Generates Customer Fragment

##### Usage

```shell
akeyless gen-customer-fragment \
--name <CF-Name> \
--type <standard/hsm_wrapped/hsm_secured> \
--hsm-key-label <Key-1> \
--description <Customer Fragment Description>
```

##### Flags

`-n, --name`: Customer Fragment name

`-t, --type[=standard]`: Customer fragment type [`standard`/`hsm_wrapped`/`hsm_secured`]

`-k, --hsm-key-label`:  The label of the hsm key to use for customer fragment operations (relevant for `hsm_wrapped`/`hsm_secured` customer fragments)

### <p style="color:blue">_get-rsa-public_</p>

Obtain the public key from a specific RSA private key

##### Usage

```shell
akeyless get-rsa-public --name <Key name>
```

##### Flags

 `-n, --name`: **Required**, Name of RSA key to extract the public key from 

### <p style="color:blue">_hmac_</p>

Generates a hash-based message authentication code (HMAC) for a message, using an HMAC algorithm

##### Usage

```shell
akeyless hmac \
--key-name <Key name> \
--display-id <Display id of the key> \ 
--item-id <Item id of the key>
```

##### Flags

 `-k, --key-name`: **Required**, The name of the key to use in the encryption process                             

 `-d, --display-id`: The display id of the key to use in the encryption process                                       

 `-I, --item-id`: The item id of the key to use in the encryption process                                          

 `-i, --in`: Path to the input file                                                                           

 `-o, --out`: Path to the output file. If not provided, the output will be printed as base64                   

 `-p, --plaintext`: Data to perform hmac on, if a file was not provided                                              

 `-f, --hash-function[=sha-256]`: Hash function `sha-256`,`sha-512`                                                                  

 `-F, --input-format`: Select the default assumed format for any plaintext input. Currently supported options: \[base64]

### <p style="color:blue">_refresh-key_</p>

Refresh a key in the current account

##### Usage

```shell
akeyless refresh-key --name <Key name>
```

#### Flags

 `-n, --name`: **Required**, Key name

### <p style="color:blue">_rotate-key_</p>

Rotates an existing key, by creating a new version of the key

##### Usage

```shell
akeyless rotate-key \
--name <Key name> \
--gateway-url <API Gateway URL:8000> \ 
--new-key-data <The new value of the key, base64 encoded>
```

##### Flags

 `-n, --name`: **Required**, Key name                                                                             

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port). Relevant only for Classic Key.                      

 `--new-key-data`: The new value of the key, base64 encoded. Relevant only for Classic Key provided by the user (BYOK). 

### <p style="color:blue">_set-item-state_</p>

Set an item's state (Enabled, Disabled)

##### Usage

```shell
akeyless set-item-state \
--name <Item name> \
--desired-state [Enabled, Disabled]
```

##### Flags

 `-n, --name`: **Required**, Current item name                                    

 `-s, --desired-state`: **Required**, Desired item state [Enabled, Disabled]                

 `--version[=0]`: The specific version you want to update: 0=item level state (default)

### <p style="color:blue">_sign-ecdsa_</p>

Calculates the signature of a given message using ECDSA and a sha hash algorithm matching the key size

###### Usage

```shell
akeyless sign-ecdsa \
--message <Input message> \
--key-name <Key name> \
--display-id <Display id of the RSA key> \
--item-id <Item id of the RSA key>
```

##### Flags

 `-k, --key-name`: The name of the EC key to use for the signing process        

 `-d, --display-id`: The display id of the EC key to use for the signing process  

 `-I, --item-id`: The item id of the key EC to use for the signing process

 `--version`: The version of the key to use for signing

 `--prehashed`: Markes that the message is already hashed

`-m, --message`: (**Mandatory**) The input message to sign in a base64 format

### <p style="color:blue">_sign-gpg_</p>

Calculates the signature of a message using GPG from an RSA key

##### Usage

```shell
akeyless sign-gpg \
--key-name <RSA key> \
--message <Message to sign> \
--display-id <Display id of the key> \
--item-id <Item id of the key>
```

##### Flags

 `-k, --key-name`: **Required**, The name of the RSA key to use in the signing process 

 `-d, --display-id`: The display id of the key to use in the signing process               

 `-I, --item-id`: The item id of the key to use in the signing process                  

 `-m, --message`: **Required**, The message to be signed                              

 `-p, --passphrase`: Passphrase to decrypt the message

### <p style="color:blue">_sign-pkcs1_</p>

Calculates the signature of hashed using RSASSA-PKCS1-V1_5-SIGN from RSA PKCS#1 v1.5

##### Usage

```shell
akeyless sign-pkcs1 \
--key-name <RSA key > \
--message <Message to sign> \
--display-id <Display id of the key> \
--item-id <Item id of the key>
```

##### Flags

 `-k, --key-name`: **Required**, The name of the RSA key to use in the signing process               

 `-d, --display-id`: The display id of the key to use in the signing process                             

 `-I, --item-id`: The item id of the key to use in the signing process

 `--version`: The version of the key to use for signing

 `-f, --hash-function[=sha-256]`: Hash function [sha-256,sha-384,sha-512]

 `--prehashed`: Markes that the message is already hashed

 `-F, --input-format`: Select default assumed format for the message input. Currently supported options: [base64]

 `-m, --message`: **Required**, The message to be signed

### <p style="color:blue">_sign-rsassa-pss_</p>

Calculates the signature of a given message using rsassa-pss

###### Usage

```shell
akeyless sign-rsassa-pss \
--message <Input message> \
--key-name <Key name> \
--display-id <Display id of the RSA key> \
--item-id <Item id of the RSA key>
```

##### Flags

 `-k, --key-name`: The name of the RSA key to use for the signing process       

 `-d, --display-id`: The display id of the RSA key to use for the signing process 

 `-I, --item-id`: The item id of the RSA key to use for the signing process    

 `--version`: The version of the key to use for signing 

`-f, --hash-function[=sha-256]`: Hash function `sha-256`,`sha-384`,`sha-512`                       

`-m, --message`: (**Mandatory**) The input message to sign in a base64 format 

 `--prehashed`: Markes that the message is already hashed

### <p style="color:blue">_update-classic-key-certificate_</p>

Update the certificate for a classic key

##### Usage

```shell
akeyless update-classic-key-certificate \
--name <Classic key name> \
--gateway-url <API Gateway URL:8000> \
--cert-file-path <path/to/cert/file> \
--cert-file-data <PEM Certificate in a Base64 format>
```

##### Flags

 `-n, --name`: (**Mandatory**) Classic key name                             

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)              

 `-c, --cert-file-path`: Path to a file that contains the certificate in a PEM format 

 `--cert-file-data`: PEM Certificate in a Base64 format                           

 `--certificate-format`: The format of the returned certificate [`pem`/`der`]

### <p style="color:blue">_update-rotation-settings_</p>

Updates rotation settings of an existing key

##### Usage

```shell
akeyless update-rotation-settings \
--name <Key name> \
--auto-rotate <True/False> 
```

#### Flags

 `-n, --name`: **Required**, Key name                                                                                                                                        

 `-r, --auto-rotate[=false]`: **Required**, [true/false] Sets automatic rotation to be enabled or disabled, if enabled rotation will be triggered periodically based on --rotation-interval 

 `--rotation-interval`: The number of days to wait between every automatic key rotation (7-365)  

`--rotation-event-in `: How many days before the rotation of the item would you like to be notified. To specify multiple events, use argument multiple times:`--rotation-event-in 1 --rotation-event-in 5`

### <p style="color:blue">_upload-pkcs12_</p>

Upload a PKCS#12 key and certificates

##### Usage

```shell
akeyless upload-pkcs12 \
--name <Key name> \
--in <Input file (private key and certificate only>  \
--passphrase <Passphrase> \
--description <Key description> 
```

##### Flags

 `-n, --name`: **Required**, Name of key to be created                                                                                                                                

 `-i, --in`: **Required**, PKCS#12 input file (private key and certificate only)                                                                                                    

 `-p, --passphrase`: **Required**, Passphrase to unlock the pkcs#12 bundle                                                                                                                  

 `--description`: Key description                                                                                                                                                          

 `-t, --tag`: List of the tags attached to this key. To specify multiple tags use argument multiple times: -t Tag1 -t Tag2                                                             

 `-s, --split-level[=2]`: The number of fragments that the item will be split into                                                                                                                 

 `-f, --customer-frg-id`: The customer fragment ID that will be used to split the key (if empty, the key will be created independently of a customer fragment)                                     

 `-c, --cert`: Path to a file that contain the certificate in a PEM format. If this  is not empty, the certificate will be taken from here and not from the PKCS#12 input file 

 `--delete-protection[=false]`: Protection from accidental deletion of this item, [true/false]                                                                                                           

### <p style="color:blue">_upload-rsa_</p>

Upload RSA key

##### Usage

```shell
akeyless upload-rsa \
--name <Key Name> \
--alg <Key type> \
--rsa-key-file-path <RSA private key file path> \
--rsa-key-data <RSA private key data, base64 encoded> \
--cert <Certificate in a PEM format> \
--cert-file-data <PEM Certificate in a Base64 format>
```

##### Flags

 `-n, --name`: **Required**, Name of key to be created                                                                                            

 `-a, --alg`: **Required**, Key type. options: [RSA1024, RSA2048, RSA3072, RSA4096]                                                              

 `-p, --rsa-key-file-path`: RSA private key file path.                                                                                                           

 `--rsa-key-data`: RSA private key data, base64 encoded                                                                                                 

 `-c, --cert`: Path to a file that contain the certificate in a PEM format                                                                          

 `--cert-file-data`: PEM Certificate in a Base64 format                                                                                                   

 `--description`: Key description                                                                                                                      

 `-t, --tag`: List of the tags attached to this key. To specify multiple tags use argument multiple times: -t Tag1 -t Tag2                         

 `-s, --split-level[=2]`: The number of fragments that the item will be split into                                                                             

 `-f, --customer-frg-id`: The customer fragment ID that will be used to split the key (if empty, the key will be created independently of a customer fragment) 

 `--overwrite[=false]`: When the overwrite flag is set, this command will only update an existing key. [true, false]                                         

 `--delete-protection`: Protection from accidental deletion of this item, [true/false]                                                                       

### <p style="color:blue">_verify-ecdsa_</p>

Verifies an ECDSA signature using a sha hash algorithm matching the key size

###### Usage

```shell
akeyless verify-rsassa-pss \
--message <Input message> \
--signature <messages signature> \
--key-name <Key name> \
--display-id <Display id of the RSA key> \
--item-id <Item id of the RSA key>
```

##### Flags

 `-k, --key-name`: The name of the EC key to use for the verification process       

 `-d, --display-id`: The display id of the key EC to use for the verification process 

 `-I, --item-id`: The item id of the EC key to use for the verification process    

 `-m, --message`: (**Mandatory**) The input message to sign in a base64 format     

 `-s, --signature`: (**Mandatory**) The message's signature     

### <p style="color:blue">_verify-gpg_</p>

Verifies a GPG based on RSA signature

##### Usage

```shell
akeyless verify-gpg \
--key-name <RSA Key> \
--signature <message signature> \ 
--message <message to verify> \
--display-id <Display id of the key> \ 
--item-id <Item id of the key>
```

##### Flags

 `-k, --key-name`: The name of the RSA key to use in the verification process   

 `-d, --display-id`: The display id of the key to use in the verification process 

 `-I, --item-id`: The item id of the key to use in the verification process    

 `-m, --message`: **Required**, The message to be verified.                  

 `-s, --signature`: **Required**, The message's signature.                     

 `-p, --passphrase`: Passphrase to decrypt the message

### <p style="color:blue">_verify-pkcs1_</p>

Verifies an RSA PKCS#1 v1.5 signature

##### Usage

```shell
akeyless verify-pkcs1 \
--key-name <RSA Key> \
--message <message to verify> \
--signature <message signature> \ 
--display-id <Display id of the key> \ 
--item-id <Item id of the key>
```

##### Flags

 `-k, --key-name`: **Required**, The name of the RSA key to use in the verification process 

 `-d, --display-id`: The display id of the key to use in the verification process               

 `-I, --item-id`: The item id of the key to use in the verification process                  

 `-m, --message`: **Required**, The message to be verified.                                

 `-s, --signature`: **Required**, The message's signature.     

### <p style="color:blue">_verify-rsassa-pss_</p>

Verifies an rsassa-pss signature

###### Usage

```shell
akeyless verify-rsassa-pss \
--message <Input message> \
--signature <messages signature> \
--key-name <Key name> \
--display-id <Display id of the RSA key> \
--item-id <Item id of the RSA key>
```

##### Flags

 `-k, --key-name`: The name of the RSA key to use for the verification process       

 `-d, --display-id`: The display id of the RSA key to use for the verification process 

 `-I, --item-id`: The item id of the RSA key to use for the verification process    

 `-f, --hash-function[=sha-256]`: Hash function [sha-256,sha-384,sha-512]                           

 `-m, --message`:(**Mandatory**) The input message to sign in a base64 format      

 `-s, --signature`: (**Mandatory**) The message's signature

## Tokenization

### <p style="color:blue">_create-tokenizer_</p>

Creates a new tokenizer

##### Usage

```shell Tokenization using Templates
akeyless create-tokenizer \
--name <Tokenizer name> \
--tokenizer-type <Tokenizer type> \
--template-type <SSN,CreditCard,USPhoneNumber,Custom> \
--tweak-type <Supplied, Generated, Internal, Masking>
```
```shell Custom Tokenization
akeyless create-tokenizer \
--name *<Tokenizer name> \
--tokenizer-type *<vaultless> \
--template-type *<SSN,CreditCard,USPhoneNumber,Custom> \
--tweak-type <Supplied, Generated, Internal, Masking> \
--alphabet <Symbols to use for tokenization> \
--pattern <A regexp pattern to extract tokenized parts> \
--encoding-template <An expression to alter the template of the encryption output> \
--decoding-template <An expression to alter the template of the decryption output>
```

##### Flags

 `-n, --name`: **Required**, Tokenizer name                                                                                     

 `-y, --tokenizer-type[=vaultless]`: **Required**, Tokenizer type(vaultless)                                                                          

 `-T, --template-type`: **Required**, Which template type this tokenizer is used for [SSN,CreditCard,USPhoneNumber,Custom]               

 `--encryption-key-name`: AES key name to use in vaultless tokenization                                                                      

 `--tweak-type`: The tweak type to use in vaultless tokenization [Supplied, Generated, Internal, Masking]                           

 `--alphabet`: Alphabet to use in custom vaultless tokenization, such as '0123456789' for credit cards.                           

 `--pattern`: Pattern to use in custom vaultless tokenization                                                                    

 `--encoding-template`: The Encoding output template to use in custom vaultless tokenization                                               

 `--decoding-template`: The Decoding output template to use in custom vaultless tokenization                                               

 `--description`: Tokenizer description                                                                                              

 `--tag`: List of the tags attached to this key. To specify multiple tags use argument multiple times: --tag Tag1 --tag Tag2 

 `--delete-protection`: Protection from accidental deletion of this item, [true/false]           

### <p style="color:blue">_detokenize_</p>

Decrypts text with a tokenizer

##### Usage

```shell
akeyless detokenize \
--tokenizer-name <Tokenizer name> \
--ciphertext <Data to be decrypted> \
--tweak <Base64-encoded tweak value that was used for encryption>
```

##### Flags

 `-n, --tokenizer-name`: **Required**, The name of the tokenizer to use in the decryption process 

 `-c, --ciphertext`: **Required**, Data to be decrypted                                       

 `--tweak`: Base64 encoded tweak for vaultless encryption                                          

### <p style="color:blue">_tokenize_</p>

Encrypts text with a tokenizer

##### Usage

```shell
akeyless tokenize \
--tokenizer-name <Tokenizer name> \
--plaintext <Data to be encrypted> \
--tweak <Base64-encoded tweak value
```

##### Flags

 `-n, --tokenizer-name `: **Required**, The name of the tokenizer to use in the encryption process 

 `-p, --plaintext`: **Required**, Data to be encrypted                                       

 `--tweak`: Base64 encoded tweak for vaultless encryption