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
To use [Universal Identity](https://docs.akeyless.io/docs/universal-identity) tokens for a Windows machine, you need to set up the machine to accept and renew tokens (through the use of **PowerShell** and **Task Scheduler**).

# Prerequisites

* An Akeyless [Universal Identity](https://docs.akeyless.io/docs/universal-identity) Auth Method

# Steps

1. On the Windows machine, create the following [PowerShell script](https://download.akeyless.io/Akeyless_Artifacts/Windows/Universal_Identity/), where you can replace the`$HOME` (wherever it appears in the script) with the home directory of the user who is going to use this token to authenticate.\
   Save the script as **akeyless\_universal\_identity.ps1**.

> 👍 Tip
>
> If the `gwURL` parameter is not set to `https://<Your-Akeyless-GW-URL:8000/api/v1>`, it will default to` https://rest.akeyless.io`

Create the PowerShell script:

```powershell
 # akeyless_universal_identity.ps1

Param(
    [string]
    $uidToken = "",

    [string]
    $gwURL = "",

    [switch]
    $Init
)

if(Test-Path alias:curl) {
	Remove-item alias:curl
}

if([string]::IsNullOrEmpty($gwURL)) {
    $proxy_url = "https://rest.akeyless.io/"
} else {
    $proxy_url = $gwURL
}

if($Init -eq $true) {
    if([string]::IsNullOrEmpty($uidToken)) {
        $uidToken = Read-Host -Prompt "Universal ID Token"
    }
            
    $sched_task_name = "akeyless_universal_identity_rotator"
    $token_file      = "$HOME\.vault-token" # replace $HOME with user's home directory

    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072

    Write-Host "Starter token received [$uidToken]"

    if([string]::IsNullOrEmpty($uidToken)) {
        Write-Host "Error! empty u-token"
    } else {
	$uidToken | Out-File $token_file -NoNewline
        $script_name = "akeyless_universal_identity.ps1"
        $script_path = "$(Get-Item -Path ".\")\${script_name}"
        $task_to_run = "powershell -noninteractive -File '${script_path}'"

        if (schtasks /query | Select-String $sched_task_name -Quiet) # if sched_task already running, delete it first
        {
            schtasks /delete /tn $sched_task_name /f
        }
        # run sched task every 10 minutes
        schtasks /create /sc MINUTE /tn $sched_task_name /tr $task_to_run /it /mo 10
        #schtasks /create /sc MINUTE /tn $sched_task_name /tr $task_to_run /ru "SYSTEM" /mo 10

        Write-Host "AKEYLESS Universal Identity successfully initiated"
    }
}
else {
    $base_dir="$HOME" # replace with user's home directory
    $token_file="$base_dir\.vault-token"

    if (!([System.IO.File]::Exists($token_file))) {
        Write-Host "Error! token file [$token_file] wasn't found"
        exit 1
    }

    $cur_token=Get-Content -Path $token_file

    if(Test-Path alias:curl) {
        Remove-item alias:curl # to avoid conflict with CmdLet Invoke-WebRequest
    }
    
    $cur_token = $cur_token.replace('+','%2b')
    $res = (curl -s $proxy_url -d "cmd=uid-rotate-token&&uid-token=$cur_token" | Select-String 'ROTATED TOKEN:' | Out-String).Trim()
    
    if([string]::IsNullOrEmpty($res)) {
        Write-Host "Error! empty response"
    } else {
	$uidToken = ($res.Split(" ")[2]).replace('[','').replace(']"','')
    	
    	Write-Host "NEW TOKEN: [$uidToken]"
    	if([string]::IsNullOrEmpty($uidToken)) {
        	Write-Host "Error! empty u-token"
    	} else {
        	$uidToken | Out-File $token_file -NoNewline
    	}
    }
}
```

2. Open **PowerShell**, and run the script using the following command, where you will be requested to insert your **initial** Universal ID token which you should first generate from the Akeyless UID Auth Method you've already created:

```powershell
./akeyless_universal_identity.ps1 -Init
```

> 👍 Note
>
> The script also auto-creates the task-scheduler job, which will rotate your u-token every 10 minutes

3. Open **Task Scheduler**, and modify the settings of the newly created task (`akeyless_universal_identity_rotator`) to use the following options:

<Image align="center" className="border" width="smart" border={true} src="https://files.readme.io/a78ce9d-universal-identity.png" />

4. Confirm the newly created `$HOME\.vault-token` file should start refreshing with a new `u-token` every 10 minutes.
