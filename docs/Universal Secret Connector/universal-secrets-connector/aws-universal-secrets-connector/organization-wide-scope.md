---
title: Organization-Wide Scope
deprecated: false
hidden: false
metadata:
  robots: index
---
This page describes how to extend an [AWS Universal Secrets Connector](https://docs.akeyless.io/docs/aws-universal-secrets-connector) (**USC**) across an entire AWS Organization. With org-wide scope, a single **USC** item can discover and manage secrets in every member account and Region in scope, instead of being limited to the single account and Region tied to its [AWS Target](https://docs.akeyless.io/docs/aws-targets).

## How It Works

AWS has no organization-level IAM binding that applies automatically to every member account. A trusted cross-account role must be deployed into each member account individually, and AWS does not provide a built-in way to be notified when a new account joins the organization. Org-wide AWS **USC** addresses both gaps:

* **Provisioning**: An Akeyless-provided CloudFormation StackSet template deploys the IAM role Akeyless needs into every account in scope, including accounts added to the organization later.

* **Discovery**: AWS Organizations account-membership events, forwarded to Akeyless, trigger an inventory refresh as soon as a new account joins. A periodic reconciliation poll serves as a backstop.

Once provisioned, a single AWS **USC** item is no longer bound to one account and Region. You can target any in-scope account and Region per request by supplying either a full secret ARN or a discrete **Account ID** and **Region** pair wherever a secret identifier is accepted.

## Prerequisites

* An existing [AWS Universal Secrets Connector](https://docs.akeyless.io/docs/aws-universal-secrets-connector), associated with an [AWS Target](https://docs.akeyless.io/docs/aws-targets) that has an [External ID](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html) configured.

* Permission in AWS Organizations to deploy a CloudFormation StackSet with **service-managed permissions** and **automatic deployment** against the organization root or a chosen Organizational Unit (OU).

* A decision on which account authenticates the integration to AWS Organizations: the **management account** or a **delegated administrator** account. See [Choosing the Authenticating Account](#choosing-the-authenticating-account).

## Provisioning the Cross-Account Role

The following CloudFormation template creates the IAM role that the Akeyless Gateway assumes in each member account. Save it as `akeyless-usc-org-role.yaml`.

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
    Description: ARN of the IAM principal used by your Akeyless AWS Target to assume this role.
  ExternalId:
    Type: String
    NoEcho: true
    Description: External ID configured on your Akeyless AWS Target.

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
            Condition:
              StringEquals:
                sts:ExternalId: !Ref ExternalId
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

The template creates an IAM role in every in-scope account with the following configuration:

* A trust policy that references the External ID configured on your Akeyless AWS Target.
* A permission policy that matches the [permission set documented for AWS USC](https://docs.akeyless.io/docs/aws-universal-secrets-connector#prerequisites), applied uniformly through the StackSet instead of being configured manually per account.

To deploy the template:

1. Create the StackSet with **service-managed permissions** and **automatic deployment** enabled. Run this command from the authenticating account:

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
     --call-as DELEGATED_ADMIN
```

If you authenticate from the management account, set `--call-as SELF`.

2. Deploy stack instances against the organization root or a specific OU:

```shell
   aws cloudformation create-stack-instances \
     --stack-set-name akeyless-usc-org-role \
     --deployment-targets OrganizationalUnitIds=<root-or-ou-id> \
     --regions <single-region> \
     --call-as DELEGATED_ADMIN
```

AWS Organizations keeps the role in sync automatically. The role is created in every account currently in the targeted scope and deployed automatically into any account added to that scope afterward, with no separate activation step required in Akeyless.

<Callout icon="🚧" theme="warn">
  ### Deploy to a Single Region

  IAM roles are global resources. Specify exactly one Region in `--regions`. Deploying the StackSet to multiple Regions in the same account fails because the role name already exists. The role still grants access to Secrets Manager in every Region of that account.
</Callout>

<Callout icon="📘" theme="info">
  ### Management Account Coverage

  Service-managed StackSets do not deploy stack instances to the management account. If the management account holds secrets you want the connector to manage, create the role there manually using the same template.
</Callout>

To change the scope later, for example to add or remove an OU, run `create-stack-instances` or `delete-stack-instances` against the new set of targets.

## Choosing the Authenticating Account

AWS Organizations requires a single account to authenticate the [account discovery](#account-discovery) integration. You can use one of the following:

* **Management account**: The simplest option, requiring no additional AWS-side setup. Note that many organizations' security policies restrict placing third-party roles in the management account, so this option might not be available to you.

* **Delegated administrator** (recommended): Keeps the Akeyless integration role out of the management account.

<Callout icon="🚧" theme="warn">
  ### Delegated Administrator Constraints

  Before registering a delegated administrator for Akeyless, note the following:

  * AWS limits an organization to 5 registered delegated administrators in total, shared across every AWS service and vendor that uses this pattern, such as Security Hub, GuardDuty, or other third-party integrations. Confirm you have an available slot before registering Akeyless.
  * A delegated administrator registered for StackSets receives full organization-wide StackSet deployment authority, which the management account cannot further restrict at the AWS Organizations level. To narrow the scope, target a specific OU with the StackSet itself rather than relying on a permission boundary on the delegated administrator.
</Callout>

## Account Discovery

To keep the connector inventory current as accounts are added to or removed from the organization, configure an EventBridge rule in the authenticating account that listens for the following native AWS Organizations account-membership events and forwards them to Akeyless:

* `AccountJoinedOrganization`: Triggers an immediate inventory refresh and begins scanning the new account.

* `AccountDepartedOrganization`: Flags the removed account for review.

This detects organization membership changes in near real time, without waiting for a periodic re-sync.

As a backstop, Akeyless also periodically polls the AWS Organizations `ListAccounts` API to reconcile its inventory. This catches any account change missed by the EventBridge rule, for example in an organization where the rule has not been configured.

## Addressing Secrets by Account ID and Region

AWS Secrets Manager calls are addressed by secret name or ARN. The account and Region are determined by the assumed role and the regional endpoint used. To target a specific account and Region from an org-wide AWS **USC** item, provide one of the following wherever a secret identifier is accepted:

* A full **ARN**: `arn:aws:secretsmanager:<region>:<account-id>:secret:<name>`

* A secret name together with discrete **Account ID** and **Region** parameters, as an alternative to the full ARN.

The Gateway resolves the supplied identifier to the matching regional endpoint and the per-account role provisioned by the StackSet, then assumes that role before calling AWS Secrets Manager.

Account and Region targeting is supported consistently across every surface that resolves an AWS-backed **USC** item:

* **CLI**: Pass an Account ID and Region, or supply a full ARN as the secret identifier, on commands such as `akeyless usc get`, `akeyless usc create`, `akeyless usc update`, and `akeyless usc delete`. For the exact flags, see the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector).

* **API**: The Get, Describe, and List request messages for AWS-backed **USC** items accept the same optional Account ID and Region (or ARN) fields, so Terraform, SDKs, and other programmatic callers can target a specific account and Region without using the CLI.

* **Sync**: Each [sync](https://docs.akeyless.io/docs/sync-secret) mapping to an AWS-backed **USC** item has its own Account ID and Region (or ARN), set at configuration time, since a sync mapping is a standing configuration rather than a one-off call.

* **Injector**: The [Akeyless Kubernetes Secrets Injector](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector) annotation syntax for an AWS-backed secret reference can specify an Account ID and Region (or ARN) per secret. This lets a single Injector deployment pointed at one org-wide **USC** item pull different secrets from different accounts and Regions within the same workload.

<Callout icon="📘" theme="info">
  ### Assumed-Role Session Caching

  Targeting a different account requires the Gateway to call `sts:AssumeRole` before the first access to that account. AWS STS sessions are valid for up to one hour. The Gateway caches assumed-role sessions per Account ID and reuses them until they are near expiry, rather than re-assuming the role on every fetch. This avoids unnecessary latency and STS rate limits when a single **USC** item spans many accounts.
</Callout>

## Global and All-Regions Aggregation

Aggregating secrets across every Region, and, combined with org-wide provisioning, across every account in scope, into a single inventory view is a governance-focused capability that is separate from the per-secret Account ID and Region addressing described above. Each individual AWS secret still resides in exactly one Region, except for native AWS Secrets Manager cross-Region replicas.
