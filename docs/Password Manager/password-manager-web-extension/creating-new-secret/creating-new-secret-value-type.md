---
title: Creating New Secret Value Type
---
A static secret's value is stored in one of two formats. The choice affects how the value is
displayed and how it is copied.

## Plain text

A single free-form value.

Use it for anything consumed as one opaque blob: an API key, a connection string, a licence
key, a block of notes, a certificate body.

The whole value is copied as one unit from the item preview.

## Key / value

A structured set of named fields.

Use it when the secret is really several related values — a host, a port, a username and a
password that belong together.

| Benefit | Detail |
|---|---|
| **Field-level copy** | Each field has its own copy control, so you can take just the password |
| **Copy All** | Copies the whole set at once |
| **Readable preview** | Fields are labelled rather than running together in one string |

## Choosing

| Use | When |
|---|---|
| **Plain text** | One value, consumed as a whole |
| **Key / value** | Several named values, consumed separately |

If you are unsure, ask whether anyone will ever need one part of this secret without the rest.
If yes, use key / value.

## Changing the format later

<Callout icon="⚠️" theme="warn">
  Switching an existing secret between formats **rewrites the value**. Copy anything you need
  before you change it.
</Callout>

Editing is otherwise unrestricted — see
[Editing, Copying & Moving Items](https://docs.akeyless.io/docs/editing-password-details-1).

## Versions

Each save creates a new version, up to the item's **Maximum Versions** limit. Lowering that
limit discards the oldest versions beyond the new value.

## Related

- [Creating New Secret](https://docs.akeyless.io/docs/creating-new-secret)
- [Item Types Reference](https://docs.akeyless.io/docs/web-extension-item-types)
- [Viewing an Item](https://docs.akeyless.io/docs/web-extension-viewing-items)
