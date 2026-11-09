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

1. **Account discovery.** The identity on your Akeyless AWS Target calls `organizations:ListAccounts` to get the accounts in your Organization. This identity must live in the **management account** or in a **delegated administrator account**. A regular member account can't list Organization accounts.
2. **Access to each account.**
   - In the target's own account, the Gateway uses the target identity directly.
   - In every other account, the Gateway assumes an IAM role named `AkeylessUSCRole` and calls Secrets Manager in the Region you chose.

## Step 1: Choose Where the Akeyless Identity Lives

|                                   | Management account     | Delegated administrator account  |
| --------------------------------- | ---------------------- | -------------------------------- |
| Where the identity lives          | The management account | A member account you choose      |
| Extra setup in management account | None                   | One delegation policy (Option B) |

## Step 2: Set Up the Akeyless Identity

Create an IAM user (with an access key) or an IAM role for your Akeyless AWS Target, then attach this policy to it.

Replace:

- `<org-id>` with your Organization ID (starts with `o-`)
- `<this-account-id>` with the ID of the account where the identity lives

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
      "Resource": "arn:aws:iam::*:role/AkeylessUSCRole",
      "Condition": {
        "StringEquals": { "aws:ResourceOrgID": "<org-id>" }
      }
    },
    {
      "Sid": "ListSecrets",
      "Effect": "Allow",
      "Action": "secretsmanager:ListSecrets",
      "Resource": "*"
    },
    {
      "Sid": "ManageSecretsInThisAccount",
      "Effect": "Allow",
      "Action": [
        "secretsmanager:DescribeSecret",
        "secretsmanager:GetSecretValue",
        "secretsmanager:CreateSecret",
        "secretsmanager:PutSecretValue",
        "secretsmanager:UpdateSecret",
        "secretsmanager:DeleteSecret",
        "secretsmanager:ListSecretVersionIds",
        "secretsmanager:TagResource",
        "secretsmanager:UntagResource"
      ],
      "Resource": "arn:aws:secretsmanager:*:<this-account-id>:secret:*"
    }
  ]
}
```

What each block does:

- `ListOrganizationAccounts` fills the account list in the USC.
- `AssumeRoleInMemberAccounts` lets the identity switch into `AkeylessUSCRole` in other accounts of your Organization only.
- `ListSecrets` and `ManageSecretsInThisAccount` let the identity manage secrets in its own account. The USC opens on this account by default.

### Option A: Management Account

Create the identity in the management account and attach the policy above. No other setup is needed.

### Option B: Delegated Administrator Account

1. Create the identity in your chosen account and attach the policy above. The account must be a member of the same Organization.

2. In the management account, go to **AWS Organizations → Settings → Delegated administrator for AWS Organizations → Delegate**, and add this policy.

   Replace:

   - `<delegated-account-id>` with the ID of the account from step 1
   - `<identity-arn>` with the exact ARN of the identity, for example `arn:aws:iam::<delegated-account-id>:user/akeyless-target`

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
         "Resource": "*",
         "Condition": {
           "ArnEquals": { "aws:PrincipalArn": "<identity-arn>" }
         }
       }
     ]
   }
   ```

   This policy is read-only and allows only the Akeyless identity to list the Organization's accounts.

<Callout icon="🚧" theme="warn">
  ### An Organization has only one delegation policy

  Saving a new policy replaces the existing one. If your Organization already has a delegation policy, add the statement above to its `Statement` list instead of replacing it.
</Callout>

### Check That Discovery Works

Using the identity's credentials, run:

```shell
aws organizations list-accounts
```

If this returns your account list, discovery is ready.

## Step 3: Create AkeylessUSCRole in the Other Accounts

Every account you want to manage, other than the target's own account, needs `AkeylessUSCRole`. The StackSet below creates it in every account under the OUs you choose, including accounts added to those OUs later.

Save this template as `akeyless-usc-org-role.yaml`:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Akeyless USC cross-account role

Parameters:
  TrustedPrincipalArn:
    Type: String
    Description: ARN of the IAM user or role used by your Akeyless AWS Target.
  ExternalId:
    Type: String
    Default: ''
    NoEcho: true
    Description: Optional. External ID set on your Akeyless AWS Target. Leave empty if you don't use one.

Conditions:
  HasExternalId: !Not [!Equals [!Ref ExternalId, '']]

Resources:
  AkeylessUSCRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: AkeylessUSCRole
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
                Action: secretsmanager:ListSecrets
                Resource: '*'
              - Effect: Allow
                Action:
                  - secretsmanager:DescribeSecret
                  - secretsmanager:GetSecretValue
                  - secretsmanager:CreateSecret
                  - secretsmanager:PutSecretValue
                  - secretsmanager:UpdateSecret
                  - secretsmanager:DeleteSecret
                  - secretsmanager:ListSecretVersionIds
                  - secretsmanager:TagResource
                  - secretsmanager:UntagResource
                Resource: !Sub arn:aws:secretsmanager:*:${AWS::AccountId}:secret:*
```

Run these commands from the management account.

**1. Enable StackSets for your Organization** (one time; skip if already enabled):

```shell
aws cloudformation activate-organizations-access
```

**2. Create the StackSet.** Set `<trusted-principal-arn>` to the identity ARN from Step 2. Remove the `ExternalId` line if you don't use one.

```shell
aws cloudformation create-stack-set \
  --stack-set-name akeyless-usc-org-role \
  --template-body file://akeyless-usc-org-role.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --permission-model SERVICE_MANAGED \
  --auto-deployment Enabled=true,RetainStacksOnAccountRemoval=false \
  --parameters \
    ParameterKey=TrustedPrincipalArn,ParameterValue=<trusted-principal-arn> \
    ParameterKey=ExternalId,ParameterValue=<external-id>
```

**3. Deploy it to the OUs you want.** Use the Organization root ID to cover every account, or specific OU IDs.

```shell
aws cloudformation create-stack-instances \
  --stack-set-name akeyless-usc-org-role \
  --deployment-targets OrganizationalUnitIds=<root-or-ou-id> \
  --regions <one-region>
```

<Callout icon="🚧" theme="warn">
  ### Use exactly one Region

  IAM roles are global. Pass a single Region in `--regions`. One role covers Secrets Manager in every Region of the account.
</Callout>

<Callout icon="📘" theme="info">
  ### The management account isn't covered

  StackSets don't deploy to the management account. To manage its secrets, create `AkeylessUSCRole` there with a regular CloudFormation stack using the same template.
</Callout>

If your secrets use customer-managed KMS keys, add `kms:Decrypt` and `kms:GenerateDataKey` for those keys to both the Step 2 policy and `AkeylessUSCRole`.

## Step 4: Configure Akeyless

1. Set your Akeyless AWS Target to use the identity from Step 2. If you used an External ID, set the same value on the target.
2. Create or edit the AWS USC and set its scope to **Organization**.
3. Open the USC. It loads the target's own account and Region first.
4. Pick another account and Region from the **Account** and **Region** dropdowns. The secrets table reloads automatically.

The account list is loaded each time you open the USC, so new accounts in your Organization appear automatically. A new account works once it's in an OU covered by the StackSet.

## Choosing an Account and Region

In the UI, use the **Account** and **Region** dropdowns. If you don't choose, the target's own account and Region are used.

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

## Which Accounts Appear and Which Work

The **Account** dropdown shows every account in your Organization, because `ListAccounts` returns all of them. An account works only if:

- it's the target's own account, or
- it has `AkeylessUSCRole` (deploy the StackSet only to the OUs you want).

Other accounts appear in the list but fail to load.

## Troubleshooting

| Error or symptom                                             | Cause                                                                                     | Fix                                                                                                                                          |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Account discovery fails (`organizations:ListAccounts` error) | The identity is in a regular member account, or it's missing `organizations:ListAccounts` | Follow Step 2. For Option B, check that the delegation policy has the right account ID and identity ARN.                                     |
| An account appears but fails to load                         | `AkeylessUSCRole` doesn't exist there, or its trust policy doesn't match                  | Deploy the StackSet to that account's OU. Check that `TrustedPrincipalArn` is the exact identity ARN and the External ID matches the target. |
| Secrets from the management account don't load               | StackSets don't deploy there                                                              | Create `AkeylessUSCRole` in the management account with a regular stack.                                                                     |
| Fewer secrets than expected                                  | Secrets are listed per Region                                                             | Select the Region where the secrets live.                                                                                                    |
| Access denied reading a secret value                         | The secret uses a customer-managed KMS key                                                | Add `kms:Decrypt` and `kms:GenerateDataKey` for that key.                                                                                    |
