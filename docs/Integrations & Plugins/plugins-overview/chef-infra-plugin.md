---
title: Chef Infra Plugin
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
# Prerequisites

* Chef Workstation installed. Refer to [this](https://docs.chef.io/workstation/install_workstation/) guide to install the workstation.

> 👍 Note
>
> Akeyless developed API compatibility with Hashicorp Vault OSS, enabling the use of Vault OSS community plugins for both Static & Dynamic Secrets, you can find more information [here](https://docs.akeyless.io/docs/hashicorp-vault-proxy)

# Chef Infra Plugin Configuration

1. Download the following Chef Infra cookbook from [here](https://github.com/exospheredata/secrets_management)

2. Add the following recipe to your cookbook:

```ruby
#
# Cookbook:: secrets_management_test
# Recipe:: akeyless-vault
#

vault_hash = {}
vault_hash[:token] = data_bag_item('vault-test', 'config')['token']
vault_hash[:address] = data_bag_item('vault-test', 'config')['addr']
vault = Vault::Client.new(vault_hash)
secret_name = 'chef/test_secret_1'
bag = open_secret_item('/secret/data/', secret_name, vault: vault_hash)
secret_value = bag['data'][secret_name.to_sym]

file '/tmp/hello_from_akeyless' do
  content "Secret is: #{secret_value}\n"
end
```

3. Upload the cookbook to your Chef Infra Server
4. Create the following Data Bag:

```json
{
  "id": "config",
  "addr": "https://hvp.akeyless.io",
  "token": "<access-id>..<access-key>",
  "chef-approle": "base"
}
```

5. Test by running Chef Infra Client:

```shell
$ sudo chef-client
Starting Chef Infra Client, version 17.0.242
[2020-05-17T10:45:36+03:00] INFO: *** Chef Infra Client 17.0.242 ***
[2020-05-17T10:45:36+03:00] INFO: Platform: x86_64-darwin17
[2020-05-17T10:45:36+03:00] INFO: Chef-client pid: 19289
[2020-05-17T10:45:42+03:00] INFO: Run List is [role[base]]
[2020-05-17T10:45:42+03:00] INFO: Run List expands to [secrets_management_test]
[2020-05-17T10:45:42+03:00] INFO: Starting Chef Infra Client Run for Test
[2020-05-17T10:45:42+03:00] INFO: Running start handlers
[2020-05-17T10:45:42+03:00] INFO: Start handlers complete.
resolving cookbooks for run list: ["secrets_management_test"]
[2020-05-17T10:45:43+03:00] INFO: Loading cookbooks [secrets_management_test@0.4.5, secrets_management@1.0.0, chef-vault@3.0.0, compat_resource@12.19.0]
Synchronizing Cookbooks:
  - secrets_management_test (0.4.5)
  - secrets_management (1.0.0)
  - chef-vault (3.0.0)
  - compat_resource (12.19.0)
Installing Cookbook Gems:
[2020-05-17T10:45:54+03:00] INFO: Dont run Bundler as root. Bundler can ask for sudo if it is needed, and
installing your bundle as root will break this application for all non-root
users on this machine.
Fetching gem metadata from https://www.rubygems.org/...........
Fetching gem metadata from https://www.rubygems.org/.
Resolving dependencies...
Using aws-eventstream 1.1.0
Using aws-sigv4 1.1.3
Using bundler 1.17.2
Using chef-vault 4.0.1
Using vault 0.13.2
Bundle complete! 2 Gemfile dependencies, 5 gems now installed.
Use `bundle info [gemname]` to see where a bundled gem is installed.
Compiling Cookbooks...
Converging 1 resources
Recipe: secrets_management_test::akeyless-vault
  * file[/tmp/hello_from_akeyless] action create[2020-05-17T10:45:56+03:00] INFO: Processing file[/tmp/hello_from_akeyless] action create (secrets_management_test::akeyless-vault line 16)
[2020-05-17T10:45:56+03:00] INFO: file[/tmp/hello_from_akeyless] created file /tmp/hello_from_akeyless
    - create new file /tmp/hello_from_akeyless[2020-05-17T10:45:56+03:00] INFO: file[/tmp/hello_from_akeyless] updated file contents /tmp/hello_from_akeyless
    - update content in file /tmp/hello_from_akeyless from none to 6236c1
    --- /tmp/hello_from_akeyless	2020-05-17 10:45:56.287670044 +0300
    +++ /tmp/.chef-hello_from_akeyless20200517-19289-i3qenl	2020-05-17 10:45:56.287419909 +0300
    @@ -1 +1,2 @@
    +Secret is: [my chef secret value!]
[2020-05-17T10:45:56+03:00] INFO: Chef Infra Client Run complete in 13.45992 seconds
Running handlers:
[2020-05-17T10:45:56+03:00] INFO: Running report handlers
Running handlers complete
[2020-05-17T10:45:56+03:00] INFO: Report handlers complete
Chef Infra Client finished, 1/1 resources updated in 20 seconds
$ cat /tmp/hello_from_akeyless
Secret is: my chef secret value!
```

> 📘 Info
>
> [Chef Plugin GitHub Repository](https://github.com/exospheredata/secrets_management)
