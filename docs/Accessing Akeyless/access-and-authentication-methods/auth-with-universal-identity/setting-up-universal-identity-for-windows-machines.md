---
title: Setting Up Universal Identity for Windows Machines
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Setting Up Universal Identity for Windows Machines
  description: ''
  robots: index
next:
  description: ''
---
To use [Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity) tokens on a Windows machine, you need to set up the machine to accept and automatically rotate tokens using the Akeyless CLI's `uid-auto-rotate` command.

<Callout icon="📘" theme="info">
  `uid-auto-rotate` replaces the PowerShell script and manual Task Scheduler setup previously documented on this page. The same command is also available on Linux and macOS, where auto-rotation is scheduled with cron or a systemd user timer instead of Windows Task Scheduler.
</Callout>

## Prerequisites

* An Akeyless [Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity) Auth Method

* The [Akeyless CLI](https://docs.akeyless.io/docs/cli) installed on the Windows machine

## Steps

1. Generate an **initial** Universal Identity token from the Akeyless UID Auth Method you've already created.

2. Open a terminal (PowerShell or Command Prompt) and initialize auto-rotation:

   ```shell
   akeyless uid-auto-rotate init --uid-token <initial UID token> --rotation-interval 15
   ```

   This saves the token to the default token file and installs a native Windows Task Scheduler job that rotates it automatically at the interval you specify.

   Where:

   * `--uid-token`: The initial Universal Identity token value, generated from your UID Auth Method.

   * `--token-file`: Path to a file that already contains the initial token, to use instead of `--uid-token`. **Note:** `--uid-token` and `--token-file` are mutually exclusive.

   * `--rotation-interval`: **Required.** How often, in minutes, the token should be rotated.

   * `--skip-token-validation`: **Optional.** Skip validating the initial token before saving it.

   * `--force`: **Optional.** Overwrite an existing `uid-auto-rotate` configuration.

   * `--gateway-url`: **Optional.** The Gateway URL to use for token rotation (Configuration Management port, for example `http://localhost:8000`). If not set, defaults to the Akeyless SaaS endpoint.

3. Confirm the scheduled task was created, either by opening **Task Scheduler** and locating the new auto-rotation job, or by running:

   ```shell
   akeyless uid-auto-rotate status
   ```

   This reports the current token file location and scheduling status.

4. Confirm the token file (`~/.uid-token` by default, in the current user's home directory, unless a different path was set with `--token-file`) starts refreshing with a new token at the configured interval.

## Managing Auto-Rotation

* To rotate the token once immediately, without waiting for the next scheduled run:

  ```shell
  akeyless uid-auto-rotate rotate -i <Token_Path>
  ```

* To remove the scheduled rotation job while keeping the existing token file:

  ```shell
  akeyless uid-auto-rotate uninstall -i <Token_Path>
  ```

* To check token and scheduling status at any time:

  ```shell
  akeyless uid-auto-rotate status -i <Token_Path>
  ```

## Legacy Configuration

For the previous PowerShell script and manual Task Scheduler setup, refer to the [legacy Universal Identity setup guide for Windows machines](https://docs.akeyless.io/update/docs/setting-up-universal-identity-for-windows-machines-legacy).