---
title: AI Agent Auto-fill
---
When an AI browser agent navigates to a sign-in page, the extension can fill the matching vault credential automatically, so the agent is not blocked and you are not asked to paste a password into a chat.

**This setting is off by default.** Turn it on in **Settings → AI agent auto-fill**.

## Supported agents

- Claude in Chrome
- Claude Code / Claude Desktop driving the browser over CDP
- ChatGPT / Codex
- OpenClaw

## Guard rails

Nothing is filled unless **all six** of these hold:

1. You enabled the setting.
2. You are signed in to the extension.
3. The tab carries a fresh agent signal.
4. The page actually looks like a sign-in page.
5. No Launch flow already owns the tab.
6. **Exactly one** vault credential matches the host.

<Callout icon="⚠️" theme="warn">
  The last condition is deliberate. If two or more credentials match the site, the extension fills nothing and leaves the choice to you. An agent is never allowed to pick between your accounts.
</Callout>

## What the agent sees

The credential is written into the page's form fields. The value is not returned to the agent, not printed, and not placed on the clipboard.

## Turning it off

**Settings → AI agent auto-fill**. Turning it off takes effect immediately on all tabs.

## Related

- [Using Autofill / Password Injection](https://docs.akeyless.io/docs/using-autofillpassword-injection-functionality-1)
- [Extension Settings](https://docs.akeyless.io/docs/web-extension-settings)
