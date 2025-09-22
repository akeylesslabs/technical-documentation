---
title: Helm Chart Changes and Enhancements
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
With the Unified Gateway comes a new Helm chart that customers will see is substantially different fro the legacy Gateway. We have optimized the new Helm chart so setup is more streamlined and simpler.

To do this, many values in the chart have either been removed altogether or moved into the Gateway UI. Below are values as they appear in each sections of the legacy Remote Access chart.

Here you will find only the values that were moved or changed for each section:

# Remote Access Chart Changes

## Global

**clusterName**: Moved to the "Global" section in the Unified Gateway Helm chart.

**legacySigningAlg**: Removed. Now appears in the Manage Gateway section.

**usernameSubClaim**: Removed. Now appears in the Manage Gateway section in the Akeyless Console UI.

**RDPusernameSubClaim**: Removed. Now appears in the Manage Gateway section in the Akeyless Console UI.

**SSHusernameSubClaim**: Removed. Now appears in the Manage Gateway section in the Akeyless Console UI.

**privilegedAccess**: This section was replaced by **authorizedAccessIDs** in the Unified Gateway Helm chart.

**azureObjectID**: Removed.

**gcpAudience**: Removed.

**httpProxySettings**: Moved to the "Global" section in the Unified Gateway Helm chart.

**deployment**: Moved to "Default values for Gateway" section in the Unified Gateway Helm chart.

## Default values for akeyless-zero-trust-bastion

**ztbConfig**: Removed. Now called **webConfig** in the Unified Gateway Helm chart.

**image**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**containerName**: Removed.

**service**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**ingress**: Moved to "Default values for Gateway" section in the Unified Gateway Helm chart.

**hostname**: Moved to "Default values for Gateway" section in the Unified Gateway Helm chart.

**path**: Moved to "Default values for Gateway" section in the Unified Gateway Helm chart.

**tls**: Moved to "Default values for Gateway" section in the Unified Gateway Helm chart.

**certManager**: Moved to "Default values for Gateway" section in the Unified Gateway Helm chart.

**allowedBastionUrls**: Removed. Now appears in the Manage Gateway section in the Akeyless Console UI.

**persistence**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**livenessProbe**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**readinessProbe**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**resources**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**hpa**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**config** (**rdpRecord**): Removed. This whole section for RDP Recording is now appears in the Manage Gateway section in the Akeyless Console UI.

## Default values for akeyless-zero-trust-portal

**ztpConfig**: Removed.

**nodeSelector**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**securityContext**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**service**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**livenessProbe**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**readinessProbe**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**resources**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**hpa**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**ingress**: Moved to "Default values for Gateway" section in the Unified Gateway Helm chart.

**hostname**: Moved to "Default values for Gateway" section in the Unified Gateway Helm chart.

**path**: Moved to "Default values for Gateway" section in the Unified Gateway Helm chart.

**tls**: Moved to "Default values for Gateway" section in the Unified Gateway Helm chart.

**certManager**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

## Default values for akeyless-ssh-bastion

**sshConfig**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**updateStrategy**: Removed.

**labels**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**nodeSelector**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**securityContext**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**env**: Removed.

**initContainer**: Removed.

**image**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**containerName**: Removed.

**service**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**persistence**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**resources**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**hpa**: Located in "Default values for akeyless-secure-remote-access" section in the Unified Gateway Helm chart.

**config**: The configuration of the **CAPublicKey** is now located under the new **sshConfig** section in the Unified Gateway Helm chart.

**sessionTermination**: Removed. Now appears in the Manage Gateway section in the Akeyless Console UI.

**logForwarding**: Removed. Now appears in the Manage Gateway section in the Akeyless Console UI.

**existingSecretName**: Removed.

**allowedBastionUrls**: Removed. Now appears in the Manage Gateway section in the Akeyless Console UI.
