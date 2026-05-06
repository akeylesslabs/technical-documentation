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
Chef InSpec is an open-source framework for testing and auditing your applications and infrastructure. Chef InSpec works by comparing the actual state of your system against the desired state you express in easy-to-read, easy-to-write Chef InSpec code. Chef InSpec detects violations and displays findings in a report, but puts you in control of remediation.

## Prerequisites

An [SSH Cert Issuer](https://docs.akeyless.io/docs/sra-ssh-certificates)

## Chef InSpec Plugin Configuration

1. Issue an SSH Certificate from Akeyless:

   ```shell
   akeyless get-ssh-certificate -s <target_username> -c ssh-cert-issuer-name -p <path_to_public_ssh_key> && echo
   ```

2. Test SSH connection

   ```shell
   ssh <target_username>@<target_ssh_server>
   ```

3. Set up `ssh-agent` and add the SSH key public key to the agent:

   ```shell
   eval `ssh-agent`
   ssh-add <path_to_public_ssh_key>
   ```

4. Test Chef InSpec

   ```ruby
   inspec shell -c 'package("git").installed?' -t <target_username>@<target_ssh_server>
   inspec shell -c 'package("git").version' -t <target_username>@<target_ssh_server>
   ```

## Example

<!-- secret-stdout-scan:ok -->
```ruby
# Sign public ssh key by Akeyless to get ssh certificate
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

<video controls preload="metadata" width="100%">
  <source src="https://raw.githubusercontent.com/akeylesslabs/technical-documentation/v1.0/media/chef-inspec-integration.mp4" type="video/mp4" />
  Your browser does not support the video tag. Use this direct link: https://raw.githubusercontent.com/akeylesslabs/technical-documentation/v1.0/media/chef-inspec-integration.mp4
</video>
