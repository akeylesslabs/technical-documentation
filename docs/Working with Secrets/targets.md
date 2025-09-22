---
title: Targets
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
A Target is an endpoint for a secret such as a database, cloud platform, or server. Targets help admins keep their secrets and endpoints more organized. Instead of adding an endpoint to each secret separately, a Target can be used.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/7481a59-Creates_Targets.png",
        "target.png",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


Using targets has three primary advantages:

- Streamline your creation flow: Creating a target that has the credentials for a specific endpoint will allow you to reference said endpoint in other items like [Dynamic Secrets](doc:how-to-create-dynamic-secret), [Rotated Secrets](doc:rotated-secrets) and more, without having to input the details again every time. You can have multiple secrets point to the same Target, making it easy for different teams to connect and minimizing the number of Targets in your organization.

- Keep your information safe: Using the [Role-based Access Control (RBAC)](doc:rbac) capabilities, users are not required to have access to, or knowledge of, your privileged account credentials. Simply grant users with `list` permissions on those Target items to provide them with the ability to create [Dynamic Secrets](doc:how-to-create-dynamic-secret) or [Rotated Secrets](doc:rotated-secrets). For example, two [Database Dynamic Secrets](doc:create-dynamic-secret-to-sql-db) can be created using the same existing Target, but each with its own set of permissions.

- Don't break the credential chain: Targets can also be used to sync encryption keys with an external KMS, or to define a Target to be used with our [Rotated Secrets](doc:rotated-secrets) to manage and automate your privilege account credentials rotation. This allows every item referencing the target to be up to date on the necessary information and to stay usable even after rotations are done.

# Tutorial

Check out our tutorial video on [Creating and Configuring Targets](https://tutorials.akeyless.io/docs/creating-targets).