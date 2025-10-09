---
title: CLI
excerpt: Command Line Interface (CLI)
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
There are multiple methods to interact with the Akeyless Platform for managing, creating, and fetching multiple types of supported [secrets](https://docs.akeyless.io/docs/manage-your-secrets-overview). One of them is our Command Line Interface (CLI).

The Akeyless CLI has pre-compiled binary versions for **Linux, macOS, and Windows** which can be easily installed.

# Download

Run the following commands to download and install the CLI binary:

```shell Linux AMD
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-linux-amd64
chmod +x akeyless
./akeyless
```
```shell Linux ARM
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-linux-arm64
chmod +x akeyless
./akeyless
```
```shell macOS Intel
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-darwin-amd64
chmod +x akeyless
./akeyless
```
```shell macOS Apple Silicon
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/cli-darwin-arm64
chmod +x akeyless
./akeyless
```
```powershell Windows
curl -o akeyless.exe https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-windows-amd64.exe
.\akeyless.exe
```

Or using the Homebrew package manager for **macOS (or Linux)**:

```shell Brew
brew install akeylesslabs/tap/akeyless
```

To download the latest version of the CLI, please make sure that the `https://akeyless-cli.s3.*` endpoint is trusted.

# Installation

Running the CLI for the first time by default, prompts you to configure the basic settings.

For example, the default Akeyless URL is `vault.akeyless.io`. This value is changed if you are running in a different SaaS environment. Press Enter to keep the default value.

```shell
AKEYLESS-CLI, first use detected
For more info please visit: https://docs.akeyless.io/docs/cli 
By default, the Akeyless URL is vault.akeyless.io. Use a different URL if another SaaS environment is being used.
Please type your answer: (Default: vault.akeyless.io) 
```

At the prompt `Would you like to configure a profile? (Y/n)` line, type `Y`. Type a name for the profile or press Enter to leave the name as `default`.

```shell
Would you like to configure a profile? (Y/n) Y
Profile Name:  (Default: default)
```

Choose an <Anchor label="Authentication Method" target="_blank" href="https://docs.akeyless.io/docs/access-and-authentication-methods">Authentication Method</Anchor>  from the list to configure the profile with. Press `Enter` to use the default  [API Key](https://docs.akeyless.io/docs/api-key) method. Set the relevant **Access ID** and **Access Key**:

```shell Shell
Access ID: '<Access-ID>' 
access-key '<Access-Key>' 
'Profile default successfully configured'
```

Continue with installing the Akeyless CLI, depending on your operating system

## Linux \ Mac

Once the authentication succeeds, follow the prompt to add the CLI executable to your `$PATH` :

```shell
Would you like to move 'akeyless' binary to: /home/username/.akeyless/bin/akeyless? (Y/n) 
The cli was successfully moved to path: /home/username/.akeyless/bin/akeyless
Would you like to add '/home/username/.akeyless/bin' To user PATH environment variable? (Y/n)
Please run the following command to start using Akeyless CLI:
	'source ~/.bash_profile'
```

The CLI will try to locate the user profile file (based on shell, i.e `.bash_profile`, `.zprofile`, `.profile`, etc), and export the `USER_HOME_DIR/.akeyless/bin/` to user `$PATH`.

Try running the `create-secret`command to test your installation:

```shell
akeyless create-secret --name MySecret1 --value MySecretPassword
```

## Windows

> 📘 Note
>
> PowerShell ISE does not support interactive input mode. Please work with the PowerShell cmdlet to set up the Akeyless CLI.

Once the authentication succeeds, the following prompt will appear:

```shell
Would you like to move 'akeyless.exe' binary to: C:\Users\username\.akeyless\bin\akeyless.exe? (Y/n)
#after user inputs 'Y'
The cli was successfully moved to path: C:\Users\username\.akeyless\bin\akeyless.exe
```

After the Akeyless CLI Binary is moved to `USER_HOME_DIR/.akeyless/bin/akeyless`, another prompt will appear:

```shell
Would you like to add 'C:\Users\username\.akeyless\bin' To user PATH environment variable? (Y/n)
#after user inputs 'Y'
Run the following command to start using Akeyless CLI:
set "PATH=%PATH%;C:\Users\username\.akeyless\bin" (Update PATH for current session)
setx PATH "%PATH%;C:\Users\username\.akeyless\bin" (Update PATH permenantly)
```

> 👍 Note
>
> The CLI updates the path env for the **current user only**.  This change only takes effect after the user logs off and logs back on.

Copy and run the relevant command for your purpose (`permanent` or `current session`), after that, The CLI should be ready to use.

Try running the `create-secret`command to test your installation:

```shell
akeyless create-secret --name MySecret1 --value MySecretPassword
```

## Non-Interactive Mode

To initiate the CLI non-interactively, run`./akeyless --init` which will work once only during the first time you run the CLI on that environment.
If you're working with a different  tenant environment than the default, i.e. `vault.akeyless.io`, you can use the `--akeyless-url` flag to specify the tenant that the CLI will be configured to communicate with.
For example, to work with the `eu` tenant you would run:

```shell
./akeyless --init --akeyless-url vault.eu.akeyless.io
```

# Authentication

The CLI supports various types of [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods):

1. [API Key](https://docs.akeyless.io/docs/api-key) (`access_key`)
2. [AWS IAM](https://docs.akeyless.io/docs/aws-iam) (`aws_iam`)
3. [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad) (`azure_ad`)
4. [SAML](https://docs.akeyless.io/docs/saml) (`saml`)
5. Password (`email/password`)
6. [Certificate ](https://docs.akeyless.io/docs/certificate-based-authentication) (`certificate`)
7. [OIDC](https://docs.akeyless.io/docs/openid) (`oidc`)
8. [K8s](https://docs.akeyless.io/docs/kubernetes-auth) (`k8s`)
9. [GCP](https://docs.akeyless.io/docs/gcp-auth-method) (`GCP`)
10. [OCI](https://docs.akeyless.io/docs/oci-iam) (`oci`)

For security reasons, if the correct credentials are not entered, the Akeyless CLI will not provide an error message immediately. Instead, you will receive an error message when attempting to run commands.

To initiate the CLI non-interactively, run`./akeyless --init` which will work once only during the first time you run the CLI on that environment.
If you're working with a different  tenant environment than the default, i.e. `vault.akeyless.io`, you can use the `--akeyless-url` flag to specify the tenant that the CLI will be configured to communicate with.
For example, to work with the `eu` tenant you would run:

```shell
./akeyless --init --akeyless-url vault.eu.akeyless.io
```

# Working with profiles

Akeyless CLI supports profiles that can be set with different authentication methods and permissions. If you wish to configure a new profile, use the following command:

```shell
akeyless configure --profile <new profile name> --access-id <Access id> --access-key <Access key> --access-type access_key
```

While the default method is an [API key](https://docs.akeyless.io/docs/api-key), if you wish to use a different authentication method, please consult the [CLI reference](https://docs.akeyless.io/docs/cli-reference#p-stylecolorblueconfigurep) for this command.

To view the profile settings file, go to the `.akeyless` folder under your `home` directory, the profiles folder contains a `toml` file for each profile.

```shell
cd .akeyless/profiles/
```

After you've created an additional profile, add the `--profile` parameter with the profile name to any `akeyless` command to use it under that profile.

## Advanced Configuration

When creating a profile in the CLI, the profile contains only the Authentication Method settings, such as `Access ID`,  and `Access Type`.

However, you can configure additional parameters as defaults in your profile. Once set, these default parameters will automatically be used for your commands unless you choose to override them explicitly.

The following parameters can be added to a profile, for example, on the`deafult` profile:

```toml default.toml
["default"]
  gateway_url = 'https://<Your-Akeyless-GW-URL:8000>'
  default_location_prefix = 'non-production' 
  cert_issuer_name = '/cert/IssuerName'
  cert_username = 'ubuntu'
  public_key_file_path = 'ssh/id_rsa.pub'
  legacy_signing_alg = 'true|false'
```

Where:

* `gateway_url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `default_location_prefix`:  A global default prefix for the `name` flag, relevant for all types of objects in the account. In the example above, all commands will be performed on `/non-production` folder.

* `cert_issuer_name`: The default name of an [SSH Certificate Issuer](https://docs.akeyless.io/docs/how-to-configure-ssh) to use.

* `cert_username`:  The username the SSH certificate Issuer will issue the certificate for, e.g `ubuntu`.

* `public_key_file_path`: Path to the file containing the SSH public key.

* `legacy_signing_alg`: Set this option to use the  SSH legacy signing algorithm.

# Working with the Gateway

To re-route the entire traffic directly via your [Gateway](https://docs.akeyless.io/docs/api-gw) for closed environments, create an environment variable `AKEYLESS_GATEWAY_URL` to point your CLI to interact with the relevant Gateway:

```shell Linux
export AKEYLESS_GATEWAY_URL=<https://Your_GW_URL:8000/api/v1> 
```
```shell Windows
set AKEYLESS_GATEWAY_URL=<https://Your_GW_URL:8080>
```

In case your Gateway uses a self-signed certificate not trusted by your machine, set the environment variable `AKEYLESS_TRUSTED_TLS_CERTIFICATE_FILE` with the location of your `PEM` file.

# Working with Zero-Knowledge Encryption

You can work with items that are protected by [Zero-Knowledge Encryption](https://docs.akeyless.io/docs/zero-knowledge) from the CLI without specifying the Gateway, as Akeyless will automatically detect it based on the **Customer Fragment ID**.

However, if the `AKEYLESS_GATEWAY_URL` environment variable is set, Akeyless will use the Gateway from that variable, and the automatic detection won't work.

# Precedence Configuration

Settings can be found in various locations, such as environment variables, the `profile` configuration file, or directly as command-line parameters. Some locations have higher precedence than others, in this order:

1. **Command line options**:  Overrides settings in any other location, including environment variables and profile configuration file.

2. **Environment variables**: Overrides settings in the profile configuration file.

3. **Profile file**: Values in the profile are used only if no explicit parameters or environment variables are set.

# Troubleshooting

For access deny issues, ensure the following:

* **Permissions**: Make sure the authentication method you created the profile with is associated with the proper role with the authority to perform the action you tried.

* **Profile configuration file**: Make sure your profile configuration file is valid and that everything is spelled correctly and matches the authentication method you chose.

# Tutorial

Check out our tutorial video on [Installing and Configuring the CLI](https://tutorials.akeyless.io/docs/installing-and-configuring-akeyless-cli).
