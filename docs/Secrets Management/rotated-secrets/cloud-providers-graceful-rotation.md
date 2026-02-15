---
title: Graceful Rotation
deprecated: false
hidden: false
metadata:
  robots: index
---
For cloud providers (**AWS**, **Azure**, and **GCP**), rotated secrets can be configured with **Graceful Rotation**  mode.

Graceful Rotation keeps the previous credentials valid for a configurable grace period. After the grace period ends, the old credentials are removed from the cloud provider.

Graceful Rotation supports two modes:

* **Before Rotation**: Creates the new credentials `X` days before the scheduled rotation date. The old credentials remain valid until the rotation date, and are removed on that date. This mode shifts the overlap before the rotation date. The new credentials are created ahead of time, and the old credentials are removed on the scheduled rotation date. As a result, at the rotation interval boundary (for example, day 90) you end up with a single active credential version (the new one).

Example of a Rotated Secret that was configured with the following rotation settings:

* **Rotation interval**: `90 days`

* **Graceful Rotation**: `10 days`

  * On day `80`: New credentials are created.

  * Days `80–90`: Both old and new credentials are valid in the cloud provider.

  * On day `90`: Old credentials are removed, only the new credentials remain.

* **After Rotation**: Creates the new credentials on the scheduled rotation date. The old credentials remain valid for `X` more days, and are rotate after the grace period ends. This mode results in an overlap after the rotation date. That means that at the rotation interval boundary (for example, day 90) you will always have two active credential versions the newly created credentials plus the previous credentials that remain valid throughout the grace period, on the grace due date a new version will be created keeping 2 versions in parallel. 

Example of a Rotated Secret that was configured with the following rotation settings:

* **Rotation interval**: `90 days`

* **Graceful Rotation**: `10 days`

  * On day `90`: New credentials are created.

  * Days `90–100`: Both old and new credentials are valid in the cloud provider.

  * On day `100`: Old credentials are rotated, only the new set of credentials remain.

Switching between Graceful Rotation modes (Before ↔ After) resets the rotation state. When you change the mode, Akeyless removes any existing rotated key versions created by the previous mode (including overlapping copies, if present) and re-initializes the secret. Rotation then restarts with a single fresh credential/key version, and subsequent versions are created according to the newly selected mode.

<br />

<br />

<br />
