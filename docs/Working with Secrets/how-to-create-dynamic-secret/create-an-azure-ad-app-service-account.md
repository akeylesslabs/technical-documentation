---
title: Create An Azure AD App & Service Account
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
**Application Registration in Active Directory:**

1. On Azure Portal -> Azure Active directory -> App Registration: 

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/407e4bf-image-20210204-103119.png",
        "image-20210204-103119.png",
        1024,
        609,
        "#252527"
      ]
    }
  ]
}
[/block]
Create a "New Registration" which will be use as a Service Account for Akeyless Application.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ada987e-image-20210204-103139.png",
        "image-20210204-103139.png",
        1024,
        731,
        "#181819"
      ]
    }
  ]
}
[/block]
2. Once the resource is created, navigate to **Overview** and note the **Application (client) ID** and **Directory (tenant) ID**. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/4d92388-image-20210204-103159.png",
        "image-20210204-103159.png",
        1024,
        580,
        "#1d2024"
      ]
    }
  ]
}
[/block]
**Configure permission for Microsoft Graph:**

1. On the left pane, select **API Permission** , select **Microsoft Graph**:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/70a9789-image-20210204-102713.png",
        "image-20210204-102713.png",
        1348,
        664,
        "#f5f7f8"
      ]
    }
  ]
}
[/block]
2. On the **Request API Permissions** select **Application permission** :
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/b8a7809-image-20210204-102948.png",
        "image-20210204-102948.png",
        1024,
        545,
        "#f6f7f9"
      ]
    }
  ]
}
[/block]
3. Scroll down to **User** and check the **User.ReadWrite.All**: 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/f31f1fe-image-20210204-103048.png",
        "image-20210204-103048.png",
        1024,
        752,
        "#f8f9fa"
      ]
    }
  ]
}
[/block]
**The following permissions required: **
[block:parameters]
{
  "data": {
    "h-0": "Action:",
    "h-1": "Permissions:",
    "0-0": "Create/Delete user",
    "0-1": "User.ReadWrite.All, Directory.ReadWrite.All",
    "1-0": "Add user to group",
    "1-1": "GroupMember.ReadWrite.All, Group.ReadWrite.All and Directory.ReadWrite.All",
    "2-0": "Add user role",
    "2-1": "RoleManagement.ReadWrite.Directory",
    "3-0": "Create\\Delete Application secret",
    "3-1": "Application.ReadWrite.OwnedBy, Application.ReadWrite.All"
  },
  "cols": 2,
  "rows": 4
}
[/block]
4. After Updating the permissions, an admin must grant consent: 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/30f6f53-image-20210204-103239.png",
        "image-20210204-103239.png",
        1024,
        468,
        "#f6f5f4"
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
        "https://files.readme.io/3c8e753-image-20210204-103317.png",
        "image-20210204-103317.png",
        1024,
        474,
        "#f4f6f5"
      ]
    }
  ]
}
[/block]
**Certificate & Secrets:**

1. Navigate to **Certificate & Secrets** on the left pane, create a **New Client Secret**. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/43eaafe-image-20210204-103441.png",
        "image-20210204-103441.png",
        1024,
        696,
        "#f6f7f8"
      ]
    }
  ]
}
[/block]
2. Save the client secret, as it will not be retrievable once you move to other page/resource: 

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/68129dc-image-20210204-103506.png",
        "image-20210204-103506.png",
        1024,
        578,
        "#f0f3f6"
      ]
    }
  ]
}
[/block]