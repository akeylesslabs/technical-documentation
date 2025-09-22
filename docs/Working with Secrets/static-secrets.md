---
title: Static Secrets
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: create-secret
      title: Create a static secret
---
Static secrets are `key/value` pairs that you create and update manually, such as passwords and API tokens. Any text-based items can be stored within their original format, including config files, `JSON` and `YAML`, etc. 

The typical flow for working with static secrets is:

1. [Create a Static Secret](doc:create-secret): Get started by defining the name and value of the static secret.

2. [Add a Static Secret to an Access Role](doc:add-a-static-secret-to-an-access-role): Enable clients to access  
   the static secret by adding it to a role, with the appropriate permissions.

3. [Get a Static Secret Value](doc:retrievestatic): Get the value of a static secret when you need it.

If required, you can update a static secret value, or create multiple versions of a static secret. See [Update and Version Static Secrets](doc:staticversions).

4. [Sharing Static Secrets](doc:sharing-static-secrets): to temporarily share with external users that are not part of your organization or who don't have access permission to those items in general. 

When a static secret becomes obsolete, you can delete it.



# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/creating-a-static-secret" target="_blank" style="color: #00e">Creating and Updating a Static Secret</a>.