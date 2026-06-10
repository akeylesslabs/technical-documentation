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

## Flow Overview

1. User signs in to the SRA portal and discovers available targets.
2. User requests access for a target that requires approval.
3. Approver reviews request context and approves or rejects.
4. If approved, the user receives a time-bounded access window.
5. User starts the remote session within the approved window.

## Request Creation

In the portal, users select a target and submit an access request when direct launch is not allowed by policy.

Request payload can include target context and operational justification, based on your policy and workflow design.

## Approval Stage

Approvers receive request notifications through the configured organizational workflow.

Approval decisions should enforce least-privilege and expected session duration boundaries.

## Time-Limited Access Grants

Approved access is expected to be temporary and bounded by policy controls.

After the grant window closes, users must submit a new request unless policy permits direct access.

## Operational Validation

During rollout, validate:

* Request visibility in the portal.
* Approver notification routing.
* Grant duration behavior.
* Session launch behavior after approval.

For session monitoring after approval, see [Session Management](https://docs.akeyless.io/docs/sra-session-management).
