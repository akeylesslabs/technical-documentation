---
title: Quick Start
deprecated: false
hidden: false
metadata:
  robots: index
---
This guide deploys Akeyless Gateway + SRA on **Amazon EKS**. Authentication uses **AWS IAM (IRSA)**, which is the native EKS way to give the Gateway an identity.

By the end you will have:

- A Gateway + SRA running as pods in your EKS cluster, authenticated via IRSA
- A real SSH server registered as a protected target
- An actual SSH session proven to work **through** SRA (not just "pods are Running")

***

## 1. How the pieces fit together

Definitions you'll need:

| Term                       | What it actually means                                                                                                                                                                                                            |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Unified Gateway**        | The current Akeyless chart (`akeyless-gateway`) that runs Gateway + SRA together in one deployment. The **legacy** model deployed Gateway and SRA as separate charts/products — don't use that path for new setups.               |
| **IRSA**                   | _IAM Roles for Service Accounts_ — EKS's native way to hand a pod real AWS credentials without storing any secret. The pod's ServiceAccount is annotated with an IAM role ARN; AWS injects short-lived credentials automatically. |
| **AWS IAM auth method**    | Akeyless's identity check that trusts "this caller can prove it holds a specific AWS IAM role/account" — no static Access Key to leak or rotate.                                                                                  |
| **Access Role**            | What an authenticated identity is allowed to do in Akeyless (read/list on which paths).                                                                                                                                           |
| **SSH Certificate Issuer** | Issues short-lived SSH certificates instead of handing out long-lived SSH keys/passwords.                                                                                                                                         |
| **Target**                 | The Akeyless record describing the real server SRA protects (host, port, allowed users).                                                                                                                                          |

***

## 2. Prerequisites checklist

- [ ] An Akeyless account ([Creating an Akeyless Account Quickstart](doc:account-quickstart))
- [ ] An **existing EKS cluster**, and `kubectl` context pointed at it.
- [ ] `aws` CLI configured with an identity that can create IAM roles and manage the cluster
- [ ] `helm` v3 installed locally
- [ ] **IAM OIDC provider enabled** on the cluster (required for IRSA):
  ```bash
  eksctl utils associate-iam-oidc-provider --cluster <your-cluster-name> --approve
  ```
- [ ] **AWS Load Balancer Controller** installed in the cluster (needed to provision the NLBs in Step 7) —
  if you're not sure, run `kubectl get deployment -n kube-system aws-load-balancer-controller`; if
  that errors, install it before continuing (Akeyless services will stay `Pending` otherwise)
- [ ] At least one node group with capacity for \~**3 vCPU / 6 GiB RAM free** across the cluster (Gateway + SRA Web + SRA SSH, 1 replica each, minimum sizing)
- [ ] Worker nodes run in a subnet with **outbound internet egress** — a NAT Gateway (private subnets) or an Internet Gateway (public subnets). No egress path = the Gateway can start and never register.
- [ ] A real Linux server you can already SSH into (username/password or key) that's reachable from inside the VPC — this is your **test target**. Without a real target you can only prove pods started, not that SRA works.

***

## 3. Step 0 — Validate network reachability from _inside the cluster_

This is the step people skip and regret. Checking connectivity from your laptop tells you nothing about
whether the **worker nodes'** security groups, NACLs, or NAT Gateway actually allow the traffic the
Gateway needs — that's a different network path entirely. Validate from a pod running in the same
subnets the Gateway will use.

```bash
kubectl run netcheck --rm -it --restart=Never --image=busybox:1.36 -- sh
```

Once inside the pod's shell, paste this (busybox `nc` is used instead of bash's `/dev/tcp` since this image has no bash):

```sh
FAIL=0
check() { nc -z -w5 "$1" "$2" && echo "OK   $1:$2" || { echo "FAIL $1:$2"; FAIL=1; }; }

echo "== HTTPS (443) =="
for h in console.akeyless.io vault.akeyless.io vault-ro.akeyless.io \
         auth.akeyless.io auth-ro.akeyless.io auth-cert.akeyless.io \
         audit.akeyless.io audit-ro.akeyless.io bis.akeyless.io bis-ro.akeyless.io \
         gator.akeyless.io gator-ro.akeyless.io \
         kfm1.akeyless.io kfm1-ro.akeyless.io kfm2.akeyless.io kfm2-ro.akeyless.io \
         kfm3.akeyless.io kfm3-ro.akeyless.io kfm4.akeyless.io kfm4-ro.akeyless.io \
         rest.akeyless.io api.akeyless.io hvp.akeyless.io \
         akeyless-cli.s3.us-east-2.amazonaws.com akeylessservices.s3.us-east-2.amazonaws.com \
         artifacts.site2.akeyless.io; do check "$h" 443; done

echo "== AMQPS (5671) =="
check mq.akeyless.io 5671

echo "== TLS (9443) log shipping =="
check log.akeyless.io 9443

echo "== Your test SSH target =="
check "<test-target-ip-or-hostname>" 22

[ "$FAIL" -eq 0 ] && echo "ALL PASS — safe to continue" || echo "FIX THE ABOVE before continuing (security group / NACL / NAT Gateway egress)"
```

(Replace `<test-target-ip-or-hostname>` with your real test target — this confirms pod-to-target routing
too, which matters if the target lives in a different VPC/subnet.)

`exit` the pod when done — `--rm` cleans it up automatically.

**If anything fails:** check, in this order — (1) does the subnet have a NAT Gateway/Internet Gateway
route, (2) does the worker node security group allow the egress port, (3) does any NACL on the subnet
block it. Do not continue until this passes.

***

## 4. Step 1 — Create the identity the Gateway will use (AWS IAM, not API key)

```bash
akeyless auth-method create aws-iam \
  --name /sra-quickstart/gateway-auth \
  --bound-aws-account-id <your-AWS-account-id>
```

No AWS-side IAM permissions are required for this — Akeyless only needs the caller to be able to call
`sts:GetCallerIdentity`, which every AWS identity can do by default.

```bash
akeyless create-role --name /sra-quickstart/gateway-role
akeyless set-role-rule --role-name /sra-quickstart/gateway-role --path "/sra-quickstart/*" --capability read --capability list
akeyless assoc-role-am --role-name /sra-quickstart/gateway-role --am-name /sra-quickstart/gateway-auth
```

***

## 5. Step 2 — Create the IAM role for IRSA

This role has **no AWS permissions attached** — its only job is to prove the pod's identity to Akeyless.

```bash
export CLUSTER_NAME=<your-cluster-name>
export ACCOUNT_ID=<your-AWS-account-id>
export OIDC_PROVIDER=$(aws eks describe-cluster --name "$CLUSTER_NAME" \
  --query "cluster.identity.oidc.issuer" --output text | sed 's|https://||')

cat > trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Federated": "arn:aws:iam::${ACCOUNT_ID}:oidc-provider/${OIDC_PROVIDER}" },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "${OIDC_PROVIDER}:sub": "system:serviceaccount:akeyless:akeyless-gateway",
        "${OIDC_PROVIDER}:aud": "sts.amazonaws.com"
      }
    }
  }]
}
EOF

aws iam create-role \
  --role-name akeyless-gateway-irsa \
  --assume-role-policy-document file://trust-policy.json
```

Note the role ARN it prints — you'll need it in the values file below. The namespace/service-account
name in the trust policy (`akeyless:akeyless-gateway`) must match exactly what you set in Helm in Step 4.

***

## 6. Step 3 — Create the SSH Certificate Issuer

```bash
akeyless create-dfc-key --name /sra-quickstart/ssh-signer-key --alg RSA2048

akeyless create-ssh-cert-issuer \
  --name /sra-quickstart/ssh-issuer \
  --signer-key-name /sra-quickstart/ssh-signer-key \
  --allowed-users '<the-ssh-username-on-your-test-target>' \
  --ttl 300

akeyless get-rsa-public --name /sra-quickstart/ssh-signer-key --json --jq-expression='.ssh' > ca.pub
cat ca.pub
```

On your test target (over your existing SSH access — this is the one manual step SRA can't do for you):

```bash
# copy ca.pub to the target as /etc/ssh/ca.pub, then on the target:
echo "TrustedUserCAKeys /etc/ssh/ca.pub" | sudo tee -a /etc/ssh/sshd_config
sudo systemctl restart sshd
```

***

## 7. Step 4 — Add the Helm repo and write `values.yaml`

```bash
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
kubectl create namespace akeyless
```

`values.yaml`:

```yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID from Step 4's aws-iam auth method>
    gatewayAccessType: aws_iam

serviceAccount:
  create: true
  serviceAccountName: akeyless-gateway
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::<your-AWS-account-id>:role/akeyless-gateway-irsa

replicaCount: 1
resources:
  requests:
    cpu: "1"
    memory: 2Gi

service:
  type: LoadBalancer
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-internal: "true"   # keep the console off the public internet
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"

sra:
  enabled: true
  sshConfig:
    replicaCount: 1
    resources:
      requests:
        cpu: "1"
        memory: 2Gi
    config:
      CAPublicKey: |
        <paste the exact contents of ca.pub here, indented>
```

Get your Access ID from the auth method you created in Step 4:

```bash
akeyless auth-method-get --name /sra-quickstart/gateway-auth
```

> **Note on exposing SRA to actual users:** the `service.beta.kubernetes.io/aws-load-balancer-internal: "true"`
> annotation above keeps everything private to the VPC — fine for this test, and generally the right
> default. If real users outside the VPC need to reach the SRA SSH proxy, that's a deliberate follow-up
> decision (put it behind a VPN/bastion, or expose only that specific service publicly) — don't flip this
> to public by default.

***

## 8. Step 5 — Install

```bash
helm install sra-quickstart akeyless/akeyless-gateway -n akeyless -f values.yaml
```

Watch until everything is `Running` / `1/1`:

```bash
kubectl get pods -n akeyless -w
```

If a pod is stuck `Pending`: not enough node capacity (check Step 2's checklist). If `CrashLoopBackOff`:

```bash
kubectl logs -n akeyless deploy/sra-quickstart-akeyless-gateway
```

— it will name the misconfigured value (almost always the IRSA role ARN or `gatewayAccessId`).

***

## 9. Step 6 — Confirm the Gateway registered with Akeyless

```bash
kubectl get svc -n akeyless
```

Note the internal NLB hostname for the Gateway service (port 8000). From inside the VPC (or via VPN):

```
http://<internal-NLB-hostname>:8000/console
```

Then check the **Akeyless SaaS console** → Gateways — `sra-quickstart` should show **Active**. If it
doesn't within \~1 minute, the pod has network egress but IAM auth is failing — re-check the IRSA trust
policy's `sub` condition matches `system:serviceaccount:akeyless:akeyless-gateway` exactly.

***

## 10. Step 7 — Register your test target

```bash
akeyless target create ssh \
  --name /sra-quickstart/test-target \
  --host <IP or hostname of your test target> \
  --port 22 \
  --ssh-username <the-ssh-username-on-your-test-target>
```

***

## 11. Step 8 — Prove it actually works end-to-end

```bash
akeyless connect \
  -t "<the-ssh-username-on-your-test-target>@<IP or hostname of your test target>:22" \
  -n /sra-quickstart/ssh-issuer \
  -g <internal-NLB-hostname-for-SRA-SSH-service>:22
```

Run this from somewhere that can reach the internal NLB (a bastion in the VPC, a VPN-connected machine,
or a debug pod like in Step 0). Landing in a real shell on your test target means SRA is genuinely
working end-to-end.

Alternative: browse to `http://<internal-NLB-hostname>:8000/sra/portal`, log in with your Akeyless
console credentials, pick the test target, and open a session there.

***

## 12. Troubleshooting

| Symptom                                                     | Likely cause                                                                                                                    | Fix                                                                            |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Step 0 reports `FAIL` for any `.akeyless.io` host           | Missing NAT/IGW route, security group, or NACL blocking egress on the **worker node's** subnet                                  | Fix the network path — nothing later works until this passes                   |
| Pod `Pending`                                               | Not enough schedulable CPU/memory in the node group                                                                             | Scale the node group or lower `resources.requests`                             |
| Pod `CrashLoopBackOff`                                      | Bad `gatewayAccessId`, malformed `values.yaml`, or unreachable auth endpoint                                                    | `kubectl logs` names the exact failure                                         |
| Gateway pod Running, but console/SaaS shows "Not connected" | IRSA trust policy `sub` doesn't match `namespace:serviceaccount` exactly, or `bound-aws-account-id` on the auth method is wrong | Re-check both against the exact values you used in Steps 2 and 4               |
| `Pending` LoadBalancer with no external IP/hostname         | AWS Load Balancer Controller not installed, or missing IAM permissions for it                                                   | Install/verify the controller (see prerequisites)                              |
| `akeyless connect` fails with a certificate/trust error     | `ca.pub` pasted into `values.yaml` doesn't match the signer key, or `sshd` wasn't restarted on the target                       | Re-export `ca.pub` (Step 3) and confirm the target's `sshd_config` and restart |
| `akeyless connect` "permission denied" for the user         | Username not in `--allowed-users` on the SSH Certificate Issuer                                                                 | Recreate the issuer with the right `--allowed-users`                           |
| Works, then stops after \~5 minutes on a _new_ connection   | SSH cert TTL (`--ttl 300`) expired                                                                                              | Expected — raise `--ttl` on the issuer for longer test sessions                |

***

## What's next

This is still a demo-grade setup (no TLS termination configured on the NLB, single replica everywhere,
no HPA). Once this works:

- Put TLS in front (ACM certificate + ALB, or terminate TLS at the Gateway) — never run this without TLS
  once anything beyond a local test target is involved
- Move real users onto SSO/SAML instead of the CLI's personal login
- Enable session recording/audit per-target in the Akeyless console
- Turn on HPA for the SRA Web/SSH deployments once you know real concurrent session load

<br />
