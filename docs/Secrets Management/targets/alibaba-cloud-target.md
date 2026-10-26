---
title: Alibaba Cloud Target
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define an AliCloud target that contains an Alibaba Cloud RAM identity to be used with an [AliCloud Rotated Secret](https://docs.akeyless.io/docs/create-an-alicloud-rotated-secret).

If you are working with an explicit **Access Key** pair, ensure you create automatic rotation for this **Access Key** using an [AliCloud Rotated Secret](https://docs.akeyless.io/docs/create-an-alicloud-rotated-secret).

When working with [Gateway](https://docs.akeyless.io/docs/gateway-overview) Cloud Identity, Akeyless uses the Alibaba Cloud default credential provider chain. In addition, if an External ID is used, make sure the RAM role your Gateway uses has permission to assume the relevant roles in the account.

<Callout icon="ℹ️" theme="info">
  ### **Alibaba Cloud RAM Best Practices:**

  The best practice for using RAM roles in Alibaba Cloud is to grant temporary, least-privilege access to resources, rather than relying on long-term AccessKeys. Use your **Gateway cloud ID** to use RAM roles. Never use the AccessKey of an Alibaba Cloud root account. Akeyless rejects root account credentials.
</Callout>

## Create an AliCloud Target with the CLI

To create an AliCloud target with the CLI, run the following command:

```shell GW Cloud ID
akeyless target create alicloud \
--name <target name> \
--use-gw-cloud-identity
```
```shell Explicit credentials
akeyless target create alicloud \
--name <target name> \
--access-key-id <AliCloud AccessKey ID> \
--access-key <AliCloud AccessKey secret> \
--region <AliCloud region>
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
- `use-gw-cloud-identity`: A boolean flag to use the Gateway cloud ID, which uses an existing RAM role (ECS instance RAM role, or ACK RRSA through OIDC).
  - `generate-external-id[=false]`: Optional. A unique auto-generated value to set as `sts:ExternalId` in the trust policy of your RAM role, to securely delegate access to Akeyless. Relevant only when using the Gateway cloud ID.
  - `role-arn`: Optional. The RAM role ARN that the Gateway assumes in your Alibaba Cloud account, in the format `acs:ram::<account-id>:role/<role-name>`. Relevant only when using an External ID.

Alternatively, to use RAM explicit credentials:

- `access-key-id`: The AccessKey ID of the RAM user that will be used to authenticate Akeyless with Alibaba Cloud.
- `access-key`: The AccessKey secret of the RAM user.
- `session-token`: Optional. Required only for temporary credentials retrieved through STS (Alibaba Cloud SecurityToken).
- `region`: Optional. The Alibaba Cloud region ID used to select the regional STS endpoint, for example `cn-hangzhou` or `ap-southeast-1`. If empty, the global endpoint `sts.aliyuncs.com` is used. RAM itself is a global service.

Akeyless validates the credentials with a read-only call when you create or update the target.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#alicloud) section.

<Callout icon="ℹ️" theme="info">
  ### **Use Gateway's Cloud Identity:**

  This is relevant when your Gateway is hosted on an Alibaba Cloud resource, such as an ECS instance with an attached RAM role, or an ACK cluster with RRSA enabled. The Gateway resolves its identity in this order: environment variables (`ALIBABA_CLOUD_ACCESS_KEY_ID`, `ALIBABA_CLOUD_ACCESS_KEY_SECRET`), the ECS instance RAM role, and ACK RRSA (`ALIBABA_CLOUD_ROLE_ARN`, `ALIBABA_CLOUD_OIDC_PROVIDER_ARN`, `ALIBABA_CLOUD_OIDC_TOKEN_FILE`). Make sure the relevant RAM role has enough permissions to perform the required actions as described in the relevant guides, for example, [AliCloud Dynamic Secrets](https://docs.akeyless.io/docs/alicloud-producer) and [AliCloud Rotated Secret](https://docs.akeyless.io/docs/create-an-alicloud-rotated-secret).

  If you are working with explicit credentials, make sure to set a [Rotated Secret](https://docs.akeyless.io/docs/create-an-alicloud-rotated-secret) for the AccessKey.
</Callout>

## Create an AliCloud Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Cloud (Alibaba Cloud)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable [Zero-Knowledge Encryption](https://docs.akeyless.io/docs/gateway-zero-knowledge) and click **Next**.

4. Choose your preferred authentication mode by selecting one of the options:
   - Check the **Use Credentials** radio button to authenticate with the AccessKey pair of a RAM user.

   - Check the **Use Gateway's Cloud Identity** option to authenticate with the Gateway's local Alibaba Cloud identity.
     <Callout icon="👍" theme="okay">
       ### Note

       **Use Gateway's Cloud Identity** is relevant when your Gateway is hosted on an Alibaba Cloud resource (for example, an ECS instance with a RAM role, or an ACK cluster with RRSA). Make sure the relevant RAM role has enough permissions to perform the required actions as described in the relevant guides, for example, [AliCloud Dynamic Secrets](https://docs.akeyless.io/docs/alicloud-producer) and [AliCloud Rotated Secret](https://docs.akeyless.io/docs/create-an-alicloud-rotated-secret).
     </Callout>

5. Define the remaining parameters as follows:
   - **Access Key ID:** If you selected the **Use Credentials** option in the previous step, specify the AccessKey ID of the RAM user that authenticates Akeyless with Alibaba Cloud.
   - **Access Key Secret:** Specify the AccessKey secret of that RAM user.
   - **Region:** Optional. The Alibaba Cloud region used to select the regional STS endpoint. If empty, the global endpoint is used.
   - **External ID:** Optional. A unique auto-generated value to set as `sts:ExternalId` in the trust policy of your RAM role, to securely delegate access to Akeyless.
   - **Role ARN:** Optional. When using an External ID, the RAM role ARN that the Gateway assumes, in the format `acs:ram::<account-id>:role/<role-name>`.

6. Click **Finish**.
