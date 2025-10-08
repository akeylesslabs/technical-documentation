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
      title: Create a Static Secret
      type: basic
---
Static Secrets are key/value pairs created and updated manually, such as passwords and API tokens. Text-based items can be stored in their original format, including configuration files, JSON formatted data, and YAML formatted data.

The typical process for working with Static Secrets includes:

1. [Create a Static Secret](doc:create-secret): Start by defining the name and value of the Static Secret.

2. [Add a Static Secret to an Access Role](doc:add-a-static-secret-to-an-access-role): Allow clients to access the Static Secret by adding it to a role with the appropriate permissions.

3. [Get a Static Secret Value](doc:retrievestatic): Retrieve the value of a Static Secret when needed.

4. [Sharing Static Secrets](doc:sharing-static-secrets): Temporarily share with external users who are not part of your organization or do not have general access permissions.

If necessary, a Static Secret value can be updated or have multiple versions. See [Update and Version Static Secrets](doc:staticversions).

When a Static Secret becomes obsolete, it can be deleted.

# Tutorial

Check out our tutorial video on [Creating and Updating a Static Secret](https://tutorials.akeyless.io/docs/creating-a-static-secret).