---
title: CLI Reference - Universal Identity
excerpt: Akeyless Universal Identity Auth Method
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
This section outlines the CLI commands relevant to Universal Identity authentication.

General Flags:

`--profile, --token`: Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

### <p style={{ color: "blue" }}>*create*</p>

Create a new Auth Method that will be able to authenticate using Akeyless Universal Identity

##### Usage

```shell
akeyless auth-method create universal-identity \
--name &lt;Auth method name&gt; \
--ttl &lt;Token TTL&gt;
```

##### Flags

`-n, --name`: **Required** Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--delete-protection`: Protection from accidental deletion of this object, \[true/false\]

`--force-sub-claims`: enforce role-association must include sub-claims

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--deny-rotate`: Deny from the token to rotate

`--deny-inheritance`: Deny from root to create children

`--ttl[=60]`: Token TTL (has the value that configured in Akeyless console &gt; Authentication settings)

### <p style={{ color: "blue" }}>*uid-create-child-token*</p>

Create a new child token using Akeyless Universal Identity

##### Usage

```shell
akeyless uid-create-child-token \
--child-deny-rotate \
--child-deny-inheritance
```

##### Flags

`--child-deny-rotate`: Deny from new child to rotate

`--child-deny-inheritance`: Deny from new child to create their own children

`--child-ttl`: New child token TTL

`-n, --auth-method-name`: The universal identity auth method name, required only when uid-token is not provided

`--tid, --uid-token-id`: The ID of the uid-token, required only when uid-token is not provided

`--profile` or `--token`: Use a specific Akeyless profile (located at $HOME/.akeyless/profiles) or a temporary access token

`--uid-token`: The universal identity token. It is required only for universal_identity authentication

### <p style={{ color: "blue" }}>*uid-generate-token*</p>

Generate a new token using Akeyless Universal Identity

##### Usage

```shell
akeyless uid-generate-token --auth-method-name &lt;Auth method name&gt;
```

### <p style={{ color: "blue" }}>*uid-list-children*</p>

List the token children ids of Akeyless Universal Identity

##### Usage

```shell
akeyless uid-list-children --auth-method-name &lt;UID Auth Method Name&gt;
```

### <p style={{ color: "blue" }}>*uid-revoke-token*</p>

Revoke token using Akeyless Universal Identity

##### Usage

```shell
akeyless uid-revoke-token \
--revoke-type &lt;revokeSelf/revokeAll&gt; \
--revoke-token &lt;UID Token ID&gt;
```

##### Flags

`--revoke-type`: **Required**, revokeSelf/revokeAll (delete only this token/this token and his children)

`--revoke-token`: **Required**, the universal identity token/token-id to revoke

`-n, --auth-method-name`: The universal identity auth method name

### <p style={{ color: "blue" }}>*uid-rotate-token*</p>

Rotate Akeyless Universal Identity token

##### Flags

`-t, --token, --uid-token`: The Universal identity token to rotate

`--fork`: Create a new child token with default Flags

`--send-manual-ack-token`: The new rotated token to send manual ack for (with uid-token=the-orig-token)

`--with-manual-ack`: Disable automatic ack

`-o, --output-file`: Path to the output file

`-i, --input-file`: Path to the input file

### <p style={{ color: "blue" }}>*update*</p>

Update a new Auth Method that will be able to authenticate using Akeyless Universal Identity

##### Usage

```shell
akeyless auth-method update universal-identity \
--name &lt;Auth method name&gt; \
--new-name &lt;Auth method new name&gt;
```

##### Flags

`--new-name`: Auth Method new name

`-n, --name`: **Required**, Auth Method name

`--descrpition`: Auth Method description

`--access-expires[=0]`: Access expiration date in Unix timestamp (select 0 for access without expiry date)

`--bound-ips`: A comma-separated CIDR block list to allow client access

`--gw-bound-ips`: A comma-separated CIDR block list as a trusted Gateway entity

`--force-sub-claims`: enforce role-association must include sub-claims

`--audit-logs-claims`: Additional sub-claims to include in audit logs. e.g. `--audit-logs-claims email --audit-logs-claims username`

`--delete-protection`: Protection from accidental deletion of this object, \[true/false\]

`--jwt-ttl[=0]`: creds expiration time in minutes. If not set, use default according to account settings (see get-account-settings)

`--deny-rotate`: Deny from the token to rotate

`--deny-inheritance`: Deny from root to create children

`--ttl[=60]`: Token ttl (in minutes)