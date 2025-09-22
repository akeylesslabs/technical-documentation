---
title: GCP Portal Access
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
You can enable secure remote access to GCP Portal on a dedicated static secret that stores the credentials for GCP. 

Users can then access the GCP Portal from the Secure Remote Access Portal without being exposed to your GCP credentials in Isolated mode.

# Prerequisites

To enable secure remote access to the GCP Portal you need:

- A [Static Secret](doc:static-secrets) that specifies the GCP login details, with **Web Access** selected.

- The [Secure Remote Access](https://docs.akeyless.io/docs/remote-access-setup-overview) deployed.

- The [Akeyless Browser Extension](doc:browser-extensions).

- The [Zero Trust Web Access](doc:web-access-bastion).

- The GCP Portal site URL specified in the **values.yaml** file on the Web Access Bastion.

# Set Up Remote Access to GCP Portal from the Akeyless Console

1. Log in to the Akeyless Console and go to **Items**.

2. Create a new static secret and enter the **Value** specifying the GCP portal login details in the following format:`Username..Password` and click Next.

> 📘 Info
> 
> The **Secret** value is a concatenation of your GCP Username and your GCP Password with double dots as a delimiter.

3. On the next screen, tick the box to `Enable Scure Remote Access` and fill in the following fields for the `Web Access` option:

`Injection URL`: The GCP login URL to inject secrets. e.g.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/b0cf7f8-Screenshot_2024-07-08_at_17.13.30.png",
        "Screen Shot 2021-10-25 at 16.05.11.png",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


- `Secure Web Browsing`: Optional, secure web browsing over isolated web browser **available only with** [Zero Trust Web Access](https://docs.akeyless.io/docs/web-access-on-k8s).

**Secure Web Browsing (Isolated)**

All secrets which have **Secure Web Browsing** option enabled are marked with a badge in the Akeyless Secure Remote Access Portal. 

> 👍 Note
> 
> Please make sure that the GCP Portal site URL specified in the **values.yaml** file on the Web Access Bastion.