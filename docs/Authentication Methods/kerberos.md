---
title: Kerberos
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
[Kerberos](https://en.wikipedia.org/wiki/Kerberos_(protocol)) is a network authentication protocol that securely verifies the identities of users and services using secret-key cryptography. It operates on a client-server model, centered around a **Key Distribution Center (KDC)**, which includes:

**Authentication Server (AS)**: Issues **Ticket Granting Tickets (TGTs)**.  

**Ticket Granting Server (TGS)**: Provides service tickets for accessing network services.  
The authentication process follows these steps:

1. **Client Sends Credentials to AS**  
   The client sends its credentials (username) to the Authentication Server (AS).

2. **AS Verifies Credentials and Issues TGT**  
   If the credentials are verified, the Authentication Server (AS) issues a Ticket Granting Ticket (TGT).

3. **Client Requests Service Ticket from TGS**  
   The client uses the TGT to request a service ticket from the Ticket Granting Server (TGS).

4. **TGS Issues Service Ticket**  
   The Ticket Granting Server (TGS) verifies the TGT and issues a service ticket for the requested service.

5. **Client Presents Service Ticket to Service Server**  
   The client presents the service ticket to the desired service server for authentication.

This method ensures secure and efficient authentication across the network, making Kerberos a widely used solution for identity verification.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/8a44b2fd698958a43ad9423a017e54f6a5622c1a39655e83267b7a377dea49ec-User_Auth_Flow_2.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


# Prerequisites

To use the **Kerberos** Auth Method in Akeyless, the following accounts and permissions need to be configured:

- **Service Account for the Gateway:** This **Domain User** account is used by the Akeyless Gateway to authenticate with services and perform actions on behalf of users.

- **Service Account for the LDAP Server:** This **Domain User** account is responsible for supplying user data to the **Gateway**, enabling it to verify credentials and complete the authentication process.

- **Admin access to the Active Directory Domain Controller**: Administrative privileges on the Active Directory Domain Controller are required to manage the accounts and services for Kerberos authentication.

- **Active Directory module for Windows**: This [module](https://learn.microsoft.com/en-us/powershell/module/activedirectory/?view=windowsserver2022-ps) needs to be installed in your Windows environment to run the commands described later in this guide. 

# Configuration

To authenticate users or clients to services using **Kerberos**, a [Service Principal Name](https://learn.microsoft.com/en-us/windows/win32/ad/service-principal-names) (SPN) must be registered with an account.

```powershell shell
setspn -U -S HTTP/<SPN> <AccountName>
```

Where:

- `U`: Updates the SPN in Active Directory.
- `S`: Checks for duplicates before adding the SPN
- `SPN`: Your Gateway FQDN, e.g. `my.gateway.com`

# Authentication

Once the SPN is successfully registered, we can proceed with authenticating to the Active Directory using **Kerberos**.

First, we will retrieve the `msDS-KeyVersionNumber` value:

```powershell shell
Get-ADUser <AccountName> -Property msDS-KeyVersionNumber
```

- `msDS-KeyVersionNumber`: An integer that indicates the version of the Kerberos key associated with a **user** or **service principal**.

The retrieved value will be used as the `kvno` parameter on the `ktpass` command. 

## keytab Generation

A [keytab](https://docs.oracle.com/cd/E27515_01/common/tutorials/kerberos_keytab.html) is a file used in Kerberos authentication that contains pairs of Kerberos principals and their corresponding secret keys. It allows services to authenticate to the **Kerberos Key Distribution Center (KDC)** without needing to interactively enter a password.

Run the following command to generate a **keytab** for the user who will be authenticated via Kerberos:

```powershell shell
ktpass /princ <username>@<REALM> /ptype krb5_nt_principal /crypto <EncryptionType> /out <OutputFile> /mapuser <MapUser> /kvno <KeyVersionNumber> /pass <Password>
```

Where:

`princ`: Specifies the Kerberos principal name to be created or modified

`ptype`: Indicates the principal type, defining the nature of the principal

`crypto`: Defines the encryption type used for the principal's key

`out`: Specifies the output filename for the keytab file that will be generated

`mapuser`: Maps the specified principal to a user account in Active Directory

`kvno`: Sets the Key Version Number (**KVNO**) for the principal, used for key management

`pass`: Indicates that a password is required for the user account

## krb5 File

The **krb5 file** is a configuration file for the **Kerberos 5** authentication system. It contains settings that define the **Kerberos realm**, **KDC (Key Distribution Center)** servers, and other Kerberos-related parameters necessary for authentication.

Create the `krb5.conf` File:

```shell krb5.conf
[libdefaults]
  default_realm = MY.TEST.COM
  dns_lookup_realm = false
  dns_lookup_kdc = true
  ticket_lifetime = 24h
  renew_lifetime = 7d
  forwardable = true
  rdns = false
  preferred_preauth_types = 23
[realms]
  MY.TEST.COM = {
    kdc = DC.TEST.COM
    admin_server = DC.TEST.COM
    master_kdc = DC.TEST.COM
    default_domain = MY.TEST.COM
  }
```

Where:

- `default_realm`: Defines the default Kerberos realm

- `dns_lookup_realm`: Controls whether the realm can be discovered via DNS

- `dns_lookup_kdc`: Controls whether the KDC can be discovered via DNS

- `ticket_lifetime`: Specifies how long tickets are valid

- `renew_lifetime`: Specifies how long tickets can be renewed

- `forwardable`: Allows tickets to be forwarded to other services

- `rdns`: Enables or disables reverse DNS lookups for KDC

- `preferred_preauth_types`: Specifies which pre-authentication methods are preferred by the client

Once done, continue with creating a Kerberos Authentication Method:

```shell
akeyless auth-method create kerberos \
--name <Auth Method Name> \      
--krb5conf-file-path /path/to/krb5.conf  \                        
--keytab-file-path /path/to/.keytab \
--ldap-url <LDAP server URL> \
--bind-dn CN=user,CN=Users,DC=TEST,DC=COM \   
--bind-dn-password <bind dn password> \
--user-dn CN=Users,DC=TEST,DC=COM \             
--user-attribute sAMAccountName \
--group-dn CN=Users,DC=TEST,DC=COM \
--group-filter (sAMAccountName={{.Username}}) \      
--group-attr memberOf \
--gateway-url '<https://<Your-Akeyless-GW-URL:8000>' \
--unique-identifier sAMAccountName 
```

Where:

- `name`: A unique name for the authentication method. The name can include the path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

- `krb5conf-file-path`: The path to a valid krb5.conf file, specifying the settings and parameters required for Kerberos authentication

- `keytab-file-path`: The path to a valid keytab file, containing the service account's entry

- `ldap-url`: LDAP server URL, e.g., `ldap://ldap.domain.com:389`

- `bind-dn`: Full DN of the LDAP user to bind with

- `bind-dn-password`: Password for the LDAP Bind DN

- `user-dn`: The base DN for user searches

- `user-attribute`: LDAP attribute that maps to the username used for signing in

- `group-dn`: Base DN for group membership searches

- `group-filter`: Go template for constructing the group membership query

- `group-attr`: LDAP attribute to follow on objects returned by `ldap_group_filter` to enumerate user group membership

- `gateway-url`: Gateway URL (Configuration Management port)

- `unique-identifier`: A unique identifier (ID) value which is a sub-claim name that contains details uniquely identifying that resource. This sub-claim is used to distinguish between different identities

You can find the complete list of additional parameters for this command in the [CLI Reference - Authentication section](https://docs.akeyless.io/docs/cli-reference-kerberos)

Once created, you can use the `akeyless auth` command to authenticate a user via **Kerberos**:

```shell
akeyless auth \
--access-id <Access ID> \
--access-type=kerberos \
--krb5conf-file-path /path/to/krb5.conf \
--keytab-file-path /path/to/keytab
```

Running this command will authenticate the user specified in the `keytab` file to akeyless using **Kerberos**

# Kerberos SSO SDK

To utilize SSO for Kerberos, add the `Akeyless.Kerberos` package to your `.NET` project, and run the following command in your project directory:

```csharp
dotnet add package Akeyless.Kerberos --version 1.0.0
```

For example, set the following:

```csharp
using System;
using System.Runtime.InteropServices;
using akeyless.Api;
using akeyless.Client;
using akeyless.Model;
using Akeyless.Kerberos;

public class Program
{
    static void Main(string[] args)
    {
        try
        {
            if (!RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                Console.WriteLine("This example is only supported on Windows");
                return;
            }

            // SPN (Service Principal Name) for the Akeyless Gateway
            string gatewaySPN = "HTTP/<your-gateway-spn>";

            // URL of the Akeyless Gateway
            string gatewayUrl = "<your-gateway-url>";

            // Retrieve the Kerberos token for the specified SPN
            string kerberosToken = new AkeylessKerberos().GetCurrentUserTokenForSPN(gatewaySPN);

            // Akeyless API Configuration
            Configuration config = new Configuration() { BasePath = gatewayUrl + "/api/v2" };
            V2Api api = new(config);

            // Authentication using Kerberos token
            Auth auth = new()
            {
                AccessId = "<your-access-id>",   // Your Akeyless Access ID
                AccessType = "kerberos",         // Authentication type
                GatewayUrl = gatewayUrl,         // Gateway url
                DisablePafxfast = "true",        // Option to disable Pafxfast
                KerberosToken = kerberosToken   // The Kerberos token retrieved earlier
            };

            // Perform authentication and get the output token
            AuthOutput authOutput = api.Auth(auth);

            // List items using the output token
            ListItems listBody = new() { Token = authOutput.Token };

            ListItemsInPathOutput listOut = api.ListItems(listBody);

            if (listOut.Items != null)
            {
                foreach (var item in listOut.Items)
                {
                    Console.WriteLine(item.ItemName);
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex);
        }
    }
}
```

Make sure to change the following:

 `<your-gateway-spn` with the Service Principal Name for your Akeyless Gateway.

 `<your-gateway-url` with the URL of your Akeyless Gateway.

 `<your-access-id`with your Akeyless Access ID.