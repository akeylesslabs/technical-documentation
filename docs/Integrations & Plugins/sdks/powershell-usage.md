---
title: PowerShell Usage
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
Akeyless Platform natively supports multiple scripting languages, the following examples demonstrate how to fetch secrets from Akeyless via PowerShell script

# Usage

The following example demonstrates fetching **dynamic secret**:

```powershell Get-Dynamic-Secret
$AuthBody = @{
    "access-id" = "<Access Id>"
    "access-key" = "<Access Key>"
    "access-type" = "access_key"
}
$AuthParameters = @{
    Method = "POST"
    Uri =  "https://api.akeyless.io/auth"
    Body = ($AuthBody | ConvertTo-Json) 
    ContentType = "application/json"
}
$token = (Invoke-RestMethod @AuthParameters).token
Write-Host "NEW TOKEN: [$token]"
$SecretBody = @{
    "name" = "/Full/Path/To/Secret"
    "token" = "$token"
}
$SecretParameters = @{
    Method = "POST"
    Uri =  "https://api.akeyless.io/get-dynamic-secret-value"
    Body = ($SecretBody | ConvertTo-Json) 
    ContentType = "application/json"
}
Invoke-RestMethod @SecretParameters
```

Make sure to set your `Access Id` and `Access Key` in the relevant places. The received token should be provided for every request that requires authentication. 

The following example demonstrates fetching **static secret**:

```powershell Get-Static-Secret
$AuthBody = @{
    "access-id" = "<Access Id>"
    "access-key" = "<Access Key>"
    "access-type" = "access_key"
}
$AuthParameters = @{
    Method = "POST"
    Uri =  "https://api.akeyless.io/auth"
    Body = ($AuthBody | ConvertTo-Json) 
    ContentType = "application/json"
}
$token = (Invoke-RestMethod @AuthParameters).token
Write-Host "NEW TOKEN: [$token]"
$SecretBody = @{
    "names" = @("mySecret")
    "token" = "$token"
}
$SecretParameters = @{
    Method = "POST"
    Uri =  "https://api.akeyless.io/get-secret-value"
    Body = ($SecretBody | ConvertTo-Json) 
    ContentType = "application/json"
}
Invoke-RestMethod @SecretParameters
```

Make sure to set your `Access Id` and `Access Key` in the relevant places. The received token should be provided for every request that requires authentication.