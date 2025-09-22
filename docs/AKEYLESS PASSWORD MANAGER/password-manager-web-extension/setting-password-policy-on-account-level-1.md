---
title: Setting Password Policy On Account Level
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
### Accessing Secret Generation Policy:

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/dcc11c6-Screenshot_2024-01-10_at_16.43.35.png",
        null,
        null
      ],
      "align": "right",
      "sizing": "200px"
    }
  ]
}
[/block]




Open the Akeyless browser extension.

Navigate to the "Settings" menu on the bottom represented as 3 dots on the upper top part of the screen.

Locate and click on "Password Generation Policy" in the displayed, click on this option.

A Password Generation Policy screen will appear, providing options to configure the secret generation policy.



### Define the Following Parameters:

**Character Length**: Set the desired default length for secrets created within your account.

**Include Uppercase Letters (A-Z):** Check this box to require at least one uppercase letter in the secret. If solely selected, the secret will consist exclusively of uppercase letters.

**Include Lowercase Letters (a-z):** Check this box to ensure at least one lowercase letter is included in the secret. If solely selected, the secret will consist exclusively of lowercase letters.

**Include Numbers (0-9):** Check this box to mandate at least one numeric character in the secret. If solely selected, the secret will consist exclusively of numeric characters.

**Include Special Characters (!@#):** Check this box to ensure at least one special character is included in the secret. If solely selected, the secret will consist exclusively of special characters.

By configuring these settings, you establish a standardized default for secret generation in your organization's account. Users can still modify parameters during secret creation, but the defaults will adhere to the rules you've set.