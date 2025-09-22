---
title: Sub-Claims
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Sub-Claims
  description: ''
  robots: index
next:
  description: ''
---
For some of the Auth Methods like JWT/OIDC, K8s, SAML, and LDAP that contain sub-claims or attribute-based access control (ABAC), also known as policy-based access control, as part of the given signed token, you can restrict the authorizations of the associated role to these specific claims or attributes. In other words, only clients whose tokens contain these sub-claims (in the case of JWT/OIDC) or attributes (in the case of SAML) will be allowed to access the rules defined in the role.

The sub-claims definition is in the structure of a map that contains keys that represent the field name of the sub-claims, and each key can contain several values ​​so the sub-claim must contain one of those values. The keys and values are case-sensitive.

For example, assume sub-claims are set to:

```json
Groups=Engineering
Email=james@example.com
```

Only JWTs or SAML-XML containing both the `Groups` and `Email` claims/attributes, and respective matching values of `Engineering` and `james@example.com`, would be authorized.

If the expected value is a list, the claim must match one of the items on the list. For example, assume sub-claims are set to:

```json
Groups=Engineering,Security
Email=james@example.com,linda@example.com
```

Only JWTs or SAML-XML containing both the `Groups` and `Email` claims/attributes, and respective matching values of [`Engineering` or `Security`] and [`james@example.com` or `linda@example.com`], would be authorized.

> 📘 Info
> 
> You may also use wildcard characters to allow a wider range of permissions. The supported wildcard characters are:  
> `?`: Replaces one character. For example, the string `1?1` will accept `121` but not `1231`.  
> `*`: Replaces any amount of characters. For example, the string `*@example.com` will accept any address in that domain.

You can set the relevant sub-claims to an existing role using the Akeyless [Command Line Interface (CLI)](doc:cli) 

```shell
akeyless assoc-role-am --role-name r1 --am-name Okta --sub-claims Groups=Engineering,Security  --sub-claims Email=james@example.com,linda@example.com
```

Or directly from the Akeyless Console using the [Access Roles](doc:rbac) with [Authentication Methods](doc:access-and-authentication-methods) association.

# Logical Operators Syntax

While by default between different sub-claims values the logic of the comma symbol  is `OR`, it is possible to use the syntax of `OR`. In addition, to force logical `AND` between different values of a specific sub-claim, you can use the `AND` syntax.

> 📘 Required Version
> 
> The Logicial Operators Syntax support requires Gateway `4.19` version or higher.

For example: 

```json
Groups=Engineering `AND` Security
Email=james@example.com `OR` linda@example.com
```

Only JWTs or SAML-XML containing both the `Groups` and `Email` claims/attributes, and respective matching values of [`Engineering` **AND** `Security`] and [`james@example.com` **OR** `linda@example.com`], would be authorized. In the case of mixing logical operators on the same sub-claim, the order of operation will start from the left.

Note that between different sub-claims keys, the logic will always use the **AND** operator. 

# Path Templating

For easier management of your access rules, sub-claims keys can be utilized for quicker and more scalable rule definitions for the access path. 

Each sub-claim key should be wrapped by double curly braces, i.e. `{{Sub-Claim Name}}` with a `/` as a separator for folders.

For example, say that the following sub-claims exist in your **Access Role**:

```json
Groups=Engineering,Security,DevOps
Username=Alice,Bob,Charlie,Dennis
```

And this is the original mapping in your **Identity Provider**:

| Groups      | Username     |
| :---------- | :----------- |
| Engineering | Alice        |
| Security    | Bob, Charlie |
| DevOps      | Dennis       |

Those claims can be templated as `/{{Groups}}/{{Username}}/*` (or the relevant attribute in your IdP) for your rule path:

```shell
 akeyless set-role-rule --role-name r1 --path "/{{Groups}}/{{Username}}/*"  -c read
```

Each user will get `read` permissions for the relevant paths, based on the sub-claims key values.

This means that `Alice` will get `read` permissions under`/Engineering/Alice/*`, `Bob`&`Charlie` will have access to `/Security/Bob/*` and `/Security/Charlie/*` accordingly, and `Dennis` will have access to `/DevOps/Dennis/*`. 

> 👍 Note
> 
> Templating Access **Rules**  supports Access **Role** case-sensitive settings.

# View Sub-Claims

To review the current Sub-Claims available for your [Authentication Method](doc:access-and-authentication-methods), from the Akeyless Console, simply click on your account logo and click on **Show Sub Claims**. 

To view the available Sub-Claims of your [Authentication Method](doc:access-and-authentication-methods) from the Akeyless [CLI](doc:cli) based on the CLI profile you are using, run the following command: 

```shell
akeyless describe-sub-claims
```

Alternatively, to view a different [Authentication Method](doc:access-and-authentication-methods) available sub-claims you can specify the exact token or the relevant [CLI](doc:cli) profile name:

```shell
akeyless describe-sub-claims --profile <CLI profile>
```