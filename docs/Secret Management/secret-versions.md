---
title: Secrets Versions
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
When updating a [Static Secret](https://docs.akeyless.io/docs/static-secrets) or a [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets) or even a [Target](https://docs.akeyless.io/docs/targets), you can update the current version, create a new version, or roll back to the previous version of a secret (for example, if the most recent version was configured incorrectly, relevant only for Static Secret).

You can globally set each type of those items to store old versions of your secrets by default, enforcing that a new version will be created on any update, simply navigate to the account settings, and enable versions by default with the option to force new versions in case needed.

From the UI, under the **Items** screen, click the settings icon, and toggle the Default versioning option to globally enable and store versions of your [Static Secrets](https://docs.akeyless.io/docs/static-secrets), [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets), and [Targets](https://docs.akeyless.io/docs/targets) items.

You can set the **Maximum** number of older versions that will be stored automatically, from the account settings you can set the global number of maximum versions, whereas, on the item level, you can control explicitly the number of versions that will be stored on the item itself.

> 🚧 Warning
>
> Setting a new **Maximum** number of versions will affect your existing versions of secret.\
> Setting a lower number than your current items versions amount will delete the older versions upon the next version update.

Once a secret has more than one version, a list of all previous values is available within the secret at the bottom of the configurations. Click the arrow to open and close the list and view older versions.
