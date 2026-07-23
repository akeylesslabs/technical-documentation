---
title: SRA RBAC Model
deprecated: false
hidden: false
metadata:
  robots: index
---
Secure Remote Access (SRA) has its own authorization model. It is evaluated independently from the **SM** RBAC model that governs `list`, `read`, `create`, `update`, and `delete` on items, targets, auth methods, and access roles. This page defines that boundary and the rules for combining SRA capabilities on the same path.

## SRA RBAC Is Independent of SM RBAC

An Access Role rule written against a secret or target path can grant SM capabilities (for example `list` or `read`) without granting any SRA capability, and it can grant an SRA capability without granting any SM capability. The two rule types are set independently:

```shell
# SM capability on a path (does not grant SRA access)
akeyless set-role-rule --role-name role1 --path "/infra/db-prod" --capability read

# SRA capability on the same path (independent grant)
akeyless set-role-rule --role-name role1 --path "/infra/db-prod" --rule-type sra-rule --capability allow_access
```

This separation exists because SM permissions and SRA permissions answer different questions. SM RBAC governs whether a client can see or manage a secret/target object. SRA RBAC governs whether a human can open a live, credentialed session to the resource that object represents.

## SRA Permission Capabilities

SRA capabilities are set with `rule-type sra-rule`:

| Capability          | CLI value             | Description                                                                                                                        |
| ------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Allow Access        | `allow_access`        | Full access to log in to the remote resource, no request or justification step required.                                           |
| Request Access      | `request_access`      | The user must submit a reason and wait for an approver to grant a time-bounded access window before connecting.                    |
| Justify Access Only | `justify_access_only` | The user can connect immediately, but must first enter a reason for access (no approval step).                                     |
| Approval Authority  | `approval_authority`  | The user is an eligible approver for SRA access requests on the specified path.                                                    |
| Upload Files        | `upload_files`        | Allows uploading local files into a remote target over SFTP. Granted on [SSH Cert Issuer](doc:sra-ssh-certificates)                |
| Download Files      | `download_files`      | Allows downloading files from a remote target to a local machine over SFTP. Granted on [SSH Cert Issuer](doc:sra-ssh-certificates) |

## Approval Authority vs. Request Access

"Who can approve a request" and "who can use/connect to the target" are two separate authorizations. An approver does not need- and, by default should not automatically have the same standing access to the target they are approving. Approval Authority is a review/gatekeeping capability; Request Access (and Allow Access, and Justify Access Only) are connect capabilities.

Because these are separate axes, a single user can legitimately hold both on the same path, for two different reasons:

- They need to approve other people's requests to that resource (Approval Authority), and
- They also, occasionally, need to connect to that same resource themselves (Request Access), so they need a way to request access for themselves rather than being permanently provisioned with standing access.

### Can an Approver Be Forced to Request Approval From Themselves?

No. If a user holds both **Approval Authority** and **Request Access** on the same path, their own request must be approved by a _different_ eligible approver. A user is never allowed to approve their own SRA access request.

This is the rule set:

- **Approval Authority + Request Access, same resource:** supported. When this user submits a request on that resource, only another user who also holds Approval Authority on that resource can approve it. The requester cannot approve their own request.
- **Approval Authority + Justify Access Only, same resource:** supported, and self-service. Since Justify Access Only does not require approval, there is no approver/requester conflict to resolve - the user justifies access and connects.
- If a user needs the ability to connect to a resource without waiting on another approver, **Justify Access Only** is the correct capability to pair with Approval Authority, not Request Access.

## Related Pages

- [RBAC](https://docs.akeyless.io/docs/rbac)
- [Sub-Claims](https://docs.akeyless.io/docs/sub-claims)
- [Request Access and Approval Flow](https://docs.akeyless.io/docs/sra-request-access-and-approval-flow)

<br />
