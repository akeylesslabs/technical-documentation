---
title: Policies
deprecated: false
hidden: false
metadata:
  robots: index
---
Policies can be used to review available **secret**, **identity**, and **certificate** policies, and to enable or adjust policy status based on findings from Dashboard and Inventory.

## Prerequisites

Policies is shown only when:

- The account has the Identity and Secrets Intelligence feature enabled.
- The user has admin-level Console access, or a role with the `isi-access` rule set to `scoped` or `all`.

For full RBAC setup instructions, see [Control Access With RBAC](doc:identity-and-secrets-intelligence#control-access-with-role-based-access-control-rbac).

## Policy Types And Examples

In the current implementation, common policy categories include:

| Category                 | Focus                                                                  |
| ------------------------ | ---------------------------------------------------------------------- |
| **Secrets policies**     | Secret exposure risks and secret hygiene                               |
| **Identity policies**    | Identity posture, privilege scope, and risky identity configurations   |
| **Certificate policies** | Certificate posture, lifecycle state, and certificate-related findings |

Examples of policy-driven findings can include exposed secrets in connected sources, over-permissive identities, and certificates that require lifecycle attention.

## Using Policies

1. Sign in to the Akeyless Console.
2. In the left navigation, open **Identity & Secrets Intelligence**.
3. Select **Policies**.
4. Review the available policies and their current status.
5. Enable or adjust policies based on findings surfaced in **Dashboard** and **Inventory**.

##
