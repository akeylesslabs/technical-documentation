---
title: CLI
slug: cli
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

The Akeyless CLI has pre-compiled binary versions for **Linux**, **macOS**, and **Windows** that can be installed locally.

## Download

Run the following commands to download and install the CLI binary:

```shell Linux AMD
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/cli-linux-amd64
chmod +x akeyless
./akeyless
```
```shell Linux ARM
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/cli-linux-arm64
chmod +x akeyless
./akeyless
```
```shell macOS Intel
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/cli-darwin-amd64
chmod +x akeyless
./akeyless
```
```shell macOS Apple Silicon
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/cli-darwin-arm64
chmod +x akeyless
./akeyless
```
```powershell Windows
curl -o akeyless.exe https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/cli-windows-amd64.exe
.\akeyless.exe
```

Alternatively, you can install it using a package manager, such as: `brew`, `apt`, `yum`, or `dnf`:

```shell brew
brew install akeylesslabs/tap/akeyless
```
```shell apt
apt-get update && apt-get install -y curl gnupg

curl -fsSL https://akeyless.jfrog.io/artifactory/api/security/keypair/akeyless_cli_repo/public |
gpg --dearmor -o /usr/share/keyrings/akeyless.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/akeyless.gpg] https://akeyless.jfrog.io/artifactory/akeyless-cli-debian stable main" |
tee /etc/apt/sources.list.d/akeyless.list

apt-get update
apt-get install -y akeyless
```
```shell yum
yum install -y curl gnupg2

curl -fsSL https://akeyless.jfrog.io/artifactory/api/security/keypair/akeyless_cli_repo/public -o /tmp/akeyless-gpg.key
rpm --import /tmp/akeyless-gpg.key
rm -f /tmp/akeyless-gpg.key

cat > /etc/yum.repos.d/akeyless.repo <<'EOF'
[akeyless]
name=Akeyless CLI Repository
baseurl=https://akeyless.jfrog.io/artifactory/akeyless-cli-rpm
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://akeyless.jfrog.io/artifactory/api/security/keypair/akeyless_cli_repo/public
EOF

yum clean all
yum makecache
yum install -y akeyless
```
```shell dnf
dnf install -y curl gnupg2

curl -fsSL https://akeyless.jfrog.io/artifactory/api/security/keypair/akeyless_cli_repo/public -o /tmp/akeyless-gpg.key
rpm --import /tmp/akeyless-gpg.key
rm -f /tmp/akeyless-gpg.key

cat > /etc/yum.repos.d/akeyless.repo <<'EOF'
[akeyless]
name=Akeyless CLI Repository
baseurl=https://akeyless.jfrog.io/artifactory/akeyless-cli-rpm
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://akeyless.jfrog.io/artifactory/api/security/keypair/akeyless_cli_repo/public
EOF

dnf clean all && dnf makecache && dnf install -y akeyless
```

To download the latest version of the CLI, ensure that the `https://akeyless-cli.s3.*` endpoint is trusted.

## Configuration

Running the CLI for the first time prompts for basic setup.

```shell
AKEYLESS-CLI, first use detected
For more info please visit: https://docs.akeyless.io/docs/cli
```

At the `Would you like to configure a profile? (Y/n)` prompt, type `Y`. Type a name for the profile or press Enter to leave the name as `default`.

```shell
Would you like to configure a profile? (Y/n) Y
Profile Name: (Default: default)
```

Choose an [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) from the list to configure the profile with. Press `Enter` to use the default [API Key](https://docs.akeyless.io/docs/auth-with-api-key) method. Set the relevant **Access ID** and **Access Key**:

```shell
Access ID: '<Access-ID>'
access-key '<Access-Key>'
'Profile default successfully configured'
```

> ℹ️ **Note:**
>
> During first-time setup, the CLI prompts for an Akeyless URL only when the configured Access ID is in legacy form, without an environment tag.

Continue with installing the Akeyless CLI, depending on your operating system.

### Linux and macOS

Once the authentication succeeds, follow the prompt to add the CLI executable to your `$PATH`:

```shell
Would you like to move 'akeyless' binary to: /home/username/.akeyless/bin/akeyless? (Y/n)
The cli was successfully moved to path: /home/username/.akeyless/bin/akeyless
Would you like to add '/home/username/.akeyless/bin' To user PATH environment variable? (Y/n)
Please run the following command to start using Akeyless CLI:
    'source ~/.bash_profile'
```

The CLI tries to locate the user profile file, such as `.bash_profile`, `.zprofile`, or `.profile`, and exports `USER_HOME_DIR/.akeyless/bin/` to the user `$PATH`.

Try running the `create-secret` command to test your installation:

```shell
akeyless create-secret --name MySecret1 --value MySecretPassword
```

### Windows

> ℹ️ **Note:**
>
> PowerShell ISE does not support interactive input mode. Use the PowerShell cmdlet to set up the Akeyless CLI.

Once the authentication succeeds, the following prompt appears:

```shell
Would you like to move 'akeyless.exe' binary to: C:\Users\username\.akeyless\bin\akeyless.exe? (Y/n)
#after user inputs 'Y'
The cli was successfully moved to path: C:\Users\username\.akeyless\bin\akeyless.exe
```

After the Akeyless CLI binary is moved to `USER_HOME_DIR/.akeyless/bin/akeyless`, another prompt appears:

```shell
Would you like to add 'C:\Users\username\.akeyless\bin' To user PATH environment variable? (Y/n)
#after user inputs 'Y'
Run the following command to start using Akeyless CLI:
set "PATH=%PATH%;C:\Users\username\.akeyless\bin" (Update PATH for current session)
setx PATH "%PATH%;C:\Users\username\.akeyless\bin" (Update PATH permanently)
```

> ℹ️ **Note:**
>
> The CLI updates the path environment variable for the **current user only**. This change takes effect after the user logs off and logs back on.

Copy and run the relevant command for your purpose, `permanent` or `current session`. After that, the CLI is ready to use.

Try running the `create-secret` command to test your installation:

```shell
akeyless create-secret --name MySecret1 --value MySecretPassword
```

### Non-Interactive Mode

To initiate the CLI non-interactively, run `./akeyless --init`. This command works only the first time you run the CLI in that environment. To re-run the command, delete ~/.akeyless directory or rename it.

If you're working with a different tenant environment than the default, that is `vault.akeyless.io`, use the `--akeyless-url` flag to specify the tenant that the CLI should communicate with.

For example, to work with the `eu` tenant:

```shell
./akeyless --init --akeyless-url vault.eu.akeyless.io
```

## Authentication

The CLI supports various types of [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods):

1. [API Key](https://docs.akeyless.io/docs/auth-with-api-key) (`access_key`)
2. [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws) (`aws_iam`)
3. [Azure Active Directory](https://docs.akeyless.io/docs/auth-with-azure) (`azure_ad`)
4. [SAML](https://docs.akeyless.io/docs/auth-with-saml) (`saml`)
5. Password (`email/password`)
6. [Certificate](https://docs.akeyless.io/docs/auth-with-certificate) (`certificate`)
7. [OIDC](https://docs.akeyless.io/docs/auth-with-oidc) (`oidc`)
8. [Kubernetes](https://docs.akeyless.io/docs/auth-with-kubernetes) (`k8s`)
9. [GCP](https://docs.akeyless.io/docs/auth-with-gcp) (`gcp`)
10. [OCI](https://docs.akeyless.io/docs/auth-with-oci) (`oci`)

For security reasons, if the correct credentials are not entered, the Akeyless CLI will not provide an error message immediately. Instead, an error message appears when attempting to run commands.

## CLI Profiles

For profile creation, default profile behavior, settings precedence, and profile-specific commands, see [CLI Profiles](https://docs.akeyless.io/docs/cli-profiles).

## Working With the Gateway

To route CLI API calls through a [Gateway](https://docs.akeyless.io/docs/gateway-overview) in a non-public, air-gapped, or network-isolated environment, set the `AKEYLESS_GATEWAY_URL` environment variable to the relevant Gateway API endpoint. For non-public Gateway API access, include `/api/v1` in the value:

```shell Linux
export AKEYLESS_GATEWAY_URL=https://Your_GW_URL:8000/api/v1
```
```shell Windows
set AKEYLESS_GATEWAY_URL=https://Your_GW_URL:8000/api/v1
```

For this scenario, the profile field `gateway_url` is not used for general CLI API calls.

If your Gateway uses a self-signed certificate that is not trusted by your machine, set the environment variable `AKEYLESS_TRUSTED_TLS_CERTIFICATE_FILE` with the location of your `PEM` file.

## Working With Zero-Knowledge Encryption

You can work with items that are protected by [Zero-Knowledge Encryption](https://docs.akeyless.io/docs/zero-knowledge) with the CLI without specifying the Gateway, as Akeyless will automatically detect it based on the **Customer Fragment ID**.

However, if the `AKEYLESS_GATEWAY_URL` environment variable is set, Akeyless will use the Gateway from that variable, and the automatic detection will not work.

## Troubleshooting

For access-denied issues, ensure the following:

* **Permissions**: Make sure the authentication method used to create the profile is associated with the proper role with the authority to perform the action you tried.
* **Profile configuration file**: Make sure the profile configuration file is valid and that all values are spelled correctly and match the chosen authentication method.

## Tutorial

Check out the tutorial video on [Installing and Configuring the CLI](https://tutorials.akeyless.io/docs/installing-and-configuring-akeyless-cli).
