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

> **Deprecation notice:** HashiCorp deprecated CDKTF on 2025-12-10 and no longer supports or maintains it. The `akeyless-cdktf` package remains available on PyPI, but the upstream CDKTF framework is end-of-life. Consider these alternatives for new projects:
>
> * [Terraform provider with HCL](https://docs.akeyless.io/docs/terraform-provider) — manage Akeyless resources using standard HCL configuration
> * [Pulumi Akeyless provider](https://www.pulumi.com/registry/packages/akeyless/) — manage Akeyless resources using Python or other languages
> * [Akeyless Python SDK](https://docs.akeyless.io/docs/python-sdk-1) — programmatic access to Akeyless without an IaC framework

## Prerequisites

* [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) (1.2+)
* [Node.js](https://nodejs.org/en) (v17–v20) and npm
* [CDK for Terraform](https://developer.hashicorp.com/terraform/cdktf/cli-reference/cli-configuration)

## Configuration

### Install the Library

Install the CDKTF for Akeyless [package](https://pypi.org/project/akeyless-cdktf/#files)

```shell
pip install akeyless-cdktf==2.0.1
```

Once the package is installed, configure the `main.py` and `cdktf.json` files:

### Example for Static Secret Creation

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
