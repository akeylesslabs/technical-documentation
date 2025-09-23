---
title: Event Center
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
# Overview

The Akeyless Event Center is your hub for everything event-related. This document will detail where you can access the Event Center, what it does, and how you can benefit from using it.

The Event Center can be accessed, by default, by **Admins** only, as well as users with explicit [permissions](doc:rbac), by clicking the bell icon at the top right-hand corner of the console screen, next to your user icon. Selecting the bell will also show you any pending notifications you might have from the Event Center, based on your settings. Setting up notification triggers will also be explained later in this guide.

# Using the Event Center

The Akeyless Event Center shows your event logs in the form of a table and allows you to monitor, filter, and search through the different events that occur in your Akeyless account.

On the upper left-hand side of the table, you will see a few interactive buttons, including a refresh button, a filter button, and a forwarder button, which allow you to use your event data to your benefit or to search through it.

# Event Types

Akeyless events are defined by object types, supporting: 

- **Items** events, for all items types e.g. [Static Secrets](doc:static-secrets), [Dynamic](doc:how-to-create-dynamic-secret)  and [Rotated Secrets](doc:rotated-secrets) , [Certificates](doc:certificate-storage)
- [Authentication Methods](doc:access-and-authentication-methods)
- [Targets](doc:targets)
- Gateway 

For each object type, a **Forwarder** can be set to forward all events for a folder, path, and even a specific item inside Akeyless. 

The following Events are currently supported:

For `items-event-source-locations`:

- `certificate-pending-expiration`  When a certificate is about to expire, the users sets and controls this event directly from the [PKI Issuer](doc:ssh-and-pkitls-certificates) or from the [Certificate](doc:certificate-storage) item.

- `certificate-expired` When a certificate is expired. 

- `certificate-error` When an error occurs during certificate issuance. 

- `certificate-provisioning-success` When a certificate is successfully provisioned

- `certificate-provisioning-failure` Upon **certificate provisioning** failure

- `next-automatic-rotation` When a [Rotated Secret](doc:rotated-secrets) or an [Encryption Key](doc:encryption-keys) is about to rotate automatically, the user sets and controls this event directly from the items.

- `rotated-secret-success` Upon successful **automatic** rotation. 

- `rotated-secret-failure` Upon **automatic** rotation failure, including the error details. 

- `rotated-secret-partial-failure` Upon **automatic** rotation partial failure, relevant for clusters, or [Linked Target](doc:linked-target) mode.

- `secret-sync` Upon **automatic** sync failure, including the error details.

- `dynamic-secret-failure` On general failure of a [Dynamic Secret](doc:how-to-create-dynamic-secret).

- `static-secret-updated` When a [Static Secret](doc:static-secrets) is set to trigger events on value changes.

- `usage_unused` When a global event is set in the Account settings, for secrets that have not been used or changed within the defined interval.

- `usage_unrotated` When a global event is set in the Account settings, for [Rotated Secrets](doc:rotated-secrets) that have not been rotated within the defined interval.

- `request-access` When a user requests access, either for privilege permission or for a Secure Remote Access session.  **Note**: Relevant also for `targets-event-source-locations`.

- `apply-justification` When the user provides a connection justification as part of the Secure Remote Access session. 

For `auth-methods-event-source-locations` :

- `uid-rotation-failure` On [Universal Identity](doc:universal-identity) rotation failure, to track the automatic rotation. 

- `auth-method-pending-expiration` by default **30 days **in advance before an [Authentication Methods](doc:access-and-authentication-methods) is about to expire can be customized.

- `auth-method-expired` When an [Authentication Methods](doc:access-and-authentication-methods) is expired.

- `email-auth-method-approved` When the invite of user based on [Email](doc:email) Auth Method is approved.

- `multi-auth-failure`  When an auth attempt keeps failing, once blocked (after 5 consecutive attempts) 

- `rate-limiting`  When a client reaches the rate-limiting threshold.

- ` usage-report` When the number of clients reaches the threshold (can be set via **Usage Report** screen)

For `gateways-event-source-locations`: 

- `gateway-inactive` When a Gateway changes its state to inactive, it must be set on the Gateway. 

# Event Forwarders

Event forwarders are tools you can configure through the Event Center to get notified on other platforms (e.g. email) when a certain event type happens. For example, one might want to be notified every time a certain [Certificate](https://docs.akeyless.io/docs/certificate-storage) is about to expire or when a user requests to access an item you have in your Akeyless Platform.

Event Forwarders can only be managed by **Admins** or by users with explicit [permissions](doc:rbac).

> 📘 Note
> 
> Event Forwarders require a running [Gateway](doc:api-gw). Both **Admins** and authorized users need to have [Access Permissions](doc:gateway-access-permissions) on at least one [Gateway](doc:api-gw) to create and manage Event Forwarders.

## Forwarded Events Format

The following JSON structure describes the forwarded event's format:

```json Akeyless Events Format
{
	"Akeyless_Events": {
		"Certificate_Expired": [{
				"name": "<cert A name>"
			},
			{
				"name": "<cert b name>"
			}
		],
		"certificate_pending_expiration": [{
				"name": "<cert c name>"
			},
			{
				"name": "<cert D name>"
			}
		],
		"Request_Access": [{...}]
	}
}
```
```json Certificate Event Format
{
  "Certificate_Expired": [
    {
      "name": "<Item Full Name>",
      "item_id": "<Item ID>",
      "payload": {
        "certificate_details": {
          "expires_at": "<Full Date>",
          "description": "<Item Description>"
        }
      }
    }
  ]
}
```

For more information about creating and configuring event forwarders, refer to:

[Email Event Forwarder](doc:email-event-forwarder)

[Webhook Event Forwarder](doc:webhook-event-forwarder)

[ServiceNow Event Forwarder](doc:servicenow-event-forwarder)

[Slack Event Forwarder](doc:slack-event-forwarder)