---
title: Chef InSpec Plugin
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
Chef InSpec is an open-source framework for testing and auditing your applications and infrastructure. Chef InSpec works by comparing the actual state of your system with the desired state that you express in easy-to-read and easy-to-write Chef InSpec code. Chef InSpec detects violations and displays findings in the form of a report, but puts you in control of remediation.

# Prerequsites

An [SSH Cert Issuer](https://docs.akeyless.io/docs/how-to-configure-ssh)

# Chef InSpec Plugin Configuration

1. Issue an SSH Certificate from Akelyess:

```shell
akeyless get-ssh-certificate -s <target_username> -c ssh-cert-issuer-name -p <path_to_public_ssh_key> && echo
```

2. Test SSH connection

```shell
ssh <target_username>@<target_ssh_server>
```

3. Setup `ssh-agent` and add SSH key public key to the agent:

```shell
eval `ssh-agent`
ssh-add <path_to_public_ssh_key>
```

4. Test Chef InSpec

```ruby
inspec shell -c 'package("git").installed?' -t <target_username>@<target_ssh_server>
inspec shell -c 'package("git").version' -t <target_username>@<target_ssh_server>
```

# Example

```ruby
# sign public ssh key by Akeyless to get ssh certificate
akeyless get-ssh-certificate -s ubuntu -c ssh-cert-issuer-demo -p ~/.ssh/id_rsa.pub --profile inspec && echo
# Test ssh connection
ssh ubuntu@172.17.0.2
# Setup ssh-agent and add ssh key + certificate to it
eval `ssh-agent`
ssh-add ~/.ssh/id_rsa
# Test chef inspec
inspec shell -c 'package("git").installed?' -t ssh://ubuntu@172.17.0.1
inspec shell -c 'package("git").version' -t ssh://ubuntu@172.17.0.1
```

<Embed url="https://drive.google.com/file/d/1eb_tzY-0MoY3UpHkO41fbKpXQzZ2dcXb/view?usp=sharing" title="AKEYLESS Vault CHEF InSpec integration.mp4" favicon="https://ssl.gstatic.com/docs/doclist/images/icon_14_video_favicon.ico" image="https://lh3.googleusercontent.com/Liw_VVJyvAVd1vSLBcx-cCggDocmAgn5GwOlAHWyX8ikA3npWB7mkvHMxBcTaxw=w1200-h630-p" provider="drive.google.com" href="https://drive.google.com/file/d/1eb_tzY-0MoY3UpHkO41fbKpXQzZ2dcXb/view?usp=sharing" iframe="false" />
