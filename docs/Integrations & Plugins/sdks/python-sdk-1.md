---
title: Python SDK
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
The Akeyless [Python SDK](https://github.com/akeylesslabs/akeyless-python) makes it easy to integrate your **Python** applications, libraries, or scripts with Akeyless. The following guide shows a typical integration.

# Installation

Install the Akeyless **Python** pacakge using `pip`:

```shell
pip install akeyless
```

Import `akeyless` package:

```python
import akeyless
```

# Configuration

Create and configure an instance of Akeyless Client:

```python
# using public API endpoint
configuration = akeyless.Configuration(
        host = "https://api.akeyless.io"
)

api_client = akeyless.ApiClient(configuration)
api = akeyless.V2Api(api_client)
```

To work with Your [Gateway](https://docs.akeyless.io/docs/api-gw) set `host` with your Gateway API endpoint on port `8081`.

# Authentication

The Akeyless **Python** SDK supports multiple [Authentication Methods](doc:access-and-authentication-methods).

## API Key

To use an [API Key](doc:api-key) for authentication set the following:

```python
body = akeyless.Auth(access_id='Access ID', access_key='Access Key')
res = api.auth(body)
token = res.token
```

Make sure to set your `Access ID` and `Access Key` in the relevant places. The received token should be provided for every request that requires authentication.

## UID

Another way to use the SDK is by using [Universal Identity](https://docs.akeyless.io/docs/universal-identity)tokens:

```python
body = akeyless.GetSecretValue(names=['my-secret'], uid_token='<some-token>')
res = api.get_secret_value(body)
print(res['my-secret'])
```

Note that when working with  **Universal Identity** you should use the`uid_token`, while for any other authentication method, you should use `token`.

## Using cloud ID

To work with a Cloud-based Auth, install the `akeyless_cloud_id` [package](https://github.com/akeylesslabs/akeyless-python-cloud-id):

```shell
pip install akeyless_cloud_id
```

### Authenticate using cloud ID

Choose the right example based on your cloud provider:

```python AWS
from akeyless_cloud_id import CloudId

cloud_id_generator = CloudId()
cloud_id = cloud_id_generator.generate()

body = akeyless.Auth(access_id='Access Id', access_type='aws_iam', cloud_id=cloud_id)
res = api.auth(body)
token = res.token
```
```python GCP
from akeyless_cloud_id import CloudId

cloud_id_generator = CloudId()
cloud_id = cloud_id_generator.generateGcp()

body = akeyless.Auth(access_id='Access Id', access_type='gcp', cloud_id=cloud_id)
res = api.auth(body)
token = res.token
```
```python Azure
from akeyless_cloud_id import CloudId

cloud_id_generator = CloudId()
cloud_id = cloud_id_generator.generateAzure()

body = akeyless.Auth(access_id='Access Id', access_type='azure_ad', cloud_id=cloud_id)
res = api.auth(body)
token = res.token
```

Make sure to set your `Access Id` in the relevant place.

# Examples

**Get static secret value(s)**:

```python
body = akeyless.GetSecretValue(names=['secret-1', 'secret-2'], token=token)
res = api.get_secret_value(body)
print(res['secret-1'])
print(res['secret-2'])
```

**Create a new static secret**

```python
body = akeyless.CreateSecret(name='new-secret', value='my-password', token=token)
api.create_secret(body)
```

**Create a new Role**

```python
body = akeyless.CreateRole(token=token, name='dev-role')
api.create_role(body)

body = akeyless.SetRoleRule(capability=['list', 'read'], path='/dev/*',
        role_name='dev-role', token=token)

for rule_type in ['role-rule', 'item-rule', 'auth-method-rule']:
    body.rule_type = rule_type
    api.set_role_rule(body)
```

**Create a new Authentication Method**

```python
body = akeyless.CreateAuthMethod(name='dev-api-key', token=token)
res = api.create_auth_method(body)

print(res.access_id)
print(res.access_key)
```

**Associate a Role with an Authentication Method**

```python
body = akeyless.AssocRoleAuthMethod(am_name='dev-api-key', role_name='dev-ro',
        token=token)
api.assoc_role_auth_method(body)
```

# API Reference

For a detailed API reference, see [here](https://github.com/akeylesslabs/akeyless-python).
