---
title: Organization-Wide Scope
deprecated: false
hidden: false
metadata:
  robots: index
---
By default, an [AWS Universal Secrets Connector](https://docs.akeyless.io/docs/aws-universal-secrets-connector) (**USC**) works with one AWS account and one Region: the ones set on its [AWS Target](https://docs.akeyless.io/docs/aws-targets). With **Organization-Wide Scope**, a single USC can list and manage AWS Secrets Manager secrets in any account of your AWS Organization, in any Region.

Existing single-account USCs keep working exactly as before.

## How It Works

Two things make this work:

1. **Account discovery.** The identity configured on your Akeyless AWS Target calls `organizations:ListAccounts` to get the list of accounts in your Organization. This identity must live in either the **management account** or a **delegated administrator account**. A regular member account can't list Organization accounts.
2. **Access to each account.** Every account you want to manage has an IAM role named `AkeylessUSCRole`, created for you by an Akeyless CloudFormation StackSet. When you select an account, the Gateway assumes that account's `AkeylessUSCRole` and calls Secrets Manager in the Region you chose.

## Step 1: Choose Where the Akeyless Identity Lives

|                                       | Management account                                         | Delegated administrator account                                  |
| ------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------- |
| Where the Akeyless identity lives     | The management account                                     | An account you choose, for example a Security or Tooling account |
| Extra setup in the management account | None                                                       | One delegation policy (Step 2B)                                  |
| Security                              | Akeyless holds credentials in your most privileged account | Akeyless never uses management-account credentials               |
| Recommended                           | Fine for testing                                           | **Yes, for production**                                          |

Many security teams don't allow third-party integrations in the management account. If that applies to you, use the delegated administrator option.

## Step 2: Set Up the Akeyless Identity

Create an IAM user (with an access key) or an IAM role for the Akeyless AWS Target. Which one you need depends on how your target authenticates. Then follow the option you chose in Step 1.

### Option A: Management Account

Create the identity in the management account and attach this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListOrganizationAccounts",
      "Effect": "Allow",
      "Action": [
        "organizations:ListAccounts",
        "organizations:DescribeOrganization"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AssumeRoleInMemberAccounts",
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::*:role/AkeylessUSCRole"
    },
    {
      "Sid": "ManageSecretsInThisAccount",
      "Effect": "Allow",
      "Action": [
        "secretsmanager:ListSecrets",
        "secretsmanager:DescribeSecret",
        "secretsmanager:GetSecretValue",
        "secretsmanager:CreateSecret",
        "secretsmanager:PutSecretValue",
        "secretsmanager:UpdateSecret",
        "secretsmanager:DeleteSecret",
        "secretsmanager:TagResource",
        "secretsmanager:UntagResource"
      ],
      "Resource": "*"
    }
  ]
}
```

### Option B: Delegated Administrator Account

This takes two parts: one done once by an admin in the management account, and one done in your account.

**1. In the management account (one time):** go to **AWS Organizations → Settings → Delegated administrator for AWS Organizations → Delegate**, and add this policy. Replace `<delegated-account-id>` with the 12-digit ID of your account.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAkeylessAccountDiscovery",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::<delegated-account-id>:root" },
      "Action": [
        "organizations:ListAccounts",
        "organizations:DescribeOrganization"
      ],
      "Resource": "*"
    }
  ]
}
```

You can also apply it from the CLI:

```shell
aws organizations put-resource-policy --content file://delegation-policy.json
```

**2. In your delegated account:** create the identity and attach the **same policy as Option A**.

<Callout icon="📘" theme="info">
  ### Why the Organizations permissions appear twice

  The delegation policy allows your _account_ to read Organization data. AWS also requires the _identity_ inside your account to be allowed to make the call, so the identity's own policy needs `organizations:ListAccounts` as well.
</Callout>

**Check that discovery works.** Using the new identity's credentials, run:

```shell
aws organizations list-accounts
```

If this returns your account list, account discovery is ready.

### About the Policy Blocks

- `ListOrganizationAccounts` fills the account list in the USC.
- `AssumeRoleInMemberAccounts` lets the identity switch into `AkeylessUSCRole` in other accounts. Cross-account access needs permission on both sides: this statement on your side, and the role's trust policy on the other side.
- `ManageSecretsInThisAccount` is only needed if you want to manage secrets in the target's own account. Remove it otherwise.

If your secrets use customer-managed KMS keys, add `kms:Decrypt` and `kms:GenerateDataKey` for those keys, both here and in `AkeylessUSCRole`.

## Step 3: Create AkeylessUSCRole in Each Account

You can only see secrets in accounts that have `AkeylessUSCRole`. The StackSet below creates the role in every account under the OUs you choose, and in any account added to those OUs later.

Save this template as `akeyless-usc-org-role.yaml`:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Akeyless org-wide AWS Universal Secrets Connector cross-account role

Parameters:
  RoleName:
    Type: String
    Default: AkeylessUSCRole
    Description: Name of the IAM role created in every member account. Must be identical across all accounts.
  TrustedPrincipalArn:
    Type: String
    Description: ARN of the IAM user or role used by your Akeyless AWS Target.
  ExternalId:
    Type: String
    Default: ''
    NoEcho: true
    Description: Optional. External ID configured on your Akeyless AWS Target. Leave empty if you don't use one.

Conditions:
  HasExternalId: !Not [!Equals [!Ref ExternalId, '']]

Resources:
  AkeylessUSCRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Ref RoleName
      MaxSessionDuration: 3600
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Ref TrustedPrincipalArn
            Action: sts:AssumeRole
            Condition: !If
              - HasExternalId
              - StringEquals:
                  sts:ExternalId: !Ref ExternalId
              - !Ref AWS::NoValue
      Policies:
        - PolicyName: AkeylessUSCSecretsManagerAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - secretsmanager:ListSecrets
                  - secretsmanager:DescribeSecret
                  - secretsmanager:GetSecretValue
                  - secretsmanager:CreateSecret
                  - secretsmanager:PutSecretValue
                  - secretsmanager:UpdateSecret
                  - secretsmanager:DeleteSecret
                  - secretsmanager:TagResource
                  - secretsmanager:UntagResource
                Resource: '*'

Outputs:
  RoleArn:
    Description: ARN of the Akeyless USC cross-account role
    Value: !GetAtt AkeylessUSCRole.Arn
```

For `TrustedPrincipalArn`, use the exact ARN of the identity from Step 2, for example:

- Option A: `arn:aws:iam::<management-account-id>:role/akeyless-target`
- Option B: `arn:aws:iam::<delegated-account-id>:role/akeyless-target`

For an IAM user, use `:user/<name>` instead of `:role/<name>`.

### Deploy the StackSet

StackSets are deployed from the management account by default. If you want to deploy from your delegated account instead, first have the management account register it as a StackSets delegated administrator:

```shell
aws organizations register-delegated-administrator \
  --account-id <delegated-account-id> \
  --service-principal member.org.stacksets.cloudformation.amazonaws.com
```

**1. Create the StackSet.** Use `--call-as SELF` from the management account, or `--call-as DELEGATED_ADMIN` from a registered delegated account.

```shell
aws cloudformation create-stack-set \
  --stack-set-name akeyless-usc-org-role \
  --template-body file://akeyless-usc-org-role.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --permission-model SERVICE_MANAGED \
  --auto-deployment Enabled=true,RetainStacksOnAccountRemoval=false \
  --parameters \
    ParameterKey=TrustedPrincipalArn,ParameterValue=<trusted-principal-arn> \
    ParameterKey=ExternalId,ParameterValue=<external-id> \
  --call-as SELF
```

If your AWS Target has no External ID, remove the `ParameterKey=ExternalId,...` line. The role then trusts only the exact `TrustedPrincipalArn`.

**2. Deploy it to the accounts you want.** Use the Organization root ID to cover every account, or specific OU IDs to limit the scope.

```shell
aws cloudformation create-stack-instances \
  --stack-set-name akeyless-usc-org-role \
  --deployment-targets OrganizationalUnitIds=<root-or-ou-id> \
  --regions <single-region> \
  --call-as SELF
```

To change the scope later, run `create-stack-instances` or `delete-stack-instances` with the new OUs.

<Callout icon="🚧" theme="warn">
  ### Use exactly one Region

  IAM roles are global. Pass a single Region in `--regions`. Deploying to more Regions fails because the role already exists in the account. One role still covers Secrets Manager in every Region of that account.
</Callout>

<Callout icon="📘" theme="info">
  ### The management account isn't covered

  Service-managed StackSets don't deploy to the management account. If you need secrets from it, create `AkeylessUSCRole` there with a regular CloudFormation stack using the same template.
</Callout>

<Callout icon="🚧" theme="warn">
  ### Delegated administrator limits

  - AWS limits how many delegated administrators an Organization can register, and the limit is shared with other services and vendors. Check that you have a free slot.
  - A StackSets delegated administrator can deploy StackSets across the whole Organization. To limit what Akeyless covers, target specific OUs in the StackSet.
</Callout>

## Step 4: Configure Akeyless

1. Update your Akeyless AWS Target to use the identity from Step 2.
2. Create or edit the AWS USC and set its scope to **Organization**.
3. Open the USC. It loads the target's own account and Region first.
4. Pick another account and Region from the **Account** and **Region** dropdowns. The secrets table reloads automatically.

## Step 5 (Optional): Keep the Account List Current

Akeyless polls `ListAccounts` periodically to pick up account changes. To pick them up right away, create an EventBridge rule in the account where the Akeyless identity lives that forwards these AWS Organizations events to Akeyless:

- `AccountJoinedOrganization`: refreshes the account list and starts scanning the new account.
- `AccountDepartedOrganization`: flags the removed account for review.

## Choosing an Account and Region

In the UI, use the **Account** and **Region** dropdowns. Everywhere else, pass either a full secret ARN (`arn:aws:secretsmanager:<region>:<account-id>:secret:<name>`) or a secret name with an account ID and Region. If you pass neither, the target's own account and Region are used.

**CLI**

```shell
akeyless usc list \
  --usc-name /prod/aws-usc \
  --aws-account-id 123456789012 \
  --region us-east-1
```

The same flags work with `usc get`, `usc create`, `usc update`, and `usc delete`. See the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector).

**API**

For list and get, pass `account_id` and `region` as query parameters. For create, update, and delete, add them to the request body:

```json
{
  "account": "123456789012",
  "region": "us-east-1"
}
```

**Sync:** each [sync](https://docs.akeyless.io/docs/sync-secret) mapping stores its own account ID and Region (or ARN).

**Kubernetes Injector:** each secret reference in the [Akeyless Kubernetes Secrets Injector](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector) annotations can set its own account ID and Region (or ARN), so one workload can pull secrets from several accounts.

The Gateway caches the assumed-role session for each account and reuses it until it's close to expiring, so switching accounts doesn't call STS every time.

## Limiting Access

The account dropdown always shows every account in the Organization, because `ListAccounts` returns all of them. You control which ones actually work:

- **By where the role exists.** Deploy the StackSet only to the OUs you want. Other accounts appear in the list but fail to load.
- **By the target identity's policy.** Replace `arn:aws:iam::*:role/AkeylessUSCRole` with a list of specific account ARNs.
- **By secret name.** In `AkeylessUSCRole`, scope `Resource` to a prefix such as `arn:aws:secretsmanager:*:*:secret:app/*`. `ListSecrets` can't be restricted this way, so names may still appear, but values outside the prefix can't be read or changed.

## Troubleshooting

| Error or symptom                                                                                                                                                  | Cause                                                                                            | Fix                                                                                                                                                                                                              |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AWS Organization account discovery requires target credentials from the management account or a delegated administrator account with organizations:ListAccounts` | The target identity is in a regular member account, or it's missing `organizations:ListAccounts` | Follow Step 2. For Option B, confirm the delegation policy names the right account ID and the identity has its own `organizations:ListAccounts` permission                                                       |
| An account appears in the list but fails to load (AssumeRole error)                                                                                               | `AkeylessUSCRole` doesn't exist there, or its trust policy doesn't match                         | Deploy the StackSet to that account's OU. Check that `TrustedPrincipalArn` is the exact identity ARN. If you use an External ID, check that it's set both on the target and in the StackSet, with the same value |
| Secrets from the management account don't load                                                                                                                    | The StackSet doesn't deploy there                                                                | Create `AkeylessUSCRole` in the management account with a regular stack                                                                                                                                          |
| Fewer secrets than expected                                                                                                                                       | Secrets are listed per Region                                                                    | Select the Region where the secrets live                                                                                                                                                                         |
| Access denied reading a secret value                                                                                                                              | The secret uses a customer-managed KMS key                                                       | Add `kms:Decrypt` and `kms:GenerateDataKey` for that key                                                                                                                                                         |
