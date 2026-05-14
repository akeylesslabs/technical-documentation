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

1. In the Azure Portal, go to **Azure Active Directory**, then **App registration**:

   ![On Azure Portal -> Azure Active Directory -> App Registration](https://files.readme.io/407e4bf-image-20210204-103119.png)

   Create a **New Registration** that will be used as a service account for the Akeyless application.

   ![Create a "New Registration" which will be use as a Service Account for Akeyless Application.](https://files.readme.io/ada987e-image-20210204-103139.png)

2. Once the resource is created, navigate to **Overview** and note the **Application (client) ID** and **Directory (tenant) ID**.

   ![Once the resource is created, navigate to Overview and note the Application (client) ID and Directory (tenant) ID.](https://files.readme.io/4d92388-image-20210204-103159.png)

## Configure permission for Microsoft Graph

1. In the left pane, select **API Permission**, then select **Microsoft Graph**:

   ![On the left pane, select API Permission, select Microsoft Graph.](https://files.readme.io/70a9789-image-20210204-102713.png)

2. On **Request API Permissions**, select **Application permission**:

   ![On the Request API Permissions, select Application permission.](https://files.readme.io/b8a7809-image-20210204-102948.png)

3. Scroll down to **User** and check the **User.ReadWrite.All**:

   ![Scroll down to User and check the User.ReadWrite.All](https://files.readme.io/f31f1fe-image-20210204-103048.png)

4. After updating the permissions, an admin must grant consent:

   ![After Updating the permissions, an admin must grant consent.](https://files.readme.io/30f6f53-image-20210204-103239.png)

   ![After Updating the permissions, an admin must grant consent.](https://files.readme.io/3c8e753-image-20210204-103317.png)

### Required Permissions

| Action | Permissions |
| --- | --- |
| Create/Delete user | `User.ReadWrite.All`, `Directory.ReadWrite.All` |
| Add user to group | `GroupMember.ReadWrite.All`, `Group.ReadWrite.All`, `Directory.ReadWrite.All` |
| Add user role | `RoleManagement.ReadWrite.Directory` |
| Create/Delete application secret | `Application.ReadWrite.OwnedBy`, `Application.ReadWrite.All` |

## Certificate & Secrets

1. In the left pane, navigate to **Certificate & Secrets**, then create a **New Client Secret**.

   ![Navigate to Certificate and Secrets on the left pane, create a New Client Secret.](https://files.readme.io/43eaafe-image-20210204-103441.png)

2. Save the client secret, as it will not be retrievable once you navigate elsewhere:

   ![Save the client secret, as it will not be retrievable once you navigate elsewhere.](https://files.readme.io/68129dc-image-20210204-103506.png)
