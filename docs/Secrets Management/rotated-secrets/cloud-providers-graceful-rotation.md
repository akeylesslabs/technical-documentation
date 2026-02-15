---
title: Graceful Rotation
deprecated: false
hidden: false
metadata:
  robots: index
---
For cloud providers (**AWS**, **Azure**, and **GCP**), rotated secrets can be configured with **Graceful Rotation** enabled.

Graceful Rotation keeps the previous credentials valid for a configurable grace period. After the grace period ends, the old credentials are removed from the cloud provider.

Graceful Rotation supports two modes:

* **Before Rotation**: Creates the new credentials `X` days before the scheduled rotation date. The old credentials remain valid until the rotation date, and are removed on that date.

Example of a Rotated Secret that was configured with the following rotation settings:

* **Rotation interval**: `90 days`

* **Graceful Rotation**: `10 days`

  * On day `80`: New credentials are created.

  * Days `80–90`: Both old and new credentials are valid in the cloud provider.

  * On day `90`: Old credentials are removed, only the new credentials remain.

* **After Rotation**: Creates the new credentials on the scheduled rotation date. The old credentials remain valid for `X` more days, and are removed after the grace period ends.

Example of a Rotated Secret that was configured with the following rotation settings:

* **Rotation interval**: `90 days`

* **Graceful Rotation**: `10 days`

  * On day `90`: New credentials are created.

  * Days `90–100`: Both old and new credentials are valid in the cloud provider.

  * On day `100`: Old credentials are removed, only the new credentials remain.

<br />

<br />

<br />

<br />