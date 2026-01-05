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
## Application Registration in Active Directory

1. On Azure Portal -> Azure Active Directory -> App Registration:

   <Image alt="1024" border={false} src="https://files.readme.io/407e4bf-image-20210204-103119.png" title="image-20210204-103119.png" />

   Create a "New Registration" which will be use as a Service Account for Akeyless Application.

   <Image alt="1024" border={false} src="https://files.readme.io/ada987e-image-20210204-103139.png" title="image-20210204-103139.png" />

2. Once the resource is created, navigate to **Overview** and note the **Application (client) ID** and **Directory (tenant) ID**.

   <Image alt="1024" border={false} src="https://files.readme.io/4d92388-image-20210204-103159.png" title="image-20210204-103159.png" />

## Configure permission for Microsoft Graph

1. On the left pane, select **API Permission**, select **Microsoft Graph**:

   <Image alt="1348" border={false} src="https://files.readme.io/70a9789-image-20210204-102713.png" title="image-20210204-102713.png" />

2. On the **Request API Permissions** select **Application permission**:

   <Image alt="1024" border={false} src="https://files.readme.io/b8a7809-image-20210204-102948.png" title="image-20210204-102948.png" />

3. Scroll down to **User** and check the **User.ReadWrite.All**:

   <Image alt="1024" border={false} src="https://files.readme.io/f31f1fe-image-20210204-103048.png" title="image-20210204-103048.png" />

4. After Updating the permissions, an admin must grant consent:

   <Image alt="1024" border={false} src="https://files.readme.io/30f6f53-image-20210204-103239.png" title="image-20210204-103239.png" />

   <Image alt="1024" border={false} src="https://files.readme.io/3c8e753-image-20210204-103317.png" title="image-20210204-103317.png" />

### Required Permissions

| Action                           | Permissions                                                                   |
| --- | --- |
| Create/Delete user               | `User.ReadWrite.All`, `Directory.ReadWrite.All`                               |
| Add user to group                | `GroupMember.ReadWrite.All`, `Group.ReadWrite.All`, `Directory.ReadWrite.All` |
| Add user role                    | `RoleManagement.ReadWrite.Directory`                                          |
| Create/Delete application secret | `Application.ReadWrite.OwnedBy`, `Application.ReadWrite.All`                  |

## Certificate & Secrets

1. Navigate to **Certificate & Secrets** on the left pane, create a **New Client Secret**.

   <Image alt="1024" border={false} src="https://files.readme.io/43eaafe-image-20210204-103441.png" title="image-20210204-103441.png" />

2. Save the client secret, as it will not be retrievable once you move to other page/resource:

   <Image alt="1024" border={false} src="https://files.readme.io/68129dc-image-20210204-103506.png" title="image-20210204-103506.png" />
