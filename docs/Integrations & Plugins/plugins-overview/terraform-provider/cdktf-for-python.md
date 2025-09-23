---
title: Python CDKTF
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
The Cloud Development Kit for Terraform (CDKTF) allows you to manage your Akeyless resources, such as secrets, roles, and authentication methods, using Terraform without needing to write HashiCorp Configuration Language (HCL). Instead, you can define and manage these resources using **Python**.

# Prerequisites

- [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)  (1.2+)
- [Node.js](https://nodejs.org/en)  and npm (v16)+
- [CDK for Terraform](https://developer.hashicorp.com/terraform/tutorials/cdktf/cdktf-install) 

# Configuration

**Install the library**

Install the CDKTF for Akeyless [package](https://pypi.org/project/akeyless-cdktf/#files)

```python
pip install akeyless-cdktf==1.6.3
```

Once the package is installed, configure the `main.py` and `cdktf.json` files:

**Example for Static Secret creation**

Create a file named `main.py` and edit it as described below:

```python main.py
from akeyless_cdktf import static_secret, provider
from cdktf import App, TerraformStack
from constructs import Construct


login = {
    "accessId":"Access ID",
    "accessKey":"Access Key",
}

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)
        provider.AkeylessProvider(
            self,
            "akeyless",
            api_gateway_address="https://api.akeyless.io",
            api_key_login=[login],
        )
        static_secret.StaticSecret(self, "<Secret Name>", path=f"/path/to/secret", value="SecretValue")


app = App()
MyStack(app, "akeyless")
app.synth()
```

Create a file named `cdktf.json` and edit it as described below:

```json cdktf.json
{
  "language": "python",
  "app": "python main.py",
  "projectId": "Enter your Project ID",
  "sendCrashReports": "false",
  "terraformProviders": [],
  "terraformModules": [],
  "context": {}
}
```

Once both files are configured, run the following command to apply the files: 

```shell
cdktf apply # or plan
```