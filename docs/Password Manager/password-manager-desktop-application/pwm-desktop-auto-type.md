---
title: Auto-Type and Quick Access
---
Browser extensions can only fill web pages. **Auto-Type** fills credentials into *any*
application — a VPN client, a database tool, an RDP window, a terminal — by typing them into
whatever has focus.

Turn it on in **Settings → Auto-Type**.

---

## How it works

1. Focus the application you want to sign in to.
2. Press **Ctrl+Shift+Space**.
3. **Quick Access** opens. Search and pick the login.
4. The credentials are typed into the window that had focus.

The shortcut is global — it works no matter which application is in front, including when the
Akeyless window is hidden.

<Callout icon="ℹ️" theme="info">
  Auto-Type **types** the credentials as keystrokes rather than putting them on the clipboard,
  so nothing is left behind for another application to read.
</Callout>

## Quick Access

The picker that opens on the shortcut. Search behaves like the vault search: it needs at least
**two characters** and waits briefly after you stop typing before querying.

**Open Quick Access** in Settings opens the same picker without the shortcut, which is useful
for checking it works.

## Submit automatically

**Submit automatically with Auto-Type** presses **Enter** after typing the password, so a
sign-in completes without you touching the keyboard again.

Leave it off where a form has more fields after the password, or where a stray Enter would do
something you did not intend.

---

## macOS: Accessibility permission

<Callout icon="⚠️" theme="warn">
  On macOS, Auto-Type **cannot work** until you allow the app under
  **System Settings → Privacy & Security → Accessibility**. Typing into another application is
  exactly what that permission controls.
</Callout>

**Grant Accessibility…** in Settings opens the right pane. After allowing it, restart the app.

## Windows

No extra permission. Some applications running as administrator will not accept synthetic
keystrokes from a non-elevated app — if typing produces no result in one of those applications, this is the reason.

---

## Troubleshooting

| Symptom | Cause |
|---|---|
| Shortcut does nothing | Another app has claimed **Ctrl+Shift+Space** — a common clash with input-method switchers |
| Picker opens, nothing is typed | macOS: Accessibility not granted, or granted before the last update. Re-grant and restart |
| Typed into the wrong window | Focus moved between the shortcut and your pick. Focus the target first, then press the shortcut |
| Characters dropped or reordered | Some remote-desktop and virtualization clients drop fast synthetic input. Try again, or copy from the item instead |
| Form submitted too early | Turn **Submit automatically with Auto-Type** off |

## Related

- [Desktop Settings](https://docs.akeyless.io/docs/pwm-desktop-settings)
