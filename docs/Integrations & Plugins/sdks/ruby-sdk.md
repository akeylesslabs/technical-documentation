---
title: Ruby SDK
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
The Akeyless SDK for Ruby makes it easy for you to integrate your Ruby applications, libraries, or scripts with the Akeyless Platform secret management services.  
The below Ruby code examples show a typical sequence of integrating secrets into your application.

# Installation

**Install the Akeyless gem package**

```ruby
gem install akeyless
```

# Getting Started

Please follow the installation procedure and then run the following code:

```ruby
require 'akeyless'

# default: public API Gateway
config = Akeyless::Configuration.new

# use port 8081 exposed by the deployment:
config.server_index = nil
config.scheme = 'https'
config.host =  'gateway.company.com:8081'

# use port 8080 exposed by the deployment with /v2 prefix: 
config.server_index = nil
config.scheme = 'https'
config.host =  'gateway.company.com:8080/v2'


api = Akeyless::V2Api.new(Akeyless::ApiClient.new(config))

# auth using email and password
body = Akeyless::Auth.new
body.admin_email = 'foo@example.com'
body.admin_password = 'strong-password'
body.access_type = "password"

result = api.auth(body)
token = result.token

# get secret value using the token
body = Akeyless::GetSecretValue.new
body.token = tokenbody.names = ['my-secret']
result = api.get_secret_value(body)
```

# API Reference

For a detailed API reference, see [here](https://github.com/akeylesslabs/akeyless-ruby).