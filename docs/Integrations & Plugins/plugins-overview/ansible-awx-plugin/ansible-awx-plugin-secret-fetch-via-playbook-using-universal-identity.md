---
title: Ansible AWX Plugin - secret fetch via playbook using Universal Identity
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Below, please find an example of using Ansible AWX with Akeyless Platform for fetching credentials, utilizing Akeyless [Universal Identity](doc:universal-identity). 
[block:api-header]
{
  "title": "Prerequisites"
}
[/block]
The section refers to changes that should be done in the awx machine (awx-task container).
1. Set akeyless-vault url in: VAULT_ADDR environment variable:
[block:code]
{
  "codes": [
    {
      "code": "export VAULT_ADDR=https://hvp.akeyless.io ",
      "language": "shell"
    }
  ]
}
[/block]
2. You’ll need to configure the Akeyless temporary API token (this is the recommended and the more secure method). For token rotation, please [read more here](doc:universal-identity). The rotated token should be saved in this file `/var/lib/awx/.vault-token` 
[block:api-header]
{
  "title": "Configuring AWX Plugin"
}
[/block]
To use the vault plugin, complete the following procedure:
1. Download [this plugin](https://github.com/TerryHowe/ansible-modules-hashivault) and add it to your lookup_plugins directory as described in the link.
2. Create a new template, according to the below:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/a66da1f-image.png",
        "image.png",
        1700,
        826,
        "#fafafa"
      ]
    }
  ]
}
[/block]

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/7f88aa4-image_2.png",
        "image (2).png",
        1037,
        217,
        "#fafbfb"
      ]
    }
  ]
}
[/block]
After successful job launch you will see the following:  
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/fdcc990-image_1.png",
        "image (1).png",
        1727,
        876,
        "#f3f3f3"
      ]
    }
  ]
}
[/block]
For an additional ways to work with Ansible AWX, see [Ansible AWX Plugin - secret fetch via playbook](doc:ansible-awx-plugin-secret-fetch-via-playbook-1).