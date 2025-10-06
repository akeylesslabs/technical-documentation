---
title: CLI Reference - K8s Auth Method
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
This section outlines the CLI commands relevant to Kubernetes authentication.

General Flags:

`--profile, --token`:  Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal\_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

### `create`

Creates a new Authentication Method object that will allow the user to authenticate using Kubernetes

##### Usage

```shell
akeyless auth-method create k8s \
--name <Auth method name> \
--public-key-file-path <Path\To\Public\Key> \
--bound-pod-names <list of pods name> \
--bound-namespaces <list of namespaces that the access is restricted to> \
--public-key <Base64-encoded or PEM formatted public key data> \
--audience <The audience in the Kubernetes JWT that the access is restricted to>
```

##### Flags

 `-n, --name`: **Required**, Auth Method name             

 `--descrpition`: Auth Method description 

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)      

 `--bound-ips`: A comma-separated CIDR block list to allow client access                                        

 `--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity                                 

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username` 

`--delete-protection`: Protection from accidental deletion of this object, \[true/false

`--force-sub-claims`: enforce role-association must include sub-claims           

 `--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)   

 `-p, --public-key-file-path`: In case the gen-key  set to false, path to a public key for K8S authentication method is required [RSA2048] 

 `--public-key`: Base64-encoded or PEM formatted public key data 

 `--audience`: The audience in the Kubernetes JWT that the access is restricted to 

 `--bound-sa-names`: A list of service account names that the access is restricted to      

 `--bound-pod-names`: A list of pod names that the access is restricted to                  

 `--bound-namespaces`: A list of namespaces that the access is restricted to               

 `--gen-key[=true]`: Automatically generate key-pair for K8S configuration. If set to false, a public key needs to be provided            

#### `gateway-create-k8s-auth-config`

Creates Kubernetes Auth config on Gateway

##### Usage

```shell Akeyless CLI
akeyless gateway-create-k8s-auth-config \
--name <k8s-conf name> \
--access-id <Access_ID> \
--gateway-url <API Gateway URL:8000> \
--signing-key <Private_Key> \
--k8s-host <https://Your-K8s-Cluster-IP:8443> \
--token-reviewer-jwt <SA_JWT_TOKEN> \
--k8s-ca-cert <CA_CERT> \
--k8s-issuer <K8S_ISSUER>
```
```shell Rancher
akeyless gateway-create-k8s-auth-config  --name k8s-conf-rancher \
--gateway-url <https://Your-GW-URL>:8000 \
--access-id $ACCESS_ID \
--signing-key $PRV_KEY \
--cluster-api-type rancher \
--k8s-host=<https://Rancher Host>:443 \
--k8s-ca-cert $CA_CERT \
--k8s-issuer $K8S_ISSUER \
--rancher-api-key <API_KEY> \
--rancher-cluster-id <CLUSTER_ID> \
```
```shell Gateway Service Account
akeyless gateway-create-k8s-auth-config  --name k8s-conf \
--gateway-url <API Gateway URL:8000> \
--access-id <Access_ID> \
--signing-key <Private_Key> \
--use-gw-service-account
```

##### Flags

 `-n, --name`: **Required**, K8S Auth config name             

 `--access-id`: **Required**, The Access ID of the Kubernetes auth method         

 `--signing-key`: The private key (base64 encoded) associated with the public key defined in the Kubernetes auth    

 `--token-exp[=300]`: Time in seconds of expiration of the Akeyless Kubernetes Auth Method token                 

 `-i, --use-gw-service-account`: Use the GW's service account                                                   

 `--cluster-api-type[=native_k8s]`: Cluster access type. options: `native_k8s`, `rancher`           

 ` --k8s-host`: The URL of the kubernetes API server                                                    

 `--k8s-ca-cert`: The CA Certificate (base64 encoded) to use to call into the kubernetes API server       

 `--k8s-auth-type[=token]`: Native K8S auth type, \[token/certificate]. (relevant for "native\_k8s" only)      

 `--k8s-client-certificate`: Content of the k8 client certificate (PEM format) in a Base64 format (relevant for "native\_k8s" only)     

 `--k8s-client-certificate-file`: Path to a file that contain the k8s client certificate in PEM format (relevant for "native\_k8s" only)  

 `--k8s-client-key`: Content of the k8 client private key (PEM format) in a Base64 format (relevant for "native\_k8s" only)              

 `--k8s-client-key-file`: Path to a file that contain the k8s client private key in PEM format (relevant for "native\_k8s" only)          

 `--token-reviewer-jwt`: A Kubernetes service account JWT used to access the TokenReview API to validate other JWTs (relevant for "native\_k8s" only) 

 `--rancher-api-key`: The API Key used to access the TokenReview API to validate other JWTs (relevant for "rancher" only)                    

 `--rancher-cluster-id`: The cluster ID as defined in Rancher (relevant for "rancher" only)                                               

 `--k8s-issuer[=kubernetes/serviceaccount]`: The Kubernetes JWT issuer name. If not set, this \<kubernetes/serviceaccount> will be used by default  

 `--disable-issuer-validation[=true]`: Disable issuer validation `true`/`false`            

 `--config-encryption-key-name`: Encrypt K8S Auth config with following key               

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)      

### `update`

Update a new Authentication Method that will be able to authenticate using Kubernetes

##### Usage

```shell
akeyless update-auth-method-k8s \
--name <Auth method name> \
--new-name <Auth method new name> 
```

##### Flags

 `--new-name`: Auth Method new name                                                                                                 

 `-n, --name`: **Required**, Auth Method name                                                                                     

 `--descrpition`: Auth Method description 

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)           

 `--bound-ips`: A comma-separated CIDR block list to allow client access        

 `--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity   

 `--force-sub-claims`: enforce role-association must include sub-claims                   

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username` 

`--delete-protection`: Protection from accidental deletion of this object, \[true/false]

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)   

 `-p, --public-key-file-path`: In case the gen-key  set to false, path to a public key for K8S authentication method is required [RSA2048] 

 `--public-key`: Base64-encoded or PEM formatted public key data                                                                 

 `--audience`: The audience in the Kubernetes JWT that the access is restricted to              

 `--bound-sa-names`: A list of service account names that the access is restricted to          

 `--bound-pod-names`: A list of pod names that the access is restricted to                  

 `--bound-namespaces`: A list of namespaces that the access is restricted to                

 `--gen-key`: Automatically generate key-pair for K8S configuration. If set to false, a public key needs to be provided

#### gateway-update-k8s-auth-config

##### Usage

```shell
akeyless gateway-update-k8s-auth-config \
--name <Auth name> \
--access-id <access-id> \
--new-name <config new-name> \
--k8s-host <kubernetes API server URL> 
```

##### Flags

 `-n, --name`: **Required**, K8S Auth config name   

 `--descrpition`: Auth Method description 

`--access-id`: **Required**, The access ID of the Kubernetes auth method         

 `--signing-key`: The private key (base64 encoded) associated with the public key defined in the Kubernetes auth    

 `--token-exp[=300]`: Time in seconds of expiration of the Akeyless Kubernetes Auth Method token              

 `-i, --use-gw-service-account`: Use the GW's service account                         

 `--cluster-api-type[=native_k8s]`: Cluster access type. options: \[native\_k8s, rancher]        

 `--k8s-host`: The URL of the kubernetes API server                   

 `--k8s-ca-cert`: The CA Certificate (base64 encoded) to use to call into the kubernetes API server      

 `--k8s-auth-type[=token]`: Native K8S auth type, \[token/certificate]. (relevant for "native\_k8s" only)  

 `--k8s-client-certificate`: Content of the k8 client certificate (PEM format) in a Base64 format (relevant for "native\_k8s" only)       

 `--k8s-client-certificate-file`: Path to a file that contain the k8s client certificate in PEM format (relevant for "native\_k8s" only)  

 `--k8s-client-key`: Content of the k8 client private key (PEM format) in a Base64 format (relevant for "native\_k8s" only)   

 `--k8s-client-key-file`: Path to a file that contain the k8s client private key in PEM format (relevant for "native\_k8s" only)  

 `--token-reviewer-jwt`: A Kubernetes service account JWT used to access the TokenReview API to validate other JWTs (relevant for "native\_k8s" only) 

 `--rancher-api-key`: The api key used to access the TokenReview API to validate other JWTs (relevant for "rancher" only)                      

 `--rancher-cluster-id`: The cluster id as define in rancher (relevant for "rancher" only)                                      

 `--k8s-issuer=[kubernetes/serviceaccount]`: The Kubernetes JWT issuer name. If not set, this \<kubernetes/serviceaccount> will be used by default.   

 `--disable-issuer-validation[=true]`: Disable issuer validation `true`/`false`                                     

 `--config-encryption-key-name`: Encrypt K8S Auth config with following key                                         

 ` -u, --gateway-url=[http://localhost:8000]`: API Gateway URL (Configuration Management port)                    

 `--new-name`: **Required**, K8S Auth config new-name    

`--audit-logs-claims`:  Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username` 

`--delete-protection`: Protection from accidental deletion of this object, \[true/false]

### `get`

Gets Gateway Kubernetes Auth config

##### Usage

```shell
akeyless gateway-get-k8s-auth-config \
--name <K8S Auth config name> \
--gateway-url <API Gateway URL:8000> 
```

##### Flags

 `-n, --name`: **Required**, K8S Auth config name\
 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)

### `delete`

Deletes K8S Auth config

##### Usage

```shell
akeyless gateway-delete-k8s-auth-config \
--name <Auth config name> \
--gateway-url <API Gateway URL:8000> 
```

##### Flags

 `-n, --name`: **Required**, K8S Auth config name

 `-u, --gateway-url[=http://localhost:8000]`: API Gateway URL (Configuration Management port)