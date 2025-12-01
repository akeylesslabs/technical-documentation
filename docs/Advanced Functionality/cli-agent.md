---
title: CLI Agent
deprecated: false
hidden: true
metadata:
  robots: index
---
The Akeyless [CLI](https://docs.akeyless.io/docs/cli#/) lets you set up an Agent that automatically delivers secrets from your Akeyless account and places them in specific locations on your system (**Linux** or **Windows** operating systems are supported).

The minimum required configuration is:

* **Authentication Method:** To authenticate to your account.
* **Secrets:** The secrets that will be fetched to your local environment

The above are defined in a single `agent.toml` file. Once it's set, the Agent handles authentication on its own, so you don’t need to manually authenticate for the agent to deliver the secrets.

The supported items that can be fetched using the Agent are:

* [Static Secrets](https://docs.akeyless.io/docs/static-secrets#/)
* [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets#/)
* [SSH Certificates](https://docs.akeyless.io/docs/ssh-certificates#/)
* [PKI Certificates](https://docs.akeyless.io/docs/certificate-lifecycle-management#/)

> 📘 CLI Version
>
> The CLI Agent is available starting from version `1.134.0`

# Agent Configuration

In order to work with the Agent, configure the following `/Users/<username>/.akeyless/profiles/agent.toml` file:

```toml agent.toml
access_type = "<AccessType>"
access_id = "AccessID"
access_key = "AccessKey"
k8s_auth_config_name = ""

gateway_url = "http://localhost:8080"

log_file_path = "path_to/agent.log"     
log_format = "text"                     
log_level = "debug"                     
log_file_max_size_mb = 10               

render_interval = "15m"                 
allow_missing_keys_in_template = true   

[[template]] 
source = "path_to/static.tmpl"
destination = "path_to/static.txt"

[[template]] 
source = "path_to/rotated.tmpl"
destination = "path_to/rotated.txt"

[[template]] 
source = "path_to/ssh_cert.tmpl"
destination = "path_to/ssh_cert.txt"

[[template]] 
source = "path_to/pki_cert_with_key.tmpl"
destination = "path_to/pki_cert_with_key.txt"

[[template]] 
source = "path_to/pki_cert_with_csr.tmpl"
destination = "path_to/pki_cert_with_csr.txt"
```

Where:

* `access_type`: The **Access Type** of the auth method that is being used to authenticate.

* `access_id`: The **Access ID** of the auth method that is being used to authenticate.

* `access_key`: The **Access Key** of the auth method that is being used to authenticate.

* `log_file_path`: The path to the `agent.log` file, defaults are:

  * `"/var/log/akeyless"` for Linux.

  * `"programdata/akeyless"` for Windows.

* `log_format`: Can be `text` or `json`.

* `log_level`: The log level, by default set to `debug`, can be set to `info/warn/error`.

* `log_file_max_size_mb`: The maximum size of a log file in `megabytes`, by default set to `10`.

* `render_interval`: The interval for provisioning the secrets, by default set to `15m`, the minimum is `1s`.

* `allow_missing_keys_in_template`: If one secret (or more) fails to be provisioned, continue with provision the rest, by default set to `true`.

# Template Examples

This section describe how to fetch each item.

**Static Secret**:

```shell static.tmpl
{{ with secret "/my_secret" }}Value: {{ .Data.Value }}{{ end -}}
```

**Rotated Secret**:

```shell rotated.tmpl
{{- with rotatedSecret "/my_rotator" -}}
username={{ .Data.Username }}
password={{ .Data.Password }}
{{- end -}}
```

**SSH Certificate**:

```shell ssh_cert.tmpl
{{- with sshCertificate "/certificates/ssh_cert_issuer" "ubuntu" "--pub-key-file-path=path_to/ssh_key.pub"-}}
{{ .Data }}
{{- end -}}
```

**PKI Certificate using a Public Key**:

```shell pki_cert_with_key.tmpl
{{- with pkiCertificate "/certificate/pki_cert_issuer" "--key-file-path=path_to/rsa_key.pub" "--ttl=3600" -}}
{{ .Data }}
{{- end -}}
```

**PKI Certificate using a CSR**:

```shell pki_cert_with_csr.tmpl
{{- with pkiCertificate "/certificate/pki_cert_issuer" "--csr-file-path=path_to/test.csr" "--ttl=3600" -}}
{{ .Data }}
{{- end -}}
```

# Start the Agent

In order to start the Agent to provision the secrets you have defined in the `agent.toml` file, run the following command:

```shell
akeyless agent start
```

The command above will start the agent.

You can find the complete list of parameters for this command in the [CLI Reference - CLI Agent](https://docs.akeyless.io/docs/cli-reference-agent#/) section.
