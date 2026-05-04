# Secret Leak Response Runbook

This document provides step-by-step guidance for responding to secret/credential leaks detected by the Gitleaks secret scanner.

## Overview

- **Scanner**: gitleaks v8.24.2 (runs on all PRs and pushes to `v1.0`)
- **Rules**: generic-api-key, jwt, private-key, aws-key, gcp-key, and others (see [Gitleaks detect](https://github.com/gitleaks/gitleaks#detect) docs)
- **Sensitivity**: Detects both real credentials and credential-like patterns in examples

## Triage Decision Tree

### Is this a real credential leak?

**YES** → Go to [Real Credential Leak](#real-credential-leak)

**NO (example/placeholder)** → Go to [False Positive / Example](#false-positive--example)

---

## Real Credential Leak

### Immediate Actions

1. **Pause the PR/push** – Do not merge until remediated.
2. **Rotate credentials immediately** – Use your credential management system (Akeyless, AWS IAM, GCP, etc.) to revoke/rotate the exposed secret.
3. **Notify security** – Alert your security team or on-call if the credential was active in production.

### Remediation Steps

1. **Remove the credential** from the documentation:
   - Delete the literal value entirely, OR
   - Replace with a generic placeholder: `<CREDENTIAL_PLACEHOLDER>`, `<API_KEY>`, `<JWT_TOKEN>`, etc.

2. **Verify the fix locally**:
   ```bash
   # Run full-repo scan to confirm no leaks remain
   docker run --rm -v "$PWD:/repo" zricethezav/gitleaks:v8.24.2 dir /repo --redact --no-banner
   ```

3. **Update the PR** – Commit the fix, which will re-trigger the Secret Scan check.

### Example Fixes

**Before** (leaked API key):
```shell
curl -H "Authorization: Bearer <EXPOSED_API_KEY>"
```

**After** (placeholder):
```shell
curl -H "Authorization: Bearer <YOUR_API_KEY>"
```

---

## False Positive / Example

### Assessment

1. **Is this a documented example** (e.g., sample token, mock certificate)?
   - Yes → Go to [Example Placeholder](#example-placeholder)
   - No → Go to [Rule False Positive](#rule-false-positive)

2. **Does the example serve documentation value?**
   - Yes, and it's clearly marked as an example → Go to [Example Placeholder](#example-placeholder)
   - No, remove it → Delete the line/block and recommit.

### Example Placeholder

1. **Replace the literal with a semantic placeholder** that clarifies the expected format:

   | Type | Placeholder |
   |------|-------------|
   | JWT | `<JWT_TOKEN>` or `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...REDACTED` |
   | API Key | `<API_KEY>` |
   | Private Key (PEM) | `<PRIVATE_KEY_PEM_CONTENT>` or `-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----` |
   | AWS Access Key | `AKIA...` with `<ACCOUNT_ID>` mask |
   | GCP Service Account | `sa-name@project.iam.gserviceaccount.com` (service account format is not sensitive; real key is in JSON) |
   | Database Password | `<DB_PASSWORD>` |

2. **Add a comment** explaining the placeholder:
   ```yaml
   # Example: replace <API_KEY> with your actual Akeyless API key
   api_key: <API_KEY>
   ```

3. **Verify the fix** locally (same command as above).

### Rule False Positive

If the gitleaks rule is too broad and is matching non-sensitive text (e.g., documentation references):

1. **Document the false positive** in the PR description.
2. **Consider a gitleaks allowlist exception** (if maintainer approval):
   - Add to `.github/lychee/.lycheeignore` or similar exclusion file (requires security review).
   - OR update the custom rule in `.github/markdownlint/custom-rules.js` to be more specific.
3. **Escalate to security** if the rule needs tuning.

---

## Local Testing Before Push

1. **Run pre-commit hooks** to catch leaks early:
   ```bash
   pre-commit run gitleaks --files <your-modified-file>
   ```

2. **Run full scan** if making extensive changes:
   ```bash
   docker run --rm -v "$PWD:/repo" zricethezav/gitleaks:v8.24.2 dir /repo --redact --no-banner
   ```

3. **Preview changes** before commit:
   ```bash
   git diff HEAD
   ```

---

## Prevention Best Practices

- **Never commit real credentials** to version control, even in private repos.
- **Use placeholders from day one** when writing examples.
- **Use environment variables** in code examples: `${API_KEY}`, `$AKEYLESS_ACCESS_KEY`, etc.
- **Reference credential docs** instead of embedding values:
  > "Set `DATABASE_PASSWORD` environment variable to your production database password."
- **Use CI/CD secrets** for sensitive values in workflows (GitHub Actions `secrets.*`).

---

## Escalation

If you have questions or encounter issues:

1. Check [gitleaks documentation](https://github.com/gitleaks/gitleaks).
2. Review [AKY023 custom rule](../.github/markdownlint/custom-rules.js) for multi-cloud identifier patterns.
3. Open an issue with the `security` label.
4. Contact your security team or on-call.

---

**Last Updated**: 2026-04-29  
**Related Issues**: DOCS-668, DOCS-669
