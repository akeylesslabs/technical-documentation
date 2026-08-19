---
title: Jenkins Plugin
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
The [Akeyless Plugin for Jenkins](https://plugins.jenkins.io/akeyless) injects Akeyless-managed secrets and certificates into Freestyle jobs and Pipeline jobs. It supports multiple [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods), JSON key selection, and optional sync into the native Jenkins credential store.

Jenkins plugin: [plugins.jenkins.io/akeyless](https://plugins.jenkins.io/akeyless)

Repository: [jenkinsci/akeyless-plugin](https://github.com/jenkinsci/akeyless-plugin)

If you are deciding between Jenkins integration paths:

* [Jenkins Plugin](https://docs.akeyless.io/docs/jenkins): Native Akeyless plugin. Use this for new implementations.
* [Jenkins Plugin by way of HashiCorp Vault Proxy](https://docs.akeyless.io/docs/jenkins-plugin-via-hvp): HashiCorp Vault plugin talking to the Akeyless HashiCorp Vault Proxy.

## Features

| Capability | How you use it | Description |
| --- | --- | --- |
| **Build Wrapper** | Freestyle **Build Environment → Akeyless Plugin** | Fetch secrets and certificates into environment variables for the duration of the build. Secret values are masked in the console log. |
| **Pipeline step** | `withAkeyless { ... }` | Same fetch behavior inside a Pipeline / Jenkinsfile. Values are available only inside the block. |
| **Synced Credentials** | **Manage Jenkins → System → Akeyless Synced Credentials** | Optional. Surfaces Akeyless items as native Jenkins credentials for `credentials('id')` / `withCredentials`. |
| **JSON key selection** | **Key Name** / `secretKey` | Fetch a single JSON field (for example `username`) or the full payload with `data`. |
| **Folder and global config** | Folder properties or **Manage Jenkins** | Share Gateway URL and credential ID across jobs. Child jobs can inherit or override. |

## Prerequisites

* Jenkins LTS **2.479.3** or later (the plugin baseline).
* An Akeyless [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) associated with an [Access Role](https://docs.akeyless.io/docs/rbac) that has **read** (and **list** if you use folder discovery) on the target items.
* Network connectivity from the Jenkins controller to your Akeyless API endpoint (`https://api.akeyless.io` or your Gateway `https://<gateway-host>:8000/api/v2`).

> ℹ️ **Note (Zero-Knowledge Encryption):**
>
> If you use a customer [key fragment](https://docs.akeyless.io/docs/dfc-overview), set **Akeyless URL** to your Gateway REST API endpoint, for example `https://Your_GW_URL:8000/api/v2`.

## Installation

1. Navigate to **Manage Jenkins → Plugins**.
2. Go to **Available Plugins** and search for **Akeyless**.
3. Select the plugin and install it.
4. Restart Jenkins if prompted.

To install a specific build, use **Manage Jenkins → Plugins → Advanced → Upload Plugin** and upload the `.hpi` file.

## Supported Authentication Methods

* [API Key](https://docs.akeyless.io/docs/auth-with-api-key)
* [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws)
* [Azure AD](https://docs.akeyless.io/docs/auth-with-azure)
* [Certificate](https://docs.akeyless.io/docs/auth-with-certificate)
* [Google Cloud Platform (GCP)](https://docs.akeyless.io/docs/auth-with-gcp)
* [Kubernetes](https://docs.akeyless.io/docs/auth-with-kubernetes)
* [Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity)
* [JWT](https://docs.akeyless.io/docs/auth-with-oauth-jwt)
* [Email](https://docs.akeyless.io/docs/auth-with-email)
* t-Token

## Configuration

You can set **Akeyless URL** and credentials at the Jenkins global level, on a folder, or on an individual job. Job-level settings override folder settings, which override global settings.

### Configure a Freestyle job

1. From the Jenkins Dashboard, select **New Item**, choose **Freestyle Project**, give it a name, and select **OK**.
2. Scroll to **Build Environment** and enable **Akeyless Plugin**.
3. Set **Akeyless URL** to `https://api.akeyless.io` or your Gateway URL with the `/api/v2` endpoint.
4. Add credentials:

   * Under **Vault Credential**, select **Add → Jenkins**.
   * Choose the authentication method from the **Kind** drop-down:

     | Kind | Akeyless Authentication Method |
     | --- | --- |
     | **Akeyless Access Key Credentials** | API Key |
     | **Akeyless Cloud Provider Credentials** | AWS IAM, Azure AD, or GCP |
     | **Akeyless Certificate Credentials** | Certificate |
     | **Akeyless Kubernetes Credentials** | Kubernetes |
     | **Akeyless Universal Identity Credentials** | Universal Identity |
     | **Akeyless JWT** | OAuth 2.0 / JWT |
     | **Username with password** | Email |
     | **Akeyless t-Token Credentials** | t-Token |

   * Select **Add** to save the credential, then select it in the job.

Optional job settings:

* **Skip SSL verification**: use only for lab environments with self-signed certificates.
* **Timeout**: HTTP timeout in seconds (default `60`).

### Cloud IAM on the Jenkins controller

For **Akeyless Cloud Provider Credentials**, the Jenkins controller (or agent, depending on where the build runs) must present a valid AWS, Azure, or GCP identity. Typical setups:

* AWS: instance profile, IRSA, or ECS/EKS task role on the Jenkins host.
* Azure: managed identity on the Jenkins VM or AKS workload identity.
* GCP: attached service account on GCE/GKE.

No static Access Key is stored in Jenkins for these methods. You still provide the Akeyless **Access ID**.

## Retrieving Items

The plugin retrieves **Static**, **Dynamic**, and **Rotated** Secrets and issues **PKI** and **SSH** certificates. It calls `describe-item` to detect the item type, then the matching get API (`get-secret-value`, `get-dynamic-secret-value`, `get-rotated-secret-value`, or certificate issue).

### Retrieving Secrets

1. Select **Add Akeyless Secret**.
2. Configure:

   * **Path**: Full Akeyless path, for example `/DevOps/Jenkins/db`.
   * **Environment Variable**: Name of the environment variable that receives the value.
   * **Key Name**: JSON field to extract. Use `data` to store the full secret payload.

Dynamic producer values are typically JSON with `username` and `password`. Map each field to its own environment variable.

Rotated secrets that store JSON (for example `username` / `password`) work the same way.

### Issuing Certificates

1. Select **Add Akeyless Issuer**.
2. Configure:

   * **Path**: Full path of the certificate issuer.
   * **Output Name**: Name of the retrieved certificate.
   * **Certificate User Name**: For SSH certificates, the principal to sign (for example `ubuntu`).
   * **Public Key**: Public key to sign (SSH).
   * **CSR in Base64**: Certificate Signing Request in Base64 (PKI).
   * **TTL**: Requested certificate lifetime when the issuer allows it.
   * **Environment Variable**: Variable that stores the issued material.
   * **Key Name**: JSON field to extract, or `data` for the full payload.

## Pipeline (`withAkeyless`)

Use the `withAkeyless` step in a Declarative or Scripted Pipeline. Fetched values exist only inside the block and are masked in the build log.

```groovy
pipeline {
  agent any
  stages {
    stage('Fetch secrets') {
      steps {
        withAkeyless(
          configuration: [
            akeylessUrl: 'https://Your_GW_URL:8000/api/v2',
            akeylessCredentialId: 'akeyless-api-key'
          ],
          akeylessSecrets: [
            [
              path: '/DevOps/Jenkins/static-json',
              secretValues: [
                [envVar: 'APP_USER', secretKey: 'username'],
                [envVar: 'APP_PASS', secretKey: 'password']
              ]
            ],
            [
              path: '/GW2/Postgres',
              secretValues: [
                [envVar: 'PGUSER', secretKey: 'username'],
                [envVar: 'PGPASSWORD', secretKey: 'password']
              ]
            ]
          ]
        ) {
          sh 'psql "host=db.example.com dbname=app user=$PGUSER password=$PGPASSWORD" -c "SELECT 1"'
        }
      }
    }
  }
}
```

To bind the entire secret JSON (or a non-JSON static value) to one variable, set `secretKey` to `data`:

```groovy
withAkeyless(
  configuration: [akeylessCredentialId: 'akeyless-api-key'],
  akeylessSecrets: [[
    path: '/DevOps/Jenkins/api-token',
    secretValues: [[envVar: 'API_TOKEN', secretKey: 'data']]
  ]]
) {
  sh 'curl -H "Authorization: Bearer $API_TOKEN" https://api.example.com/health'
}
```

SSH certificate example:

```groovy
withAkeyless(
  configuration: [akeylessCredentialId: 'akeyless-api-key'],
  akeylessSSHIssuers: [[
    path: '/SRA/DemoSSHCertIssuer',
    name: 'jenkins-ssh',
    certUserName: 'ubuntu',
    publicKey: "${SSH_PUBLIC_KEY}",
    ttl: 300,
    secretValues: [[envVar: 'SSH_CERT', secretKey: 'data']]
  ]]
) {
  sh 'echo "$SSH_CERT" > signed-cert.pub'
}
```

PKI certificate example:

```groovy
withAkeyless(
  configuration: [akeylessCredentialId: 'akeyless-api-key'],
  akeylessPKIIssuers: [[
    path: '/PKI/JenkinsIssuer',
    name: 'jenkins-pki',
    csrBase64: "${CSR_B64}",
    ttl: 3600,
    secretValues: [[envVar: 'TLS_CERT', secretKey: 'data']]
  ]]
) {
  sh 'echo "$TLS_CERT" > server.crt'
}
```

You can generate this syntax from the Jenkins **Pipeline Syntax** snippet generator: select **withAkeyless: Akeyless Plugin**.

## Synced Credentials (Credentials Provider)

Optional. When configured, Akeyless items appear in **Manage Jenkins → Credentials** under the Akeyless store. Jobs then use standard Jenkins credentials APIs. Classic `withAkeyless` / Build Wrapper jobs are unchanged if you leave this section empty.

### Configure

1. Open **Manage Jenkins → System**.
2. Find **Akeyless Synced Credentials (Credentials Provider)**.
3. Set:

   * **Akeyless URL**: Gateway or SaaS API URL used as-is (no suffix is added). If the Gateway is behind a load balancer, include the path, for example `https://gateway.example.com/api/v2`.
   * **Authentication scope**:
     * **Global**: one Akeyless identity for all Jenkins users (configured on this page).
     * **Per user**: each Jenkins user configures Akeyless auth on **People → user → Configure**.
   * **Access ID** and **Authentication Method** (when using Global scope): API Key, JWT, AWS IAM, Azure AD, GCP, Certificate, Kubernetes, Universal Identity, or Email.
   * **Cache**: when enabled, folder `list-items` results are cached for 5 minutes.
   * **Folder path**: Akeyless folder, for example `/CICD/jenkins/secrets`. Cannot be `/` alone (that would list the entire vault).
   * **Secret names**: optional. One name per line. Full path is `folder + / + name`. The name is the Jenkins credential ID, for example `credentials('jenkinsai')`.
   * **Secret paths**: optional. Full paths, one per line, as an alternative to folder + names.

4. Save, then open **Manage Jenkins → Credentials** and confirm items appear under the Akeyless store.

Discovery modes:

| What you fill in | Behavior |
| --- | --- |
| Folder path only | Recursive `list-items` under that folder (requires **list** permission). Credential ID is the last path segment when unique. |
| Folder path + secret names | No listing. Each name is fetched at `folder/name`. |
| Secret paths | No listing. Each full path is fetched. |

### Map Akeyless items to Jenkins credential types

Tag the Akeyless item (same convention as the AWS Secrets Manager Credentials Provider):

| Tag | Values | Meaning |
| --- | --- | --- |
| `jenkins:credentials:type` | `string` (default), `usernamePassword`, `sshUserPrivateKey`, `certificate`, `file` | Jenkins credential kind |
| `jenkins:credentials:username` | string | Username when the secret body is not JSON |
| `jenkins:credentials:valueFormat` | `json` | Parse username/password (or username/privateKey) from a JSON secret body |
| `jenkins:credentials:filename` | string | File name for `file` credentials |

When `jenkins:credentials:valueFormat=json`:

* **usernamePassword** reads `username` / `user` / `usr` and `password` / `psw` / `secret` / `passwd`.
* **sshUserPrivateKey** reads `username` and `privateKey` / `private_key` / `key`, plus optional `passphrase`.

### Use in a Pipeline

```groovy
withCredentials([string(credentialsId: 'jenkinsai', variable: 'TOKEN')]) {
  sh 'echo "secret loaded"'
}
```

Username/password example:

```groovy
withCredentials([usernamePassword(credentialsId: 'db-creds', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASS')]) {
  sh 'mysql --user="$DB_USER" --password="$DB_PASS" -e "SELECT 1"'
}
```

## Examples

The following examples show Freestyle configuration in the Jenkins UI.

### Setting API Key Authentication

The following configuration uses an existing API Key in Akeyless for Jenkins authentication.

![Illustration for: Setting API Key Authentication The following configuration uses an existing API Key in Akeyless for Jenkins authentication.](https://files.readme.io/fd278b50a80159780c9b765772b37859ba715f7ad777ae12d0d214db21c1b55c-image.png)

### Fetching a Static Secret

The following configuration fetches a static secret into the pipeline. This example uses a JSON-structured secret, where only the **UserName** key is saved to the **User** environment variable.

![Illustration for: The following configuration will fetch a static secret to your pipeline. This example uses a JSON-Structured secret, where only the UserName key of the secret is saved to User…](https://files.readme.io/9f31c3fcbc87a157d318e00535237be8fb2ac2f7ba8d7b003375341fb4478eff-image.png)

### Fetching a Rotated Secret With Specific Keys

The following example fetches only the **username** of the rotated secret value and stores it in the **User** environment variable:

![Illustration for: Fetching a Rotated Secret With Specific Keys The following example will only fetch the username of the rotated secret value, and will store it into User environment variable](https://files.readme.io/2ee1e96798d98e9d3c2c06d87f93f882da509660dddf979bdf997ede339acd71-image.png)

### Fetching a Dynamic Secret

Add an Akeyless Secret whose **Path** is the dynamic producer (for example `/GW2/Postgres`). Map JSON keys such as `username` and `password` to environment variables. The plugin detects `DYNAMIC_SECRET` and calls `get-dynamic-secret-value`.

Use those variables only inside the job or `withAkeyless` block. Ephemeral credentials expire according to the producer's TTL.

### Issuing an SSH Certificate

The following example generates an SSH certificate allowed for the `ubuntu` user, using a public key:

![Illustration for: Issuing an SSH Certificate The following above will generate an SSH Certificate that will be allowed for the ubuntu user, using a public key](https://files.readme.io/20d1d24c8bf53d285e233e8c698442a101f65c381ff31ec1c5b9b972a4671494-image.png)

### Issuing a PKI Certificate

The following example generates a PKI certificate using a predefined Certificate Signing Request:

![Illustration for: Issuing a PKI Certificate The following example will generate PKI Certificate using predefined Certificate Signing Request](https://files.readme.io/572a3006acc9bf1bae374b45fe721ec09e1658fc5c954c1c0114056049254b5f-image.png)

## Troubleshooting

### Authentication fails

* Confirm **Akeyless URL** includes `/api/v2` for classic job binding (Build Wrapper / `withAkeyless`).
* Confirm the selected Jenkins credential Kind matches the Authentication Method in Akeyless.
* Confirm the Access Role associated with that method has **read** on the item path.
* For cloud IAM, confirm the Jenkins host actually has the expected AWS/Azure/GCP identity.

### `Required secret ... is either null or empty`

The **Key Name** / `secretKey` does not exist in the returned JSON. For dynamic and rotated database secrets, use `username` and `password` (or `data` for the full object). For a plain static string, use `data`.

### `The field ... is not defined in the ItemGeneralInfo properties`

The Gateway/API returned a newer `describe-item` field than the Java SDK bundled in the installed plugin. Update the Akeyless Jenkins plugin to the latest release from [plugins.jenkins.io/akeyless](https://plugins.jenkins.io/akeyless).

### Synced credentials do not appear

* Confirm **Akeyless URL**, Access ID, and auth method under **Manage Jenkins → System**.
* Folder path cannot be `/` alone.
* Folder-only discovery needs **list** permission on that folder.
* Credential ID is the last path segment (for example `/CICD/jenkins/secrets/jenkinsai` → `jenkinsai`) unless that ID is already used.

### SSL errors talking to the Gateway

Install a trusted CA on the Jenkins JVM, or (labs only) enable **Skip SSL verification** on the job configuration.
