---
title: Azure Databricks Plugin
excerpt: Secure Databricks Workloads with Akeyless Centralized Secrets Management
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Easily manage secrets across Databricks DataOps / MLOps pipelines using Akeyless

### Background

Azure Databricks allows secret management via its native secret scope or integration with Azure Key Vault. However, organizations operating across clouds or teams often face challenges such as:

Secret sprawl across environments  
Cloud vendor lock-in  
Inconsistent RBAC policies  
Akeyless provides a centralized, cloud-agnostic vault for managing secrets securely and consistently — making it ideal for managing secrets in Databricks DLT (delta live table) and non-DLT workloads, across Azure and AWS.

### Use Case

Akeyless enables:

- Seamless secrets access in DataOps and MLOps workflows (Python, Scala, R)
- Cross-cloud workload portability with minimal code changes
- Integration with Azure Managed Identity or Akeyless API key authentication

While Databricks supports SQL, most SQL queries don’t require secrets — hence Akeyless primarily targets Python, Scala, and R notebooks.

### Prerequisites

- An active Azure Databricks workspace with internet access or the access to Akeyless Gateway
- Akeyless account with an Access ID
- A stored secret in Akeyless (e.g., API key for data access)

### Authentication Options

#### Option 1: Azure Managed Identity (recommended for Azure-native workloads)

- Use Azure AD with Akeyless to authenticate Databricks using the VM's managed identity.

#### Option 2: API Key stored in Azure Key Vault

- Enables user-level RBAC by storing each user's Akeyless API key securely.

### Language Support

#### Databricks supports:

- Python ✅ (fully supported by Akeyless SDK)
- Scala / R ✅ (via Spark config or Databricks utilities)
- SQL 🚫 (usually not required for secrets)

### Example: Sharing a secret across languages

```shell Python
# Python Cell: retrieve secret and set Spark config
spark.conf.set("api.key", "RETRIEVED_SECRET")
```

```shell Scala
// Scala Cell: read secret from Spark config
val apiKey = spark.conf.get("api.key")
println(s"Retrieved API Key: $apiKey")
```

### Implementation: Sample Python Notebook

This notebook retrieves a secret (API key), fetches data from a public API, and saves it into a Databricks table.

#### Step-by-Step Notebook:

```shell Python
# Install Akeyless packages
%pip install akeyless akeyless_cloud_id
%restart_python
```

What it does:

- Installs the Akeyless SDK and the akeyless_cloud_id helper, which generates the required identity token.
- akeyless_cloud_id helps authenticate with Akeyless using Azure Managed Identity.
- %restart_python is required in Databricks after installing new packages to reload the environment.

```shell Python
# Import Akeyless SDK and cloud ID generator
from akeyless_cloud_id import CloudId
import akeyless

# Set up Akeyless API client
configuration = akeyless.Configuration(host="https://api.akeyless.io")
api_client = akeyless.ApiClient(configuration)
api = akeyless.V2Api(api_client)

# Generate cloud ID for Azure Managed Identity
cloud_id = CloudId().generateAzure()

# Authenticate with Akeyless using Azure AD
access_id = "REPLACE_WITH_YOUR_ACCESS_ID"
secret_path = "/devops/data_gov_api_key"
auth_body = akeyless.Auth(access_id=access_id, access_type='azure_ad', cloud_id=cloud_id)
token = api.auth(auth_body).token

# Retrieve the secret value
secret_body = akeyless.GetSecretValue(names=[secret_path], token=token)
res = api.get_secret_value(secret_body)
API_KEY = res[secret_path]
print(f"🔐 Retrieved API Key: {API_KEY}")
```

What it does:

- Initializes the Akeyless API client.
- Points to the public Akeyless API endpoint.
- Generates an Azure-specific identity token (JWT) using the current VM’s managed identity.
- Authenticates with Akeyless using that token and your Akeyless Access ID.
- Retrieves a temporary session token (token) that will be used to fetch secrets securely.
- Requests the secret value from Akeyless for the given path (/devops/data_gov_api_key).
- Stores the result in the API_KEY variable.
- You can now use this API key in your code securely — without ever hardcoding it!

```shell Python
# Use the API key to fetch public data
import requests
url = "https://health.data.ny.gov/api/views/jxy9-yhdk/rows.csv"
params = {"api_key": API_KEY, "per_page": 5}
response = requests.get(url, params=params)
```

What it does:

- Calls a public API that requires authentication (in this case, data.gov) using the secret from Akeyless.

```shell Python
# Load response into DataFrame and save to Databricks
import pandas as pd
from io import StringIO

if response.status_code == 200:
    pdf = pd.read_csv(StringIO(response.text))
    pdf.columns = pdf.columns.str.replace(" ", "_")
    df = spark.createDataFrame(pdf.fillna(""))

    table_name = "baby_names_by_non_dlt"
    df.write.mode("overwrite").saveAsTable(table_name)
    display(spark.sql(f"SELECT * FROM {table_name}"))
else:
    print(f"❌ API Request Failed: {response.status_code}")
```

What it does:

- Converts the API response into a Pandas DataFrame.
- Cleans the data (removes nulls and spaces in column names).
- Converts to a Spark DataFrame and saves it as a Databricks table.
- Displays the table contents for validation.



> 👍 Note
> 
> - DLT workloads may not attach Managed Identity to every VM. In that case, use API key authentication.
> - For user-level or group-level RBAC, store access keys in Azure Key Vault per user/team.

### Final Result

If successful, you’ll see the data from the API inside your Databricks workspace, stored securely using a secret retrieved from Akeyless.