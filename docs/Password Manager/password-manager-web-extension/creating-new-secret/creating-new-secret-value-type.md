---
title: Creating New Secret Value Type
---
A static secret's value is stored in one of **three** formats, chosen with the tabs at the top
of the New Secret overlay.

![The three value formats](https://files.readme.io/cfbbfbe5bfcb6053707eba0ee75ae77e41909e70a22e0d64036a43a4c6f4b123-new-secret-overlay.png)
*Text, Key/value and JSON, with the secret Type and Maximum Versions above*

---

## Text

A single free-form value, stored exactly as typed.

Use it for anything consumed as one opaque blob: an API key, a connection string, a license
key, a certificate body, a block of notes.

The whole value copies as one unit from the Item Preview.

## Key/value

A set of named fields, entered as pairs.

Use it when the secret is really several related values — a host, a port, a username and a
password that belong together.

| Benefit | Detail |
|---|---|
| **Field-level copy** | Each field has its own copy control, so you can take just the password |
| **Copy All** | Copies the whole set at once |
| **Readable preview** | Fields are labelled rather than running together |

Key/value is stored as structured data, so it round-trips cleanly to the API and the console.

## JSON

A raw JSON document you type or paste directly.

Use it when the structure is more than flat pairs — nested objects, arrays, a service-account
file — or when something downstream expects a specific JSON shape you need to control exactly.

<Callout icon="ℹ️" theme="info">
  Choosing **JSON** or **Key/value** reveals the value field by default, since structured
  content cannot be edited blind. **Text** keeps it masked until you choose to reveal it.
</Callout>

The editor validates the JSON before saving. An invalid document is reported rather than
stored.

---

## Choosing

| Use | When |
|---|---|
| **Text** | One value, consumed whole |
| **Key/value** | Several named values, consumed separately |
| **JSON** | Nested structure, or a shape something downstream depends on |

If unsure, ask whether anyone will need one part of this secret without the rest. If yes,
Key/value. If the structure is deeper than one level, JSON.

## Secret Type

Above the format tabs, **Type** classifies the secret — **Generic** by default. Select it to
choose a more specific type where one applies. The type affects how the item is presented and
how other Akeyless components interpret it.

## Maximum Versions

How many historical versions the vault keeps, defaulting to **100**. Each save creates a
version; lowering the limit discards the oldest beyond the new value.

## Changing format later

<Callout icon="⚠️" theme="warn">
  Switching an existing secret between formats **rewrites the value**. Copy anything you need
  before changing it.
</Callout>

## Related

- [Creating New Secret](https://docs.akeyless.io/docs/creating-new-secret)
- [Item Types Reference](https://docs.akeyless.io/docs/web-extension-item-types)
- [Viewing an Item](https://docs.akeyless.io/docs/web-extension-viewing-items)
