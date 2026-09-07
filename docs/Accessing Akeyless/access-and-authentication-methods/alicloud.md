---
title: 'AliCloud '
excerpt: Alibaba Cloud (AliCloud) Resource Access Management (RAM)
deprecated: false
hidden: false
metadata:
  robots: index
---
This page discusses creating and using an AliCloud RAM-based authentication method in Akeyless.

[AliCloud](https://www.alibabacloud.com/en?_p_lc=1) authentication provides an automated flow to retrieve an Akeyless token for RAM principals and AliCloud services or resources.

AliCloud authentication is intended for **workload authentication** and is not recommended for direct interactive Console sign-in.

## Creating an AliCloud Authentication Method

This action is distinct from creating a new Akeyless account: it creates an additional AliCloud RAM-based authentication method for an existing account.

Required AliCloud setting:

- **Bounded Account IDs:** Configure one or more AliCloud account IDs that are allowed to authenticate by using this authentication method.<br />In the Console, enter values as a comma-separated list (for example, `1234567890123,9876543210987`).
  With the CLI, repeat `--bound-account-id` for each value.

### Creating an AliCloud Authentication Method with the Console

To create a new AliCloud-based authentication method with the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select **+ New**. This opens the **Create Authentication Method** form.
3. On the **Type** selection screen, select **AliCloud**, then **Next →**.
4. Enter a name for the Authentication Method in the **Name** field. Optionally, include a path using `/` separators to place the Authentication Method in a virtual folder, then select **Next →**.
5. Configure AliCloud-specific fields as needed.&#x20;
6. &#x20;Select **Finish**.

### Creating an AliCloud Authentication Method with the CLI

To create an AliCloud-based authentication method with the CLI:

```shell
akeyless auth-method create alicloud \
  --name <AliCloud Auth Method Name> \
  --bound-account-id <AliCloud Account ID>
```

You can provide multiple AliCloud account IDs by repeating `--bound-account-id`.

[Read about more parameters available when creating an AliCloud-based authentication method.](https://docs.akeyless.io/docs/cli-ref-auth#create)

## Using an AliCloud Authentication Method

### Using an AliCloud Authentication Method with the CLI

To use an AliCloud-based authentication method with a CLI profile, run the [Akeyless configure command](https://docs.akeyless.io/docs/cli-reference#configure) from an AliCloud resource (for example, an ECS instance or a container running under a RAM role):

```shell
akeyless configure \
  --profile default \
  --access-id <Access ID> \
  --access-type alicloud
```

To inspect the cloud identity token, run the [Akeyless get-cloud-identity command](https://docs.akeyless.io/docs/cli-ref-auth#get-cloud-identity):

```shell
akeyless get-cloud-identity \
  --cloud-provider alicloud
```

To authenticate and retrieve a temporary Akeyless token, run the [Akeyless auth command](https://docs.akeyless.io/docs/cli-ref-auth#auth):

```shell
akeyless auth \
  --access-id <Access ID> \
  --access-type alicloud
```

<Callout icon="ℹ️" theme="info">
  ### **Note (Least Privilege):**

  AliCloud authentication does not require privileged RAM permissions. Attach a minimally privileged RAM role to the resource that authenticates to Akeyless (for example, an ECS instance or a container).
</Callout>

## Associate with Access Roles

After creating the authentication method, associate it with one or more Access Roles so authenticated identities can perform actions in Akeyless.

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select the AliCloud authentication method.
3. Add the required Access Roles.
4. Save the changes.

For role configuration details, see [Access Roles](https://docs.akeyless.io/docs/rbac).

## Update an Existing AliCloud Authentication Method

AliCloud authentication methods can require updates over time, for example when bounded account IDs, ARNs, or related constraints change.

To update in the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select the AliCloud authentication method to update.
3. Update the required fields.
4. Save the changes.

To update with the CLI, use the relevant `akeyless auth-method update alicloud` flags in [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#update).

## Troubleshooting

If AliCloud authentication fails, check the following:

- The workload is running with the expected RAM principal.
- The workload account matches configured bounded account IDs, ARNs, or other bounded fields.
- The configured **Access ID** and `alicloud` access type are correct.
- The STS endpoint is reachable from the Gateway and matches the configured region, if a custom endpoint is set.

## Optional Features

For optional features that apply across Authentication Methods, see [Common Optional Features](https://docs.akeyless.io/docs/access-and-authentication-methods#common-optional-features).

### AliCloud-Specific Optional Features

- **Bounded ARNs:** Enter one or more full RAM role or user ARNs that are allowed to authenticate by using this method. In the Console, enter values as a comma-separated list. With the CLI, repeat `--bound-arn` for each value. Supports wildcard patterns such as `*` and `?`.
- **Bounded Role Names:** Enter one or more RAM role names that are allowed to authenticate. In the Console, enter values as a comma-separated list. With the CLI, repeat `--bound-role-name` for each value.
- **Bounded Role IDs:** Enter one or more RAM role IDs that are allowed to authenticate. In the Console, enter values as a comma-separated list. With the CLI, repeat `--bound-role-id` for each value.
- **Bounded User Names:** Enter one or more RAM user names that are allowed to authenticate. In the Console, enter values as a comma-separated list. With the CLI, repeat `--bound-user-name` for each value.
- **Bounded User IDs:** Enter one or more RAM user IDs that are allowed to authenticate. In the Console, enter values as a comma-separated list. With the CLI, repeat `--bound-user-id` for each value.
- **Custom STS Endpoint:** Set a custom AliCloud STS endpoint URL if your environment requires a non-default endpoint. If not set, Akeyless uses `https://sts.aliyuncs.com`.
- **Unique Identifier:** Set a sub-claim key used to uniquely identify authenticated RAM principals.

***

### What's Next

Make sure to associate your new Authentication Method with an Access Role to grant the relevant permissions within Akeyless.
