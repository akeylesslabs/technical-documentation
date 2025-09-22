---
title: PassKey
excerpt: API
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
### Passkey Management Overview

This documentation provides a comprehensive guide to creating, viewing, and managing passkeys within the Akeyless platform. Passkeys enable password-less authentication, which is more secure and user-friendly. The documentation covers the use of both the Akeyless API and CLI for creating and managing passkeys.

<br />

### What is a Passkey?

A Passkey is a cryptographic key designed for password-less authentication, bound to specific user credentials and associated with certain origins (websites). Passkeys simplify secure login workflows and enhance security by eliminating password-based vulnerabilities.

Passkeys in Akeyless can be either regular or personal, depending on the accessibility settings. They also support searchable parameters like the associated website (origin URL) and the username, making them easy to manage and locate within the platform.

### Supported Algorithms for Passkeys

Passkeys only support the following Elliptic Curve (EC) key types:

- EC256
- EC384
- EC512

### Creating a Passkey using the API

To create a passkey via the Akeyless API, follow this structure:

**API Endpoint:**

```shell http
POST http://localhost:8081/create-passkey
```

**Request Payload:**

```shell JSON
{
    "token": "t-...",
    "name": "/testpasskey5",
    "alg": "EC256", // allowed values: [EC256, EC384, EC512]
    "username": "my_username",
    "origin-url": ["http://example.com"],
    "accessibility": "personal" // allowed values: [regular (default), personal]
}
```

### Parameter Descriptions:

- token: The authentication token required to interact with the Akeyless API.
- name: The name of the passkey. You can organize passkeys into folders using / separators in the name.
- alg: The elliptic curve algorithm for the passkey. Allowed values are EC256, EC384, or EC512.
- username: The username associated with the passkey, which will be searchable in the system.
- origin-url: A list of allowed origin URLs (websites) where the passkey can be used. This parameter is searchable.
- accessibility: Determines whether the passkey is for personal or regular use. If not specified, the passkey is classified as regular.