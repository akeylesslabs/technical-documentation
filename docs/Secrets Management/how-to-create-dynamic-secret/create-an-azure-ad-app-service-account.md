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

![1024](https://files.readme.io/407e4bf-image-20210204-103119.png "image-20210204-103119.png")

Create a "New Registration" which will be use as a Service Account for Akeyless Application.

![1024](https://files.readme.io/ada987e-image-20210204-103139.png "image-20210204-103139.png")

2. Once the resource is created, navigate to **Overview** and note the **Application (client) ID** and **Directory (tenant) ID**. 

![1024](https://files.readme.io/4d92388-image-20210204-103159.png "image-20210204-103159.png")

**Configure permission for Microsoft Graph:**

1. On the left pane, select **API Permission** , select **Microsoft Graph**:

![1348](https://files.readme.io/70a9789-image-20210204-102713.png "image-20210204-102713.png")

2. On the **Request API Permissions** select **Application permission** :

![1024](https://files.readme.io/b8a7809-image-20210204-102948.png "image-20210204-102948.png")

3. Scroll down to **User** and check the **User.ReadWrite.All**: 

![1024](https://files.readme.io/f31f1fe-image-20210204-103048.png "image-20210204-103048.png")

**The following permissions required:**

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Action:
      </th>

      <th>
        Permissions:
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        Create/Delete user
      </td>

      <td>
        User.ReadWrite.All, Directory.ReadWrite.All
      </td>
    </tr>

    <tr>
      <td>
        Add user to group
      </td>

      <td>
        GroupMember.ReadWrite.All, Group.ReadWrite.All and Directory.ReadWrite.All
      </td>
    </tr>

    <tr>
      <td>
        Add user role
      </td>

      <td>
        RoleManagement.ReadWrite.Directory
      </td>
    </tr>

    <tr>
      <td>
        Create\Delete Application secret
      </td>

      <td>
        Application.ReadWrite.OwnedBy, Application.ReadWrite.All
      </td>
    </tr>
  </tbody>
</Table>

4. After Updating the permissions, an admin must grant consent: 

![1024](https://files.readme.io/30f6f53-image-20210204-103239.png "image-20210204-103239.png")

![1024](https://files.readme.io/3c8e753-image-20210204-103317.png "image-20210204-103317.png")

**Certificate & Secrets:**

1. Navigate to **Certificate & Secrets** on the left pane, create a **New Client Secret**. 

![1024](https://files.readme.io/43eaafe-image-20210204-103441.png "image-20210204-103441.png")

2. Save the client secret, as it will not be retrievable once you move to other page/resource: 

![1024](https://files.readme.io/68129dc-image-20210204-103506.png "image-20210204-103506.png")
