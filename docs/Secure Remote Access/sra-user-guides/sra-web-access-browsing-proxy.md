---
title: Web Access (Browsing / Proxy)
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
Use this page to choose between isolated web browsing and proxy-based web access for Secure Remote Access (SRA).

Web access behavior depends on target configuration, user permissions, and the web access runtime topology.

## Before You Start

Confirm the following prerequisites:

1. You can sign in to the SRA portal and view web-access-capable targets.
2. The target item has Secure Remote Access enabled and includes the required web fields.
3. Your deployment has working dispatcher and proxy endpoints where required.
4. Redirect and proxy URL allowlists are configured for your environment.

For deployment requirements and endpoint planning, see [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements) and [Zero Trust Web Access Topology](https://docs.akeyless.io/docs/sra-web-access-topology).

## Choose the Right Mode

Use this guidance to choose the access mode per use case.

| Mode                | Where session runs                               | Best for                                               | Key consideration                                |
| ------------------- | ------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------ |
| Secure Web Browsing | Isolated remote browser runtime                  | Strong browser isolation and policy control            | Requires web-worker runtime readiness            |
| Secure Web Proxy    | User local browser, traffic routed through proxy | Access to internal web apps from approved entry points | Requires validated proxy endpoint and allowlists |

If both modes are available for the same target, prefer:

1. Secure Web Browsing for privileged administrative workflows and tighter isolation requirements.
2. Secure Web Proxy for day-to-day internal app access where local browser behavior is required.

## Access Modes

### Secure Web Browsing

Secure web browsing runs the target website in an isolated browser session managed by the SRA web stack.

Use this mode when you want tighter isolation and stronger control over browser context during the active session.

Typical scenarios:

- Access to sensitive administrative consoles.
- Sessions that require strict browser-policy enforcement.
- Environments where local browser context should not directly interact with target credentials.

### Secure Web Proxy

Secure web proxy mode routes user browser traffic through the dispatcher proxy path while users remain in their local browser.

Use this mode when users need direct browser interaction with internal web applications by way of approved proxy endpoints.

Typical scenarios:

- Internal web applications that are not directly reachable from user networks.
- Workflows where users must stay in their local browser.
- Access paths that require controlled, policy-backed proxy routing.

## Connect from the Portal

Use the portal flow below for both modes:

1. Sign in to the SRA portal.
2. Open the web-access application area.
3. Search for the required target.
4. Open the target and choose the available web action.
5. Complete any identity-provider challenge shown by your environment.

If approval is required before launch, complete the approval flow first. See [Request Access and Approval Flow](https://docs.akeyless.io/docs/sra-request-access-and-approval-flow).

### Mode-Specific Launch Confirmation

After selecting the target action, confirm you are in the expected mode:

1. Secure Web Browsing: the session opens in an isolated runtime window managed by SRA.
2. Secure Web Proxy: the session opens in your local browser through the configured proxy route.

If the observed behavior does not match the intended mode, re-check target mode configuration before retrying.

## What to Expect After Launch

### Secure Web Browsing Session

After launch, the session opens in an isolated browser runtime managed by the SRA web stack.

Expected behavior:

- Session controls and policy enforcement are applied from the remote browser side.
- Navigation and browser capabilities can be restricted by deployment policy.
- Session recording behavior depends on your Zero Trust Web Access (ZTWA) recording configuration.

### Secure Web Proxy Session

After launch, the session opens in your local browser while traffic is routed through the configured proxy path.

Expected behavior:

- Connectivity depends on valid proxy endpoint configuration and URL allowlists.
- Access is limited to routes and targets permitted by your policy and target configuration.
- If you have several SRA sessions open concurrently, your browser may suspend inactive background tabs to save resources. This can cause an inactive proxy session to disconnect, which surfaces as an unexpected termination when you switch back to that tab.

## Configuration Inputs

For both modes, verify these settings before user rollout:

1. Dispatcher URL (typically on port `9000`).
2. Web proxy URL when proxy mode is enabled (typically on port `19414`).
3. Allowed bastion and proxy URL allowlists in your SRA and ZTWA configuration.

For deployment-level setup details, see [Zero Trust Web Access on Kubernetes](https://docs.akeyless.io/docs/sra-web-access-on-k8s) and [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements).

## Quick Troubleshooting

If launch fails or opens the wrong path, validate in this order:

1. Target configuration values for web access mode and URL fields.
2. Dispatcher and proxy endpoint reachability.
3. Redirect and proxy URL allowlists.
4. Current user permissions and approval state.

For infrastructure-level diagnostics, see [Session Drops and Timeout Runbooks](https://docs.akeyless.io/docs/sra-session-drops-and-timeout-runbooks) and [Sticky Sessions and Ingress Patterns](https://docs.akeyless.io/docs/sra-sticky-sessions-and-ingress-patterns).

### Symptom-to-Check Mapping

| Symptom                                    | First check                                        | Next check                                                 |
| ------------------------------------------ | -------------------------------------------------- | ---------------------------------------------------------- |
| Target does not appear in web access view  | Confirm identity and SRA permissions               | Confirm target is configured for web access                |
| Session opens in wrong mode                | Confirm target mode setting                        | Confirm dispatcher or proxy URL mapping                    |
| Session launches, then drops quickly       | Confirm endpoint reachability and timeout behavior | Review ingress affinity and session routing patterns       |
| Proxy launch fails for selected users only | Confirm approval and policy state                  | Confirm allowlist and identity mapping for that user group |

## Resource Discovery Scope

Web-access-capable targets appear in the portal based on your authenticated identity, SRA permissions, and target configuration.

For resource onboarding details by target type, see [Supported Resource Types](https://docs.akeyless.io/docs/sra-resource-types).

## Related Pages

- [Portal Login and Target Discovery](https://docs.akeyless.io/docs/sra-portal)
- [Request Access and Approval Flow](https://docs.akeyless.io/docs/sra-request-access-and-approval-flow)
- [Zero Trust Web Applications Access](https://docs.akeyless.io/docs/sra-web-applications)
- [Zero Trust Web Access Topology](https://docs.akeyless.io/docs/sra-web-access-topology)
