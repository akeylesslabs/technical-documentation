---
title: Python - API Key
description: Recipe Description
hidden: true
recipe:
  color: '#018FF4'
  icon: 🦉
---
```python Python
# Import the required packages
import akeyless

Access_id = ""
Access_key = ""
StaticSecretName = 'Secret Name'  # Static Secret Name
DynamicSecretName = 'Dynamic Secret Name'  # Dynamic Secret Name

#Set API URL 
configuration = akeyless.Configuration(host="https://api.akeyless.io")

# Create a context with an instance of the API client
with akeyless.ApiClient() as api_client:
    # Create an instance of the API class
    api = akeyless.V2Api(api_client)

# Authenticate to Akeyless
auth = akeyless.Auth(access_id, access_key)
res = api.auth(auth)
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

# Install and Import "Akeyless" package

<!-- python@1-2 -->

First, install the Akeyless package on the client machine, and then, import the package on Python.

To install the package use the following command: 

`pip install akeyless`

To import (from Python session) use:  
`import akeyless`

# Set variables

<!-- python@4-7 -->

Set the following variables in order to generate token that will allow you to communicate with Akeyless.

"Access_Id", "Access_key", "DynamicSecretName" and "StaticSecretName" are optional variables (you can set it inside the code itself).

"Access_Id" - The access ID of the AWS_IAM Auth method.  
"Access_Key" - The access Key of the AWS_IAM Auth method.  
"StaticSecretName" - Static Secret Name.  "DynamicSecretName" - Dynamic Secret Name.

# API endpoint configuration

<!-- python@9-10 -->

Defining the host is optional and defaults to https://api.akeyless.io.
Use port 8081 in order to use a private API endpoint host = "https://<gateway.company>.com:8081"

# Set up the Akeyless client

<!-- python@12-15 -->

Configure the API client to work with Akeyless by creating an instance of the API class.

# Authenticate to Akeyless

<!-- python@17-20 -->

Generate a token using your Access ID, Access Type and the cloud_id.  
This token will allow the authentication to Akeyless.

# Create a new Static Secret

<!-- python@22-25 -->

Create a new Static Secret using a token.  
name = The Static Secret name.  
value = The value of the secret.

# Get a Static Secret

<!-- python@27-30 -->

get a Static Secret using a token.  
names = The Static secret name.

# Get a Dynamic Secret

<!-- python@32-35 -->

Get a Dynamic Secret using a token.  
name = The Static Secret name.

# Create and set a new role

<!-- python@37-46 -->

Create and set a new role using a token.  
This command will allow you to create a new access role and set the permissions for the access role.

# Auth method creation

<!-- python@48-50 -->

Create an Authentication method using a token.

# Role and auth method association

<!-- python@52-54 -->

Associate a Role with an Authentication Method.  
This command allows you to associate an authentication method with an access role