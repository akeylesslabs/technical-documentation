---
title: GCP Dynamic Secrets
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
You can use Akeyless dynamic secrets to generate programmatic access credentials for GCP (Google Cloud Platform) based on IAM policies that apply to Service Accounts. To do this, configure a dynamic secret with the details required for Akeyless to authenticate and communicate with GCP. This requires privileged account credentials.

There are two GCP dynamic secret modes:

* **Fixed Service Account**

* **Dynamic Service Account**

Fixed Service Accounts are existing GCP service accounts that Akeyless generates JIT tokens or keys and manage them. TTL in GCP is 1 hour by default, but this may be configured for up to 12 hours, as explained in GCP [documentation](https://cloud.google.com/iam/docs/create-short-lived-credentials-delegated#sa-credentials-oauth).

Dynamic Service Accounts are generated and managed by Akeyless Platform, where you can bind a set of IAM roles predefined for that service account. Upon getting a dynamic secret request, Akeyless will generate a Just In time key, or token for this managed service account.

You can generate up to 10 service account keys at the same time. A generated key is revoked when the TTL defined for it expires.

Service Accounts role bindings define a list of resources and the associated IAM roles for that resource. To bind a set of roles to a Dynamic Service Account, you can provide them inline or as a JSON file using the following format:

```json
{
  "/path/to/resource" : ['roles/rolename']
}
```

Where `path/to/resource` should be in the following format according to GCP [Resource](https://cloud.google.com/apis/design/resource_names#full_resource_name) names guide.

For example:

```json
{
  "projects/<Your Project name>/zones/<us-central1-a>/<resource name>": ["roles/resourcemanager.tagViewer"],
  "buckets/<Bucket Name>": ["roles/storage.objectCreator"]
}
```

# Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw).

* A GCP [privileged service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts)  to generate keys and access tokens.

* A [privileged service account roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access#granting-console) includes  `Service Account Key Admin` and `Service Account Token Creator`.

* A [key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) of the privilege service account.

Example list of GCP Service Account permissions:

```shell
iam.serviceAccounts.create
iam.serviceAccounts.delete
iam.serviceAccounts.get
iam.serviceAccounts.list
iam.serviceAccounts.update
iam.serviceAccountKeys.create
iam.serviceAccountKeys.delete
iam.serviceAccountKeys.get
iam.serviceAccountKeys.list
```

# Create a Dynamic GCP Secret from the CLI

> 👍 Note
>
> We recommend using dynamic secrets with [Targets](https://docs.akeyless.io/docs/gcp-targets). While it saves time for multiple secret-level configurations by not requiring you to provide an [inline connection string](https://docs.akeyless.io/docs/gcp-dynamic-secrets#inline-connection-strings) each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.

To create a dynamic GCP secret from the CLI using an existing [GCP Targets](https://docs.akeyless.io/docs/gcp-targets), run the following command:

```shell Fixed Service Account
akeyless dynamic-secret create gcp \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--gcp-sa-email <service account email>
--gcp-cred-type <token|key> \
--gcp-token-scopes <Token Scopes> \
--gcp-key-algo <Service Key Algorithm>
```
```shell Dynamic Service Account
akeyless dynamic-secret create gcp \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--service-account-type dynamic \
--role-binding <Path to JSON roles file> \
--gcp-cred-type <token|key> \
--gcp-token-scopes <Token Scopes> \
--gcp-key-algo <Service Key Algorithm>
```

Or using an inline connection string:

```shell Akeyless CLI
akeyless dynamic-secret create gcp \
--name <Dynamic Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--gcp-sa-email <service account email>
--gcp-cred-type <token|key> \
--gcp-token-scopes <Token Scopes> \
--gcp-key-algo <Service Key Algorithm> \
--gcp-sa-email <GCP Service Account Email> \
--gcp-key-file-path <GCP Service Account Private Key>
```

Where:

* `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

* `target-name`: A name of the target that enables connection to the GCP server. The name can include the path to the virtual folder where this target resides.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `service-account-type`: `Fixed` or `Dynamic`type. By default set to **Fixed**.

* `role-binding`: A path to a JSON file that holds the relevant resource with roles to bind for the created Service Account. Relevant only for **Dynamic** type.

* `gcp-sa-email`: The email of the Service Account to create JIT keys/tokens. Relevant only for **Fixed** Service Account.

* `gcp-cred-type`: Credentials type. Available options are: `token`, `key`.

* `gcp-token-scopes`:  Access token scopes list.

* `gcp-key-algo`: Service account key algorithm, e.g. `KEY_ALG_RSA_1024`, `KEY_ALG_RSA_2048`

### Inline connection string

If you don't have a [GCP Target](https://docs.akeyless.io/docs/gcp-targets)  yet, you can use the command with your GCP connection strings:

* `gcp-sa-email`: privileged service account email.

* `gcp-key-file-path`: Path to file with the Base64-encoded privileged service account private key.

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#p-stylecolorbluegcpp) section.

# Fetch a Dynamic GCP Secret value from the CLI

To fetch a dynamic GCP secret value from the CLI, run the following command:

```shell Akeyless CLI
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

# Create a Dynamic GCP Secret in the Akeyless Console

> 👍 Note
>
> To start working with dynamic secrets from the [Akeyless Console](https://docs.akeyless.io/docs/gcp-dynamic-secrets#create-a-dynamic-gcp-secret-in-the-akeyless-console), you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the GCP secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

* **Delete Protection:** When enabled, it protects the secret from accidental deletion.

* **Target mode:** In this section, you can either select an existing [GCP Target](https://docs.akeyless.io/docs/gcp-targets) or specify details of the GCP target explicitly.

  * Use the **Choose an existing target** drop-down list to select the existing [GCP Target](https://docs.akeyless.io/docs/gcp-targets).

  * Check the **Explicitly specify target properties**  to provide details of the GCP target in the next step.

* **Fixed:** A fixed Service Account. with **Service Account  Email** to create JIT Keys/Tokens for.

* **Dynamic:** A Dynamic Service Account with **Role Binding** to attach an IAM policy and roles for the created Service Account.
  * **Project ID:** A comma-separated list of Project ID's where the Service Account will be created in, During secret usage, a Project ID defined in the list can be chosen for Service Account creation (Relevant only for **Dynamic Secret mode**.

* **Access Token:** Select this radio button to create a GCP access token as a dynamic secret.

* **Service Account Key:** Select this radio button to create a GCP service account key as a dynamic secret.

* **Token Scopes:** Provide a comma-separated list of [GCP access token scopes](https://developers.google.com/identity/protocols/oauth2/scopes). (If **Access Token** is selected.)

* **Key Algorithm:** Key algorithm. Available options: `KEY_ALG_UNSPECIFIED`, `KEY_ALG_RSA_1024`, `KEY_ALG_RSA_2048`. (If **Service Account Key** is selected.)

* **Custom Username Template:** Set a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) for the generated user (relevant only for **Dynamic Secret** mode).

* **User TTL:** Provide a time-to-live value for a dynamic secret (i.e., a token). When TTL expires, the token becomes obsolete.

* **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.

* **Gateway:** Select the Gateway through which the dynamic secret will create users.

* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

5. If you checked the **Explicitly specify target properties** radio button, click **Next**.

6. Provide the connection string to your GCP :

* **Service Account Email:** privileged service account email.

* **Service Account Key:** Base64-encoded privileged service account key.

7. Click **Finish**.

# Fetch a Dynamic GCP Secret Value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click **Get Dynamic Secret** button.
