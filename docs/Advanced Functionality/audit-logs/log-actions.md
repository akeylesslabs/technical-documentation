---
title: Log Actions
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
# Introduction

This page includes a thorough comb through all of the different options for the **action** part of the Akeyless [log line](https://docs.akeyless.io/docs/audit-logs#reading-the-raw-logs) by category.

# Items

* `list_items`: List items, either in a specific path or in your root Akeyless folder

* `delete_items`: Delete an item or items in a certain path

* `set_item_state`: Set an item state disabled/enabled

* `share_item`: Share an item from Akeyless

# Roles

* `create_role`: Create a new role

* `get_role`: Fetch the details of a certain role

* `update_role`: Updated role details

* `delete_role`: Delete a role

* `delete_roles`: Delete multiple roles

* `list_roles`: List roles, either in a specific path or in your root Akeyless folder

# Authentication Methods

* `create_auth_method`: Create a new authentication method

* `get_auth_method`: Fetch an auth method or all auth methods in a certain path

* `list_auth_methods`: List all auth methods

* `delete_auth_method`: Delete an auth method

* `delete_auth_methods`: Delete all auth methods in a certain path

* `create_assoc_role_auth_method`: Associate a role and an auth method

* `delete_assoc_role_auth_method`: Delete an association between a role and an auth method

# General Item Actions

* `create_item`: Create an item

* `get_item`: Get item details

* `update_item`: Update item details

* `delete_item`: Delete an item

* `rotate_item`: Rotate a key

* `share_item`: Share an item

# Secrets and Keys Actions

* `get_secret_value`: Fetch secret value

* `get_rotated_secret_value`: Fetch rotated secret value

* `get_dynamic_secret_details`: Fetch rotated secret value

* `get_item_derivation_creds`: Get item creds

* `gen_ssh_certificate`: Generate an SSH certificate

* `gen_pki_certificate`: Generate a PKI certificate

* `access_to_dynamic_secret_producer`: Request access to a dynamic secret producer

* `get_dynamic_secret_value`: Fetch a dynamic secret

* `new_dynamic_secret_value_pushed_by_producer`: Information that a dynamic secret has been fetched

# Universal Identity Actions

* `generate_universal_identity_token`: Generated a UID token

* `universal_identity_operation`: Any operation that involves a child token (create, revoke, list)

* `universal_identity_rotate`: Rotation of UIDs

# Targets

* `create_target`: Create a new target

* `get_target`: Get the details of a specific target

* `update_target`: Update target information

* `delete_target`: Delete a target

* `delete_targets`: Delete all targets in a path

* `list_targets`: List targets in a certain path or in your head folder

* `create_assoc_target_item`: Associate an item with a target

* `delete_assoc_target_item`: Break association between a target and an item

# Notification Forwarders

* `create_notification_forwarder`: Create a notification forwarder

* `updates_notification_forwarder`: Update a notification forwarder

* `delete_notification_forwarder`: Delete a notification forwarder

# Secure Remote Access Bastion

* `update_display_name_of_bastion`: Update a bastion name

* `get_bastion_information`: Fetch details of a specific bastion

* `list_bastions`: List bastions

# Gateways

* `issue_gateway_jwt`: Get gateway credentials

* `retrieve_gateway_information`: Fetch details of a specific gateway

* `list_gateways`: List gateways

# Billing

* `get_billing_details`: Fetch billing details

* `update_billing_details`: Update billing details

* `checkout`: Checkout

* `add_subscription`: Add a subscription

* `update_subscription`: Update subscription details

* `list_invoices`: List all invoices

* `get_next_invoice`: Show next invoice

# Additional Log Actions

* `user_notification`: User notification eas issued

* `move_objects`: Bulk transfer of items

* `list_kmip_servers`: List KMIP servers

* `update_object_version_settings_for_account`: Update account settings for objects

* `impersonation`: Impersonate another user in your Akeyless account
