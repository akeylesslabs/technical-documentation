---
title: Personal & Corporate Areas
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
## Personal Folder

The Akeyless Personal Folder is a unique, private space for each human user who logs in using an email-based authentication method, such as SAML or OIDC. This folder is completely separate from the user's Access Roles, and is for the user's personal use only.

The Personal Folder can be used to store any type of secret or key, including:

* Passwords
* API keys
* SSH keys
* Database credentials
* Certificate keys
* Other sensitive data

The user can create and manage the secrets and keys in their Personal Folder however they see fit. They can also grant access to other users, if needed.

The Personal Folder is protected by the user's own credentials, and is encrypted using Akeyless's zero-knowledge encryption technology. This means that Akeyless cannot access or decrypt the contents of the Personal Folder.

Here are some examples of how the Personal Folder can be used:

* A developer can use the Personal Folder to store their personal API keys and SSH keys.
* A DevOps engineer can use the Personal Folder to store their personal AWS credentials and Kubernetes secrets.
* A security engineer can use the Personal Folder to store their personal SSH keys and database credentials.
* A sales representative can use the Personal Folder to store their personal CRM login credentials and email passwords.

In general, the Personal Folder can be used to store any type of sensitive data that the user needs to access securely, but does not want to be tied to their Access Roles.

Here are some additional details about the Personal Folder:

* The Personal Folder is created automatically for each user when they first log in to Akeyless.
* The Personal Folder is located at the root of the Akeyless hierarchy, and is accessible to the user only.
* The user can create subfolders within their Personal Folder to organize their secrets and keys.
* The user can grant access to other users to specific secrets or keys in their Personal Folder.
* The user can also revoke access to secrets and keys that they have granted to other users.

The Personal Folder is a powerful tool that can help users to securely manage their personal secrets and keys. It is completely private and isolated from the user's Access Roles, making it ideal for storing sensitive data that the user does not want to share with others.

## Corporate Folder

A corporate folder in Akeyless is a folder that is managed by the company and can be used to store and manage secrets and keys for use by multiple users within the organization. Corporate folders are created and managed by Akeyless administrators, and can be configured to allow specific users or groups of users to access and manage the secrets and keys within the folder.

Corporate folders can be used to store a wide variety of secrets and keys, including:

* Infrastructure secrets (e.g., AWS credentials, Kubernetes secrets, etc.)
* Application secrets (e.g., database credentials, API keys, etc.)
* Development secrets (e.g., SSH keys, code signing keys, etc.)
* Other sensitive data

Corporate folders can be used to improve the security and efficiency of secret management within an organization. By centralizing the management of secrets and keys in a corporate folder, organizations can make it easier for users to access the secrets and keys they need, while also reducing the risk of secrets and keys being lost or compromised.

Here are some examples of how corporate folders can be used:

* An IT department can use a corporate folder to store and manage secrets and keys for all of the company's infrastructure, such as AWS credentials, Kubernetes secrets, and database passwords.
* A development team can use a corporate folder to store and manage secrets and keys for their applications, such as API keys and SSH keys.
* A security team can use a corporate folder to store and manage secrets and keys for security tools and applications, such as SSH keys and certificate keys.

In general, corporate folders can be used to store any type of secret or key that the company needs to manage centrally and securely.

Here are some additional details about corporate folders in Akeyless:

* Corporate folders are created and managed by Akeyless administrators.
* Corporate folders can be configured to allow specific users or groups of users to access and manage the secrets and keys within the folder.
* Corporate folders can be nested within other corporate folders to create a hierarchical structure.
* Secrets and keys can be inherited from parent folders, or they can be specific to a particular folder.
* Akeyless administrators can audit all activity on corporate folders, including who accessed what secrets and keys, and when.

Corporate folders are a powerful tool that can help organizations to improve the security and efficiency of their secret management. By centralizing the management of secrets and keys in corporate folders, organizations can make it easier for users to access the secrets and keys they need, while also reducing the risk of secrets and keys being lost or compromised.
