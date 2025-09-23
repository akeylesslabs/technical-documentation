---
title: AWS Databricks Plugin
excerpt: Using Akeyless Secrets in AWS Databricks for DataOps and MLOps
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
### Overview

Managing secrets across AWS services can be challenging, especially in a multi-cloud environment or when moving workloads between AWS and Azure.

With Akeyless Vault, you can manage secrets centrally and securely for Databricks workloads, including:

- Delta Live Tables (DLT) and Non-DLT jobs
- DataOps and MLOps use cases

Akeyless helps avoid secret scattering across AWS Secrets Manager, Databricks secret scopes, and other platforms, giving you a cloud-agnostic and portable solution.



### Supported Languages in Databricks

#### Databricks supports:

- Python (natively supported by Akeyless SDK)
- Scala & R (via spark.conf or dbutils)
- SQL (generally does not require secrets)

### Requirements

#### AWS Infrastructure

- An IAM role for EC2 instances used by Databricks compute clusters
- A cross-account IAM role allowing Databricks to manage AWS resources
- Properly configured Instance Profile in Databricks to link IAM roles

#### Akeyless Configuration

- An Akeyless Access ID
- An AWS IAM Auth Method created in Akeyless
- A secret stored in Akeyless (e.g., /devops/data_gov_api_key)
- A Databricks workspace with internet access or the access to the Akeyless gateway

### Architecture Overview

Databricks EC2 → AWS IAM Role → Akeyless IAM Auth Method → Secret Retrieval → Use in Notebook (Python, DLT)

![](https://files.readme.io/2189d87976ab1d76db0a28db1143de5d30fa789a94c370b1dc49030eb4f4a6ee-image.png)

### Step-by-Step Guide: Using Akeyless in Databricks

#### Step 1: Install Required Packages

```shell Python
%pip install akeyless akeyless_cloud_id
%restart_python
```

Installs the Akeyless SDK and cloud identity helper, then restarts the Python kernel in Databricks.

#### Step 2: Authenticate with Akeyless Using AWS IAM

```shell Python
from akeyless_cloud_id import CloudId
import akeyless

# Set up Akeyless client
config = akeyless.Configuration(host="https://api.akeyless.io")
client = akeyless.ApiClient(config)
api = akeyless.V2Api(client)

# Generate cloud ID from IAM role
cloud_id = CloudId().generate()

# Replace with your actual Akeyless Access ID
access_id = "REPLACE_WITH_YOUR_ACCESS_ID"

# Define secret path
secret_path = "/devops/data_gov_api_key"

# Authenticate using AWS IAM
auth_request = akeyless.Auth(
    access_id=access_id,
    access_type="aws_iam",
    cloud_id=cloud_id
)
token = api.auth(auth_request).token
```

This uses the IAM role attached to the Databricks EC2 instance to securely get a short-lived session token from Akeyless.

#### Step 3: Retrieve a Secret from Akeyless

```shell Python
# Get the API key from Akeyless Vault
secret_request = akeyless.GetSecretValue(names=[secret_path], token=token)
res = api.get_secret_value(secret_request)
API_KEY = res[secret_path]
```

This fetches your API key securely and stores it in the API_KEY variable.

#### Step 4: Use the Secret (API Call Example)

```shell Python
import requests

url = "https://health.data.ny.gov/api/views/jxy9-yhdk/rows.csv"
params = {"api_key": API_KEY, "per_page": 5}
response = requests.get(url, params=params)
```

Uses the API key to fetch public healthcare data as an example.

#### Step 5: Load API Data into a Spark Table

```shell Python
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

#### DLT Version: Using Akeyless in Delta Live Tables

The only change from the non-DLT version is how the data is saved:

```shell Python
@dlt.table(
    name="default.baby_names_by_dlt_pipeline",
    comment="This table is created by a DLT pipeline."
)
def mytable():
    return spark.createDataFrame(pdf)
```

Uses DLT’s @dlt.table decorator to register the DataFrame as a managed DLT table.

### IAM Role Configuration (Summary)

You’ll need:

- IAM Role for EC2: Trusted entity includes ec2.amazonaws.com and Databricks AWS accounts
- IAM Role for cross-account: Allows Databricks to provision compute
- External IDs: Use STORAGE_EXTERNAL-ID and DATABRICKS_WORKSPACE_ID in trust policies

Example trust policy (EC2 role):

```shell JSON
{
  "Effect": "Allow",
  "Principal": {
    "Service": "ec2.amazonaws.com"
  },
  "Action": "sts:AssumeRole"
}
```

Example trust policy (cross-account):

```shell JSON
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::414351767826:root"
  },
  "Action": "sts:AssumeRole",
  "Condition": {
    "StringEquals": {
      "sts:ExternalId": "<STORAGE_EXTERNAL_ID>"
    }
  }
}
```

### Best Practices

- Use Instance Profiles in Databricks to map to IAM roles
- Use Akeyless short-lived tokens to avoid hardcoding secrets
- For Scala or R notebooks, set the secret in spark.conf and read it back in the appropriate language

Example:

```shell Python
# Python cell
spark.conf.set("api.key", API_KEY)
```

```shell Scala
// Scala cell
val apiKey = spark.conf.get("api.key")
println(apiKey)
```