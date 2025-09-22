---
title: Windows Target
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
You can define a Windows target to be used with an RDP [Rotated Secrets](doc:rotated-secrets). Akeyless Windows Targets use WinRM by default over TLS. While Windows Secrets Rotation also supports SSH targets, for legacy environments, you can work with Akeyless Windows Targets instead. 

# Create a Windows Target in the CLI

To create a Windows target from the CLI, run the following command:

```shell Akeyless CLI
akeyless target create windows \
--name <target name> \ 
--hostname <Windows Hostname\IP> \
--username <Windows Local Username> \
--password <Password>
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `hostname`: The Windows Server Hostname or IP address.

* `username`: A local or domain Windows priviledge username.

* `password`: The password of the Windows user. 

> 👍 Note
>
> **WinRM TLS**
>
> By default, Windows targets are working with TLS. When using a self-signed certificate, you can either load the certificate to your Target, or mount the relevant certificate into your Gateway filesystem under `etc/ssl/certs`

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-reference-akeyless-targets#p-stylecolorblue-create-windows-targetp) section.

# Create a Windows Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Operating System (Windows)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.\
   For more information, [read here](doc:implement-zero-knowledge).

4. Define the remaining parameters as follows:

* **Hostname** ,**Port** , **Username**  and **Domain** to set up the connection. 

* **TLS:** Check to work with TLS and load your CA certificate.

5. Click **Finish**.

# Troubleshooting

While facing connection errors, make sure that WinRM is enabled and that the relevant port is opened  i.e. `5985` for WinRM or `5986` for winRM over TLS and not blocked by a Firewall rule.

**Check WinRM Service Status**:

```powershell
Get-Service -Name WinRM
winrm get winrm/config
```

Verify that the service is configured to listen on the desired address and port.

**Test WinRM Connectivity**:

```powershell
Test-WSMan
# and from a remote server run:
Test-WSMan -ComputerName <RemoteComputer>

Test-NetConnection -ComputerName <RemoteComputer> -Port 5985
```

Replace `<RemoteComputer>` with the actual hostname or IP address of the remote machine and use the `Test-NetConnection` cmdlet to check if WinRM is listening on the default ports (`5985` for HTTP and `5986` for HTTPS).

**Check Firewall Rules**:

Ensure that the firewall on the target machine allows WinRM traffic. You can use the following command to check firewall rules:

```powershell
Get-NetFirewallRule | Where-Object { $_.DisplayName -like "*WinRM*" }
```

**Check Windows Event Logs**: 

Inspect the Windows Event Logs for WinRM-related events that might provide additional information about any issues:

```powershell
Get-EventLog -LogName "Windows PowerShell" -Source "Microsoft-Windows-WinRM"
```
