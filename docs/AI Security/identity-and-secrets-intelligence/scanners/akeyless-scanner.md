---
title: Akeyless  Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
The Akeyless Scanner is a native scanner type that inspects your Akeyless account, discovering the full inventory of identities, roles, and secrets it contains, along with the relationships between them. Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## prerequisite

1. An Akeyless account with the Identity & Secrets Intelligence license
2. A deployed and connected Akeyless Gateway version 4.52.0+
3. A Gateway with AI Insights enabled and properly configured.
4. A user with "Manage ISI Scanners"  or "Admin" Gateway Permission.
5. A user with  "Identity & Secrets Intelligence" administrative rule set to Scoped or All.<br />

## Create a Dynamic AWS Secret in the Akeyless Console<br />

Provider	What it covers
GCP Scanner	Secret findings, enriched with last-access timestamps pulled from Cloud Audit Logs (when available in the environment), plus identity resolution for group-member identities
AWS Scanner	Cloud identities — scans by operating through an AWS Target configured with Gateway Cloud Identity

🟡 NEEDS INPUT — the exact resource types scanned (e.g., does AWS scanning cover IAM users/roles/service accounts/access keys, or identities only? does GCP scanning cover secrets only, or also GCP identities?) isn't spelled out in public docs.

3. Prerequisites
   Feature enabled on the account (ISI is early access — gated per-account).
   Admin-level Console access — the ISI menu only appears for admin-level users.
   RBAC role rule: a role with isi-access set to scoped or all (not none):
   akeyless create-role --name <role-name> --isi-access \<scoped|all>
   For AWS scanning: an AWS Target using Gateway Cloud Identity — meaning a Gateway deployed with an assumable AWS IAM role attached (--use-gw-cloud-identity on target creation).
   For GCP scanning: 🟡 NEEDS INPUT — target/auth setup isn't detailed in public docs (likely a GCP target with a service account, but not confirmed).
   Optional but recommended: Cloud Audit Logs enabled in the target GCP project, for last-access enrichment on secret findings.
4. How to Create a Scanner
   Sign in to the Akeyless Console.
   Open Identity & Secrets Intelligence in the left nav.
   Go to Scanners.
   Create a new scanner, choosing the cloud provider (AWS or GCP).
   Point it at the relevant Target (AWS: must use Gateway Cloud Identity).
   Save, then start the scan from Scanners.
   Track status/history in Scanners; review results in Inventory.

🟡 NEEDS INPUT — exact console field names/screen (scope filters like account/region/project, resource-type toggles, scheduling options) aren't documented publicly; steps above are the confirmed high-level flow only.

Questions to fill the gaps
Gateway — Do you already have a Gateway deployed for this? Is it dedicated to ISI scanning or shared with other Akeyless functions (secrets, SRA, etc.)?
Gateway permissions (AWS) — Beyond the assumable IAM role for Gateway Cloud Identity, what IAM permissions did you grant it for scanning (e.g., read-only IAM list/get actions, CloudTrail/Audit access)?
GCP setup — What target/auth are you using for the GCP scanner (service account? which IAM roles)?
User/role permissions — Who in your org gets isi-access — is it scoped (and if so, scoped to what) or all? Any other role rules involved?
Scan scope — What does the scanner actually scan in your setup — specific accounts/projects, all resources, or a filtered subset?
Anything console-specific — exact button labels, scan scheduling, or scope-filter options you've seen in the actual Scanners screen, so the doc matches reality instead of the high-level docs description.

<br />
