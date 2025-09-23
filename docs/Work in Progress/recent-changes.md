---
title: Release Notes and Changes
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
# Release Notes

## December 2023

> ### Secrets Management

### Enhanced RBAC configuration for Secure Remote Access

Admins can now more easily define Role-Based Access Controls for user access to specific resources from the Secure Remote Access Bastion based on the `Secure Remote Access` permissions set within the specific `role`. The options offered are Full Access to connect without justifying a request for access, Justifying a request for access without requiring permission, and Requesting Approval which require an approval request and note for justification to access the resource.

### Active Directory Windows Services Discovery

As part of our Resource Discovery feature for Active Directory, we now enable users to discover any Windows service that runs with explicit user credentials and save them as rotated secrets. Upon rotation, the relevant services will be restarted with the latest password.

### Datadog Marketplace Integration

We have made it even easier to add Datadog integration for your telemetry metrics. Simply activate Datadog dashboards for Akeyless Gateways with a single click from the Marketplace within the Datadog Platform.

### Support for KMIP caching

We now support KMIP caching to enable using existing keys without SaaS connectivity.

### Allow creating Rotated Secrets without an initial secret value

Users can now create Rotated Secrets without an initial value for machines without an initial password. Upon rotation, a password will be created and updated in both the application and Akeyless.

### Renamed 'External Secrets Manager' to 'Universal Secrets Connector'

The new name of External Secrets Manager feature is now Universal Secrets Connector.

## November 2023

> ### Secrets Management

### Rotated Secret and Auth Method Event Notification

We have added an important security notification which tells a user if a Rotated Secret and specified Auth Method have never been rotated or used, which will show in the Event Center.

### Certificate Analytics

Users can now see analytics of their Certificate usage as a widget in Analytics section of the Console.

### Updated Rotated Secret Screen

We now have a simple step-by-step wizard for Rotated Secret creation in the Console.

### Better UI for Secret Migration

We have improved the look and feel of the Automatic Migration screen in the Gateway Console for a better user experience.

> ### Secure Remote Access

### Snowflake Support

We now support Snowflake Dynamic Secrets for Secure Remote Access.

### Linked Targets for SSH

We now support using SSH Linked Targets (Parentless mode) with Secure Remote Access to connect to your SSH hosts.

## October 2023

> ### Secrets Management

### Gateway Authentication Support

The Gateway login now supports authenticating using OAuth 2.0/JWT auth methods.

### Adding Custom Name to Customer Fragment

Users now have the options to give a custom name to Customer Fragments held in the Gateway.

### Caching of Gateway Clusters

Gateway Clusters are now supported with a caching synchronization mechanism.

### Gateway Analytics

A number of new Gateway metrics have been added for analytics as well as number of requests and http status codes.

### Sub-Claims Custom Delimiters

By default, Akeyless treats the `,` character as a delimiter for the JWT attributes. If needed, users can now add a custom delimiter tailored to an Auth Method’s Sub-Claims in cases where the IdP uses a different delimiter.

> ### Secure Remote Access

### File Download

Users can now also download files in Secure Remote Access RDP sessions.

### RD Gateway Support

Users now have the ability to use Microsoft RD Gateway in addition to the Secure Remote Access bastion.

## September 2023

> ### Secrets Management

### OIDC Identity Provider

Akeyless can now be used as an OpenID Connect (OIDC) identity provider enabling client applications full support of the OIDC protocol to leverage any Akeyless supported Authentication Method as a source of identity, and a wide range of authentication methods when authenticating end-users. Client applications can configure their authentication logic to talk to Akeyless. Once enabled, Akeyless will act as the bridge to other identity providers via its existing authentication methods.

### Groups for Authentication Methods

Groups enable administrators to more easily manage and reuse Authentication Methods by associating them to a single Access Role as a Group rather than manually associating multiple individual Authentication Methods. The Groups feature can also be used with an OIDC Application.

### Enhanced Authentication with Client Certificates in Kubernetes

Users can now authenticate with Kubernetes using certificates generated within Kubernetes. This method utilizes a private key paired with a public key set inside of Kubernetes which follows K8s best practices for auth strategies since no token is being exchanged as part of the flow directly with your cluster.

### Force Default Protection Key

This feature enhances security giving admins the ability to lock a Default Protection Key at the account level for all items.

### MS-SQL Service Principal Authentication

We now support authenticating to Microsoft Azure SQL (MS-SQL target) using a service principal. This makes interactions with Azure SQL more seamless and secure.

### Grant Access to Usage Reports

Admins can now easily grant access to the Usage Report screen.

> ### Secure Remote Access

### LDAP Authentication

Users can now log into the Secure Remote Access Portal using LDAP authentication.

## August 2023

### Path Templating for Sub-Claims

For easier management of your access rules, sub-claims keys can be utilized for quicker and more scalable rule definitions for the access path, which enables admins to give multiple users access to their specific paths based on the sub-claim values. This means [claims can be templated](https://docs.akeyless.io/docs/sub-claims#path-templating), for example, as /\{\{Group}}/\{\{Username}}/\* for your rule path based on your IdP mapping.

### Item Naming Convention

You can now set a list of characters that are not allowed to be used when naming items in your Akeyless account from the Console under the “Account Settings” section.

### GlobalSign Atlas Target

A new [GlobalSign Atlas Target](https://docs.akeyless.io/docs/cli-reference-akeyless-targets#p-stylecolorblue-create-globalsign-atlas-targetp) is now available for users of the certificate automation service.

### Certificate Caching

We now support Gateway [caching](https://docs.akeyless.io/docs/configure-the-gateway-cache) of Certificate items.

### Redis Rotated Secret

We now support [Rotated Secrets](https://docs.akeyless.io/docs/create-a-database-rotated-secret) for Redis databases.

### Web-based Auth Configurations

You can now configure K8s and [LDAP](https://docs.akeyless.io/docs/ldap#create-ldap-authentication-method-from-the-akeyless-console) Auth Methods from the WebUI.

## July 2023

### SPIRE Plugin Support

Users can now integrate with SPIFFE systems using our [SPIRE plugin](https://docs.akeyless.io/docs/spire-plugin) for:\
SPIRE Key Manager\
SPIRE Secret Manager\
SPIRE Upstream Authority\
SPIRE Upstream Authority SM

### Auth Method Expiration in Event Center

Users will now receive notifications in the Event Center when an Authentication Method has expired.

### RDP Dynamic Secrets

[RDP Dynamic Secrets](https://docs.akeyless.io/docs/rdp-dynamic-secrets) can now be associated with a Windows Target which enables users to dynamically generate user credentials for connecting to a specified Windows host. When a client requests a dynamic secret value, Akeyless, through your Gateway, connects to the target Windows host over SSH and creates a new user.

## June 2023

### User Requests for Access

Users in an organization can now [request temporary permission elevation](https://docs.akeyless.io/docs/request-access) for certain actions and approval is given through the Event Center.

### Kubernetes Dynamic Secret Authentication

Users now have the ability to authenticate Dynamic Secret requests using a [Gateway Kubernetes Service Account](https://docs.akeyless.io/docs/kubernetes-targets#k8s-generic) (if you have a K8s auth method). This setting is found inside the Generic Kubernetes Target.

### MFA Support

All human authentication methods, such as OIDC, SAML, or Email, now support Multi-Factor Authentication.

### Gateway Force Delete

Admins can now force delete a Gateway cluster, from the CLI only, using the `--force` flag even if it is active with associated secrets. Note that all Gateway secrets will also be deleted.

### Available Updates Notification for Gateway

The Akeyless Console will offer a notification in the `Gateways` screen if there is an available update for your Gateway(s).

### New Classic Key Types

Added new types of Classic Keys: AES128CBC and AES256CBC

### Self-Signed Certificates

Users now have the option to generate self-signed certificates when creating DFC or classic encryption keys by choosing the “Import Key” option.

### New Certificate Automation Targets

Users can now create GlobalSign and ZeroSSL Targets which can be found in the “Certificate Automation” section of the UI.

### Linked Targets for Rotated Secrets

Users can now associate [Rotated Secrets with Linked Targets](https://docs.akeyless.io/docs/linked-target-rotated-secret) for Windows and SSH Targets. Linked Targets offers an easier way to manage automated password rotation for Local users with the same login credentials across different servers simultaneously. Set a Parent Target, add your other server hostnames, and rotate them all at once.

### New Log Forwarders

We’ve added Sumo Logic and Google Chronicle as options to forward all your Akeyless Gateway audit logs.

### Cert-Manager Integration with PKI Issuer

Users can now use an Akeyless PKI Issuer to issue Kubernetes certificates using [cert-manager](https://docs.akeyless.io/docs/kubernetes-cert-manager).

## May 2023

### External Secrets Manager

The [External Secrets Manager](https://docs.akeyless.io/docs/external-secrets-manager) (i.e., Bring Your Own Vault) is a new capability in the Akeyless Vault Platform that allows you to centralize governance and control of your secrets without migrating existing secrets or replacing existing secret managers.  

ESM not only allows you to store and manage the lifecycle of secrets, but also serves as a “secrets manager of managers,” enabling you to manage secrets on other platforms such as AWS, GCP, Azure, and Kubernetes.

# Breaking Changes

Starting from SDK version 4 the following methods: 

`getSecretValue()`  and `getDynamicSecretValue()`

return value is  `map[string]interface{}` instead of `map[string]string`

<br>
