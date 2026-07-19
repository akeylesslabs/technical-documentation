---
title: test
deprecated: false
hidden: false
metadata:
  robots: index
---
# Akeyless Secure Remote Access (SRA) — Beginner Quick Start (Docker Compose)

This guide is written for someone who has **never touched Akeyless before**. Follow it top to bottom,
in order, without skipping the validation steps. By the end, you will have:

- An Akeyless Gateway + SRA running locally via Docker Compose
- A real SSH server registered as a protected target
- An actual SSH session proven to work **through** SRA (not just "containers are running")

This is a **test/demo setup** — not hardened for production. See [What's next](#whats-next) at the bottom
for the production path.

***

## 1. How the pieces fit together (read this first)

```
 You (SSH client / browser)
        │
        ▼
 ┌─────────────────────────────┐        outbound HTTPS/AMQPS/TLS only
 │   Docker host (your laptop) │ ─────────────────────────────────────►  Akeyless SaaS
 │  ┌────────────┐ ┌─────────┐ │                                        (console, auth,
 │  │  Gateway   │ │  SRA    │ │                                         vault, key mgmt)
 │  │ (auth,     │ │ Web +   │ │
 │  │  policy)   │ │ SSH     │ │
 │  └────────────┘ └────┬────┘ │
 │                       │      │
 └───────────────────────┼──────┘
                          ▼
                  Target SSH server
                  (the machine you actually
                   want to access)
```

Plain-English definitions — you'll need these words for every step below:

| Term                           | What it actually means                                                                                                                  |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Akeyless account / console** | Your login at `console.akeyless.io`. This is the control plane — it stores policy, not your servers' credentials.                       |
| **Gateway**                    | A container you run yourself (on your laptop, in this guide) that talks to Akeyless SaaS and enforces access. Nothing works without it. |
| **Auth Method**                | _How_ something proves its identity to Akeyless (here: an API Key). The Gateway uses one to authenticate itself.                        |
| **Access Role**                | _What_ an authenticated identity is allowed to do (read/list on which paths). You attach an Auth Method to a Role.                      |
| **SSH Certificate Issuer**     | Issues short-lived SSH certificates instead of handing out long-lived SSH keys/passwords. This is the core of SRA's SSH access.         |
| **SRA (Secure Remote Access)** | The proxy layer (Web + SSH containers) that sits between you and a target server, so you never get the target's real credentials.       |
| **Target**                     | The record in Akeyless describing the actual server you want to reach (its host, port, and how to authenticate to it).                  |

***

## 2. Prerequisites checklist

Tick every box **before** starting Step 3. Most guide failures trace back to one of these being skipped.

- [ ] An Akeyless account [Creating an Akeyless Account Quickstart](doc:account-quickstart)&#x20;
- [ ] Docker Engine **20.10+** and Docker Compose **v1.29+** installed (`docker --version`, `docker compose version`)
- [ ] Docker daemon actually running (`docker ps` doesn't error out)
- [ ] At least **1 vCPU / 2 GiB RAM free** per component (Gateway + SRA Web + SRA SSH ≈ 3–4 vCPU / 6–8 GiB total to be safe)
- [ ] Local ports **8000, 8080, 8889, 2222, 9900** are free on your machine (nothing else listening on them)
- [ ] A real Linux server you can already SSH into with a username/password or key — this is your **test target**. It can be a spare VM, a cloud instance, or a container; it just needs sshd running and a routable IP from your Docker host. Don't skip this — without a real target you cannot prove SRA works, only that containers started.
- [ ] Outbound internet access from your Docker host with **no corporate proxy/VPN blocking non-standard ports** (checked automatically in Step 3)

***

## 3. Step 0 — Validate network reachability (do this before anything else)

Akeyless Gateway is a hybrid component: it runs on your machine but must continuously reach Akeyless SaaS
over the internet. If your firewall, VPN, or corporate proxy blocks any of the hosts below, the Gateway
will start, look "up" in `docker ps`, and still silently fail to register — which is confusing and wastes
hours. Run this check now, from the **same machine/network** where you'll run Docker Compose.

Save this as `check-akeyless-network.sh` and run `bash check-akeyless-network.sh`:

```bash
#!/usr/bin/env bash
# Validates outbound connectivity to every host Akeyless Gateway/SRA needs.
# For EU tenants, replace ".akeyless.io" with ".eu.akeyless.io" in the HTTPS_HOSTS list.

set -u
FAIL=0

check_tcp() {
  local host="$1" port="$2"
  if timeout 5 bash -c "cat < /dev/null > /dev/tcp/${host}/${port}" 2>/dev/null; then
    printf "  OK    %-45s %s\n" "$host" "$port"
  else
    printf "  FAIL  %-45s %s\n" "$host" "$port"
    FAIL=1
  fi
}

echo "== HTTPS (443) — core SaaS services =="
for h in console.akeyless.io vault.akeyless.io vault-ro.akeyless.io \
         auth.akeyless.io auth-ro.akeyless.io auth-cert.akeyless.io \
         audit.akeyless.io audit-ro.akeyless.io bis.akeyless.io bis-ro.akeyless.io \
         gator.akeyless.io gator-ro.akeyless.io \
         kfm1.akeyless.io kfm1-ro.akeyless.io kfm2.akeyless.io kfm2-ro.akeyless.io \
         kfm3.akeyless.io kfm3-ro.akeyless.io kfm4.akeyless.io kfm4-ro.akeyless.io \
         rest.akeyless.io api.akeyless.io hvp.akeyless.io \
         akeyless-cli.s3.us-east-2.amazonaws.com akeylessservices.s3.us-east-2.amazonaws.com \
         artifacts.site2.akeyless.io; do
  check_tcp "$h" 443
done

echo "== AMQPS (5671) — message queue =="
check_tcp mq.akeyless.io 5671

echo "== TLS (9443) — log shipping =="
check_tcp log.akeyless.io 9443

echo
echo "== Local ports that must be FREE on this Docker host =="
for p in 8000 8080 8889 2222 9900; do
  if lsof -i ":$p" -sTCP:LISTEN >/dev/null 2>&1; then
    printf "  IN USE  port %s — something else is already listening, stop it or you'll get container start errors\n" "$p"
    FAIL=1
  else
    printf "  FREE    port %s\n" "$p"
  fi
done

echo
if [ "$FAIL" -eq 0 ]; then
  echo "All checks passed. Safe to continue to Step 1."
else
  echo "One or more checks FAILED. Fix firewall/proxy/VPN rules or free the port(s) above before continuing —"
  echo "the Gateway will not register correctly otherwise."
fi
```

**If anything fails here:** talk to whoever controls your firewall/VPN before continuing — no step later
in this guide can work around blocked connectivity to Akeyless SaaS.

***

## 4. Step 1 — Log into your Akeyless account

Go to [console.akeyless.io](https://console.akeyless.io) and log in (or create a free account). You don't
need to click anything else yet — you just need working credentials for the CLI in the next step.

***

## 5. Step 2 — Install and configure the Akeyless CLI

The CLI is how you'll create the identities and permissions the Gateway needs.

**macOS:**

```bash
brew tap akeylesslabs/tap
brew trust akeylesslabs/tap
brew install akeyless
```

**Linux (Debian/Ubuntu):**

```bash
apt-get update && apt-get install -y curl gnupg
curl -fsSL https://akeyless.jfrog.io/artifactory/api/security/keypair/akeyless_cli_repo/public | gpg --dearmor -o /usr/share/keyrings/akeyless.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/akeyless.gpg] https://akeyless.jfrog.io/artifactory/akeyless-cli-debian stable main" | tee /etc/apt/sources.list.d/akeyless.list
apt-get update && apt-get install -y akeyless
```

Verify it's installed:

```bash
akeyless --version
```

Configure it with your console login (first run walks you through creating a personal Auth Method — accept the defaults):

```bash
akeyless
```

Sanity-check that the CLI can really talk to Akeyless:

```bash
akeyless create-secret --name /sra-quickstart/hello --value world
akeyless get-secret-value --name /sra-quickstart/hello
```

If that prints `world`, your CLI is correctly authenticated. If it errors, stop and re-run Step 0 —
it's almost always network connectivity, not the CLI.

***

## 6. Step 3 — Create the identity the Gateway will use

The Gateway container needs its _own_ Auth Method (don't reuse your personal login) and a Role that
scopes what it's allowed to do.

```bash
# 1. An identity for the Gateway itself
akeyless auth-method create api-key --name /sra-quickstart/gateway-auth

# 2. A role, scoped only to what the Gateway needs for this test
akeyless create-role --name /sra-quickstart/gateway-role
akeyless set-role-rule --role-name /sra-quickstart/gateway-role --path "/sra-quickstart/*" --capability read --capability list

# 3. Attach the role to the auth method
akeyless assoc-role-am --role-name /sra-quickstart/gateway-role --am-name /sra-quickstart/gateway-auth
```

Get the credentials — **save these two values**, you'll paste them into `gateway.env` in Step 5:

```bash
akeyless auth-method-get --name /sra-quickstart/gateway-auth
```

This prints an **Access ID** (starts with `p-...`) and, since it's an API-Key method, you were also
shown an **Access Key** at creation time — if you lost it, delete and recreate the auth method.

***

## 7. Step 4 — Create the SSH Certificate Issuer

This is what lets SRA issue short-lived SSH certificates instead of handing out real SSH passwords/keys.

```bash
# The signing key backing the issuer
akeyless create-dfc-key --name /sra-quickstart/ssh-signer-key --alg RSA2048

# The issuer itself — "allowed-users" must match a real login user on your test target
akeyless create-ssh-cert-issuer \
  --name /sra-quickstart/ssh-issuer \
  --signer-key-name /sra-quickstart/ssh-signer-key \
  --allowed-users '<the-ssh-username-on-your-test-target>' \
  --ttl 300
```

Export the issuer's public CA key — you'll paste this into `docker-compose.yaml` in Step 5 so your test
target can trust certificates Akeyless issues:

```bash
akeyless get-rsa-public --name /sra-quickstart/ssh-signer-key --json --jq-expression='.ssh' > ca.pub
cat ca.pub
```

**On your test target server**, tell sshd to trust this CA (do this now, over your existing SSH access —
this is the one manual step SRA cannot do for you):

```bash
# copy ca.pub to the target, e.g. /etc/ssh/ca.pub, then on the target:
echo "TrustedUserCAKeys /etc/ssh/ca.pub" | sudo tee -a /etc/ssh/sshd_config
sudo systemctl restart sshd
```

***

## 8. Step 5 — Get and configure the Docker Compose files

```bash
git clone https://github.com/akeylesslabs/docker-compose.git akeyless-sra
cd akeyless-sra
```

Edit `gateway.env`:

```bash
CLUSTER_NAME=sra-quickstart
UNIFIED_GATEWAY=true
GATEWAY_ACCESS_ID=<Access ID from Step 3>
GATEWAY_ACCESS_TYPE=access_key
GATEWAY_ACCESS_KEY=<Access Key from Step 3>
ALLOWED_ACCESS_PERMISSIONS=<your akeyless console username/email>
```

Edit `sra.env`:

```bash
UNIFIED_GATEWAY=true
```

Edit `cache.env` (Redis password — make one up, it's local only):

```bash
REDIS_PASS=<a-strong-random-password>
```

In `docker-compose.yaml`, mount the `ca.pub` file you created in Step 4 into the SRA SSH container:

```yaml
volumes:
  - ./ca.pub:/var/akeyless/creds/ca.pub
```

***

## 9. Step 6 — Start it

```bash
docker compose --profile gateway --profile sra up -d
```

Confirm all four containers are up and **not restarting**:

```bash
docker ps
```

You should see, all with status `Up` (not `Restarting`):

- `akeyless-gateway`
- `akeyless-sra-web`
- `akeyless-sra-ssh`
- `akeyless-cache`

If any container is stuck restarting, jump to [Troubleshooting](#troubleshooting) before continuing —
do not proceed to Step 7 with an unhealthy container.

***

## 10. Step 7 — Confirm the Gateway registered with Akeyless

Open in your browser:

```
http://<your-docker-host-ip>:8000/console
```

You should see the Gateway console load (not a connection error/timeout). Then check in the **Akeyless
SaaS console** (console.akeyless.io) under Gateways — your `sra-quickstart` cluster should appear as
**Active**, not "Not connected." If it doesn't show as active within \~1 minute, this is a network problem
— re-run the Step 0 script from inside the Docker host itself.

***

## 11. Step 8 — Register your test target

This tells Akeyless which real server SRA is protecting.

```bash
akeyless target create ssh \
  --name /sra-quickstart/test-target \
  --host <IP or hostname of your test target> \
  --port 22 \
  --ssh-username <the-ssh-username-on-your-test-target>
```

***

## 12. Step 9 — Prove it actually works (end-to-end test)

This is the step that separates "containers are running" from "SRA actually works." Do not skip it.

```bash
akeyless connect \
  -t "<the-ssh-username-on-your-test-target>@<IP or hostname of your test target>:22" \
  -n /sra-quickstart/ssh-issuer \
  -g <your-docker-host-ip>:9900
```

If you land in a real shell prompt on your test target, **SRA is working end-to-end** — you connected
through the Gateway/SRA proxy using a short-lived certificate, never touching the target's real
credentials directly.

Alternative (no CLI needed): open `http://<your-docker-host-ip>:8000/sra/portal` in a browser, log in
with your Akeyless console credentials, select the test target, and open a session from there.

***

## 13. Troubleshooting

| Symptom                                                        | Likely cause                                                                                                   | Fix                                                                                                       |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Step 0 script reports `FAIL` on any `.akeyless.io` host        | Corporate firewall/VPN/proxy blocking outbound traffic                                                         | Get that host:port allow-listed; nothing later will work until this passes                                |
| Container restarts in a loop                                   | Missing/misspelled env var in `gateway.env` or `sra.env`                                                       | `docker compose logs akeyless-gateway` — it names the missing variable                                    |
| Gateway console loads but SaaS console shows "Not connected"   | `GATEWAY_ACCESS_ID`/`GATEWAY_ACCESS_KEY` wrong, or MQ (mq.akeyless.io:5671) blocked                            | Recheck credentials pasted from Step 3; re-run Step 0 network check                                       |
| `akeyless connect` fails with a certificate/trust error        | `ca.pub` on the target doesn't match the signer key, or sshd wasn't restarted after adding `TrustedUserCAKeys` | Re-export `ca.pub` (Step 4) and confirm it's byte-for-byte what's on the target; confirm `sshd` restarted |
| `akeyless connect` fails with "permission denied" for the user | The username isn't in `--allowed-users` on the SSH Certificate Issuer                                          | Recreate the issuer with the correct `--allowed-users`, or add the user                                   |
| Ports already in use when starting Compose                     | Something else on 8000/8080/8889/2222/9900                                                                     | Stop the conflicting process, or remap ports in `docker-compose.yaml`                                     |
| Everything works but stops after \~5 minutes                   | SSH cert TTL (`--ttl 300` = 5 minutes) expired mid-session for a _new_ connection attempt                      | Expected behavior — increase `--ttl` on the issuer if you want longer-lived certs for testing             |

***

## What's next

This setup is **not TLS-secured and not meant for production** — Docker Compose SRA also only supports a
subset of the configuration options available on Kubernetes. Once this works and you understand the
moving parts, move to:

- **Kubernetes (Helm) production deployment** — for TLS, scaling, and advanced SRA features (web app isolation, etc.)
- **SSO/SAML instead of local users** — replace the single test user with your real identity provider
- **Session recording & audit** — enabled per-target in the Akeyless console once you're past the demo stage

<br />
