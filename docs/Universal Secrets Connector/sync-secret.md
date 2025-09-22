---
title: Sync Secrets
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
The Akeyless [Universal Secret Connector](https://docs.akeyless.io/docs/universal-secrets-connector) provides a powerful way to ensure that secrets remain synchronized across multiple external secret management solutions. Whenever a secret value is updated in Akeyless, the connector automatically ensures that the updated value is propagated to all integrated systems in real time, eliminating the need for manual synchronization.

# Prerequisites

- Universal Secret Connector Item.

- An [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) with **Read** permission on the the associated USC, and its target.

- An [Authentication Method ](https://docs.akeyless.io/docs/access-and-authentication-methods) with **Read** and **Update** permission on the [Rotated Secret](https://docs.akeyless.io/docs/rotated-secrets) item, and **Read** permission on the associated USC.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/84d68fd1c6e90bb12b48f538b74db51f35ad9c15a90235524268f07b20572d61-Synced_Secret-2.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


This solution makes managing secrets in remote endpoints more efficient and consistent, enabling a secure, centralized approach to secret lifecycle management.