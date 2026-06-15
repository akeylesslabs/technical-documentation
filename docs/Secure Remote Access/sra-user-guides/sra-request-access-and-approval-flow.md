---
title: Request Access and Approval Flow
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
Use this page to understand how users request temporary access and how approvers grant time-limited access to targets.

Use this workflow when a target is approval-gated by policy and direct launch is not allowed.

## Flow Overview

1. User signs in to the SRA portal and discovers available targets.
2. User requests access for a target that requires approval.
3. Approver reviews request context and approves or rejects.
4. If approved, the user receives a time-bounded access window.
5. User starts the remote session within the approved window.

## Prerequisites

Before testing this flow, confirm:

1. The user can sign in to the SRA portal.
2. The target is visible to the user but requires approval before launch.
3. Approver assignment and notification routing are already configured for your environment.
4. Session mode prerequisites are configured for the target type (for example, web, SSH, or RDP).

For portal access and target discovery, see [Portal Login and Target Discovery](https://docs.akeyless.io/docs/sra-portal).

## Requester Steps (Portal User)

Use this sequence from the requester perspective:

1. Sign in to the SRA portal.
2. Open the relevant application area (for example, web, SSH, or desktop target list).
3. Search and select the target.
4. Choose the request action shown for approval-gated access.
5. Enter required request details:

* Access justification
* Requested duration (if your workflow exposes this field)
* Any ticket or operational context required by policy

1. Submit the request.
2. Confirm request status changes to a pending state in the portal.

If the request does not appear, refresh the target view and verify you are in the correct target scope.

## Request Creation

In the portal, users select a target and submit an access request when direct launch is not allowed by policy.

Request payload can include target context and operational justification, based on your policy and workflow design.

Minimum request content should be specific enough for approver risk assessment.

Recommended request text includes:

1. Why access is needed now.
2. Which target action is planned.
3. How long access is expected to be used.

## Approval Stage

Approvers receive request notifications through the configured organizational workflow.

Approval decisions should enforce least-privilege and expected session duration boundaries.

## Approver Steps

Use this sequence from the approver perspective:

1. Open the incoming request in your configured approval channel.
2. Verify requester identity and target context.
3. Validate business justification and requested duration.
4. Approve only the minimum duration needed for the task.
5. Reject requests that lack sufficient justification or violate policy.
6. Add decision notes when your workflow supports audit comments.

After approval, confirm the requester can launch only within the approved window.

## Time-Limited Access Grants

Approved access is expected to be temporary and bounded by policy controls.

After the grant window closes, users must submit a new request unless policy permits direct access.

## Post-Approval User Steps

After approval is granted, requester workflow is:

1. Return to the SRA portal target list.
2. Confirm request status is approved.
3. Launch the session before the approval window expires.
4. Complete the required operation.
5. End the session when work is complete.

If launch fails after approval, verify that:

1. Approval has not expired.
2. The selected target still matches the approved request context.
3. Required runtime endpoints are healthy for that session mode.

## Operational Validation

During rollout, validate:

* Request visibility in the portal.
* Approver notification routing.
* Grant duration behavior.
* Session launch behavior after approval.

Add these validation checks for production readiness:

1. Rejected requests remain blocked and cannot be launched.
2. Expired approvals cannot be reused for new launches.
3. New requests are required after grant expiry where policy requires bounded access.
4. Approval and launch events are visible in your audit and session monitoring surfaces.

For session monitoring after approval, see [Session Management](https://docs.akeyless.io/docs/sra-session-management).
