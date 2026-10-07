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

Admins can view, and either approve or decline those requests directly from the Akeyless [Event Center](https://docs.akeyless.io/docs/event-center) where you can forward those events to any of the supported endpoints like ServiceNow, and so on.

This option needs to be enabled by an admin in the account under Account settings navigate to **Settings > Items Settings > Request access**.

While default access can be assigned by way of [Role-Based Access Control (RBAC)](https://docs.akeyless.io/docs/rbac), this article discusses how to easily manage your access requests using customizable notifications and easy workflow to approve such requests

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  Upon approval of an Access Request, a temporary Access Role is created with details about the request ID under a dedicated folder `/Access Requests/<Requestor AccessID>/<ID>`. The role is deleted automatically when the granted access TTL expires (60 minutes by default).
</Callout>

## Required RBAC Permissions for Request Access Approval

To approve or decline Access Requests on **items and targets**, the approver's Access Role requires:

* **Approve Access Request permission**: Set on the Access Role, with one of the following values:
  * `none`: The role cannot approve Access Requests (default).
  * `scoped`: The role can approve Access Requests, with Auth Method visibility limited to the scope of the request.
  * `all`: The role can approve Access Requests, with visibility of all Auth Methods.
* **Item/Target rule**: The requested capabilities (`Read`, `Update`, and/or `Delete`) on the relevant item or target path.

Approvers can only grant capabilities they already hold on the requested item or target.

To set the permission with the CLI:

```shell
akeyless update-role \
--name <approver-role-name> \
--approve-access-request scoped
```

## Requesting Access with the CLI

To request access to an item, use the following command:

```shell
akeyless request-access \
--name <item-name> \
--type <item-type> \
--capability <permissions-needed> \
--requested-ttl <minutes> \
--description <reason-for-request>
```

Where:

* `name`: Name of the item to which access is requested.
* `type`: The type of item to which access is requested. The supported types are Static Secret and Target.
* `capability`: List of the required capabilities. The supported options are `read`, `update`, and `delete`.
* `requested-ttl`: How long access is needed, in minutes. The allowed range is 1 to 1440 (24 hours). Defaults to 60.
* `description`: The reason for the request. Replaces the deprecated `comment` parameter.

## Approving or Declining a Request

Once access was requested, a new event will be triggered inside the [Event Center](https://docs.akeyless.io/docs/event-center), to view the request, on the event from the action menu click on **View Request** and choose either to approve or decline this request.

## Requesting Access from the Console

On a [Static Secret](https://docs.akeyless.io/docs/static-secrets), or [Target](https://docs.akeyless.io/docs/targets) Item, go to the top right-hand corner and select the three-dot options menu, click on **Request Access**, and choose the desired permissions.
