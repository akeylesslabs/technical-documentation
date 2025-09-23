---
title: Deploy a Gateway using CloudFormation
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
This guide explains how to automate the integration with Akeyless using a [CloudFormation](https://aws.amazon.com/cloudformation/) script. The script provisions an EC2 instance with the [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw), creates an IAM Role with permissions to manage IAM users and secrets, and can generate both an [AWS Target](https://docs.akeyless.io/docs/aws-targets) and a [Dynamic Secret](https://docs.akeyless.io/docs/aws-producer) in Akeyless. The entire setup—from infrastructure deployment to integration configuration—is handled end to end.

# General Configuration

The following steps will be used to set up the environment and prepare it for integration with AWS.

## Create an Akeyless Account

1. Go to the Akeyless [Registration Page](https://console.akeyless.io/registration).

2. Sign up and log in to the Akeyless Console using your Email.

## Create an Authentication Methods

In this case, for simplicity, we used [API Key](https://docs.akeyless.io/docs/api-key) and [AWS IAM](doc:aws-iam)Authentication Method.

In the Akeyless Console, navigate to **Users & Auth Methods**.

1. Click **New** > **AWS IAM**.

2. Provide a name AWS Account and click **Finish**. More details about the AWS IAM authentication method can be found [here](https://docs.akeyless.io/docs/aws-iam)

In addition, to create an authentication methods that support user login, for simplicity, we will use [API Key](doc:api-key)

1. Click **New** > **API Key**
2. Provide a name and click **Finish**

> 👍 API Key Credentials
>
> Save the **Access ID** and **Access Key** shown. You’ll need them later.

## Create an Access Role

1. Navigate to [Access Roles](https://docs.akeyless.io/docs/rbac), click **New**.

2. Provide a name and click **Next**.

3. Click **Associate**, then select the **API Key** and the **AWS IAM**  authentication methods.

4. Click **Add** to define permissions:

   * **Type**: **Items** and **Targets** 

   * **Access Path**: Apply recursively

   * **Permissions**: All except Deny

# Gateway Configuration

The following steps will be used to set up the Gateway and create the required **IAM Role** in **AWS**.

## Deploy the Gateway Using AWS CloudFormation

To deploy the Akeyless Gateway using [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html):

1. Open the **AWS Console**, navigate to **CloudFormation** > **Create Stack** > **With new resources (standard)**

2. Select **Upload a template file**, then upload the `yaml` file containing the CloudFormation template.

Set the `AccessId` with your [AWS IAM](https://docs.akeyless.io/docs/aws-iam) Auth Method's `Access ID`, where you can define a list of users that will be able to manage your Gateway settings via the `AllowedAccessID` setting with any other `Access ID`. In our example, we will use the [API Key](doc:api-key) we created earlier; alternatively, you can use your [SAML](https://docs.akeyless.io/docs/saml),[OIDC](https://docs.akeyless.io/docs/openid)as described [here](https://docs.akeyless.io/docs/gateway-k8s#access-permissions).

```yaml Gateway
AWSTemplateFormatVersion: '2010-09-09'
Description: >
  EC2 instance running the Akeyless Gateway ? ready for cross-account
  deployments (no on-instance object creation).

Parameters:
  AccessId:
    Type: String
    Description: Gateway Access ID
  AllowedAccessID:
    Type: String
    Description: Gateway Allowed Access IDs
  ClusterName:
    Type: String
    Description: Logical name of the Akeyless Gateway cluster
  InstanceType:
    Type: String
    Default: t3.medium
    AllowedValues:
      - t2.micro
      - t2.small 
      - t2.medium
      - t2.large
      - t3.micro
      - t3.small
      - t3.medium 
      - t3.large
      - m5.large
  ImageId:
    Type: String
    Description: AMI ID for the instance
  AllowedIP:
    Type: String
    Description: IP/CIDR allowed inbound (e.g. 0.0.0.0/0)
  AllowedPorts:
    Type: CommaDelimitedList
    Default: "22,8000,8081"
    Description: Allowed TCP ports
  KeyName:
    Type: String
    Default: ""
    AllowedPattern: ".*"
    Description: Optional EC2 key pair for SSH
  AssumableRoleArns:
    Type: CommaDelimitedList
    Default: ""
    Description: >
      (Optional) Comma-separated list of role ARNs in *other* AWS accounts
      this gateway is allowed to assume. Leave empty to allow any role.

Conditions:
  HasKey: !Not [!Equals [!Ref KeyName, ""]]
  HasAssumableRoleArns: !Not [!Equals [!Join ["", !Ref AssumableRoleArns], ""]]

Resources:

  DockerInstanceRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub AkeylessGwRole-${AWS::StackName}
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: AkeylessIAMAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              # IAM user-level permissions (same account)
              - Effect: Allow
                Action:
                  - iam:AddUserToGroup    
                  - iam:AttachUserPolicy
                  - iam:CreateAccessKey
                  - iam:CreateLoginProfile
                  - iam:CreateUser 
                  - iam:DeleteAccessKey
                  - iam:DeleteLoginProfile
                  - iam:DeleteUser
                  - iam:DetachUserPolicy
                  - iam:GetLoginProfile
                  - iam:ListAccessKeys 
                  - iam:ListAttachedUserPolicies
                  - iam:ListGroupsForUser 
                  - iam:ListUserPolicies
                  - iam:ListUserTags 
                  - iam:RemoveUserFromGroup
                  - iam:TagUser
                Resource: !Sub arn:aws:iam::${AWS::AccountId}:user/tmp.*
              - Effect: Allow
                Action: iam:ListUsers
                Resource: "*"

              # Cross-account-capable AssumeRole
              - Effect: Allow
                Action: sts:AssumeRole
                Resource: !If
                  - HasAssumableRoleArns
                  - !Ref AssumableRoleArns
                  - "*"

              # AWS Secrets Manager (same account)
              - Effect: Allow
                Action:
                  - secretsmanager:CreateSecret
                  - secretsmanager:DeleteSecret
                  - secretsmanager:DescribeSecret 
                  - secretsmanager:GetSecretValue
                  - secretsmanager:PutSecretValue                     
                  - secretsmanager:TagResource
                  - secretsmanager:UntagResource  
                  - secretsmanager:UpdateSecret
                Resource: !Sub arn:aws:secretsmanager:${AWS::Region}:${AWS::AccountId}:secret:*
              - Effect: Allow
                Action: secretsmanager:ListSecrets
                Resource: "*"

  DockerInstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Roles: [!Ref DockerInstanceRole]

  InstanceSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow specified TCP ports from AllowedIP
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: !Select [0, !Ref AllowedPorts]
          ToPort:   !Select [0, !Ref AllowedPorts]
          CidrIp:   !Ref AllowedIP
        - IpProtocol: tcp
          FromPort: !Select [1, !Ref AllowedPorts]
          ToPort:   !Select [1, !Ref AllowedPorts]
          CidrIp:   !Ref AllowedIP
        - IpProtocol: tcp
          FromPort: !Select [2, !Ref AllowedPorts]
          ToPort:   !Select [2, !Ref AllowedPorts]
          CidrIp:   !Ref AllowedIP

  DockerInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType:        !Ref InstanceType
      ImageId:             !Ref ImageId
      IamInstanceProfile:  !Ref DockerInstanceProfile
      KeyName:             !If [HasKey, !Ref KeyName, !Ref "AWS::NoValue"]
      SecurityGroups:      [!Ref InstanceSecurityGroup]
      Tags:
        - Key: Name
          Value: Akeyless-Gateway-Instance
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          set -e
          exec > >(tee -a /var/log/akeyless-init.log | logger -t user-data -s 2>/dev/console) 2>&1

          # Install Docker & run the gateway container
          apt-get update -y
          apt-get install -y docker.io
          systemctl start docker
          usermod -aG docker ubuntu

          docker run -d -p 8000:8000 -p 8081:8081 \
            -e GATEWAY_ACCESS_ID='${AccessId}' \
            -e ALLOWED_ACCESS_IDS='${AllowedAccessID}' \
            -e CLUSTER_NAME='${ClusterName}' \
            --name akeyless-gw akeyless/base:latest-akeyless

Outputs:
  InstancePublicIP:
    Description: Public IP address of the Gateway EC2 instance
    Value: !GetAtt DockerInstance.PublicIp
  InstanceRoleName:
    Description: Name of the IAM role attached to the instance
    Value: !Ref DockerInstanceRole
  InstanceRoleArn:
    Description: ARN of the IAM role
    Value: !GetAtt DockerInstanceRole.Arn

```
```yaml Gateway With Exmaples
AWSTemplateFormatVersion: '2010-09-09'

Description: EC2 instance with Akeyless Gateway, IAM Role, and automatic producer creation

Parameters:
  AccessId:
    Type: String
    Description: Gateway Access ID

  AllowedAccessID:
    Type: String
    Description: Gateway Allowed Access IDs

  ClusterName:
    Type: String
    Description: Logical name of the Akeyless Gateway cluster

  InstanceType:
    Type: String
    Default: t3.medium
    AllowedValues:
      - t2.micro
      - t2.small
      - t2.medium
      - t2.large
      - t3.micro
      - t3.small
      - t3.medium
      - t3.large
      - m5.large

  ImageId:
    Type: String
    Description: AMI ID for the Ubuntu EC2 instance

  AllowedIP:
    Type: String
    Description: IP address or CIDR block allowed to access the instance (e.g., 0.0.0.0/0)

  AllowedPorts:
    Type: CommaDelimitedList
    Description: List of TCP ports to allow inbound access (e.g., 22,80,443)
    Default: "22,8000,8081"

  KeyName:
    Type: String
    Description: Optional EC2 Key Pair name for SSH access
    Default: ""
    AllowedPattern: ".*"

  AssumeRoleArn:
    Type: String
    Description: ARN of the role to assume for the assume_role dynamic secret

Resources:

  DockerInstanceRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: DockerCloudFormationRole
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action: sts:AssumeRole
            Principal:
              Service:
                - ec2.amazonaws.com
              AWS:
                - !Sub arn:aws:iam::${AWS::AccountId}:root
      Policies:
        - PolicyName: AkeylessIAMAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - iam:AddUserToGroup
                  - iam:AttachUserPolicy
                  - iam:CreateAccessKey
                  - iam:CreateLoginProfile
                  - iam:CreateUser
                  - iam:DeleteAccessKey
                  - iam:DeleteLoginProfile
                  - iam:DeleteUser
                  - iam:DetachUserPolicy
                  - iam:GetLoginProfile
                  - iam:ListAccessKeys
                  - iam:ListAttachedUserPolicies
                  - iam:ListGroupsForUser
                  - iam:ListUserPolicies
                  - iam:ListUserTags
                  - iam:RemoveUserFromGroup
                  - iam:TagUser
                Resource: !Sub "arn:aws:iam::${AWS::AccountId}:user/tmp.*"

              - Effect: Allow
                Action:
                  - iam:ListUsers
                Resource: "*"

              - Effect: Allow
                Action:
                  - sts:AssumeRole
                Resource: !Sub "arn:aws:iam::${AWS::AccountId}:role/*"

              - Effect: Allow
                Action:
                  - secretsmanager:CreateSecret
                  - secretsmanager:DeleteSecret
                  - secretsmanager:DescribeSecret
                  - secretsmanager:GetSecretValue
                  - secretsmanager:PutSecretValue
                  - secretsmanager:TagResource
                  - secretsmanager:UntagResource
                  - secretsmanager:UpdateSecret
                Resource: !Sub "arn:aws:secretsmanager:${AWS::Region}:${AWS::AccountId}:secret:*"

              - Effect: Allow
                Action:
                  - secretsmanager:ListSecrets
                Resource: "*"

  DockerInstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Roles:
        - !Ref DockerInstanceRole

  InstanceSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow specified TCP ports from allowed IP
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: !Select [0, !Ref AllowedPorts]
          ToPort: !Select [0, !Ref AllowedPorts]
          CidrIp: !Ref AllowedIP

        - IpProtocol: tcp
          FromPort: !Select [1, !Ref AllowedPorts]
          ToPort: !Select [1, !Ref AllowedPorts]
          CidrIp: !Ref AllowedIP

        - IpProtocol: tcp
          FromPort: !Select [2, !Ref AllowedPorts]
          ToPort: !Select [2, !Ref AllowedPorts]
          CidrIp: !Ref AllowedIP

  DockerInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      ImageId: !Ref ImageId
      IamInstanceProfile: !Ref DockerInstanceProfile
      KeyName: !If [HasKey, !Ref KeyName, !Ref "AWS::NoValue"]
      SecurityGroups:
        - !Ref InstanceSecurityGroup
      Tags:
        - Key: Name
          Value: Akeyless-Gateway-Instance
      UserData:
        Fn::Base64:
          Fn::Sub:
            - |
              #!/bin/bash
              set -e
              exec > >(tee -a /var/log/akeyless-init.log | logger -t user-data -s 2>/dev/console) 2>&1

              apt update -y
              apt install -y docker.io curl

              if ! command -v jq &> /dev/null; then
                apt install -y jq
              fi

              systemctl start docker
              usermod -aG docker ubuntu

              docker run -d -p 8000:8000 -p 8081:8081 \
                -e GATEWAY_ACCESS_ID="${AccessId}" \
                -e ALLOWED_ACCESS_IDS='${AllowedAccessID}' \
                -e CLUSTER_NAME="${ClusterName}" \
                --name akeyless-gw akeyless/base:latest-akeyless

              sleep 90

              TOKEN=$(curl --silent --request POST \
                --url http://127.0.0.1:8081/auth \
                --header 'accept: application/json' \
                --header 'content-type: application/json' \
                --data "{
                  \"access-type\": \"aws_iam\",
                  \"json\": false,
                  \"access-id\": \"${AccessId}\"
                }" | jq -r '.token')

              echo $TOKEN

              curl --request POST \
                --url http://127.0.0.1:8081/create-aws-target \
                --header 'accept: application/json' \
                --header 'content-type: application/json' \
                --data "{
                  \"json\": false,
                  \"region\": \"us-east-2\",
                  \"use-gw-cloud-identity\": true,
                  \"generate-external-id\": true,
                  \"Role-arn\": \"${RoleArn}\",
                  \"name\": \"AWS-Target\",
                  \"token\": \"$TOKEN\"
                }"

              curl --request POST \
                --url http://127.0.0.1:8081/dynamic-secret-create-aws \
                --header 'accept: application/json' \
                --header 'content-type: application/json' \
                --data "{
                 \"admin-rotation-interval-days\": 0,
                 \"aws-user-console-access\": false,
                 \"aws-user-programmatic-access\": true,
                 \"json\": false,
                 \"region\": \"us-east-2\",
                 \"user-ttl\": \"60m\",
                 \"access-mode\": \"iam_user\",
                 \"token\": \"$TOKEN\",
                 \"name\": \"AWS-Dynamic-Secret\",
                 \"target-name\": \"AWS-Target\"
               }"

              curl --request POST \
                --url http://127.0.0.1:8081/dynamic-secret-create-aws \
                --header 'accept: application/json' \
                --header 'content-type: application/json' \
                --data "{
                 \"admin-rotation-interval-days\": 0,
                 \"aws-user-console-access\": false,
                 \"aws-user-programmatic-access\": true,
                 \"json\": false,
                 \"region\": \"us-east-2\",
                 \"user-ttl\": \"60m\",
                 \"access-mode\": \"assume_role\",
                 \"token\": \"$TOKEN\",
                 \"name\": \"AWS-Dynamic-Secret-Assume-Role\",
                 \"aws-role-arns\": \"${AssumeRoleArn}\",
                 \"target-name\": \"AWS-Target\"
               }"
            - {
                RoleArn: !GetAtt DockerInstanceRole.Arn
              }

Conditions:
  HasKey: !Not [!Equals [!Ref KeyName, ""]]

Outputs:
  InstancePublicIP:
    Description: Public IP of the EC2 instance (use as Gateway URL)
    Value: !GetAtt DockerInstance.PublicIp

  InstanceRole:
    Description: IAM Role attached to the EC2 instance
    Value: !Ref DockerInstanceRole

  InstanceRoleArn:
    Description: ARN of the EC2 IAM Role
    Value: !GetAtt DockerInstanceRole.Arn


```

After uploading the `.yaml` file, set the following parameters:

* **AccessID** – The **Access ID** of the **AWS IAM** Auth Method that was created earlier.

* **AllowedAccessID** – The **Access ID** of the **API Key** Auth Method that was created earlier.

* **AllowedIP** – Your IP address or CIDR block (e.g. `203.0.113.5/32`).

* **AssumeRoleArn** -  ARN of the role to assume for the assume\_role dynamic secret

* **ClusterName** – A name for your Gateway cluster

* **ImageID** – The **AMI ID** of the EC2 image. Run the following command to fetch the latest Ubuntu `22.04` image:

```shell
aws ec2 describe-images \
  --owners 099720109477 \
  --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
  --query "Images | sort_by(@, &CreationDate) | [-1].ImageId" \
  --region <Your-region> \
  --output text
```

* **InstanceType** – e.g. `t3.small`, `t3.medium`
* **KeyName** - Optional, EC2 Key Pair name for SSH access.

3. Click **Next**, then **Create Stack**.

This stack will:

* Launch an [EC2 instance](https://aws.amazon.com/pm/ec2/?refid=3fc1271f-8d0f-43b5-b177-4fba4b680f8b) with Docker installed and ready to run containers.

* Deploy the [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) inside a Docker container on the **EC2 instance** for secure, high-availability access to Akeyless Vault services.

* Create an IAM Role with scoped permissions for managing secrets and IAM users through AWS.

## Log In to the Gateway

First, login to `http://<YOUR_INSTANCE_PUBLIC_IP>:8000/console` , and enter the **Access ID** and **Access Key**, this will automatically update the **Gateway URL**, once done, proceed with the following steps:

1. Visit: `http://<YOUR_INSTANCE_PUBLIC_IP>:8000/console`.

> 👍 Public IP
>
> The `INSTANCE_PUBLIC_IP` can be found under the **Outputs** tab in the CloudFormation stack.

2. Select **Access Key** login.
3. Enter the **Access ID** and **Access Key**.

# Create the Resources in Akeyless

The following steps will create the required resources in Akeyless to generate a temporary **AWS user**, rotate its **Access Key**, and sync the **Access ID** and **Access Key** with **AWS Secrets Manager**.

## Get a temporary user credentials

1. Navigate to **Items**, search for the [Dynamic Secret](https://docs.akeyless.io/docs/aws-producer) named `AWS-Dynamic-Secret` (created by the script), and click **Get Dynamic Secret**.

2. This will generate temporary AWS credentials for a user, which will later be used by the [Rotated Secret](https://docs.akeyless.io/docs/create-an-aws-rotated-secret).

## Create a Rotated Secret

1. Go to **Items** > **New** > **Rotated Secret**, then select **AWS**.

2. Provide a name and location.

3. Under **Target**, select your **AWS target**.

4. For **Rotator Type**, choose **API Key**.

5. Under **Authenticate with the following credentials**, choose **Target credentials**.

6. Enter your **Access Key ID** and **Access Key**

7. Under **Gateway**, choose **This Gateway**, then click **Finish**

Click the **eye** icon to view the current credentials, or select **Rotate Secret** to generate a new set of credentials.

## Create a Universal Secret Connector (USC)

1. Go to **Items** > **New** > **Universal Secret Connector**, and choose **AWS**.

2. Provide a name and location.

3. Under **Target**, select your **AWS target**.

4. Under **Gateway**, select **This Gateway**.

5. Add a prefix for your secrets - (Optional).

6. Click **Finish**, then click **View All Secrets**

You can use the USC to:

* **View**, **update**, and **create** new **AWS secrets**.

* Rotate AWS credentials directly from Akeyless

## Sync the Rotated Secret with your AWS Account

To sync the **Rotated Secret** that was just created with the **AWS Secret Manager**:

1. Choose the **Rotated Secret** item.

2. Go to **Sync** tab, press **Add** and fill the following parameters:

   1. **Universal Secret Connector Name** - The name of the **AWS Universal Secret Connector**.

   2. **Remote Secret Name** - Enter the name of the secret that will be created or updated on your **AWS Secret Manager**.

   3. **Filter secret value (jq)** - Optional, to filter the value of the rotated secret, to sync only specific fields, or to manipulate the value using a jq expression, e.g. `.password` etc.

Once completed, if the secret is rotated in **Akeyless**, its value will be automatically updated in **AWS**.
