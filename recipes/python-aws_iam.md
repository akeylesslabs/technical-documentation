---
title: Python  - AWS_IAM
description: Recipe Description
hidden: false
recipe:
  color: '#018FF4'
  icon: 🦉
---
```python Python
# Import the required packages
import akeyless
from akeyless_cloud_id import CloudId

Access_Id = ''  # Access ID of the AWS_IAM Auth method
StaticSecretName = 'Secret Name'  # Static Secret Name
DynamicSecretName = 'Dynamic Secret Name'  # Dynamic Secret Name

# Cloud identity authentication
cloud_id_generator = CloudId()
cloud_id = cloud_id_generator.generate()

# Set API URL 
configuration = akeyless.Configuration(host="https://api.akeyless.io")

# Create a context with an instance of the API client
with akeyless.ApiClient() as api_client:
    # Create an instance of the API class
    api = akeyless.V2Api(api_client)

# Authenticate to Akeyless
body = akeyless.Auth(Access_Id, access_type='aws_iam', cloud_id=cloud_id)
res = api.auth(body)
token = res.token

# Create a new secert
body = akeyless.CreateSecret(
    name='Secret_Name', value='Secret_Value', token=token)
api.create_secret(body)

# Get a static secret
body = akeyless.GetSecretValue(names=[StaticSecretName], token=token)
res = api.get_secret_value(body)
print(res[StaticSecretName])

# Get a dynamic secret
body = akeyless.GetDynamicSecretValue(name=DynamicSecretName, token=token)
res = api.get_dynamic_secret_value(body)
print(res)

# Create and set a new role
body = akeyless.CreateRole(token=token, name='Role-Name')
api.create_role(body)

body = akeyless.SetRoleRule(capability=['list', 'read'], path='/*',
        role_name='Role-Name', token=token)

for rule_type in ['role-rule', 'item-rule', 'auth-method-rule']:
    body.rule_type = rule_type
    api.set_role_rule(body)

# Create an Authentication method
body = akeyless.CreateAuthMethod(name='Method-Name', token=token)
res = api.create_auth_method(body)

# Role and Authentication Method authentication
body = akeyless.AssocRoleAuthMethod(am_name='Method-Name', role_name='Role-Name',token=token)
api.assoc_role_auth_method(body)

```

```json Response Example
{"success":true}
```

# Import the required packages

<!-- python@1-3 -->

First, install the `akeyless` and `akeyless_cloud_id` packages on the client machine, and then, import the packages on in your Python session. 

To install the package use the following commands: 

`pip install akeyless`
`pip install akeyless_cloud_id`

# Set variables

<!-- python@5-11 -->

Set the following variables in order to generate token that will allow you to communicate with Akeyless.

`Access_Id`, `StaticSecretName` and `DynamicSecretName` are optional variables (you can set it inside the code itself).

`Access_Id` - The access ID of the AWS_IAM Auth method.
`StaticSecretName` - Static Secret Name.  `DynamicSecretName` - Dynamic Secret Name.

Line 11 is where the AWS SDK will be used to get the cloud identity from the AWS metadata services used for authorization.

*Note that an AWS IAM role is required in order to successfully retrieve this data*

# API endpoint configuration

<!-- python@13-14 -->

Defining the host is optional and defaults to https://api.akeyless.io.
use port 8081 in order to use your own gateway API endpoint host = `https://gateway.example.com:8081`

# Set up Akeyless client

<!-- python@16-19 -->

Configure the API client to work with Akeyless by creating an instance of the API class.

# Authenticate to Akeyless

<!-- python@21-24 -->

Generate a token using your Access ID, Access Type and the cloud_id. 
This token will allow the authentication to Akeyless.

# Create a new Static Secret

<!-- python@26-29 -->

Create a new Static Secret using a token.
name = The Static Secret name. 
value = The value of the secret.

# Get a Static Secret

<!-- python@31-34 -->

get a Static Secret using a token.
names = The Static secret name.

# Get a Dynamic Secret

<!-- python@36-39 -->

Get a Dynamic Secret using a token.
name = The Static Secret name.

# Create and set a new role

<!-- python@5,41-50 -->

Create and set a new role using a token.
This command will allow you to create a new access role and set the permissions for the access role.

In this example we are granting permission to all secrets as well as permission to list and read all Access Roles and all Auth Method associations the access ID of the AWS Auth Method listed on line 5 has permission to share.

# Auth method creation

<!-- python@52-57 -->

Create an Authentication method using a token.

# Role and auth method association

<!-- python@59-61 -->

Associate a Role with an Authentication Method.
This command allows you to associate an authentication method with an access role