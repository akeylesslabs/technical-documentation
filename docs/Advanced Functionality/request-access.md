---
title: Request Access
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
Akeyless allows users to request temporary access or to elevate their current permissions for specific items using a built-in approval workflow which requires approval from the system admin. 

Admins can view, and either approve or decline those requests directly from the Akeyless [Event Center](https://docs.akeyless.io/docs/event-center) where you can forward those events to any of the supported endpoints like ServiceNow, etc. 

This option needs to be enabled by an admin in the account under Account settings navigate to **Settings > Items Settings > Request access**.

While default access can be assigned via [Role-based Access Control (RBAC)](https://docs.akeyless.io/docs/rbac),  this article discusses how to easily manage your access requests using customizable notifications and easy workflow to approve such requests

> 👍 Note
>
> Upon approval of an Access Request a temporary Access Role will be created with details about the request ID under a dedicated folder `/Access Requests/<Requestor AccessID>/<ID>`, and will be deleted automatically within an hour.

# Requesting Access  From the CLI

In order to request access to an item, use the following command:

```shell
akeyless request-access --name <name> --type <item type> --capability <permissions needed> --comment <comment about the request>
```

Where:

* `name`: Name of the item to which access is requested.
* `type`: The type of item to which access is requested. The supported types are Static Secret and Target.
* `capability`: List of the required capabilities, the supported options are: `read`, `update`, `delete`
* `comment`: A comment about the request.

Once requested, a new event will be triggered inside your [Event Center](https://docs.akeyless.io/docs/event-center), to view the request, on the event from the action menu click on **View Request** and choose either to approve or decline this request.

# Requesting Access From the Console

On a [Static Secret](https://docs.akeyless.io/docs/static-secrets), or [Target](https://docs.akeyless.io/docs/targets) Item, go to the top right-hand corner and select the three-dot options menu, click on **Request Access**, and choose the desired permissions.
