---
title: SRA RBAC Model
deprecated: false
hidden: false
metadata:
  robots: index
---
Secure Remote Access (SRA) has its own authorization model. It is evaluated independently from the Secrets Management (SM) RBAC model that governs `list`, `read`, `create`, `update`, and `delete` on items, targets, auth methods, and access roles. This page defines that boundary and the rules for combining SRA capabilities on the same path.

## SRA RBAC Is Independent of SM RBAC

An Access Role rule written against a secret or target path can grant SM capabilities (for example `list` or `read`) without granting any SRA capability, and it can grant an SRA capability without granting any SM capability. The two rule types are set independently:

```shell
# SM capability on a path (does not grant SRA access)
akeyless set-role-rule --role-name role1 --path "/infra/db-prod" --capability read

# SRA capability on the same path (independent grant)
akeyless set-role-rule --role-name role1 --path "/infra/db-prod" --rule-type sra-rule --capability allow_access
```

The rule that matters for this page: **a user having `list` (or `read`) on an item under SM RBAC must never be treated as implicit SRA authorization.** Specifically:

* An explicit SM `list` permission on a folder or path — used, for example, so a role can enumerate items, populate a picker, or satisfy a dependency for another feature — must **not** be translated into "allow access" for SRA sessions on the items under that path.
* When an account, role, or path is under SRA RBAC control, SRA must evaluate only the SRA-specific rules (`sra-rule` capabilities) that apply to that path. Any pre-existing SM RBAC grants (including broad `list` grants) on that same path are ignored for the purpose of deciding whether a session can be requested or launched.
* In other words, `list` is not sufficient, and it is not a fallback. If no `sra-rule` capability is present on a path, SRA must deny the request, regardless of what SM capabilities exist there.

This separation exists because SM permissions and SRA permissions answer different questions. SM RBAC governs whether a client can see or manage a secret/target object. SRA RBAC governs whether a human can open a live, credentialed session to the resource that object represents. Conflating the two would let a broad `list` grant (often used for dashboards, sync tooling, or discovery) silently turn into standing access to production infrastructure.

## SRA Permission Capabilities

SRA capabilities are set with `--rule-type sra-rule`:

| Capability | CLI value | Description |
|---|---|---|
| Allow Access | `allow_access` | Full access to log in to the remote resource, no request or justification step required. |
| Request Access | `request_access` | The user must submit a reason and wait for an approver to grant a time-bounded access window before connecting. |
| Justify Access Only | `justify_access_only` | The user can connect immediately, but must first enter a reason for access (no approval step). |
| Approval Authority | — | The user is an eligible approver for SRA access requests on the specified path. |
| Upload Files | — | Allows uploading local files into the remote session. |
| Download Files | — | Allows downloading files from the remote session to the local machine. |

## Approval Authority vs. Request Access

"Who can approve a request" and "who can use/connect to the target" are two separate authorizations, the same way most PAM products separate them. An approver does not need — and, by default in most designs, should not automatically have — the same standing access to the target they are approving. Approval Authority is a review/gatekeeping capability; Request Access (and Allow Access, and Justify Access Only) are connect capabilities.

Because these are separate axes, a single user can legitimately hold both on the same path, for two different reasons:

* They need to approve other people's requests to that resource (Approval Authority), and
* They also, occasionally, need to connect to that same resource themselves (Request Access), so they need a way to request access for themselves rather than being permanently provisioned with standing access.

### Can an Approver Be Forced to Request Approval From Themselves?

No. If a user holds both **Approval Authority** and **Request Access** on the same path, their own request must be approved by a *different* eligible approver. A user is never allowed to approve their own SRA access request.

This is the rule set:

* **Approval Authority + Request Access, same resource:** supported. When this user submits a request on that resource, only another user who also holds Approval Authority on that resource can approve it. The requester cannot approve their own request.
* **Approval Authority + Justify Access Only, same resource:** supported, and self-service. Since Justify Access Only does not require approval, there is no approver/requester conflict to resolve — the user justifies access and connects.
* If a user needs the ability to connect to a resource without waiting on another approver, **Justify Access Only** is the correct capability to pair with Approval Authority, not Request Access.

### Summary

* Support both **Approval Authority** and **Request Access** on the same resource for the same user. When that user requests access, only a *different* approver can approve the request — self-approval is not permitted.
* If a user needs to be able to connect to a resource without depending on another approver, use **Approval Authority** together with **Justify Access Only** instead.
* **UI change:** the Access Roles rule setup must no longer block selecting **Approval Authority** together with **Request Access** on the same rule. (Today, selecting Approval Authority disables Request Access on that rule; this restriction is removed. Approval Authority remains mutually achievable alongside Request Access or Justify Access Only, subject to the self-approval rule above.)

## Related Pages

* [RBAC](https://docs.akeyless.io/docs/rbac)
* [Sub-Claims](https://docs.akeyless.io/docs/sub-claims)
* [Request Access and Approval Flow](https://docs.akeyless.io/docs/sra-request-access-and-approval-flow)
* [Allowed Access IDs and SRA Entitlements](https://docs.akeyless.io/docs/sra-allowed-access-ids-and-sra-entitlements)