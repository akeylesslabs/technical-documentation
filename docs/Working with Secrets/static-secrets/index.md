---
title: Static Secrets
deprecated: false
hidden: false
link:
  new_tab: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  pages:
    - slug: create-secret
      title: Create a static secret
      type: basic
---
Static secrets are key/value pairs created and updated manually, such as passwords and API tokens. You can store any text-based items in their original format, including configuration files, `JSON` formatted data, and `YAML`formatted data.

The typical process for working with static secrets includes:

1. [Create a Static Secret](doc:create-secret): Start by defining the name and value of the static secret.

2. [Add a Static Secret to an Access Role](doc:add-a-static-secret-to-an-access-role): Allow clients to access the static secret by adding it to a role with the appropriate permissions.

3. [Get a Static Secret Value](doc:retrievestatic): Retrieve the value of a static secret when needed.

4. [Sharing Static Secrets](doc:sharing-static-secrets): Temporarily share with external users who are not part of your organization or do not have general access permissions.

If necessary, you can update a static secret value or create multiple versions of a static secret. See [Update and Version Static Secrets](doc:staticversions).

When a static secret becomes obsolete, you can delete it.

# Tutorial

Check out our tutorial video on [Creating and Updating a Static Secret](https://tutorials.akeyless.io/docs/creating-a-static-secret).
